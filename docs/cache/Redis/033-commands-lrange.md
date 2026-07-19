url: https://redis.io/docs/latest/commands/lrange/
----

# LRANGE

Returns a range of elements from a list.

Returns the specified elements of the list stored at `key`.
The offsets `start` and `stop` are zero-based indexes, with `0` being the first
element of the list (the head of the list), `1` being the next element and so
on.

These offsets can also be negative numbers indicating offsets starting at the
end of the list.
For example, `-1` is the last element of the list, `-2` the penultimate, and so
on.

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key that holds the list.

</details>

<details open><summary><code>start</code></summary>

The zero-based start index. Negative indexes count from the tail.

</details>

<details open><summary><code>stop</code></summary>

The zero-based stop index (inclusive). Negative indexes count from the tail.

</details>

## Examples

redis> RPUSH mylist "one"
(integer) 1
redis> RPUSH mylist "two"
(integer) 2
redis> RPUSH mylist "three"
(integer) 3
redis> LRANGE mylist 0 0
1) "one"
redis> LRANGE mylist -3 2
1) "one"
2) "two"
3) "three"
redis> LRANGE mylist -100 100
1) "one"
2) "two"
3) "three"
redis> LRANGE mylist 5 10
(empty array)

## Details

### Consistency with range functions in various programming languages

Note that if you have a list of numbers from 0 to 100, `LRANGE list 0 10` will
return 11 elements, that is, the rightmost item is included.
This may or may not be consistent with the behavior of range-related functions
in your programming language of choice (think Ruby's `Range.new`, `Array#slice`
or Python's `range()` function).

### Out-of-range indexes

Out of range indexes will not produce an error.
If `start` is larger than the end of the list, an empty list is returned.
If `stop` is larger than the actual end of the list, Redis will treat it like
the last element of the list.

## Return information


[Array reply](../../develop/reference/protocol-spec#arrays): a list of elements in the specified range, or an empty array if the key doesn't exist.

-tab-sep-

[Array reply](../../develop/reference/protocol-spec#arrays): a list of elements in the specified range, or an empty array if the key doesn't exist.



----
