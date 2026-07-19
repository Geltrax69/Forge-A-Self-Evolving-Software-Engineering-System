url: https://react.dev/reference/react/useState
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useState[](#undefined "Link for this heading")

`useState` is a React Hook that lets you add a [state variable](/learn/state-a-components-memory) to your component.

```
const [state, setState] = useState(initialState)
```

***

## Reference[](#reference "Link for Reference ")

### `useState(initialState)`[](#usestate "Link for this heading")

Call `useState` at the top level of your component to declare a [state variable.](/learn/state-a-components-memory)

```
import { useState } from 'react';



function MyComponent() {

  const [age, setAge] = useState(28);

  const [name, setName] = useState('Taylor');

  const [todos, setTodos] = useState(() => createTodos());

  // ...
```

***

### `set` functions, like `setSomething(nextState)`[](#setstate "Link for this heading")

The `set` function returned by `useState` lets you update the state to a different value and trigger a re-render. You can pass the next state directly, or a function that calculates it from the previous state:

```
const [name, setName] = useState('Edward');



function handleClick() {

  setName('Taylor');

  setAge(a => a + 1);

  // ...
```

***

## Usage[](#usage "Link for Usage ")

### Adding state to a component[](#adding-state-to-a-component "Link for Adding state to a component ")

Call `useState` at the top level of your component to declare one or more [state variables.](/learn/state-a-components-memory)

```
import { useState } from 'react';



function MyComponent() {

  const [age, setAge] = useState(42);

  const [name, setName] = useState('Taylor');

  // ...
```

The convention is to name state variables like `[something, setSomething]` using [array destructuring.](https://javascript.info/destructuring-assignment)

`useState` returns an array with exactly two items:

1. The current state of this state variable, initially set to the initial state you provided.
2. The `set` function that lets you change it to any other value in response to interaction.

To update what’s on the screen, call the `set` function with some next state:

```
function handleClick() {

  setName('Robin');

}
```

React will store the next state, render your component again with the new values, and update the UI.

### Pitfall

Calling the `set` function [**does not** change the current state in the already executing code](#ive-updated-the-state-but-logging-gives-me-the-old-value):

```
function handleClick() {

  setName('Robin');

  console.log(name); // Still "Taylor"!

}
```

It only affects what `useState` will return starting from the *next* render.

#### Basic useState examples[](#examples-basic "Link for Basic useState examples")

#### Example 1 of 4:Counter (number)[](#counter-number "Link for this heading")

In this example, the `count` state variable holds a number. Clicking the button increments it.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <button onClick={handleClick}>
      You pressed me {count} times
    </button>
  );
}
```

***

### Updating state based on the previous state[](#updating-state-based-on-the-previous-state "Link for Updating state based on the previous state ")

Suppose the `age` is `42`. This handler calls `setAge(age + 1)` three times:

```
function handleClick() {

  setAge(age + 1); // setAge(42 + 1)

  setAge(age + 1); // setAge(42 + 1)

  setAge(age + 1); // setAge(42 + 1)

}
```

However, after one click, `age` will only be `43` rather than `45`! This is because calling the `set` function [does not update](/learn/state-as-a-snapshot) the `age` state variable in the already running code. So each `setAge(age + 1)` call becomes `setAge(43)`.

To solve this problem, **you may pass an *updater function*** to `setAge` instead of the next state:

```
function handleClick() {

  setAge(a => a + 1); // setAge(42 => 43)

  setAge(a => a + 1); // setAge(43 => 44)

  setAge(a => a + 1); // setAge(44 => 45)

}
```

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useState } from 'react';

export default function Counter() {
  const [age, setAge] = useState(42);

  function increment() {
    setAge(a => a + 1);
  }

  return (
    <>
      <h1>Your age: {age}</h1>
      <button onClick={() => {
        increment();
        increment();
        increment();
      }}>+3</button>
      <button onClick={() => {
        increment();
      }}>+1</button>
    </>
  );
}
```

***

### Updating objects and arrays in state[](#updating-objects-and-arrays-in-state "Link for Updating objects and arrays in state ")

You can put objects and arrays into state. In React, state is considered read-only, so **you should *replace* it rather than *mutate* your existing objects**. For example, if you have a `form` object in state, don’t mutate it:

```
// 🚩 Don't mutate an object in state like this:

form.firstName = 'Taylor';
```

Instead, replace the whole object by creating a new one:

```
// ✅ Replace state with a new object

setForm({

  ...form,

  firstName: 'Taylor'

});
```

Read [updating objects in state](/learn/updating-objects-in-state) and [updating arrays in state](/learn/updating-arrays-in-state) to learn more.

#### Examples of objects and arrays in state[](#examples-objects "Link for Examples of objects and arrays in state")

#### Example 1 of 4:Form (object)[](#form-object "Link for this heading")

In this example, the `form` state variable holds an object. Each input has a change handler that calls `setForm` with the next state of the entire form. The `{ ...form }` spread syntax ensures that the state object is replaced rather than mutated.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useState } from 'react';

export default function Form() {
  const [form, setForm] = useState({
    firstName: 'Barbara',
    lastName: 'Hepworth',
    email: 'bhepworth@sculpture.com',
  });

  return (
    <>
      <label>
        First name:
        <input
          value={form.firstName}
          onChange={e => {
            setForm({
              ...form,
              firstName: e.target.value
            });
          }}
        />
      </label>
      <label>
        Last name:
        <input
          value={form.lastName}
          onChange={e => {
            setForm({
              ...form,
              lastName: e.target.value
            });
          }}
        />
      </label>
      <label>
        Email:
        <input
          value={form.email}
          onChange={e => {
            setForm({
              ...form,
              email: e.target.value
            });
          }}
        />
      </label>
      <p>
        {form.firstName}{' '}
        {form.lastName}{' '}
        ({form.email})
      </p>
    </>
  );
}
```

***

### Avoiding recreating the initial state[](#avoiding-recreating-the-initial-state "Link for Avoiding recreating the initial state ")

React saves the initial state once and ignores it on the next renders.

```
function TodoList() {

  const [todos, setTodos] = useState(createInitialTodos());

  // ...
```

Although the result of `createInitialTodos()` is only used for the initial render, you’re still calling this function on every render. This can be wasteful if it’s creating large arrays or performing expensive calculations.

To solve this, you may **pass it as an *initializer* function** to `useState` instead:

```
function TodoList() {

  const [todos, setTodos] = useState(createInitialTodos);

  // ...
```

Notice that you’re passing `createInitialTodos`, which is the *function itself*, and not `createInitialTodos()`, which is the result of calling it. If you pass a function to `useState`, React will only call it during initialization.

React may [call your initializers twice](#my-initializer-or-updater-function-runs-twice) in development to verify that they are [pure.](/learn/keeping-components-pure)

#### The difference between passing an initializer and passing the initial state directly[](#examples-initializer "Link for The difference between passing an initializer and passing the initial state directly")

#### Example 1 of 2:Passing the initializer function[](#passing-the-initializer-function "Link for this heading")

This example passes the initializer function, so the `createInitialTodos` function only runs during initialization. It does not run when component re-renders, such as when you type into the input.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useState } from 'react';

function createInitialTodos() {
  const initialTodos = [];
  for (let i = 0; i < 50; i++) {
    initialTodos.push({
      id: i,
      text: 'Item ' + (i + 1)
    });
  }
  return initialTodos;
}

export default function TodoList() {
  const [todos, setTodos] = useState(createInitialTodos);
  const [text, setText] = useState('');

  return (
    <>
      <input
        value={text}
        onChange={e => setText(e.target.value)}
      />
      <button onClick={() => {
        setText('');
        setTodos([{
          id: todos.length,
          text: text
        }, ...todos]);
      }}>Add</button>
      <ul>
        {todos.map(item => (
          <li key={item.id}>
            {item.text}
          </li>
        ))}
      </ul>
    </>
  );
}
```

***

### Resetting state with a key[](#resetting-state-with-a-key "Link for Resetting state with a key ")

You’ll often encounter the `key` attribute when [rendering lists.](/learn/rendering-lists) However, it also serves another purpose.

You can **reset a component’s state by passing a different `key` to a component.** In this example, the Reset button changes the `version` state variable, which we pass as a `key` to the `Form`. When the `key` changes, React re-creates the `Form` component (and all of its children) from scratch, so its state gets reset.

Read [preserving and resetting state](/learn/preserving-and-resetting-state) to learn more.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useState } from 'react';

export default function App() {
  const [version, setVersion] = useState(0);

  function handleReset() {
    setVersion(version + 1);
  }

  return (
    <>
      <button onClick={handleReset}>Reset</button>
      <Form key={version} />
    </>
  );
}

function Form() {
  const [name, setName] = useState('Taylor');

  return (
    <>
      <input
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <p>Hello, {name}.</p>
    </>
  );
}
```

***

```
export default function CountLabel({ count }) {

  return <h1>{count}</h1>

}
```

Say you want to show whether the counter has *increased or decreased* since the last change. The `count` prop doesn’t tell you this — you need to keep track of its previous value. Add the `prevCount` state variable to track it. Add another state variable called `trend` to hold whether the count has increased or decreased. Compare `prevCount` with `count`, and if they’re not equal, update both `prevCount` and `trend`. Now you can show both the current count prop and *how it has changed since the last render*.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useState } from 'react';

export default function CountLabel({ count }) {
  const [prevCount, setPrevCount] = useState(count);
  const [trend, setTrend] = useState(null);
  if (prevCount !== count) {
    setPrevCount(count);
    setTrend(count > prevCount ? 'increasing' : 'decreasing');
  }
  return (
    <>
      <h1>{count}</h1>
      {trend && <p>The count is {trend}</p>}
    </>
  );
}
```

Note that if you call a `set` function while rendering, it must be inside a condition like `prevCount !== count`, and there must be a call like `setPrevCount(count)` inside of the condition. Otherwise, your component would re-render in a loop until it crashes. Also, you can only update the state of the *currently rendering* component like this. Calling the `set` function of *another* component during rendering is an error. Finally, your `set` call should still [update state without mutation](#updating-objects-and-arrays-in-state) — this doesn’t mean you can break other rules of [pure functions.](/learn/keeping-components-pure)

This pattern can be hard to understand and is usually best avoided. However, it’s better than updating state in an effect. When you call the `set` function during render, React will re-render that component immediately after your component exits with a `return` statement, and before rendering the children. This way, children don’t need to render twice. The rest of your component function will still execute (and the result will be thrown away). If your condition is below all the Hook calls, you may add an early `return;` to restart rendering earlier.

***

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### I’ve updated the state, but logging gives me the old value[](#ive-updated-the-state-but-logging-gives-me-the-old-value "Link for I’ve updated the state, but logging gives me the old value ")

Calling the `set` function **does not change state in the running code**:

```
function handleClick() {

  console.log(count);  // 0



  setCount(count + 1); // Request a re-render with 1

  console.log(count);  // Still 0!



  setTimeout(() => {

    console.log(count); // Also 0!

  }, 5000);

}
```

This is because [states behaves like a snapshot.](/learn/state-as-a-snapshot) Updating state requests another render with the new state value, but does not affect the `count` JavaScript variable in your already-running event handler.

If you need to use the next state, you can save it in a variable before passing it to the `set` function:

```
const nextCount = count + 1;

setCount(nextCount);



console.log(count);     // 0

console.log(nextCount); // 1
```

***

### I’ve updated the state, but the screen doesn’t update[](#ive-updated-the-state-but-the-screen-doesnt-update "Link for I’ve updated the state, but the screen doesn’t update ")

React will **ignore your update if the next state is equal to the previous state,** as determined by an [`Object.is`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. This usually happens when you change an object or an array in state directly:

```
obj.x = 10;  // 🚩 Wrong: mutating existing object

setObj(obj); // 🚩 Doesn't do anything
```

You mutated an existing `obj` object and passed it back to `setObj`, so React ignored the update. To fix this, you need to ensure that you’re always [*replacing* objects and arrays in state instead of *mutating* them](#updating-objects-and-arrays-in-state):

```
// ✅ Correct: creating a new object

setObj({

  ...obj,

  x: 10

});
```

***

### I’m getting an error: “Too many re-renders”[](#im-getting-an-error-too-many-re-renders "Link for I’m getting an error: “Too many re-renders” ")

You might get an error that says: `Too many re-renders. React limits the number of renders to prevent an infinite loop.` Typically, this means that you’re unconditionally setting state *during render*, so your component enters a loop: render, set state (which causes a render), render, set state (which causes a render), and so on. Very often, this is caused by a mistake in specifying an event handler:

```
// 🚩 Wrong: calls the handler during render

return <button onClick={handleClick()}>Click me</button>



// ✅ Correct: passes down the event handler

return <button onClick={handleClick}>Click me</button>



// ✅ Correct: passes down an inline function

return <button onClick={(e) => handleClick(e)}>Click me</button>
```

If you can’t find the cause of this error, click on the arrow next to the error in the console and look through the JavaScript stack to find the specific `set` function call responsible for the error.

***

### My initializer or updater function runs twice[](#my-initializer-or-updater-function-runs-twice "Link for My initializer or updater function runs twice ")

In [Strict Mode](/reference/react/StrictMode), React will call some of your functions twice instead of once:

```
function TodoList() {

  // This component function will run twice for every render.



  const [todos, setTodos] = useState(() => {

    // This initializer function will run twice during initialization.

    return createTodos();

  });



  function handleClick() {

    setTodos(prevTodos => {

      // This updater function will run twice for every click.

      return [...prevTodos, createTodo()];

    });

  }

  // ...
```

This is expected and shouldn’t break your code.

This **development-only** behavior helps you [keep components pure.](/learn/keeping-components-pure) React uses the result of one of the calls, and ignores the result of the other call. As long as your component, initializer, and updater functions are pure, this shouldn’t affect your logic. However, if they are accidentally impure, this helps you notice the mistakes.

For example, this impure updater function mutates an array in state:

```
setTodos(prevTodos => {

  // 🚩 Mistake: mutating state

  prevTodos.push(createTodo());

});
```

Because React calls your updater function twice, you’ll see the todo was added twice, so you’ll know that there is a mistake. In this example, you can fix the mistake by [replacing the array instead of mutating it](#updating-objects-and-arrays-in-state):

```
setTodos(prevTodos => {

  // ✅ Correct: replacing with new state

  return [...prevTodos, createTodo()];

});
```

Now that this updater function is pure, calling it an extra time doesn’t make a difference in behavior. This is why React calling it twice helps you find mistakes. **Only component, initializer, and updater functions need to be pure.** Event handlers don’t need to be pure, so React will never call your event handlers twice.

Read [keeping components pure](/learn/keeping-components-pure) to learn more.

***

### I’m trying to set state to a function, but it gets called instead[](#im-trying-to-set-state-to-a-function-but-it-gets-called-instead "Link for I’m trying to set state to a function, but it gets called instead ")

You can’t put a function into state like this:

```
const [fn, setFn] = useState(someFunction);



function handleClick() {

  setFn(someOtherFunction);

}
```

Because you’re passing a function, React assumes that `someFunction` is an [initializer function](#avoiding-recreating-the-initial-state), and that `someOtherFunction` is an [updater function](#updating-state-based-on-the-previous-state), so it tries to call them and store the result. To actually *store* a function, you have to put `() =>` before them in both cases. Then React will store the functions you pass.

```
const [fn, setFn] = useState(() => someFunction);



function handleClick() {

  setFn(() => someOtherFunction);

}
```

[PrevioususeRef](/reference/react/useRef)

[NextuseSyncExternalStore](/reference/react/useSyncExternalStore)

***

----
