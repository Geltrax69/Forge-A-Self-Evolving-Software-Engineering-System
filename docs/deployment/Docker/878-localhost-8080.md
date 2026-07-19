        url: http://localhost:8080
        name: specialist
```

The `url` specifies where the remote agent is running, and `name` is an optional identifier for the tool. Your agent can now delegate tasks to the remote specialist agent.

If the remote agent requires authentication or custom headers:

```yaml
agents:
  root:
    toolsets:
      - type: a2a
