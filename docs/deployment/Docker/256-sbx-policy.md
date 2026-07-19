url: https://docs.docker.com/reference/cli/sbx/policy/
----

# sbx policy

| Description | Manage sandbox policies |
| ----------- | ----------------------- |
| Usage       | `sbx policy COMMAND`    |

## [Description](#description)

Manage persistent access policies for sandboxes.

Policies contain rules that control what sandboxes can access. Local rules can apply globally across all sandboxes or be scoped to one sandbox. Use subcommands to allow, deny, list, or remove rules.

## [Commands](#commands)

| Command                                                                                   | Description                     |
| ----------------------------------------------------------------------------------------- | ------------------------------- |
| [`sbx policy allow`](https://docs.docker.com/reference/cli/sbx/policy/allow/)             | Add an allow rule for sandboxes |
| [`sbx policy deny`](https://docs.docker.com/reference/cli/sbx/policy/deny/)               | Add a deny rule for sandboxes   |
| [`sbx policy log`](https://docs.docker.com/reference/cli/sbx/policy/log/)                 | Show sandbox policy logs        |
| [`sbx policy ls`](https://docs.docker.com/reference/cli/sbx/policy/ls/)                   | List sandbox policy rules       |
| [`sbx policy reset`](https://docs.docker.com/reference/cli/sbx/policy/reset/)             | Reset policies to defaults      |
| [`sbx policy rm`](https://docs.docker.com/reference/cli/sbx/policy/rm/)                   | Remove a policy rule            |
| [`sbx policy set-default`](https://docs.docker.com/reference/cli/sbx/policy/set-default/) | Set the default network policy  |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
