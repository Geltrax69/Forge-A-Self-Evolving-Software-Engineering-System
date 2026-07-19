url: https://redis.io/docs/latest/commands/ttl/
----

# TTL

Returns the expiration time in seconds of a key.

Returns the remaining time to live of a key that has a timeout.
This introspection capability allows a Redis client to check how many seconds a
given key will continue to be part of the dataset.

In Redis 2.6 or older the command returns `-1` if the key does not exist or if the key exists but has no associated expire.

Starting with Redis 2.8 the return value in case of error changed:

* The command returns `-2` if the key does not exist.
* The command returns `-1` if the key exists but has no associated expire.

See also the [`PTTL`]() command that returns the same information with milliseconds resolution (Only available in Redis 2.6 or greater).

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

## Examples

> SET mykey "Hello"
"OK"
> EXPIRE mykey 10
(integer) 1
> TTL mykey
(integer) 10

## Return information


One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): TTL in seconds.
* [Integer reply](../../develop/reference/protocol-spec#integers): `-1` if the key exists but has no associated expiration.
* [Integer reply](../../develop/reference/protocol-spec#integers): `-2` if the key does not exist.

-tab-sep-

One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): TTL in seconds.
* [Integer reply](../../develop/reference/protocol-spec#integers): `-1` if the key exists but has no associated expiration.
* [Integer reply](../../develop/reference/protocol-spec#integers): `-2` if the key does not exist.



----
