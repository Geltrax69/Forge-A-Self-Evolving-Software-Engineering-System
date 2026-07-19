url: https://redis.io/docs/latest/commands/rpop/
----

# RPOP

Returns and removes the last elements of a list. Deletes the list if

Removes and returns the last elements of the list stored at `key`.

By default, the command pops a single element from the end of the list.
When provided with the optional `count` argument, the reply will consist of up
to `count` elements, depending on the list's length.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the list.

</details>

## Optional arguments

<details open><summary><code>count</code></summary>

The number of elements to pop. Without it, a single element is popped.

</details>

## Examples

redis> RPUSH mylist "one" "two" "three" "four" "five"
(integer) 5
redis> RPOP mylist
"five"
redis> RPOP mylist 2
1) "four"
2) "three"
redis> LRANGE mylist 0 -1
1) "one"
2) "two"

## Return information


One of the following:
* [Nil reply](../../develop/reference/protocol-spec#bulk-strings): if the key does not exist.
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): when called without the _count_ argument, the value of the last element.
* [Array reply](../../develop/reference/protocol-spec#arrays): when called with the _count_ argument, a list of popped elements.

-tab-sep-

One of the following:
* [Null reply](../../develop/reference/protocol-spec#nulls): if the key does not exist.
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): when called without the _count_ argument, the value of the last element.
* [Array reply](../../develop/reference/protocol-spec#arrays): when called with the _count_ argument, a list of popped elements.



----
