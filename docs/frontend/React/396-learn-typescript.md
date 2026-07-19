url: https://react.dev/learn/typescript
----

[Learn React](/learn)

[Setup](/learn/setup)

All [production-grade React frameworks](/learn/creating-a-react-app#full-stack-frameworks) offer support for using TypeScript. Follow the framework specific guide for installation:

```
npm install --save-dev @types/react @types/react-dom
```

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")[TypeScript Playground](https://www.typescriptlang.org/play#src=import%20*%20as%20React%20from%20'react'%3B%0A%0Afunction%20MyButton\(%7B%20title%20%7D%3A%20%7B%20title%3A%20string%20%7D\)%20%7B%0A%20%20return%20\(%0A%20%20%20%20%3Cbutton%3E%7Btitle%7D%3C%2Fbutton%3E%0A%20%20\)%3B%0A%7D%0A%0Aexport%20default%20function%20MyApp\(\)%20%7B%0A%20%20return%20\(%0A%20%20%20%20%3Cdiv%3E%0A%20%20%20%20%20%20%3Ch1%3EWelcome%20to%20my%20app%3C%2Fh1%3E%0A%20%20%20%20%20%20%3CMyButton%20title%3D%22I'm%20a%20button%22%20%2F%3E%0A%20%20%20%20%3C%2Fdiv%3E%0A%20%20\)%3B%0A%7D%0A "Open in TypeScript Playground")

```
function MyButton({ title }: { title: string }) {
  return (
    <button>{title}</button>
  );
}

export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton title="I'm a button" />
    </div>
  );
}
```

### Note

These sandboxes can handle TypeScript code, but they do not run the type-checker. This means you can amend the TypeScript sandboxes to learn, but you won’t get any type errors or warnings. To get type-checking, you can use the [TypeScript Playground](https://www.typescriptlang.org/play) or use a more fully-featured online sandbox.

This inline syntax is the simplest way to provide types for a component, though once you start to have a few fields to describe it can become unwieldy. Instead, you can use an `interface` or `type` to describe the component’s props:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")[TypeScript Playground](https://www.typescriptlang.org/play#src=import%20*%20as%20React%20from%20'react'%3B%0A%0Ainterface%20MyButtonProps%20%7B%0A%20%20%2F**%20The%20text%20to%20display%20inside%20the%20button%20*%2F%0A%20%20title%3A%20string%3B%0A%20%20%2F**%20Whether%20the%20button%20can%20be%20interacted%20with%20*%2F%0A%20%20disabled%3A%20boolean%3B%0A%7D%0A%0Afunction%20MyButton\(%7B%20title%2C%20disabled%20%7D%3A%20MyButtonProps\)%20%7B%0A%20%20return%20\(%0A%20%20%20%20%3Cbutton%20disabled%3D%7Bdisabled%7D%3E%7Btitle%7D%3C%2Fbutton%3E%0A%20%20\)%3B%0A%7D%0A%0Aexport%20default%20function%20MyApp\(\)%20%7B%0A%20%20return%20\(%0A%20%20%20%20%3Cdiv%3E%0A%20%20%20%20%20%20%3Ch1%3EWelcome%20to%20my%20app%3C%2Fh1%3E%0A%20%20%20%20%20%20%3CMyButton%20title%3D%22I'm%20a%20disabled%20button%22%20disabled%3D%7Btrue%7D%2F%3E%0A%20%20%20%20%3C%2Fdiv%3E%0A%20%20\)%3B%0A%7D%0A "Open in TypeScript Playground")

```
interface MyButtonProps {
  /** The text to display inside the button */
  title: string;
  /** Whether the button can be interacted with */
  disabled: boolean;
}

function MyButton({ title, disabled }: MyButtonProps) {
  return (
    <button disabled={disabled}>{title}</button>
  );
}

export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton title="I'm a disabled button" disabled={true}/>
    </div>
  );
}
```

The type describing your component’s props can be as simple or as complex as you need, though they should be an object type described with either a `type` or `interface`. You can learn about how TypeScript describes objects in [Object Types](https://www.typescriptlang.org/docs/handbook/2/objects.html) but you may also be interested in using [Union Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#union-types) to describe a prop that can be one of a few different types and the [Creating Types from Types](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html) guide for more advanced use cases.

## Example Hooks[](#example-hooks "Link for Example Hooks ")

The type definitions from `@types/react` include types for the built-in Hooks, so you can use them in your components without any additional setup. They are built to take into account the code you write in your component, so you will get [inferred types](https://www.typescriptlang.org/docs/handbook/type-inference.html) a lot of the time and ideally do not need to handle the minutiae of providing the types.

However, we can look at a few examples of how to provide types for Hooks.

### `useState`[](#typing-usestate "Link for this heading")

The [`useState` Hook](/reference/react/useState) will re-use the value passed in as the initial state to determine what the type of the value should be. For example:

```
// Infer the type as "boolean"

const [enabled, setEnabled] = useState(false);
```

This will assign the type of `boolean` to `enabled`, and `setEnabled` will be a function accepting either a `boolean` argument, or a function that returns a `boolean`. If you want to explicitly provide a type for the state, you can do so by providing a type argument to the `useState` call:

```
// Explicitly set the type to "boolean"

const [enabled, setEnabled] = useState<boolean>(false);
```

This isn’t very useful in this case, but a common case where you may want to provide a type is when you have a union type. For example, `status` here can be one of a few different strings:

```
type Status = "idle" | "loading" | "success" | "error";



const [status, setStatus] = useState<Status>("idle");
```

Or, as recommended in [Principles for structuring state](/learn/choosing-the-state-structure#principles-for-structuring-state), you can group related state as an object and describe the different possibilities via object types:

```
type RequestState =

  | { status: 'idle' }

  | { status: 'loading' }

  | { status: 'success', data: any }

  | { status: 'error', error: Error };



const [requestState, setRequestState] = useState<RequestState>({ status: 'idle' });
```

### `useReducer`[](#typing-usereducer "Link for this heading")

The [`useReducer` Hook](/reference/react/useReducer) is a more complex Hook that takes a reducer function and an initial state. The types for the reducer function are inferred from the initial state. You can optionally provide a type argument to the `useReducer` call to provide a type for the state, but it is often better to set the type on the initial state instead:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")[TypeScript Playground](https://www.typescriptlang.org/play#src=import%20*%20as%20React%20from%20'react'%3B%0A%0Aimport%20%7BuseReducer%7D%20from%20'react'%3B%0A%0Ainterface%20State%20%7B%0A%20%20%20count%3A%20number%0A%7D%3B%0A%0Atype%20CounterAction%20%3D%0A%20%20%7C%20%7B%20type%3A%20%22reset%22%20%7D%0A%20%20%7C%20%7B%20type%3A%20%22setCount%22%3B%20value%3A%20State%5B%22count%22%5D%20%7D%0A%0Aconst%20initialState%3A%20State%20%3D%20%7B%20count%3A%200%20%7D%3B%0A%0Afunction%20stateReducer\(state%3A%20State%2C%20action%3A%20CounterAction\)%3A%20State%20%7B%0A%20%20switch%20\(action.type\)%20%7B%0A%20%20%20%20case%20%22reset%22%3A%0A%20%20%20%20%20%20return%20initialState%3B%0A%20%20%20%20case%20%22setCount%22%3A%0A%20%20%20%20%20%20return%20%7B%20...state%2C%20count%3A%20action.value%20%7D%3B%0A%20%20%20%20default%3A%0A%20%20%20%20%20%20throw%20new%20Error\(%22Unknown%20action%22\)%3B%0A%20%20%7D%0A%7D%0A%0Aexport%20default%20function%20App\(\)%20%7B%0A%20%20const%20%5Bstate%2C%20dispatch%5D%20%3D%20useReducer\(stateReducer%2C%20initialState\)%3B%0A%0A%20%20const%20addFive%20%3D%20\(\)%20%3D%3E%20dispatch\(%7B%20type%3A%20%22setCount%22%2C%20value%3A%20state.count%20%2B%205%20%7D\)%3B%0A%20%20const%20reset%20%3D%20\(\)%20%3D%3E%20dispatch\(%7B%20type%3A%20%22reset%22%20%7D\)%3B%0A%0A%20%20return%20\(%0A%20%20%20%20%3Cdiv%3E%0A%20%20%20%20%20%20%3Ch1%3EWelcome%20to%20my%20counter%3C%2Fh1%3E%0A%0A%20%20%20%20%20%20%3Cp%3ECount%3A%20%7Bstate.count%7D%3C%2Fp%3E%0A%20%20%20%20%20%20%3Cbutton%20onClick%3D%7BaddFive%7D%3EAdd%205%3C%2Fbutton%3E%0A%20%20%20%20%20%20%3Cbutton%20onClick%3D%7Breset%7D%3EReset%3C%2Fbutton%3E%0A%20%20%20%20%3C%2Fdiv%3E%0A%20%20\)%3B%0A%7D%0A%0A "Open in TypeScript Playground")

```
import {useReducer} from 'react';

interface State {
   count: number
};

type CounterAction =
  | { type: "reset" }
  | { type: "setCount"; value: State["count"] }

const initialState: State = { count: 0 };

function stateReducer(state: State, action: CounterAction): State {
  switch (action.type) {
    case "reset":
      return initialState;
    case "setCount":
      return { ...state, count: action.value };
    default:
      throw new Error("Unknown action");
  }
}

export default function App() {
  const [state, dispatch] = useReducer(stateReducer, initialState);

  const addFive = () => dispatch({ type: "setCount", value: state.count + 5 });
  const reset = () => dispatch({ type: "reset" });

  return (
    <div>
      <h1>Welcome to my counter</h1>

      <p>Count: {state.count}</p>
      <button onClick={addFive}>Add 5</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}
```

We are using TypeScript in a few key places:

* `interface State` describes the shape of the reducer’s state.
* `type CounterAction` describes the different actions which can be dispatched to the reducer.
* `const initialState: State` provides a type for the initial state, and also the type which is used by `useReducer` by default.
* `stateReducer(state: State, action: CounterAction): State` sets the types for the reducer function’s arguments and return value.

A more explicit alternative to setting the type on `initialState` is to provide a type argument to `useReducer`:

```
import { stateReducer, State } from './your-reducer-implementation';



const initialState = { count: 0 };



export default function App() {

  const [state, dispatch] = useReducer<State>(stateReducer, initialState);

}
```

### `useContext`[](#typing-usecontext "Link for this heading")

The [`useContext` Hook](/reference/react/useContext) is a technique for passing data down the component tree without having to pass props through components. It is used by creating a provider component and often by creating a Hook to consume the value in a child component.

The type of the value provided by the context is inferred from the value passed to the `createContext` call:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")[TypeScript Playground](https://www.typescriptlang.org/play#src=import%20*%20as%20React%20from%20'react'%3B%0A%0Aimport%20%7B%20createContext%2C%20useContext%2C%20useState%20%7D%20from%20'react'%3B%0A%0Atype%20Theme%20%3D%20%22light%22%20%7C%20%22dark%22%20%7C%20%22system%22%3B%0Aconst%20ThemeContext%20%3D%20createContext%3CTheme%3E\(%22system%22\)%3B%0A%0Aconst%20useGetTheme%20%3D%20\(\)%20%3D%3E%20useContext\(ThemeContext\)%3B%0A%0Aexport%20default%20function%20MyApp\(\)%20%7B%0A%20%20const%20%5Btheme%2C%20setTheme%5D%20%3D%20useState%3CTheme%3E\('light'\)%3B%0A%0A%20%20return%20\(%0A%20%20%20%20%3CThemeContext%20value%3D%7Btheme%7D%3E%0A%20%20%20%20%20%20%3CMyComponent%20%2F%3E%0A%20%20%20%20%3C%2FThemeContext%3E%0A%20%20\)%0A%7D%0A%0Afunction%20MyComponent\(\)%20%7B%0A%20%20const%20theme%20%3D%20useGetTheme\(\)%3B%0A%0A%20%20return%20\(%0A%20%20%20%20%3Cdiv%3E%0A%20%20%20%20%20%20%3Cp%3ECurrent%20theme%3A%20%7Btheme%7D%3C%2Fp%3E%0A%20%20%20%20%3C%2Fdiv%3E%0A%20%20\)%0A%7D%0A "Open in TypeScript Playground")

```
import { createContext, useContext, useState } from 'react';

type Theme = "light" | "dark" | "system";
const ThemeContext = createContext<Theme>("system");

const useGetTheme = () => useContext(ThemeContext);

export default function MyApp() {
  const [theme, setTheme] = useState<Theme>('light');

  return (
    <ThemeContext value={theme}>
      <MyComponent />
    </ThemeContext>
  )
}

function MyComponent() {
  const theme = useGetTheme();

  return (
    <div>
      <p>Current theme: {theme}</p>
    </div>
  )
}
```

This technique works when you have a default value which makes sense - but there are occasionally cases when you do not, and in those cases `null` can feel reasonable as a default value. However, to allow the type-system to understand your code, you need to explicitly set `ContextShape | null` on the `createContext`.

This causes the issue that you need to eliminate the `| null` in the type for context consumers. Our recommendation is to have the Hook do a runtime check for it’s existence and throw an error when not present:

```
import { createContext, useContext, useState, useMemo } from 'react';



// This is a simpler example, but you can imagine a more complex object here

type ComplexObject = {

  kind: string

};



// The context is created with `| null` in the type, to accurately reflect the default value.

const Context = createContext<ComplexObject | null>(null);



// The `| null` will be removed via the check in the Hook.

const useGetComplexObject = () => {

  const object = useContext(Context);

  if (!object) { throw new Error("useGetComplexObject must be used within a Provider") }

  return object;

}



export default function MyApp() {

  const object = useMemo(() => ({ kind: "complex" }), []);



  return (

    <Context value={object}>

      <MyComponent />

    </Context>

  )

}



function MyComponent() {

  const object = useGetComplexObject();



  return (

    <div>

      <p>Current object: {object.kind}</p>

    </div>

  )

}
```

### `useMemo`[](#typing-usememo "Link for this heading")

### Note

[React Compiler](/learn/react-compiler) automatically memoizes values and functions, reducing the need for manual `useMemo` calls. You can use the compiler to handle memoization automatically.

The [`useMemo`](/reference/react/useMemo) Hooks will create/re-access a memorized value from a function call, re-running the function only when dependencies passed as the 2nd parameter are changed. The result of calling the Hook is inferred from the return value from the function in the first parameter. You can be more explicit by providing a type argument to the Hook.

```
// The type of visibleTodos is inferred from the return value of filterTodos

const visibleTodos = useMemo(() => filterTodos(todos, tab), [todos, tab]);
```

### `useCallback`[](#typing-usecallback "Link for this heading")

### Note

[React Compiler](/learn/react-compiler) automatically memoizes values and functions, reducing the need for manual `useCallback` calls. You can use the compiler to handle memoization automatically.

The [`useCallback`](/reference/react/useCallback) provide a stable reference to a function as long as the dependencies passed into the second parameter are the same. Like `useMemo`, the function’s type is inferred from the return value of the function in the first parameter, and you can be more explicit by providing a type argument to the Hook.

```
const handleClick = useCallback(() => {

  // ...

}, [todos]);
```

When working in TypeScript strict mode `useCallback` requires adding types for the parameters in your callback. This is because the type of the callback is inferred from the return value of the function, and without parameters the type cannot be fully understood.

Depending on your code-style preferences, you could use the `*EventHandler` functions from the React types to provide the type for the event handler at the same time as defining the callback:

```
import { useState, useCallback } from 'react';



export default function Form() {

  const [value, setValue] = useState("Change me");



  const handleChange = useCallback<React.ChangeEventHandler<HTMLInputElement>>((event) => {

    setValue(event.currentTarget.value);

  }, [setValue])



  return (

    <>

      <input value={value} onChange={handleChange} />

      <p>Value: {value}</p>

    </>

  );

}
```

## Useful Types[](#useful-types "Link for Useful Types ")

There is quite an expansive set of types which come from the `@types/react` package, it is worth a read when you feel comfortable with how React and TypeScript interact. You can find them [in React’s folder in DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/react/index.d.ts). We will cover a few of the more common types here.

### DOM Events[](#typing-dom-events "Link for DOM Events ")

When working with DOM events in React, the type of the event can often be inferred from the event handler. However, when you want to extract a function to be passed to an event handler, you will need to explicitly set the type of the event.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")[TypeScript Playground](https://www.typescriptlang.org/play#src=import%20*%20as%20React%20from%20'react'%3B%0A%0Aimport%20%7B%20useState%20%7D%20from%20'react'%3B%0A%0Aexport%20default%20function%20Form\(\)%20%7B%0A%20%20const%20%5Bvalue%2C%20setValue%5D%20%3D%20useState\(%22Change%20me%22\)%3B%0A%0A%20%20function%20handleChange\(event%3A%20React.ChangeEvent%3CHTMLInputElement%3E\)%20%7B%0A%20%20%20%20setValue\(event.currentTarget.value\)%3B%0A%20%20%7D%0A%0A%20%20return%20\(%0A%20%20%20%20%3C%3E%0A%20%20%20%20%20%20%3Cinput%20value%3D%7Bvalue%7D%20onChange%3D%7BhandleChange%7D%20%2F%3E%0A%20%20%20%20%20%20%3Cp%3EValue%3A%20%7Bvalue%7D%3C%2Fp%3E%0A%20%20%20%20%3C%2F%3E%0A%20%20\)%3B%0A%7D%0A "Open in TypeScript Playground")

```
import { useState } from 'react';

export default function Form() {
  const [value, setValue] = useState("Change me");

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    setValue(event.currentTarget.value);
  }

  return (
    <>
      <input value={value} onChange={handleChange} />
      <p>Value: {value}</p>
    </>
  );
}
```

There are many types of events provided in the React types - the full list can be found [here](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/b580df54c0819ec9df62b0835a315dd48b8594a9/types/react/index.d.ts#L1247C1-L1373) which is based on the [most popular events from the DOM](https://developer.mozilla.org/en-US/docs/Web/Events).

When determining the type you are looking for you can first look at the hover information for the event handler you are using, which will show the type of the event.

If you need to use an event that is not included in this list, you can use the `React.SyntheticEvent` type, which is the base type for all events.

### Children[](#typing-children "Link for Children ")

There are two common paths to describing the children of a component. The first is to use the `React.ReactNode` type, which is a union of all the possible types that can be passed as children in JSX:

```
interface ModalRendererProps {

  title: string;

  children: React.ReactNode;

}
```

This is a very broad definition of children. The second is to use the `React.ReactElement` type, which is only JSX elements and not JavaScript primitives like strings or numbers:

```
interface ModalRendererProps {

  title: string;

  children: React.ReactElement;

}
```

Note, that you cannot use TypeScript to describe that the children are a certain type of JSX elements, so you cannot use the type-system to describe a component which only accepts `<li>` children.

You can see an example of both `React.ReactNode` and `React.ReactElement` with the type-checker in [this TypeScript playground](https://www.typescriptlang.org/play?#code/JYWwDg9gTgLgBAJQKYEMDG8BmUIjgIilQ3wChSB6CxYmAOmXRgDkIATJOdNJMGAZzgwAFpxAR+8YADswAVwGkZMJFEzpOjDKw4AFHGEEBvUnDhphwADZsi0gFw0mDWjqQBuUgF9yaCNMlENzgAXjgACjADfkctFnYkfQhDAEpQgD44AB42YAA3dKMo5P46C2tbJGkvLIpcgt9-QLi3AEEwMFCItJDMrPTTbIQ3dKywdIB5aU4kKyQQKpha8drhhIGzLLWODbNs3b3s8YAxKBQAcwXpAThMaGWDvbH0gFloGbmrgQfBzYpd1YjQZbEYARkB6zMwO2SHSAAlZlYIBCdtCRkZpHIrFYahQYQD8UYYFA5EhcfjyGYqHAXnJAsIUHlOOUbHYhMIIHJzsI0Qk4P9SLUBuRqXEXEwAKKfRZcNA8PiCfxWACecAAUgBlAAacFm80W-CU11U6h4TgwUv11yShjgJjMLMqDnN9Dilq+nh8pD8AXgCHdMrCkWisVoAet0R6fXqhWKhjKllZVVxMcavpd4Zg7U6Qaj+2hmdG4zeRF10uu-Aeq0LBfLMEe-V+T2L7zLVu+FBWLdLeq+lc7DYFf39deFVOotMCACNOCh1dq219a+30uC8YWoZsRyuEdjkevR8uvoVMdjyTWt4WiSSydXD4NqZP4AymeZE072ZzuUeZQKheQgA).

### Style Props[](#typing-style-props "Link for Style Props ")

When using inline styles in React, you can use `React.CSSProperties` to describe the object passed to the `style` prop. This type is a union of all the possible CSS properties, and is a good way to ensure you are passing valid CSS properties to the `style` prop, and to get auto-complete in your editor.

```
interface MyComponentProps {

  style: React.CSSProperties;

}
```

***

----
