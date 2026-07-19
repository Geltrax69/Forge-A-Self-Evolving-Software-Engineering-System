url: https://redis.io/docs/latest/commands/get/
----

# GET

Returns the string value of a key.

Get the value of `key`.
If the key does not exist, `nil` is returned.
An error is returned if the value stored at `key` is not a string, because `GET`
only handles string values.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

## Examples

> GET nonexisting
(nil)
> SET mykey "Hello"
"OK"
> GET mykey
"Hello"

## Return information


One of the following:
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): the value of the key.
* [Nil reply](../../develop/reference/protocol-spec#bulk-strings): if the key does not exist.

-tab-sep-

One of the following:
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): the value of the key.
* [Null reply](../../develop/reference/protocol-spec#nulls): key does not exist.



----
