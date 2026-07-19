url: https://docs.docker.com/reference/cli/docker/service/rm/
----

# docker service rm

***

| Description                                                               | Remove one or more services              |
| ------------------------------------------------------------------------- | ---------------------------------------- |
| Usage                                                                     | `docker service rm SERVICE [SERVICE...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker service remove`                  |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Removes the specified services from the swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Examples](#examples)

Remove the `redis` service:

```console
$ docker service rm redis

redis

$ docker service ls

ID  NAME  MODE  REPLICAS  IMAGE
```

> Warning
>
> Unlike `docker rm`, this command does not ask for confirmation before removing a running service.

----
