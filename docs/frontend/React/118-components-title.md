url: https://18.react.dev/reference/react-dom/components/title
----

[API Reference](/reference/react)

[Components](/reference/react-dom/components)

# \<title>[](#undefined "Link for this heading")

### Canary

React’s extensions to `<title>` are currently only available in React’s canary and experimental channels. In stable releases of React `<title>` works only as a [built-in browser HTML component](https://react.dev/reference/react-dom/components#all-html-components). Learn more about [React’s release channels here](/community/versioning-policy#all-release-channels).

The [built-in browser `<title>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title) lets you specify the title of the document.

```
<title>My Blog</title>
```

* [Reference](#reference)
  * [`<title>`](#title)

* [Usage](#usage)

  * [Set the document title](#set-the-document-title)
  * [Use variables in the title](#use-variables-in-the-title)

***

## Reference[](#reference "Link for Reference ")

### `<title>`[](#title "Link for this heading")

To specify the title of the document, render the [built-in browser `<title>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title). You can render `<title>` from any component and React will always place the corresponding DOM element in the document head.

```
<title>My Blog</title>
```

[See more examples below.](#usage)

#### Props[](#props "Link for Props ")

`<title>` supports all [common element props.](/reference/react-dom/components/common#props)

***

## Usage[](#usage "Link for Usage ")

### Set the document title[](#set-the-document-title "Link for Set the document title ")

Render the `<title>` component from any component with text as its children. React will put a `<title>` DOM node in the document `<head>`.

```
import ShowRenderedHTML from './ShowRenderedHTML.js';

export default function ContactUsPage() {
  return (
    <ShowRenderedHTML>
      <title>My Site: Contact Us</title>
      <h1>Contact Us</h1>
      <p>Email us at support@example.com</p>
    </ShowRenderedHTML>
  );
}
```

### Use variables in the title[](#use-variables-in-the-title "Link for Use variables in the title ")

The children of the `<title>` component must be a single string of text. (Or a single number or a single object with a `toString` method.) It might not be obvious, but using JSX curly braces like this:

```
<title>Results page {pageNumber}</title> // 🔴 Problem: This is not a single string
```

… actually causes the `<title>` component to get a two-element array as its children (the string `"Results page"` and the value of `pageNumber`). This will cause an error. Instead, use string interpolation to pass `<title>` a single string:

```
<title>{`Results page ${pageNumber}`}</title>
```

[Previous\<style>](/reference/react-dom/components/style)

[NextAPIs](/reference/react-dom)

***

----
