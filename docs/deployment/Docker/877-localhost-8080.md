        url: http://localhost:8080
        name: code-reviewer
```

Now when users ask the main agent about code quality, it can delegate to the specialist. The main agent sees `code-reviewer` as a tool it can call, and the specialist has access to the codebase tools it needs.

## [Calling other A2A agents](#calling-other-a2a-agents)

Your agents can call remote A2A agents as tools. Configure the A2A toolset with the remote agent's URL:

```yaml
agents:
  root:
    toolsets:
      - type: a2a
