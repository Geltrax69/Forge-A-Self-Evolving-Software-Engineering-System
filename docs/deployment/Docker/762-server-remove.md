url: https://docs.docker.com/reference/cli/docker/mcp/catalog/server/remove/
----

# docker mcp catalog server remove

***

| Description                                                               | Remove MCP servers from a catalog                                                    |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Usage                                                                     | `docker mcp catalog server remove <oci-reference> --name <name1> --name <name2> ...` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker mcp catalog server rm`                                                       |

## [Description](#description)

Remove MCP servers from a catalog by server name.

## [Options](#options)

| Option   | Default | Description                                             |
| -------- | ------- | ------------------------------------------------------- |
| `--name` |         | Server name to remove (can be specified multiple times) |

## [Examples](#examples)

# [Remove servers by name](#remove-servers-by-name)

docker mcp catalog server remove mcp/my-catalog:latest --name github --name slack

# [Remove a single server](#remove-a-single-server)

docker mcp catalog server remove mcp/my-catalog:latest --name github

----
