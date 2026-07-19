url: https://react.dev/reference/react-dom/components/meta
----

[API Reference](/reference/react)

[Components](/reference/react-dom/components)

# \<meta>[](#undefined "Link for this heading")

The [built-in browser `<meta>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta) lets you add metadata to the document.

```
<meta name="keywords" content="React, JavaScript, semantic markup, html" />
```

* [Reference](#reference)
  * [`<meta>`](#meta)

* [Usage](#usage)

  * [Annotating the document with metadata](#annotating-the-document-with-metadata)
  * [Annotating specific items within the document with metadata](#annotating-specific-items-within-the-document-with-metadata)

***

## Reference[](#reference "Link for Reference ")

### `<meta>`[](#meta "Link for this heading")

To add document metadata, render the [built-in browser `<meta>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta). You can render `<meta>` from any component and React will always place the corresponding DOM element in the document head.

```
<meta name="keywords" content="React, JavaScript, semantic markup, html" />
```

[See more examples below.](#usage)

#### Props[](#props "Link for Props ")

`<meta>` supports all [common element props.](/reference/react-dom/components/common#common-props)

***

## Usage[](#usage "Link for Usage ")

### Annotating the document with metadata[](#annotating-the-document-with-metadata "Link for Annotating the document with metadata ")

You can annotate the document with metadata such as keywords, a summary, or the author’s name. React will place this metadata within the document `<head>` regardless of where in the React tree it is rendered.

```
<meta name="author" content="John Smith" />

<meta name="keywords" content="React, JavaScript, semantic markup, html" />

<meta name="description" content="API reference for the <meta> component in React DOM" />
```

You can render the `<meta>` component from any component. React will put a `<meta>` DOM node in the document `<head>`.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function SiteMapPage() {
  return (
    <ShowRenderedHTML>
      <meta name="keywords" content="React" />
      <meta name="description" content="A site map for the React website" />
      <h1>Site Map</h1>
      <p>...</p>
    </ShowRenderedHTML>
  );
}
```

### Annotating specific items within the document with metadata[](#annotating-specific-items-within-the-document-with-metadata "Link for Annotating specific items within the document with metadata ")

You can use the `<meta>` component with the `itemProp` prop to annotate specific items within the document with metadata. In this case, React will *not* place these annotations within the document `<head>` but will place them like any other React component.

```
<section itemScope>

  <h3>Annotating specific items</h3>

  <meta itemProp="description" content="API reference for using <meta> with itemProp" />

  <p>...</p>

</section>
```

[Previous\<link>](/reference/react-dom/components/link)

[Next\<script>](/reference/react-dom/components/script)

***

----
