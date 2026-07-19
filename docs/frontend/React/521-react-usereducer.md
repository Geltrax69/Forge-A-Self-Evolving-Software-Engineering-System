url: https://18.react.dev/reference/react/useReducer
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useReducer[](#undefined "Link for this heading")

`useReducer` is a React Hook that lets you add a [reducer](/learn/extracting-state-logic-into-a-reducer) to your component.

```
const [state, dispatch] = useReducer(reducer, initialArg, init?)
```

***

## Reference[](#reference "Link for Reference ")

### `useReducer(reducer, initialArg, init?)`[](#usereducer "Link for this heading")

Call `useReducer` at the top level of your component to manage its state with a [reducer.](/learn/extracting-state-logic-into-a-reducer)

```
import { useReducer } from 'react';



function reducer(state, action) {

  // ...

}



function MyComponent() {

  const [state, dispatch] = useReducer(reducer, { age: 42 });

  // ...
```

***

### `dispatch` function[](#dispatch "Link for this heading")

The `dispatch` function returned by `useReducer` lets you update the state to a different value and trigger a re-render. You need to pass the action as the only argument to the `dispatch` function:

```
const [state, dispatch] = useReducer(reducer, { age: 42 });



function handleClick() {

  dispatch({ type: 'incremented_age' });

  // ...
```

***

## Usage[](#usage "Link for Usage ")

### Adding a reducer to a component[](#adding-a-reducer-to-a-component "Link for Adding a reducer to a component ")

Call `useReducer` at the top level of your component to manage state with a [reducer.](/learn/extracting-state-logic-into-a-reducer)

```
import { useReducer } from 'react';



function reducer(state, action) {

  // ...

}



function MyComponent() {

  const [state, dispatch] = useReducer(reducer, { age: 42 });

  // ...
```

`useReducer` returns an array with exactly two items:

1. The current state of this state variable, initially set to the initial state you provided.
2. The `dispatch` function that lets you change it in response to interaction.

To update what’s on the screen, call `dispatch` with an object representing what the user did, called an *action*:

```
function handleClick() {

  dispatch({ type: 'incremented_age' });

}
```

React will pass the current state and the action to your reducer function. Your reducer will calculate and return the next state. React will store that next state, render your component with it, and update the UI.

```
import { useReducer } from 'react';

function reducer(state, action) {
  if (action.type === 'incremented_age') {
    return {
      age: state.age + 1
    };
  }
  throw Error('Unknown action.');
}

export default function Counter() {
  const [state, dispatch] = useReducer(reducer, { age: 42 });

  return (
    <>
      <button onClick={() => {
        dispatch({ type: 'incremented_age' })
      }}>
        Increment age
      </button>
      <p>Hello! You are {state.age}.</p>
    </>
  );
}
```

`useReducer` is very similar to [`useState`](/reference/react/useState), but it lets you move the state update logic from event handlers into a single function outside of your component. Read more about [choosing between `useState` and `useReducer`.](/learn/extracting-state-logic-into-a-reducer#comparing-usestate-and-usereducer)

***

### Writing the reducer function[](#writing-the-reducer-function "Link for Writing the reducer function ")

A reducer function is declared like this:

```
function reducer(state, action) {

  // ...

}
```

Then you need to fill in the code that will calculate and return the next state. By convention, it is common to write it as a [`switch` statement.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/switch) For each `case` in the `switch`, calculate and return some next state.

```
function reducer(state, action) {

  switch (action.type) {

    case 'incremented_age': {

      return {

        name: state.name,

        age: state.age + 1

      };

    }

    case 'changed_name': {

      return {

        name: action.nextName,

        age: state.age

      };

    }

  }

  throw Error('Unknown action: ' + action.type);

}
```

Actions can have any shape. By convention, it’s common to pass objects with a `type` property identifying the action. It should include the minimal necessary information that the reducer needs to compute the next state.

```
function Form() {

  const [state, dispatch] = useReducer(reducer, { name: 'Taylor', age: 42 });

  

  function handleButtonClick() {

    dispatch({ type: 'incremented_age' });

  }



  function handleInputChange(e) {

    dispatch({

      type: 'changed_name',

      nextName: e.target.value

    });

  }

  // ...
```

The action type names are local to your component. [Each action describes a single interaction, even if that leads to multiple changes in data.](/learn/extracting-state-logic-into-a-reducer#writing-reducers-well) The shape of the state is arbitrary, but usually it’ll be an object or an array.

Read [extracting state logic into a reducer](/learn/extracting-state-logic-into-a-reducer) to learn more.

### Pitfall

State is read-only. Don’t modify any objects or arrays in state:

```
function reducer(state, action) {

  switch (action.type) {

    case 'incremented_age': {

      // 🚩 Don't mutate an object in state like this:

      state.age = state.age + 1;

      return state;

    }
```

Instead, always return new objects from your reducer:

```
function reducer(state, action) {

  switch (action.type) {

    case 'incremented_age': {

      // ✅ Instead, return a new object

      return {

        ...state,

        age: state.age + 1

      };

    }
```

Read [updating objects in state](/learn/updating-objects-in-state) and [updating arrays in state](/learn/updating-arrays-in-state) to learn more.

#### Basic useReducer examples[](#examples-basic "Link for Basic useReducer examples")

#### Example 1 of 3:Form (object)[](#form-object "Link for this heading")

In this example, the reducer manages a state object with two fields: `name` and `age`.

```
import { useReducer } from 'react';

function reducer(state, action) {
  switch (action.type) {
    case 'incremented_age': {
      return {
        name: state.name,
        age: state.age + 1
      };
    }
    case 'changed_name': {
      return {
        name: action.nextName,
        age: state.age
      };
    }
  }
  throw Error('Unknown action: ' + action.type);
}

const initialState = { name: 'Taylor', age: 42 };

export default function Form() {
  const [state, dispatch] = useReducer(reducer, initialState);

  function handleButtonClick() {
    dispatch({ type: 'incremented_age' });
  }

  function handleInputChange(e) {
    dispatch({
      type: 'changed_name',
      nextName: e.target.value
    }); 
  }

  return (
    <>
      <input
        value={state.name}
        onChange={handleInputChange}
      />
      <button onClick={handleButtonClick}>
        Increment age
      </button>
      <p>Hello, {state.name}. You are {state.age}.</p>
    </>
  );
}
```

***

### Avoiding recreating the initial state[](#avoiding-recreating-the-initial-state "Link for Avoiding recreating the initial state ")

React saves the initial state once and ignores it on the next renders.

```
function createInitialState(username) {

  // ...

}



function TodoList({ username }) {

  const [state, dispatch] = useReducer(reducer, createInitialState(username));

  // ...
```

Although the result of `createInitialState(username)` is only used for the initial render, you’re still calling this function on every render. This can be wasteful if it’s creating large arrays or performing expensive calculations.

To solve this, you may **pass it as an *initializer* function** to `useReducer` as the third argument instead:

```
function createInitialState(username) {

  // ...

}



function TodoList({ username }) {

  const [state, dispatch] = useReducer(reducer, username, createInitialState);

  // ...
```

Notice that you’re passing `createInitialState`, which is the *function itself*, and not `createInitialState()`, which is the result of calling it. This way, the initial state does not get re-created after initialization.

In the above example, `createInitialState` takes a `username` argument. If your initializer doesn’t need any information to compute the initial state, you may pass `null` as the second argument to `useReducer`.

#### The difference between passing an initializer and passing the initial state directly[](#examples-initializer "Link for The difference between passing an initializer and passing the initial state directly")

#### Example 1 of 2:Passing the initializer function[](#passing-the-initializer-function "Link for this heading")

This example passes the initializer function, so the `createInitialState` function only runs during initialization. It does not run when component re-renders, such as when you type into the input.

```
import { useReducer } from 'react';

function createInitialState(username) {
  const initialTodos = [];
  for (let i = 0; i < 50; i++) {
    initialTodos.push({
      id: i,
      text: username + "'s task #" + (i + 1)
    });
  }
  return {
    draft: '',
    todos: initialTodos,
  };
}

function reducer(state, action) {
  switch (action.type) {
    case 'changed_draft': {
      return {
        draft: action.nextDraft,
        todos: state.todos,
      };
    };
    case 'added_todo': {
      return {
        draft: '',
        todos: [{
          id: state.todos.length,
          text: state.draft
        }, ...state.todos]
      }
    }
  }
  throw Error('Unknown action: ' + action.type);
}

export default function TodoList({ username }) {
  const [state, dispatch] = useReducer(
    reducer,
    username,
    createInitialState
  );
  return (
    <>
      <input
        value={state.draft}
        onChange={e => {
          dispatch({
            type: 'changed_draft',
            nextDraft: e.target.value
          })
        }}
      />
      <button onClick={() => {
        dispatch({ type: 'added_todo' });
      }}>Add</button>
      <ul>
        {state.todos.map(item => (
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

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### I’ve dispatched an action, but logging gives me the old state value[](#ive-dispatched-an-action-but-logging-gives-me-the-old-state-value "Link for I’ve dispatched an action, but logging gives me the old state value ")

Calling the `dispatch` function **does not change state in the running code**:

```
function handleClick() {

  console.log(state.age);  // 42



  dispatch({ type: 'incremented_age' }); // Request a re-render with 43

  console.log(state.age);  // Still 42!



  setTimeout(() => {

    console.log(state.age); // Also 42!

  }, 5000);

}
```

This is because [states behaves like a snapshot.](/learn/state-as-a-snapshot) Updating state requests another render with the new state value, but does not affect the `state` JavaScript variable in your already-running event handler.

If you need to guess the next state value, you can calculate it manually by calling the reducer yourself:

```
const action = { type: 'incremented_age' };

dispatch(action);



const nextState = reducer(state, action);

console.log(state);     // { age: 42 }

console.log(nextState); // { age: 43 }
```

***

### I’ve dispatched an action, but the screen doesn’t update[](#ive-dispatched-an-action-but-the-screen-doesnt-update "Link for I’ve dispatched an action, but the screen doesn’t update ")

React will **ignore your update if the next state is equal to the previous state,** as determined by an [`Object.is`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. This usually happens when you change an object or an array in state directly:

```
function reducer(state, action) {

  switch (action.type) {

    case 'incremented_age': {

      // 🚩 Wrong: mutating existing object

      state.age++;

      return state;

    }

    case 'changed_name': {

      // 🚩 Wrong: mutating existing object

      state.name = action.nextName;

      return state;

    }

    // ...

  }

}
```

You mutated an existing `state` object and returned it, so React ignored the update. To fix this, you need to ensure that you’re always [updating objects in state](/learn/updating-objects-in-state) and [updating arrays in state](/learn/updating-arrays-in-state) instead of mutating them:

```
function reducer(state, action) {

  switch (action.type) {

    case 'incremented_age': {

      // ✅ Correct: creating a new object

      return {

        ...state,

        age: state.age + 1

      };

    }

    case 'changed_name': {

      // ✅ Correct: creating a new object

      return {

        ...state,

        name: action.nextName

      };

    }

    // ...

  }

}
```

***

### A part of my reducer state becomes undefined after dispatching[](#a-part-of-my-reducer-state-becomes-undefined-after-dispatching "Link for A part of my reducer state becomes undefined after dispatching ")

Make sure that every `case` branch **copies all of the existing fields** when returning the new state:

```
function reducer(state, action) {

  switch (action.type) {

    case 'incremented_age': {

      return {

        ...state, // Don't forget this!

        age: state.age + 1

      };

    }

    // ...
```

Without `...state` above, the returned next state would only contain the `age` field and nothing else.

***

### My entire reducer state becomes undefined after dispatching[](#my-entire-reducer-state-becomes-undefined-after-dispatching "Link for My entire reducer state becomes undefined after dispatching ")

If your state unexpectedly becomes `undefined`, you’re likely forgetting to `return` state in one of the cases, or your action type doesn’t match any of the `case` statements. To find why, throw an error outside the `switch`:

```
function reducer(state, action) {

  switch (action.type) {

    case 'incremented_age': {

      // ...

    }

    case 'edited_name': {

      // ...

    }

  }

  throw Error('Unknown action: ' + action.type);

}
```

You can also use a static type checker like TypeScript to catch such mistakes.

***

### I’m getting an error: “Too many re-renders”[](#im-getting-an-error-too-many-re-renders "Link for I’m getting an error: “Too many re-renders” ")

You might get an error that says: `Too many re-renders. React limits the number of renders to prevent an infinite loop.` Typically, this means that you’re unconditionally dispatching an action *during render*, so your component enters a loop: render, dispatch (which causes a render), render, dispatch (which causes a render), and so on. Very often, this is caused by a mistake in specifying an event handler:

```
// 🚩 Wrong: calls the handler during render

return <button onClick={handleClick()}>Click me</button>



// ✅ Correct: passes down the event handler

return <button onClick={handleClick}>Click me</button>



// ✅ Correct: passes down an inline function

return <button onClick={(e) => handleClick(e)}>Click me</button>
```

If you can’t find the cause of this error, click on the arrow next to the error in the console and look through the JavaScript stack to find the specific `dispatch` function call responsible for the error.

***

### My reducer or initializer function runs twice[](#my-reducer-or-initializer-function-runs-twice "Link for My reducer or initializer function runs twice ")

In [Strict Mode](/reference/react/StrictMode), React will call your reducer and initializer functions twice. This shouldn’t break your code.

This **development-only** behavior helps you [keep components pure.](/learn/keeping-components-pure) React uses the result of one of the calls, and ignores the result of the other call. As long as your component, initializer, and reducer functions are pure, this shouldn’t affect your logic. However, if they are accidentally impure, this helps you notice the mistakes.

For example, this impure reducer function mutates an array in state:

```
function reducer(state, action) {

  switch (action.type) {

    case 'added_todo': {

      // 🚩 Mistake: mutating state

      state.todos.push({ id: nextId++, text: action.text });

      return state;

    }

    // ...

  }

}
```

Because React calls your reducer function twice, you’ll see the todo was added twice, so you’ll know that there is a mistake. In this example, you can fix the mistake by [replacing the array instead of mutating it](/learn/updating-arrays-in-state#adding-to-an-array):

```
function reducer(state, action) {

  switch (action.type) {

    case 'added_todo': {

      // ✅ Correct: replacing with new state

      return {

        ...state,

        todos: [

          ...state.todos,

          { id: nextId++, text: action.text }

        ]

      };

    }

    // ...

  }

}
```

Now that this reducer function is pure, calling it an extra time doesn’t make a difference in behavior. This is why React calling it twice helps you find mistakes. **Only component, initializer, and reducer functions need to be pure.** Event handlers don’t need to be pure, so React will never call your event handlers twice.

Read [keeping components pure](/learn/keeping-components-pure) to learn more.

[PrevioususeOptimistic](/reference/react/useOptimistic)

[NextuseRef](/reference/react/useRef)

***

----
