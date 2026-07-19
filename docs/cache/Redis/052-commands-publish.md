url: https://redis.io/docs/latest/commands/publish/
----

# PUBLISH

Posts a message to a channel.

Posts a message to the given channel.

In a Redis Cluster, clients can publish to every node. The cluster makes sure
that published messages are forwarded as needed, so clients can subscribe to any
channel by connecting to any one of the nodes.

## Required arguments

<details open><summary><code>channel</code></summary>

The channel to publish to.

</details>

<details open><summary><code>message</code></summary>

The message to publish.

</details>

## Return information


[Integer reply](../../develop/reference/protocol-spec#integers): the number of clients that the message was sent to. Note that in a Redis Cluster, only clients that are connected to the same node as the publishing client are included in the count.

-tab-sep-

[Integer reply](../../develop/reference/protocol-spec#integers): the number of clients that the message was sent to. Note that in a Redis Cluster, only clients that are connected to the same node as the publishing client are included in the count.



----
