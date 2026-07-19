"""Project Graph engine — stdlib only, JSON-backed. No Neo4j (schema is the point).

ponytail: nodes+edges+query merged into one file. A dict of nodes and a list of
edges IS the graph; splitting it across 4 files would be ceremony. Swap to a real
graph DB only if traversal gets slow at thousands of nodes.
"""
import json
from pathlib import Path
from graph import schema

STORE = Path(__file__).resolve().parent.parent / "memory" / "project_graph" / "graph.json"


class Graph:
    def __init__(self):
        self.nodes = {}          # id -> {id, type, name, attrs}
        self.edges = []          # [ [src_id, rel, dst_id], ... ]

    # --- build ---
    def add(self, id, type, name, **attrs):
        assert type in schema.NODE_TYPES, f"unknown node type: {type}"
        self.nodes[id] = {"id": id, "type": type, "name": name, "attrs": attrs}
        return id

    def link(self, src, rel, dst):
        assert rel in schema.EDGE_TYPES, f"unknown edge type: {rel}"
        assert src in self.nodes and dst in self.nodes, f"link on missing node: {src}->{dst}"
        e = [src, rel, dst]
        if e not in self.edges:
            self.edges.append(e)

    # --- query engine ---
    def neighbors(self, id, rel=None, out=True):
        """Nodes reachable from `id` along `rel`. out=False walks edges backwards."""
        res = []
        for s, r, d in self.edges:
            if rel and r != rel:
                continue
            if out and s == id:
                res.append(self.nodes[d])
            elif not out and d == id:
                res.append(self.nodes[s])
        return res

    def traverse(self, start, rels, out=True, _seen=None):
        """Follow a chain of relations, collecting every node hit. rels is a list,
        e.g. ['REQUIRES','DOCUMENTED_BY'] to go Feature->Framework->Doc."""
        _seen = _seen or {}
        frontier = [start]
        for rel in rels:
            nxt = []
            for nid in frontier:
                for n in self.neighbors(nid, rel, out):
                    _seen[n["id"]] = n
                    nxt.append(n["id"])
            frontier = nxt
        return list(_seen.values())

    def by_type(self, type):
        return [n for n in self.nodes.values() if n["type"] == type]

    def find(self, name):
        low = name.lower()
        return [n for n in self.nodes.values() if low in n["name"].lower() or low in n["id"].lower()]

    # --- the 5 schema queries ---
    def docs_for(self, feature_id):          # Q1
        return [n for n in self.traverse(feature_id, ["REQUIRES", "DOCUMENTED_BY"])
                if n["type"] == "Documentation"]
    def files_of(self, feature_id):          # Q2
        return self.neighbors(feature_id, "IMPLEMENTED_BY")
    def blast_radius(self, framework_id):    # Q3  what breaks if this changes
        return self.neighbors(framework_id, "DEPENDS_ON", out=False)
    def similar_bugs(self, keyword):         # Q4
        k = keyword.lower()
        return [b for b in self.by_type("Bug")
                if k in b["name"].lower() or k in b["attrs"].get("message", "").lower()]
    def tests_for(self, feature_id):         # Q5
        return self.neighbors(feature_id, "VERIFIED_BY")

    # --- persistence ---
    def save(self, path=STORE):
        Path(path).write_text(json.dumps({"nodes": self.nodes, "edges": self.edges}, indent=2))
    @classmethod
    def load(cls, path=STORE):
        g = cls()
        if Path(path).exists() and Path(path).stat().st_size:
            d = json.loads(Path(path).read_text())
            g.nodes, g.edges = d["nodes"], d["edges"]
        return g
