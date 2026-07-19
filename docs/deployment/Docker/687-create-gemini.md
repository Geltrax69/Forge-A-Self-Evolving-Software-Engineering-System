url: https://docs.docker.com/reference/cli/docker/sandbox/create/gemini/
----

# docker sandbox create gemini

***

| Description | Create a sandbox for gemini                                   |
| ----------- | ------------------------------------------------------------- |
| Usage       | `docker sandbox create gemini WORKSPACE [EXTRA_WORKSPACE...]` |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Create a sandbox with access to a host workspace for gemini.

The workspace path is required and will be exposed inside the sandbox at the same path as on the host. Additional workspaces can be provided as extra arguments. Append ":ro" to mount them read-only.

Use 'docker sandbox run SANDBOX' to start gemini after creation.

## [Examples](#examples)

### [Create a Gemini sandbox in the current directory](#create-a-gemini-sandbox-in-the-current-directory)

```console
$ docker sandbox create gemini .
```

### [Create with an absolute path](#create-with-an-absolute-path)

```console
$ docker sandbox create gemini /home/user/my-project
```

### [Create and then run](#create-and-then-run)

```console
$ docker sandbox create --name my-gemini gemini ~/my-project
$ docker sandbox run my-gemini
```

----
