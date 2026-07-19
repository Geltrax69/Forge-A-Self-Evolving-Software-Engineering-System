url: https://react.dev/reference/react-dom/server/renderToStaticMarkup
----

[API Reference](/reference/react)

[Server APIs](/reference/react-dom/server)

# renderToStaticMarkup[](#undefined "Link for this heading")

`renderToStaticMarkup` renders a non-interactive React tree to an HTML string.

```
const html = renderToStaticMarkup(reactNode, options?)
```

* [Reference](#reference)
  * [`renderToStaticMarkup(reactNode, options?)`](#rendertostaticmarkup)
* [Usage](#usage)
  * [Rendering a non-interactive React tree as HTML to a string](#rendering-a-non-interactive-react-tree-as-html-to-a-string)

***

## Reference[](#reference "Link for Reference ")

### `renderToStaticMarkup(reactNode, options?)`[](#rendertostaticmarkup "Link for this heading")

On the server, call `renderToStaticMarkup` to render your app to HTML.

```
import { renderToStaticMarkup } from 'react-dom/server';



const html = renderToStaticMarkup(<Page />);
```

***

## Usage[](#usage "Link for Usage ")

### Rendering a non-interactive React tree as HTML to a string[](#rendering-a-non-interactive-react-tree-as-html-to-a-string "Link for Rendering a non-interactive React tree as HTML to a string ")

Call `renderToStaticMarkup` to render your app to an HTML string which you can send with your server response:

```
import { renderToStaticMarkup } from 'react-dom/server';



// The route handler syntax depends on your backend framework

app.use('/', (request, response) => {

  const html = renderToStaticMarkup(<Page />);

  response.send(html);

});
```

This will produce the initial non-interactive HTML output of your React components.

### Pitfall

This method renders **non-interactive HTML that cannot be hydrated.** This is useful if you want to use React as a simple static page generator, or if you’re rendering completely static content like emails.

Interactive apps should use [`renderToString`](/reference/react-dom/server/renderToString) on the server and [`hydrateRoot`](/reference/react-dom/client/hydrateRoot) on the client.

[PreviousrenderToReadableStream](/reference/react-dom/server/renderToReadableStream)

[NextrenderToString](/reference/react-dom/server/renderToString)

***

----
