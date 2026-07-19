url: https://redis.io/docs/latest/commands/rename/
----

# RENAME

Renames a key and overwrites the destination.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


Renames `key` to `newkey`.
It returns an error when `key` does not exist.
If `newkey` already exists it is overwritten, when this happens `RENAME` executes an implicit [`DEL`]() operation, so if the deleted key contains a very big value it may cause high latency even if `RENAME` itself is usually a constant-time operation.

In Cluster mode, both `key` and `newkey` must be in the same **hash slot**, meaning that in practice only keys that have the same hash tag can be reliably renamed in cluster.

## Required arguments

<details open><summary><code>key</code></summary>

The key to rename.

</details>

<details open><summary><code>newkey</code></summary>

The new key name. An existing key with this name is overwritten.

</details>

## Examples

SET mykey "Hello"
RENAME mykey myotherkey
GET myotherkey

## Return information


[Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`.

-tab-sep-

[Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`.



