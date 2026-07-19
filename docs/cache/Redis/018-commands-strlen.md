url: https://redis.io/docs/latest/commands/strlen/
----

# STRLEN

Returns the length of a string value.

Returns the length of the string value stored at `key`.
An error is returned when `key` holds a non-string value.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

## Examples

SET mykey "Hello world"
STRLEN mykey
STRLEN nonexisting

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the length of the string stored at key, or 0 when the key does not exist.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the length of the string stored at key, or 0 when the key does not exist.



----
