url: https://react.dev/reference/react/useRef
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useRef[](#undefined "Link for this heading")

`useRef` is a React Hook that lets you reference a value that’s not needed for rendering.

```
const ref = useRef(initialValue)
```

***

## Reference[](#reference "Link for Reference ")

### `useRef(initialValue)`[](#useref "Link for this heading")

Call `useRef` at the top level of your component to declare a [ref.](/learn/referencing-values-with-refs)

```
import { useRef } from 'react';



function MyComponent() {

  const intervalRef = useRef(0);

  const inputRef = useRef(null);

  // ...
```

***

## Usage[](#usage "Link for Usage ")

### Referencing a value with a ref[](#referencing-a-value-with-a-ref "Link for Referencing a value with a ref ")

Call `useRef` at the top level of your component to declare one or more [refs.](/learn/referencing-values-with-refs)

```
import { useRef } from 'react';



function Stopwatch() {

  const intervalRef = useRef(0);

  // ...
```

`useRef` returns a ref object with a single `current` property initially set to the initial value you provided.

On the next renders, `useRef` will return the same object. You can change its `current` property to store information and read it later. This might remind you of [state](/reference/react/useState), but there is an important difference.

**Changing a ref does not trigger a re-render.** This means refs are perfect for storing information that doesn’t affect the visual output of your component. For example, if you need to store an [interval ID](https://developer.mozilla.org/en-US/docs/Web/API/setInterval) and retrieve it later, you can put it in a ref. To update the value inside the ref, you need to manually change its `current` property:

```
function handleStartClick() {

  const intervalId = setInterval(() => {

    // ...

  }, 1000);

  intervalRef.current = intervalId;

}
```

Later, you can read that interval ID from the ref so that you can call [clear that interval](https://developer.mozilla.org/en-US/docs/Web/API/clearInterval):

```
function handleStopClick() {

  const intervalId = intervalRef.current;

  clearInterval(intervalId);

}
```

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useRef } from 'react';

export default function Counter() {
  let ref = useRef(0);

  function handleClick() {
    ref.current = ref.current + 1;
    alert('You clicked ' + ref.current + ' times!');
  }

  return (
    <button onClick={handleClick}>
      Click me!
    </button>
  );
}
```

```
function MyComponent() {

  // ...

  // 🚩 Don't write a ref during rendering

  myRef.current = 123;

  // ...

  // 🚩 Don't read a ref during rendering

  return <h1>{myOtherRef.current}</h1>;

}
```

You can read or write refs **from event handlers or effects instead**.

```
function MyComponent() {

  // ...

  useEffect(() => {

    // ✅ You can read or write refs in effects

    myRef.current = 123;

  });

  // ...

  function handleClick() {

    // ✅ You can read or write refs in event handlers

    doSomething(myOtherRef.current);

  }

  // ...

}
```

If you *have to* read [or write](/reference/react/useState#storing-information-from-previous-renders) something during rendering, [use state](/reference/react/useState) instead.

When you break these rules, your component might still work, but most of the newer features we’re adding to React will rely on these expectations. Read more about [keeping your components pure.](/learn/keeping-components-pure#where-you-_can_-cause-side-effects)

***

### Manipulating the DOM with a ref[](#manipulating-the-dom-with-a-ref "Link for Manipulating the DOM with a ref ")

It’s particularly common to use a ref to manipulate the [DOM.](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API) React has built-in support for this.

First, declare a ref object with an initial value of `null`:

```
import { useRef } from 'react';



function MyComponent() {

  const inputRef = useRef(null);

  // ...
```

Then pass your ref object as the `ref` attribute to the JSX of the DOM node you want to manipulate:

```
  // ...

  return <input ref={inputRef} />;
```

After React creates the DOM node and puts it on the screen, React will set the `current` property of your ref object to that DOM node. Now you can access the `<input>`’s DOM node and call methods like [`focus()`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus):

```
  function handleClick() {

    inputRef.current.focus();

  }
```

React will set the `current` property back to `null` when the node is removed from the screen.

Read more about [manipulating the DOM with refs.](/learn/manipulating-the-dom-with-refs)

#### Examples of manipulating the DOM with useRef[](#examples-dom "Link for Examples of manipulating the DOM with useRef")

#### Example 1 of 4:Focusing a text input[](#focusing-a-text-input "Link for this heading")

In this example, clicking the button will focus the input:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useRef } from 'react';

export default function Form() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <input ref={inputRef} />
      <button onClick={handleClick}>
        Focus the input
      </button>
    </>
  );
}
```

***

### Avoiding recreating the ref contents[](#avoiding-recreating-the-ref-contents "Link for Avoiding recreating the ref contents ")

React saves the initial ref value once and ignores it on the next renders.

```
function Video() {

  const playerRef = useRef(new VideoPlayer());

  // ...
```

Although the result of `new VideoPlayer()` is only used for the initial render, you’re still calling this function on every render. This can be wasteful if it’s creating expensive objects.

To solve it, you may initialize the ref like this instead:

```
function Video() {

  const playerRef = useRef(null);

  if (playerRef.current === null) {

    playerRef.current = new VideoPlayer();

  }

  // ...
```

Normally, writing or reading `ref.current` during render is not allowed. However, it’s fine in this case because the result is always the same, and the condition only executes during initialization so it’s fully predictable.

##### Deep Dive#### How to avoid null checks when initializing useRef later[](#how-to-avoid-null-checks-when-initializing-use-ref-later "Link for How to avoid null checks when initializing useRef later ")

If you use a type checker and don’t want to always check for `null`, you can try a pattern like this instead:

```
function Video() {

  const playerRef = useRef(null);



  function getPlayer() {

    if (playerRef.current !== null) {

      return playerRef.current;

    }

    const player = new VideoPlayer();

    playerRef.current = player;

    return player;

  }



  // ...
```

Here, the `playerRef` itself is nullable. However, you should be able to convince your type checker that there is no case in which `getPlayer()` returns `null`. Then use `getPlayer()` in your event handlers.

***

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### I can’t get a ref to a custom component[](#i-cant-get-a-ref-to-a-custom-component "Link for I can’t get a ref to a custom component ")

If you try to pass a `ref` to your own component like this:

```
const inputRef = useRef(null);



return <MyInput ref={inputRef} />;
```

You might get an error in the console:

Console

TypeError: Cannot read properties of null

By default, your own components don’t expose refs to the DOM nodes inside them.

To fix this, find the component that you want to get a ref to:

```
export default function MyInput({ value, onChange }) {

  return (

    <input

      value={value}

      onChange={onChange}

    />

  );

}
```

And then add `ref` to the list of props your component accepts and pass `ref` as a prop to the relevant child [built-in component](/reference/react-dom/components/common) like this:

```
function MyInput({ value, onChange, ref }) {

  return (

    <input

      value={value}

      onChange={onChange}

      ref={ref}

    />

  );

};



export default MyInput;
```

Then the parent component can get a ref to it.

Read more about [accessing another component’s DOM nodes.](/learn/manipulating-the-dom-with-refs#accessing-another-components-dom-nodes)

[PrevioususeReducer](/reference/react/useReducer)

[NextuseState](/reference/react/useState)

***

----
