"""LLM client — stdlib only, OpenAI-compatible. Works with LM Studio, Ollama, etc.
Handles reasoning models (MiniCPM) that split output into reasoning_content + content."""
import json, urllib.request, urllib.error
import config


def chat(messages, temperature=0.3, max_tokens=1500, model=None):
    """Send chat messages, return the assistant text. Falls back to reasoning_content
    if the model spent its whole budget thinking and left content empty."""
    body = json.dumps({
        "model": model or config.LLM_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(
        f"{config.LLM_BASE_URL}/chat/completions",
        data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {config.LLM_API_KEY}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read())
    except urllib.error.URLError as e:
        raise RuntimeError(f"LLM unreachable at {config.LLM_BASE_URL}: {e}") from e

    msg = data["choices"][0]["message"]
    content = (msg.get("content") or "").strip()
    if not content:  # reasoning model burned budget thinking — use that, flag it
        content = (msg.get("reasoning_content") or "").strip()
    if data["choices"][0].get("finish_reason") == "length":
        content += "\n\n[truncated: hit max_tokens]"
    return content


def ask(system, user, **kw):
    """Convenience: single system+user turn."""
    return chat([{"role": "system", "content": system},
                 {"role": "user", "content": user}], **kw)


if __name__ == "__main__":
    # smoke test against whatever is configured
    print(ask("You are terse.", "Say 'pipeline online' and nothing else.", max_tokens=200))
