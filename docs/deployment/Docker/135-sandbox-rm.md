url: https://docs.docker.com/reference/cli/docker/sandbox/rm/
----

# docker sandbox rm

***

| Description                                                               | Remove one or more sandboxes             |
| ------------------------------------------------------------------------- | ---------------------------------------- |
| Usage                                                                     | `docker sandbox rm SANDBOX [SANDBOX...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker sandbox remove`                  |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Remove one or more sandboxes and all their associated resources.

This command will:

* Check if the sandbox exists
* Remove the sandbox and clean up its associated resources

## [Examples](#examples)

### [Remove a sandbox](#remove-a-sandbox)

```console
$ docker sandbox rm abc123def
abc123def
```

### [Remove multiple sandboxes](#remove-multiple-sandboxes)

```console
$ docker sandbox rm abc123def def456ghi
abc123def
def456ghi
```

### [Remove all sandboxes](#remove-all-sandboxes)

```console
$ docker sandbox rm $(docker sandbox ls -q)
```

----
