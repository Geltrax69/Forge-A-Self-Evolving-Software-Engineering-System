url: https://redis.io/docs/latest/commands/set/
----

# SET

Sets the string value of a key, ignoring its type. The key is created

Set `key` to hold the string `value`.
If `key` already holds a value, it is overwritten, regardless of its type.
Any previous time to live associated with the key is discarded on successful `SET` operation.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

<details open><summary><code>value</code></summary>

The string value to set.

</details>

## Optional arguments

The following options modify the command's behavior. The condition options (`NX`, `XX`, `IFEQ`, `IFNE`, `IFDEQ`, `IFDNE`) are mutually exclusive, as are the expiration options (`EX`, `PX`, `EXAT`, `PXAT`, `KEEPTTL`).

<details open><summary><code>NX</code></summary>

Only set the key if it does not already exist.

</details>

<details open><summary><code>XX</code></summary>

Only set the key if it already exists.

</details>

<details open><summary><code>IFEQ ifeq-value</code></summary>

Set the key's value and expiration only if its current value is equal to `ifeq-value`. If the key doesn't exist, it won't be created.

</details>

<details open><summary><code>IFNE ifne-value</code></summary>

Set the key's value and expiration only if its current value is not equal to `ifne-value`. If the key doesn't exist, it will be created.

</details>

<details open><summary><code>IFDEQ ifdeq-digest</code></summary>

Set the key's value and expiration only if the hash digest of its current value is equal to `ifdeq-digest`. If the key doesn't exist, it won't be created. See the [Hash Digest](#hash-digest) section below for more information.

</details>

<details open><summary><code>IFDNE ifdne-digest</code></summary>

Set the key's value and expiration only if the hash digest of its current value is not equal to `ifdne-digest`. If the key doesn't exist, it will be created. See the [Hash Digest](#hash-digest) section below for more information.

</details>

<details open><summary><code>GET</code></summary>

Return the old string stored at the key, or nil if the key did not exist. An error is returned and `SET` is aborted if the value stored at the key is not a string.

</details>

<details open><summary><code>EX seconds</code></summary>

Set the specified expire time, in seconds (a positive integer).

</details>

<details open><summary><code>PX milliseconds</code></summary>

Set the specified expire time, in milliseconds (a positive integer).

</details>

<details open><summary><code>EXAT unix-time-seconds</code></summary>

Set the specified Unix time at which the key will expire, in seconds (a positive integer).

</details>

<details open><summary><code>PXAT unix-time-milliseconds</code></summary>

Set the specified Unix time at which the key will expire, in milliseconds (a positive integer).

</details>

<details open><summary><code>KEEPTTL</code></summary>

Retain the time to live associated with the key.

</details>

Note: Since the `SET` command options can replace [`SETNX`](), [`SETEX`](), [`PSETEX`](), [`GETSET`](), it is possible that in future versions of Redis these commands will be deprecated and finally removed.

## Examples

> SET mykey "Hello"
"OK"
> GET mykey
"Hello"
> SET anotherkey "will expire in a minute" EX 60
"OK"

## Details

### Hash digest

A hash digest is a fixed-size numerical representation of a string value, computed using the XXH3 hash algorithm. Redis uses this hash digest for efficient comparison operations without needing to compare the full string content. You can retrieve a key's hash digest using the [`DIGEST`]() command, which returns it as a hexadecimal string that you can use with the `IFDEQ` and `IFDNE` options, and also the [`DELEX`]() command's `IFDEQ` and `IFDNE` options.

### Patterns

Note: The following pattern is discouraged in favor of [the Redlock algorithm]() which is only a bit more complex to implement, but offers better guarantees and is fault tolerant.

The command `SET resource-name anystring NX EX max-lock-time` is a simple way to implement a locking system with Redis.

A client can acquire the lock if the above command returns `OK` (or retry after some time if the command returns Nil), and remove the lock just using [`DEL`]().

The lock will be auto-released after the expire time is reached.

It is possible to make this system more robust modifying the unlock schema as follows:

* Instead of setting a fixed string, set a non-guessable large random string, called token.
* Instead of releasing the lock with [`DEL`](), send a script that only removes the key if the value matches.

This avoids that a client will try to release the lock after the expire time deleting the key created by another client that acquired the lock later.

An example of unlock script would be similar to the following:

    if redis.call("get",KEYS[1]) == ARGV[1]
    then
        return redis.call("del",KEYS[1])
    else
        return 0
    end

The script should be called with `EVAL ...script... 1 resource-name token-value`

## Return information


* If `GET` was not specified, one of the following:
  * [Null bulk string reply](../../develop/reference/protocol-spec#bulk-strings) in the following two cases.
    * The key doesn’t exist and `XX/IFEQ/IFDEQ` was specified. The key was not created.
    * The key exists, and `NX` was specified or a specified `IFEQ/IFNE/IFDEQ/IFDNE` condition is false. The key was not set.
  * [Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`: The key was set.
* If `GET` was specified, one of the following:
  * [Null bulk string reply](../../develop/reference/protocol-spec#bulk-strings): The key didn't exist before the `SET` operation, whether the key was created of not.
  * [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): The previous value of the key, whether the key was set or not.

-tab-sep-

* If `GET` was not specified, one of the following:
  * [Null reply](../../develop/reference/protocol-spec#nulls) in the following two cases.
    * The key doesn’t exist and `XX/IFEQ/IFDEQ` was specified. The key was not created.
    * The key exists, and `NX` was specified or a specified `IFEQ/IFNE/IFDEQ/IFDNE` condition is false. The key was not set.
  * [Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`: The key was set.
* If `GET` was specified, one of the following:
  * [Null reply](../../develop/reference/protocol-spec#nulls): The key didn't exist before the `SET` operation, whether the key was created of not.
  * [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): The previous value of the key, whether the key was set or not.



----
