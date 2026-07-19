"""Experiment: evidence + cheap probe + generate + verify + auto-repair loop.

Run: python3 -m experiments.login_experiment
Prints every input/output/token count, then the deterministic build verdicts and
the patch loop. This is the reusable recorder — you just read the printout.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experiments.harness import Recorder, go_build, extract_code
from knowledge.packages import render

MODEL = os.environ.get("FORGE_LLM_MODEL", "dolphin-x1-8b")
EVIDENCE = render("jwt-go", "chi-go")

STRICT = ("You MUST ONLY use imports, functions, types and packages explicitly "
          "provided in the CONTEXT. Include EVERY import listed under OFFICIAL IMPORTS "
          "and ALSO REQUIRES. Never use anything under NEVER USE. If a required API is "
          "missing from the context, reply NEED_MORE_CONTEXT instead of inventing one.\n\n"
          "CONTEXT:\n" + EVIDENCE)


def run():
    rec = Recorder(model=MODEL)

    # Phase 3 — cheap probe before spending tokens on generation
    p = rec.call("PROBE: which JWT package?",
                 STRICT + "\nAnswer with the import path ONLY.",
                 "What Go JWT package should be used?", max_tokens=30)
    if "golang-jwt/jwt/v5" not in p["answer"]:
        print("\n✗ PROBE FAILED — context insufficient, stopping before generation.")
        rec.summary(); return
    print("\n✓ Probe passed — canonical package confirmed. Proceeding to generate.")

    # Generate
    g = rec.call("GENERATE: login handler",
                 STRICT + "\nGenerate a complete, COMPILABLE Go file for a login handler. "
                 "Output one ```go block only.",
                 "Generate a login handler for the Login feature.", max_tokens=900)
    code = extract_code(g["answer"])

    # Phase 4/5/6 — deterministic verify + auto-repair loop (patch, don't regenerate)
    for attempt in range(1, 4):
        ok, errors = go_build(code)
        print(f"\n── go build (attempt {attempt}): {'PASS ✓' if ok else 'FAIL ✗'}")
        if ok:
            print("── VERIFIED CODE ACCEPTED ──")
            break
        print(errors)
        # feed ONLY the compiler errors back — patch, not regenerate
        r = rec.call(f"PATCH #{attempt} (compiler errors only)",
                     "You are a Go compiler-error fixer. You are given code and its go build "
                     "errors. Return the FULL corrected file as one ```go block. Fix ONLY what "
                     "the errors demand (usually missing imports). Change nothing else.",
                     f"CODE:\n```go\n{code}\n```\n\nBUILD ERRORS:\n{errors}",
                     max_tokens=900, show_input=False)
        code = extract_code(r["answer"])
    else:
        print("\n✗ Still failing after 3 patches — would return nothing (Phase 7 confidence gate).")

    rec.summary()


if __name__ == "__main__":
    run()
