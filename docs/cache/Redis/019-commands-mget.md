url: https://redis.io/docs/latest/commands/mget/
----

# MGET

Atomically returns the string values of one or more keys.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.

Returns the values of all specified keys.
For every key that does not hold a string value or does not exist, `nil` is returned.
Because of this, the operation never fails.

## Required arguments

<details open><summary><code>key [key ...]</code></summary>

One or more keys whose values to retrieve.

</details>

## Examples

> SET key1 "Hello"
"OK"
> SET key2 "World"
"OK"
> MGET key1 key2 nonexisting
1) "Hello"
2) "World"
3) (nil)

## Return information


[Array reply](../../develop/reference/protocol-spec#arrays): a list of values at the specified keys.

-tab-sep-

[Array reply](../../develop/reference/protocol-spec#arrays): a list of values at the specified keys.



----
