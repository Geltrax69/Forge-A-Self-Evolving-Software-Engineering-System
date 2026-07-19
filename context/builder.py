"""Context Builder — turns a graph query into a prompt. MiniCPM never searches;
it receives exactly the docs/examples/files/bugs connected to the feature."""
from graph.graph import Graph
import config


def _read_doc(path, limit=1200):
    """Read the intro of a routed docs/ folder (or a file)."""
    p = config.DOCS / path
    if p.is_dir():
        files = sorted(p.glob("*.md"), key=lambda f: (not f.name.startswith("000"), f.name))
        return files[0].read_text(errors="replace")[:limit] if files else ""
    if p.is_file():
        return p.read_text(errors="replace")[:limit]
    return ""


def build_for_feature(g: Graph, feature_id):
    f = g.nodes[feature_id]
    parts = [f"FEATURE: {f['name']} (status: {f['attrs'].get('status','?')})"]

    reqs = g.neighbors(feature_id, "REQUIRES")
    parts.append("REQUIRES: " + ", ".join(n["name"] for n in reqs))

    # docs — only what the graph connects to this feature
    docs = g.docs_for(feature_id)
    if docs:
        parts.append("\n=== DOCUMENTATION (connected via graph) ===")
        for d in docs:
            txt = _read_doc(d["attrs"].get("path", ""))
            if txt:
                parts.append(f"\n## {d['name']} ({d['attrs']['path']})\n{txt}")

    files = g.files_of(feature_id)
    if files:
        parts.append("\n=== IMPLEMENTS ===\n" + ", ".join(n["attrs"].get("path", n["name"]) for n in files))

    tests = g.tests_for(feature_id)
    if tests:
        parts.append("=== VERIFIED BY ===\n" + ", ".join(n["attrs"].get("path", n["name"]) for n in tests))

    # past bugs on the files this feature touches — "have I seen this before?"
    bugs = []
    for fl in files:
        bugs += g.neighbors(fl["id"], "CAUSED_BY", out=False)
    if bugs:
        parts.append("\n=== KNOWN BUGS (learn from these) ===")
        for b in bugs:
            parts.append(f"- {b['name']}: {b['attrs'].get('message','')}")

    return "\n".join(parts)


if __name__ == "__main__":
    from graph.seed import seed
    g = seed()
    print(build_for_feature(g, "feature:login")[:2000])
