url: https://react.dev/reference/react-dom/components/link
----

[API Reference](/reference/react)

[Components](/reference/react-dom/components)

# \<link>[](#undefined "Link for this heading")

The [built-in browser `<link>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link) lets you use external resources such as stylesheets or annotate the document with link metadata.

```
<link rel="icon" href="favicon.ico" />
```

***

## Reference[](#reference "Link for Reference ")

### `<link>`[](#link "Link for this heading")

To link to external resources such as stylesheets, fonts, and icons, or to annotate the document with link metadata, render the [built-in browser `<link>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link). You can render `<link>` from any component and React will [in most cases](#special-rendering-behavior) place the corresponding DOM element in the document head.

```
<link rel="icon" href="favicon.ico" />
```

[See more examples below.](#usage)

#### Props[](#props "Link for Props ")

`<link>` supports all [common element props.](/reference/react-dom/components/common#common-props)

***

## Usage[](#usage "Link for Usage ")

### Linking to related resources[](#linking-to-related-resources "Link for Linking to related resources ")

You can annotate the document with links to related resources such as an icon, canonical URL, or pingback. React will place this metadata within the document `<head>` regardless of where in the React tree it is rendered.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function BlogPage() {
  return (
    <ShowRenderedHTML>
      <link rel="icon" href="favicon.ico" />
      <link rel="pingback" href="http://www.example.com/xmlrpc.php" />
      <h1>My Blog</h1>
      <p>...</p>
    </ShowRenderedHTML>
  );
}
```

### Linking to a stylesheet[](#linking-to-a-stylesheet "Link for Linking to a stylesheet ")

If a component depends on a certain stylesheet in order to be displayed correctly, you can render a link to that stylesheet within the component. Your component will [suspend](/reference/react/Suspense) while the stylesheet is loading. You must supply the `precedence` prop, which tells React where to place this stylesheet relative to others — stylesheets with higher precedence can override those with lower precedence.

### Note

When you want to use a stylesheet, it can be beneficial to call the [preinit](/reference/react-dom/preinit) function. Calling this function may allow the browser to start fetching the stylesheet earlier than if you just render a `<link>` component, for example by sending an [HTTP Early Hints response](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/103).

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function SiteMapPage() {
  return (
    <ShowRenderedHTML>
      <link rel="stylesheet" href="sitemap.css" precedence="medium" />
      <p>...</p>
    </ShowRenderedHTML>
  );
}
```

### Controlling stylesheet precedence[](#controlling-stylesheet-precedence "Link for Controlling stylesheet precedence ")

Stylesheets can conflict with each other, and when they do, the browser goes with the one that comes later in the document. React lets you control the order of stylesheets with the `precedence` prop. In this example, three components render stylesheets, and the ones with the same precedence are grouped together in the `<head>`.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function HomePage() {
  return (
    <ShowRenderedHTML>
      <FirstComponent />
      <SecondComponent />
      <ThirdComponent/>
      ...
    </ShowRenderedHTML>
  );
}

function FirstComponent() {
  return <link rel="stylesheet" href="first.css" precedence="first" />;
}

function SecondComponent() {
  return <link rel="stylesheet" href="second.css" precedence="second" />;
}

function ThirdComponent() {
  return <link rel="stylesheet" href="third.css" precedence="first" />;
}
```

Note the `precedence` values themselves are arbitrary and their naming is up to you. React will infer that precedence values it discovers first are “lower” and precedence values it discovers later are “higher”.

### Deduplicated stylesheet rendering[](#deduplicated-stylesheet-rendering "Link for Deduplicated stylesheet rendering ")

If you render the same stylesheet from multiple components, React will place only a single `<link>` in the document head.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function HomePage() {
  return (
    <ShowRenderedHTML>
      <Component />
      <Component />
      ...
    </ShowRenderedHTML>
  );
}

function Component() {
  return <link rel="stylesheet" href="styles.css" precedence="medium" />;
}
```

### Annotating specific items within the document with links[](#annotating-specific-items-within-the-document-with-links "Link for Annotating specific items within the document with links ")

You can use the `<link>` component with the `itemProp` prop to annotate specific items within the document with links to related resources. In this case, React will *not* place these annotations within the document `<head>` but will place them like any other React component.

```
<section itemScope>

  <h3>Annotating specific items</h3>

  <link itemProp="author" href="http://example.com/" />

  <p>...</p>

</section>
```

[Previous\<textarea>](/reference/react-dom/components/textarea)

[Next\<meta>](/reference/react-dom/components/meta)

***

----
