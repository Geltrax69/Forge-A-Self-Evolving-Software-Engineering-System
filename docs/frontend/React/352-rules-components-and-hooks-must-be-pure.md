url: https://react.dev/reference/rules/components-and-hooks-must-be-pure
----

*Rendering* refers to calculating what the next version of your UI should look like. After rendering, React takes this new calculation and compares it to the calculation used to create the previous version of your UI. Then React commits just the minimum changes needed to the [DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) (what your user actually sees) to apply the changes. Finally, [Effects](/learn/synchronizing-with-effects) are flushed (meaning they are run until there are no more left). For more detailed information see the docs for [Render](/learn/render-and-commit) and [Commit and Effect Hooks](/reference/react/hooks#effect-hooks).

##### Deep Dive#### How to tell if code runs in render[](#how-to-tell-if-code-runs-in-render "Link for How to tell if code runs in render ")

One quick heuristic to tell if code runs during render is to examine where it is: if it’s written at the top level like in the example below, there’s a good chance it runs during render.

```
function Dropdown() {

  const selectedItems = new Set(); // created during render

  // ...

}
```

Event handlers and Effects don’t run in render:

```
function Dropdown() {

  const selectedItems = new Set();

  const onSelect = (item) => {

    // this code is in an event handler, so it's only run when the user triggers this

    selectedItems.add(item);

  }

}
```

```
function Dropdown() {

  const selectedItems = new Set();

  useEffect(() => {

    // this code is inside of an Effect, so it only runs after rendering

    logForAnalytics(selectedItems);

  }, [selectedItems]);

}
```

***

## Components and Hooks must be idempotent[](#components-and-hooks-must-be-idempotent "Link for Components and Hooks must be idempotent ")

Components must always return the same output with respect to their inputs – props, state, and context. This is known as *idempotency*. [Idempotency](https://en.wikipedia.org/wiki/Idempotence) is a term popularized in functional programming. It refers to the idea that you [always get the same result every time](/learn/keeping-components-pure) you run that piece of code with the same inputs.

This means that *all* code that runs [during render](#how-does-react-run-your-code) must also be idempotent in order for this rule to hold. For example, this line of code is not idempotent (and therefore, neither is the component):

```
function Clock() {

  const time = new Date(); // 🔴 Bad: always returns a different result!

  return <span>{time.toLocaleString()}</span>

}
```

`new Date()` is not idempotent as it always returns the current date and changes its result every time it’s called. When you render the above component, the time displayed on the screen will stay stuck on the time that the component was rendered. Similarly, functions like `Math.random()` also aren’t idempotent, because they return different results every time they’re called, even when the inputs are the same.

This doesn’t mean you shouldn’t use non-idempotent functions like `new Date()` *at all* – you should just avoid using them [during render](#how-does-react-run-your-code). In this case, we can *synchronize* the latest date to this component using an [Effect](/reference/react/useEffect):

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useState, useEffect } from 'react';

function useTime() {
  // 1. Keep track of the current date's state. `useState` receives an initializer function as its
  //    initial state. It only runs once when the hook is called, so only the current date at the
  //    time the hook is called is set first.
  const [time, setTime] = useState(() => new Date());

  useEffect(() => {
    // 2. Update the current date every second using `setInterval`.
    const id = setInterval(() => {
      setTime(new Date()); // ✅ Good: non-idempotent code no longer runs in render
    }, 1000);
    // 3. Return a cleanup function so we don't leak the `setInterval` timer.
    return () => clearInterval(id);
  }, []);

  return time;
}

export default function Clock() {
  const time = useTime();
  return <span>{time.toLocaleString()}</span>;
}
```

By wrapping the non-idempotent `new Date()` call in an Effect, it moves that calculation [outside of rendering](#how-does-react-run-your-code).

If you don’t need to synchronize some external state with React, you can also consider using an [event handler](/learn/responding-to-events) if it only needs to be updated in response to a user interaction.

***

```
function FriendList({ friends }) {

  const items = []; // ✅ Good: locally created

  for (let i = 0; i < friends.length; i++) {

    const friend = friends[i];

    items.push(

      <Friend key={friend.id} friend={friend} />

    ); // ✅ Good: local mutation is okay

  }

  return <section>{items}</section>;

}
```

There is no need to contort your code to avoid local mutation. [`Array.map`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) could also be used here for brevity, but there is nothing wrong with creating a local array and then pushing items into it [during render](#how-does-react-run-your-code).

Even though it looks like we are mutating `items`, the key point to note is that this code only does so *locally* – the mutation isn’t “remembered” when the component is rendered again. In other words, `items` only stays around as long as the component does. Because `items` is always *recreated* every time `<FriendList />` is rendered, the component will always return the same result.

On the other hand, if `items` was created outside of the component, it holds on to its previous values and remembers changes:

```
const items = []; // 🔴 Bad: created outside of the component

function FriendList({ friends }) {

  for (let i = 0; i < friends.length; i++) {

    const friend = friends[i];

    items.push(

      <Friend key={friend.id} friend={friend} />

    ); // 🔴 Bad: mutates a value created outside of render

  }

  return <section>{items}</section>;

}
```

When `<FriendList />` runs again, we will continue appending `friends` to `items` every time that component is run, leading to multiple duplicated results. This version of `<FriendList />` has observable side effects [during render](#how-does-react-run-your-code) and **breaks the rule**.

#### Lazy initialization[](#lazy-initialization "Link for Lazy initialization ")

Lazy initialization is also fine despite not being fully “pure”:

```
function ExpenseForm() {

  SuperCalculator.initializeIfNotReady(); // ✅ Good: if it doesn't affect other components

  // Continue rendering...

}
```

#### Changing the DOM[](#changing-the-dom "Link for Changing the DOM ")

Side effects that are directly visible to the user are not allowed in the render logic of React components. In other words, merely calling a component function shouldn’t by itself produce a change on the screen.

```
function ProductDetailPage({ product }) {

  document.title = product.title; // 🔴 Bad: Changes the DOM

}
```

One way to achieve the desired result of updating `document.title` outside of render is to [synchronize the component with `document`](/learn/synchronizing-with-effects).

As long as calling a component multiple times is safe and doesn’t affect the rendering of other components, React doesn’t care if it’s 100% pure in the strict functional programming sense of the word. It is more important that [components must be idempotent](/reference/rules/components-and-hooks-must-be-pure).

***

## Props and state are immutable[](#props-and-state-are-immutable "Link for Props and state are immutable ")

A component’s props and state are immutable [snapshots](/learn/state-as-a-snapshot). Never mutate them directly. Instead, pass new props down, and use the setter function from `useState`.

You can think of the props and state values as snapshots that are updated after rendering. For this reason, you don’t modify the props or state variables directly: instead you pass new props, or use the setter function provided to you to tell React that state needs to update the next time the component is rendered.

### Don’t mutate Props[](#props "Link for Don’t mutate Props ")

Props are immutable because if you mutate them, the application will produce inconsistent output, which can be hard to debug as it may or may not work depending on the circumstances.

```
function Post({ item }) {

  item.url = new Url(item.url, base); // 🔴 Bad: never mutate props directly

  return <Link url={item.url}>{item.title}</Link>;

}
```

```
function Post({ item }) {

  const url = new Url(item.url, base); // ✅ Good: make a copy instead

  return <Link url={url}>{item.title}</Link>;

}
```

### Don’t mutate State[](#state "Link for Don’t mutate State ")

`useState` returns the state variable and a setter to update that state.

```
const [stateVariable, setter] = useState(0);
```

Rather than updating the state variable in-place, we need to update it using the setter function that is returned by `useState`. Changing values on the state variable doesn’t cause the component to update, leaving your users with an outdated UI. Using the setter function informs React that the state has changed, and that we need to queue a re-render to update the UI.

```
function Counter() {

  const [count, setCount] = useState(0);



  function handleClick() {

    count = count + 1; // 🔴 Bad: never mutate state directly

  }



  return (

    <button onClick={handleClick}>

      You pressed me {count} times

    </button>

  );

}
```

```
function Counter() {

  const [count, setCount] = useState(0);



  function handleClick() {

    setCount(count + 1); // ✅ Good: use the setter function returned by useState

  }



  return (

    <button onClick={handleClick}>

      You pressed me {count} times

    </button>

  );

}
```

***

## Return values and arguments to Hooks are immutable[](#return-values-and-arguments-to-hooks-are-immutable "Link for Return values and arguments to Hooks are immutable ")

Once values are passed to a hook, you should not modify them. Like props in JSX, values become immutable when passed to a hook.

```
function useIconStyle(icon) {

  const theme = useContext(ThemeContext);

  if (icon.enabled) {

    icon.className = computeStyle(icon, theme); // 🔴 Bad: never mutate hook arguments directly

  }

  return icon;

}
```

```
function useIconStyle(icon) {

  const theme = useContext(ThemeContext);

  const newIcon = { ...icon }; // ✅ Good: make a copy instead

  if (icon.enabled) {

    newIcon.className = computeStyle(icon, theme);

  }

  return newIcon;

}
```

One important principle in React is *local reasoning*: the ability to understand what a component or hook does by looking at its code in isolation. Hooks should be treated like “black boxes” when they are called. For example, a custom hook might have used its arguments as dependencies to memoize values inside it:

```
function useIconStyle(icon) {

  const theme = useContext(ThemeContext);



  return useMemo(() => {

    const newIcon = { ...icon };

    if (icon.enabled) {

      newIcon.className = computeStyle(icon, theme);

    }

    return newIcon;

  }, [icon, theme]);

}
```

If you were to mutate the Hook’s arguments, the custom hook’s memoization will become incorrect, so it’s important to avoid doing that.

```
style = useIconStyle(icon);         // `style` is memoized based on `icon`

icon.enabled = false;               // Bad: 🔴 never mutate hook arguments directly

style = useIconStyle(icon);         // previously memoized result is returned
```

```
style = useIconStyle(icon);         // `style` is memoized based on `icon`

icon = { ...icon, enabled: false }; // Good: ✅ make a copy instead

style = useIconStyle(icon);         // new value of `style` is calculated
```

Similarly, it’s important to not modify the return values of Hooks, as they may have been memoized.

***

## Values are immutable after being passed to JSX[](#values-are-immutable-after-being-passed-to-jsx "Link for Values are immutable after being passed to JSX ")

Don’t mutate values after they’ve been used in JSX. Move the mutation to before the JSX is created.

When you use JSX in an expression, React may eagerly evaluate the JSX before the component finishes rendering. This means that mutating values after they’ve been passed to JSX can lead to outdated UIs, as React won’t know to update the component’s output.

```
function Page({ colour }) {

  const styles = { colour, size: "large" };

  const header = <Header styles={styles} />;

  styles.size = "small"; // 🔴 Bad: styles was already used in the JSX above

  const footer = <Footer styles={styles} />;

  return (

    <>

      {header}

      <Content />

      {footer}

    </>

  );

}
```

```
function Page({ colour }) {

  const headerStyles = { colour, size: "large" };

  const header = <Header styles={headerStyles} />;

  const footerStyles = { colour, size: "small" }; // ✅ Good: we created a new value

  const footer = <Footer styles={footerStyles} />;

  return (

    <>

      {header}

      <Content />

      {footer}

    </>

  );

}
```

[PreviousOverview](/reference/rules)

[NextReact calls Components and Hooks](/reference/rules/react-calls-components-and-hooks)

***

----
