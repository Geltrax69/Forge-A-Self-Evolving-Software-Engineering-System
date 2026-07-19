url: https://redis.io/docs/latest/commands/zincrby/
----

# ZINCRBY

Increments the score of a member in a sorted set.

Increments the score of `member` in the sorted set stored at `key` by
`increment`.
If `member` does not exist in the sorted set, it is added with `increment` as
its score (as if its previous score was `0.0`).
If `key` does not exist, a new sorted set with the specified `member` as its
sole member is created.

An error is returned when `key` exists but does not hold a sorted set.

The `score` value should be the string representation of a numeric value, and
accepts double precision floating point numbers.
It is possible to provide a negative value to decrement the score.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the sorted set.

</details>

<details open><summary><code>increment</code></summary>

The amount to add to the member's current score.

</details>

<details open><summary><code>member</code></summary>

The member whose score to increment. It is added with the increment as its score if it does not exist.

</details>

## Examples

ZADD myzset 1 "one"
ZADD myzset 2 "two"
ZINCRBY myzset 2 "one"
ZRANGE myzset 0 -1 WITHSCORES

## Return information


[Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): the new score of _member_ as a double precision floating point number.

-tab-sep-

[Double reply](../../develop/reference/protocol-spec#doubles): the new score of _member_.



----
