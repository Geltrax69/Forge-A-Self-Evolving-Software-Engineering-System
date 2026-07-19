url: https://18.react.dev/reference/rsc/server-actions
----

[API Reference](/reference/react)

# Server Actions[](#undefined "Link for this heading")

Server Actions allow Client Components to call async functions executed on the server.

* [Creating a Server Action from a Server Component](#creating-a-server-action-from-a-server-component)
* [Importing Server Actions from Client Components](#importing-server-actions-from-client-components)
* [Composing Server Actions with Actions](#composing-server-actions-with-actions)
* [Form Actions with Server Actions](#form-actions-with-server-actions)
* [Server Actions with `useActionState`](#server-actions-with-use-action-state)
* [Progressive enhancement with `useActionState`](#progressive-enhancement-with-useactionstate)

### Note

#### How do I build support for Server Actions?[](#how-do-i-build-support-for-server-actions "Link for How do I build support for Server Actions? ")

While Server Actions in React 19 are stable and will not break between major versions, the underlying APIs used to implement Server Actions in a React Server Components bundler or framework do not follow semver and may break between minors in React 19.x.

To support Server Actions as a bundler or framework, we recommend pinning to a specific React version, or using the Canary release. We will continue working with bundlers and frameworks to stabilize the APIs used to implement Server Actions in the future.

When a Server Action is defined with the `"use server"` directive, your framework will automatically create a reference to the server function, and pass that reference to the Client Component. When that function is called on the client, React will send a request to the server to execute the function, and return the result.

Server Actions can be created in Server Components and passed as props to Client Components, or they can be imported and used in Client Components.

### Creating a Server Action from a Server Component[](#creating-a-server-action-from-a-server-component "Link for Creating a Server Action from a Server Component ")

Server Components can define Server Actions with the `"use server"` directive:

```
// Server Component

import Button from './Button';



function EmptyNote () {

  async function createNoteAction() {

    // Server Action

    'use server';

    

    await db.notes.create();

  }



  return <Button onClick={createNoteAction}/>;

}
```

When React renders the `EmptyNote` Server Component, it will create a reference to the `createNoteAction` function, and pass that reference to the `Button` Client Component. When the button is clicked, React will send a request to the server to execute the `createNoteAction` function with the reference provided:

```
"use client";



export default function Button({onClick}) { 

  console.log(onClick); 

  // {$$typeof: Symbol.for("react.server.reference"), $$id: 'createNoteAction'}

  return <button onClick={() => onClick()}>Create Empty Note</button>

}
```

For more, see the docs for [`"use server"`](/reference/rsc/use-server).

### Importing Server Actions from Client Components[](#importing-server-actions-from-client-components "Link for Importing Server Actions from Client Components ")

Client Components can import Server Actions from files that use the `"use server"` directive:

```
"use server";



export async function createNoteAction() {

  await db.notes.create();

}
```

When the bundler builds the `EmptyNote` Client Component, it will create a reference to the `createNoteAction` function in the bundle. When the `button` is clicked, React will send a request to the server to execute the `createNoteAction` function using the reference provided:

```
"use client";

import {createNoteAction} from './actions';



function EmptyNote() {

  console.log(createNoteAction);

  // {$$typeof: Symbol.for("react.server.reference"), $$id: 'createNoteAction'}

  return <button onClick={createNoteAction} />

}
```

For more, see the docs for [`"use server"`](/reference/rsc/use-server).

### Composing Server Actions with Actions[](#composing-server-actions-with-actions "Link for Composing Server Actions with Actions ")

Server Actions can be composed with Actions on the client:

```
"use server";



export async function updateName(name) {

  if (!name) {

    return {error: 'Name is required'};

  }

  await db.users.updateName(name);

}
```

```
"use client";



import {updateName} from './actions';



function UpdateName() {

  const [name, setName] = useState('');

  const [error, setError] = useState(null);



  const [isPending, startTransition] = useTransition();



  const submitAction = async () => {

    startTransition(async () => {

      const {error} = await updateName(name);

      if (!error) {

        setError(error);

      } else {

        setName('');

      }

    })

  }

  

  return (

    <form action={submitAction}>

      <input type="text" name="name" disabled={isPending}/>

      {state.error && <span>Failed: {state.error}</span>}

    </form>

  )

}
```

This allows you to access the `isPending` state of the Server Action by wrapping it in an Action on the client.

For more, see the docs for [Calling a Server Action outside of `<form>`](/reference/rsc/use-server#calling-a-server-action-outside-of-form)

### Form Actions with Server Actions[](#form-actions-with-server-actions "Link for Form Actions with Server Actions ")

Server Actions work with the new Form features in React 19.

You can pass a Server Action to a Form to automatically submit the form to the server:

```
"use client";



import {updateName} from './actions';



function UpdateName() {

  return (

    <form action={updateName}>

      <input type="text" name="name" />

    </form>

  )

}
```

When the Form submission succeeds, React will automatically reset the form. You can add `useActionState` to access the pending state, last response, or to support progressive enhancement.

For more, see the docs for [Server Actions in Forms](/reference/rsc/use-server#server-actions-in-forms).

### Server Actions with `useActionState`[](#server-actions-with-use-action-state "Link for this heading")

You can compose Server Actions with `useActionState` for the common case where you just need access to the action pending state and last returned response:

```
"use client";



import {updateName} from './actions';



function UpdateName() {

  const [state, submitAction, isPending] = useActionState(updateName, {error: null});



  return (

    <form action={submitAction}>

      <input type="text" name="name" disabled={isPending}/>

      {state.error && <span>Failed: {state.error}</span>}

    </form>

  );

}
```

When using `useActionState` with Server Actions, React will also automatically replay form submissions entered before hydration finishes. This means users can interact with your app even before the app has hydrated.

For more, see the docs for [`useActionState`](/reference/react-dom/hooks/useFormState).

### Progressive enhancement with `useActionState`[](#progressive-enhancement-with-useactionstate "Link for this heading")

Server Actions also support progressive enhancement with the third argument of `useActionState`.

```
"use client";



import {updateName} from './actions';



function UpdateName() {

  const [, submitAction] = useActionState(updateName, null, `/name/update`);



  return (

    <form action={submitAction}>

      ...

    </form>

  );

}
```

When the permalink is provided to `useActionState`, React will redirect to the provided URL if the form is submitted before the JavaScript bundle loads.

For more, see the docs for [`useActionState`](/reference/react-dom/hooks/useFormState).

[PreviousServer Components](/reference/rsc/server-components)

[NextDirectives](/reference/rsc/directives)

***

----
