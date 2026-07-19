url: https://redis.io/docs/latest/commands/del/
----

# DEL

Deletes one or more keys.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


Removes the specified keys.
A key is ignored if it does not exist.

## Required arguments

<details open><summary><code>key [key ...]</code></summary>

One or more keys to delete.

</details>

## Examples

> SET key1 "Hello"
"OK"
> SET key2 "World"
"OK"
> DEL key1 key2 key3
(integer) 2

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the number of keys that were removed.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the number of keys that were removed.



----
