url: https://docs.docker.com/reference/cli/docker/context/update/
----

# docker context update

***

| Description | Update a context                          |
| ----------- | ----------------------------------------- |
| Usage       | `docker context update [OPTIONS] CONTEXT` |

## [Description](#description)

Updates an existing `context`. See [context create](/reference/cli/docker/context/create/).

## [Options](#options)

| Option          | Default | Description                |
| --------------- | ------- | -------------------------- |
| `--description` |         | Description of the context |
| `--docker`      |         | set the docker endpoint    |

## [Examples](#examples)

### [Update an existing context](#update-an-existing-context)

```console
$ docker context update \
    --description "some description" \
    --docker "host=tcp://myserver:2376,ca=~/ca-file,cert=~/cert-file,key=~/key-file" \
    my-context
```

----
