"""Confidence gate — the core of Forge's reliability.

The intelligence isn't that the 1B knows everything. It's that Forge knows when
there IS enough verified evidence to answer, and when there isn't. Below the
threshold, Forge does not let the model guess — it returns "I don't know" (or,
later, triggers a search).

Evidence sources, in the order the vision prescribes:
  1. knowledge packages (verified, confidence 1.0)   -> strongest
  2. docs folders that exist for the topic            -> medium
  3. nothing                                          -> refuse
"""
import re
import config
from knowledge.packages import PACKAGES


def _keywords(q):
    return set(re.findall(r"[a-z0-9]+", q.lower()))


def assess(question):
    """Return (confidence 0..1, matched_package_keys, sources[])."""
    kw = _keywords(question)
    sources, pkg_keys = [], []

    # 1. verified knowledge packages — match on CONCEPT only, not language.
    # (matching on "go" would make every Go package fire on any Go question.)
    for key, p in PACKAGES.items():
        tokens = _keywords(key.replace("-go", "") + " " + p["concept"])
        if kw & tokens and p.get("verified"):
            pkg_keys.append(key)
            sources.append(f"package:{key} (conf {p['confidence']/100:.2f})")

    # 2. docs folders routed by keyword — but a GENERIC term (the language, umbrella
    # words) is not evidence for a specific concept. "How to configure Kafka in Go?"
    # must not score just because "go" matched the Go docs. Only specific terms count.
    GENERIC = {"go", "golang", "code", "function", "frontend", "backend", "database",
               "auth", "cache", "query", "router", "proxy", "storage", "design", "ui", "css"}
    doc_hits = {d for k, paths in config.ROUTES.items()
                if k in kw and k not in GENERIC for d in paths}
    for d in sorted(doc_hits):
        if (config.DOCS / d).is_dir():
            sources.append(f"docs:{d}")

    # score: a verified package is decisive; docs alone are partial; nothing = refuse
    if pkg_keys:
        conf = 1.0
    elif doc_hits:
        conf = 0.5
    else:
        conf = 0.1
    return conf, pkg_keys, sources


THRESHOLD = 0.5  # below this, do not let the model answer


def decision(question):
    conf, keys, sources = assess(question)
    return {"confidence": conf, "answerable": conf >= THRESHOLD,
            "package_keys": keys, "sources": sources}


if __name__ == "__main__":
    for q in ["How do I sign a JWT in Go?",
              "How do I use Redis Streams consumer groups in Go?",
              "What Chi function registers a route?"]:
        d = decision(q)
        print(f"{d['confidence']:.2f}  answerable={d['answerable']}  {q}")
        print(f"      sources: {d['sources'] or 'NONE'}")
