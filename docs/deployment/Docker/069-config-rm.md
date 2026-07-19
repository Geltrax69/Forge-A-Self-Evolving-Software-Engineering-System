url: https://docs.docker.com/reference/cli/docker/config/rm/
----

# docker config rm

***

| Description                                                               | Remove one or more configs            |
| ------------------------------------------------------------------------- | ------------------------------------- |
| Usage                                                                     | `docker config rm CONFIG [CONFIG...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker config remove`                |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Removes the specified configs from the Swarm.

For detailed information about using configs, refer to [store configuration data using Docker Configs](/engine/swarm/configs/).

> Note
>
> This is a cluster management command, and must be executed on a Swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Examples](#examples)

This example removes a config:

```console
$ docker config rm my_config
sapth4csdo5b6wz2p5uimh5xg
```

> Warning
>
> This command doesn't ask for confirmation before removing a config.

----
