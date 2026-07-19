url: https://react.dev/reference/react-dom/components
----

[API Reference](/reference/react)

# React DOM Components[](#undefined "Link for this heading")

React supports all of the browser built-in [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML/Element) and [SVG](https://developer.mozilla.org/en-US/docs/Web/SVG/Element) components.

***

## Common components[](#common-components "Link for Common components ")

All of the built-in browser components support some props and events.

* [Common components (e.g. `<div>`)](/reference/react-dom/components/common)

This includes React-specific props like `ref` and `dangerouslySetInnerHTML`.

***

## Form components[](#form-components "Link for Form components ")

These built-in browser components accept user input:

* [`<input>`](/reference/react-dom/components/input)
* [`<select>`](/reference/react-dom/components/select)
* [`<textarea>`](/reference/react-dom/components/textarea)

They are special in React because passing the `value` prop to them makes them *[controlled.](/reference/react-dom/components/input#controlling-an-input-with-a-state-variable)*

***

***

***

### Custom HTML elements[](#custom-html-elements "Link for Custom HTML elements ")

If you render a tag with a dash, like `<my-element>`, React will assume you want to render a [custom HTML element.](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements)

If you render a built-in browser HTML element with an [`is`](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/is) attribute, it will also be treated as a custom element.

#### Setting values on custom elements[](#attributes-vs-properties "Link for Setting values on custom elements ")

Custom elements have two methods of passing data into them:

1. Attributes: Which are displayed in markup and can only be set to string values
2. Properties: Which are not displayed in markup and can be set to arbitrary JavaScript values

By default, React will pass values bound in JSX as attributes:

```
<my-element value="Hello, world!"></my-element>
```

Non-string JavaScript values passed to custom elements will be serialized by default:

```
// Will be passed as `"1,2,3"` as the output of `[1,2,3].toString()`

<my-element value={[1,2,3]}></my-element>
```

React will, however, recognize an custom element’s property as one that it may pass arbitrary values to if the property name shows up on the class during construction:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
export class MyElement extends HTMLElement {
  constructor() {
    super();
    // The value here will be overwritten by React
    // when initialized as an element
    this.value = undefined;
  }

  connectedCallback() {
    this.innerHTML = this.value.join(", ");
  }
}
```

#### Listening for events on custom elements[](#custom-element-events "Link for Listening for events on custom elements ")

A common pattern when using custom elements is that they may dispatch [`CustomEvent`s](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent) rather than accept a function to call when an event occur. You can listen for these events using an `on` prefix when binding to the event via JSX.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
export function App() {
  return (
    <my-element
      onspeak={e => console.log(e.detail.message)}
    ></my-element>
  )
}
```

### Note

Events are case-sensitive and support dashes (`-`). Preserve the casing of the event and include all dashes when listening for custom element’s events:

```
// Listens for `say-hi` events

<my-element onsay-hi={console.log}></my-element>

// Listens for `sayHi` events

<my-element onsayHi={console.log}></my-element>
```

***

***

----
