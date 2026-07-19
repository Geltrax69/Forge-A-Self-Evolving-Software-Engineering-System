url: https://18.react.dev/reference/react-dom/findDOMNode
----

[API Reference](/reference/react)

[APIs](/reference/react-dom)

# findDOMNode[](#undefined "Link for this heading")

### Deprecated

This API will be removed in a future major version of React. [See the alternatives.](#alternatives)

`findDOMNode` finds the browser DOM node for a React [class component](/reference/react/Component) instance.

```
const domNode = findDOMNode(componentInstance)
```

***

## Reference[](#reference "Link for Reference ")

### `findDOMNode(componentInstance)`[](#finddomnode "Link for this heading")

Call `findDOMNode` to find the browser DOM node for a given React [class component](/reference/react/Component) instance.

```
import { findDOMNode } from 'react-dom';



const domNode = findDOMNode(componentInstance);
```

***

## Usage[](#usage "Link for Usage ")

### Finding the root DOM node of a class component[](#finding-the-root-dom-node-of-a-class-component "Link for Finding the root DOM node of a class component ")

Call `findDOMNode` with a [class component](/reference/react/Component) instance (usually, `this`) to find the DOM node it has rendered.

```
class AutoselectingInput extends Component {

  componentDidMount() {

    const input = findDOMNode(this);

    input.select()

  }



  render() {

    return <input defaultValue="Hello" />

  }

}
```

Here, the `input` variable will be set to the `<input>` DOM element. This lets you do something with it. For example, when clicking “Show example” below mounts the input, [`input.select()`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/select) selects all text in the input:

```
import { Component } from 'react';
import { findDOMNode } from 'react-dom';

class AutoselectingInput extends Component {
  componentDidMount() {
    const input = findDOMNode(this);
    input.select()
  }

  render() {
    return <input defaultValue="Hello" />
  }
}

export default AutoselectingInput;
```

***

## Alternatives[](#alternatives "Link for Alternatives ")

### Reading component’s own DOM node from a ref[](#reading-components-own-dom-node-from-a-ref "Link for Reading component’s own DOM node from a ref ")

Code using `findDOMNode` is fragile because the connection between the JSX node and the code manipulating the corresponding DOM node is not explicit. For example, try wrapping this `<input />` into a `<div>`:

```
import { Component } from 'react';
import { findDOMNode } from 'react-dom';

class AutoselectingInput extends Component {
  componentDidMount() {
    const input = findDOMNode(this);
    input.select()
  }
  render() {
    return <input defaultValue="Hello" />
  }
}

export default AutoselectingInput;
```

This will break the code because now, `findDOMNode(this)` finds the `<div>` DOM node, but the code expects an `<input>` DOM node. To avoid these kinds of problems, use [`createRef`](/reference/react/createRef) to manage a specific DOM node.

In this example, `findDOMNode` is no longer used. Instead, `inputRef = createRef(null)` is defined as an instance field on the class. To read the DOM node from it, you can use `this.inputRef.current`. To attach it to the JSX, you render `<input ref={this.inputRef} />`. This connects the code using the DOM node to its JSX:

```
import { createRef, Component } from 'react';

class AutoselectingInput extends Component {
  inputRef = createRef(null);

  componentDidMount() {
    const input = this.inputRef.current;
    input.select()
  }

  render() {
    return (
      <input ref={this.inputRef} defaultValue="Hello" />
    );
  }
}

export default AutoselectingInput;
```

In modern React without class components, the equivalent code would call [`useRef`](/reference/react/useRef) instead:

```
import { useRef, useEffect } from 'react';

export default function AutoselectingInput() {
  const inputRef = useRef(null);

  useEffect(() => {
    const input = inputRef.current;
    input.select();
  }, []);

  return <input ref={inputRef} defaultValue="Hello" />
}
```

[Read more about manipulating the DOM with refs.](/learn/manipulating-the-dom-with-refs)

***

### Reading a child component’s DOM node from a forwarded ref[](#reading-a-child-components-dom-node-from-a-forwarded-ref "Link for Reading a child component’s DOM node from a forwarded ref ")

In this example, `findDOMNode(this)` finds a DOM node that belongs to another component. The `AutoselectingInput` renders `MyInput`, which is your own component that renders a browser `<input>`.

```
import { Component } from 'react';
import { findDOMNode } from 'react-dom';
import MyInput from './MyInput.js';

class AutoselectingInput extends Component {
  componentDidMount() {
    const input = findDOMNode(this);
    input.select()
  }
  render() {
    return <MyInput />;
  }
}

export default AutoselectingInput;
```

Notice that calling `findDOMNode(this)` inside `AutoselectingInput` still gives you the DOM `<input>`—even though the JSX for this `<input>` is hidden inside the `MyInput` component. This seems convenient for the above example, but it leads to fragile code. Imagine that you wanted to edit `MyInput` later and add a wrapper `<div>` around it. This would break the code of `AutoselectingInput` (which expects to find an `<input>`).

To replace `findDOMNode` in this example, the two components need to coordinate:

1. `AutoSelectingInput` should declare a ref, like [in the earlier example](#reading-components-own-dom-node-from-a-ref), and pass it to `<MyInput>`.
2. `MyInput` should be declared with [`forwardRef`](/reference/react/forwardRef) to take that ref and forward it down to the `<input>` node.

This version does that, so it no longer needs `findDOMNode`:

```
import { createRef, Component } from 'react';
import MyInput from './MyInput.js';

class AutoselectingInput extends Component {
  inputRef = createRef(null);

  componentDidMount() {
    const input = this.inputRef.current;
    input.select()
  }

  render() {
    return (
      <MyInput ref={this.inputRef} />
    );
  }
}

export default AutoselectingInput;
```

Here is how this code would look like with function components instead of classes:

```
import { useRef, useEffect } from 'react';
import MyInput from './MyInput.js';

export default function AutoselectingInput() {
  const inputRef = useRef(null);

  useEffect(() => {
    const input = inputRef.current;
    input.select();
  }, []);

  return <MyInput ref={inputRef} defaultValue="Hello" />
}
```

***

### Adding a wrapper `<div>` element[](#adding-a-wrapper-div-element "Link for this heading")

Sometimes a component needs to know the position and size of its children. This makes it tempting to find the children with `findDOMNode(this)`, and then use DOM methods like [`getBoundingClientRect`](https://developer.mozilla.org/en-US/docs/Web/API/Element/getBoundingClientRect) for measurements.

There is currently no direct equivalent for this use case, which is why `findDOMNode` is deprecated but is not yet removed completely from React. In the meantime, you can try rendering a wrapper `<div>` node around the content as a workaround, and getting a ref to that node. However, extra wrappers can break styling.

```
<div ref={someRef}>

  {children}

</div>
```

This also applies to focusing and scrolling to arbitrary children.

[PreviousflushSync](/reference/react-dom/flushSync)

[Nexthydrate](/reference/react-dom/hydrate)

***

----
