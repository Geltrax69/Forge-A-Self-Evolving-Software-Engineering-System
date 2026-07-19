url: https://redis.io/docs/latest/commands/hdel/
----

# HDEL

Deletes one or more fields and their values from a hash. Deletes the

Removes the specified fields from the hash stored at `key`.
Specified fields that do not exist within this hash are ignored.
Deletes the hash if no fields remain.
If `key` does not exist, it is treated as an empty hash and this command returns
`0`.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the hash.

</details>

<details open><summary><code>field [field ...]</code></summary>

One or more fields to delete from the hash.

</details>

## Examples

> HSET myhash field1 "foo"
(integer) 1
> HDEL myhash field1
(integer) 1
> HDEL myhash field2
(integer) 0

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the number of fields that were removed from the hash, excluding any specified but non-existing fields.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): The number of fields that were removed from the hash, excluding any specified but non-existing fields.



----
