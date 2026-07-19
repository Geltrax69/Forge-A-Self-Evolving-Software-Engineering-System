url: https://redis.io/docs/latest/commands/getset/
----

# GETSET

Returns the previous string value of a key after setting it to a new

Atomically sets `key` to `value` and returns the old value stored at `key`.
Returns an error when `key` exists but does not hold a string value.  Any 
previous time to live associated with the key is discarded on successful 
[`SET`]() operation.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

<details open><summary><code>value</code></summary>

The new value to set.

</details>

## Examples

SET mykey "Hello"
GETSET mykey "World"
GET mykey

## Details

### Design pattern

You can use GETSET with [INCR]() to count events and reset the counter atomically.
For example, you can call [INCR]() on the key `mycounter` each time an event occurs. When you need to read the counter value and reset it to zero atomically, call GETSET.
This can be done using `GETSET mycounter "0"`:

INCR mycounter
GETSET mycounter "0"
GET mycounter

## Return information


One of the following:
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): the old value stored at the key.
* [Nil reply](../../develop/reference/protocol-spec#bulk-strings): if the key does not exist.

-tab-sep-

One of the following:
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): the old value stored at the key.
* [Null reply](../../develop/reference/protocol-spec#nulls): if the key does not exist.



----
