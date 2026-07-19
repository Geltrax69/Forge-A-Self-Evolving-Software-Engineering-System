url: https://18.react.dev/reference/react/useCallback
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useCallback[](#undefined "Link for this heading")

`useCallback` is a React Hook that lets you cache a function definition between re-renders.

```
const cachedFn = useCallback(fn, dependencies)
```

***

## Reference[](#reference "Link for Reference ")

### `useCallback(fn, dependencies)`[](#usecallback "Link for this heading")

Call `useCallback` at the top level of your component to cache a function definition between re-renders:

```
import { useCallback } from 'react';



export default function ProductPage({ productId, referrer, theme }) {

  const handleSubmit = useCallback((orderDetails) => {

    post('/product/' + productId + '/buy', {

      referrer,

      orderDetails,

    });

  }, [productId, referrer]);
```

***

## Usage[](#usage "Link for Usage ")

### Skipping re-rendering of components[](#skipping-re-rendering-of-components "Link for Skipping re-rendering of components ")

When you optimize rendering performance, you will sometimes need to cache the functions that you pass to child components. Let’s first look at the syntax for how to do this, and then see in which cases it’s useful.

To cache a function between re-renders of your component, wrap its definition into the `useCallback` Hook:

```
import { useCallback } from 'react';



function ProductPage({ productId, referrer, theme }) {

  const handleSubmit = useCallback((orderDetails) => {

    post('/product/' + productId + '/buy', {

      referrer,

      orderDetails,

    });

  }, [productId, referrer]);

  // ...
```

```
function ProductPage({ productId, referrer, theme }) {

  // ...

  return (

    <div className={theme}>

      <ShippingForm onSubmit={handleSubmit} />

    </div>

  );
```

You’ve noticed that toggling the `theme` prop freezes the app for a moment, but if you remove `<ShippingForm />` from your JSX, it feels fast. This tells you that it’s worth trying to optimize the `ShippingForm` component.

**By default, when a component re-renders, React re-renders all of its children recursively.** This is why, when `ProductPage` re-renders with a different `theme`, the `ShippingForm` component *also* re-renders. This is fine for components that don’t require much calculation to re-render. But if you verified a re-render is slow, you can tell `ShippingForm` to skip re-rendering when its props are the same as on last render by wrapping it in [`memo`:](/reference/react/memo)

```
import { memo } from 'react';



const ShippingForm = memo(function ShippingForm({ onSubmit }) {

  // ...

});
```

**With this change, `ShippingForm` will skip re-rendering if all of its props are the *same* as on the last render.** This is when caching a function becomes important! Let’s say you defined `handleSubmit` without `useCallback`:

```
function ProductPage({ productId, referrer, theme }) {

  // Every time the theme changes, this will be a different function...

  function handleSubmit(orderDetails) {

    post('/product/' + productId + '/buy', {

      referrer,

      orderDetails,

    });

  }

  

  return (

    <div className={theme}>

      {/* ... so ShippingForm's props will never be the same, and it will re-render every time */}

      <ShippingForm onSubmit={handleSubmit} />

    </div>

  );

}
```

**In JavaScript, a `function () {}` or `() => {}` always creates a *different* function,** similar to how the `{}` object literal always creates a new object. Normally, this wouldn’t be a problem, but it means that `ShippingForm` props will never be the same, and your [`memo`](/reference/react/memo) optimization won’t work. This is where `useCallback` comes in handy:

```
function ProductPage({ productId, referrer, theme }) {

  // Tell React to cache your function between re-renders...

  const handleSubmit = useCallback((orderDetails) => {

    post('/product/' + productId + '/buy', {

      referrer,

      orderDetails,

    });

  }, [productId, referrer]); // ...so as long as these dependencies don't change...



  return (

    <div className={theme}>

      {/* ...ShippingForm will receive the same props and can skip re-rendering */}

      <ShippingForm onSubmit={handleSubmit} />

    </div>

  );

}
```

**By wrapping `handleSubmit` in `useCallback`, you ensure that it’s the *same* function between the re-renders** (until dependencies change). You don’t *have to* wrap a function in `useCallback` unless you do it for some specific reason. In this example, the reason is that you pass it to a component wrapped in [`memo`,](/reference/react/memo) and this lets it skip re-rendering. There are other reasons you might need `useCallback` which are described further on this page.

### Note

**You should only rely on `useCallback` as a performance optimization.** If your code doesn’t work without it, find the underlying problem and fix it first. Then you may add `useCallback` back.

##### Deep Dive#### How is useCallback related to useMemo?[](#how-is-usecallback-related-to-usememo "Link for How is useCallback related to useMemo? ")

You will often see [`useMemo`](/reference/react/useMemo) alongside `useCallback`. They are both useful when you’re trying to optimize a child component. They let you [memoize](https://en.wikipedia.org/wiki/Memoization) (or, in other words, cache) something you’re passing down:

```
import { useMemo, useCallback } from 'react';



function ProductPage({ productId, referrer }) {

  const product = useData('/product/' + productId);



  const requirements = useMemo(() => { // Calls your function and caches its result

    return computeRequirements(product);

  }, [product]);



  const handleSubmit = useCallback((orderDetails) => { // Caches your function itself

    post('/product/' + productId + '/buy', {

      referrer,

      orderDetails,

    });

  }, [productId, referrer]);



  return (

    <div className={theme}>

      <ShippingForm requirements={requirements} onSubmit={handleSubmit} />

    </div>

  );

}
```

The difference is in *what* they’re letting you cache:

* **[`useMemo`](/reference/react/useMemo) caches the *result* of calling your function.** In this example, it caches the result of calling `computeRequirements(product)` so that it doesn’t change unless `product` has changed. This lets you pass the `requirements` object down without unnecessarily re-rendering `ShippingForm`. When necessary, React will call the function you’ve passed during rendering to calculate the result.
* **`useCallback` caches *the function itself.*** Unlike `useMemo`, it does not call the function you provide. Instead, it caches the function you provided so that `handleSubmit` *itself* doesn’t change unless `productId` or `referrer` has changed. This lets you pass the `handleSubmit` function down without unnecessarily re-rendering `ShippingForm`. Your code won’t run until the user submits the form.

If you’re already familiar with [`useMemo`,](/reference/react/useMemo) you might find it helpful to think of `useCallback` as this:

```
// Simplified implementation (inside React)

function useCallback(fn, dependencies) {

  return useMemo(() => fn, dependencies);

}
```

```
import { useCallback } from 'react';
import ShippingForm from './ShippingForm.js';

export default function ProductPage({ productId, referrer, theme }) {
  const handleSubmit = useCallback((orderDetails) => {
    post('/product/' + productId + '/buy', {
      referrer,
      orderDetails,
    });
  }, [productId, referrer]);

  return (
    <div className={theme}>
      <ShippingForm onSubmit={handleSubmit} />
    </div>
  );
}

function post(url, data) {
  // Imagine this sends a request...
  console.log('POST /' + url);
  console.log(data);
}
```

***

### Updating state from a memoized callback[](#updating-state-from-a-memoized-callback "Link for Updating state from a memoized callback ")

Sometimes, you might need to update state based on previous state from a memoized callback.

This `handleAddTodo` function specifies `todos` as a dependency because it computes the next todos from it:

```
function TodoList() {

  const [todos, setTodos] = useState([]);



  const handleAddTodo = useCallback((text) => {

    const newTodo = { id: nextId++, text };

    setTodos([...todos, newTodo]);

  }, [todos]);

  // ...
```

You’ll usually want memoized functions to have as few dependencies as possible. When you read some state only to calculate the next state, you can remove that dependency by passing an [updater function](/reference/react/useState#updating-state-based-on-the-previous-state) instead:

```
function TodoList() {

  const [todos, setTodos] = useState([]);



  const handleAddTodo = useCallback((text) => {

    const newTodo = { id: nextId++, text };

    setTodos(todos => [...todos, newTodo]);

  }, []); // ✅ No need for the todos dependency

  // ...
```

Here, instead of making `todos` a dependency and reading it inside, you pass an instruction about *how* to update the state (`todos => [...todos, newTodo]`) to React. [Read more about updater functions.](/reference/react/useState#updating-state-based-on-the-previous-state)

***

### Preventing an Effect from firing too often[](#preventing-an-effect-from-firing-too-often "Link for Preventing an Effect from firing too often ")

Sometimes, you might want to call a function from inside an [Effect:](/learn/synchronizing-with-effects)

```
function ChatRoom({ roomId }) {

  const [message, setMessage] = useState('');



  function createOptions() {

    return {

      serverUrl: 'https://localhost:1234',

      roomId: roomId

    };

  }



  useEffect(() => {

    const options = createOptions();

    const connection = createConnection(options);

    connection.connect();

    // ...
```

This creates a problem. [Every reactive value must be declared as a dependency of your Effect.](/learn/lifecycle-of-reactive-effects#react-verifies-that-you-specified-every-reactive-value-as-a-dependency) However, if you declare `createOptions` as a dependency, it will cause your Effect to constantly reconnect to the chat room:

```
  useEffect(() => {

    const options = createOptions();

    const connection = createConnection(options);

    connection.connect();

    return () => connection.disconnect();

  }, [createOptions]); // 🔴 Problem: This dependency changes on every render

  // ...
```

To solve this, you can wrap the function you need to call from an Effect into `useCallback`:

```
function ChatRoom({ roomId }) {

  const [message, setMessage] = useState('');



  const createOptions = useCallback(() => {

    return {

      serverUrl: 'https://localhost:1234',

      roomId: roomId

    };

  }, [roomId]); // ✅ Only changes when roomId changes



  useEffect(() => {

    const options = createOptions();

    const connection = createConnection(options);

    connection.connect();

    return () => connection.disconnect();

  }, [createOptions]); // ✅ Only changes when createOptions changes

  // ...
```

This ensures that the `createOptions` function is the same between re-renders if the `roomId` is the same. **However, it’s even better to remove the need for a function dependency.** Move your function *inside* the Effect:

```
function ChatRoom({ roomId }) {

  const [message, setMessage] = useState('');



  useEffect(() => {

    function createOptions() { // ✅ No need for useCallback or function dependencies!

      return {

        serverUrl: 'https://localhost:1234',

        roomId: roomId

      };

    }



    const options = createOptions();

    const connection = createConnection(options);

    connection.connect();

    return () => connection.disconnect();

  }, [roomId]); // ✅ Only changes when roomId changes

  // ...
```

Now your code is simpler and doesn’t need `useCallback`. [Learn more about removing Effect dependencies.](/learn/removing-effect-dependencies#move-dynamic-objects-and-functions-inside-your-effect)

***

### Optimizing a custom Hook[](#optimizing-a-custom-hook "Link for Optimizing a custom Hook ")

If you’re writing a [custom Hook,](/learn/reusing-logic-with-custom-hooks) it’s recommended to wrap any functions that it returns into `useCallback`:

```
function useRouter() {

  const { dispatch } = useContext(RouterStateContext);



  const navigate = useCallback((url) => {

    dispatch({ type: 'navigate', url });

  }, [dispatch]);



  const goBack = useCallback(() => {

    dispatch({ type: 'back' });

  }, [dispatch]);



  return {

    navigate,

    goBack,

  };

}
```

This ensures that the consumers of your Hook can optimize their own code when needed.

***

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### Every time my component renders, `useCallback` returns a different function[](#every-time-my-component-renders-usecallback-returns-a-different-function "Link for this heading")

Make sure you’ve specified the dependency array as a second argument!

If you forget the dependency array, `useCallback` will return a new function every time:

```
function ProductPage({ productId, referrer }) {

  const handleSubmit = useCallback((orderDetails) => {

    post('/product/' + productId + '/buy', {

      referrer,

      orderDetails,

    });

  }); // 🔴 Returns a new function every time: no dependency array

  // ...
```

This is the corrected version passing the dependency array as a second argument:

```
function ProductPage({ productId, referrer }) {

  const handleSubmit = useCallback((orderDetails) => {

    post('/product/' + productId + '/buy', {

      referrer,

      orderDetails,

    });

  }, [productId, referrer]); // ✅ Does not return a new function unnecessarily

  // ...
```

If this doesn’t help, then the problem is that at least one of your dependencies is different from the previous render. You can debug this problem by manually logging your dependencies to the console:

```
  const handleSubmit = useCallback((orderDetails) => {

    // ..

  }, [productId, referrer]);



  console.log([productId, referrer]);
```

You can then right-click on the arrays from different re-renders in the console and select “Store as a global variable” for both of them. Assuming the first one got saved as `temp1` and the second one got saved as `temp2`, you can then use the browser console to check whether each dependency in both arrays is the same:

```
Object.is(temp1[0], temp2[0]); // Is the first dependency the same between the arrays?

Object.is(temp1[1], temp2[1]); // Is the second dependency the same between the arrays?

Object.is(temp1[2], temp2[2]); // ... and so on for every dependency ...
```

When you find which dependency is breaking memoization, either find a way to remove it, or [memoize it as well.](/reference/react/useMemo#memoizing-a-dependency-of-another-hook)

***

### I need to call `useCallback` for each list item in a loop, but it’s not allowed[](#i-need-to-call-usememo-for-each-list-item-in-a-loop-but-its-not-allowed "Link for this heading")

Suppose the `Chart` component is wrapped in [`memo`](/reference/react/memo). You want to skip re-rendering every `Chart` in the list when the `ReportList` component re-renders. However, you can’t call `useCallback` in a loop:

```
function ReportList({ items }) {

  return (

    <article>

      {items.map(item => {

        // 🔴 You can't call useCallback in a loop like this:

        const handleClick = useCallback(() => {

          sendReport(item)

        }, [item]);



        return (

          <figure key={item.id}>

            <Chart onClick={handleClick} />

          </figure>

        );

      })}

    </article>

  );

}
```

Instead, extract a component for an individual item, and put `useCallback` there:

```
function ReportList({ items }) {

  return (

    <article>

      {items.map(item =>

        <Report key={item.id} item={item} />

      )}

    </article>

  );

}



function Report({ item }) {

  // ✅ Call useCallback at the top level:

  const handleClick = useCallback(() => {

    sendReport(item)

  }, [item]);



  return (

    <figure>

      <Chart onClick={handleClick} />

    </figure>

  );

}
```

Alternatively, you could remove `useCallback` in the last snippet and instead wrap `Report` itself in [`memo`.](/reference/react/memo) If the `item` prop does not change, `Report` will skip re-rendering, so `Chart` will skip re-rendering too:

```
function ReportList({ items }) {

  // ...

}



const Report = memo(function Report({ item }) {

  function handleClick() {

    sendReport(item);

  }



  return (

    <figure>

      <Chart onClick={handleClick} />

    </figure>

  );

});
```

[PrevioususeActionState](/reference/react/useActionState)

[NextuseContext](/reference/react/useContext)

***

----
