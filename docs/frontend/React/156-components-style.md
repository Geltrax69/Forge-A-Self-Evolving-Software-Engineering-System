url: https://react.dev/reference/react-dom/components/style
----

[API Reference](/reference/react)

[Components](/reference/react-dom/components)

# \<style>[](#undefined "Link for this heading")

The [built-in browser `<style>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style) lets you add inline CSS stylesheets to your document.

```
<style>{` p { color: red; } `}</style>
```

* [Reference](#reference)
  * [`<style>`](#style)
* [Usage](#usage)
  * [Rendering an inline CSS stylesheet](#rendering-an-inline-css-stylesheet)

***

## Reference[](#reference "Link for Reference ")

### `<style>`[](#style "Link for this heading")

To add inline styles to your document, render the [built-in browser `<style>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style). You can render `<style>` from any component and React will [in certain cases](#special-rendering-behavior) place the corresponding DOM element in the document head and de-duplicate identical styles.

```
<style>{` p { color: red; } `}</style>
```

[See more examples below.](#usage)

#### Props[](#props "Link for Props ")

`<style>` supports all [common element props.](/reference/react-dom/components/common#common-props)

This special treatment comes with three caveats:

* React will ignore changes to props after the style has been rendered. (React will issue a warning in development if this happens.)
* React will drop all extraneous props when using the `precedence` prop (beyond `href` and `precedence`).
* React may leave the style in the DOM even after the component that rendered it has been unmounted.

***

## Usage[](#usage "Link for Usage ")

### Rendering an inline CSS stylesheet[](#rendering-an-inline-css-stylesheet "Link for Rendering an inline CSS stylesheet ")

If a component depends on certain CSS styles in order to be displayed correctly, you can render an inline stylesheet within the component.

The `href` prop should uniquely identify the stylesheet, because React will de-duplicate stylesheets that have the same `href`. If you supply a `precedence` prop, React will reorder inline stylesheets based on the order these values appear in the component tree.

Inline stylesheets will not trigger Suspense boundaries while they’re loading. Even if they load async resources like fonts or images.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import ShowRenderedHTML from './ShowRenderedHTML.js';
import { useId } from 'react';

function PieChart({data, colors}) {
  const id = useId();
  const stylesheet = colors.map((color, index) =>
    `#${id} .color-${index}: \{ color: "${color}"; \}`
  ).join();
  return (
    <>
      <style href={"PieChart-" + JSON.stringify(colors)} precedence="medium">
        {stylesheet}
      </style>
      <svg id={id}>
        …
      </svg>
    </>
  );
}

export default function App() {
  return (
    <ShowRenderedHTML>
      <PieChart data="..." colors={['red', 'green', 'blue']} />
    </ShowRenderedHTML>
  );
}
```

[Previous\<script>](/reference/react-dom/components/script)

[Next\<title>](/reference/react-dom/components/title)

***

----
