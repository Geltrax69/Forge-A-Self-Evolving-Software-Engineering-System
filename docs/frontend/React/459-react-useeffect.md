url: https://18.react.dev/reference/react/useEffect
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useEffect[](#undefined "Link for this heading")

`useEffect` is a React Hook that lets you [synchronize a component with an external system.](/learn/synchronizing-with-effects)

```
useEffect(setup, dependencies?)
```

***

## Reference[](#reference "Link for Reference ")

### `useEffect(setup, dependencies?)`[](#useeffect "Link for this heading")

Call `useEffect` at the top level of your component to declare an Effect:

```
import { useEffect } from 'react';

import { createConnection } from './chat.js';



function ChatRoom({ roomId }) {

  const [serverUrl, setServerUrl] = useState('https://localhost:1234');



  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, [serverUrl, roomId]);

  // ...

}
```

[See more examples below.](#usage)

#### Parameters[](#parameters "Link for Parameters ")

* `setup`: The function with your Effect’s logic. Your setup function may also optionally return a *cleanup* function. When your component is added to the DOM, React will run your setup function. After every re-render with changed dependencies, React will first run the cleanup function (if you provided it) with the old values, and then run your setup function with the new values. After your component is removed from the DOM, React will run your cleanup function.

* **optional** `dependencies`: The list of all reactive values referenced inside of the `setup` code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is [configured for React](/learn/editor-setup#linting), it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like `[dep1, dep2, dep3]`. React will compare each dependency with its previous value using the [`Object.is`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. If you omit this argument, your Effect will re-run after every re-render of the component. [See the difference between passing an array of dependencies, an empty array, and no dependencies at all.](#examples-dependencies)

***

## Usage[](#usage "Link for Usage ")

### Connecting to an external system[](#connecting-to-an-external-system "Link for Connecting to an external system ")

Some components need to stay connected to the network, some browser API, or a third-party library, while they are displayed on the page. These systems aren’t controlled by React, so they are called *external.*

To [connect your component to some external system,](/learn/synchronizing-with-effects) call `useEffect` at the top level of your component:

```
import { useEffect } from 'react';

import { createConnection } from './chat.js';



function ChatRoom({ roomId }) {

  const [serverUrl, setServerUrl] = useState('https://localhost:1234');



  useEffect(() => {

  	const connection = createConnection(serverUrl, roomId);

    connection.connect();

  	return () => {

      connection.disconnect();

  	};

  }, [serverUrl, roomId]);

  // ...

}
```

You need to pass two arguments to `useEffect`:

1. A *setup function* with setup code that connects to that system.
   * It should return a *cleanup function* with cleanup code that disconnects from that system.
2. A list of dependencies including every value from your component used inside of those functions.

**React calls your setup and cleanup functions whenever it’s necessary, which may happen multiple times:**

1. Your setup code runs when your component is added to the page *(mounts)*.

2. After every re-render of your component where the dependencies have changed:

   * First, your cleanup code runs with the old props and state.
   * Then, your setup code runs with the new props and state.

3. Your cleanup code runs one final time after your component is removed from the page *(unmounts).*

**Let’s illustrate this sequence for the example above.**

When the `ChatRoom` component above gets added to the page, it will connect to the chat room with the initial `serverUrl` and `roomId`. If either `serverUrl` or `roomId` change as a result of a re-render (say, if the user picks a different chat room in a dropdown), your Effect will *disconnect from the previous room, and connect to the next one.* When the `ChatRoom` component is removed from the page, your Effect will disconnect one last time.

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

function ChatRoom({ roomId }) {
  const [serverUrl, setServerUrl] = useState('https://localhost:1234');

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
      connection.disconnect();
    };
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

***

### Wrapping Effects in custom Hooks[](#wrapping-effects-in-custom-hooks "Link for Wrapping Effects in custom Hooks ")

Effects are an [“escape hatch”:](/learn/escape-hatches) you use them when you need to “step outside React” and when there is no better built-in solution for your use case. If you find yourself often needing to manually write Effects, it’s usually a sign that you need to extract some [custom Hooks](/learn/reusing-logic-with-custom-hooks) for common behaviors your components rely on.

For example, this `useChatRoom` custom Hook “hides” the logic of your Effect behind a more declarative API:

```
function useChatRoom({ serverUrl, roomId }) {

  useEffect(() => {

    const options = {

      serverUrl: serverUrl,

      roomId: roomId

    };

    const connection = createConnection(options);

    connection.connect();

    return () => connection.disconnect();

  }, [roomId, serverUrl]);

}
```

Then you can use it from any component like this:

```
function ChatRoom({ roomId }) {

  const [serverUrl, setServerUrl] = useState('https://localhost:1234');



  useChatRoom({

    roomId: roomId,

    serverUrl: serverUrl

  });

  // ...
```

There are also many excellent custom Hooks for every purpose available in the React ecosystem.

[Learn more about wrapping Effects in custom Hooks.](/learn/reusing-logic-with-custom-hooks)

#### Examples of wrapping Effects in custom Hooks[](#examples-custom-hooks "Link for Examples of wrapping Effects in custom Hooks")

#### Example 1 of 3:Custom `useChatRoom` Hook[](#custom-usechatroom-hook "Link for this heading")

This example is identical to one of the [earlier examples,](#examples-connecting) but the logic is extracted to a custom Hook.

```
import { useState } from 'react';
import { useChatRoom } from './useChatRoom.js';

function ChatRoom({ roomId }) {
  const [serverUrl, setServerUrl] = useState('https://localhost:1234');

  useChatRoom({
    roomId: roomId,
    serverUrl: serverUrl
  });

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

***

### Controlling a non-React widget[](#controlling-a-non-react-widget "Link for Controlling a non-React widget ")

Sometimes, you want to keep an external system synchronized to some prop or state of your component.

For example, if you have a third-party map widget or a video player component written without React, you can use an Effect to call methods on it that make its state match the current state of your React component. This Effect creates an instance of a `MapWidget` class defined in `map-widget.js`. When you change the `zoomLevel` prop of the `Map` component, the Effect calls the `setZoom()` on the class instance to keep it synchronized:

```
import { useRef, useEffect } from 'react';
import { MapWidget } from './map-widget.js';

export default function Map({ zoomLevel }) {
  const containerRef = useRef(null);
  const mapRef = useRef(null);

  useEffect(() => {
    if (mapRef.current === null) {
      mapRef.current = new MapWidget(containerRef.current);
    }

    const map = mapRef.current;
    map.setZoom(zoomLevel);
  }, [zoomLevel]);

  return (
    <div
      style={{ width: 200, height: 200 }}
      ref={containerRef}
    />
  );
}
```

In this example, a cleanup function is not needed because the `MapWidget` class manages only the DOM node that was passed to it. After the `Map` React component is removed from the tree, both the DOM node and the `MapWidget` class instance will be automatically garbage-collected by the browser JavaScript engine.

***

### Fetching data with Effects[](#fetching-data-with-effects "Link for Fetching data with Effects ")

You can use an Effect to fetch data for your component. Note that [if you use a framework,](/learn/start-a-new-react-project#production-grade-react-frameworks) using your framework’s data fetching mechanism will be a lot more efficient than writing Effects manually.

If you want to fetch data from an Effect manually, your code might look like this:

```
import { useState, useEffect } from 'react';

import { fetchBio } from './api.js';



export default function Page() {

  const [person, setPerson] = useState('Alice');

  const [bio, setBio] = useState(null);



  useEffect(() => {

    let ignore = false;

    setBio(null);

    fetchBio(person).then(result => {

      if (!ignore) {

        setBio(result);

      }

    });

    return () => {

      ignore = true;

    };

  }, [person]);



  // ...
```

Note the `ignore` variable which is initialized to `false`, and is set to `true` during cleanup. This ensures [your code doesn’t suffer from “race conditions”:](https://maxrozen.com/race-conditions-fetching-data-react-with-useeffect) network responses may arrive in a different order than you sent them.

```
import { useState, useEffect } from 'react';
import { fetchBio } from './api.js';

export default function Page() {
  const [person, setPerson] = useState('Alice');
  const [bio, setBio] = useState(null);
  useEffect(() => {
    let ignore = false;
    setBio(null);
    fetchBio(person).then(result => {
      if (!ignore) {
        setBio(result);
      }
    });
    return () => {
      ignore = true;
    }
  }, [person]);

  return (
    <>
      <select value={person} onChange={e => {
        setPerson(e.target.value);
      }}>
        <option value="Alice">Alice</option>
        <option value="Bob">Bob</option>
        <option value="Taylor">Taylor</option>
      </select>
      <hr />
      <p><i>{bio ?? 'Loading...'}</i></p>
    </>
  );
}
```

You can also rewrite using the [`async` / `await`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) syntax, but you still need to provide a cleanup function:

```
import { useState, useEffect } from 'react';
import { fetchBio } from './api.js';

export default function Page() {
  const [person, setPerson] = useState('Alice');
  const [bio, setBio] = useState(null);
  useEffect(() => {
    async function startFetching() {
      setBio(null);
      const result = await fetchBio(person);
      if (!ignore) {
        setBio(result);
      }
    }

    let ignore = false;
    startFetching();
    return () => {
      ignore = true;
    }
  }, [person]);

  return (
    <>
      <select value={person} onChange={e => {
        setPerson(e.target.value);
      }}>
        <option value="Alice">Alice</option>
        <option value="Bob">Bob</option>
        <option value="Taylor">Taylor</option>
      </select>
      <hr />
      <p><i>{bio ?? 'Loading...'}</i></p>
    </>
  );
}
```

* **If you use a [framework](/learn/start-a-new-react-project#production-grade-react-frameworks), use its built-in data fetching mechanism.** Modern React frameworks have integrated data fetching mechanisms that are efficient and don’t suffer from the above pitfalls.
* **Otherwise, consider using or building a client-side cache.** Popular open source solutions include [React Query](https://tanstack.com/query/latest/), [useSWR](https://swr.vercel.app/), and [React Router 6.4+.](https://beta.reactrouter.com/en/main/start/overview) You can build your own solution too, in which case you would use Effects under the hood but also add logic for deduplicating requests, caching responses, and avoiding network waterfalls (by preloading data or hoisting data requirements to routes).

You can continue fetching data directly in Effects if neither of these approaches suit you.

***

### Specifying reactive dependencies[](#specifying-reactive-dependencies "Link for Specifying reactive dependencies ")

**Notice that you can’t “choose” the dependencies of your Effect.** Every reactive value used by your Effect’s code must be declared as a dependency. Your Effect’s dependency list is determined by the surrounding code:

```
function ChatRoom({ roomId }) { // This is a reactive value

  const [serverUrl, setServerUrl] = useState('https://localhost:1234'); // This is a reactive value too



  useEffect(() => {

    const connection = createConnection(serverUrl, roomId); // This Effect reads these reactive values

    connection.connect();

    return () => connection.disconnect();

  }, [serverUrl, roomId]); // ✅ So you must specify them as dependencies of your Effect

  // ...

}
```

If either `serverUrl` or `roomId` change, your Effect will reconnect to the chat using the new values.

**[Reactive values](/learn/lifecycle-of-reactive-effects#effects-react-to-reactive-values) include props and all variables and functions declared directly inside of your component.** Since `roomId` and `serverUrl` are reactive values, you can’t remove them from the dependencies. If you try to omit them and [your linter is correctly configured for React,](/learn/editor-setup#linting) the linter will flag this as a mistake you need to fix:

```
function ChatRoom({ roomId }) {

  const [serverUrl, setServerUrl] = useState('https://localhost:1234');

  

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => connection.disconnect();

  }, []); // 🔴 React Hook useEffect has missing dependencies: 'roomId' and 'serverUrl'

  // ...

}
```

**To remove a dependency, you need to [“prove” to the linter that it *doesn’t need* to be a dependency.](/learn/removing-effect-dependencies#removing-unnecessary-dependencies)** For example, you can move `serverUrl` out of your component to prove that it’s not reactive and won’t change on re-renders:

```
const serverUrl = 'https://localhost:1234'; // Not a reactive value anymore



function ChatRoom({ roomId }) {

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => connection.disconnect();

  }, [roomId]); // ✅ All dependencies declared

  // ...

}
```

Now that `serverUrl` is not a reactive value (and can’t change on a re-render), it doesn’t need to be a dependency. **If your Effect’s code doesn’t use any reactive values, its dependency list should be empty (`[]`):**

```
const serverUrl = 'https://localhost:1234'; // Not a reactive value anymore

const roomId = 'music'; // Not a reactive value anymore



function ChatRoom() {

  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => connection.disconnect();

  }, []); // ✅ All dependencies declared

  // ...

}
```

[An Effect with empty dependencies](/learn/lifecycle-of-reactive-effects#what-an-effect-with-empty-dependencies-means) doesn’t re-run when any of your component’s props or state change.

### Pitfall

If you have an existing codebase, you might have some Effects that suppress the linter like this:

```
useEffect(() => {

  // ...

  // 🔴 Avoid suppressing the linter like this:

  // eslint-ignore-next-line react-hooks/exhaustive-deps

}, []);
```

**When dependencies don’t match the code, there is a high risk of introducing bugs.** By suppressing the linter, you “lie” to React about the values your Effect depends on. [Instead, prove they’re unnecessary.](/learn/removing-effect-dependencies#removing-unnecessary-dependencies)

#### Examples of passing reactive dependencies[](#examples-dependencies "Link for Examples of passing reactive dependencies")

#### Example 1 of 3:Passing a dependency array[](#passing-a-dependency-array "Link for this heading")

If you specify the dependencies, your Effect runs **after the initial render *and* after re-renders with changed dependencies.**

```
useEffect(() => {

  // ...

}, [a, b]); // Runs again if a or b are different
```

In the below example, `serverUrl` and `roomId` are [reactive values,](/learn/lifecycle-of-reactive-effects#effects-react-to-reactive-values) so they both must be specified as dependencies. As a result, selecting a different room in the dropdown or editing the server URL input causes the chat to re-connect. However, since `message` isn’t used in the Effect (and so it isn’t a dependency), editing the message doesn’t re-connect to the chat.

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

function ChatRoom({ roomId }) {
  const [serverUrl, setServerUrl] = useState('https://localhost:1234');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, [serverUrl, roomId]);

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
      <label>
        Your message:{' '}
        <input value={message} onChange={e => setMessage(e.target.value)} />
      </label>
    </>
  );
}

export default function App() {
  const [show, setShow] = useState(false);
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
        <button onClick={() => setShow(!show)}>
          {show ? 'Close chat' : 'Open chat'}
        </button>
      </label>
      {show && <hr />}
      {show && <ChatRoom roomId={roomId}/>}
    </>
  );
}
```

***

### Updating state based on previous state from an Effect[](#updating-state-based-on-previous-state-from-an-effect "Link for Updating state based on previous state from an Effect ")

When you want to update state based on previous state from an Effect, you might run into a problem:

```
function Counter() {

  const [count, setCount] = useState(0);



  useEffect(() => {

    const intervalId = setInterval(() => {

      setCount(count + 1); // You want to increment the counter every second...

    }, 1000)

    return () => clearInterval(intervalId);

  }, [count]); // 🚩 ... but specifying `count` as a dependency always resets the interval.

  // ...

}
```

Since `count` is a reactive value, it must be specified in the list of dependencies. However, that causes the Effect to cleanup and setup again every time the `count` changes. This is not ideal.

To fix this, [pass the `c => c + 1` state updater](/reference/react/useState#updating-state-based-on-the-previous-state) to `setCount`:

```
import { useState, useEffect } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCount(c => c + 1); // ✅ Pass a state updater
    }, 1000);
    return () => clearInterval(intervalId);
  }, []); // ✅ Now count is not a dependency

  return <h1>{count}</h1>;
}
```

Now that you’re passing `c => c + 1` instead of `count + 1`, [your Effect no longer needs to depend on `count`.](/learn/removing-effect-dependencies#are-you-reading-some-state-to-calculate-the-next-state) As a result of this fix, it won’t need to cleanup and setup the interval again every time the `count` changes.

***

### Removing unnecessary object dependencies[](#removing-unnecessary-object-dependencies "Link for Removing unnecessary object dependencies ")

If your Effect depends on an object or a function created during rendering, it might run too often. For example, this Effect re-connects after every render because the `options` object is [different for every render:](/learn/removing-effect-dependencies#does-some-reactive-value-change-unintentionally)

```
const serverUrl = 'https://localhost:1234';



function ChatRoom({ roomId }) {

  const [message, setMessage] = useState('');



  const options = { // 🚩 This object is created from scratch on every re-render

    serverUrl: serverUrl,

    roomId: roomId

  };



  useEffect(() => {

    const connection = createConnection(options); // It's used inside the Effect

    connection.connect();

    return () => connection.disconnect();

  }, [options]); // 🚩 As a result, these dependencies are always different on a re-render

  // ...
```

Avoid using an object created during rendering as a dependency. Instead, create the object inside the Effect:

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const options = {
      serverUrl: serverUrl,
      roomId: roomId
    };
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);

  return (
    <>
      <h1>Welcome to the {roomId} room!</h1>
      <input value={message} onChange={e => setMessage(e.target.value)} />
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

Now that you create the `options` object inside the Effect, the Effect itself only depends on the `roomId` string.

With this fix, typing into the input doesn’t reconnect the chat. Unlike an object which gets re-created, a string like `roomId` doesn’t change unless you set it to another value. [Read more about removing dependencies.](/learn/removing-effect-dependencies)

***

### Removing unnecessary function dependencies[](#removing-unnecessary-function-dependencies "Link for Removing unnecessary function dependencies ")

If your Effect depends on an object or a function created during rendering, it might run too often. For example, this Effect re-connects after every render because the `createOptions` function is [different for every render:](/learn/removing-effect-dependencies#does-some-reactive-value-change-unintentionally)

```
function ChatRoom({ roomId }) {

  const [message, setMessage] = useState('');



  function createOptions() { // 🚩 This function is created from scratch on every re-render

    return {

      serverUrl: serverUrl,

      roomId: roomId

    };

  }



  useEffect(() => {

    const options = createOptions(); // It's used inside the Effect

    const connection = createConnection();

    connection.connect();

    return () => connection.disconnect();

  }, [createOptions]); // 🚩 As a result, these dependencies are always different on a re-render

  // ...
```

By itself, creating a function from scratch on every re-render is not a problem. You don’t need to optimize that. However, if you use it as a dependency of your Effect, it will cause your Effect to re-run after every re-render.

Avoid using a function created during rendering as a dependency. Instead, declare it inside the Effect:

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  const [message, setMessage] = useState('');

  useEffect(() => {
    function createOptions() {
      return {
        serverUrl: serverUrl,
        roomId: roomId
      };
    }

    const options = createOptions();
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);

  return (
    <>
      <h1>Welcome to the {roomId} room!</h1>
      <input value={message} onChange={e => setMessage(e.target.value)} />
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

Now that you define the `createOptions` function inside the Effect, the Effect itself only depends on the `roomId` string. With this fix, typing into the input doesn’t reconnect the chat. Unlike a function which gets re-created, a string like `roomId` doesn’t change unless you set it to another value. [Read more about removing dependencies.](/learn/removing-effect-dependencies)

***

### Reading the latest props and state from an Effect[](#reading-the-latest-props-and-state-from-an-effect "Link for Reading the latest props and state from an Effect ")

### Under Construction

This section describes an **experimental API that has not yet been released** in a stable version of React.

By default, when you read a reactive value from an Effect, you have to add it as a dependency. This ensures that your Effect “reacts” to every change of that value. For most dependencies, that’s the behavior you want.

**However, sometimes you’ll want to read the *latest* props and state from an Effect without “reacting” to them.** For example, imagine you want to log the number of the items in the shopping cart for every page visit:

```
function Page({ url, shoppingCart }) {

  useEffect(() => {

    logVisit(url, shoppingCart.length);

  }, [url, shoppingCart]); // ✅ All dependencies declared

  // ...

}
```

**What if you want to log a new page visit after every `url` change, but *not* if only the `shoppingCart` changes?** You can’t exclude `shoppingCart` from dependencies without breaking the [reactivity rules.](#specifying-reactive-dependencies) However, you can express that you *don’t want* a piece of code to “react” to changes even though it is called from inside an Effect. [Declare an *Effect Event*](/learn/separating-events-from-effects#declaring-an-effect-event) with the [`useEffectEvent`](/reference/react/experimental_useEffectEvent) Hook, and move the code reading `shoppingCart` inside of it:

```
function Page({ url, shoppingCart }) {

  const onVisit = useEffectEvent(visitedUrl => {

    logVisit(visitedUrl, shoppingCart.length)

  });



  useEffect(() => {

    onVisit(url);

  }, [url]); // ✅ All dependencies declared

  // ...

}
```

**Effect Events are not reactive and must always be omitted from dependencies of your Effect.** This is what lets you put non-reactive code (where you can read the latest value of some props and state) inside of them. By reading `shoppingCart` inside of `onVisit`, you ensure that `shoppingCart` won’t re-run your Effect.

[Read more about how Effect Events let you separate reactive and non-reactive code.](/learn/separating-events-from-effects#reading-latest-props-and-state-with-effect-events)

***

### Displaying different content on the server and the client[](#displaying-different-content-on-the-server-and-the-client "Link for Displaying different content on the server and the client ")

If your app uses server rendering (either [directly](/reference/react-dom/server) or via a [framework](/learn/start-a-new-react-project#production-grade-react-frameworks)), your component will render in two different environments. On the server, it will render to produce the initial HTML. On the client, React will run the rendering code again so that it can attach your event handlers to that HTML. This is why, for [hydration](/reference/react-dom/client/hydrateRoot#hydrating-server-rendered-html) to work, your initial render output must be identical on the client and the server.

In rare cases, you might need to display different content on the client. For example, if your app reads some data from [`localStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage), it can’t possibly do that on the server. Here is how you could implement this:

```
function MyComponent() {

  const [didMount, setDidMount] = useState(false);



  useEffect(() => {

    setDidMount(true);

  }, []);



  if (didMount) {

    // ... return client-only JSX ...

  }  else {

    // ... return initial JSX ...

  }

}
```

While the app is loading, the user will see the initial render output. Then, when it’s loaded and hydrated, your Effect will run and set `didMount` to `true`, triggering a re-render. This will switch to the client-only render output. Effects don’t run on the server, so this is why `didMount` was `false` during the initial server render.

Use this pattern sparingly. Keep in mind that users with a slow connection will see the initial content for quite a bit of time—potentially, many seconds—so you don’t want to make jarring changes to your component’s appearance. In many cases, you can avoid the need for this by conditionally showing different things with CSS.

***

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### My Effect runs twice when the component mounts[](#my-effect-runs-twice-when-the-component-mounts "Link for My Effect runs twice when the component mounts ")

When Strict Mode is on, in development, React runs setup and cleanup one extra time before the actual setup.

This is a stress-test that verifies your Effect’s logic is implemented correctly. If this causes visible issues, your cleanup function is missing some logic. The cleanup function should stop or undo whatever the setup function was doing. The rule of thumb is that the user shouldn’t be able to distinguish between the setup being called once (as in production) and a setup → cleanup → setup sequence (as in development).

Read more about [how this helps find bugs](/learn/synchronizing-with-effects#step-3-add-cleanup-if-needed) and [how to fix your logic.](/learn/synchronizing-with-effects#how-to-handle-the-effect-firing-twice-in-development)

***

### My Effect runs after every re-render[](#my-effect-runs-after-every-re-render "Link for My Effect runs after every re-render ")

First, check that you haven’t forgotten to specify the dependency array:

```
useEffect(() => {

  // ...

}); // 🚩 No dependency array: re-runs after every render!
```

If you’ve specified the dependency array but your Effect still re-runs in a loop, it’s because one of your dependencies is different on every re-render.

You can debug this problem by manually logging your dependencies to the console:

```
  useEffect(() => {

    // ..

  }, [serverUrl, roomId]);



  console.log([serverUrl, roomId]);
```

You can then right-click on the arrays from different re-renders in the console and select “Store as a global variable” for both of them. Assuming the first one got saved as `temp1` and the second one got saved as `temp2`, you can then use the browser console to check whether each dependency in both arrays is the same:

```
Object.is(temp1[0], temp2[0]); // Is the first dependency the same between the arrays?

Object.is(temp1[1], temp2[1]); // Is the second dependency the same between the arrays?

Object.is(temp1[2], temp2[2]); // ... and so on for every dependency ...
```

When you find the dependency that is different on every re-render, you can usually fix it in one of these ways:

* [Updating state based on previous state from an Effect](#updating-state-based-on-previous-state-from-an-effect)
* [Removing unnecessary object dependencies](#removing-unnecessary-object-dependencies)
* [Removing unnecessary function dependencies](#removing-unnecessary-function-dependencies)
* [Reading the latest props and state from an Effect](#reading-the-latest-props-and-state-from-an-effect)

As a last resort (if these methods didn’t help), wrap its creation with [`useMemo`](/reference/react/useMemo#memoizing-a-dependency-of-another-hook) or [`useCallback`](/reference/react/useCallback#preventing-an-effect-from-firing-too-often) (for functions).

***

***

### My cleanup logic runs even though my component didn’t unmount[](#my-cleanup-logic-runs-even-though-my-component-didnt-unmount "Link for My cleanup logic runs even though my component didn’t unmount ")

The cleanup function runs not only during unmount, but before every re-render with changed dependencies. Additionally, in development, React [runs setup+cleanup one extra time immediately after component mounts.](#my-effect-runs-twice-when-the-component-mounts)

If you have cleanup code without corresponding setup code, it’s usually a code smell:

```
useEffect(() => {

  // 🔴 Avoid: Cleanup logic without corresponding setup logic

  return () => {

    doSomething();

  };

}, []);
```

Your cleanup logic should be “symmetrical” to the setup logic, and should stop or undo whatever setup did:

```
  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, [serverUrl, roomId]);
```

[Learn how the Effect lifecycle is different from the component’s lifecycle.](/learn/lifecycle-of-reactive-effects#the-lifecycle-of-an-effect)

***

### My Effect does something visual, and I see a flicker before it runs[](#my-effect-does-something-visual-and-i-see-a-flicker-before-it-runs "Link for My Effect does something visual, and I see a flicker before it runs ")

If your Effect must block the browser from [painting the screen,](/learn/render-and-commit#epilogue-browser-paint) replace `useEffect` with [`useLayoutEffect`](/reference/react/useLayoutEffect). Note that **this shouldn’t be needed for the vast majority of Effects.** You’ll only need this if it’s crucial to run your Effect before the browser paint: for example, to measure and position a tooltip before the user sees it.

[PrevioususeDeferredValue](/reference/react/useDeferredValue)

[NextuseId](/reference/react/useId)

***

----
