"""Deterministic verifier — the software that does what the 1B is bad at.

The benchmark showed the model loops on mechanical fixes (imports, package clause,
formatting). So software handles those; the model is reserved for semantic errors.

Pipeline per candidate:  goimports (adds/removes imports + formats) -> go build.
best_code_block compiles EVERY fenced block and keeps the one that builds — because
the model sometimes puts a broken block first and a correct one second.
"""
import os, re, subprocess, tempfile, shutil

GOIMPORTS = os.path.expanduser("~/go/bin/goimports")


def all_code_blocks(text):
    """Every fenced code block (lang tag stripped). Falls back to 'package ' onward."""
    blocks = [m.strip() for m in re.findall(r"```(?:go|golang)?\s*\n(.*?)```", text, re.S)]
    if blocks:
        return blocks
    p = text.find("package ")
    return [text[p:].strip()] if p != -1 else [text.strip()]


def classify(error):
    """Route a compiler error AFTER goimports has already run. So anything mechanical
    (missing/unused imports, formatting) is already fixed — a surviving `undefined:` or
    type error is a genuine SEMANTIC problem (wrong API), which is the model's job."""
    e = error.lower()
    if any(k in e for k in ("imported and not used", "expected 'package'",
                            "syntax error", "expected declaration")):
        return "MECHANICAL"   # goimports missed it (rare) — still not the model's job
    if any(k in e for k in ("undefined:", "has no field or method", "cannot use",
                            "invalid operation", "mismatched types", "too many arguments",
                            "not enough arguments")):
        return "SEMANTIC"     # wrong API/type — the model should fix this
    return "ARCHITECTURAL"


def _mech_fix(path):
    """goimports = add missing imports + drop unused + gofmt, in one deterministic pass."""
    subprocess.run([GOIMPORTS, "-w", path], capture_output=True, timeout=60)


def verify(code, deps=()):
    """goimports -> go get deps -> go build. Returns (ok, fixed_code, errors)."""
    d = tempfile.mkdtemp(prefix="forge_verify_")
    try:
        f = os.path.join(d, "main.go")
        with open(f, "w") as fh:
            fh.write(code)
        subprocess.run(["go", "mod", "init", "forgetest"], cwd=d, capture_output=True)
        _mech_fix(f)                                    # mechanical stage
        for dep in deps:
            subprocess.run(["go", "get", dep], cwd=d, capture_output=True, timeout=120)
        _mech_fix(f)                                    # re-run now that deps exist
        r = subprocess.run(["go", "build", "./..."], cwd=d, capture_output=True, text=True, timeout=120)
        fixed = open(f).read()
        return r.returncode == 0, fixed, r.stderr.strip()
    finally:
        shutil.rmtree(d, ignore_errors=True)


def _score(ok, code):
    return (5 if ok else 0) + (2 if "package " in code else 0) + \
           (2 if "import" in code else 0) + (1 if "func Test" in code else 0)


def best_code_block(text, deps=()):
    """Compile every block after mechanical fixes; return the best-scoring one.
    Returns (code, ok, errors) for the winner."""
    best = None
    for block in all_code_blocks(text):
        ok, fixed, errors = verify(block, deps)
        s = _score(ok, fixed)
        if best is None or s > best[0]:
            best = (s, fixed, ok, errors)
        if ok:
            break  # a compiling block is good enough
    _, code, ok, errors = best
    return code, ok, errors


if __name__ == "__main__":
    # self-check: a block that goimports can rescue (missing import) vs a broken one
    good = 'package main\nfunc main(){ fmt.Println("hi") }'   # missing "fmt" import
    ok, fixed, err = verify(good)
    print("goimports rescued missing import:", ok, "| import fmt' in fixed:", '"fmt"' in fixed)
    assert ok and '"fmt"' in fixed, "goimports should have added fmt"
    print("OK")
