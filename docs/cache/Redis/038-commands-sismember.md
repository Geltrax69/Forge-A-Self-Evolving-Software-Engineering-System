url: https://redis.io/docs/latest/commands/sismember/
----

# SISMEMBER

Determines whether a member belongs to a set.

Returns if `member` is a member of the set stored at `key`.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the set.

</details>

<details open><summary><code>member</code></summary>

The member to check for.

</details>

## Examples

SADD myset "one"
SISMEMBER myset "one"
SISMEMBER myset "two"

## Return information


One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if the element is not a member of the set, or when the key does not exist.
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if the element is a member of the set.

-tab-sep-

One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if the element is not a member of the set, or when the key does not exist.
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if the element is a member of the set.



----
