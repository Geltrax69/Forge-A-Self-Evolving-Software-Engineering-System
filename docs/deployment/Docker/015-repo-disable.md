url: https://docs.docker.com/reference/cli/docker/scout/repo/disable/
----

# docker scout repo disable

***

| Description | Disable Docker Scout                     |
| ----------- | ---------------------------------------- |
| Usage       | `docker scout repo disable [REPOSITORY]` |

## [Description](#description)

The docker scout repo disable command disables Docker Scout on repositories.

## [Options](#options)

| Option          | Default | Description                                                                   |
| --------------- | ------- | ----------------------------------------------------------------------------- |
| `--all`         |         | Disable all repositories of the organization. Can not be used with --filter.  |
| `--filter`      |         | Regular expression to filter repositories by name                             |
| `--integration` |         | Name of the integration to use for enabling an image                          |
| `--org`         |         | Namespace of the Docker organization                                          |
| `--registry`    |         | Container Registry                                                            |

## [Examples](#examples)

### [Disable a specific repository](#disable-a-specific-repository)

```console
$ docker scout repo disable my/repository
```

### [Disable all repositories of the organization](#disable-all-repositories-of-the-organization)

```console
$ docker scout repo disable --all
```

### [Disable some repositories based on a filter](#disable-some-repositories-based-on-a-filter)

```console
$ docker scout repo disable --filter namespace/backend
```

### [Disable a repository from a specific registry](#disable-a-repository-from-a-specific-registry)

```console
$ docker scout repo disable my/repository --registry 123456.dkr.ecr.us-east-1.amazonaws.com
```

----
