url: https://redis.io/docs/latest/commands/multi/
----

# MULTI

Starts a transaction.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


Marks the start of a [transaction][tt] block.
Subsequent commands will be queued for atomic execution using [`EXEC`]().

[tt]: /develop/interact/transactions

## Return information


[Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`.

-tab-sep-

[Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`.



----
