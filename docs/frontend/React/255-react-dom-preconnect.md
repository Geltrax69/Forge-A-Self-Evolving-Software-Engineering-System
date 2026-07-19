url: https://react.dev/reference/react-dom/preconnect
----

[API Reference](/reference/react)

[APIs](/reference/react-dom)

# preconnect[](#undefined "Link for this heading")

`preconnect` lets you eagerly connect to a server that you expect to load resources from.

```
preconnect("https://example.com");
```

* [Reference](#reference)
  * [`preconnect(href)`](#preconnect)

* [Usage](#usage)

  * [Preconnecting when rendering](#preconnecting-when-rendering)
  * [Preconnecting in an event handler](#preconnecting-in-an-event-handler)

***

## Reference[](#reference "Link for Reference ")

### `preconnect(href)`[](#preconnect "Link for this heading")

To preconnect to a host, call the `preconnect` function from `react-dom`.

```
import { preconnect } from 'react-dom';



function AppRoot() {

  preconnect("https://example.com");

  // ...

}
```

***

## Usage[](#usage "Link for Usage ")

### Preconnecting when rendering[](#preconnecting-when-rendering "Link for Preconnecting when rendering ")

Call `preconnect` when rendering a component if you know that its children will load external resources from that host.

```
import { preconnect } from 'react-dom';



function AppRoot() {

  preconnect("https://example.com");

  return ...;

}
```

### Preconnecting in an event handler[](#preconnecting-in-an-event-handler "Link for Preconnecting in an event handler ")

Call `preconnect` in an event handler before transitioning to a page or state where external resources will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

```
import { preconnect } from 'react-dom';



function CallToAction() {

  const onClick = () => {

    preconnect('http://example.com');

    startWizard();

  }

  return (

    <button onClick={onClick}>Start Wizard</button>

  );

}
```

[PreviousflushSync](/reference/react-dom/flushSync)

[NextprefetchDNS](/reference/react-dom/prefetchDNS)

***

----
