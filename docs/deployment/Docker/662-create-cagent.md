url: https://docs.docker.com/reference/cli/docker/sandbox/create/cagent/
----

# docker sandbox create cagent

***

| Description | Create a sandbox for cagent                                   |
| ----------- | ------------------------------------------------------------- |
| Usage       | `docker sandbox create cagent WORKSPACE [EXTRA_WORKSPACE...]` |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Create a sandbox with access to a host workspace for cagent.

The workspace path is required and will be exposed inside the sandbox at the same path as on the host. Additional workspaces can be provided as extra arguments. Append ":ro" to mount them read-only.

Use 'docker sandbox run SANDBOX' to start cagent after creation.

## [Examples](#examples)

### [Create a Cagent sandbox in the current directory](#create-a-cagent-sandbox-in-the-current-directory)

```console
$ docker sandbox create cagent .
```

### [Create with an absolute path](#create-with-an-absolute-path)

```console
$ docker sandbox create cagent /home/user/my-project
```

### [Create and then run](#create-and-then-run)

```console
$ docker sandbox create --name my-cagent cagent ~/my-project
$ docker sandbox run my-cagent
```

----
