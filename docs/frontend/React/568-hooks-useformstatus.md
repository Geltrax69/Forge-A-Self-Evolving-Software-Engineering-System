url: https://18.react.dev/reference/react-dom/hooks/useFormStatus
----

[API Reference](/reference/react)

[Hooks](/reference/react-dom/hooks)

# useFormStatus[](#undefined "Link for this heading")

### Canary

The `useFormStatus` Hook is currently only available in React’s Canary and experimental channels. Learn more about [React’s release channels here](/community/versioning-policy#all-release-channels).

`useFormStatus` is a Hook that gives you status information of the last form submission.

```
const { pending, data, method, action } = useFormStatus();
```

***

## Reference[](#reference "Link for Reference ")

### `useFormStatus()`[](#use-form-status "Link for this heading")

The `useFormStatus` Hook provides status information of the last form submission.

```
import { useFormStatus } from "react-dom";

import action from './actions';



function Submit() {

  const status = useFormStatus();

  return <button disabled={status.pending}>Submit</button>

}



export default function App() {

  return (

    <form action={action}>

      <Submit />

    </form>

  );

}
```

***

## Usage[](#usage "Link for Usage ")

### Display a pending state during form submission[](#display-a-pending-state-during-form-submission "Link for Display a pending state during form submission ")

To display a pending state while a form is submitting, you can call the `useFormStatus` Hook in a component rendered in a `<form>` and read the `pending` property returned.

Here, we use the `pending` property to indicate the form is submitting.

```
import { useFormStatus } from "react-dom";
import { submitForm } from "./actions.js";

function Submit() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? "Submitting..." : "Submit"}
    </button>
  );
}

function Form({ action }) {
  return (
    <form action={action}>
      <Submit />
    </form>
  );
}

export default function App() {
  return <Form action={submitForm} />;
}
```

### Pitfall

##### `useFormStatus` will not return status information for a `<form>` rendered in the same component.[](#useformstatus-will-not-return-status-information-for-a-form-rendered-in-the-same-component "Link for this heading")

The `useFormStatus` Hook only returns status information for a parent `<form>` and not for any `<form>` rendered in the same component calling the Hook, or child components.

```
function Form() {

  // 🚩 `pending` will never be true

  // useFormStatus does not track the form rendered in this component

  const { pending } = useFormStatus();

  return <form action={submit}></form>;

}
```

Instead call `useFormStatus` from inside a component that is located inside `<form>`.

```
function Submit() {

  // ✅ `pending` will be derived from the form that wraps the Submit component

  const { pending } = useFormStatus(); 

  return <button disabled={pending}>...</button>;

}



function Form() {

  // This is the <form> `useFormStatus` tracks

  return (

    <form action={submit}>

      <Submit />

    </form>

  );

}
```

### Read the form data being submitted[](#read-form-data-being-submitted "Link for Read the form data being submitted ")

You can use the `data` property of the status information returned from `useFormStatus` to display what data is being submitted by the user.

Here, we have a form where users can request a username. We can use `useFormStatus` to display a temporary status message confirming what username they have requested.

```
import {useState, useMemo, useRef} from 'react';
import {useFormStatus} from 'react-dom';

export default function UsernameForm() {
  const {pending, data} = useFormStatus();

  return (
    <div>
      <h3>Request a Username: </h3>
      <input type="text" name="username" disabled={pending}/>
      <button type="submit" disabled={pending}>
        Submit
      </button>
      <br />
      <p>{data ? `Requesting ${data?.get("username")}...`: ''}</p>
    </div>
  );
}
```

***

***

----
