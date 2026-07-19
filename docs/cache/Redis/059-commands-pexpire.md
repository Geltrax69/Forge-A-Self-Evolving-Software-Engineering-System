url: https://redis.io/docs/latest/commands/pexpire/
----

# PEXPIRE

Sets the expiration time of a key in milliseconds.

This command works exactly like [`EXPIRE`]() but the time to live of the key is
specified in milliseconds instead of seconds.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key to set a timeout on.

</details>

<details open><summary><code>milliseconds</code></summary>

The timeout, in milliseconds.

</details>

## Optional arguments

The following options modify the command's behavior. They are mutually exclusive.

<details open><summary><code>NX</code></summary>

Set expiry only when the key has no expiry.

</details>

<details open><summary><code>XX</code></summary>

Set expiry only when the key has an existing expiry.

</details>

<details open><summary><code>GT</code></summary>

Set expiry only when the new expiry is greater than the current one. A non-volatile key is treated as an infinite TTL for the purpose of `GT`.

</details>

<details open><summary><code>LT</code></summary>

Set expiry only when the new expiry is less than the current one. A non-volatile key is treated as an infinite TTL for the purpose of `LT`.

</details>

## Examples

SET mykey "Hello"
PEXPIRE mykey 1500
TTL mykey
PTTL mykey
PEXPIRE mykey 1000 XX
TTL mykey
PEXPIRE mykey 1000 NX
TTL mykey

## Return information


One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if the timeout was not set. For example, if the key doesn't exist, or the operation skipped because of the provided arguments.
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if the timeout was set.

-tab-sep-

One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if the timeout was not set. For example, if the key doesn't exist, or the operation skipped because of the provided arguments.
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if the timeout was set.



----
