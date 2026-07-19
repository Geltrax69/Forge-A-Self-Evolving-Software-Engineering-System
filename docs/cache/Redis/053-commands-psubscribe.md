url: https://redis.io/docs/latest/commands/psubscribe/
----

# PSUBSCRIBE

Listens for messages published to channels that match one or more patterns.

Subscribes the client to the given patterns.


Once the client enters the subscribed state it is not supposed to issue any other commands, except for additional [`SUBSCRIBE`](), [`SSUBSCRIBE`](), `PSUBSCRIBE`, [`UNSUBSCRIBE`](), [`SUNSUBSCRIBE`](), [`PUNSUBSCRIBE`](), [`PING`](), [`RESET`]() and [`QUIT`]() commands.
However, if RESP3 is used (see [`HELLO`]()), it is possible for a client to issue any commands while in a subscribed state.

For more information, see [Pub/sub]().

## Required arguments

<details open><summary><code>pattern [pattern ...]</code></summary>

One or more glob-style patterns to subscribe to. Messages published to any channel whose name matches a pattern are delivered to the client.

Supported glob-style patterns:

* `h?llo` subscribes to `hello`, `hallo` and `hxllo`
* `h*llo` subscribes to `hllo` and `heeeello`
* `h[ae]llo` subscribes to `hello` and `hallo,` but not `hillo`

Use `\` to escape special characters if you want to match them verbatim.

</details>

## Return information


When successful, this command doesn't return anything. Instead, for each pattern, one message with the first element being the string `psubscribe` is pushed as a confirmation that the command succeeded.

-tab-sep-

When successful, this command doesn't return anything. Instead, for each pattern, one message with the first element being the string `psubscribe` is pushed as a confirmation that the command succeeded.



----
