url: https://react.dev/reference/rsc/use-client
----

[API Reference](/reference/react)

[Directives](/reference/rsc/directives)

# 'use client'[](#undefined "Link for this heading")

### React Server Components

`'use client'` is for use with [React Server Components](/reference/rsc/server-components).

***

## Reference[](#reference "Link for Reference ")

### `'use client'`[](#use-client "Link for this heading")

Add `'use client'` at the top of a file to mark the module and its transitive dependencies as client code.

```
'use client';



import { useState } from 'react';

import { formatDate } from './formatters';

import Button from './button';



export default function RichTextEditor({ timestamp, text }) {

  const date = formatDate(timestamp);

  // ...

  const editButton = <Button />;

  // ...

}
```

When a file marked with `'use client'` is imported from a Server Component, [compatible bundlers](/learn/creating-a-react-app#full-stack-frameworks) will treat the module import as a boundary between server-run and client-run code.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import FancyText from './FancyText';
import InspirationGenerator from './InspirationGenerator';
import Copyright from './Copyright';

export default function App() {
  return (
    <>
      <FancyText title text="Get Inspired App" />
      <InspirationGenerator>
        <Copyright year={2004} />
      </InspirationGenerator>
    </>
  );
}
```

```
// This is a definition of a component

function MyComponent() {

  return <p>My Component</p>

}
```

2. A “component” can also refer to a **component usage** of its definition.

```
import MyComponent from './MyComponent';



function App() {

  // This is a usage of a component

  return <MyComponent />;

}
```

* Functions that are [Server Functions](/reference/rsc/server-functions)

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
'use client';

import { useState } from 'react';

export default function Counter({initialValue = 0}) {
  const [countValue, setCountValue] = useState(initialValue);
  const increment = () => setCountValue(countValue + 1);
  const decrement = () => setCountValue(countValue - 1);
  return (
    <>
      <h2>Count Value: {countValue}</h2>
      <button onClick={increment}>+1</button>
      <button onClick={decrement}>-1</button>
    </>
  );
}
```

As `Counter` requires both the `useState` Hook and event handlers to increment or decrement the value, this component must be a Client Component and will require a `'use client'` directive at the top.

In contrast, a component that renders UI without interaction will not need to be a Client Component.

```
import { readFile } from 'node:fs/promises';

import Counter from './Counter';



export default async function CounterContainer() {

  const initialValue = await readFile('/path/to/counter_value');

  return <Counter initialValue={initialValue} />

}
```

For example, `Counter`’s parent component, `CounterContainer`, does not require `'use client'` as it is not interactive and does not use state. In addition, `CounterContainer` must be a Server Component as it reads from the local file system on the server, which is possible only in a Server Component.

There are also components that don’t use any server or client-only features and can be agnostic to where they render. In our earlier example, `FancyText` is one such component.

```
export default function FancyText({title, text}) {

  return title

    ? <h1 className='fancy title'>{text}</h1>

    : <h3 className='fancy cursive'>{text}</h3>

}
```

In this case, we don’t add the `'use client'` directive, resulting in `FancyText`’s *output* (rather than its source code) to be sent to the browser when referenced from a Server Component. As demonstrated in the earlier Inspirations app example, `FancyText` is used as both a Server or Client Component, depending on where it is imported and used.

But if `FancyText`’s HTML output was large relative to its source code (including dependencies), it might be more efficient to force it to always be a Client Component. Components that return a long SVG path string are one case where it may be more efficient to force a component to be a Client Component.

### Using client APIs[](#using-client-apis "Link for Using client APIs ")

Your React app may use client-specific APIs, such as the browser’s APIs for web storage, audio and video manipulation, and device hardware, among [others](https://developer.mozilla.org/en-US/docs/Web/API).

In this example, the component uses [DOM APIs](https://developer.mozilla.org/en-US/docs/Glossary/DOM) to manipulate a [`canvas`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/canvas) element. Since those APIs are only available in the browser, it must be marked as a Client Component.

```
'use client';



import {useRef, useEffect} from 'react';



export default function Circle() {

  const ref = useRef(null);

  useLayoutEffect(() => {

    const canvas = ref.current;

    const context = canvas.getContext('2d');

    context.reset();

    context.beginPath();

    context.arc(100, 75, 50, 0, 2 * Math.PI);

    context.stroke();

  });

  return <canvas ref={ref} />;

}
```

***

----
