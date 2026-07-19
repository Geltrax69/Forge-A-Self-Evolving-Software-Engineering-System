url: https://react.dev/reference/react/useId
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useId[](#undefined "Link for this heading")

`useId` is a React Hook for generating unique IDs that can be passed to accessibility attributes.

```
const id = useId()
```

***

## Reference[](#reference "Link for Reference ")

### `useId()`[](#useid "Link for this heading")

Call `useId` at the top level of your component to generate a unique ID:

```
import { useId } from 'react';



function PasswordField() {

  const passwordHintId = useId();

  // ...
```

* `useId` **should not be used to generate cache keys** for [use()](/reference/react/use). The ID is stable when a component is mounted but may change during rendering. Cache keys should be generated from your data.

* `useId` **should not be used to generate keys** in a list. [Keys should be generated from your data.](/learn/rendering-lists#where-to-get-your-key)

* `useId` currently cannot be used in [async Server Components](/reference/rsc/server-components#async-components-with-server-components).

***

## Usage[](#usage "Link for Usage ")

### Pitfall

**Do not call `useId` to generate keys in a list.** [Keys should be generated from your data.](/learn/rendering-lists#where-to-get-your-key)

### Generating unique IDs for accessibility attributes[](#generating-unique-ids-for-accessibility-attributes "Link for Generating unique IDs for accessibility attributes ")

Call `useId` at the top level of your component to generate a unique ID:

```
import { useId } from 'react';



function PasswordField() {

  const passwordHintId = useId();

  // ...
```

You can then pass the generated ID to different attributes:

```
<>

  <input type="password" aria-describedby={passwordHintId} />

  <p id={passwordHintId}>

</>
```

**Let’s walk through an example to see when this is useful.**

[HTML accessibility attributes](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA) like [`aria-describedby`](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-describedby) let you specify that two tags are related to each other. For example, you can specify that an element (like an input) is described by another element (like a paragraph).

In regular HTML, you would write it like this:

```
<label>

  Password:

  <input

    type="password"

    aria-describedby="password-hint"

  />

</label>

<p id="password-hint">

  The password should contain at least 18 characters

</p>
```

However, hardcoding IDs like this is not a good practice in React. A component may be rendered more than once on the page—but IDs have to be unique! Instead of hardcoding an ID, generate a unique ID with `useId`:

```
import { useId } from 'react';



function PasswordField() {

  const passwordHintId = useId();

  return (

    <>

      <label>

        Password:

        <input

          type="password"

          aria-describedby={passwordHintId}

        />

      </label>

      <p id={passwordHintId}>

        The password should contain at least 18 characters

      </p>

    </>

  );

}
```

Now, even if `PasswordField` appears multiple times on the screen, the generated IDs won’t clash.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useId } from 'react';

function PasswordField() {
  const passwordHintId = useId();
  return (
    <>
      <label>
        Password:
        <input
          type="password"
          aria-describedby={passwordHintId}
        />
      </label>
      <p id={passwordHintId}>
        The password should contain at least 18 characters
      </p>
    </>
  );
}

export default function App() {
  return (
    <>
      <h2>Choose password</h2>
      <PasswordField />
      <h2>Confirm password</h2>
      <PasswordField />
    </>
  );
}
```

***

### Generating IDs for several related elements[](#generating-ids-for-several-related-elements "Link for Generating IDs for several related elements ")

If you need to give IDs to multiple related elements, you can call `useId` to generate a shared prefix for them:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { useId } from 'react';

export default function Form() {
  const id = useId();
  return (
    <form>
      <label htmlFor={id + '-firstName'}>First Name:</label>
      <input id={id + '-firstName'} type="text" />
      <hr />
      <label htmlFor={id + '-lastName'}>Last Name:</label>
      <input id={id + '-lastName'} type="text" />
    </form>
  );
}
```

This lets you avoid calling `useId` for every single element that needs a unique ID.

***

### Specifying a shared prefix for all generated IDs[](#specifying-a-shared-prefix-for-all-generated-ids "Link for Specifying a shared prefix for all generated IDs ")

If you render multiple independent React applications on a single page, pass `identifierPrefix` as an option to your [`createRoot`](/reference/react-dom/client/createRoot#parameters) or [`hydrateRoot`](/reference/react-dom/client/hydrateRoot) calls. This ensures that the IDs generated by the two different apps never clash because every identifier generated with `useId` will start with the distinct prefix you’ve specified.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?undefined\&environment=create-react-app "Open in CodeSandbox")

```
import { createRoot } from 'react-dom/client';
import App from './App.js';
import './styles.css';

const root1 = createRoot(document.getElementById('root1'), {
  identifierPrefix: 'my-first-app-'
});
root1.render(<App />);

const root2 = createRoot(document.getElementById('root2'), {
  identifierPrefix: 'my-second-app-'
});
root2.render(<App />);
```

***

### Using the same ID prefix on the client and the server[](#using-the-same-id-prefix-on-the-client-and-the-server "Link for Using the same ID prefix on the client and the server ")

If you [render multiple independent React apps on the same page](#specifying-a-shared-prefix-for-all-generated-ids), and some of these apps are server-rendered, make sure that the `identifierPrefix` you pass to the [`hydrateRoot`](/reference/react-dom/client/hydrateRoot) call on the client side is the same as the `identifierPrefix` you pass to the [server APIs](/reference/react-dom/server) such as [`renderToPipeableStream`.](/reference/react-dom/server/renderToPipeableStream)

```
// Server

import { renderToPipeableStream } from 'react-dom/server';



const { pipe } = renderToPipeableStream(

  <App />,

  { identifierPrefix: 'react-app1' }

);
```

```
// Client

import { hydrateRoot } from 'react-dom/client';



const domNode = document.getElementById('root');

const root = hydrateRoot(

  domNode,

  reactNode,

  { identifierPrefix: 'react-app1' }

);
```

You do not need to pass `identifierPrefix` if you only have one React app on the page.

[PrevioususeEffectEvent](/reference/react/useEffectEvent)

[NextuseImperativeHandle](/reference/react/useImperativeHandle)

***

----
