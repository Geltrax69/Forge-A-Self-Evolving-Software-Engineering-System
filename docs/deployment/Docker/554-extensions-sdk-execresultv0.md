url: https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/
----

# Interface: ExecResultV0

***

Table of contents

***

## [Properties](#properties)

### [cmd](#cmd)

• `Optional` `Readonly` **cmd**: `string`

***

### [killed](#killed)

• `Optional` `Readonly` **killed**: `boolean`

***

### [signal](#signal)

• `Optional` `Readonly` **signal**: `string`

***

### [code](#code)

• `Optional` `Readonly` **code**: `number`

***

### [stdout](#stdout)

• `Readonly` **stdout**: `string`

***

### [stderr](#stderr)

• `Readonly` **stderr**: `string`

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

----
