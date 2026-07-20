"""Forge benchmark v2 — deterministic-first pipeline. Same 6 tasks as v1, so the
delta is measurable (one big variable: software handles mechanical fixes).

Per task:  generate -> best_code_block (goimports + compile every block, keep the
one that builds) -> if still broken AND error is SEMANTIC, ONE model micro-patch.
The model is out of the import/format/package business entirely.

Run: python3 -m experiments.forge_bench2
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experiments.harness import Recorder
from agent.verifier import best_code_block, verify, classify, all_code_blocks
from knowledge.packages import render

MODEL = os.environ.get("FORGE_LLM_MODEL", "minicpm5-1b")
SYS = ("Output only the final answer. One Go code block only. Use ONLY "
       "imports/functions in the CONTEXT if one is given.")

STDLIB, CHI, JWT = (), ("github.com/go-chi/chi/v5",), ("github.com/golang-jwt/jwt/v5",)
TASKS = [
    ("reverse-string", 1, [], STDLIB, "Write a Go function reverseString(s string) string. One code block."),
    ("health-endpoint", 2, [], STDLIB, "Write a complete Go program: net/http server with GET /health returning \"ok\"."),
    ("user-struct", 2, [], STDLIB, "Write a complete Go program with a User struct (ID int, Name string) and a String() method."),
    ("jwt-sign", 4, ["jwt-go"], JWT, "Write a complete Go program with a function that signs a JWT for a userID using the CONTEXT's package."),
    ("chi-route", 4, ["chi-go"], CHI, "Write a complete Go program: a chi router with one GET /ping route returning \"pong\"."),
    ("patch-import", 8, [], STDLIB, "Add \"time\" to this file, output the whole corrected file:\npackage main\nimport (\n    \"fmt\"\n)\nfunc main(){ fmt.Println(\"x\") }"),
]


def run():
    rec = Recorder(model=MODEL, temperature=0.4)
    rows = []
    for tid, amb, ev, deps, prompt in TASKS:
        ctx = ("CONTEXT:\n" + render(*ev) + "\n\n") if ev else ""
        t0 = time.time()
        g = rec.call(f"{tid} (amb {amb})", SYS, ctx + prompt, max_tokens=1400, show_input=False)

        # deterministic first: mechanical fixes + best compiling block. Zero model tokens.
        code, ok, errors = best_code_block(g["answer"], deps)
        route = "mechanical" if ok else classify(errors)
        patches = 0

        # only reach for the model if the leftover error is SEMANTIC
        if not ok and route == "SEMANTIC":
            patches = 1
            pr = rec.call(f"{tid} semantic-patch", SYS,
                          f"Fix ONLY this compiler error. Return the whole file, one code block.\n"
                          f"```go\n{code}\n```\nERROR:\n{errors}", max_tokens=900, show_input=False)
            code, ok, errors = best_code_block(pr["answer"], deps)

        rows.append((tid, amb, g["reasoning_tokens"], g["answer_tokens"], route,
                     patches, "YES" if ok else "NO", round(time.time() - t0, 1)))

    print("\n" + "#" * 92)
    print(f"# FORGE BENCHMARK v2 (deterministic-first) — {MODEL}")
    print("#" * 92)
    print(f"  {'task':16s} {'amb':>3s} {'reason':>6s} {'answer':>6s} {'route':>11s} {'patch':>5s} {'ok':>3s} {'sec':>5s}")
    npass = 0
    for t, a, rt, at, route, pt, ok, s in rows:
        npass += ok == "YES"
        print(f"  {t:16s} {a:3d} {rt:6d} {at:6d} {route:>11s} {pt:5d} {ok:>3s} {s:5.1f}")
    print(f"\n  PASS: {npass}/{len(rows)}   (v1 was 2/6)")


if __name__ == "__main__":
    run()
