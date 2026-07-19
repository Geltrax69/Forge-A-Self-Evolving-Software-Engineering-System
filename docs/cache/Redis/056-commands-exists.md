url: https://redis.io/docs/latest/commands/exists/
----

# EXISTS

Determines whether one or more keys exist.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


Returns the number of keys that exist.

If you specify the same existing key multiple times, `EXISTS` counts it each time. For example, if `somekey` exists, `EXISTS somekey somekey` returns `2`.

## Required arguments

<details open><summary><code>key [key ...]</code></summary>

One or more keys to check for existence. A repeated key is counted once per occurrence.

</details>

## Examples

> SET key1 "Hello"
> EXISTS key1
> EXISTS nosuchkey
> SET key2 "World"
> EXISTS key1 key2 nosuchkey

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the number of keys that exist from those specified as arguments.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the number of keys that exist from those specified as arguments.



----
