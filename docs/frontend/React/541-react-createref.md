url: https://18.react.dev/reference/react/createRef
----

[API Reference](/reference/react)

[Legacy React APIs](/reference/react/legacy)

# createRef[](#undefined "Link for this heading")

### Pitfall

`createRef` is mostly used for [class components.](/reference/react/Component) Function components typically rely on [`useRef`](/reference/react/useRef) instead.

`createRef` creates a [ref](/learn/referencing-values-with-refs) object which can contain arbitrary value.

```
class MyInput extends Component {

  inputRef = createRef();

  // ...

}
```

* [Reference](#reference)
  * [`createRef()`](#createref)
* [Usage](#usage)
  * [Declaring a ref in a class component](#declaring-a-ref-in-a-class-component)
* [Alternatives](#alternatives)
  * [Migrating from a class with `createRef` to a function with `useRef`](#migrating-from-a-class-with-createref-to-a-function-with-useref)

***

## Reference[](#reference "Link for Reference ")

### `createRef()`[](#createref "Link for this heading")

Call `createRef` to declare a [ref](/learn/referencing-values-with-refs) inside a [class component.](/reference/react/Component)

```
import { createRef, Component } from 'react';



class MyComponent extends Component {

  intervalRef = createRef();

  inputRef = createRef();

  // ...
```

***

## Usage[](#usage "Link for Usage ")

### Declaring a ref in a class component[](#declaring-a-ref-in-a-class-component "Link for Declaring a ref in a class component ")

To declare a ref inside a [class component,](/reference/react/Component) call `createRef` and assign its result to a class field:

```
import { Component, createRef } from 'react';



class Form extends Component {

  inputRef = createRef();



  // ...

}
```

If you now pass `ref={this.inputRef}` to an `<input>` in your JSX, React will populate `this.inputRef.current` with the input DOM node. For example, here is how you make a button that focuses the input:

```
import { Component, createRef } from 'react';

export default class Form extends Component {
  inputRef = createRef();

  handleClick = () => {
    this.inputRef.current.focus();
  }

  render() {
    return (
      <>
        <input ref={this.inputRef} />
        <button onClick={this.handleClick}>
          Focus the input
        </button>
      </>
    );
  }
}
```

### Pitfall

`createRef` is mostly used for [class components.](/reference/react/Component) Function components typically rely on [`useRef`](/reference/react/useRef) instead.

***

## Alternatives[](#alternatives "Link for Alternatives ")

### Migrating from a class with `createRef` to a function with `useRef`[](#migrating-from-a-class-with-createref-to-a-function-with-useref "Link for this heading")

We recommend using function components instead of [class components](/reference/react/Component) in new code. If you have some existing class components using `createRef`, here is how you can convert them. This is the original code:

```
import { Component, createRef } from 'react';

export default class Form extends Component {
  inputRef = createRef();

  handleClick = () => {
    this.inputRef.current.focus();
  }

  render() {
    return (
      <>
        <input ref={this.inputRef} />
        <button onClick={this.handleClick}>
          Focus the input
        </button>
      </>
    );
  }
}
```

When you [convert this component from a class to a function,](/reference/react/Component#alternatives) replace calls to `createRef` with calls to [`useRef`:](/reference/react/useRef)

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

[PreviouscreateFactory](/reference/react/createFactory)

[NextisValidElement](/reference/react/isValidElement)

***

----
