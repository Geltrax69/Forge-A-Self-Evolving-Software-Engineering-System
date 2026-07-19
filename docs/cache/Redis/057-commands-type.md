url: https://redis.io/docs/latest/commands/type/
----

# TYPE

Determines the type of value stored at a key.

Returns the string representation of the type of the value stored at `key`.
The different types that can be returned are: `string`, `list`, `set`, `zset`,
`hash`, `stream`, and `vectorset`.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

## Examples

SET key1 "value"
LPUSH key2 "value"
SADD key3 "value"
TYPE key1
TYPE key2
TYPE key3

## Return information


[Simple string reply](../../develop/reference/protocol-spec#simple-strings): the type of _key_, or `none` when _key_ doesn't exist.

-tab-sep-

[Simple string reply](../../develop/reference/protocol-spec#simple-strings): the type of _key_, or `none` when _key_ doesn't exist.



----
