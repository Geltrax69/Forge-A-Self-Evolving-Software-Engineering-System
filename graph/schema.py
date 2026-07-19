"""Forge Project Graph — SCHEMA (the foundation, per the design brief).

Everything in Forge is a node. Nodes connect via typed edges. This file is the
single source of truth for what can exist in the graph and what each node stores.

------------------------------------------------------------------------------
NODE TYPES  — what each node stores in `attrs`
------------------------------------------------------------------------------
  Feature        {status}                  a capability, e.g. Login
  Task           {status}                  one unit of work, e.g. Generate JWT
  Component       {}                        a logical module, e.g. AuthService
  File           {path}                     a real source file, e.g. auth.go
  Documentation  {path}                     a docs/ folder or file to read
  Example        {path}                     an examples/ folder to read
  Bug            {message, status}          a problem seen, e.g. Bearer prefix missing
  Decision       {rationale, date}          a choice made and why
  Test           {path, status}             a verifier, e.g. jwt_test.go
  Tool           {}                         something the agent can run, e.g. go build
  Framework      {}                         a stack element, e.g. Go, Chi, JWT

------------------------------------------------------------------------------
EDGE TYPES  — (source) --REL--> (target)
------------------------------------------------------------------------------
  REQUIRES       Feature/Task -> Framework/Feature   what it needs
  IMPLEMENTED_BY Feature/Task -> File                 where the code lives
  DOCUMENTED_BY  Framework/Feature -> Documentation   where to read about it
  HAS_EXAMPLE    Framework/Feature -> Example         reference code
  VERIFIED_BY    Feature/Task -> Test                 what proves it works
  DEPENDS_ON     Component/File -> Framework/Component blast radius for changes
  CAUSED_BY      Bug -> File/Framework                where a bug came from
  FIXED_BY       Bug -> File/Decision                 how it was solved
  USES           File -> Framework                     concrete usage

------------------------------------------------------------------------------
QUERIES the graph must answer cleanly (these drive context building)
------------------------------------------------------------------------------
  Q1 "What docs are needed for feature X?"   X -REQUIRES-> F -DOCUMENTED_BY-> Doc
  Q2 "Which files implement X?"              X -IMPLEMENTED_BY-> File
  Q3 "What breaks if I change Redis?"        *reverse* DEPENDS_ON -> Redis
  Q4 "Have I solved a similar bug before?"   Bug nodes matching keywords
  Q5 "What tests verify X?"                  X -VERIFIED_BY-> Test
"""

NODE_TYPES = {
    "Feature", "Task", "Component", "File", "Documentation", "Example",
    "Bug", "Decision", "Test", "Tool", "Framework",
}

EDGE_TYPES = {
    "REQUIRES", "IMPLEMENTED_BY", "DOCUMENTED_BY", "HAS_EXAMPLE",
    "VERIFIED_BY", "DEPENDS_ON", "CAUSED_BY", "FIXED_BY", "USES",
}

# which node types a context build pulls readable text from (has a `path`)
READABLE = {"Documentation", "Example", "File", "Test"}
