url: https://redis.io/docs/latest/commands/copy/
----

# COPY

Copies the value of a key to a new key.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


This command copies the value stored at the `source` key to the `destination`
key.

By default, the `destination` key is created in the logical database used by the
connection. The `DB` option allows specifying an alternative logical database
index for the destination key.

The command returns zero when the `destination` key already exists. The
`REPLACE` option removes the `destination` key before copying the value to it.

## Required arguments

<details open><summary><code>source</code></summary>

The key to copy from.

</details>

<details open><summary><code>destination</code></summary>

The key to copy to.

</details>

## Optional arguments

<details open><summary><code>DB destination-db</code></summary>

Copy the key to the given database index instead of the current one.

</details>

<details open><summary><code>REPLACE</code></summary>

Replace the destination key if it already exists.

</details>

## Examples

```
SET dolly "sheep"
COPY dolly clone
GET clone
```

## Return information


One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if _source_ was copied.
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if _source_ was not copied.

-tab-sep-

One of the following:
* [Integer reply](../../develop/reference/protocol-spec#integers): `1` if _source_ was copied.
* [Integer reply](../../develop/reference/protocol-spec#integers): `0` if _source_ was not copied.



----
