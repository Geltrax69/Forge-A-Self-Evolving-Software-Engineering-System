url: https://react.dev/reference/react/isValidElement
----

[API Reference](/reference/react)

[Legacy React APIs](/reference/react/legacy)

# isValidElement[](#undefined "Link for this heading")

`isValidElement` checks whether a value is a React element.

```
const isElement = isValidElement(value)
```

* [Reference](#reference)
  * [`isValidElement(value)`](#isvalidelement)
* [Usage](#usage)
  * [Checking if something is a React element](#checking-if-something-is-a-react-element)

***

## Reference[](#reference "Link for Reference ")

### `isValidElement(value)`[](#isvalidelement "Link for this heading")

Call `isValidElement(value)` to check whether `value` is a React element.

```
import { isValidElement, createElement } from 'react';



// ✅ React elements

console.log(isValidElement(<p />)); // true

console.log(isValidElement(createElement('p'))); // true



// ❌ Not React elements

console.log(isValidElement(25)); // false

console.log(isValidElement('Hello')); // false

console.log(isValidElement({ age: 42 })); // false
```

***

```
import { isValidElement, createElement } from 'react';



// ✅ JSX tags are React elements

console.log(isValidElement(<p />)); // true

console.log(isValidElement(<MyComponent />)); // true



// ✅ Values returned by createElement are React elements

console.log(isValidElement(createElement('p'))); // true

console.log(isValidElement(createElement(MyComponent))); // true
```

Any other values, such as strings, numbers, or arbitrary objects and arrays, are not React elements.

For them, `isValidElement` returns `false`:

```
// ❌ These are *not* React elements

console.log(isValidElement(null)); // false

console.log(isValidElement(25)); // false

console.log(isValidElement('Hello')); // false

console.log(isValidElement({ age: 42 })); // false

console.log(isValidElement([<div />, <div />])); // false

console.log(isValidElement(MyComponent)); // false
```

It is very uncommon to need `isValidElement`. It’s mostly useful if you’re calling another API that *only* accepts elements (like [`cloneElement`](/reference/react/cloneElement) does) and you want to avoid an error when your argument is not a React element.

Unless you have some very specific reason to add an `isValidElement` check, you probably don’t need it.

##### Deep Dive#### React elements vs React nodes[](#react-elements-vs-react-nodes "Link for React elements vs React nodes ")

When you write a component, you can return any kind of *React node* from it:

```
function MyComponent() {

  // ... you can return any React node ...

}
```

```
function MyComponent() {

  return 42; // It's ok to return a number from component

}
```

This is why you shouldn’t use `isValidElement` as a way to check whether something can be rendered.

[PreviousforwardRef](/reference/react/forwardRef)

[NextPureComponent](/reference/react/PureComponent)

***

----
