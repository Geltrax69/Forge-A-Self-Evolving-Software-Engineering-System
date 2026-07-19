url: https://18.react.dev/reference/react/useLayoutEffect
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useLayoutEffect[](#undefined "Link for this heading")

### Pitfall

`useLayoutEffect` can hurt performance. Prefer [`useEffect`](/reference/react/useEffect) when possible.

`useLayoutEffect` is a version of [`useEffect`](/reference/react/useEffect) that fires before the browser repaints the screen.

```
useLayoutEffect(setup, dependencies?)
```

* [Reference](#reference)
  * [`useLayoutEffect(setup, dependencies?)`](#useinsertioneffect)
* [Usage](#usage)
  * [Measuring layout before the browser repaints the screen](#measuring-layout-before-the-browser-repaints-the-screen)
* [Troubleshooting](#troubleshooting)
  * [I’m getting an error: “`useLayoutEffect` does nothing on the server”](#im-getting-an-error-uselayouteffect-does-nothing-on-the-server)

***

## Reference[](#reference "Link for Reference ")

### `useLayoutEffect(setup, dependencies?)`[](#useinsertioneffect "Link for this heading")

Call `useLayoutEffect` to perform the layout measurements before the browser repaints the screen:

```
import { useState, useRef, useLayoutEffect } from 'react';



function Tooltip() {

  const ref = useRef(null);

  const [tooltipHeight, setTooltipHeight] = useState(0);



  useLayoutEffect(() => {

    const { height } = ref.current.getBoundingClientRect();

    setTooltipHeight(height);

  }, []);

  // ...
```

[See more examples below.](#usage)

#### Parameters[](#parameters "Link for Parameters ")

* `setup`: The function with your Effect’s logic. Your setup function may also optionally return a *cleanup* function. Before your component is added to the DOM, React will run your setup function. After every re-render with changed dependencies, React will first run the cleanup function (if you provided it) with the old values, and then run your setup function with the new values. Before your component is removed from the DOM, React will run your cleanup function.

* **optional** `dependencies`: The list of all reactive values referenced inside of the `setup` code. Reactive values include props, state, and all the variables and functions declared directly inside your component body. If your linter is [configured for React](/learn/editor-setup#linting), it will verify that every reactive value is correctly specified as a dependency. The list of dependencies must have a constant number of items and be written inline like `[dep1, dep2, dep3]`. React will compare each dependency with its previous value using the [`Object.is`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. If you omit this argument, your Effect will re-run after every re-render of the component.

***

```
function Tooltip() {

  const ref = useRef(null);

  const [tooltipHeight, setTooltipHeight] = useState(0); // You don't know real height yet



  useLayoutEffect(() => {

    const { height } = ref.current.getBoundingClientRect();

    setTooltipHeight(height); // Re-render now that you know the real height

  }, []);



  // ...use tooltipHeight in the rendering logic below...

}
```

```
import { useRef, useLayoutEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import TooltipContainer from './TooltipContainer.js';

export default function Tooltip({ children, targetRect }) {
  const ref = useRef(null);
  const [tooltipHeight, setTooltipHeight] = useState(0);

  useLayoutEffect(() => {
    const { height } = ref.current.getBoundingClientRect();
    setTooltipHeight(height);
    console.log('Measured tooltip height: ' + height);
  }, []);

  let tooltipX = 0;
  let tooltipY = 0;
  if (targetRect !== null) {
    tooltipX = targetRect.left;
    tooltipY = targetRect.top - tooltipHeight;
    if (tooltipY < 0) {
      // It doesn't fit above, so place below.
      tooltipY = targetRect.bottom;
    }
  }

  return createPortal(
    <TooltipContainer x={tooltipX} y={tooltipY} contentRef={ref}>
      {children}
    </TooltipContainer>,
    document.body
  );
}
```

Notice that even though the `Tooltip` component has to render in two passes (first, with `tooltipHeight` initialized to `0` and then with the real measured height), you only see the final result. This is why you need `useLayoutEffect` instead of [`useEffect`](/reference/react/useEffect) for this example. Let’s look at the difference in detail below.

#### useLayoutEffect vs useEffect[](#examples "Link for useLayoutEffect vs useEffect")

#### Example 1 of 2:`useLayoutEffect` blocks the browser from repainting[](#uselayouteffect-blocks-the-browser-from-repainting "Link for this heading")

React guarantees that the code inside `useLayoutEffect` and any state updates scheduled inside it will be processed **before the browser repaints the screen.** This lets you render the tooltip, measure it, and re-render the tooltip again without the user noticing the first extra render. In other words, `useLayoutEffect` blocks the browser from painting.

```
import { useRef, useLayoutEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import TooltipContainer from './TooltipContainer.js';

export default function Tooltip({ children, targetRect }) {
  const ref = useRef(null);
  const [tooltipHeight, setTooltipHeight] = useState(0);

  useLayoutEffect(() => {
    const { height } = ref.current.getBoundingClientRect();
    setTooltipHeight(height);
  }, []);

  let tooltipX = 0;
  let tooltipY = 0;
  if (targetRect !== null) {
    tooltipX = targetRect.left;
    tooltipY = targetRect.top - tooltipHeight;
    if (tooltipY < 0) {
      // It doesn't fit above, so place below.
      tooltipY = targetRect.bottom;
    }
  }

  return createPortal(
    <TooltipContainer x={tooltipX} y={tooltipY} contentRef={ref}>
      {children}
    </TooltipContainer>,
    document.body
  );
}
```

### Note

Rendering in two passes and blocking the browser hurts performance. Try to avoid this when you can.

***

***

----
