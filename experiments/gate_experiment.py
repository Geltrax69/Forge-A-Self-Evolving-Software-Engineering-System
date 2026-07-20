"""Confidence-gated answering. The test: does Forge make the 1B say "I don't know"
instead of inventing, when evidence is thin or absent?

Three questions by design:
  Q1 JWT sign      -> verified package (conf 1.0)  -> answer FROM evidence
  Q2 Kafka EOS     -> no evidence     (conf 0.1)   -> gate REFUSES, model never called
  Q3 Redis Streams -> docs only       (conf 0.5)   -> passes gate, but does the doc
                      actually cover streams? watch if the model refuses or invents.

Run: python3 -m experiments.gate_experiment
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experiments.harness import Recorder
from agent.confidence import decision
from knowledge.packages import render
import config

# The rule that forbids invention:
SYS = ("Answer ONLY using the EVIDENCE provided. If the evidence does not contain "
       "the answer, reply with exactly: I DON'T KNOW. Never use knowledge outside the "
       "evidence. Never invent package names, functions, or APIs.")


def evidence_text(d):
    parts = []
    if d["package_keys"]:
        parts.append(render(*d["package_keys"]))
    for s in d["sources"]:
        if s.startswith("docs:"):
            folder = config.DOCS / s.split("docs:")[1]
            files = sorted(folder.glob("*.md"))
            if files:
                parts.append(f"[{s}]\n" + files[0].read_text(errors="replace")[:900])
    return "\n\n".join(parts)


def run():
    rec = Recorder(model=config.LLM_MODEL, temperature=0.4)
    questions = [
        "How do I sign a JWT in Go?",
        "How do I configure Kafka exactly-once semantics in Go?",
        "How do I use Redis Streams consumer groups in Go?",
    ]
    for q in questions:
        d = decision(q)
        print("\n" + "=" * 72)
        print(f"Q: {q}")
        print(f"   confidence={d['confidence']:.2f}  answerable={d['answerable']}")
        print(f"   sources: {d['sources'] or 'NONE'}")
        if not d["answerable"]:
            print("   → GATE REFUSED (below threshold). Model NOT called. Forge says: I DON'T KNOW.")
            print("   → tokens spent: 0")
            continue
        ev = evidence_text(d)
        rec.call(f"gated answer", SYS, f"EVIDENCE:\n{ev}\n\nQUESTION: {q}",
                 max_tokens=700, show_input=False)


if __name__ == "__main__":
    run()
