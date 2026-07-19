url: https://docs.docker.com/reference/cli/docker/context/inspect/
----

# docker context inspect

***

| Description | Display detailed information on one or more contexts      |
| ----------- | --------------------------------------------------------- |
| Usage       | `docker context inspect [OPTIONS] [CONTEXT] [CONTEXT...]` |

## [Description](#description)

Inspects one or more contexts.

## [Options](#options)

| Option         | Default | Description                                                                                                                                                                                                                             |
| -------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-f, --format` |         | Format output using a custom template: 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |

## [Examples](#examples)

### [Inspect a context by name](#inspect-a-context-by-name)

```console
$ docker context inspect "local+aks"

[
  {
    "Name": "local+aks",
    "Metadata": {
      "Description": "Local Docker Engine",
      "StackOrchestrator": "swarm"
    },
    "Endpoints": {
      "docker": {
        "Host": "npipe:////./pipe/docker_engine",
        "SkipTLSVerify": false
      }
    },
    "TLSMaterial": {},
    "Storage": {
      "MetadataPath": "C:\\Users\\simon\\.docker\\contexts\\meta\\cb6d08c0a1bfa5fe6f012e61a442788c00bed93f509141daff05f620fc54ddee",
      "TLSPath": "C:\\Users\\simon\\.docker\\contexts\\tls\\cb6d08c0a1bfa5fe6f012e61a442788c00bed93f509141daff05f620fc54ddee"
    }
  }
]
```

----
