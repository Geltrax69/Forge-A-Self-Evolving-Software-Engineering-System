url: https://docs.docker.com/reference/cli/docker/node/promote/
----

# docker node promote

***

| Description | Promote one or more nodes to manager in the swarm |
| ----------- | ------------------------------------------------- |
| Usage       | `docker node promote NODE [NODE...]`              |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Promotes a node to manager. This command can only be executed on a manager node.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Examples](#examples)

```console
$ docker node promote <node name>
```

----
