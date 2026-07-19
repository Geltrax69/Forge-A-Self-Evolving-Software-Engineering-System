url: https://redis.io/docs/latest/commands/hgetall/
----

# HGETALL

Returns all fields and values in a hash.

Returns all fields and values of the hash stored at `key`.
In the returned value, every field name is followed by its value, so the length
of the reply is twice the size of the hash.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the hash.

</details>

## Examples

redis> HSET myhash field1 "Hello"
(integer) 1
redis> HSET myhash field2 "World"
(integer) 1
redis> HGETALL myhash
1) "field1"
2) "Hello"
3) "field2"
4) "World"

## Return information


[Array reply](../../develop/reference/protocol-spec#arrays): a list of fields and their values, or an empty list when key does not exist.

-tab-sep-

[Map reply](../../develop/reference/protocol-spec#maps): a map of fields and their values, or an empty list when key does not exist.



----
