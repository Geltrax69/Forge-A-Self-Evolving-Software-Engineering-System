url: https://18.react.dev/reference/react-dom/client/createRoot
----

[API Reference](/reference/react)

[Client APIs](/reference/react-dom/client)

# createRoot[](#undefined "Link for this heading")

`createRoot` lets you create a root to display React components inside a browser DOM node.

```
const root = createRoot(domNode, options?)
```

  * [Show a dialog for uncaught errors](#show-a-dialog-for-uncaught-errors)
  * [Displaying Error Boundary errors](#displaying-error-boundary-errors)
  * [Displaying a dialog for recoverable errors](#displaying-a-dialog-for-recoverable-errors)

* [Troubleshooting](#troubleshooting)

  * [I’ve created a root, but nothing is displayed](#ive-created-a-root-but-nothing-is-displayed)
  * [I’m getting an error: “You passed a second argument to root.render”](#im-getting-an-error-you-passed-a-second-argument-to-root-render)
  * [I’m getting an error: “Target container is not a DOM element”](#im-getting-an-error-target-container-is-not-a-dom-element)
  * [I’m getting an error: “Functions are not valid as a React child.”](#im-getting-an-error-functions-are-not-valid-as-a-react-child)
  * [My server-rendered HTML gets re-created from scratch](#my-server-rendered-html-gets-re-created-from-scratch)

***

## Reference[](#reference "Link for Reference ")

### `createRoot(domNode, options?)`[](#createroot "Link for this heading")

Call `createRoot` to create a React root for displaying content inside a browser DOM element.

```
import { createRoot } from 'react-dom/client';



const domNode = document.getElementById('root');

const root = createRoot(domNode);
```

React will create a root for the `domNode`, and take over managing the DOM inside it. After you’ve created a root, you need to call [`root.render`](#root-render) to display a React component inside of it:

```
root.render(<App />);
```

An app fully built with React will usually only have one `createRoot` call for its root component. A page that uses “sprinkles” of React for parts of the page may have as many separate roots as needed.

[See more examples below.](#usage)

#### Parameters[](#parameters "Link for Parameters ")

* `domNode`: A [DOM element.](https://developer.mozilla.org/en-US/docs/Web/API/Element) React will create a root for this DOM element and allow you to call functions on the root, such as `render` to display rendered React content.

* **optional** `options`: An object with options for this React root.

  * Canary only **optional** `onCaughtError`: Callback called when React catches an error in an Error Boundary. Called with the `error` caught by the Error Boundary, and an `errorInfo` object containing the `componentStack`.
  * Canary only **optional** `onUncaughtError`: Callback called when an error is thrown and not caught by an Error Boundary. Called with the `error` that was thrown, and an `errorInfo` object containing the `componentStack`.

***

### `root.render(reactNode)`[](#root-render "Link for this heading")

Call `root.render` to display a piece of [JSX](/learn/writing-markup-with-jsx) (“React node”) into the React root’s browser DOM node.

```
root.render(<App />);
```

***

### `root.unmount()`[](#root-unmount "Link for this heading")

Call `root.unmount` to destroy a rendered tree inside a React root.

```
root.unmount();
```

***

## Usage[](#usage "Link for Usage ")

### Rendering an app fully built with React[](#rendering-an-app-fully-built-with-react "Link for Rendering an app fully built with React ")

If your app is fully built with React, create a single root for your entire app.

```
import { createRoot } from 'react-dom/client';



const root = createRoot(document.getElementById('root'));

root.render(<App />);
```

Usually, you only need to run this code once at startup. It will:

1. Find the browser DOM node defined in your HTML.
2. Display the React component for your app inside.

```
import { createRoot } from 'react-dom/client';
import App from './App.js';
import './styles.css';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

**If your app is fully built with React, you shouldn’t need to create any more roots, or to call [`root.render`](#root-render) again.**

From this point on, React will manage the DOM of your entire app. To add more components, [nest them inside the `App` component.](/learn/importing-and-exporting-components) When you need to update the UI, each of your components can do this by [using state.](/reference/react/useState) When you need to display extra content like a modal or a tooltip outside the DOM node, [render it with a portal.](/reference/react-dom/createPortal)

### Note

When your HTML is empty, the user sees a blank page until the app’s JavaScript code loads and runs:

```
<div id="root"></div>
```

This can feel very slow! To solve this, you can generate the initial HTML from your components [on the server or during the build.](/reference/react-dom/server) Then your visitors can read text, see images, and click links before any of the JavaScript code loads. We recommend [using a framework](/learn/start-a-new-react-project#production-grade-react-frameworks) that does this optimization out of the box. Depending on when it runs, this is called *server-side rendering (SSR)* or *static site generation (SSG).*

### Pitfall

**Apps using server rendering or static generation must call [`hydrateRoot`](/reference/react-dom/client/hydrateRoot) instead of `createRoot`.** React will then *hydrate* (reuse) the DOM nodes from your HTML instead of destroying and re-creating them.

***

### Rendering a page partially built with React[](#rendering-a-page-partially-built-with-react "Link for Rendering a page partially built with React ")

If your page [isn’t fully built with React](/learn/add-react-to-an-existing-project#using-react-for-a-part-of-your-existing-page), you can call `createRoot` multiple times to create a root for each top-level piece of UI managed by React. You can display different content in each root by calling [`root.render`.](#root-render)

Here, two different React components are rendered into two DOM nodes defined in the `index.html` file:

```
import './styles.css';
import { createRoot } from 'react-dom/client';
import { Comments, Navigation } from './Components.js';

const navDomNode = document.getElementById('navigation');
const navRoot = createRoot(navDomNode); 
navRoot.render(<Navigation />);

const commentDomNode = document.getElementById('comments');
const commentRoot = createRoot(commentDomNode); 
commentRoot.render(<Comments />);
```

You could also create a new DOM node with [`document.createElement()`](https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement) and add it to the document manually.

```
const domNode = document.createElement('div');

const root = createRoot(domNode); 

root.render(<Comment />);

document.body.appendChild(domNode); // You can add it anywhere in the document
```

To remove the React tree from the DOM node and clean up all the resources used by it, call [`root.unmount`.](#root-unmount)

```
root.unmount();
```

This is mostly useful if your React components are inside an app written in a different framework.

***

### Updating a root component[](#updating-a-root-component "Link for Updating a root component ")

You can call `render` more than once on the same root. As long as the component tree structure matches up with what was previously rendered, React will [preserve the state.](/learn/preserving-and-resetting-state) Notice how you can type in the input, which means that the updates from repeated `render` calls every second in this example are not destructive:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?parameters=N4IgZglgNgpgziAXKOAnAxgeggOwCYwAeAdAFYLIjoD2OALjPUiBALYAO1qdABMD-lQwAhgwBK1arwC-PMKmqseAciHD0dALR5FmdFAiM6ygNwAdHG07cVxTHDoBPWHGLo4cUxatdeAQXZ2OQUlZTsA9jJPcxwLGhwHHgUpHgBeATVxSToACh10AFdWI2IAcxg6AFFYYvoAIUcASTwc1WzlAEoOmItYXgg0ngAGGLgKxvoYVAA3YSgcnI60gD4-Cx4k7OIhfCmcgB4IgWoCydRU4AhZTGXu9Z4IAGpHmOkAGh4ARiGfu5wQN4sOB1XDCVCOJBgOZjd4gdjqADWwnKUVoSFA8QYTEQIGA9zMIBwwmKBMQPAJag0xAI0wJb3xIGmUzgEFopPJICGxC5QzpDNYwlw7IJ9gw2F2JHIfJwGwJcEEEHYdDg7LxMo2HIcYLowpAlK08tQiuVPC13GlGo5ACMCtA8Lr9ZpDca4DwbXaLRqCQwHA6RBonQqla6fbxNJpGNNUuQdKxPbKQDBSDANH71AagyakymdSB7u8GQR2IwCDh0IYVUg1uqE_rdQA9T4ADm53PjHMdsYbzdbvIB91r_ozRuDDYArL2Cfn6eqCTSACIwYu7MsV1XSCzSAFAkFE8GQ6EwWHsApWgxYXAEEgACzorCg6KotCxdGY-wAhPOAPIAYQAKgAmgACpUPC3veywWPs4FQDwUDCDgpSpASjAEpBODQSIeDoRs-zFHQwgCNeYJjHQyEgAAqn-ABimhNmh9x4RUhFEsU5HTIYADu1i5sckz0ORnEQHgdDXqkNIQOgMCaEJInXh8uAQHQEBzIGcwwKknxtiAOE8Psyl0LAyzztQhS1HQ-yYAZRlQZg15Yeh-xWtQeCOLp-x4BA0wPHg5HJLmyyWZ50yOZgzmuaFMHLNuEDAqC-6IFCUAwoCaBYBEUSPpiRjMEQPE8AQUIFFAvBgKcGisjKEQ5MANCnAwqDSEsaobEIdAFKgMo5AOem6Za0GfMsAASMBQFA1AfJxXBQHg758HVZzSJZ16DT1uG4CevDsPBUnXtQM1TORf6OMWpqKBU164KUYFTDABI8DcPWWbpfwbv8gKxbuYIQolh6wml9hOC4bgeFlz45TiABU1YbM5hBOhAABeV1ks5qAEKgmhw68FgWOFjgw3Iz6aFCrDQI4ZJwAhcBOlMEBgDEGwCqgpS4GSABMQzsIQjM8PCeCeYhZIjJuuM4CthPM6zOCaHQ1DsMLvNgMTLKIzAHPs9zOOxOL7OS2C0uy_Liv3Mr9AI2rHNczzos69eADM-ss7gRsK8MSsq0j6tfE2Wu2xY14ACxO4bctuyL6pmwaXtkp8ABsfs4G9AdjiHLthybkee5bXyB4nyfi3Hacyxn7um9n3ufJrNtJ2LNAEITUcW5XxDszArDaxYxWE_zgulJouAGDg0lmnQVv52LMVxXuP1JTCsIMBw8EMMwggiAwmiOsIgQgNIQA\&query=file%3D%252Fsrc%252Findex.js%26utm_medium%3Dsandpack\&environment=create-react-app "Open in CodeSandbox")

```
import { createRoot } from 'react-dom/client';
import './styles.css';
import App from './App.js';

const root = createRoot(document.getElementById('root'));

let i = 0;
setInterval(() => {
  root.render(<App counter={i} />);
  i++;
}, 1000);
```

It is uncommon to call `render` multiple times. Usually, your components will [update state](/reference/react/useState) instead.

### Show a dialog for uncaught errors[](#show-a-dialog-for-uncaught-errors "Link for Show a dialog for uncaught errors ")

### Canary

`onUncaughtError` is only available in the latest React Canary release.

By default, React will log all uncaught errors to the console. To implement your own error reporting, you can provide the optional `onUncaughtError` root option:

```
import { createRoot } from 'react-dom/client';



const root = createRoot(

  document.getElementById('root'),

  {

    onUncaughtError: (error, errorInfo) => {

      console.error(

        'Uncaught error',

        error,

        errorInfo.componentStack

      );

    }

  }

);

root.render(<App />);
```

The onUncaughtError option is a function called with two arguments:

1. The error that was thrown.
2. An errorInfo object that contains the componentStack of the error.

You can use the `onUncaughtError` root option to display error dialogs:

```
import { createRoot } from "react-dom/client";
import App from "./App.js";
import {reportUncaughtError} from "./reportError";
import "./styles.css";

const container = document.getElementById("root");
const root = createRoot(container, {
  onUncaughtError: (error, errorInfo) => {
    if (error.message !== 'Known error') {
      reportUncaughtError({
        error,
        componentStack: errorInfo.componentStack
      });
    }
  }
});
root.render(<App />);
```

### Displaying Error Boundary errors[](#displaying-error-boundary-errors "Link for Displaying Error Boundary errors ")

### Canary

`onCaughtError` is only available in the latest React Canary release.

By default, React will log all errors caught by an Error Boundary to `console.error`. To override this behavior, you can provide the optional `onCaughtError` root option to handle errors caught by an [Error Boundary](/reference/react/Component#catching-rendering-errors-with-an-error-boundary):

```
import { createRoot } from 'react-dom/client';



const root = createRoot(

  document.getElementById('root'),

  {

    onCaughtError: (error, errorInfo) => {

      console.error(

        'Caught error',

        error,

        errorInfo.componentStack

      );

    }

  }

);

root.render(<App />);
```

The onCaughtError option is a function called with two arguments:

1. The error that was caught by the boundary.
2. An errorInfo object that contains the componentStack of the error.

You can use the `onCaughtError` root option to display error dialogs or filter known errors from logging:

```
import { createRoot } from "react-dom/client";
import App from "./App.js";
import {reportCaughtError} from "./reportError";
import "./styles.css";

const container = document.getElementById("root");
const root = createRoot(container, {
  onCaughtError: (error, errorInfo) => {
    if (error.message !== 'Known error') {
      reportCaughtError({
        error, 
        componentStack: errorInfo.componentStack,
      });
    }
  }
});
root.render(<App />);
```

### Displaying a dialog for recoverable errors[](#displaying-a-dialog-for-recoverable-errors "Link for Displaying a dialog for recoverable errors ")

React may automatically render a component a second time to attempt to recover from an error thrown in render. If successful, React will log a recoverable error to the console to notify the developer. To override this behavior, you can provide the optional `onRecoverableError` root option:

```
import { createRoot } from 'react-dom/client';



const root = createRoot(

  document.getElementById('root'),

  {

    onRecoverableError: (error, errorInfo) => {

      console.error(

        'Recoverable error',

        error,

        error.cause,

        errorInfo.componentStack,

      );

    }

  }

);

root.render(<App />);
```

The onRecoverableError option is a function called with two arguments:

1. The error that React throws. Some errors may include the original cause as error.cause.
2. An errorInfo object that contains the componentStack of the error.

You can use the `onRecoverableError` root option to display error dialogs:

```
import { createRoot } from "react-dom/client";
import App from "./App.js";
import {reportRecoverableError} from "./reportError";
import "./styles.css";

const container = document.getElementById("root");
const root = createRoot(container, {
  onRecoverableError: (error, errorInfo) => {
    reportRecoverableError({
      error,
      cause: error.cause,
      componentStack: errorInfo.componentStack,
    });
  }
});
root.render(<App />);
```

***

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### I’ve created a root, but nothing is displayed[](#ive-created-a-root-but-nothing-is-displayed "Link for I’ve created a root, but nothing is displayed ")

Make sure you haven’t forgotten to actually *render* your app into the root:

```
import { createRoot } from 'react-dom/client';

import App from './App.js';



const root = createRoot(document.getElementById('root'));

root.render(<App />);
```

Until you do that, nothing is displayed.

***

### I’m getting an error: “You passed a second argument to root.render”[](#im-getting-an-error-you-passed-a-second-argument-to-root-render "Link for I’m getting an error: “You passed a second argument to root.render” ")

A common mistake is to pass the options for `createRoot` to `root.render(...)`:

Console

Warning: You passed a second argument to root.render(…) but it only accepts one argument.

To fix, pass the root options to `createRoot(...)`, not `root.render(...)`:

```
// 🚩 Wrong: root.render only takes one argument.

root.render(App, {onUncaughtError});



// ✅ Correct: pass options to createRoot.

const root = createRoot(container, {onUncaughtError}); 

root.render(<App />);
```

***

### I’m getting an error: “Target container is not a DOM element”[](#im-getting-an-error-target-container-is-not-a-dom-element "Link for I’m getting an error: “Target container is not a DOM element” ")

This error means that whatever you’re passing to `createRoot` is not a DOM node.

If you’re not sure what’s happening, try logging it:

```
const domNode = document.getElementById('root');

console.log(domNode); // ???

const root = createRoot(domNode);

root.render(<App />);
```

For example, if `domNode` is `null`, it means that [`getElementById`](https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById) returned `null`. This will happen if there is no node in the document with the given ID at the time of your call. There may be a few reasons for it:

1. The ID you’re looking for might differ from the ID you used in the HTML file. Check for typos!
2. Your bundle’s `<script>` tag cannot “see” any DOM nodes that appear *after* it in the HTML.

Another common way to get this error is to write `createRoot(<App />)` instead of `createRoot(domNode)`.

***

### I’m getting an error: “Functions are not valid as a React child.”[](#im-getting-an-error-functions-are-not-valid-as-a-react-child "Link for I’m getting an error: “Functions are not valid as a React child.” ")

This error means that whatever you’re passing to `root.render` is not a React component.

This may happen if you call `root.render` with `Component` instead of `<Component />`:

```
// 🚩 Wrong: App is a function, not a Component.

root.render(App);



// ✅ Correct: <App /> is a component.

root.render(<App />);
```

Or if you pass a function to `root.render`, instead of the result of calling it:

```
// 🚩 Wrong: createApp is a function, not a component.

root.render(createApp);



// ✅ Correct: call createApp to return a component.

root.render(createApp());
```

***

### My server-rendered HTML gets re-created from scratch[](#my-server-rendered-html-gets-re-created-from-scratch "Link for My server-rendered HTML gets re-created from scratch ")

If your app is server-rendered and includes the initial HTML generated by React, you might notice that creating a root and calling `root.render` deletes all that HTML, and then re-creates all the DOM nodes from scratch. This can be slower, resets focus and scroll positions, and may lose other user input.

Server-rendered apps must use [`hydrateRoot`](/reference/react-dom/client/hydrateRoot) instead of `createRoot`:

```
import { hydrateRoot } from 'react-dom/client';

import App from './App.js';



hydrateRoot(

  document.getElementById('root'),

  <App />

);
```

Note that its API is different. In particular, usually there will be no further `root.render` call.

[PreviousClient APIs](/reference/react-dom/client)

[NexthydrateRoot](/reference/react-dom/client/hydrateRoot)

***

----
