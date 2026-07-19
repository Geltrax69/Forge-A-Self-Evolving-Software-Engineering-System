url: https://redis.io/docs/latest/commands/object-encoding/
----

# OBJECT ENCODING

Returns the internal encoding of a Redis object.

Returns the internal encoding for the Redis object stored at `key`.


## Required arguments

<details open><summary><code>key</code></summary>

The name of the key.

</details>

## Details

Redis objects can be encoded in different ways:

* Strings can be encoded as: 

    - `raw`, normal string encoding.
    - `int`, strings representing integers in a 64-bit signed interval, encoded in this way to save space.
    - `embstr`, an embedded string, which is an object where the internal simple dynamic string, `sds`, is an unmodifiable string allocated in the same chuck as the object itself.
      `embstr` can be strings with lengths up to the hardcoded limit of `OBJ_ENCODING_EMBSTR_SIZE_LIMIT` or 44 bytes. 

* Lists can be encoded as:
 
    - `linkedlist`, simple list encoding. No longer used, an old list encoding.
    - `ziplist`, Redis <= 6.2, a space-efficient encoding used for small lists.
    - `listpack`, Redis >= 7.0, a space-efficient encoding used for small lists.
    - `quicklist`, encoded as linkedlist of ziplists or listpacks.

* Sets can be encoded as:

    - `hashtable`, normal set encoding.
    - `intset`, a special encoding used for small sets composed solely of integers.
    - `listpack`, Redis >= 7.2, a space-efficient encoding used for small sets.

* Hashes can be encoded as:

    - `zipmap`, no longer used, an old hash encoding.
    - `hashtable`, normal hash encoding.
    - `ziplist`, Redis <= 6.2, a space-efficient encoding used for small hashes.
    - `listpack`, Redis >= 7.0, a space-efficient encoding used for small hashes.

* Sorted Sets can be encoded as:

    - `skiplist`, normal sorted set encoding.
    - `ziplist`, Redis <= 6.2, a space-efficient encoding used for small sorted sets.
    - `listpack`, Redis >= 7.0, a space-efficient encoding used for small sorted sets.

* Streams can be encoded as:

  - `stream`, encoded as a radix tree of listpacks.

All the specially encoded types are automatically converted to the general type once you perform an operation that makes it impossible for Redis to retain the space saving encoding.

## Return information


One of the following:
* [Nil reply](../../develop/reference/protocol-spec#bulk-strings): if the key doesn't exist.
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): the encoding of the object.

-tab-sep-

One of the following:
* [Null reply](../../develop/reference/protocol-spec#nulls): if the key doesn't exist.
* [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): the encoding of the object.



----
