url: https://redis.io/docs/latest/commands/hget/
----

# HGET

Returns the value of a field in a hash.

Returns the value associated with `field` in the hash stored at `key`.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the hash.

</details>

<details open><summary><code>field</code></summary>

The field whose value to retrieve.

</details>

## Examples

> HSET myhash field1 "foo"
(integer) 1
> HGET myhash field1
"foo"
> HGET myhash field2
(nil)

## Return information


One of the following:
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): The value associated with the field.
* [Nil reply](../../develop/reference/protocol-spec#bulk-strings): If the field is not present in the hash or key does not exist.

-tab-sep-

One of the following:
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): The value associated with the field.
* [Null reply](../../develop/reference/protocol-spec#nulls): If the field is not present in the hash or key does not exist.



----
