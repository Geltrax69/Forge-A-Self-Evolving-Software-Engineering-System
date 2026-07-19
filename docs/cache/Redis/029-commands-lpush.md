url: https://redis.io/docs/latest/commands/lpush/
----

# LPUSH

Prepends one or more elements to a list. Creates the key if it doesn't

Insert all the specified values at the head of the list stored at `key`.
If `key` does not exist, it is created as empty list before performing the push
operations.
When `key` holds a value that is not a list, an error is returned.

It is possible to push multiple elements using a single command call just
specifying multiple arguments at the end of the command.
Elements are inserted one after the other to the head of the list, from the
leftmost element to the rightmost element.
So for instance the command `LPUSH mylist a b c` will result into a list
containing `c` as first element, `b` as second element and `a` as third element.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the list.

</details>

<details open><summary><code>element [element ...]</code></summary>

One or more values to prepend to the list.

</details>

## Examples
redis> LPUSH mylist "world"
(integer) 1
redis> LPUSH mylist "hello"
(integer) 2
redis> LRANGE mylist 0 -1
1) "hello"
2) "world"

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the length of the list after the push operation.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the length of the list after the push operation.



----
