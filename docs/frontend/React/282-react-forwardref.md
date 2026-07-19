url: https://18.react.dev/reference/react/forwardRef
----

[API Reference](/reference/react)

[APIs](/reference/react/apis)

# forwardRef[](#undefined "Link for this heading")

`forwardRef` lets your component expose a DOM node to parent component with a [ref.](/learn/manipulating-the-dom-with-refs)

```
const SomeComponent = forwardRef(render)
```

***

## Reference[](#reference "Link for Reference ")

### `forwardRef(render)`[](#forwardref "Link for this heading")

Call `forwardRef()` to let your component receive a ref and forward it to a child component:

```
import { forwardRef } from 'react';



const MyInput = forwardRef(function MyInput(props, ref) {

  // ...

});
```

***

### `render` function[](#render-function "Link for this heading")

`forwardRef` accepts a render function as an argument. React calls this function with `props` and `ref`:

```
const MyInput = forwardRef(function MyInput(props, ref) {

  return (

    <label>

      {props.label}

      <input ref={ref} />

    </label>

  );

});
```

#### Parameters[](#render-parameters "Link for Parameters ")

* `props`: The props passed by the parent component.

* `ref`: The `ref` attribute passed by the parent component. The `ref` can be an object or a function. If the parent component has not passed a ref, it will be `null`. You should either pass the `ref` you receive to another component, or pass it to [`useImperativeHandle`.](/reference/react/useImperativeHandle)

#### Returns[](#render-returns "Link for Returns ")

`forwardRef` returns a React component that you can render in JSX. Unlike React components defined as plain functions, the component returned by `forwardRef` is able to take a `ref` prop.

***

## Usage[](#usage "Link for Usage ")

### Exposing a DOM node to the parent component[](#exposing-a-dom-node-to-the-parent-component "Link for Exposing a DOM node to the parent component ")

By default, each component’s DOM nodes are private. However, sometimes it’s useful to expose a DOM node to the parent—for example, to allow focusing it. To opt in, wrap your component definition into `forwardRef()`:

```
import { forwardRef } from 'react';



const MyInput = forwardRef(function MyInput(props, ref) {

  const { label, ...otherProps } = props;

  return (

    <label>

      {label}

      <input {...otherProps} />

    </label>

  );

});
```

You will receive a ref as the second argument after props. Pass it to the DOM node that you want to expose:

```
import { forwardRef } from 'react';



const MyInput = forwardRef(function MyInput(props, ref) {

  const { label, ...otherProps } = props;

  return (

    <label>

      {label}

      <input {...otherProps} ref={ref} />

    </label>

  );

});
```

This lets the parent `Form` component access the `<input>` DOM node exposed by `MyInput`:

```
function Form() {

  const ref = useRef(null);



  function handleClick() {

    ref.current.focus();

  }



  return (

    <form>

      <MyInput label="Enter your name:" ref={ref} />

      <button type="button" onClick={handleClick}>

        Edit

      </button>

    </form>

  );

}
```

This `Form` component [passes a ref](/reference/react/useRef#manipulating-the-dom-with-a-ref) to `MyInput`. The `MyInput` component *forwards* that ref to the `<input>` browser tag. As a result, the `Form` component can access that `<input>` DOM node and call [`focus()`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus) on it.

Keep in mind that exposing a ref to the DOM node inside your component makes it harder to change your component’s internals later. You will typically expose DOM nodes from reusable low-level components like buttons or text inputs, but you won’t do it for application-level components like an avatar or a comment.

#### Examples of forwarding a ref[](#examples "Link for Examples of forwarding a ref")

#### Example 1 of 2:Focusing a text input[](#focusing-a-text-input "Link for this heading")

Clicking the button will focus the input. The `Form` component defines a ref and passes it to the `MyInput` component. The `MyInput` component forwards that ref to the browser `<input>`. This lets the `Form` component focus the `<input>`.

```
import { useRef } from 'react';
import MyInput from './MyInput.js';

export default function Form() {
  const ref = useRef(null);

  function handleClick() {
    ref.current.focus();
  }

  return (
    <form>
      <MyInput label="Enter your name:" ref={ref} />
      <button type="button" onClick={handleClick}>
        Edit
      </button>
    </form>
  );
}
```

***

### Forwarding a ref through multiple components[](#forwarding-a-ref-through-multiple-components "Link for Forwarding a ref through multiple components ")

Instead of forwarding a `ref` to a DOM node, you can forward it to your own component like `MyInput`:

```
const FormField = forwardRef(function FormField(props, ref) {

  // ...

  return (

    <>

      <MyInput ref={ref} />

      ...

    </>

  );

});
```

If that `MyInput` component forwards a ref to its `<input>`, a ref to `FormField` will give you that `<input>`:

```
function Form() {

  const ref = useRef(null);



  function handleClick() {

    ref.current.focus();

  }



  return (

    <form>

      <FormField label="Enter your name:" ref={ref} isRequired={true} />

      <button type="button" onClick={handleClick}>

        Edit

      </button>

    </form>

  );

}
```

The `Form` component defines a ref and passes it to `FormField`. The `FormField` component forwards that ref to `MyInput`, which forwards it to a browser `<input>` DOM node. This is how `Form` accesses that DOM node.

```
import { useRef } from 'react';
import FormField from './FormField.js';

export default function Form() {
  const ref = useRef(null);

  function handleClick() {
    ref.current.focus();
  }

  return (
    <form>
      <FormField label="Enter your name:" ref={ref} isRequired={true} />
      <button type="button" onClick={handleClick}>
        Edit
      </button>
    </form>
  );
}
```

***

### Exposing an imperative handle instead of a DOM node[](#exposing-an-imperative-handle-instead-of-a-dom-node "Link for Exposing an imperative handle instead of a DOM node ")

Instead of exposing an entire DOM node, you can expose a custom object, called an *imperative handle,* with a more constrained set of methods. To do this, you’d need to define a separate ref to hold the DOM node:

```
const MyInput = forwardRef(function MyInput(props, ref) {

  const inputRef = useRef(null);



  // ...



  return <input {...props} ref={inputRef} />;

});
```

Pass the `ref` you received to [`useImperativeHandle`](/reference/react/useImperativeHandle) and specify the value you want to expose to the `ref`:

```
import { forwardRef, useRef, useImperativeHandle } from 'react';



const MyInput = forwardRef(function MyInput(props, ref) {

  const inputRef = useRef(null);



  useImperativeHandle(ref, () => {

    return {

      focus() {

        inputRef.current.focus();

      },

      scrollIntoView() {

        inputRef.current.scrollIntoView();

      },

    };

  }, []);



  return <input {...props} ref={inputRef} />;

});
```

If some component gets a ref to `MyInput`, it will only receive your `{ focus, scrollIntoView }` object instead of the DOM node. This lets you limit the information you expose about your DOM node to the minimum.

```
import { useRef } from 'react';
import MyInput from './MyInput.js';

export default function Form() {
  const ref = useRef(null);

  function handleClick() {
    ref.current.focus();
    // This won't work because the DOM node isn't exposed:
    // ref.current.style.opacity = 0.5;
  }

  return (
    <form>
      <MyInput placeholder="Enter your name" ref={ref} />
      <button type="button" onClick={handleClick}>
        Edit
      </button>
    </form>
  );
}
```

[Read more about using imperative handles.](/reference/react/useImperativeHandle)

### Pitfall

**Do not overuse refs.** You should only use refs for *imperative* behaviors that you can’t express as props: for example, scrolling to a node, focusing a node, triggering an animation, selecting text, and so on.

**If you can express something as a prop, you should not use a ref.** For example, instead of exposing an imperative handle like `{ open, close }` from a `Modal` component, it is better to take `isOpen` as a prop like `<Modal isOpen={isOpen} />`. [Effects](/learn/synchronizing-with-effects) can help you expose imperative behaviors via props.

***

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### My component is wrapped in `forwardRef`, but the `ref` to it is always `null`[](#my-component-is-wrapped-in-forwardref-but-the-ref-to-it-is-always-null "Link for this heading")

This usually means that you forgot to actually use the `ref` that you received.

For example, this component doesn’t do anything with its `ref`:

```
const MyInput = forwardRef(function MyInput({ label }, ref) {

  return (

    <label>

      {label}

      <input />

    </label>

  );

});
```

To fix it, pass the `ref` down to a DOM node or another component that can accept a ref:

```
const MyInput = forwardRef(function MyInput({ label }, ref) {

  return (

    <label>

      {label}

      <input ref={ref} />

    </label>

  );

});
```

The `ref` to `MyInput` could also be `null` if some of the logic is conditional:

```
const MyInput = forwardRef(function MyInput({ label, showInput }, ref) {

  return (

    <label>

      {label}

      {showInput && <input ref={ref} />}

    </label>

  );

});
```

If `showInput` is `false`, then the ref won’t be forwarded to any node, and a ref to `MyInput` will remain empty. This is particularly easy to miss if the condition is hidden inside another component, like `Panel` in this example:

```
const MyInput = forwardRef(function MyInput({ label, showInput }, ref) {

  return (

    <label>

      {label}

      <Panel isExpanded={showInput}>

        <input ref={ref} />

      </Panel>

    </label>

  );

});
```

[PreviouscreateContext](/reference/react/createContext)

[Nextlazy](/reference/react/lazy)

***

----
