url: https://redis.io/docs/latest/commands/watch/
----

# WATCH

Monitors changes to keys to determine the execution of a transaction.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


Marks the given keys to be watched for conditional execution of a
[transaction][tt].

[tt]: /develop/interact/transactions

## Return information


[Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`.

-tab-sep-

[Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`.



----
