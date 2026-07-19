url: https://redis.io/docs/latest/commands/subscribe/
----

# SUBSCRIBE

Listens for messages published to channels.

Subscribes the client to the specified channels.

Once the client enters the subscribed state it is not supposed to issue any
other commands, except for additional `SUBSCRIBE`, [`SSUBSCRIBE`](), [`PSUBSCRIBE`](), [`UNSUBSCRIBE`](), [`SUNSUBSCRIBE`](), 
[`PUNSUBSCRIBE`](), [`PING`](), [`RESET`]() and [`QUIT`]() commands.
However, if RESP3 is used (see [`HELLO`]()) it is possible for a client to issue any commands while in subscribed state.

For more information, see [Pub/sub]().

## Required arguments

<details open><summary><code>channel [channel ...]</code></summary>

One or more channels to subscribe to.

</details>

## Return information


When successful, this command doesn't return anything. Instead, for each channel, one message with the first element being the string `subscribe` is pushed as a confirmation that the command succeeded.

-tab-sep-

When successful, this command doesn't return anything. Instead, for each channel, one message with the first element being the string `subscribe` is pushed as a confirmation that the command succeeded.



----
