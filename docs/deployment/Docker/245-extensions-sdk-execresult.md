url: https://docs.docker.com/reference/api/extensions-sdk/ExecResult/
----

# Interface: ExecResult

***

Table of contents

***

**`Since`**

0.2.0

## [Hierarchy](#hierarchy)

* [`RawExecResult`](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/)

  ↳ **`ExecResult`**

***

### [parseJsonLines](#parsejsonlines)

▸ **parseJsonLines**(): `any`\[]

Parse each output line as a JSON object.

#### [Returns](#returns-1)

`any`\[]

The list of lines where each line is a JSON object.

***

### [parseJsonObject](#parsejsonobject)

▸ **parseJsonObject**(): `any`

Parse a well-formed JSON output.

#### [Returns](#returns-2)

`any`

The JSON object.

## [Properties](#properties)

### [cmd](#cmd)

• `Optional` `Readonly` **cmd**: `string`

#### [Inherited from](#inherited-from)

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[cmd](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#cmd)

***

### [killed](#killed)

• `Optional` `Readonly` **killed**: `boolean`

#### [Inherited from](#inherited-from-1)

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[killed](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#killed)

***

### [signal](#signal)

• `Optional` `Readonly` **signal**: `string`

#### [Inherited from](#inherited-from-2)

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[signal](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#signal)

***

### [code](#code)

• `Optional` `Readonly` **code**: `number`

#### [Inherited from](#inherited-from-3)

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[code](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#code)

***

### [stdout](#stdout)

• `Readonly` **stdout**: `string`

#### [Inherited from](#inherited-from-4)

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[stdout](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#stdout)

***

### [stderr](#stderr)

• `Readonly` **stderr**: `string`

#### [Inherited from](#inherited-from-5)

[RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/).[stderr](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/#stderr)

----
