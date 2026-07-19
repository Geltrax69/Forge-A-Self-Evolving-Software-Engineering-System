url: https://redis.io/docs/latest/commands/discard/
----

# DISCARD

Discards a transaction.

Flushes all previously queued commands in a [transaction][tt] and restores the
connection state to normal.

[tt]: /develop/interact/transactions

If [`WATCH`]() was used, `DISCARD` unwatches all keys watched by the connection.

## Return information


[Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`.

-tab-sep-

[Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`.



----
