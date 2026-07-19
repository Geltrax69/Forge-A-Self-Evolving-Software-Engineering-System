url: https://redis.io/docs/latest/commands/incrby/
----

# INCRBY

Increments the integer value of a key by a number. Uses 0 as initial

Increments the number stored at `key` by `increment`.
If the key does not exist, it is set to `0` before performing the operation.
An error is returned if the key contains a value of the wrong type or contains a
string that can not be represented as integer.
This operation is limited to 64-bit signed integers.

See [`INCR`]() for extra information on increment/decrement operations.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

<details open><summary><code>increment</code></summary>

The integer amount to add to the value.

</details>

## Examples

SET mykey "10"
INCRBY mykey 5

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the value of the key after the increment.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the value of the key after the increment.



----
