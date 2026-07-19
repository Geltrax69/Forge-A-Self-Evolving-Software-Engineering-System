url: https://redis.io/docs/latest/commands/keys/
----

# KEYS

Returns all key names that match a pattern.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


Returns all keys matching `pattern`.



## Required arguments

<details open><summary><code>pattern</code></summary>

The glob-style pattern to match key names against.

</details>

## Details

While the time complexity for this operation is O(N), the constant times are
fairly low.
For example, Redis running on an entry level laptop can scan a 1 million key
database in 40 milliseconds.

Use extreme care when using this command in production environments.
It may ruin performance when it is executed against large databases.
This command is intended for debugging and special operations, such as changing
your keyspace layout.
Don't use `KEYS` in your regular application code.
If you're looking for a way to find keys in a subset of your keyspace, consider
using [`SCAN`]() or [sets]().

Supported glob-style patterns:

* `h?llo` matches `hello`, `hallo` and `hxllo`
* `h*llo` matches `hllo` and `heeeello`
* `h[ae]llo` matches `hello` and `hallo,` but not `hillo`
* `h[^e]llo` matches `hallo`, `hbllo`, ... but not `hello`
* `h[a-b]llo` matches `hallo` and `hbllo`

Use `\` to escape special characters if you want to match them verbatim.

When using [Redis Cluster](), the search is optimized for patterns that imply a single slot.
If a pattern can only match keys of one slot,
Redis only iterates over keys in that slot, rather than the whole database,
when searching for keys matching the pattern.
For example, with the pattern `{a}h*llo`, Redis would only try to match it with the keys in slot 15495, which hash tag `{a}` implies.
To use pattern with a hash tag, see [Hash tags]() in the Cluster specification for more information.

## Examples

> MSET firstname Jack lastname Stuntman age 35
"OK"
> KEYS *name*
1) "lastname"
2) "firstname"
> KEYS a??
1) "age"
> KEYS *
1) "age"
2) "lastname"
3) "firstname"

## Return information


[Array reply](../../develop/reference/protocol-spec#arrays): a list of keys matching _pattern_.

-tab-sep-

[Array reply](../../develop/reference/protocol-spec#arrays): a list of keys matching _pattern_.



----
