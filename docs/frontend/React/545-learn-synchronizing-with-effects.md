url: https://18.react.dev/learn/synchronizing-with-effects
----

```
import { useEffect } from 'react';
```

Then, call it at the top level of your component and put some code inside your Effect:

```
function MyComponent() {

  useEffect(() => {

    // Code here will run after *every* render

  });

  return <div />;

}
```

Every time your component renders, React will update the screen *and then* run the code inside `useEffect`. In other words, **`useEffect` “delays” a piece of code from running until that render is reflected on the screen.**

Let’s see how you can use an Effect to synchronize with an external system. Consider a `<VideoPlayer>` React component. It would be nice to control whether it’s playing or paused by passing an `isPlaying` prop to it:

```
<VideoPlayer isPlaying={isPlaying} />;
```

Your custom `VideoPlayer` component renders the built-in browser [`<video>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video) tag:

```
function VideoPlayer({ src, isPlaying }) {

  // TODO: do something with isPlaying

  return <video src={src} />;

}
```

However, the browser `<video>` tag does not have an `isPlaying` prop. The only way to control it is to manually call the [`play()`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/play) and [`pause()`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/pause) methods on the DOM element. **You need to synchronize the value of `isPlaying` prop, which tells whether the video *should* currently be playing, with calls like `play()` and `pause()`.**

We’ll need to first [get a ref](/learn/manipulating-the-dom-with-refs) to the `<video>` DOM node.

You might be tempted to try to call `play()` or `pause()` during rendering, but that isn’t correct:

```
import { useState, useRef, useEffect } from 'react';

function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);

  if (isPlaying) {
    ref.current.play();  // Calling these while rendering isn't allowed.
  } else {
    ref.current.pause(); // Also, this crashes.
  }

  return <video ref={ref} src={src} loop playsInline />;
}

export default function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  return (
    <>
      <button onClick={() => setIsPlaying(!isPlaying)}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
      <VideoPlayer
        isPlaying={isPlaying}
        src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
      />
    </>
  );
}
```

The reason this code isn’t correct is that it tries to do something with the DOM node during rendering. In React, [rendering should be a pure calculation](/learn/keeping-components-pure) of JSX and should not contain side effects like modifying the DOM.

Moreover, when `VideoPlayer` is called for the first time, its DOM does not exist yet! There isn’t a DOM node yet to call `play()` or `pause()` on, because React doesn’t know what DOM to create until you return the JSX.

The solution here is to **wrap the side effect with `useEffect` to move it out of the rendering calculation:**

```
import { useEffect, useRef } from 'react';



function VideoPlayer({ src, isPlaying }) {

  const ref = useRef(null);



  useEffect(() => {

    if (isPlaying) {

      ref.current.play();

    } else {

      ref.current.pause();

    }

  });



  return <video ref={ref} src={src} loop playsInline />;

}
```

By wrapping the DOM update in an Effect, you let React update the screen first. Then your Effect runs.

When your `VideoPlayer` component renders (either the first time or if it re-renders), a few things will happen. First, React will update the screen, ensuring the `<video>` tag is in the DOM with the right props. Then React will run your Effect. Finally, your Effect will call `play()` or `pause()` depending on the value of `isPlaying`.

Press Play/Pause multiple times and see how the video player stays synchronized to the `isPlaying` value:

```
import { useState, useRef, useEffect } from 'react';

function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);

  useEffect(() => {
    if (isPlaying) {
      ref.current.play();
    } else {
      ref.current.pause();
    }
  });

  return <video ref={ref} src={src} loop playsInline />;
}

export default function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  return (
    <>
      <button onClick={() => setIsPlaying(!isPlaying)}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
      <VideoPlayer
        isPlaying={isPlaying}
        src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
      />
    </>
  );
}
```

In this example, the “external system” you synchronized to React state was the browser media API. You can use a similar approach to wrap legacy non-React code (like jQuery plugins) into declarative React components.

Note that controlling a video player is much more complex in practice. Calling `play()` may fail, the user might play or pause using the built-in browser controls, and so on. This example is very simplified and incomplete.

### Pitfall

By default, Effects run after *every* render. This is why code like this will **produce an infinite loop:**

```
const [count, setCount] = useState(0);

useEffect(() => {

  setCount(count + 1);

});
```

```
import { useState, useRef, useEffect } from 'react';

function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);

  useEffect(() => {
    if (isPlaying) {
      console.log('Calling video.play()');
      ref.current.play();
    } else {
      console.log('Calling video.pause()');
      ref.current.pause();
    }
  });

  return <video ref={ref} src={src} loop playsInline />;
}

export default function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [text, setText] = useState('');
  return (
    <>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button onClick={() => setIsPlaying(!isPlaying)}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
      <VideoPlayer
        isPlaying={isPlaying}
        src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
      />
    </>
  );
}
```

You can tell React to **skip unnecessarily re-running the Effect** by specifying an array of *dependencies* as the second argument to the `useEffect` call. Start by adding an empty `[]` array to the above example on line 14:

```
  useEffect(() => {

    // ...

  }, []);
```

You should see an error saying `React Hook useEffect has a missing dependency: 'isPlaying'`:

```
import { useState, useRef, useEffect } from 'react';

function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);

  useEffect(() => {
    if (isPlaying) {
      console.log('Calling video.play()');
      ref.current.play();
    } else {
      console.log('Calling video.pause()');
      ref.current.pause();
    }
  }, []); // This causes an error

  return <video ref={ref} src={src} loop playsInline />;
}

export default function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [text, setText] = useState('');
  return (
    <>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button onClick={() => setIsPlaying(!isPlaying)}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
      <VideoPlayer
        isPlaying={isPlaying}
        src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
      />
    </>
  );
}
```

The problem is that the code inside of your Effect *depends on* the `isPlaying` prop to decide what to do, but this dependency was not explicitly declared. To fix this issue, add `isPlaying` to the dependency array:

```
  useEffect(() => {

    if (isPlaying) { // It's used here...

      // ...

    } else {

      // ...

    }

  }, [isPlaying]); // ...so it must be declared here!
```

Now all dependencies are declared, so there is no error. Specifying `[isPlaying]` as the dependency array tells React that it should skip re-running your Effect if `isPlaying` is the same as it was during the previous render. With this change, typing into the input doesn’t cause the Effect to re-run, but pressing Play/Pause does:

```
import { useState, useRef, useEffect } from 'react';

function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);

  useEffect(() => {
    if (isPlaying) {
      console.log('Calling video.play()');
      ref.current.play();
    } else {
      console.log('Calling video.pause()');
      ref.current.pause();
    }
  }, [isPlaying]);

  return <video ref={ref} src={src} loop playsInline />;
}

export default function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [text, setText] = useState('');
  return (
    <>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button onClick={() => setIsPlaying(!isPlaying)}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
      <VideoPlayer
        isPlaying={isPlaying}
        src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
      />
    </>
  );
}
```

The dependency array can contain multiple dependencies. React will only skip re-running the Effect if *all* of the dependencies you specify have exactly the same values as they had during the previous render. React compares the dependency values using the [`Object.is`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. See the [`useEffect` reference](/reference/react/useEffect#reference) for details.

**Notice that you can’t “choose” your dependencies.** You will get a lint error if the dependencies you specified don’t match what React expects based on the code inside your Effect. This helps catch many bugs in your code. If you don’t want some code to re-run, [*edit the Effect code itself* to not “need” that dependency.](/learn/lifecycle-of-reactive-effects#what-to-do-when-you-dont-want-to-re-synchronize)

### Pitfall

The behaviors without the dependency array and with an *empty* `[]` dependency array are different:

```
useEffect(() => {

  // This runs after every render

});



useEffect(() => {

  // This runs only on mount (when the component appears)

}, []);



useEffect(() => {

  // This runs on mount *and also* if either a or b have changed since the last render

}, [a, b]);
```

We’ll take a close look at what “mount” means in the next step.

##### Deep Dive#### Why was the ref omitted from the dependency array?[](#why-was-the-ref-omitted-from-the-dependency-array "Link for Why was the ref omitted from the dependency array? ")

This Effect uses *both* `ref` and `isPlaying`, but only `isPlaying` is declared as a dependency:

```
function VideoPlayer({ src, isPlaying }) {

  const ref = useRef(null);

  useEffect(() => {

    if (isPlaying) {

      ref.current.play();

    } else {

      ref.current.pause();

    }

  }, [isPlaying]);
```

This is because the `ref` object has a *stable identity:* React guarantees [you’ll always get the same object](/reference/react/useRef#returns) from the same `useRef` call on every render. It never changes, so it will never by itself cause the Effect to re-run. Therefore, it does not matter whether you include it or not. Including it is fine too:

```
function VideoPlayer({ src, isPlaying }) {

  const ref = useRef(null);

  useEffect(() => {

    if (isPlaying) {

      ref.current.play();

    } else {

      ref.current.pause();

    }

  }, [isPlaying, ref]);
```

The [`set` functions](/reference/react/useState#setstate) returned by `useState` also have stable identity, so you will often see them omitted from the dependencies too. If the linter lets you omit a dependency without errors, it is safe to do.

Omitting always-stable dependencies only works when the linter can “see” that the object is stable. For example, if `ref` was passed from a parent component, you would have to specify it in the dependency array. However, this is good because you can’t know whether the parent component always passes the same ref, or passes one of several refs conditionally. So your Effect *would* depend on which ref is passed.

### Step 3: Add cleanup if needed[](#step-3-add-cleanup-if-needed "Link for Step 3: Add cleanup if needed ")

Consider a different example. You’re writing a `ChatRoom` component that needs to connect to the chat server when it appears. You are given a `createConnection()` API that returns an object with `connect()` and `disconnect()` methods. How do you keep the component connected while it is displayed to the user?

Start by writing the Effect logic:

```
useEffect(() => {

  const connection = createConnection();

  connection.connect();

});
```

It would be slow to connect to the chat after every re-render, so you add the dependency array:

```
useEffect(() => {

  const connection = createConnection();

  connection.connect();

}, []);
```

**The code inside the Effect does not use any props or state, so your dependency array is `[]` (empty). This tells React to only run this code when the component “mounts”, i.e. appears on the screen for the first time.**

Let’s try running this code:

```
import { useEffect } from 'react';
import { createConnection } from './chat.js';

export default function ChatRoom() {
  useEffect(() => {
    const connection = createConnection();
    connection.connect();
  }, []);
  return <h1>Welcome to the chat!</h1>;
}
```

This Effect only runs on mount, so you might expect `"✅ Connecting..."` to be printed once in the console. **However, if you check the console, `"✅ Connecting..."` gets printed twice. Why does it happen?**

Imagine the `ChatRoom` component is a part of a larger app with many different screens. The user starts their journey on the `ChatRoom` page. The component mounts and calls `connection.connect()`. Then imagine the user navigates to another screen—for example, to the Settings page. The `ChatRoom` component unmounts. Finally, the user clicks Back and `ChatRoom` mounts again. This would set up a second connection—but the first connection was never destroyed! As the user navigates across the app, the connections would keep piling up.

Bugs like this are easy to miss without extensive manual testing. To help you spot them quickly, in development React remounts every component once immediately after its initial mount.

Seeing the `"✅ Connecting..."` log twice helps you notice the real issue: your code doesn’t close the connection when the component unmounts.

To fix the issue, return a *cleanup function* from your Effect:

```
  useEffect(() => {

    const connection = createConnection();

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, []);
```

React will call your cleanup function each time before the Effect runs again, and one final time when the component unmounts (gets removed). Let’s see what happens when the cleanup function is implemented:

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

export default function ChatRoom() {
  useEffect(() => {
    const connection = createConnection();
    connection.connect();
    return () => connection.disconnect();
  }, []);
  return <h1>Welcome to the chat!</h1>;
}
```

```
  const connectionRef = useRef(null);

  useEffect(() => {

    // 🚩 This wont fix the bug!!!

    if (!connectionRef.current) {

      connectionRef.current = createConnection();

      connectionRef.current.connect();

    }

  }, []);
```

This makes it so you only see `"✅ Connecting..."` once in development, but it doesn’t fix the bug.

When the user navigates away, the connection still isn’t closed and when they navigate back, a new connection is created. As the user navigates across the app, the connections would keep piling up, the same as it would before the “fix”.

To fix the bug, it is not enough to just make the Effect run once. The effect needs to work after re-mounting, which means the connection needs to be cleaned up like in the solution above.

See the examples below for how to handle common patterns.

### Controlling non-React widgets[](#controlling-non-react-widgets "Link for Controlling non-React widgets ")

Sometimes you need to add UI widgets that aren’t written in React. For example, let’s say you’re adding a map component to your page. It has a `setZoomLevel()` method, and you’d like to keep the zoom level in sync with a `zoomLevel` state variable in your React code. Your Effect would look similar to this:

```
useEffect(() => {

  const map = mapRef.current;

  map.setZoomLevel(zoomLevel);

}, [zoomLevel]);
```

Note that there is no cleanup needed in this case. In development, React will call the Effect twice, but this is not a problem because calling `setZoomLevel` twice with the same value does not do anything. It may be slightly slower, but this doesn’t matter because it won’t remount needlessly in production.

Some APIs may not allow you to call them twice in a row. For example, the [`showModal`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal) method of the built-in [`<dialog>`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement) element throws if you call it twice. Implement the cleanup function and make it close the dialog:

```
useEffect(() => {

  const dialog = dialogRef.current;

  dialog.showModal();

  return () => dialog.close();

}, []);
```

In development, your Effect will call `showModal()`, then immediately `close()`, and then `showModal()` again. This has the same user-visible behavior as calling `showModal()` once, as you would see in production.

### Subscribing to events[](#subscribing-to-events "Link for Subscribing to events ")

If your Effect subscribes to something, the cleanup function should unsubscribe:

```
useEffect(() => {

  function handleScroll(e) {

    console.log(window.scrollX, window.scrollY);

  }

  window.addEventListener('scroll', handleScroll);

  return () => window.removeEventListener('scroll', handleScroll);

}, []);
```

In development, your Effect will call `addEventListener()`, then immediately `removeEventListener()`, and then `addEventListener()` again with the same handler. So there would be only one active subscription at a time. This has the same user-visible behavior as calling `addEventListener()` once, as in production.

### Triggering animations[](#triggering-animations "Link for Triggering animations ")

If your Effect animates something in, the cleanup function should reset the animation to the initial values:

```
useEffect(() => {

  const node = ref.current;

  node.style.opacity = 1; // Trigger the animation

  return () => {

    node.style.opacity = 0; // Reset to the initial value

  };

}, []);
```

In development, opacity will be set to `1`, then to `0`, and then to `1` again. This should have the same user-visible behavior as setting it to `1` directly, which is what would happen in production. If you use a third-party animation library with support for tweening, your cleanup function should reset the timeline to its initial state.

### Fetching data[](#fetching-data "Link for Fetching data ")

If your Effect fetches something, the cleanup function should either [abort the fetch](https://developer.mozilla.org/en-US/docs/Web/API/AbortController) or ignore its result:

```
useEffect(() => {

  let ignore = false;



  async function startFetching() {

    const json = await fetchTodos(userId);

    if (!ignore) {

      setTodos(json);

    }

  }



  startFetching();



  return () => {

    ignore = true;

  };

}, [userId]);
```

You can’t “undo” a network request that already happened, but your cleanup function should ensure that the fetch that’s *not relevant anymore* does not keep affecting your application. If the `userId` changes from `'Alice'` to `'Bob'`, cleanup ensures that the `'Alice'` response is ignored even if it arrives after `'Bob'`.

**In development, you will see two fetches in the Network tab.** There is nothing wrong with that. With the approach above, the first Effect will immediately get cleaned up so its copy of the `ignore` variable will be set to `true`. So even though there is an extra request, it won’t affect the state thanks to the `if (!ignore)` check.

**In production, there will only be one request.** If the second request in development is bothering you, the best approach is to use a solution that deduplicates requests and caches their responses between components:

```
function TodoList() {

  const todos = useSomeDataLibrary(`/api/user/${userId}/todos`);

  // ...
```

* **If you use a [framework](/learn/start-a-new-react-project#production-grade-react-frameworks), use its built-in data fetching mechanism.** Modern React frameworks have integrated data fetching mechanisms that are efficient and don’t suffer from the above pitfalls.
* **Otherwise, consider using or building a client-side cache.** Popular open source solutions include [React Query](https://tanstack.com/query/latest), [useSWR](https://swr.vercel.app/), and [React Router 6.4+.](https://beta.reactrouter.com/en/main/start/overview) You can build your own solution too, in which case you would use Effects under the hood, but add logic for deduplicating requests, caching responses, and avoiding network waterfalls (by preloading data or hoisting data requirements to routes).

You can continue fetching data directly in Effects if neither of these approaches suit you.

### Sending analytics[](#sending-analytics "Link for Sending analytics ")

Consider this code that sends an analytics event on the page visit:

```
useEffect(() => {

  logVisit(url); // Sends a POST request

}, [url]);
```

In development, `logVisit` will be called twice for every URL, so you might be tempted to try to fix that. **We recommend keeping this code as is.** Like with earlier examples, there is no *user-visible* behavior difference between running it once and running it twice. From a practical point of view, `logVisit` should not do anything in development because you don’t want the logs from the development machines to skew the production metrics. Your component remounts every time you save its file, so it logs extra visits in development anyway.

**In production, there will be no duplicate visit logs.**

To debug the analytics events you’re sending, you can deploy your app to a staging environment (which runs in production mode) or temporarily opt out of [Strict Mode](/reference/react/StrictMode) and its development-only remounting checks. You may also send analytics from the route change event handlers instead of Effects. For more precise analytics, [intersection observers](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) can help track which components are in the viewport and how long they remain visible.

### Not an Effect: Initializing the application[](#not-an-effect-initializing-the-application "Link for Not an Effect: Initializing the application ")

Some logic should only run once when the application starts. You can put it outside your components:

```
if (typeof window !== 'undefined') { // Check if we're running in the browser.

  checkAuthToken();

  loadDataFromLocalStorage();

}



function App() {

  // ...

}
```

This guarantees that such logic only runs once after the browser loads the page.

### Not an Effect: Buying a product[](#not-an-effect-buying-a-product "Link for Not an Effect: Buying a product ")

Sometimes, even if you write a cleanup function, there’s no way to prevent user-visible consequences of running the Effect twice. For example, maybe your Effect sends a POST request like buying a product:

```
useEffect(() => {

  // 🔴 Wrong: This Effect fires twice in development, exposing a problem in the code.

  fetch('/api/buy', { method: 'POST' });

}, []);
```

You wouldn’t want to buy the product twice. However, this is also why you shouldn’t put this logic in an Effect. What if the user goes to another page and then presses Back? Your Effect would run again. You don’t want to buy the product when the user *visits* a page; you want to buy it when the user *clicks* the Buy button.

Buying is not caused by rendering; it’s caused by a specific interaction. It should run only when the user presses the button. **Delete the Effect and move your `/api/buy` request into the Buy button event handler:**

```
  function handleClick() {

    // ✅ Buying is an event because it is caused by a particular interaction.

    fetch('/api/buy', { method: 'POST' });

  }
```

**This illustrates that if remounting breaks the logic of your application, this usually uncovers existing bugs.** From a user’s perspective, visiting a page shouldn’t be different from visiting it, clicking a link, then pressing Back to view the page again. React verifies that your components abide by this principle by remounting them once in development.

## Putting it all together[](#putting-it-all-together "Link for Putting it all together ")

This playground can help you “get a feel” for how Effects work in practice.

This example uses [`setTimeout`](https://developer.mozilla.org/en-US/docs/Web/API/setTimeout) to schedule a console log with the input text to appear three seconds after the Effect runs. The cleanup function cancels the pending timeout. Start by pressing “Mount the component”:

```
import { useState, useEffect } from 'react';

function Playground() {
  const [text, setText] = useState('a');

  useEffect(() => {
    function onTimeout() {
      console.log('⏰ ' + text);
    }

    console.log('🔵 Schedule "' + text + '" log');
    const timeoutId = setTimeout(onTimeout, 3000);

    return () => {
      console.log('🟡 Cancel "' + text + '" log');
      clearTimeout(timeoutId);
    };
  }, [text]);

  return (
    <>
      <label>
        What to log:{' '}
        <input
          value={text}
          onChange={e => setText(e.target.value)}
        />
      </label>
      <h1>{text}</h1>
    </>
  );
}

export default function App() {
  const [show, setShow] = useState(false);
  return (
    <>
      <button onClick={() => setShow(!show)}>
        {show ? 'Unmount' : 'Mount'} the component
      </button>
      {show && <hr />}
      {show && <Playground />}
    </>
  );
}
```

```
export default function ChatRoom({ roomId }) {

  useEffect(() => {

    const connection = createConnection(roomId);

    connection.connect();

    return () => connection.disconnect();

  }, [roomId]);



  return <h1>Welcome to {roomId}!</h1>;

}
```

Let’s see what exactly happens as the user navigates around the app.

#### Initial render[](#initial-render "Link for Initial render ")

The user visits `<ChatRoom roomId="general" />`. Let’s [mentally substitute](/learn/state-as-a-snapshot#rendering-takes-a-snapshot-in-time) `roomId` with `'general'`:

```
  // JSX for the first render (roomId = "general")

  return <h1>Welcome to general!</h1>;
```

**The Effect is *also* a part of the rendering output.** The first render’s Effect becomes:

```
  // Effect for the first render (roomId = "general")

  () => {

    const connection = createConnection('general');

    connection.connect();

    return () => connection.disconnect();

  },

  // Dependencies for the first render (roomId = "general")

  ['general']
```

React runs this Effect, which connects to the `'general'` chat room.

#### Re-render with same dependencies[](#re-render-with-same-dependencies "Link for Re-render with same dependencies ")

Let’s say `<ChatRoom roomId="general" />` re-renders. The JSX output is the same:

```
  // JSX for the second render (roomId = "general")

  return <h1>Welcome to general!</h1>;
```

React sees that the rendering output has not changed, so it doesn’t update the DOM.

The Effect from the second render looks like this:

```
  // Effect for the second render (roomId = "general")

  () => {

    const connection = createConnection('general');

    connection.connect();

    return () => connection.disconnect();

  },

  // Dependencies for the second render (roomId = "general")

  ['general']
```

React compares `['general']` from the second render with `['general']` from the first render. **Because all dependencies are the same, React *ignores* the Effect from the second render.** It never gets called.

#### Re-render with different dependencies[](#re-render-with-different-dependencies "Link for Re-render with different dependencies ")

Then, the user visits `<ChatRoom roomId="travel" />`. This time, the component returns different JSX:

```
  // JSX for the third render (roomId = "travel")

  return <h1>Welcome to travel!</h1>;
```

React updates the DOM to change `"Welcome to general"` into `"Welcome to travel"`.

The Effect from the third render looks like this:

```
  // Effect for the third render (roomId = "travel")

  () => {

    const connection = createConnection('travel');

    connection.connect();

    return () => connection.disconnect();

  },

  // Dependencies for the third render (roomId = "travel")

  ['travel']
```

```
import { useEffect, useRef } from 'react';

export default function MyInput({ value, onChange }) {
  const ref = useRef(null);

  // TODO: This doesn't quite work. Fix it.
  // ref.current.focus()    

  return (
    <input
      ref={ref}
      value={value}
      onChange={onChange}
    />
  );
}
```

To verify that your solution works, press “Show form” and verify that the input receives focus (becomes highlighted and the cursor is placed inside). Press “Hide form” and “Show form” again. Verify the input is highlighted again.

`MyInput` should only focus *on mount* rather than after every render. To verify that the behavior is right, press “Show form” and then repeatedly press the “Make it uppercase” checkbox. Clicking the checkbox should *not* focus the input above it.

[PreviousManipulating the DOM with Refs](/learn/manipulating-the-dom-with-refs)

[NextYou Might Not Need an Effect](/learn/you-might-not-need-an-effect)

***

----
