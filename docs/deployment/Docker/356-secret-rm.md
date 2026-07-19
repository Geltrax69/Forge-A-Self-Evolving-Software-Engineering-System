url: https://docs.docker.com/reference/cli/docker/secret/rm/
----

# docker secret rm

***

| Description                                                               | Remove one or more secrets            |
| ------------------------------------------------------------------------- | ------------------------------------- |
| Usage                                                                     | `docker secret rm SECRET [SECRET...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker secret remove`                |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Removes the specified secrets from the swarm.

For detailed information about using secrets, refer to [manage sensitive data with Docker secrets](/engine/swarm/secrets/).

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Examples](#examples)

This example removes a secret:

```console
$ docker secret rm secret.json
sapth4csdo5b6wz2p5uimh5xg
```

> Warning
>
> Unlike `docker rm`, this command does not ask for confirmation before removing a secret.

----
