url: https://redis.io/docs/latest/commands/mset/
----

# MSET

Atomically creates or modifies the string values of one or more keys.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


Sets the given keys to their respective values.
`MSET` replaces existing values with new values, just as regular [`SET`]().
See [`MSETNX`]() if you don't want to overwrite existing values.

`MSET` is atomic, so all given keys are set at once.
It is not possible for clients to see that some of the keys were updated while
others are unchanged.

## Required arguments

<details open><summary><code>key value [key value ...]</code></summary>

One or more key-value pairs to set.

</details>

## Examples

MSET key1 "Hello" key2 "World"
GET key1
GET key2

## Return information


[Simple string reply](../../develop/reference/protocol-spec#simple-strings): always `OK` because `MSET` can't fail.

-tab-sep-

[Simple string reply](../../develop/reference/protocol-spec#simple-strings): always `OK` because `MSET` can't fail.



----
