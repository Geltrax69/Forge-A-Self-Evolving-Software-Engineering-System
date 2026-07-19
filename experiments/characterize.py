"""Characterize the model, not Forge. Find the operating envelope: at what output
size / task type does MiniCPM5-1B break down?

One controlled setup (terse anti-think prompt, temperature 0.4), 10 tasks of
increasing output length. Records for each: did it emit real content or loop into
reasoning, tokens, finish reason. Run: python3 -m experiments.characterize
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experiments.harness import Recorder

MODEL = os.environ.get("FORGE_LLM_MODEL", "minicpm5-1b")
TEMP = float(os.environ.get("FORGE_TEMP", "0.4"))

# terse, anti-reasoning system prompt (the opposite of "think step by step")
SYS = ("Output only the final answer. No reasoning, no explanation, no step-by-step. "
       "If code is asked for, output only the code block. If uncertain, answer UNKNOWN.")

# (label, prompt, max_tokens) — sized to the task so failure is fast
TASKS = [
    ("T01 arithmetic",      "What is 2+2? Answer with the number only. /no_think", 40),
    ("T02 one-line fact",   "What is the canonical Go JWT import path? One line only. /no_think", 60),
    ("T03 hello world Go",  "Write a Go function returning the string \"Hello World\". Code only. /no_think", 150),
    ("T04 json output",     "Output a JSON object with keys name=Forge and lang=Go. JSON only. /no_think", 80),
    ("T05 20-line func",    "Write a Go function that reverses a string. Code only. /no_think", 250),
    ("T06 explain short",   "In 2 sentences, what is SQLC? /no_think", 150),
    ("T07 struct+method",   "Write a Go User struct with ID and Name fields and a String() method. Code only. /no_think", 300),
    ("T08 http handler",    "Write a Go net/http handler that responds 'ok' at GET /health. Code only. /no_think", 350),
    ("T09 patch edit",      "Given `import (\"fmt\")` that needs \"time\" added, output the corrected import block only. /no_think", 120),
    ("T10 login handler",   "Write a Go chi+jwt login handler (~60 lines). Imports: github.com/go-chi/chi/v5, "
                            "github.com/golang-jwt/jwt/v5, net/http, time. Code only. /no_think", 700),
]


def run():
    rec = Recorder(model=MODEL, temperature=TEMP)
    print(f"Characterizing {MODEL} @ temp={TEMP}, terse anti-think prompt\n")
    for label, prompt, mx in TASKS:
        rec.call(label, SYS, prompt, max_tokens=mx, show_input=False)

    # envelope table
    print("\n" + "#" * 72)
    print(f"# OPERATING ENVELOPE — {MODEL} @ temp {TEMP}")
    print("#" * 72)
    print(f"  {'task':18s} {'out':>4s} {'finish':>7s}  {'emitted?':10s}")
    for r in rec.log:
        emitted = "LOOPED" if r["used_reasoning"] else ("CUT" if r["finish"] == "length" else "OK")
        print(f"  {r['label']:18s} {r['output_tokens']:4d} {r['finish']:>7s}  {emitted}")


if __name__ == "__main__":
    run()
