"""Forge execution pipeline — the 'operating system'.

Request -> Intent -> Project Context -> Knowledge Router -> Plan -> Context Build -> LLM.
Each stage is small and observable. The LLM is called only where reasoning is needed;
routing and context loading are plain code (deterministic, no token cost).

ponytail: executor/verifier/reflector are stubs for now — this proves the pipeline
end-to-end against the real model first. Fill them once the plan output is good.
"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from models import inference

PROMPTS = config.PROMPTS


def _prompt(name):
    return (PROMPTS / f"{name}.md").read_text()


# --- Stage 1: Intent -------------------------------------------------------
def analyze_intent(request):
    raw = inference.ask(_prompt("intent"), request, temperature=0, max_tokens=2000)
    m = re.search(r"\{.*\}", raw, re.S)  # model may wrap JSON in stray text
    try:
        return json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        return {"goal": request, "keywords": [], "_parse_failed": True}


# --- Stage 2: Project Context ----------------------------------------------
def load_project():
    f = config.ROOT / "knowledge" / "frameworks.json"
    return json.loads(f.read_text()) if f.stat().st_size else {}


# --- Stage 3: Knowledge Router (deterministic, no LLM) ---------------------
def route_docs(request, intent, project):
    terms = set(re.findall(r"[a-z0-9]+", request.lower()))
    terms |= {str(k).lower() for k in intent.get("keywords", [])}
    terms |= {str(v).lower() for v in project.values()}
    folders = []
    for kw, paths in config.ROUTES.items():
        if kw in terms:
            for p in paths:
                if p not in folders:
                    folders.append(p)
    return folders


def build_context(folders, max_files_per_folder=2, max_chars=1400):
    """Load a couple of the smallest doc files per routed folder (intro/overview first)."""
    chunks = []
    for folder in folders:
        d = config.DOCS / folder
        if not d.is_dir():
            continue
        files = sorted(d.glob("*.md"), key=lambda p: (not p.name.startswith("000"), p.name))
        for f in files[:max_files_per_folder]:
            text = f.read_text(errors="replace")[:max_chars]
            chunks.append(f"### {folder}/{f.name}\n{text}")
    return "\n\n".join(chunks)


# --- Stage 4: Planner ------------------------------------------------------
def make_plan(request, project, folders):
    ctx = (f"USER REQUEST: {request}\n"
           f"PROJECT STACK: {json.dumps(project)}\n"
           f"AVAILABLE DOCS: {', '.join(folders) or 'none matched'}")
    return inference.chat(
        [{"role": "system", "content": _prompt("system") + "\n\n" + _prompt("planner")},
         {"role": "user", "content": ctx}],
        temperature=0.2, max_tokens=2500, model=config.STAGE_MODELS["planner"])


# --- Orchestrator ----------------------------------------------------------
def run(request):
    print(f"\n{'='*60}\nREQUEST: {request}\n{'='*60}")

    intent = analyze_intent(request)
    print("\n[1] INTENT\n" + json.dumps(intent, indent=2))

    project = load_project()
    print("\n[2] PROJECT STACK\n" + json.dumps(project, indent=2))

    folders = route_docs(request, intent, project)
    print("\n[3] KNOWLEDGE ROUTER -> " + (", ".join(folders) or "(no match)"))

    context = build_context(folders)
    print(f"\n[4] CONTEXT BUILT: {len(context)} chars from {len(folders)} folder(s)")

    plan = make_plan(request, project, folders)
    print("\n[5] PLAN\n" + plan)
    print(f"\n{'='*60}\n(executor/verifier/reflector: not yet implemented)\n")
    return {"intent": intent, "project": project, "folders": folders, "plan": plan}


if __name__ == "__main__":
    req = " ".join(sys.argv[1:]) or "Build a Go login backend with JWT"
    run(req)
