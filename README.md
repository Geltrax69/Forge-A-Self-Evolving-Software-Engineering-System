# Forge — A Self-Evolving Software Engineering System

Forge is a **local** AI software engineer. A small model (MiniCPM5-1B, running in LM
Studio) acts as a reasoning engine, not an oracle. Instead of guessing, Forge checks
its project graph, reads only the documentation connected to the task, writes code,
runs it, reads the errors, and fixes them — and stores what it learns outside the model.

> **Design rule:** everything the model learns is stored *outside* the model.
> The LLM is interchangeable (MiniCPM today, Qwen/Gemma/Llama tomorrow). The graph,
> the docs, the history, and the lessons are files that any future model can read.

```
User → Intent → Query Engine → Project Graph → Context Builder → LLM → Executor → Verifier → Graph Updater
```

There is **no hand-written planner and no keyword search**. Context comes from
traversing a graph of the project. The graph *is* the planner.

---

## Why it's built this way

An agent is not `LLM + tools`. It's a state machine with memory. The model is only
the CPU. So Forge is split into replaceable parts:

| Part | Role | Status |
|------|------|--------|
| Project Graph | the file system of knowledge (features, files, docs, bugs, tests) | ✅ working |
| Query Engine | answers "what does this feature need?" by traversal | ✅ working |
| Context Builder | turns a graph query into a prompt (no search) | ✅ working |
| Model Interface | OpenAI-compatible client, per-brain model routing | ✅ working |
| Executor | write files, run commands | 🔜 stub |
| Verifier | `go build` / `go test`, feed errors back | 🔜 stub |
| Graph Updater | write verified results + lessons back to the graph | 🔜 planned |

---

## The Project Graph (the foundation)

Everything is a node; relationships are typed edges. Full schema in
[`graph/schema.py`](graph/schema.py).

**Node types:** Feature · Task · Component · File · Documentation · Example · Bug ·
Decision · Test · Tool · Framework

**Edge types:** `REQUIRES` · `IMPLEMENTED_BY` · `DOCUMENTED_BY` · `HAS_EXAMPLE` ·
`VERIFIED_BY` · `DEPENDS_ON` · `CAUSED_BY` · `FIXED_BY` · `USES`

The five queries the graph must answer cleanly:

```
Q1  What docs are needed for feature X?   X -REQUIRES-> F -DOCUMENTED_BY-> Doc
Q2  Which files implement X?              X -IMPLEMENTED_BY-> File
Q3  What breaks if I change Redis?        *reverse* DEPENDS_ON -> Redis
Q4  Have I solved a similar bug before?   Bug nodes matching keywords
Q5  What tests verify X?                  X -VERIFIED_BY-> Test
```

---

## Repository layout

```
forge/
├── app.py                # entry point
├── config.py             # endpoint, model routing, doc routes
│
├── graph/                # ✅ the Project Graph
│   ├── schema.py         #   node/edge types, the 5 queries
│   ├── graph.py          #   engine: add / link / traverse / query
│   └── seed.py           #   the Login example (16 nodes, 14 edges)
│
├── context/
│   └── builder.py        # ✅ graph query -> prompt
│
├── models/
│   ├── inference.py      # ✅ OpenAI-compatible client (LM Studio / Ollama)
│   └── prompts/          #   one prompt per "brain": system, intent, planner, coder
│
├── planner/
│   └── pipeline.py       # first pipeline (intent→route→context→plan), pre-graph
│
├── docs/                 # ✅ official docs, chunked per topic for retrieval
│   ├── frontend/  (NextJS 46, React 594, TailwindCSS 42, TypeScript 23, Design/)
│   ├── backend/   (Go, Chi, SQLC)
│   ├── database/  (PostgreSQL)   cache/ (Redis)   objectstorage/ (S3)
│   ├── auth/      (JWT, OAuth)    deployment/ (Docker 896, Nginx)
│   └── frontend/Design/          (impeccable + taste-skill UI design packs)
│
├── knowledge/            # frameworks.json — the declared stack
├── memory/               # experience / history / project_graph / architecture
├── tools/  examples/  project/  index/  workspace/  logs/  tests/
```

The docs are split into ~1,700 single-topic markdown files (one page each) so they
embed cleanly for semantic search instead of being one 800-page blob.

---

## Current stage

**Stage 1 — Foundation (in progress).** The graph → context → model loop runs
end-to-end against the real model. Proven on the Login example:

- The graph fed the model a **past bug** (`Bearer prefix missing`) as context, and the
  model fixed it unprompted — the learning loop works in principle.
- **Per-brain model routing** matters: the 1B model *loops* on planning (burns 2,500
  tokens producing nothing), while an 8B produces a clean plan in ~260 tokens. Cheap
  mechanical stages stay on the small model; reasoning stages use a bigger one.

**Known gaps:**
- Executor / Verifier are stubs — code is generated but not yet run and fed back.
- Grounding depth: the context builder pulls a folder's first doc file, which can be
  thin; it should select the *code-bearing* chunk so the model stops inventing
  library names.
- Graph is seeded by hand; automatic project scanning + graph updates come next.

**Stage 2 — Learning (next):** executor + verifier, automatic graph updates,
experience nodes, architecture extraction.

---

## Running it

Point at any OpenAI-compatible server (LM Studio default: `http://127.0.0.1:1234/v1`).

```bash
# seed the graph and run the 5 queries
python3 -m graph.seed

# build context for a feature from the graph
python3 -m context.builder

# the earlier keyword pipeline (pre-graph)
python3 app.py "Build a Go login backend with JWT"
```

Swap the model without touching code:

```bash
export FORGE_LLM_MODEL="dolphin-x1-8b"      # or qwen2.5-coder, etc.
export FORGE_LLM_URL="http://localhost:11434/v1"   # Ollama, etc.
```

---

*The LLM is interchangeable. The pipeline is what makes Forge unique.*
