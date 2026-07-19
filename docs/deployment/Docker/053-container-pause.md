url: https://docs.docker.com/reference/cli/docker/container/pause/
----

# docker container pause

***

| Description                                                               | Pause all processes within one or more containers |
| ------------------------------------------------------------------------- | ------------------------------------------------- |
| Usage                                                                     | `docker container pause CONTAINER [CONTAINER...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker pause`                                    |

## [Description](#description)

The `docker pause` command suspends all processes in the specified containers. On Linux, this uses the freezer cgroup. Traditionally, when suspending a process the `SIGSTOP` signal is used, which is observable by the process being suspended. With the freezer cgroup the process is unaware, and unable to capture, that it is being suspended, and subsequently resumed. On Windows, only Hyper-V containers can be paused.

See the [freezer cgroup documentation](https://www.kernel.org/doc/Documentation/cgroup-v1/freezer-subsystem.txt) for further details.

## [Examples](#examples)

```console
$ docker pause my_container
```

----
