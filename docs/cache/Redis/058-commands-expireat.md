url: https://redis.io/docs/latest/commands/expireat/
----

# EXPIREAT

Sets the expiration time of a key to a Unix timestamp.

`EXPIREAT` has the same effect and semantic as [`EXPIRE`](), but instead of
specifying the number of seconds representing the TTL (time to live), it takes
an absolute [Unix timestamp][hewowu] (seconds since January 1, 1970). A
timestamp in the past will delete the key immediately.

[hewowu]: http://en.wikipedia.org/wiki/Unix_time

Please for the specific semantics of the command refer to the documentation of
[`EXPIRE`]().

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

<details open><summary><code>unix-time-seconds</code></summary>

The absolute expiration time as a Unix timestamp in seconds. A timestamp in the past deletes the key immediately.

</details>

## Optional arguments

These options are mutually exclusive.

<details open><summary><code>NX</code></summary>

Set the expiry only when the key has no expiry.

</details>

<details open><summary><code>XX</code></summary>

Set the expiry only when the key already has an expiry.

</details>

<details open><summary><code>GT</code></summary>

Set the expiry only when the new expiry is greater than the current one. A non-volatile key is treated as an infinite TTL for the purpose of `GT`.

</details>

<details open><summary><code>LT</code></summary>

Set the expiry only when the new expiry is less than the current one. A non-volatile key is treated as an infinite TTL for the purpose of `LT`.

</details>

## Examples

SET mykey "Hello"
EXISTS mykey
EXPIREAT mykey 1293840000
EXISTS mykey

## Details

### Background

`EXPIREAT` was introduced in order to convert relative timeouts to absolute
timeouts for the AOF persistence mode.
Of course, it can be used directly to specify that a given key should expire at
a given time in the future.

## Return information


One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if the timeout was not set; for example, the key doesn't exist, or the operation was skipped because of the provided arguments.
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if the timeout was set.

-tab-sep-

One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if the timeout was not set; for example, the key doesn't exist, or the operation was skipped because of the provided arguments.
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if the timeout was set.



----
