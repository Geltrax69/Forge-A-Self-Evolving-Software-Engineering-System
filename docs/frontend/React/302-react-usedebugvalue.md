url: https://react.dev/reference/react/useDebugValue
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useDebugValue[](#undefined "Link for this heading")

`useDebugValue` is a React Hook that lets you add a label to a custom Hook in [React DevTools.](/learn/react-developer-tools)

```
useDebugValue(value, format?)
```

* [Reference](#reference)
  * [`useDebugValue(value, format?)`](#usedebugvalue)

* [Usage](#usage)

  * [Adding a label to a custom Hook](#adding-a-label-to-a-custom-hook)
  * [Deferring formatting of a debug value](#deferring-formatting-of-a-debug-value)

***

## Reference[](#reference "Link for Reference ")

### `useDebugValue(value, format?)`[](#usedebugvalue "Link for this heading")

Call `useDebugValue` at the top level of your [custom Hook](/learn/reusing-logic-with-custom-hooks) to display a readable debug value:

```
import { useDebugValue } from 'react';



function useOnlineStatus() {

  // ...

  useDebugValue(isOnline ? 'Online' : 'Offline');

  // ...

}
```

```
import { useDebugValue } from 'react';



function useOnlineStatus() {

  // ...

  useDebugValue(isOnline ? 'Online' : 'Offline');

  // ...

}
```

This gives components calling `useOnlineStatus` a label like `OnlineStatus: "Online"` when you inspect them:

Without the `useDebugValue` call, only the underlying data (in this example, `true`) would be displayed.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useSyncExternalStore, useDebugValue } from 'react';

export function useOnlineStatus() {
  const isOnline = useSyncExternalStore(subscribe, () => navigator.onLine, () => true);
  useDebugValue(isOnline ? 'Online' : 'Offline');
  return isOnline;
}

function subscribe(callback) {
  window.addEventListener('online', callback);
  window.addEventListener('offline', callback);
  return () => {
    window.removeEventListener('online', callback);
    window.removeEventListener('offline', callback);
  };
}
```

### Note

Don’t add debug values to every custom Hook. It’s most valuable for custom Hooks that are part of shared libraries and that have a complex internal data structure that’s difficult to inspect.

***

### Deferring formatting of a debug value[](#deferring-formatting-of-a-debug-value "Link for Deferring formatting of a debug value ")

You can also pass a formatting function as the second argument to `useDebugValue`:

```
useDebugValue(date, date => date.toDateString());
```

Your formatting function will receive the debug value as a parameter and should return a formatted display value. When your component is inspected, React DevTools will call this function and display its result.

This lets you avoid running potentially expensive formatting logic unless the component is actually inspected. For example, if `date` is a Date value, this avoids calling `toDateString()` on it for every render.

[PrevioususeContext](/reference/react/useContext)

[NextuseDeferredValue](/reference/react/useDeferredValue)

***

----
