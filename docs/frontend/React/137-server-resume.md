url: https://react.dev/reference/react-dom/server/resume
----

[API Reference](/reference/react)

[Server APIs](/reference/react-dom/server)

# resume[](#undefined "Link for this heading")

`resume` streams a pre-rendered React tree to a [Readable Web Stream.](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream)

```
const stream = await resume(reactNode, postponedState, options?)
```

* [Reference](#reference)
  * [`resume(node, postponedState, options?)`](#resume)

* [Usage](#usage)

  * [Resuming a prerender](#resuming-a-prerender)
  * [Further reading](#further-reading)

### Note

This API depends on [Web Streams.](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) For Node.js, use [`resumeToNodeStream`](/reference/react-dom/server/renderToPipeableStream) instead.

***

## Reference[](#reference "Link for Reference ")

### `resume(node, postponedState, options?)`[](#resume "Link for this heading")

Call `resume` to resume rendering a pre-rendered React tree as HTML into a [Readable Web Stream.](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream)

```
import { resume } from 'react-dom/server';

import {getPostponedState} from './storage';



async function handler(request, writable) {

  const postponed = await getPostponedState(request);

  const resumeStream = await resume(<App />, postponed);

  return resumeStream.pipeTo(writable)

}
```


#### Returns[](#returns "Link for Returns ")

`resume` returns a Promise:

* If `resume` successfully produced a [shell](/reference/react-dom/server/renderToReadableStream#specifying-what-goes-into-the-shell), that Promise will resolve to a [Readable Web Stream.](https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream) that can be piped to a [Writable Web Stream.](https://developer.mozilla.org/en-US/docs/Web/API/WritableStream).
* If an error happens in the shell, the Promise will reject with that error.

The returned stream has an additional property:

* `allReady`: A Promise that resolves when all rendering is complete. You can `await stream.allReady` before returning a response [for crawlers and static generation.](/reference/react-dom/server/renderToReadableStream#waiting-for-all-content-to-load-for-crawlers-and-static-generation) If you do that, you won’t get any progressive loading. The stream will contain the final HTML.

#### Caveats[](#caveats "Link for Caveats ")

* `resume` does not accept options for `bootstrapScripts`, `bootstrapScriptContent`, or `bootstrapModules`. Instead, you need to pass these options to the `prerender` call that generates the `postponedState`. You can also inject bootstrap content into the writable stream manually.
* `resume` does not accept `identifierPrefix` since the prefix needs to be the same in both `prerender` and `resume`.
* Since `nonce` cannot be provided to prerender, you should only provide `nonce` to `resume` if you’re not providing scripts to prerender.
* `resume` re-renders from the root until it finds a component that was not fully pre-rendered. Only fully prerendered Components (the Component and its children finished prerendering) are skipped entirely.

## Usage[](#usage "Link for Usage ")

### Resuming a prerender[](#resuming-a-prerender "Link for Resuming a prerender ")

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import {
  flushReadableStreamToFrame,
  getUser,
  Postponed,
  sleep,
} from "./demo-helpers";
import { StrictMode, Suspense, use, useEffect } from "react";
import { prerender } from "react-dom/static";
import { resume } from "react-dom/server";
import { hydrateRoot } from "react-dom/client";

function Header() {
  return <header>Me and my descendants can be prerendered</header>;
}

const { promise: cookies, resolve: resolveCookies } = Promise.withResolvers();

function Main() {
  const { sessionID } = use(cookies);
  const user = getUser(sessionID);

  useEffect(() => {
    console.log("reached interactivity!");
  }, []);

  return (
    <main>
      Hello, {user.name}!
      <button onClick={() => console.log("hydrated!")}>
        Clicking me requires hydration.
      </button>
    </main>
  );
}

function Shell({ children }) {
  // In a real app, this is where you would put your html and body.
  // We're just using tags here we can include in an existing body for demonstration purposes
  return (
    <html>
      <body>{children}</body>
    </html>
  );
}

function App() {
  return (
    <Shell>
      <Suspense fallback="loading header">
        <Header />
      </Suspense>
      <Suspense fallback="loading main">
        <Main />
      </Suspense>
    </Shell>
  );
}

async function main(frame) {
  // Layer 1
  const controller = new AbortController();
  const prerenderedApp = prerender(<App />, {
    signal: controller.signal,
    onError(error) {
      if (error instanceof Postponed) {
      } else {
        console.error(error);
      }
    },
  });
  // We're immediately aborting in a macrotask.
  // Any data fetching that's not available synchronously, or in a microtask, will not have finished.
  setTimeout(() => {
    controller.abort(new Postponed());
  });

  const { prelude, postponed } = await prerenderedApp;
  await flushReadableStreamToFrame(prelude, frame);

  // Layer 2
  // Just waiting here for demonstration purposes.
  // In a real app, the prelude and postponed state would've been serialized in Layer 1 and Layer would deserialize them.
  // The prelude content could be flushed immediated as plain HTML while
  // React is continuing to render from where the prerender left off.
  await sleep(2000);

  // You would get the cookies from the incoming HTTP request
  resolveCookies({ sessionID: "abc" });

  const stream = await resume(<App />, postponed);

  await flushReadableStreamToFrame(stream, frame);

  // Layer 3
  // Just waiting here for demonstration purposes.
  await sleep(2000);

  hydrateRoot(frame.contentWindow.document, <App />);
}

main(document.getElementById("container"));
```

### Further reading[](#further-reading "Link for Further reading ")

Resuming behaves like `renderToReadableStream`. For more examples, check out the [usage section of `renderToReadableStream`](/reference/react-dom/server/renderToReadableStream#usage). The [usage section of `prerender`](/reference/react-dom/static/prerender#usage) includes examples of how to use `prerender` specifically.

[PreviousrenderToString](/reference/react-dom/server/renderToString)

[NextresumeToPipeableStream](/reference/react-dom/server/resumeToPipeableStream)

***

----
