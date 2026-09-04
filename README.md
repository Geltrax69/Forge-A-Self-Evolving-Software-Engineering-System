# Forge

**A local AI software engineer built on a 1B model — where the intelligence lives in the system, not the weights.**

Forge runs MiniCPM5-1B locally (LM Studio). A 1B model can't hold knowledge and
hallucinates when asked to. So Forge doesn't ask it to. Knowledge lives in files —
a graph, docs, verified packages, past bugs. The model is a small reasoning step in
the middle of a pipeline that checks its work.

> **Design rule:** everything learned is stored *outside* the model.
> MiniCPM today, Qwen or Llama tomorrow — the graph, the docs, and the lessons are
> files any future model can read.

---

## The two questions this project is asking

> **1. Why do we train LLMs to *hold* all the knowledge?**
> A search engine never memorized the web — it indexed it and retrieved on demand.
> Docs, code and the internet already exist as text. Why bake them into weights?
>
> **2. What if the model isn't the knowledge at all?**
> Just a small one, low hallucination, used for one narrow job: judging whether a
> retrieved answer is correct. Then build the code and the answers *around* it —
> in files, not in weights.

Forge is my attempt to actually build the second one and find out where it breaks.

---

## The idea

We train models to *memorize* the world. Search engines never did — they indexed it
and retrieved on demand. Forge asks whether the same split works for code generation:

- **retrieval** decides *what is true* → files, docs, a graph
- **the model** decides *how to phrase it* → one small, replaceable component
- **compilers and tests** decide *whether it's correct* → deterministic, no tokens

The model is never the source of truth. It's asked one narrow question at a time,
with evidence attached, and everything it produces is verified by software.

---

## How it works

```
question
   ↓
[1] confidence gate      is there verified evidence?  no → "I don't know" (0 tokens)
   ↓
[2] project graph        traverse to what this feature actually needs
   ↓
[3] context builder      build the prompt from ONLY those nodes — no search
   ↓
[4] model (1B)           generate one function, with evidence in context
   ↓
[5] verifier             goimports → go build; mechanical errors fixed in software
   ↓
[6] graph update         write the verified result and the lesson back   (planned)
```

**[1] Confidence gate** — [`agent/confidence.py`](agent/confidence.py)
Scores a question before the model is ever called: verified knowledge package → `1.0`,
matching docs → `0.5`, nothing → `0.1`. Below `0.5` Forge refuses outright.
Generic words (`go`, `auth`, `cache`) are stripped, so "Kafka in Go" can't score just
because *go* matched the Go docs — it refuses at zero tokens.

**[2] Project graph** — [`graph/`](graph/)
Features, files, docs, bugs, decisions and tests are nodes; relationships are typed
edges (`REQUIRES`, `DOCUMENTED_BY`, `CAUSED_BY`, `FIXED_BY`, `VERIFIED_BY`, …).
"What does this feature need?" is a traversal, not a keyword search.
**There is no hand-written planner — the graph is the planner.**

**[3] Context builder** — [`context/builder.py`](context/builder.py)
Turns one traversal into one prompt. The model receives exactly the docs, examples,
files and past bugs connected to the feature. It never searches.

**[4] The model** — kept inside its measured limits (see below): one function at a
time, evidence in context, never a whole file at once.

**[5] Verifier** — [`agent/verifier.py`](agent/verifier.py)
`goimports` fixes imports, package clause and formatting deterministically. Then
`go build`. `best_code_block()` compiles *every* fenced block and keeps the one that
builds. Surviving errors are classified `MECHANICAL` / `SEMANTIC` / `ARCHITECTURAL` —
only semantic ones (wrong API, wrong type) go back to the model.

---

## What's measured

Not claims — numbers from [`experiments/`](experiments/), all on `minicpm5-1b`.

**The model's operating envelope** (`characterize.py`, 10 tasks)
- It always reasons before answering; `/no_think` is ignored. Reasoning can't be turned off.
- Most apparent "loops" were **token starvation** — a tight `max_tokens` cut it off
  mid-reasoning. Budget ≥250–300 tokens even for a one-word answer.
- Reliable up to **~1 function / ~30 lines / ~250 output tokens**. Genuine looping
  starts around a 60-line one-shot file.
- Without evidence it invents package names (`gorilla-jwt`). With evidence it doesn't.
- `temperature 0` loops worse than `0.4`.

**Deterministic-first repair** (`forge_bench.py` → `forge_bench2.py`, 6 tasks)
- v1: 2/6. The bottleneck was **the patch loop, not generation** — the model wrote
  correct code, then destroyed it during repair (repeating verbatim, dropping
  `package main`, never fixing imports).
- v2 with `goimports` first: **3–4/6, ~5× faster (1.5–9s vs 42–66s), zero tokens
  spent on mechanically-fixable errors.**
- Remaining failures are generation quality, not repair.

**The gate** (`gate_experiment.py`, 3 questions)
- JWT (verified package) → grounded answer, correct `golang-jwt/jwt/v5` APIs.
- Kafka (no evidence) → refused by the gate, model never called.
- Redis Streams (docs don't cover it) → model itself replied **"I DON'T KNOW"**.
- The same model that previously invented `gorilla-jwt` and `go-chi/jwts` now refuses.

**Learning loop, in principle:** the graph fed the model a past bug node
(`Bearer prefix missing`) as context, and the model fixed it unprompted.

**Model routing:** the 1B loops on planning (2,500 tokens, nothing produced); an 8B
plans in ~260. Mechanical stages stay small, reasoning stages go bigger.

---

## Flaws and open gaps

Stated plainly, because the honest version is more useful than the demo version.

- **The learning loop isn't closed.** The verifier runs, but results and lessons are
  not yet written back to the graph automatically. Forge doesn't get smarter between runs yet.
- **The graph is hand-seeded.** 16 nodes, 14 edges, one Login example. No automatic
  project scanning.
- **Context depth is thin.** The builder takes a folder's *first* doc file, which is
  often an intro. It should select the code-bearing chunk — this is why the model
  still occasionally invents an API on `0.5`-confidence questions.
- **N=6, single run, is too noisy for a pass rate.** The structural wins (speed,
  mechanical rescue) are stable; the pass rate needs a larger suite.
- **Compile-pass ≠ task-correct.** One "passing" task had ignored the instruction —
  the original already compiled. The success metric is still too weak.
- **The grounded answer path rambles** into `reasoning_content` and can hit
  `max_tokens`; it needs the reasoning budget and extraction that codegen already has.
- **Several modules are still empty files** — `agent/planner.py`, `executor.py`,
  `reflector.py`, `state.py`, and most of `tools/`.
- **Go only.** Every deterministic stage assumes `goimports` and `go build`.

---

## Layout

```
forge/
├── app.py                 entry point
├── config.py              endpoint, model routing, doc routes
│
├── agent/
│   ├── confidence.py      ✅ the gate — answer or refuse
│   ├── verifier.py        ✅ goimports → go build, error classifier
│   └── planner/executor/reflector/state.py    ⬜ empty
│
├── graph/                 ✅ nodes, typed edges, traversal, Login seed
├── context/builder.py     ✅ graph query → prompt
├── knowledge/packages.py  ✅ verified, hand-checked API facts
├── experiments/           ✅ the benchmarks behind every number above
│
├── models/                OpenAI-compatible client + one prompt per "brain"
├── docs/                  ~1,700 single-topic markdown files (Go, Chi, SQLC,
│                          Postgres, Redis, JWT, OAuth, Next.js, React, Docker…)
├── memory/                experience · history · architecture · project_graph
└── tools/                 ⬜ mostly empty
```

Docs are split one page per file so they retrieve cleanly, instead of being one
800-page blob.

---

## Running it

Any OpenAI-compatible server works (LM Studio default: `http://127.0.0.1:1234/v1`).

```bash
python3 -m graph.seed              # seed the graph, run the 5 traversal queries
python3 -m context.builder         # build a feature's prompt from the graph
python3 -m agent.confidence        # score three questions through the gate
python3 -m agent.verifier          # self-check: goimports rescues a missing import
python3 app.py "Build a Go login backend with JWT"
```

Swap the model without touching code:

```bash
export FORGE_LLM_MODEL="dolphin-x1-8b"
export FORGE_LLM_URL="http://localhost:11434/v1"
```

---

## Status

**Stage 1 — Foundation.** Gate, graph, context builder and verifier work end-to-end
against the real model.

**Stage 2 — Learning (next).** Close the loop: executor, automatic graph updates,
experience nodes, architecture extraction. That's the step that turns a grounded
pipeline into a system that improves.

*The LLM is interchangeable. The pipeline is what makes Forge Forge.*

---

**Am I missing why this doesn't work at scale?** Genuinely asking — open an issue.
The measurements above are what I have; the flaws section is what I know is broken.
