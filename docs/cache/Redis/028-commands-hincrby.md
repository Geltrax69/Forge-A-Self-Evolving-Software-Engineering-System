url: https://redis.io/docs/latest/commands/hincrby/
----

# HINCRBY

Increments the integer value of a field in a hash by a number. Uses 0

Increments the number stored at `field` in the hash stored at `key` by
`increment`.
If `key` does not exist, a new key holding a hash is created.
If `field` does not exist the value is set to `0` before the operation is
performed.

The range of values supported by `HINCRBY` is limited to 64 bit signed integers.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the hash.

</details>

<details open><summary><code>field</code></summary>

The field whose value to increment.

</details>

<details open><summary><code>increment</code></summary>

The integer amount to add to the field's value.

</details>

## Examples

Since the `increment` argument is signed, both increment and decrement
operations can be performed:

HSET myhash field 5
HINCRBY myhash field 1
HINCRBY myhash field -1
HINCRBY myhash field -10

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the value of the field after the increment operation.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the value of the field after the increment operation.



----
