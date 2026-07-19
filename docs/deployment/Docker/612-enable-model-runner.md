url: https://docs.docker.com/reference/cli/docker/desktop/enable/model-runner/
----

# docker desktop enable model-runner

***

| Description | Manage Docker Model Runner settings            |
| ----------- | ---------------------------------------------- |
| Usage       | `docker desktop enable model-runner [OPTIONS]` |

## [Description](#description)

Enable and manage Docker Model Runner settings used by 'docker model'

## [Options](#options)

| Option     | Default | Description                                                                           |
| ---------- | ------- | ------------------------------------------------------------------------------------- |
| `--no-tcp` |         | Disable TCP connection. Cannot be used with --tcp.                                    |
| `--tcp`    | `12434` | Enable or change TCP port for connection (1-65535). Cannot be used with --no-tcp.     |
| `--cors`   | `all`   | CORS configuration. Can be `all`, `none`, or comma-separated list of allowed origins. |

----
