url: https://18.react.dev/reference/react-dom/preinit
----

[API Reference](/reference/react)

[APIs](/reference/react-dom)

# preinit[](#undefined "Link for this heading")

### Canary

The `preinit` function is currently only available in React’s Canary and experimental channels. Learn more about [React’s release channels here](/community/versioning-policy#all-release-channels).

### Note

[React-based frameworks](/learn/start-a-new-react-project) frequently handle resource loading for you, so you might not have to call this API yourself. Consult your framework’s documentation for details.

`preinit` lets you eagerly fetch and evaluate a stylesheet or external script.

```
preinit("https://example.com/script.js", {as: "script"});
```

* [Reference](#reference)
  * [`preinit(href, options)`](#preinit)

* [Usage](#usage)

  * [Preiniting when rendering](#preiniting-when-rendering)
  * [Preiniting in an event handler](#preiniting-in-an-event-handler)

***

## Reference[](#reference "Link for Reference ")

### `preinit(href, options)`[](#preinit "Link for this heading")

To preinit a script or stylesheet, call the `preinit` function from `react-dom`.

```
import { preinit } from 'react-dom';



function AppRoot() {

  preinit("https://example.com/script.js", {as: "script"});

  // ...

}
```

  * `crossOrigin`: a string. The [CORS policy](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin) to use. Its possible values are `anonymous` and `use-credentials`. It is required when `as` is set to `"fetch"`.

***

## Usage[](#usage "Link for Usage ")

### Preiniting when rendering[](#preiniting-when-rendering "Link for Preiniting when rendering ")

Call `preinit` when rendering a component if you know that it or its children will use a specific resource, and you’re OK with the resource being evaluated and thereby taking effect immediately upon being downloaded.

#### Examples of preiniting[](#examples "Link for Examples of preiniting")

#### Example 1 of 2:Preiniting an external script[](#preiniting-an-external-script "Link for this heading")

```
import { preinit } from 'react-dom';



function AppRoot() {

  preinit("https://example.com/script.js", {as: "script"});

  return ...;

}
```

If you want the browser to download the script but not to execute it right away, use [`preload`](/reference/react-dom/preload) instead. If you want to load an ESM module, use [`preinitModule`](/reference/react-dom/preinitModule).

### Preiniting in an event handler[](#preiniting-in-an-event-handler "Link for Preiniting in an event handler ")

Call `preinit` in an event handler before transitioning to a page or state where external resources will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

```
import { preinit } from 'react-dom';



function CallToAction() {

  const onClick = () => {

    preinit("https://example.com/wizardStyles.css", {as: "style"});

    startWizard();

  }

  return (

    <button onClick={onClick}>Start Wizard</button>

  );

}
```

[PreviousprefetchDNS](/reference/react-dom/prefetchDNS)

[NextpreinitModule](/reference/react-dom/preinitModule)

***

----
