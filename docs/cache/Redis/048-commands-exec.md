url: https://redis.io/docs/latest/commands/exec/
----

# EXEC

Executes all commands in a transaction.

This command's behavior varies in clustered Redis environments. See the [multi-key operations]() page for more information.


Executes all previously queued commands in a [transaction][tt] and restores the
connection state to normal.

[tt]: /develop/interact/transactions

When using [`WATCH`](), `EXEC` will execute commands only if the watched keys were
not modified, allowing for a [check-and-set mechanism][ttc].

[ttc]: /develop/interact/transactions#cas

## Return information


One of the following:
* [Array reply](../../develop/reference/protocol-spec#arrays): each element being the reply to each of the commands in the atomic transaction.
* [Nil reply](../../develop/reference/protocol-spec#bulk-strings): the transaction was aborted because a `WATCH`ed key was touched.

-tab-sep-

One of the following:
* [Array reply](../../develop/reference/protocol-spec#arrays): each element being the reply to each of the commands in the atomic transaction.
* [Null reply](../../develop/reference/protocol-spec#nulls): the transaction was aborted because a `WATCH`ed key was touched.



----
