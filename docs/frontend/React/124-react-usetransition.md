url: https://18.react.dev/reference/react/useTransition
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useTransition[](#undefined "Link for this heading")

`useTransition` is a React Hook that lets you update the state without blocking the UI.

```
const [isPending, startTransition] = useTransition()
```

* [Reference](#reference)

  * [`useTransition()`](#usetransition)
  * [`startTransition` function](#starttransition)

* [Usage](#usage)

  * [Marking a state update as a non-blocking Transition](#marking-a-state-update-as-a-non-blocking-transition)
  * [Updating the parent component in a Transition](#updating-the-parent-component-in-a-transition)
  * [Displaying a pending visual state during the Transition](#displaying-a-pending-visual-state-during-the-transition)
  * [Preventing unwanted loading indicators](#preventing-unwanted-loading-indicators)
  * [Building a Suspense-enabled router](#building-a-suspense-enabled-router)
  * [Displaying an error to users with an error boundary](#displaying-an-error-to-users-with-error-boundary)

* [Troubleshooting](#troubleshooting)

  * [Updating an input in a Transition doesn’t work](#updating-an-input-in-a-transition-doesnt-work)
  * [React doesn’t treat my state update as a Transition](#react-doesnt-treat-my-state-update-as-a-transition)
  * [I want to call `useTransition` from outside a component](#i-want-to-call-usetransition-from-outside-a-component)
  * [The function I pass to `startTransition` executes immediately](#the-function-i-pass-to-starttransition-executes-immediately)

***

## Reference[](#reference "Link for Reference ")

### `useTransition()`[](#usetransition "Link for this heading")

Call `useTransition` at the top level of your component to mark some state updates as Transitions.

```
import { useTransition } from 'react';



function TabContainer() {

  const [isPending, startTransition] = useTransition();

  // ...

}
```

[See more examples below.](#usage)

#### Parameters[](#parameters "Link for Parameters ")

`useTransition` does not take any parameters.

#### Returns[](#returns "Link for Returns ")

`useTransition` returns an array with exactly two items:

1. The `isPending` flag that tells you whether there is a pending Transition.
2. The [`startTransition` function](#starttransition) that lets you mark a state update as a Transition.

***

### `startTransition` function[](#starttransition "Link for this heading")

The `startTransition` function returned by `useTransition` lets you mark a state update as a Transition.

```
function TabContainer() {

  const [isPending, startTransition] = useTransition();

  const [tab, setTab] = useState('about');



  function selectTab(nextTab) {

    startTransition(() => {

      setTab(nextTab);

    });

  }

  // ...

}
```

#### Parameters[](#starttransition-parameters "Link for Parameters ")

* `scope`: A function that updates some state by calling one or more [`set` functions.](/reference/react/useState#setstate) React immediately calls `scope` with no parameters and marks all state updates scheduled synchronously during the `scope` function call as Transitions. They will be [non-blocking](#marking-a-state-update-as-a-non-blocking-transition) and [will not display unwanted loading indicators.](#preventing-unwanted-loading-indicators)

#### Returns[](#starttransition-returns "Link for Returns ")

`startTransition` does not return anything.

#### Caveats[](#starttransition-caveats "Link for Caveats ")

* `useTransition` is a Hook, so it can only be called inside components or custom Hooks. If you need to start a Transition somewhere else (for example, from a data library), call the standalone [`startTransition`](/reference/react/startTransition) instead.

* You can wrap an update into a Transition only if you have access to the `set` function of that state. If you want to start a Transition in response to some prop or a custom Hook value, try [`useDeferredValue`](/reference/react/useDeferredValue) instead.

* The function you pass to `startTransition` must be synchronous. React immediately executes this function, marking all state updates that happen while it executes as Transitions. If you try to perform more state updates later (for example, in a timeout), they won’t be marked as Transitions.

* The `startTransition` function has a stable identity, so you will often see it omitted from Effect dependencies, but including it will not cause the Effect to fire. If the linter lets you omit a dependency without errors, it is safe to do. [Learn more about removing Effect dependencies.](/learn/removing-effect-dependencies#move-dynamic-objects-and-functions-inside-your-effect)

* A state update marked as a Transition will be interrupted by other state updates. For example, if you update a chart component inside a Transition, but then start typing into an input while the chart is in the middle of a re-render, React will restart the rendering work on the chart component after handling the input update.

* Transition updates can’t be used to control text inputs.

* If there are multiple ongoing Transitions, React currently batches them together. This is a limitation that will likely be removed in a future release.

***

## Usage[](#usage "Link for Usage ")

### Marking a state update as a non-blocking Transition[](#marking-a-state-update-as-a-non-blocking-transition "Link for Marking a state update as a non-blocking Transition ")

Call `useTransition` at the top level of your component to mark state updates as non-blocking *Transitions*.

```
import { useState, useTransition } from 'react';



function TabContainer() {

  const [isPending, startTransition] = useTransition();

  // ...

}
```

`useTransition` returns an array with exactly two items:

1. The `isPending` flag that tells you whether there is a pending Transition.
2. The `startTransition` function that lets you mark a state update as a Transition.

You can then mark a state update as a Transition like this:

```
function TabContainer() {

  const [isPending, startTransition] = useTransition();

  const [tab, setTab] = useState('about');



  function selectTab(nextTab) {

    startTransition(() => {

      setTab(nextTab);

    });

  }

  // ...

}
```

Transitions let you keep the user interface updates responsive even on slow devices.

With a Transition, your UI stays responsive in the middle of a re-render. For example, if the user clicks a tab but then change their mind and click another tab, they can do that without waiting for the first re-render to finish.

#### The difference between useTransition and regular state updates[](#examples "Link for The difference between useTransition and regular state updates")

#### Example 1 of 2:Updating the current tab in a Transition[](#updating-the-current-tab-in-a-transition "Link for this heading")

In this example, the “Posts” tab is **artificially slowed down** so that it takes at least a second to render.

Click “Posts” and then immediately click “Contact”. Notice that this interrupts the slow render of “Posts”. The “Contact” tab shows immediately. Because this state update is marked as a Transition, a slow re-render did not freeze the user interface.

```
import { useState, useTransition } from 'react';
import TabButton from './TabButton.js';
import AboutTab from './AboutTab.js';
import PostsTab from './PostsTab.js';
import ContactTab from './ContactTab.js';

export default function TabContainer() {
  const [isPending, startTransition] = useTransition();
  const [tab, setTab] = useState('about');

  function selectTab(nextTab) {
    startTransition(() => {
      setTab(nextTab);
    });
  }

  return (
    <>
      <TabButton
        isActive={tab === 'about'}
        onClick={() => selectTab('about')}
      >
        About
      </TabButton>
      <TabButton
        isActive={tab === 'posts'}
        onClick={() => selectTab('posts')}
      >
        Posts (slow)
      </TabButton>
      <TabButton
        isActive={tab === 'contact'}
        onClick={() => selectTab('contact')}
      >
        Contact
      </TabButton>
      <hr />
      {tab === 'about' && <AboutTab />}
      {tab === 'posts' && <PostsTab />}
      {tab === 'contact' && <ContactTab />}
    </>
  );
}
```

***

### Updating the parent component in a Transition[](#updating-the-parent-component-in-a-transition "Link for Updating the parent component in a Transition ")

You can update a parent component’s state from the `useTransition` call, too. For example, this `TabButton` component wraps its `onClick` logic in a Transition:

```
export default function TabButton({ children, isActive, onClick }) {

  const [isPending, startTransition] = useTransition();

  if (isActive) {

    return <b>{children}</b>

  }

  return (

    <button onClick={() => {

      startTransition(() => {

        onClick();

      });

    }}>

      {children}

    </button>

  );

}
```

Because the parent component updates its state inside the `onClick` event handler, that state update gets marked as a Transition. This is why, like in the earlier example, you can click on “Posts” and then immediately click “Contact”. Updating the selected tab is marked as a Transition, so it does not block user interactions.

```
import { useTransition } from 'react';

export default function TabButton({ children, isActive, onClick }) {
  const [isPending, startTransition] = useTransition();
  if (isActive) {
    return <b>{children}</b>
  }
  return (
    <button onClick={() => {
      startTransition(() => {
        onClick();
      });
    }}>
      {children}
    </button>
  );
}
```

***

### Displaying a pending visual state during the Transition[](#displaying-a-pending-visual-state-during-the-transition "Link for Displaying a pending visual state during the Transition ")

You can use the `isPending` boolean value returned by `useTransition` to indicate to the user that a Transition is in progress. For example, the tab button can have a special “pending” visual state:

```
function TabButton({ children, isActive, onClick }) {

  const [isPending, startTransition] = useTransition();

  // ...

  if (isPending) {

    return <b className="pending">{children}</b>;

  }

  // ...
```

Notice how clicking “Posts” now feels more responsive because the tab button itself updates right away:

```
import { useTransition } from 'react';

export default function TabButton({ children, isActive, onClick }) {
  const [isPending, startTransition] = useTransition();
  if (isActive) {
    return <b>{children}</b>
  }
  if (isPending) {
    return <b className="pending">{children}</b>;
  }
  return (
    <button onClick={() => {
      startTransition(() => {
        onClick();
      });
    }}>
      {children}
    </button>
  );
}
```

***

### Preventing unwanted loading indicators[](#preventing-unwanted-loading-indicators "Link for Preventing unwanted loading indicators ")

In this example, the `PostsTab` component fetches some data using a [Suspense-enabled](/reference/react/Suspense) data source. When you click the “Posts” tab, the `PostsTab` component *suspends*, causing the closest loading fallback to appear:

```
import { Suspense, useState } from 'react';
import TabButton from './TabButton.js';
import AboutTab from './AboutTab.js';
import PostsTab from './PostsTab.js';
import ContactTab from './ContactTab.js';

export default function TabContainer() {
  const [tab, setTab] = useState('about');
  return (
    <Suspense fallback={<h1>🌀 Loading...</h1>}>
      <TabButton
        isActive={tab === 'about'}
        onClick={() => setTab('about')}
      >
        About
      </TabButton>
      <TabButton
        isActive={tab === 'posts'}
        onClick={() => setTab('posts')}
      >
        Posts
      </TabButton>
      <TabButton
        isActive={tab === 'contact'}
        onClick={() => setTab('contact')}
      >
        Contact
      </TabButton>
      <hr />
      {tab === 'about' && <AboutTab />}
      {tab === 'posts' && <PostsTab />}
      {tab === 'contact' && <ContactTab />}
    </Suspense>
  );
}
```

Hiding the entire tab container to show a loading indicator leads to a jarring user experience. If you add `useTransition` to `TabButton`, you can instead indicate display the pending state in the tab button instead.

Notice that clicking “Posts” no longer replaces the entire tab container with a spinner:

```
import { useTransition } from 'react';

export default function TabButton({ children, isActive, onClick }) {
  const [isPending, startTransition] = useTransition();
  if (isActive) {
    return <b>{children}</b>
  }
  if (isPending) {
    return <b className="pending">{children}</b>;
  }
  return (
    <button onClick={() => {
      startTransition(() => {
        onClick();
      });
    }}>
      {children}
    </button>
  );
}
```

[Read more about using Transitions with Suspense.](/reference/react/Suspense#preventing-already-revealed-content-from-hiding)

### Note

Transitions will only “wait” long enough to avoid hiding *already revealed* content (like the tab container). If the Posts tab had a [nested `<Suspense>` boundary,](/reference/react/Suspense#revealing-nested-content-as-it-loads) the Transition would not “wait” for it.

***

### Building a Suspense-enabled router[](#building-a-suspense-enabled-router "Link for Building a Suspense-enabled router ")

If you’re building a React framework or a router, we recommend marking page navigations as Transitions.

```
function Router() {

  const [page, setPage] = useState('/');

  const [isPending, startTransition] = useTransition();



  function navigate(url) {

    startTransition(() => {

      setPage(url);

    });

  }

  // ...
```

This is recommended for two reasons:

* [Transitions are interruptible,](#marking-a-state-update-as-a-non-blocking-transition) which lets the user click away without waiting for the re-render to complete.
* [Transitions prevent unwanted loading indicators,](#preventing-unwanted-loading-indicators) which lets the user avoid jarring jumps on navigation.

Here is a tiny simplified router example using Transitions for navigations.

```
import { Suspense, useState, useTransition } from 'react';
import IndexPage from './IndexPage.js';
import ArtistPage from './ArtistPage.js';
import Layout from './Layout.js';

export default function App() {
  return (
    <Suspense fallback={<BigSpinner />}>
      <Router />
    </Suspense>
  );
}

function Router() {
  const [page, setPage] = useState('/');
  const [isPending, startTransition] = useTransition();

  function navigate(url) {
    startTransition(() => {
      setPage(url);
    });
  }

  let content;
  if (page === '/') {
    content = (
      <IndexPage navigate={navigate} />
    );
  } else if (page === '/the-beatles') {
    content = (
      <ArtistPage
        artist={{
          id: 'the-beatles',
          name: 'The Beatles',
        }}
      />
    );
  }
  return (
    <Layout isPending={isPending}>
      {content}
    </Layout>
  );
}

function BigSpinner() {
  return <h2>🌀 Loading...</h2>;
}
```

### Note

[Suspense-enabled](/reference/react/Suspense) routers are expected to wrap the navigation updates into Transitions by default.

***

### Displaying an error to users with an error boundary[](#displaying-an-error-to-users-with-error-boundary "Link for Displaying an error to users with an error boundary ")

### Canary

Error Boundary for useTransition is currently only available in React’s canary and experimental channels. Learn more about [React’s release channels here](/community/versioning-policy#all-release-channels).

If a function passed to `startTransition` throws an error, you can display an error to your user with an [error boundary](/reference/react/Component#catching-rendering-errors-with-an-error-boundary). To use an error boundary, wrap the component where you are calling the `useTransition` in an error boundary. Once the function passed to `startTransition` errors, the fallback for the error boundary will be displayed.

```
import { useTransition } from "react";
import { ErrorBoundary } from "react-error-boundary";

export function AddCommentContainer() {
  return (
    <ErrorBoundary fallback={<p>⚠️Something went wrong</p>}>
      <AddCommentButton />
    </ErrorBoundary>
  );
}

function addComment(comment) {
  // For demonstration purposes to show Error Boundary
  if (comment == null) {
    throw new Error("Example Error: An error thrown to trigger error boundary");
  }
}

function AddCommentButton() {
  const [pending, startTransition] = useTransition();

  return (
    <button
      disabled={pending}
      onClick={() => {
        startTransition(() => {
          // Intentionally not passing a comment
          // so error gets thrown
          addComment();
        });
      }}
    >
      Add comment
    </button>
  );
}
```

***

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### Updating an input in a Transition doesn’t work[](#updating-an-input-in-a-transition-doesnt-work "Link for Updating an input in a Transition doesn’t work ")

You can’t use a Transition for a state variable that controls an input:

```
const [text, setText] = useState('');

// ...

function handleChange(e) {

  // ❌ Can't use Transitions for controlled input state

  startTransition(() => {

    setText(e.target.value);

  });

}

// ...

return <input value={text} onChange={handleChange} />;
```

This is because Transitions are non-blocking, but updating an input in response to the change event should happen synchronously. If you want to run a Transition in response to typing, you have two options:

1. You can declare two separate state variables: one for the input state (which always updates synchronously), and one that you will update in a Transition. This lets you control the input using the synchronous state, and pass the Transition state variable (which will “lag behind” the input) to the rest of your rendering logic.
2. Alternatively, you can have one state variable, and add [`useDeferredValue`](/reference/react/useDeferredValue) which will “lag behind” the real value. It will trigger non-blocking re-renders to “catch up” with the new value automatically.

***

### React doesn’t treat my state update as a Transition[](#react-doesnt-treat-my-state-update-as-a-transition "Link for React doesn’t treat my state update as a Transition ")

When you wrap a state update in a Transition, make sure that it happens *during* the `startTransition` call:

```
startTransition(() => {

  // ✅ Setting state *during* startTransition call

  setPage('/about');

});
```

The function you pass to `startTransition` must be synchronous.

You can’t mark an update as a Transition like this:

```
startTransition(() => {

  // ❌ Setting state *after* startTransition call

  setTimeout(() => {

    setPage('/about');

  }, 1000);

});
```

Instead, you could do this:

```
setTimeout(() => {

  startTransition(() => {

    // ✅ Setting state *during* startTransition call

    setPage('/about');

  });

}, 1000);
```

Similarly, you can’t mark an update as a Transition like this:

```
startTransition(async () => {

  await someAsyncFunction();

  // ❌ Setting state *after* startTransition call

  setPage('/about');

});
```

However, this works instead:

```
await someAsyncFunction();

startTransition(() => {

  // ✅ Setting state *during* startTransition call

  setPage('/about');

});
```

***

### I want to call `useTransition` from outside a component[](#i-want-to-call-usetransition-from-outside-a-component "Link for this heading")

You can’t call `useTransition` outside a component because it’s a Hook. In this case, use the standalone [`startTransition`](/reference/react/startTransition) method instead. It works the same way, but it doesn’t provide the `isPending` indicator.

***

### The function I pass to `startTransition` executes immediately[](#the-function-i-pass-to-starttransition-executes-immediately "Link for this heading")

If you run this code, it will print 1, 2, 3:

```
console.log(1);

startTransition(() => {

  console.log(2);

  setPage('/about');

});

console.log(3);
```

**It is expected to print 1, 2, 3.** The function you pass to `startTransition` does not get delayed. Unlike with the browser `setTimeout`, it does not run the callback later. React executes your function immediately, but any state updates scheduled *while it is running* are marked as Transitions. You can imagine that it works like this:

```
// A simplified version of how React works



let isInsideTransition = false;



function startTransition(scope) {

  isInsideTransition = true;

  scope();

  isInsideTransition = false;

}



function setState() {

  if (isInsideTransition) {

    // ... schedule a Transition state update ...

  } else {

    // ... schedule an urgent state update ...

  }

}
```

[PrevioususeSyncExternalStore](/reference/react/useSyncExternalStore)

[NextComponents](/reference/react/components)

***

----
