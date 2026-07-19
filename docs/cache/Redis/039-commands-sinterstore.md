url: https://redis.io/docs/latest/commands/sinterstore/
----

# SINTERSTORE

Stores the intersect of multiple sets in a key.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


This command is equal to [`SINTER`](), but instead of returning the resulting set,
it is stored in `destination`.

If `destination` already exists, it is overwritten.

## Required arguments

<details open><summary><code>destination</code></summary>

The key to store the resulting set in.

</details>

<details open><summary><code>key [key ...]</code></summary>

One or more set keys to intersect.

</details>

## Examples

SADD key1 "a"
SADD key1 "b"
SADD key1 "c"
SADD key2 "c"
SADD key2 "d"
SADD key2 "e"
SINTERSTORE key key1 key2
SMEMBERS key

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the number of elements in the resulting set.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the number of elements in the result set.



----
