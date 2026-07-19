url: https://redis.io/docs/latest/commands/hset/
----

# HSET

Creates or modifies the value of a field in a hash.

Sets the specified fields to their respective values in the hash stored at `key`.

This command overwrites the values of specified fields that exist in the hash.
If `key` doesn't exist, a new key holding a hash is created.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the hash.

</details>

<details open><summary><code>field value [field value ...]</code></summary>

One or more field-value pairs to set in the hash.

</details>

## Examples

> HSET myhash field1 "Hello"
(integer) 1
> HGET myhash field1
"Hello"
> HSET myhash field2 "Hi" field3 "World"
(integer) 2
> HGET myhash field2
"Hi"
> HGET myhash field3
"World"
> HGETALL myhash
1) "field1"
2) "Hello"
3) "field2"
4) "Hi"
5) "field3"
6) "World"

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the number of fields that were added.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the number of fields that were added.



----
