"""Forge experiment harness — records and prints every model call.

Reusable recorder: what went in, what came back (or what it 'thought'), tokens,
timing, speed. Plus a real Go verifier (goimports/vet/build) for the patch loop.

Usage:
    from experiments.harness import Recorder, go_build
    rec = Recorder(model="dolphin-x1-8b")
    rec.call("probe: jwt package", system, user, max_tokens=30)
    rec.summary()
"""
import sys, os, json, time, urllib.request, subprocess, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class Recorder:
    def __init__(self, model=None, temperature=0):
        self.model = model or config.LLM_MODEL
        self.temperature = temperature
        self.log = []

    def call(self, label, system, user, max_tokens=600, show_input=True):
        messages = [{"role": "system", "content": system},
                    {"role": "user", "content": user}]
        body = json.dumps({"model": self.model, "messages": messages,
                           "temperature": self.temperature, "max_tokens": max_tokens}).encode()
        req = urllib.request.Request(config.LLM_BASE_URL + "/chat/completions",
                                     data=body, headers={"Content-Type": "application/json"})
        t = time.time()
        data = json.loads(urllib.request.urlopen(req, timeout=300).read())
        dt = time.time() - t

        u = data["usage"]
        m = data["choices"][0]["message"]
        content = (m.get("content") or "").strip()
        thought = (m.get("reasoning_content") or "").strip()
        answer = content or thought
        finish = data["choices"][0]["finish_reason"]

        rec = {"label": label, "model": self.model, "answer": answer,
               "used_reasoning": not content and bool(thought),
               "prompt_tokens": u["prompt_tokens"], "output_tokens": u["completion_tokens"],
               "total_tokens": u["total_tokens"], "finish": finish,
               "seconds": round(dt, 1), "tok_per_s": round(u["completion_tokens"] / dt, 1)}
        self.log.append(rec)
        self._print(label, system, user, rec, show_input)
        return rec

    def _print(self, label, system, user, rec, show_input):
        print("\n" + "=" * 72)
        print(f"▶ {label}   [model: {rec['model']}]")
        print("=" * 72)
        if show_input:
            print("── INPUT (user) ──")
            print(user if len(user) < 1500 else user[:1500] + "\n…[truncated]")
        tag = "  ⚠ from reasoning_content (no final answer)" if rec["used_reasoning"] else ""
        print("── OUTPUT ──" + tag)
        print(rec["answer"])
        print(f"── tokens: in={rec['prompt_tokens']} out={rec['output_tokens']} "
              f"total={rec['total_tokens']} | finish={rec['finish']} | "
              f"{rec['seconds']}s @ {rec['tok_per_s']} tok/s")

    def summary(self):
        tot = sum(r["total_tokens"] for r in self.log)
        secs = sum(r["seconds"] for r in self.log)
        print("\n" + "#" * 72)
        print(f"# SUMMARY — {len(self.log)} calls | {tot} total tokens | {secs:.1f}s")
        print("#" * 72)
        for r in self.log:
            print(f"  {r['label'][:40]:40s}  out={r['output_tokens']:4d}  "
                  f"total={r['total_tokens']:5d}  {r['finish']}")


# --- deterministic Go verifier -------------------------------------------
def go_build(code, deps=("github.com/go-chi/chi/v5", "github.com/golang-jwt/jwt/v5")):
    """Write code to a temp module, fetch deps, go build. Returns (ok, errors)."""
    d = tempfile.mkdtemp(prefix="forge_build_")
    try:
        with open(os.path.join(d, "main.go"), "w") as f:
            f.write(code)
        subprocess.run(["go", "mod", "init", "forgetest"], cwd=d, capture_output=True)
        for dep in deps:
            subprocess.run(["go", "get", dep], cwd=d, capture_output=True, timeout=120)
        r = subprocess.run(["go", "build", "./..."], cwd=d, capture_output=True, text=True, timeout=120)
        return r.returncode == 0, r.stderr.strip()
    finally:
        shutil.rmtree(d, ignore_errors=True)


def extract_code(text):
    """Pull the first ```go fenced block, else return text as-is."""
    if "```" in text:
        block = text.split("```", 2)[1]
        return block[len("go"):].lstrip("\n") if block.startswith("go") else block.lstrip("\n")
    return text
