url: https://docs.docker.com/reference/cli/docker/mcp/catalog/server/ls/
----

# docker mcp catalog server ls

***

| Description                                                               | List servers in a catalog                      |
| ------------------------------------------------------------------------- | ---------------------------------------------- |
| Usage                                                                     | `docker mcp catalog server ls <oci-reference>` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker mcp catalog server list`               |

## [Description](#description)

List all servers in a catalog.

Use --filter to search for servers matching a query (case-insensitive substring matching on server names). Filters use key=value format (e.g., name=github).

## [Options](#options)

| Option         | Default | Description                       |
| -------------- | ------- | --------------------------------- |
| `-f, --filter` |         | Filter output (e.g., name=github) |
| `--format`     | `human` | Supported: json, yaml, human.     |

## [Examples](#examples)

# [List all servers in a catalog](#list-all-servers-in-a-catalog)

docker mcp catalog server ls mcp/docker-mcp-catalog:latest

# [Filter servers by name](#filter-servers-by-name)

docker mcp catalog server ls mcp/docker-mcp-catalog:latest --filter name=github

# [Combine multiple filters (using short flag)](#combine-multiple-filters-using-short-flag)

docker mcp catalog server ls mcp/docker-mcp-catalog:latest -f name=slack -f name=github

# [Output in JSON format](#output-in-json-format)

docker mcp catalog server ls mcp/docker-mcp-catalog:latest --format json

----
