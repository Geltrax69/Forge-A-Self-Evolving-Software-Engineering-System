url: https://18.react.dev/reference/react/createElement
----

[API Reference](/reference/react)

[Legacy React APIs](/reference/react/legacy)

# createElement[](#undefined "Link for this heading")

`createElement` lets you create a React element. It serves as an alternative to writing [JSX.](/learn/writing-markup-with-jsx)

```
const element = createElement(type, props, ...children)
```

* [Reference](#reference)
  * [`createElement(type, props, ...children)`](#createelement)
* [Usage](#usage)
  * [Creating an element without JSX](#creating-an-element-without-jsx)

***

## Reference[](#reference "Link for Reference ")

### `createElement(type, props, ...children)`[](#createelement "Link for this heading")

Call `createElement` to create a React element with the given `type`, `props`, and `children`.

```
import { createElement } from 'react';



function Greeting({ name }) {

  return createElement(

    'h1',

    { className: 'greeting' },

    'Hello'

  );

}
```

* `props`: The `props` you have passed except for `ref` and `key`. If the `type` is a component with legacy `type.defaultProps`, then any missing or undefined `props` will get the values from `type.defaultProps`.

***

## Usage[](#usage "Link for Usage ")

### Creating an element without JSX[](#creating-an-element-without-jsx "Link for Creating an element without JSX ")

If you don’t like [JSX](/learn/writing-markup-with-jsx) or can’t use it in your project, you can use `createElement` as an alternative.

To create an element without JSX, call `createElement` with some type, props, and children:

```
import { createElement } from 'react';



function Greeting({ name }) {

  return createElement(

    'h1',

    { className: 'greeting' },

    'Hello ',

    createElement('i', null, name),

    '. Welcome!'

  );

}
```

The children are optional, and you can pass as many as you need (the example above has three children). This code will display a `<h1>` header with a greeting. For comparison, here is the same example rewritten with JSX:

```
function Greeting({ name }) {

  return (

    <h1 className="greeting">

      Hello <i>{name}</i>. Welcome!

    </h1>

  );

}
```

To render your own React component, pass a function like `Greeting` as the type instead of a string like `'h1'`:

```
export default function App() {

  return createElement(Greeting, { name: 'Taylor' });

}
```

With JSX, it would look like this:

```
export default function App() {

  return <Greeting name="Taylor" />;

}
```

Here is a complete example written with `createElement`:

```
import { createElement } from 'react';

function Greeting({ name }) {
  return createElement(
    'h1',
    { className: 'greeting' },
    'Hello ',
    createElement('i', null, name),
    '. Welcome!'
  );
}

export default function App() {
  return createElement(
    Greeting,
    { name: 'Taylor' }
  );
}
```

And here is the same example written using JSX:

```
function Greeting({ name }) {
  return (
    <h1 className="greeting">
      Hello <i>{name}</i>. Welcome!
    </h1>
  );
}

export default function App() {
  return <Greeting name="Taylor" />;
}
```

Both coding styles are fine, so you can use whichever one you prefer for your project. The main benefit of using JSX compared to `createElement` is that it’s easy to see which closing tag corresponds to which opening tag.

##### Deep Dive#### What is a React element, exactly?[](#what-is-a-react-element-exactly "Link for What is a React element, exactly? ")

An element is a lightweight description of a piece of the user interface. For example, both `<Greeting name="Taylor" />` and `createElement(Greeting, { name: 'Taylor' })` produce an object like this:

```
// Slightly simplified

{

  type: Greeting,

  props: {

    name: 'Taylor'

  },

  key: null,

  ref: null,

}
```

**Note that creating this object does not render the `Greeting` component or create any DOM elements.**

A React element is more like a description—an instruction for React to later render the `Greeting` component. By returning this object from your `App` component, you tell React what to do next.

Creating elements is extremely cheap so you don’t need to try to optimize or avoid it.

[PreviousComponent](/reference/react/Component)

[NextcreateFactory](/reference/react/createFactory)

***

----
