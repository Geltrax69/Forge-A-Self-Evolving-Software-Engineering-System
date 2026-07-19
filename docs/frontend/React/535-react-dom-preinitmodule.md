url: https://18.react.dev/reference/react-dom/preinitModule
----

[API Reference](/reference/react)

[APIs](/reference/react-dom)

# preinitModule[](#undefined "Link for this heading")

### Canary

The `preinitModule` function is currently only available in React’s Canary and experimental channels. Learn more about [React’s release channels here](/community/versioning-policy#all-release-channels).

### Note

[React-based frameworks](/learn/start-a-new-react-project) frequently handle resource loading for you, so you might not have to call this API yourself. Consult your framework’s documentation for details.

`preinitModule` lets you eagerly fetch and evaluate an ESM module.

```
preinitModule("https://example.com/module.js", {as: "script"});
```

* [Reference](#reference)
  * [`preinitModule(href, options)`](#preinitmodule)

* [Usage](#usage)

  * [Preloading when rendering](#preloading-when-rendering)
  * [Preloading in an event handler](#preloading-in-an-event-handler)

***

## Reference[](#reference "Link for Reference ")

### `preinitModule(href, options)`[](#preinitmodule "Link for this heading")

To preinit an ESM module, call the `preinitModule` function from `react-dom`.

```
import { preinitModule } from 'react-dom';



function AppRoot() {

  preinitModule("https://example.com/module.js", {as: "script"});

  // ...

}
```

***

## Usage[](#usage "Link for Usage ")

### Preloading when rendering[](#preloading-when-rendering "Link for Preloading when rendering ")

Call `preinitModule` when rendering a component if you know that it or its children will use a specific module and you’re OK with the module being evaluated and thereby taking effect immediately upon being downloaded.

```
import { preinitModule } from 'react-dom';



function AppRoot() {

  preinitModule("https://example.com/module.js", {as: "script"});

  return ...;

}
```

If you want the browser to download the module but not to execute it right away, use [`preloadModule`](/reference/react-dom/preloadModule) instead. If you want to preinit a script that isn’t an ESM module, use [`preinit`](/reference/react-dom/preinit).

### Preloading in an event handler[](#preloading-in-an-event-handler "Link for Preloading in an event handler ")

Call `preinitModule` in an event handler before transitioning to a page or state where the module will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

```
import { preinitModule } from 'react-dom';



function CallToAction() {

  const onClick = () => {

    preinitModule("https://example.com/module.js", {as: "script"});

    startWizard();

  }

  return (

    <button onClick={onClick}>Start Wizard</button>

  );

}
```

[Previouspreinit](/reference/react-dom/preinit)

[Nextpreload](/reference/react-dom/preload)

***

----
