url: https://docs.docker.com/reference/api/extensions-sdk/Exec/
----

# Interface: Exec

***

Table of contents

***

## [Callable](#callable)

### [Exec](#exec)

▸ **Exec**(`cmd`, `args`, `options?`): `Promise`<[`ExecResult`](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/)>

Executes a command.

**`Since`**

0.2.0

#### [Parameters](#parameters)

| Name       | Type                                                                               | Description                              |
| ---------- | ---------------------------------------------------------------------------------- | ---------------------------------------- |
| `cmd`      | `string`                                                                           | The command to execute.                  |
| `args`     | `string`\[]                                                                        | The arguments of the command to execute. |
| `options?` | [`ExecOptions`](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/) | The list of options.                     |

#### [Returns](#returns)

`Promise`<[`ExecResult`](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/)>

A promise that will resolve once the command finishes.

### [Exec](#exec-1)

▸ **Exec**(`cmd`, `args`, `options`): [`ExecProcess`](https://docs.docker.com/reference/api/extensions-sdk/ExecProcess/)

Streams the result of a command if `stream` is specified in the `options` parameter.

Specify the `stream` if the output of your command is too long or if you need to stream things indefinitely (for example container logs).

**`Since`**

0.2.2

#### [Parameters](#parameters-1)

| Name      | Type                                                                                 | Description                              |
| --------- | ------------------------------------------------------------------------------------ | ---------------------------------------- |
| `cmd`     | `string`                                                                             | The command to execute.                  |
| `args`    | `string`\[]                                                                          | The arguments of the command to execute. |
| `options` | [`SpawnOptions`](https://docs.docker.com/reference/api/extensions-sdk/SpawnOptions/) | The list of options.                     |

#### [Returns](#returns-1)

[`ExecProcess`](https://docs.docker.com/reference/api/extensions-sdk/ExecProcess/)

The spawned process.

----
