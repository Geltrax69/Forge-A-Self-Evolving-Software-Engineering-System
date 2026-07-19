url: https://18.react.dev/reference/react-dom/components
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

If you render a tag with a dash, like `<my-element>`, React will assume you want to render a [custom HTML element.](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements) In React, rendering custom elements works differently from rendering built-in browser tags:

* All custom element props are serialized to strings and are always set using attributes.
* Custom elements accept `class` rather than `className`, and `for` rather than `htmlFor`.

If you render a built-in browser HTML element with an [`is`](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/is) attribute, it will also be treated as a custom element.

### Note

[A future version of React will include more comprehensive support for custom elements.](https://github.com/facebook/react/issues/11347#issuecomment-1122275286)

You can try it by upgrading React packages to the most recent experimental version:

* `react@experimental`
* `react-dom@experimental`

Experimental versions of React may contain bugs. Don’t use them in production.

***

***

----
