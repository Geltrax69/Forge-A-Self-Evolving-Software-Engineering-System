url: https://react.dev/reference/react-dom/preloadModule
----

[API Reference](/reference/react)

[APIs](/reference/react-dom)

# preloadModule[](#undefined "Link for this heading")

### Note

[React-based frameworks](/learn/creating-a-react-app) frequently handle resource loading for you, so you might not have to call this API yourself. Consult your framework’s documentation for details.

`preloadModule` lets you eagerly fetch an ESM module that you expect to use.

```
preloadModule("https://example.com/module.js", {as: "script"});
```

* [Reference](#reference)
  * [`preloadModule(href, options)`](#preloadmodule)

* [Usage](#usage)

  * [Preloading when rendering](#preloading-when-rendering)
  * [Preloading in an event handler](#preloading-in-an-event-handler)

***

## Reference[](#reference "Link for Reference ")

### `preloadModule(href, options)`[](#preloadmodule "Link for this heading")

To preload an ESM module, call the `preloadModule` function from `react-dom`.

```
import { preloadModule } from 'react-dom';



function AppRoot() {

  preloadModule("https://example.com/module.js", {as: "script"});

  // ...

}
```

***

## Usage[](#usage "Link for Usage ")

### Preloading when rendering[](#preloading-when-rendering "Link for Preloading when rendering ")

Call `preloadModule` when rendering a component if you know that it or its children will use a specific module.

```
import { preloadModule } from 'react-dom';



function AppRoot() {

  preloadModule("https://example.com/module.js", {as: "script"});

  return ...;

}
```

If you want the browser to start executing the module immediately (rather than just downloading it), use [`preinitModule`](/reference/react-dom/preinitModule) instead. If you want to load a script that isn’t an ESM module, use [`preload`](/reference/react-dom/preload).

### Preloading in an event handler[](#preloading-in-an-event-handler "Link for Preloading in an event handler ")

Call `preloadModule` in an event handler before transitioning to a page or state where the module will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

```
import { preloadModule } from 'react-dom';



function CallToAction() {

  const onClick = () => {

    preloadModule("https://example.com/module.js", {as: "script"});

    startWizard();

  }

  return (

    <button onClick={onClick}>Start Wizard</button>

  );

}
```

[Previouspreload](/reference/react-dom/preload)

[NextClient APIs](/reference/react-dom/client)

***

----
