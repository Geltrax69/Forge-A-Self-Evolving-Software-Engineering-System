url: https://18.react.dev/learn/lifecycle-of-reactive-effects
----

```
const serverUrl = 'https://localhost:1234';



function ChatRoom({ roomId }) {

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, [roomId]);

  // ...

}
```

Your Effect’s body specifies how to **start synchronizing:**

```
    // ...

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

    // ...
```

The cleanup function returned by your Effect specifies how to **stop synchronizing:**

```
    // ...

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

    // ...
```

Intuitively, you might think that React would **start synchronizing** when your component mounts and **stop synchronizing** when your component unmounts. However, this is not the end of the story! Sometimes, it may also be necessary to **start and stop synchronizing multiple times** while the component remains mounted.

Let’s look at *why* this is necessary, *when* it happens, and *how* you can control this behavior.

### Note

Some Effects don’t return a cleanup function at all. [More often than not,](/learn/synchronizing-with-effects#how-to-handle-the-effect-firing-twice-in-development) you’ll want to return one—but if you don’t, React will behave as if you returned an empty cleanup function.

### Why synchronization may need to happen more than once[](#why-synchronization-may-need-to-happen-more-than-once "Link for Why synchronization may need to happen more than once ")

Imagine this `ChatRoom` component receives a `roomId` prop that the user picks in a dropdown. Let’s say that initially the user picks the `"general"` room as the `roomId`. Your app displays the `"general"` chat room:

```
const serverUrl = 'https://localhost:1234';



function ChatRoom({ roomId /* "general" */ }) {

  // ...

  return <h1>Welcome to the {roomId} room!</h1>;

}
```

After the UI is displayed, React will run your Effect to **start synchronizing.** It connects to the `"general"` room:

```
function ChatRoom({ roomId /* "general" */ }) {

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId); // Connects to the "general" room

    connection.connect();

    return () => {

      connection.disconnect(); // Disconnects from the "general" room

    };

  }, [roomId]);

  // ...
```

So far, so good.

Later, the user picks a different room in the dropdown (for example, `"travel"`). First, React will update the UI:

```
function ChatRoom({ roomId /* "travel" */ }) {

  // ...

  return <h1>Welcome to the {roomId} room!</h1>;

}
```

```
function ChatRoom({ roomId /* "general" */ }) {

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId); // Connects to the "general" room

    connection.connect();

    return () => {

      connection.disconnect(); // Disconnects from the "general" room

    };

    // ...
```

Then React will run the Effect that you’ve provided during this render. This time, `roomId` is `"travel"` so it will **start synchronizing** to the `"travel"` chat room (until its cleanup function is eventually called too):

```
function ChatRoom({ roomId /* "travel" */ }) {

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId); // Connects to the "travel" room

    connection.connect();

    // ...
```

```
  useEffect(() => {

    // Your Effect connected to the room specified with roomId...

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      // ...until it disconnected

      connection.disconnect();

    };

  }, [roomId]);
```

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);
  return <h1>Welcome to the {roomId} room!</h1>;
}

export default function App() {
  const [roomId, setRoomId] = useState('general');
  const [show, setShow] = useState(false);
  return (
    <>
      <label>
        Choose the chat room:{' '}
        <select
          value={roomId}
          onChange={e => setRoomId(e.target.value)}
        >
          <option value="general">general</option>
          <option value="travel">travel</option>
          <option value="music">music</option>
        </select>
      </label>
      <button onClick={() => setShow(!show)}>
        {show ? 'Close chat' : 'Open chat'}
      </button>
      {show && <hr />}
      {show && <ChatRoom roomId={roomId} />}
    </>
  );
}
```

```
function ChatRoom({ roomId }) { // The roomId prop may change over time

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId); // This Effect reads roomId 

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, [roomId]); // So you tell React that this Effect "depends on" roomId

  // ...
```

```
function ChatRoom({ roomId }) {

  useEffect(() => {

    logVisit(roomId);

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, [roomId]);

  // ...

}
```

But imagine you later add another dependency to this Effect that needs to re-establish the connection. If this Effect re-synchronizes, it will also call `logVisit(roomId)` for the same room, which you did not intend. Logging the visit **is a separate process** from connecting. Write them as two separate Effects:

```
function ChatRoom({ roomId }) {

  useEffect(() => {

    logVisit(roomId);

  }, [roomId]);



  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    // ...

  }, [roomId]);

  // ...

}
```

**Each Effect in your code should represent a separate and independent synchronization process.**

In the above example, deleting one Effect wouldn’t break the other Effect’s logic. This is a good indication that they synchronize different things, and so it made sense to split them up. On the other hand, if you split up a cohesive piece of logic into separate Effects, the code may look “cleaner” but will be [more difficult to maintain.](/learn/you-might-not-need-an-effect#chains-of-computations) This is why you should think whether the processes are same or separate, not whether the code looks cleaner.

## Effects “react” to reactive values[](#effects-react-to-reactive-values "Link for Effects “react” to reactive values ")

Your Effect reads two variables (`serverUrl` and `roomId`), but you only specified `roomId` as a dependency:

```
const serverUrl = 'https://localhost:1234';



function ChatRoom({ roomId }) {

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, [roomId]);

  // ...

}
```

Why doesn’t `serverUrl` need to be a dependency?

This is because the `serverUrl` never changes due to a re-render. It’s always the same no matter how many times the component re-renders and why. Since `serverUrl` never changes, it wouldn’t make sense to specify it as a dependency. After all, dependencies only do something when they change over time!

On the other hand, `roomId` may be different on a re-render. **Props, state, and other values declared inside the component are *reactive* because they’re calculated during rendering and participate in the React data flow.**

If `serverUrl` was a state variable, it would be reactive. Reactive values must be included in dependencies:

```
function ChatRoom({ roomId }) { // Props change over time

  const [serverUrl, setServerUrl] = useState('https://localhost:1234'); // State may change over time



  useEffect(() => {

    const connection = createConnection(serverUrl, roomId); // Your Effect reads props and state

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, [roomId, serverUrl]); // So you tell React that this Effect "depends on" on props and state

  // ...

}
```

By including `serverUrl` as a dependency, you ensure that the Effect re-synchronizes after it changes.

Try changing the selected chat room or edit the server URL in this sandbox:

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

function ChatRoom({ roomId }) {
  const [serverUrl, setServerUrl] = useState('https://localhost:1234');

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId, serverUrl]);

  return (
    <>
      <label>
        Server URL:{' '}
        <input
          value={serverUrl}
          onChange={e => setServerUrl(e.target.value)}
        />
      </label>
      <h1>Welcome to the {roomId} room!</h1>
    </>
  );
}

export default function App() {
  const [roomId, setRoomId] = useState('general');
  return (
    <>
      <label>
        Choose the chat room:{' '}
        <select
          value={roomId}
          onChange={e => setRoomId(e.target.value)}
        >
          <option value="general">general</option>
          <option value="travel">travel</option>
          <option value="music">music</option>
        </select>
      </label>
      <hr />
      <ChatRoom roomId={roomId} />
    </>
  );
}
```

Whenever you change a reactive value like `roomId` or `serverUrl`, the Effect re-connects to the chat server.

### What an Effect with empty dependencies means[](#what-an-effect-with-empty-dependencies-means "Link for What an Effect with empty dependencies means ")

What happens if you move both `serverUrl` and `roomId` outside the component?

```
const serverUrl = 'https://localhost:1234';

const roomId = 'general';



function ChatRoom() {

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, []); // ✅ All dependencies declared

  // ...

}
```

Now your Effect’s code does not use *any* reactive values, so its dependencies can be empty (`[]`).

Thinking from the component’s perspective, the empty `[]` dependency array means this Effect connects to the chat room only when the component mounts, and disconnects only when the component unmounts. (Keep in mind that React would still [re-synchronize it an extra time](#how-react-verifies-that-your-effect-can-re-synchronize) in development to stress-test your logic.)

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

const serverUrl = 'https://localhost:1234';
const roomId = 'general';

function ChatRoom() {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, []);
  return <h1>Welcome to the {roomId} room!</h1>;
}

export default function App() {
  const [show, setShow] = useState(false);
  return (
    <>
      <button onClick={() => setShow(!show)}>
        {show ? 'Close chat' : 'Open chat'}
      </button>
      {show && <hr />}
      {show && <ChatRoom />}
    </>
  );
}
```

However, if you [think from the Effect’s perspective,](#thinking-from-the-effects-perspective) you don’t need to think about mounting and unmounting at all. What’s important is you’ve specified what your Effect does to start and stop synchronizing. Today, it has no reactive dependencies. But if you ever want the user to change `roomId` or `serverUrl` over time (and they would become reactive), your Effect’s code won’t change. You will only need to add them to the dependencies.

### All variables declared in the component body are reactive[](#all-variables-declared-in-the-component-body-are-reactive "Link for All variables declared in the component body are reactive ")

Props and state aren’t the only reactive values. Values that you calculate from them are also reactive. If the props or state change, your component will re-render, and the values calculated from them will also change. This is why all variables from the component body used by the Effect should be in the Effect dependency list.

Let’s say that the user can pick a chat server in the dropdown, but they can also configure a default server in settings. Suppose you’ve already put the settings state in a [context](/learn/scaling-up-with-reducer-and-context) so you read the `settings` from that context. Now you calculate the `serverUrl` based on the selected server from props and the default server:

```
function ChatRoom({ roomId, selectedServerUrl }) { // roomId is reactive

  const settings = useContext(SettingsContext); // settings is reactive

  const serverUrl = selectedServerUrl ?? settings.defaultServerUrl; // serverUrl is reactive

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId); // Your Effect reads roomId and serverUrl

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, [roomId, serverUrl]); // So it needs to re-synchronize when either of them changes!

  // ...

}
```

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

function ChatRoom({ roomId }) { // roomId is reactive
  const [serverUrl, setServerUrl] = useState('https://localhost:1234'); // serverUrl is reactive

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, []); // <-- Something's wrong here!

  return (
    <>
      <label>
        Server URL:{' '}
        <input
          value={serverUrl}
          onChange={e => setServerUrl(e.target.value)}
        />
      </label>
      <h1>Welcome to the {roomId} room!</h1>
    </>
  );
}

export default function App() {
  const [roomId, setRoomId] = useState('general');
  return (
    <>
      <label>
        Choose the chat room:{' '}
        <select
          value={roomId}
          onChange={e => setRoomId(e.target.value)}
        >
          <option value="general">general</option>
          <option value="travel">travel</option>
          <option value="music">music</option>
        </select>
      </label>
      <hr />
      <ChatRoom roomId={roomId} />
    </>
  );
}
```

This may look like a React error, but really React is pointing out a bug in your code. Both `roomId` and `serverUrl` may change over time, but you’re forgetting to re-synchronize your Effect when they change. You will remain connected to the initial `roomId` and `serverUrl` even after the user picks different values in the UI.

To fix the bug, follow the linter’s suggestion to specify `roomId` and `serverUrl` as dependencies of your Effect:

```
function ChatRoom({ roomId }) { // roomId is reactive

  const [serverUrl, setServerUrl] = useState('https://localhost:1234'); // serverUrl is reactive

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, [serverUrl, roomId]); // ✅ All dependencies declared

  // ...

}
```

Try this fix in the sandbox above. Verify that the linter error is gone, and the chat re-connects when needed.

### Note

In some cases, React *knows* that a value never changes even though it’s declared inside the component. For example, the [`set` function](/reference/react/useState#setstate) returned from `useState` and the ref object returned by [`useRef`](/reference/react/useRef) are *stable*—they are guaranteed to not change on a re-render. Stable values aren’t reactive, so you may omit them from the list. Including them is allowed: they won’t change, so it doesn’t matter.

### What to do when you don’t want to re-synchronize[](#what-to-do-when-you-dont-want-to-re-synchronize "Link for What to do when you don’t want to re-synchronize ")

In the previous example, you’ve fixed the lint error by listing `roomId` and `serverUrl` as dependencies.

**However, you could instead “prove” to the linter that these values aren’t reactive values,** i.e. that they *can’t* change as a result of a re-render. For example, if `serverUrl` and `roomId` don’t depend on rendering and always have the same values, you can move them outside the component. Now they don’t need to be dependencies:

```
const serverUrl = 'https://localhost:1234'; // serverUrl is not reactive

const roomId = 'general'; // roomId is not reactive



function ChatRoom() {

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, []); // ✅ All dependencies declared

  // ...

}
```

You can also move them *inside the Effect.* They aren’t calculated during rendering, so they’re not reactive:

```
function ChatRoom() {

  useEffect(() => {

    const serverUrl = 'https://localhost:1234'; // serverUrl is not reactive

    const roomId = 'general'; // roomId is not reactive

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, []); // ✅ All dependencies declared

  // ...

}
```

```
useEffect(() => {

  // ...

  // 🔴 Avoid suppressing the linter like this:

  // eslint-ignore-next-line react-hooks/exhaustive-deps

}, []);
```

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  });

  return (
    <>
      <h1>Welcome to the {roomId} room!</h1>
      <input
        value={message}
        onChange={e => setMessage(e.target.value)}
      />
    </>
  );
}

export default function App() {
  const [roomId, setRoomId] = useState('general');
  return (
    <>
      <label>
        Choose the chat room:{' '}
        <select
          value={roomId}
          onChange={e => setRoomId(e.target.value)}
        >
          <option value="general">general</option>
          <option value="travel">travel</option>
          <option value="music">music</option>
        </select>
      </label>
      <hr />
      <ChatRoom roomId={roomId} />
    </>
  );
}
```

[PreviousYou Might Not Need an Effect](/learn/you-might-not-need-an-effect)

[NextSeparating Events from Effects](/learn/separating-events-from-effects)

***

----
