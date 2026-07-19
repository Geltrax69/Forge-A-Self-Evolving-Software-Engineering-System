url: https://docs.docker.com/reference/cli/sbx/policy/deny/
----

# sbx policy deny

| Description | Add a deny rule for sandboxes |
| ----------- | ----------------------------- |
| Usage       | `sbx policy deny COMMAND`     |

## [Description](#description)

Add a rule that blocks sandboxes from accessing specified resources.

Deny rules always take precedence over allow rules. If a resource matches both an allow and a deny rule, the request is blocked.

## [Commands](#commands)

| Command                                                                                     | Description                            |
| ------------------------------------------------------------------------------------------- | -------------------------------------- |
| [`sbx policy deny network`](https://docs.docker.com/reference/cli/sbx/policy/deny/network/) | Deny network access to specified hosts |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
