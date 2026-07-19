url: https://redis.io/docs/latest/commands/append/
----

# APPEND

Appends a string to the value of a key. Creates the key if it doesn't

Appends a value to the string stored at `key`. If `key` does not exist, it is created with an empty string, so in that case, `APPEND` behaves like [`SET`]().

## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

<details open><summary><code>value</code></summary>

The string to append to the existing value.

</details>

## Examples

EXISTS mykey
APPEND mykey "Hello"
APPEND mykey " World"
GET mykey

## Details

### Pattern: time series

The `APPEND` command can be used to create a very compact representation of a
list of fixed-size samples, usually referred as _time series_.
Every time a new sample arrives we can store it using the command

```
APPEND timeseries "fixed-size sample"
```

Accessing individual elements in the time series is not hard:

* [`STRLEN`]() can be used in order to obtain the number of samples.
* [`GETRANGE`]() allows for random access of elements.
  If our time series have associated time information we can easily implement
  a binary search to get range combining [`GETRANGE`]() with the Lua scripting
  engine available in Redis 2.6.
* [`SETRANGE`]() can be used to overwrite an existing time series.

The limitation of this pattern is that we are forced into an append-only mode
of operation, there is no way to cut the time series to a given size easily
because Redis currently lacks a command able to trim string objects.
However the space efficiency of time series stored in this way is remarkable.

Hint: it is possible to switch to a different key based on the current Unix
time, in this way it is possible to have just a relatively small amount of
samples per key, to avoid dealing with very big keys, and to make this pattern
more friendly to be distributed across many Redis instances.

An example sampling the temperature of a sensor using fixed-size strings (using
a binary format is better in real implementations).

APPEND ts "0043"
APPEND ts "0035"
GETRANGE ts 0 3
GETRANGE ts 4 7

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the length of the string after the append operation.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the length of the string after the append operation.



----
