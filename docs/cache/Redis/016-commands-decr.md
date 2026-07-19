url: https://redis.io/docs/latest/commands/decr/
----

# DECR

Decrements the integer value of a key by one. Uses 0 as initial value

Decrements the number stored at `key` by one.
If the key does not exist, it is set to `0` before performing the operation.
An error is returned if the key contains a value of the wrong type or contains a
string that can not be represented as integer.
This operation is limited to 64-bit signed integers.

See [`INCR`]() for extra information on increment/decrement operations.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

## Examples

SET mykey "10"
DECR mykey
SET mykey "234293482390480948029348230948"
DECR mykey

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the value of the key after decrementing it.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the value of the key after decrementing it.



----
