url: https://redis.io/docs/latest/commands/zrem/
----

# ZREM

Removes one or more members from a sorted set. Deletes the sorted set

Removes the specified members from the sorted set stored at `key`.
Non existing members are ignored.

An error is returned when `key` exists and does not hold a sorted set.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the sorted set.

</details>

<details open><summary><code>member [member ...]</code></summary>

One or more members to remove from the sorted set.

</details>

## Examples

ZADD myzset 1 "one"
ZADD myzset 2 "two"
ZADD myzset 3 "three"
ZREM myzset "two"
ZRANGE myzset 0 -1 WITHSCORES

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the number of members removed from the sorted set, not including non-existing members.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the number of members removed from the sorted set, not including non-existing members.



----
