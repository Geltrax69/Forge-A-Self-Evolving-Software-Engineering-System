url: https://18.react.dev/reference/react-dom/flushSync
----

[API Reference](/reference/react)

[APIs](/reference/react-dom)

# flushSync[](#undefined "Link for this heading")

### Pitfall

Using `flushSync` is uncommon and can hurt the performance of your app.

`flushSync` lets you force React to flush any updates inside the provided callback synchronously. This ensures that the DOM is updated immediately.

```
flushSync(callback)
```

* [Reference](#reference)
  * [`flushSync(callback)`](#flushsync)
* [Usage](#usage)
  * [Flushing updates for third-party integrations](#flushing-updates-for-third-party-integrations)

***

## Reference[](#reference "Link for Reference ")

### `flushSync(callback)`[](#flushsync "Link for this heading")

Call `flushSync` to force React to flush any pending work and update the DOM synchronously.

```
import { flushSync } from 'react-dom';



flushSync(() => {

  setSomething(123);

});
```

***

## Usage[](#usage "Link for Usage ")

### Flushing updates for third-party integrations[](#flushing-updates-for-third-party-integrations "Link for Flushing updates for third-party integrations ")

When integrating with third-party code such as browser APIs or UI libraries, it may be necessary to force React to flush updates. Use `flushSync` to force React to flush any state updates inside the callback synchronously:

```
flushSync(() => {

  setSomething(123);

});

// By this line, the DOM is updated.
```

This ensures that, by the time the next line of code runs, React has already updated the DOM.

**Using `flushSync` is uncommon, and using it often can significantly hurt the performance of your app.** If your app only uses React APIs, and does not integrate with third-party libraries, `flushSync` should be unnecessary.

However, it can be helpful for integrating with third-party code like browser APIs.

Some browser APIs expect results inside of callbacks to be written to the DOM synchronously, by the end of the callback, so the browser can do something with the rendered DOM. In most cases, React handles this for you automatically. But in some cases it may be necessary to force a synchronous update.

For example, the browser `onbeforeprint` API allows you to change the page immediately before the print dialog opens. This is useful for applying custom print styles that allow the document to display better for printing. In the example below, you use `flushSync` inside of the `onbeforeprint` callback to immediately “flush” the React state to the DOM. Then, by the time the print dialog opens, `isPrinting` displays “yes”:

```
import { useState, useEffect } from 'react';
import { flushSync } from 'react-dom';

export default function PrintApp() {
  const [isPrinting, setIsPrinting] = useState(false);

  useEffect(() => {
    function handleBeforePrint() {
      flushSync(() => {
        setIsPrinting(true);
      })
    }

    function handleAfterPrint() {
      setIsPrinting(false);
    }

    window.addEventListener('beforeprint', handleBeforePrint);
    window.addEventListener('afterprint', handleAfterPrint);
    return () => {
      window.removeEventListener('beforeprint', handleBeforePrint);
      window.removeEventListener('afterprint', handleAfterPrint);
    }
  }, []);

  return (
    <>
      <h1>isPrinting: {isPrinting ? 'yes' : 'no'}</h1>
      <button onClick={() => window.print()}>
        Print
      </button>
    </>
  );
}
```

Without `flushSync`, the print dialog will display `isPrinting` as “no”. This is because React batches the updates asynchronously and the print dialog is displayed before the state is updated.

### Pitfall

`flushSync` can significantly hurt performance, and may unexpectedly force pending Suspense boundaries to show their fallback state.

Most of the time, `flushSync` can be avoided, so use `flushSync` as a last resort.

[PreviouscreatePortal](/reference/react-dom/createPortal)

[NextfindDOMNode](/reference/react-dom/findDOMNode)

***

----
