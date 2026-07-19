url: https://redis.io/docs/latest/commands/zscore/
----

# ZSCORE

Returns the score of a member in a sorted set.

Returns the score of `member` in the sorted set at `key`.

If `member` does not exist in the sorted set, or `key` does not exist, `nil` is
returned.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the sorted set.

</details>

<details open><summary><code>member</code></summary>

The member whose score to return.

</details>

## Examples

ZADD myzset 1 "one"
ZSCORE myzset "one"

## Return information


One of the following:
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): the score of the member (a double-precision floating point number), represented as a string.
* [Nil reply](../../develop/reference/protocol-spec#bulk-strings): if _member_ does not exist in the sorted set, or the key does not exist.

-tab-sep-

One of the following:
* [Double reply](../../develop/reference/protocol-spec#doubles): the score of the member (a double-precision floating point number).
* [Nil reply](../../develop/reference/protocol-spec#bulk-strings): if _member_ does not exist in the sorted set, or the key does not exist.



----
