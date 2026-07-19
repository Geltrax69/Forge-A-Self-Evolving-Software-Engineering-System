url: https://18.react.dev/reference/react-dom/components/script
----

[API Reference](/reference/react)

[Components](/reference/react-dom/components)

# \<script>[](#undefined "Link for this heading")

### Canary

React’s extensions to `<script>` are currently only available in React’s canary and experimental channels. In stable releases of React `<script>` works only as a [built-in browser HTML component](https://react.dev/reference/react-dom/components#all-html-components). Learn more about [React’s release channels here](/community/versioning-policy#all-release-channels).

The [built-in browser `<script>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script) lets you add a script to your document.

```
<script> alert("hi!") </script>
```

* [Reference](#reference)
  * [`<script>`](#script)

* [Usage](#usage)

  * [Rendering an external script](#rendering-an-external-script)
  * [Rendering an inline script](#rendering-an-inline-script)

***

## Reference[](#reference "Link for Reference ")

### `<script>`[](#script "Link for this heading")

To add inline or external scripts to your document, render the [built-in browser `<script>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script). You can render `<script>` from any component and React will [in certain cases](#special-rendering-behavior) place the corresponding DOM element in the document head and de-duplicate identical scripts.

```
<script> alert("hi!") </script>

<script src="script.js" />
```

[See more examples below.](#usage)

#### Props[](#props "Link for Props ")

`<script>` supports all [common element props.](/reference/react-dom/components/common#props)

***

## Usage[](#usage "Link for Usage ")

### Rendering an external script[](#rendering-an-external-script "Link for Rendering an external script ")

If a component depends on certain scripts in order to be displayed correctly, you can render a `<script>` within the component. However, the component might be committed before the script has finished loading. You can start depending on the script content once the `load` event is fired e.g. by using the `onLoad` prop.

React will de-duplicate scripts that have the same `src`, inserting only one of them into the DOM even if multiple components render it.

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

function Map({lat, long}) {
  return (
    <>
      <script async src="map-api.js" onLoad={() => console.log('script loaded')} />
      <div id="map" data-lat={lat} data-long={long} />
    </>
  );
}

export default function Page() {
  return (
    <ShowRenderedHTML>
      <Map />
    </ShowRenderedHTML>
  );
}
```

### Note

When you want to use a script, it can be beneficial to call the [preinit](/reference/react-dom/preinit) function. Calling this function may allow the browser to start fetching the script earlier than if you just render a `<script>` component, for example by sending an [HTTP Early Hints response](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/103).

### Rendering an inline script[](#rendering-an-inline-script "Link for Rendering an inline script ")

To include an inline script, render the `<script>` component with the script source code as its children. Inline scripts are not de-duplicated or moved to the document `<head>`.

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

function Tracking() {
  return (
    <script>
      ga('send', 'pageview');
    </script>
  );
}

export default function Page() {
  return (
    <ShowRenderedHTML>
      <h1>My Website</h1>
      <Tracking />
      <p>Welcome</p>
    </ShowRenderedHTML>
  );
}
```

[Previous\<meta>](/reference/react-dom/components/meta)

[Next\<style>](/reference/react-dom/components/style)

***

----
