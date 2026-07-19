url: https://redis.io/docs/latest/commands/sadd/
----

# SADD

Adds one or more members to a set. Creates the key if it doesn't exist.

Add the specified members to the set stored at `key`.
Specified members that are already a member of this set are ignored.
If `key` does not exist, a new set is created before adding the specified
members.

An error is returned when the value stored at `key` is not a set.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the set.

</details>

<details open><summary><code>member [member ...]</code></summary>

One or more members to add to the set.

</details>

## Examples

redis> SADD myset "Hello" "World"
(integer) 2
redis> SADD myset "World"
(integer) 0
redis> SMEMBERS myset
1) "Hello"
2) "World"

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the number of elements that were added to the set, not including all the elements already present in the set.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the number of elements that were added to the set, not including all the elements already present in the set.



----
