"""Seed the graph with the Login example from the design brief, so the query
engine and context builder have something real to traverse."""
from graph.graph import Graph


def seed():
    g = Graph()
    # frameworks (stack)
    g.add("fw:go", "Framework", "Go")
    g.add("fw:chi", "Framework", "Chi")
    g.add("fw:sqlc", "Framework", "SQLC")
    g.add("fw:postgres", "Framework", "Postgres")
    g.add("fw:jwt", "Framework", "JWT")

    # docs (real paths into docs/)
    g.add("doc:go", "Documentation", "Go docs", path="backend/Go")
    g.add("doc:chi", "Documentation", "Chi docs", path="backend/Chi")
    g.add("doc:jwt", "Documentation", "JWT docs", path="auth/JWT")
    g.add("doc:sqlc", "Documentation", "SQLC docs", path="backend/SQLC")
    g.add("doc:pg", "Documentation", "Postgres docs", path="database/PostgreSQL")

    # feature + tasks + file + test + example + bug
    g.add("feature:login", "Feature", "Login", status="planned")
    g.add("task:jwt", "Task", "Generate JWT", status="todo")
    g.add("file:auth", "File", "auth.go", path="workspace/auth.go")
    g.add("test:login", "Test", "Login API Test", path="workspace/auth_test.go", status="untested")
    g.add("ex:login", "Example", "go/login", path="go/login")
    g.add("bug:bearer", "Bug", "Bearer prefix missing",
          message="JWT validation failed: token had no 'Bearer ' prefix trimmed", status="open")

    # relationships (edges) — this is what makes it a graph
    g.link("feature:login", "REQUIRES", "fw:jwt")
    g.link("feature:login", "REQUIRES", "fw:chi")
    g.link("feature:login", "REQUIRES", "fw:go")
    g.link("feature:login", "REQUIRES", "fw:sqlc")
    g.link("fw:jwt", "DOCUMENTED_BY", "doc:jwt")
    g.link("fw:chi", "DOCUMENTED_BY", "doc:chi")
    g.link("fw:go", "DOCUMENTED_BY", "doc:go")
    g.link("fw:sqlc", "DOCUMENTED_BY", "doc:sqlc")
    g.link("fw:jwt", "HAS_EXAMPLE", "ex:login")
    g.link("feature:login", "IMPLEMENTED_BY", "file:auth")
    g.link("feature:login", "VERIFIED_BY", "test:login")
    g.link("file:auth", "DEPENDS_ON", "fw:jwt")
    g.link("file:auth", "USES", "fw:chi")
    g.link("bug:bearer", "CAUSED_BY", "file:auth")
    return g


if __name__ == "__main__":
    g = seed()
    g.save()
    print(f"seeded {len(g.nodes)} nodes, {len(g.edges)} edges -> {g.STORE if hasattr(g,'STORE') else 'graph.json'}")
    print("\nQ1 docs for Login:", [n['name'] for n in g.docs_for('feature:login')])
    print("Q2 files of Login:", [n['name'] for n in g.files_of('feature:login')])
    print("Q3 blast radius of JWT:", [n['name'] for n in g.blast_radius('fw:jwt')])
    print("Q4 similar bugs 'prefix':", [n['name'] for n in g.similar_bugs('prefix')])
    print("Q5 tests for Login:", [n['name'] for n in g.tests_for('feature:login')])
