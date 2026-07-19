url: https://legacy.reactjs.org/tips/controlled-input-null-value.html
----

[API Reference](/reference/react)

[Components](/reference/react-dom/components)

# \<input>[](#undefined "Link for this heading")

The [built-in browser `<input>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input) lets you render different kinds of form inputs.

```
<input />
```

***

## Reference[](#reference "Link for Reference ")

### `<input>`[](#input "Link for this heading")

To display an input, render the [built-in browser `<input>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input) component.

```
<input name="myInput" />
```

***

## Usage[](#usage "Link for Usage ")

### Displaying inputs of different types[](#displaying-inputs-of-different-types "Link for Displaying inputs of different types ")

To display an input, render an `<input>` component. By default, it will be a text input. You can pass `type="checkbox"` for a checkbox, `type="radio"` for a radio button, [or one of the other input types.](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#input_types)

```
export default function MyForm() {
  return (
    <>
      <label>
        Text input: <input name="myInput" />
      </label>
      <hr />
      <label>
        Checkbox: <input type="checkbox" name="myCheckbox" />
      </label>
      <hr />
      <p>
        Radio buttons:
        <label>
          <input type="radio" name="myRadio" value="option1" />
          Option 1
        </label>
        <label>
          <input type="radio" name="myRadio" value="option2" />
          Option 2
        </label>
        <label>
          <input type="radio" name="myRadio" value="option3" />
          Option 3
        </label>
      </p>
    </>
  );
}
```

***

### Providing a label for an input[](#providing-a-label-for-an-input "Link for Providing a label for an input ")

Typically, you will place every `<input>` inside a [`<label>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label) tag. This tells the browser that this label is associated with that input. When the user clicks the label, the browser will automatically focus the input. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the associated input.

If you can’t nest `<input>` into a `<label>`, associate them by passing the same ID to `<input id>` and [`<label htmlFor>`.](https://developer.mozilla.org/en-US/docs/Web/API/HTMLLabelElement/htmlFor) To avoid conflicts between multiple instances of one component, generate such an ID with [`useId`.](/reference/react/useId)

```
import { useId } from 'react';

export default function Form() {
  const ageInputId = useId();
  return (
    <>
      <label>
        Your first name:
        <input name="firstName" />
      </label>
      <hr />
      <label htmlFor={ageInputId}>Your age:</label>
      <input id={ageInputId} name="age" type="number" />
    </>
  );
}
```

***

### Providing an initial value for an input[](#providing-an-initial-value-for-an-input "Link for Providing an initial value for an input ")

You can optionally specify the initial value for any input. Pass it as the `defaultValue` string for text inputs. Checkboxes and radio buttons should specify the initial value with the `defaultChecked` boolean instead.

```
export default function MyForm() {
  return (
    <>
      <label>
        Text input: <input name="myInput" defaultValue="Some initial value" />
      </label>
      <hr />
      <label>
        Checkbox: <input type="checkbox" name="myCheckbox" defaultChecked={true} />
      </label>
      <hr />
      <p>
        Radio buttons:
        <label>
          <input type="radio" name="myRadio" value="option1" />
          Option 1
        </label>
        <label>
          <input
            type="radio"
            name="myRadio"
            value="option2"
            defaultChecked={true}
          />
          Option 2
        </label>
        <label>
          <input type="radio" name="myRadio" value="option3" />
          Option 3
        </label>
      </p>
    </>
  );
}
```

***

### Reading the input values when submitting a form[](#reading-the-input-values-when-submitting-a-form "Link for Reading the input values when submitting a form ")

Add a [`<form>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form) around your inputs with a [`<button type="submit">`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) inside. It will call your `<form onSubmit>` event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling `e.preventDefault()`. Read the form data with [`new FormData(e.target)`](https://developer.mozilla.org/en-US/docs/Web/API/FormData).

```
export default function MyForm() {
  function handleSubmit(e) {
    // Prevent the browser from reloading the page
    e.preventDefault();

    // Read the form data
    const form = e.target;
    const formData = new FormData(form);

    // You can pass formData as a fetch body directly:
    fetch('/some-api', { method: form.method, body: formData });

    // Or you can work with it as a plain object:
    const formJson = Object.fromEntries(formData.entries());
    console.log(formJson);
  }

  return (
    <form method="post" onSubmit={handleSubmit}>
      <label>
        Text input: <input name="myInput" defaultValue="Some initial value" />
      </label>
      <hr />
      <label>
        Checkbox: <input type="checkbox" name="myCheckbox" defaultChecked={true} />
      </label>
      <hr />
      <p>
        Radio buttons:
        <label><input type="radio" name="myRadio" value="option1" /> Option 1</label>
        <label><input type="radio" name="myRadio" value="option2" defaultChecked={true} /> Option 2</label>
        <label><input type="radio" name="myRadio" value="option3" /> Option 3</label>
      </p>
      <hr />
      <button type="reset">Reset form</button>
      <button type="submit">Submit form</button>
    </form>
  );
}
```

### Note

Give a `name` to every `<input>`, for example `<input name="firstName" defaultValue="Taylor" />`. The `name` you specified will be used as a key in the form data, for example `{ firstName: "Taylor" }`.

### Pitfall

By default, a `<button>` inside a `<form>` without a `type` attribute will submit it. This can be surprising! If you have your own custom `Button` React component, consider using [`<button type="button">`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) instead of `<button>` (with no type). Then, to be explicit, use `<button type="submit">` for buttons that *are* supposed to submit the form.

***

### Controlling an input with a state variable[](#controlling-an-input-with-a-state-variable "Link for Controlling an input with a state variable ")

An input like `<input />` is *uncontrolled.* Even if you [pass an initial value](#providing-an-initial-value-for-an-input) like `<input defaultValue="Initial text" />`, your JSX only specifies the initial value. It does not control what the value should be right now.

**To render a *controlled* input, pass the `value` prop to it (or `checked` for checkboxes and radios).** React will force the input to always have the `value` you passed. Usually, you would do this by declaring a [state variable:](/reference/react/useState)

```
function Form() {

  const [firstName, setFirstName] = useState(''); // Declare a state variable...

  // ...

  return (

    <input

      value={firstName} // ...force the input's value to match the state variable...

      onChange={e => setFirstName(e.target.value)} // ... and update the state variable on any edits!

    />

  );

}
```

A controlled input makes sense if you needed state anyway—for example, to re-render your UI on every edit:

```
function Form() {

  const [firstName, setFirstName] = useState('');

  return (

    <>

      <label>

        First name:

        <input value={firstName} onChange={e => setFirstName(e.target.value)} />

      </label>

      {firstName !== '' && <p>Your name is {firstName}.</p>}

      ...
```

It’s also useful if you want to offer multiple ways to adjust the input state (for example, by clicking a button):

```
function Form() {

  // ...

  const [age, setAge] = useState('');

  const ageAsNumber = Number(age);

  return (

    <>

      <label>

        Age:

        <input

          value={age}

          onChange={e => setAge(e.target.value)}

          type="number"

        />

        <button onClick={() => setAge(ageAsNumber + 10)}>

          Add 10 years

        </button>
```

The `value` you pass to controlled components should not be `undefined` or `null`. If you need the initial value to be empty (such as with the `firstName` field below), initialize your state variable to an empty string (`''`).

```
import { useState } from 'react';

export default function Form() {
  const [firstName, setFirstName] = useState('');
  const [age, setAge] = useState('20');
  const ageAsNumber = Number(age);
  return (
    <>
      <label>
        First name:
        <input
          value={firstName}
          onChange={e => setFirstName(e.target.value)}
        />
      </label>
      <label>
        Age:
        <input
          value={age}
          onChange={e => setAge(e.target.value)}
          type="number"
        />
        <button onClick={() => setAge(ageAsNumber + 10)}>
          Add 10 years
        </button>
      </label>
      {firstName !== '' &&
        <p>Your name is {firstName}.</p>
      }
      {ageAsNumber > 0 &&
        <p>Your age is {ageAsNumber}.</p>
      }
    </>
  );
}
```

### Pitfall

**If you pass `value` without `onChange`, it will be impossible to type into the input.** When you control an input by passing some `value` to it, you *force* it to always have the value you passed. So if you pass a state variable as a `value` but forget to update that state variable synchronously during the `onChange` event handler, React will revert the input after every keystroke back to the `value` that you specified.

***

### Optimizing re-rendering on every keystroke[](#optimizing-re-rendering-on-every-keystroke "Link for Optimizing re-rendering on every keystroke ")

When you use a controlled input, you set the state on every keystroke. If the component containing your state re-renders a large tree, this can get slow. There’s a few ways you can optimize re-rendering performance.

For example, suppose you start with a form that re-renders all page content on every keystroke:

```
function App() {

  const [firstName, setFirstName] = useState('');

  return (

    <>

      <form>

        <input value={firstName} onChange={e => setFirstName(e.target.value)} />

      </form>

      <PageContent />

    </>

  );

}
```

Since `<PageContent />` doesn’t rely on the input state, you can move the input state into its own component:

```
function App() {

  return (

    <>

      <SignupForm />

      <PageContent />

    </>

  );

}



function SignupForm() {

  const [firstName, setFirstName] = useState('');

  return (

    <form>

      <input value={firstName} onChange={e => setFirstName(e.target.value)} />

    </form>

  );

}
```

This significantly improves performance because now only `SignupForm` re-renders on every keystroke.

If there is no way to avoid re-rendering (for example, if `PageContent` depends on the search input’s value), [`useDeferredValue`](/reference/react/useDeferredValue#deferring-re-rendering-for-a-part-of-the-ui) lets you keep the controlled input responsive even in the middle of a large re-render.

***

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### My text input doesn’t update when I type into it[](#my-text-input-doesnt-update-when-i-type-into-it "Link for My text input doesn’t update when I type into it ")

If you render an input with `value` but no `onChange`, you will see an error in the console:

```
// 🔴 Bug: controlled text input with no onChange handler

<input value={something} />
```

Console

You provided a `value` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultValue`. Otherwise, set either `onChange` or `readOnly`.

As the error message suggests, if you only wanted to [specify the *initial* value,](#providing-an-initial-value-for-an-input) pass `defaultValue` instead:

```
// ✅ Good: uncontrolled input with an initial value

<input defaultValue={something} />
```

If you want [to control this input with a state variable,](#controlling-an-input-with-a-state-variable) specify an `onChange` handler:

```
// ✅ Good: controlled input with onChange

<input value={something} onChange={e => setSomething(e.target.value)} />
```

If the value is intentionally read-only, add a `readOnly` prop to suppress the error:

```
// ✅ Good: readonly controlled input without on change

<input value={something} readOnly={true} />
```

***

### My checkbox doesn’t update when I click on it[](#my-checkbox-doesnt-update-when-i-click-on-it "Link for My checkbox doesn’t update when I click on it ")

If you render a checkbox with `checked` but no `onChange`, you will see an error in the console:

```
// 🔴 Bug: controlled checkbox with no onChange handler

<input type="checkbox" checked={something} />
```

Console

You provided a `checked` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultChecked`. Otherwise, set either `onChange` or `readOnly`.

As the error message suggests, if you only wanted to [specify the *initial* value,](#providing-an-initial-value-for-an-input) pass `defaultChecked` instead:

```
// ✅ Good: uncontrolled checkbox with an initial value

<input type="checkbox" defaultChecked={something} />
```

If you want [to control this checkbox with a state variable,](#controlling-an-input-with-a-state-variable) specify an `onChange` handler:

```
// ✅ Good: controlled checkbox with onChange

<input type="checkbox" checked={something} onChange={e => setSomething(e.target.checked)} />
```

### Pitfall

You need to read `e.target.checked` rather than `e.target.value` for checkboxes.

If the checkbox is intentionally read-only, add a `readOnly` prop to suppress the error:

```
// ✅ Good: readonly controlled input without on change

<input type="checkbox" checked={something} readOnly={true} />
```

***

### My input caret jumps to the beginning on every keystroke[](#my-input-caret-jumps-to-the-beginning-on-every-keystroke "Link for My input caret jumps to the beginning on every keystroke ")

If you [control an input,](#controlling-an-input-with-a-state-variable) you must update its state variable to the input’s value from the DOM during `onChange`.

You can’t update it to something other than `e.target.value` (or `e.target.checked` for checkboxes):

```
function handleChange(e) {

  // 🔴 Bug: updating an input to something other than e.target.value

  setFirstName(e.target.value.toUpperCase());

}
```

You also can’t update it asynchronously:

```
function handleChange(e) {

  // 🔴 Bug: updating an input asynchronously

  setTimeout(() => {

    setFirstName(e.target.value);

  }, 100);

}
```

To fix your code, update it synchronously to `e.target.value`:

```
function handleChange(e) {

  // ✅ Updating a controlled input to e.target.value synchronously

  setFirstName(e.target.value);

}
```

If this doesn’t fix the problem, it’s possible that the input gets removed and re-added from the DOM on every keystroke. This can happen if you’re accidentally [resetting state](/learn/preserving-and-resetting-state) on every re-render, for example if the input or one of its parents always receives a different `key` attribute, or if you nest component function definitions (which is not supported and causes the “inner” component to always be considered a different tree).

***

***

----
