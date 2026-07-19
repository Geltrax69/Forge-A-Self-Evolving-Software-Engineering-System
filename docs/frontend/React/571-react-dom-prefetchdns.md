url: https://react.dev/reference/react-dom/prefetchDNS
----

[API Reference](/reference/react)

[APIs](/reference/react-dom)

# prefetchDNS[](#undefined "Link for this heading")

`prefetchDNS` lets you eagerly look up the IP of a server that you expect to load resources from.

```
prefetchDNS("https://example.com");
```

* [Reference](#reference)
  * [`prefetchDNS(href)`](#prefetchdns)

* [Usage](#usage)

  * [Prefetching DNS when rendering](#prefetching-dns-when-rendering)
  * [Prefetching DNS in an event handler](#prefetching-dns-in-an-event-handler)

***

## Reference[](#reference "Link for Reference ")

### `prefetchDNS(href)`[](#prefetchdns "Link for this heading")

To look up a host, call the `prefetchDNS` function from `react-dom`.

```
import { prefetchDNS } from 'react-dom';



function AppRoot() {

  prefetchDNS("https://example.com");

  // ...

}
```

***

## Usage[](#usage "Link for Usage ")

### Prefetching DNS when rendering[](#prefetching-dns-when-rendering "Link for Prefetching DNS when rendering ")

Call `prefetchDNS` when rendering a component if you know that its children will load external resources from that host.

```
import { prefetchDNS } from 'react-dom';



function AppRoot() {

  prefetchDNS("https://example.com");

  return ...;

}
```

### Prefetching DNS in an event handler[](#prefetching-dns-in-an-event-handler "Link for Prefetching DNS in an event handler ")

Call `prefetchDNS` in an event handler before transitioning to a page or state where external resources will be needed. This gets the process started earlier than if you call it during the rendering of the new page or state.

```
import { prefetchDNS } from 'react-dom';



function CallToAction() {

  const onClick = () => {

    prefetchDNS('http://example.com');

    startWizard();

  }

  return (

    <button onClick={onClick}>Start Wizard</button>

  );

}
```

[Previouspreconnect](/reference/react-dom/preconnect)

[Nextpreinit](/reference/react-dom/preinit)

***

----
