url: https://redis.io/docs/latest/commands/hexists/
----

# HEXISTS

Determines whether a field exists in a hash.

Returns if `field` is an existing field in the hash stored at `key`.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the hash.

</details>

<details open><summary><code>field</code></summary>

The field to check for existence.

</details>

## Examples

HSET myhash field1 "foo"
HEXISTS myhash field1
HEXISTS myhash field2

## Return information


One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if the hash does not contain the field, or the key does not exist.
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if the hash contains the field.

-tab-sep-

One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if the hash does not contain the field, or the key does not exist.
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if the hash contains the field.



----
