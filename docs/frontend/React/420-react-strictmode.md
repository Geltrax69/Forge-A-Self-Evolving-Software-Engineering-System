url: https://18.react.dev/reference/react/StrictMode
----

[API Reference](/reference/react)

[Components](/reference/react/components)

# \<StrictMode>[](#undefined "Link for this heading")

`<StrictMode>` lets you find common bugs in your components early during development.

```
<StrictMode>

  <App />

</StrictMode>
```

  * [Fixing deprecation warnings enabled by Strict Mode](#fixing-deprecation-warnings-enabled-by-strict-mode)

***

## Reference[](#reference "Link for Reference ")

### `<StrictMode>`[](#strictmode "Link for this heading")

Use `StrictMode` to enable additional development behaviors and warnings for the component tree inside:

```
import { StrictMode } from 'react';

import { createRoot } from 'react-dom/client';



const root = createRoot(document.getElementById('root'));

root.render(

  <StrictMode>

    <App />

  </StrictMode>

);
```

[See more examples below.](#usage)

Strict Mode enables the following development-only behaviors:

* Your components will [re-render an extra time](#fixing-bugs-found-by-double-rendering-in-development) to find bugs caused by impure rendering.
* Your components will [re-run Effects an extra time](#fixing-bugs-found-by-re-running-effects-in-development) to find bugs caused by missing Effect cleanup.
* Your components will [be checked for usage of deprecated APIs.](#fixing-deprecation-warnings-enabled-by-strict-mode)

#### Props[](#props "Link for Props ")

`StrictMode` accepts no props.

#### Caveats[](#caveats "Link for Caveats ")

* There is no way to opt out of Strict Mode inside a tree wrapped in `<StrictMode>`. This gives you confidence that all components inside `<StrictMode>` are checked. If two teams working on a product disagree whether they find the checks valuable, they need to either reach consensus or move `<StrictMode>` down in the tree.

***

## Usage[](#usage "Link for Usage ")

### Enabling Strict Mode for entire app[](#enabling-strict-mode-for-entire-app "Link for Enabling Strict Mode for entire app ")

Strict Mode enables extra development-only checks for the entire component tree inside the `<StrictMode>` component. These checks help you find common bugs in your components early in the development process.

To enable Strict Mode for your entire app, wrap your root component with `<StrictMode>` when you render it:

```
import { StrictMode } from 'react';

import { createRoot } from 'react-dom/client';



const root = createRoot(document.getElementById('root'));

root.render(

  <StrictMode>

    <App />

  </StrictMode>

);
```

We recommend wrapping your entire app in Strict Mode, especially for newly created apps. If you use a framework that calls [`createRoot`](/reference/react-dom/client/createRoot) for you, check its documentation for how to enable Strict Mode.

Although the Strict Mode checks **only run in development,** they help you find bugs that already exist in your code but can be tricky to reliably reproduce in production. Strict Mode lets you fix bugs before your users report them.

### Note

Strict Mode enables the following checks in development:

* Your components will [re-render an extra time](#fixing-bugs-found-by-double-rendering-in-development) to find bugs caused by impure rendering.
* Your components will [re-run Effects an extra time](#fixing-bugs-found-by-re-running-effects-in-development) to find bugs caused by missing Effect cleanup.
* Your components will [be checked for usage of deprecated APIs.](#fixing-deprecation-warnings-enabled-by-strict-mode)

**All of these checks are development-only and do not impact the production build.**

***

### Enabling Strict Mode for a part of the app[](#enabling-strict-mode-for-a-part-of-the-app "Link for Enabling Strict Mode for a part of the app ")

You can also enable Strict Mode for any part of your application:

```
import { StrictMode } from 'react';



function App() {

  return (

    <>

      <Header />

      <StrictMode>

        <main>

          <Sidebar />

          <Content />

        </main>

      </StrictMode>

      <Footer />

    </>

  );

}
```

In this example, Strict Mode checks will not run against the `Header` and `Footer` components. However, they will run on `Sidebar` and `Content`, as well as all of the components inside them, no matter how deep.

***

```
export default function StoryTray({ stories }) {
  const items = stories;
  items.push({ id: 'create', label: 'Create Story' });
  return (
    <ul>
      {items.map(story => (
        <li key={story.id}>
          {story.label}
        </li>
      ))}
    </ul>
  );
}
```

There is a mistake in the code above. However, it is easy to miss because the initial output appears correct.

This mistake will become more noticeable if the `StoryTray` component re-renders multiple times. For example, let’s make the `StoryTray` re-render with a different background color whenever you hover over it:

```
import { useState } from 'react';

export default function StoryTray({ stories }) {
  const [isHover, setIsHover] = useState(false);
  const items = stories;
  items.push({ id: 'create', label: 'Create Story' });
  return (
    <ul
      onPointerEnter={() => setIsHover(true)}
      onPointerLeave={() => setIsHover(false)}
      style={{
        backgroundColor: isHover ? '#ddd' : '#fff'
      }}
    >
      {items.map(story => (
        <li key={story.id}>
          {story.label}
        </li>
      ))}
    </ul>
  );
}
```

Notice how every time you hover over the `StoryTray` component, “Create Story” gets added to the list again. The intention of the code was to add it once at the end. But `StoryTray` directly modifies the `stories` array from the props. Every time `StoryTray` renders, it adds “Create Story” again at the end of the same array. In other words, `StoryTray` is not a pure function—running it multiple times produces different results.

To fix this problem, you can make a copy of the array, and modify that copy instead of the original one:

```
export default function StoryTray({ stories }) {

  const items = stories.slice(); // Clone the array

  // ✅ Good: Pushing into a new array

  items.push({ id: 'create', label: 'Create Story' });
```

This would [make the `StoryTray` function pure.](/learn/keeping-components-pure) Each time it is called, it would only modify a new copy of the array, and would not affect any external objects or variables. This solves the bug, but you had to make the component re-render more often before it became obvious that something is wrong with its behavior.

**In the original example, the bug wasn’t obvious. Now let’s wrap the original (buggy) code in `<StrictMode>`:**

```
export default function StoryTray({ stories }) {
  const items = stories;
  items.push({ id: 'create', label: 'Create Story' });
  return (
    <ul>
      {items.map(story => (
        <li key={story.id}>
          {story.label}
        </li>
      ))}
    </ul>
  );
}
```

**Strict Mode *always* calls your rendering function twice, so you can see the mistake right away** (“Create Story” appears twice). This lets you notice such mistakes early in the process. When you fix your component to render in Strict Mode, you *also* fix many possible future production bugs like the hover functionality from before:

```
import { useState } from 'react';

export default function StoryTray({ stories }) {
  const [isHover, setIsHover] = useState(false);
  const items = stories.slice(); // Clone the array
  items.push({ id: 'create', label: 'Create Story' });
  return (
    <ul
      onPointerEnter={() => setIsHover(true)}
      onPointerLeave={() => setIsHover(false)}
      style={{
        backgroundColor: isHover ? '#ddd' : '#fff'
      }}
    >
      {items.map(story => (
        <li key={story.id}>
          {story.label}
        </li>
      ))}
    </ul>
  );
}
```

Without Strict Mode, it was easy to miss the bug until you added more re-renders. Strict Mode made the same bug appear right away. Strict Mode helps you find bugs before you push them to your team and to your users.

[Read more about keeping components pure.](/learn/keeping-components-pure)

### Note

If you have [React DevTools](/learn/react-developer-tools) installed, any `console.log` calls during the second render call will appear slightly dimmed. React DevTools also offers a setting (off by default) to suppress them completely.

***

### Fixing bugs found by re-running Effects in development[](#fixing-bugs-found-by-re-running-effects-in-development "Link for Fixing bugs found by re-running Effects in development ")

Strict Mode can also help find bugs in [Effects.](/learn/synchronizing-with-effects)

Every Effect has some setup code and may have some cleanup code. Normally, React calls setup when the component *mounts* (is added to the screen) and calls cleanup when the component *unmounts* (is removed from the screen). React then calls cleanup and setup again if its dependencies changed since the last render.

When Strict Mode is on, React will also run **one extra setup+cleanup cycle in development for every Effect.** This may feel surprising, but it helps reveal subtle bugs that are hard to catch manually.

**Here is an example to illustrate how re-running Effects in Strict Mode helps you find bugs early.**

Consider this example that connects a component to a chat:

```
import { createRoot } from 'react-dom/client';
import './styles.css';

import App from './App';

const root = createRoot(document.getElementById("root"));
root.render(<App />);
```

There is an issue with this code, but it might not be immediately clear.

To make the issue more obvious, let’s implement a feature. In the example below, `roomId` is not hardcoded. Instead, the user can select the `roomId` that they want to connect to from a dropdown. Click “Open chat” and then select different chat rooms one by one. Keep track of the number of active connections in the console:

```
import { createRoot } from 'react-dom/client';
import './styles.css';

import App from './App';

const root = createRoot(document.getElementById("root"));
root.render(<App />);
```

You’ll notice that the number of open connections always keeps growing. In a real app, this would cause performance and network problems. The issue is that [your Effect is missing a cleanup function:](/learn/synchronizing-with-effects#step-3-add-cleanup-if-needed)

```
  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => connection.disconnect();

  }, [roomId]);
```

Now that your Effect “cleans up” after itself and destroys the outdated connections, the leak is solved. However, notice that the problem did not become visible until you’ve added more features (the select box).

**In the original example, the bug wasn’t obvious. Now let’s wrap the original (buggy) code in `<StrictMode>`:**

```
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

import App from './App';

const root = createRoot(document.getElementById("root"));
root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

**With Strict Mode, you immediately see that there is a problem** (the number of active connections jumps to 2). Strict Mode runs an extra setup+cleanup cycle for every Effect. This Effect has no cleanup logic, so it creates an extra connection but doesn’t destroy it. This is a hint that you’re missing a cleanup function.

Strict Mode lets you notice such mistakes early in the process. When you fix your Effect by adding a cleanup function in Strict Mode, you *also* fix many possible future production bugs like the select box from before:

```
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

import App from './App';

const root = createRoot(document.getElementById("root"));
root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

Notice how the active connection count in the console doesn’t keep growing anymore.

Without Strict Mode, it was easy to miss that your Effect needed cleanup. By running *setup → cleanup → setup* instead of *setup* for your Effect in development, Strict Mode made the missing cleanup logic more noticeable.

[Read more about implementing Effect cleanup.](/learn/synchronizing-with-effects#how-to-handle-the-effect-firing-twice-in-development)

***

### Fixing deprecation warnings enabled by Strict Mode[](#fixing-deprecation-warnings-enabled-by-strict-mode "Link for Fixing deprecation warnings enabled by Strict Mode ")

React warns if some component anywhere inside a `<StrictMode>` tree uses one of these deprecated APIs:

* [`findDOMNode`](/reference/react-dom/findDOMNode). [See alternatives.](https://reactjs.org/docs/strict-mode.html#warning-about-deprecated-finddomnode-usage)
* `UNSAFE_` class lifecycle methods like [`UNSAFE_componentWillMount`](/reference/react/Component#unsafe_componentwillmount). [See alternatives.](https://reactjs.org/blog/2018/03/27/update-on-async-rendering.html#migrating-from-legacy-lifecycles)
* Legacy context ([`childContextTypes`](/reference/react/Component#static-childcontexttypes), [`contextTypes`](/reference/react/Component#static-contexttypes), and [`getChildContext`](/reference/react/Component#getchildcontext)). [See alternatives.](/reference/react/createContext)
* Legacy string refs ([`this.refs`](/reference/react/Component#refs)). [See alternatives.](https://reactjs.org/docs/strict-mode.html#warning-about-legacy-string-ref-api-usage)

These APIs are primarily used in older [class components](/reference/react/Component) so they rarely appear in modern apps.

[Previous\<Profiler>](/reference/react/Profiler)

[Next\<Suspense>](/reference/react/Suspense)

***

----
