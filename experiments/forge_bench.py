"""Benchmark FORGE (not the model): run real tasks end-to-end and record the
empirical table — ambiguity vs reasoning/answer tokens vs compile success.

Pipeline per task: evidence -> generate -> extract FIRST code block (deterministic,
we don't fight the trailing-prose problem with prompts) -> go build -> patch loop.

Run: python3 -m experiments.forge_bench
"""
import os, sys, time, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experiments.harness import Recorder, go_build
from knowledge.packages import render

MODEL = os.environ.get("FORGE_LLM_MODEL", "minicpm5-1b")
SYS = ("Output only the final answer. No reasoning, no explanation. Output one Go "
       "code block only. Use ONLY imports/functions in the CONTEXT if one is given.")

STDLIB = ()
CHI = ("github.com/go-chi/chi/v5",)
JWT = ("github.com/golang-jwt/jwt/v5",)

# (id, ambiguity 0-10, evidence_keys, deps, prompt)
TASKS = [
    ("reverse-string", 1, [], STDLIB,
     "Write a Go function reverseString(s string) string. One code block."),
    ("health-endpoint", 2, [], STDLIB,
     "Write a complete Go program: net/http server with GET /health returning \"ok\". One code block."),
    ("user-struct", 2, [], STDLIB,
     "Write a complete Go program with a User struct (ID int, Name string) and a "
     "String() string method using fmt.Sprintf. One code block."),
    ("jwt-sign", 4, ["jwt-go"], JWT,
     "Write a complete Go program with a function that signs a JWT for a userID using "
     "the CONTEXT's package. One code block."),
    ("chi-route", 4, ["chi-go"], CHI,
     "Write a complete Go program: a chi router with one GET /ping route returning \"pong\". "
     "One code block."),
    ("patch-import", 8, [], STDLIB,   # deliberately ambiguous (the failure case)
     "Add \"time\" to this Go file and output the whole corrected file:\n"
     "package main\nimport (\n    \"fmt\"\n)\nfunc main(){ fmt.Println(\"x\") }"),
]


def first_code_block(text):
    """Deterministic: first fenced code block, lang tag stripped. Falls back to the
    text from the first `package ` line if the model never fenced (odd fence counts)."""
    m = re.search(r"```(?:go|golang)?\s*\n(.*?)```", text, re.S)
    if m:
        return m.group(1).strip()
    # no closed fence — salvage from 'package ' onward
    p = text.find("package ")
    return text[p:].strip() if p != -1 else text.strip()


def run():
    rec = Recorder(model=MODEL, temperature=0.4)
    rows = []
    for tid, amb, ev, deps, prompt in TASKS:
        ctx = ("CONTEXT:\n" + render(*ev) + "\n\n") if ev else ""
        ev_tokens = 0
        t0 = time.time()
        r = rec.call(f"{tid} (amb {amb})", SYS, ctx + prompt, max_tokens=900, show_input=False)
        ev_tokens = r["prompt_tokens"]
        code = first_code_block(r["answer"])

        passes, patches, ok, errors = 0, 0, False, ""
        for attempt in range(3):
            passes += 1
            ok, errors = go_build(code, deps=deps or ("github.com/go-chi/chi/v5",))
            if ok:
                break
            patches += 1
            pr = rec.call(f"{tid} patch#{patches}", SYS,
                          f"Fix ONLY the build errors. Return the whole corrected file, one code block.\n"
                          f"```go\n{code}\n```\nERRORS:\n{errors}", max_tokens=900, show_input=False)
            code = first_code_block(pr["answer"])
        secs = round(time.time() - t0, 1)
        rows.append((tid, amb, ev_tokens, r["reasoning_tokens"], r["answer_tokens"],
                     passes, patches, "YES" if ok else "NO", secs))

    print("\n" + "#" * 96)
    print(f"# FORGE BENCHMARK — {MODEL}")
    print("#" * 96)
    print(f"  {'task':16s} {'amb':>3s} {'evid':>5s} {'reason':>6s} {'answer':>6s} "
          f"{'builds':>6s} {'patch':>5s} {'ok':>3s} {'sec':>5s}")
    for t, a, e, rt, at, p, pt, ok, s in rows:
        print(f"  {t:16s} {a:3d} {e:5d} {rt:6d} {at:6d} {p:6d} {pt:5d} {ok:>3s} {s:5.1f}")


if __name__ == "__main__":
    run()
