url: https://docs.docker.com/reference/cli/docker/buildx/imagetools/
----

# docker buildx imagetools

***

| Description | Commands to work on images in registry |
| ----------- | -------------------------------------- |
| Usage       | `docker buildx imagetools`             |

## [Description](#description)

The `imagetools` commands contains subcommands for working with manifest lists in container registries. These commands are useful for inspecting manifests to check multi-platform configuration and attestations.

## [Examples](#examples)

### [Override the configured builder instance (--builder)](#builder)

Same as [`buildx --builder`](/reference/cli/docker/buildx/#builder).

## [Subcommands](#subcommands)

| Command                                                                                                       | Description                               |
| ------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| [`docker buildx imagetools create`](https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/)   | Create a new image based on source images |
| [`docker buildx imagetools inspect`](https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/) | Show details of an image in the registry  |

----
