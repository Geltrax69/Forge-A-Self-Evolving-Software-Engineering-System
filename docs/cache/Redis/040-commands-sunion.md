url: https://redis.io/docs/latest/commands/sunion/
----

# SUNION

Returns the union of multiple sets.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


Returns the members of the set resulting from the union of all the given sets.

For example:

```
key1 = {a,b,c,d}
key2 = {c}
key3 = {a,c,e}
SUNION key1 key2 key3 = {a,b,c,d,e}
```

Keys that do not exist are considered to be empty sets.

## Required arguments

<details open><summary><code>key [key ...]</code></summary>

One or more set keys to union.

</details>

## Examples

SADD key1 "a"
SADD key1 "b"
SADD key1 "c"
SADD key2 "c"
SADD key2 "d"
SADD key2 "e"
SUNION key1 key2

## Return information


[Array reply](../../develop/reference/protocol-spec#arrays): a list with members of the resulting set.

-tab-sep-

[Set reply](../../develop/reference/protocol-spec#sets): a set with the members of the resulting set.



----
