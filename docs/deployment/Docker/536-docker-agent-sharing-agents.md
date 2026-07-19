url: https://docs.docker.com/ai/docker-agent/sharing-agents/
----

# Sharing agents

***

Table of contents

***

Push your agent to a registry and share it by name. Your teammates reference `agentcatalog/security-expert` instead of copying YAML files around or asking you where your agent configuration lives.

When you update the agent in the registry, everyone gets the new version the next time they pull or restart their client.

## [Prerequisites](#prerequisites)

To push agents to a registry, authenticate first:

```console
$ docker login
```

For other registries, use their authentication method.

## [Publishing agents](#publishing-agents)

Push your agent configuration to a registry:

```console
$ docker agent share push ./agent.yml myusername/agent-name
```

Push creates the repository if it doesn't exist yet. Use Docker Hub or any OCI-compatible registry.

Tag specific versions:

```console
$ docker agent share push ./agent.yml myusername/agent-name:v1.0.0
$ docker agent share push ./agent.yml myusername/agent-name:latest
```

## [Using published agents](#using-published-agents)

Pull an agent to inspect it locally:

```console
$ docker agent share pull agentcatalog/pirate
```

This saves the configuration as a local YAML file.

Run agents directly from the registry:

```console
$ docker agent run agentcatalog/pirate
```

Or reference it directly in integrations:

### [Editor integration (ACP)](#editor-integration-acp)

Use registry references in ACP configurations so your editor always uses the latest version:

```json
{
  "agent_servers": {
    "myagent": {
      "command": "docker",
      "args": ["agent", "aserve", "acp", "agentcatalog/pirate"]
    }
  }
}
```

### [MCP client integration](#mcp-client-integration)

Agents can be exposed as tools in MCP clients:

```json
{
  "mcpServers": {
    "myagent": {
      "command": "docker",
      "args": ["agent", "serve", "mcp", "agentcatalog/pirate"]
    }
  }
}
```

## [What's next](#whats-next)

* Set up [ACP integration](https://docs.docker.com/ai/docker-agent/integrations/acp/) with shared agents
* Configure [MCP integration](https://docs.docker.com/ai/docker-agent/integrations/mcp/) with shared agents
* Browse the [agent catalog](https://hub.docker.com/u/agentcatalog) for examples

----
