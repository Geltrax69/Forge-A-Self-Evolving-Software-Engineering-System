url: https://redis.io/docs/latest/commands/llen/
----

# LLEN

Returns the length of a list.

Returns the length of the list stored at `key`.
If `key` does not exist, it is interpreted as an empty list and `0` is returned.
An error is returned when the value stored at `key` is not a list.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the list.

</details>

## Examples

redis> LPUSH mylist "World"
(integer) 1
redis> LPUSH mylist "Hello"
(integer) 2
redis> LLEN mylist
(integer) 2

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the length of the list.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the length of the list.



----
