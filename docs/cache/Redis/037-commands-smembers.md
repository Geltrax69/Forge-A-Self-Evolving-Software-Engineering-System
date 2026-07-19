url: https://redis.io/docs/latest/commands/smembers/
----

# SMEMBERS

Returns all members of a set.

Returns all the members of the set value stored at `key`.

This has the same effect as running [`SINTER`]() with one argument `key`.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the set.

</details>

## Examples

redis> SADD myset "Hello"
(integer) 1
redis> SADD myset "World"
(integer) 1
redis> SMEMBERS myset
1) "Hello"
2) "World"

## Return information


[Array reply](../../develop/reference/protocol-spec#arrays): an array with all the members of the set.

-tab-sep-

[Set reply](../../develop/reference/protocol-spec#sets): a set with all the members of the set.



----
