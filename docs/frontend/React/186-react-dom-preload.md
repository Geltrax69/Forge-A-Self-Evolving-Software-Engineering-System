url: https://18.react.dev/reference/react-dom/preload
----

[API Reference](/reference/react)

[APIs](/reference/react-dom)

# preload[](#undefined "Link for this heading")

### Canary

The `preload` function is currently only available in React’s Canary and experimental channels. Learn more about [React’s release channels here](/community/versioning-policy#all-release-channels).

### Note

[React-based frameworks](/learn/start-a-new-react-project) frequently handle resource loading for you, so you might not have to call this API yourself. Consult your framework’s documentation for details.

`preload` lets you eagerly fetch a resource such as a stylesheet, font, or external script that you expect to use.

```
preload("https://example.com/font.woff2", {as: "font"});
```

* [Reference](#reference)
  * [`preload(href, options)`](#preload)

* [Usage](#usage)

  * [Preloading when rendering](#preloading-when-rendering)
  * [Preloading in an event handler](#preloading-in-an-event-handler)

***

## Reference[](#reference "Link for Reference ")

### `preload(href, options)`[](#preload "Link for this heading")

To preload a resource, call the `preload` function from `react-dom`.

```
import { preload } from 'react-dom';



function AppRoot() {

  preload("https://example.com/font.woff2", {as: "font"});

  // ...

}
```

***

## Usage[](#usage "Link for Usage ")

### Preloading when rendering[](#preloading-when-rendering "Link for Preloading when rendering ")

Call `preload` when rendering a component if you know that it or its children will use a specific resource.

#### Examples of preloading[](#examples "Link for Examples of preloading")

#### Example 1 of 4:Preloading an external script[](#preloading-an-external-script "Link for this heading")

```
import { preload } from 'react-dom';



function AppRoot() {

  preload("https://example.com/script.js", {as: "script"});

  return ...;

}
```

If you want the browser to start executing the script immediately (rather than just downloading it), use [`preinit`](/reference/react-dom/preinit) instead. If you want to load an ESM module, use [`preloadModule`](/reference/react-dom/preloadModule).

### Preloading in an event handler[](#preloading-in-an-event-handler "Link for Preloading in an event handler ")

Call `preload` in an event handler before transitioning to a page or state where external resources will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

```
import { preload } from 'react-dom';



function CallToAction() {

  const onClick = () => {

    preload("https://example.com/wizardStyles.css", {as: "style"});

    startWizard();

  }

  return (

    <button onClick={onClick}>Start Wizard</button>

  );

}
```

[PreviouspreinitModule](/reference/react-dom/preinitModule)

[NextpreloadModule](/reference/react-dom/preloadModule)

***

----
