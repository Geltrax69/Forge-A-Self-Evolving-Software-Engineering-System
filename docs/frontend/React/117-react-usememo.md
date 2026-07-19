url: https://react.dev/reference/react/useMemo
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useMemo[](#undefined "Link for this heading")

`useMemo` is a React Hook that lets you cache the result of a calculation between re-renders.

```
const cachedValue = useMemo(calculateValue, dependencies)
```

### Note

[React Compiler](/learn/react-compiler) automatically memoizes values and functions, reducing the need for manual `useMemo` calls. You can use the compiler to handle memoization automatically.

***

## Reference[](#reference "Link for Reference ")

### `useMemo(calculateValue, dependencies)`[](#usememo "Link for this heading")

Call `useMemo` at the top level of your component to cache a calculation between re-renders:

```
import { useMemo } from 'react';



function TodoList({ todos, tab }) {

  const visibleTodos = useMemo(

    () => filterTodos(todos, tab),

    [todos, tab]

  );

  // ...

}
```

***

## Usage[](#usage "Link for Usage ")

### Skipping expensive recalculations[](#skipping-expensive-recalculations "Link for Skipping expensive recalculations ")

To cache a calculation between re-renders, wrap it in a `useMemo` call at the top level of your component:

```
import { useMemo } from 'react';



function TodoList({ todos, tab, theme }) {

  const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);

  // ...

}
```

```
function TodoList({ todos, tab, theme }) {

  const visibleTodos = filterTodos(todos, tab);

  // ...

}
```

Usually, this isn’t a problem because most calculations are very fast. However, if you’re filtering or transforming a large array, or doing some expensive computation, you might want to skip doing it again if data hasn’t changed. If both `todos` and `tab` are the same as they were during the last render, wrapping the calculation in `useMemo` like earlier lets you reuse `visibleTodos` you’ve already calculated before.

This type of caching is called *[memoization.](https://en.wikipedia.org/wiki/Memoization)*

### Note

**You should only rely on `useMemo` as a performance optimization.** If your code doesn’t work without it, find the underlying problem and fix it first. Then you may add `useMemo` to improve performance.

##### Deep Dive#### How to tell if a calculation is expensive?[](#how-to-tell-if-a-calculation-is-expensive "Link for How to tell if a calculation is expensive? ")

In general, unless you’re creating or looping over thousands of objects, it’s probably not expensive. If you want to get more confidence, you can add a console log to measure the time spent in a piece of code:

```
console.time('filter array');

const visibleTodos = filterTodos(todos, tab);

console.timeEnd('filter array');
```

Perform the interaction you’re measuring (for example, typing into the input). You will then see logs like `filter array: 0.15ms` in your console. If the overall logged time adds up to a significant amount (say, `1ms` or more), it might make sense to memoize that calculation. As an experiment, you can then wrap the calculation in `useMemo` to verify whether the total logged time has decreased for that interaction or not:

```
console.time('filter array');

const visibleTodos = useMemo(() => {

  return filterTodos(todos, tab); // Skipped if todos and tab haven't changed

}, [todos, tab]);

console.timeEnd('filter array');
```

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useMemo } from 'react';
import { filterTodos } from './utils.js'

export default function TodoList({ todos, theme, tab }) {
  const visibleTodos = useMemo(
    () => filterTodos(todos, tab),
    [todos, tab]
  );
  return (
    <div className={theme}>
      <p><b>Note: <code>filterTodos</code> is artificially slowed down!</b></p>
      <ul>
        {visibleTodos.map(todo => (
          <li key={todo.id}>
            {todo.completed ?
              <s>{todo.text}</s> :
              todo.text
            }
          </li>
        ))}
      </ul>
    </div>
  );
}
```

***

### Skipping re-rendering of components[](#skipping-re-rendering-of-components "Link for Skipping re-rendering of components ")

In some cases, `useMemo` can also help you optimize performance of re-rendering child components. To illustrate this, let’s say this `TodoList` component passes the `visibleTodos` as a prop to the child `List` component:

```
export default function TodoList({ todos, tab, theme }) {

  // ...

  return (

    <div className={theme}>

      <List items={visibleTodos} />

    </div>

  );

}
```

You’ve noticed that toggling the `theme` prop freezes the app for a moment, but if you remove `<List />` from your JSX, it feels fast. This tells you that it’s worth trying to optimize the `List` component.

**By default, when a component re-renders, React re-renders all of its children recursively.** This is why, when `TodoList` re-renders with a different `theme`, the `List` component *also* re-renders. This is fine for components that don’t require much calculation to re-render. But if you’ve verified that a re-render is slow, you can tell `List` to skip re-rendering when its props are the same as on last render by wrapping it in [`memo`:](/reference/react/memo)

```
import { memo } from 'react';



const List = memo(function List({ items }) {

  // ...

});
```

**With this change, `List` will skip re-rendering if all of its props are the *same* as on the last render.** This is where caching the calculation becomes important! Imagine that you calculated `visibleTodos` without `useMemo`:

```
export default function TodoList({ todos, tab, theme }) {

  // Every time the theme changes, this will be a different array...

  const visibleTodos = filterTodos(todos, tab);

  return (

    <div className={theme}>

      {/* ... so List's props will never be the same, and it will re-render every time */}

      <List items={visibleTodos} />

    </div>

  );

}
```

**In the above example, the `filterTodos` function always creates a *different* array,** similar to how the `{}` object literal always creates a new object. Normally, this wouldn’t be a problem, but it means that `List` props will never be the same, and your [`memo`](/reference/react/memo) optimization won’t work. This is where `useMemo` comes in handy:

```
export default function TodoList({ todos, tab, theme }) {

  // Tell React to cache your calculation between re-renders...

  const visibleTodos = useMemo(

    () => filterTodos(todos, tab),

    [todos, tab] // ...so as long as these dependencies don't change...

  );

  return (

    <div className={theme}>

      {/* ...List will receive the same props and can skip re-rendering */}

      <List items={visibleTodos} />

    </div>

  );

}
```

**By wrapping the `visibleTodos` calculation in `useMemo`, you ensure that it has the *same* value between the re-renders** (until dependencies change). You don’t *have to* wrap a calculation in `useMemo` unless you do it for some specific reason. In this example, the reason is that you pass it to a component wrapped in [`memo`,](/reference/react/memo) and this lets it skip re-rendering. There are a few other reasons to add `useMemo` which are described further on this page.

##### Deep Dive#### Memoizing individual JSX nodes[](#memoizing-individual-jsx-nodes "Link for Memoizing individual JSX nodes ")

Instead of wrapping `List` in [`memo`](/reference/react/memo), you could wrap the `<List />` JSX node itself in `useMemo`:

```
export default function TodoList({ todos, tab, theme }) {

  const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);

  const children = useMemo(() => <List items={visibleTodos} />, [visibleTodos]);

  return (

    <div className={theme}>

      {children}

    </div>

  );

}
```

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useMemo } from 'react';
import List from './List.js';
import { filterTodos } from './utils.js'

export default function TodoList({ todos, theme, tab }) {
  const visibleTodos = useMemo(
    () => filterTodos(todos, tab),
    [todos, tab]
  );
  return (
    <div className={theme}>
      <p><b>Note: <code>List</code> is artificially slowed down!</b></p>
      <List items={visibleTodos} />
    </div>
  );
}
```

***

### Preventing an Effect from firing too often[](#preventing-an-effect-from-firing-too-often "Link for Preventing an Effect from firing too often ")

Sometimes, you might want to use a value inside an [Effect:](/learn/synchronizing-with-effects)

```
function ChatRoom({ roomId }) {

  const [message, setMessage] = useState('');



  const options = {

    serverUrl: 'https://localhost:1234',

    roomId: roomId

  }



  useEffect(() => {

    const connection = createConnection(options);

    connection.connect();

    // ...
```

This creates a problem. [Every reactive value must be declared as a dependency of your Effect.](/learn/lifecycle-of-reactive-effects#react-verifies-that-you-specified-every-reactive-value-as-a-dependency) However, if you declare `options` as a dependency, it will cause your Effect to constantly reconnect to the chat room:

```
  useEffect(() => {

    const connection = createConnection(options);

    connection.connect();

    return () => connection.disconnect();

  }, [options]); // 🔴 Problem: This dependency changes on every render

  // ...
```

To solve this, you can wrap the object you need to call from an Effect in `useMemo`:

```
function ChatRoom({ roomId }) {

  const [message, setMessage] = useState('');



  const options = useMemo(() => {

    return {

      serverUrl: 'https://localhost:1234',

      roomId: roomId

    };

  }, [roomId]); // ✅ Only changes when roomId changes



  useEffect(() => {

    const connection = createConnection(options);

    connection.connect();

    return () => connection.disconnect();

  }, [options]); // ✅ Only changes when options changes

  // ...
```

This ensures that the `options` object is the same between re-renders if `useMemo` returns the cached object.

However, since `useMemo` is performance optimization, not a semantic guarantee, React may throw away the cached value if [there is a specific reason to do that](#caveats). This will also cause the effect to re-fire, **so it’s even better to remove the need for a function dependency** by moving your object *inside* the Effect:

```
function ChatRoom({ roomId }) {

  const [message, setMessage] = useState('');



  useEffect(() => {

    const options = { // ✅ No need for useMemo or object dependencies!

      serverUrl: 'https://localhost:1234',

      roomId: roomId

    }



    const connection = createConnection(options);

    connection.connect();

    return () => connection.disconnect();

  }, [roomId]); // ✅ Only changes when roomId changes

  // ...
```

Now your code is simpler and doesn’t need `useMemo`. [Learn more about removing Effect dependencies.](/learn/removing-effect-dependencies#move-dynamic-objects-and-functions-inside-your-effect)

### Memoizing a dependency of another Hook[](#memoizing-a-dependency-of-another-hook "Link for Memoizing a dependency of another Hook ")

Suppose you have a calculation that depends on an object created directly in the component body:

```
function Dropdown({ allItems, text }) {

  const searchOptions = { matchMode: 'whole-word', text };



  const visibleItems = useMemo(() => {

    return searchItems(allItems, searchOptions);

  }, [allItems, searchOptions]); // 🚩 Caution: Dependency on an object created in the component body

  // ...
```

Depending on an object like this defeats the point of memoization. When a component re-renders, all of the code directly inside the component body runs again. **The lines of code creating the `searchOptions` object will also run on every re-render.** Since `searchOptions` is a dependency of your `useMemo` call, and it’s different every time, React knows the dependencies are different, and recalculate `searchItems` every time.

To fix this, you could memoize the `searchOptions` object *itself* before passing it as a dependency:

```
function Dropdown({ allItems, text }) {

  const searchOptions = useMemo(() => {

    return { matchMode: 'whole-word', text };

  }, [text]); // ✅ Only changes when text changes



  const visibleItems = useMemo(() => {

    return searchItems(allItems, searchOptions);

  }, [allItems, searchOptions]); // ✅ Only changes when allItems or searchOptions changes

  // ...
```

In the example above, if the `text` did not change, the `searchOptions` object also won’t change. However, an even better fix is to move the `searchOptions` object declaration *inside* of the `useMemo` calculation function:

```
function Dropdown({ allItems, text }) {

  const visibleItems = useMemo(() => {

    const searchOptions = { matchMode: 'whole-word', text };

    return searchItems(allItems, searchOptions);

  }, [allItems, text]); // ✅ Only changes when allItems or text changes

  // ...
```

Now your calculation depends on `text` directly (which is a string and can’t “accidentally” become different).

***

### Memoizing a function[](#memoizing-a-function "Link for Memoizing a function ")

Suppose the `Form` component is wrapped in [`memo`.](/reference/react/memo) You want to pass a function to it as a prop:

```
export default function ProductPage({ productId, referrer }) {

  function handleSubmit(orderDetails) {

    post('/product/' + productId + '/buy', {

      referrer,

      orderDetails

    });

  }



  return <Form onSubmit={handleSubmit} />;

}
```

Just as `{}` creates a different object, function declarations like `function() {}` and expressions like `() => {}` produce a *different* function on every re-render. By itself, creating a new function is not a problem. This is not something to avoid! However, if the `Form` component is memoized, presumably you want to skip re-rendering it when no props have changed. A prop that is *always* different would defeat the point of memoization.

To memoize a function with `useMemo`, your calculation function would have to return another function:

```
export default function Page({ productId, referrer }) {

  const handleSubmit = useMemo(() => {

    return (orderDetails) => {

      post('/product/' + productId + '/buy', {

        referrer,

        orderDetails

      });

    };

  }, [productId, referrer]);



  return <Form onSubmit={handleSubmit} />;

}
```

This looks clunky! **Memoizing functions is common enough that React has a built-in Hook specifically for that. Wrap your functions into [`useCallback`](/reference/react/useCallback) instead of `useMemo`** to avoid having to write an extra nested function:

```
export default function Page({ productId, referrer }) {

  const handleSubmit = useCallback((orderDetails) => {

    post('/product/' + productId + '/buy', {

      referrer,

      orderDetails

    });

  }, [productId, referrer]);



  return <Form onSubmit={handleSubmit} />;

}
```

The two examples above are completely equivalent. The only benefit to `useCallback` is that it lets you avoid writing an extra nested function inside. It doesn’t do anything else. [Read more about `useCallback`.](/reference/react/useCallback)

***

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### My calculation runs twice on every re-render[](#my-calculation-runs-twice-on-every-re-render "Link for My calculation runs twice on every re-render ")

In [Strict Mode](/reference/react/StrictMode), React will call some of your functions twice instead of once:

```
function TodoList({ todos, tab }) {

  // This component function will run twice for every render.



  const visibleTodos = useMemo(() => {

    // This calculation will run twice if any of the dependencies change.

    return filterTodos(todos, tab);

  }, [todos, tab]);



  // ...
```

This is expected and shouldn’t break your code.

This **development-only** behavior helps you [keep components pure.](/learn/keeping-components-pure) React uses the result of one of the calls, and ignores the result of the other call. As long as your component and calculation functions are pure, this shouldn’t affect your logic. However, if they are accidentally impure, this helps you notice and fix the mistake.

For example, this impure calculation function mutates an array you received as a prop:

```
  const visibleTodos = useMemo(() => {

    // 🚩 Mistake: mutating a prop

    todos.push({ id: 'last', text: 'Go for a walk!' });

    const filtered = filterTodos(todos, tab);

    return filtered;

  }, [todos, tab]);
```

React calls your function twice, so you’d notice the todo is added twice. Your calculation shouldn’t change any existing objects, but it’s okay to change any *new* objects you created during the calculation. For example, if the `filterTodos` function always returns a *different* array, you can mutate *that* array instead:

```
  const visibleTodos = useMemo(() => {

    const filtered = filterTodos(todos, tab);

    // ✅ Correct: mutating an object you created during the calculation

    filtered.push({ id: 'last', text: 'Go for a walk!' });

    return filtered;

  }, [todos, tab]);
```

Read [keeping components pure](/learn/keeping-components-pure) to learn more about purity.

Also, check out the guides on [updating objects](/learn/updating-objects-in-state) and [updating arrays](/learn/updating-arrays-in-state) without mutation.

***

### My `useMemo` call is supposed to return an object, but returns undefined[](#my-usememo-call-is-supposed-to-return-an-object-but-returns-undefined "Link for this heading")

This code doesn’t work:

```
  // 🔴 You can't return an object from an arrow function with () => {

  const searchOptions = useMemo(() => {

    matchMode: 'whole-word',

    text: text

  }, [text]);
```

In JavaScript, `() => {` starts the arrow function body, so the `{` brace is not a part of your object. This is why it doesn’t return an object, and leads to mistakes. You could fix it by adding parentheses like `({` and `})`:

```
  // This works, but is easy for someone to break again

  const searchOptions = useMemo(() => ({

    matchMode: 'whole-word',

    text: text

  }), [text]);
```

However, this is still confusing and too easy for someone to break by removing the parentheses.

To avoid this mistake, write a `return` statement explicitly:

```
  // ✅ This works and is explicit

  const searchOptions = useMemo(() => {

    return {

      matchMode: 'whole-word',

      text: text

    };

  }, [text]);
```

***

### Every time my component renders, the calculation in `useMemo` re-runs[](#every-time-my-component-renders-the-calculation-in-usememo-re-runs "Link for this heading")

Make sure you’ve specified the dependency array as a second argument!

If you forget the dependency array, `useMemo` will re-run the calculation every time:

```
function TodoList({ todos, tab }) {

  // 🔴 Recalculates every time: no dependency array

  const visibleTodos = useMemo(() => filterTodos(todos, tab));

  // ...
```

This is the corrected version passing the dependency array as a second argument:

```
function TodoList({ todos, tab }) {

  // ✅ Does not recalculate unnecessarily

  const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);

  // ...
```

If this doesn’t help, then the problem is that at least one of your dependencies is different from the previous render. You can debug this problem by manually logging your dependencies to the console:

```
  const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);

  console.log([todos, tab]);
```

You can then right-click on the arrays from different re-renders in the console and select “Store as a global variable” for both of them. Assuming the first one got saved as `temp1` and the second one got saved as `temp2`, you can then use the browser console to check whether each dependency in both arrays is the same:

```
Object.is(temp1[0], temp2[0]); // Is the first dependency the same between the arrays?

Object.is(temp1[1], temp2[1]); // Is the second dependency the same between the arrays?

Object.is(temp1[2], temp2[2]); // ... and so on for every dependency ...
```

When you find which dependency breaks memoization, either find a way to remove it, or [memoize it as well.](#memoizing-a-dependency-of-another-hook)

***

### I need to call `useMemo` for each list item in a loop, but it’s not allowed[](#i-need-to-call-usememo-for-each-list-item-in-a-loop-but-its-not-allowed "Link for this heading")

Suppose the `Chart` component is wrapped in [`memo`](/reference/react/memo). You want to skip re-rendering every `Chart` in the list when the `ReportList` component re-renders. However, you can’t call `useMemo` in a loop:

```
function ReportList({ items }) {

  return (

    <article>

      {items.map(item => {

        // 🔴 You can't call useMemo in a loop like this:

        const data = useMemo(() => calculateReport(item), [item]);

        return (

          <figure key={item.id}>

            <Chart data={data} />

          </figure>

        );

      })}

    </article>

  );

}
```

Instead, extract a component for each item and memoize data for individual items:

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

  // ✅ Call useMemo at the top level:

  const data = useMemo(() => calculateReport(item), [item]);

  return (

    <figure>

      <Chart data={data} />

    </figure>

  );

}
```

Alternatively, you could remove `useMemo` and instead wrap `Report` itself in [`memo`.](/reference/react/memo) If the `item` prop does not change, `Report` will skip re-rendering, so `Chart` will skip re-rendering too:

```
function ReportList({ items }) {

  // ...

}



const Report = memo(function Report({ item }) {

  const data = calculateReport(item);

  return (

    <figure>

      <Chart data={data} />

    </figure>

  );

});
```

[PrevioususeLayoutEffect](/reference/react/useLayoutEffect)

[NextuseOptimistic](/reference/react/useOptimistic)

***

----
