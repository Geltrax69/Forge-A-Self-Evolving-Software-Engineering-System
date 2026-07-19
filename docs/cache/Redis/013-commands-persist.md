url: https://redis.io/docs/latest/commands/persist/
----

# PERSIST

Removes the expiration time of a key.

Remove the existing timeout on `key`, turning the key from _volatile_ (a key
with an expire set) to _persistent_ (a key that will never expire as no timeout
is associated).

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

## Examples

SET mykey "Hello"
EXPIRE mykey 10
TTL mykey
PERSIST mykey
TTL mykey

## Return information


One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if _key_ does not exist or does not have an associated timeout.
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if the timeout has been removed.

-tab-sep-

One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if _key_ does not exist or does not have an associated timeout.
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if the timeout has been removed.



----
