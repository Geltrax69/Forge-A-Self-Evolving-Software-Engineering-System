url: https://18.react.dev/reference/react-dom/components/select
----

[API Reference](/reference/react)

[Components](/reference/react-dom/components)

# \<select>[](#undefined "Link for this heading")

The [built-in browser `<select>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) lets you render a select box with options.

```
<select>

  <option value="someOption">Some option</option>

  <option value="otherOption">Other option</option>

</select>
```

***

## Reference[](#reference "Link for Reference ")

### `<select>`[](#select "Link for this heading")

To display a select box, render the [built-in browser `<select>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) component.

```
<select>

  <option value="someOption">Some option</option>

  <option value="otherOption">Other option</option>

</select>
```

[See more examples below.](#usage)

#### Props[](#props "Link for Props ")

`<select>` supports all [common element props.](/reference/react-dom/components/common#props)

***

## Usage[](#usage "Link for Usage ")

### Displaying a select box with options[](#displaying-a-select-box-with-options "Link for Displaying a select box with options ")

Render a `<select>` with a list of `<option>` components inside to display a select box. Give each `<option>` a `value` representing the data to be submitted with the form.

```
export default function FruitPicker() {
  return (
    <label>
      Pick a fruit:
      <select name="selectedFruit">
        <option value="apple">Apple</option>
        <option value="banana">Banana</option>
        <option value="orange">Orange</option>
      </select>
    </label>
  );
}
```

***

### Providing a label for a select box[](#providing-a-label-for-a-select-box "Link for Providing a label for a select box ")

Typically, you will place every `<select>` inside a [`<label>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label) tag. This tells the browser that this label is associated with that select box. When the user clicks the label, the browser will automatically focus the select box. It’s also essential for accessibility: a screen reader will announce the label caption when the user focuses the select box.

If you can’t nest `<select>` into a `<label>`, associate them by passing the same ID to `<select id>` and [`<label htmlFor>`.](https://developer.mozilla.org/en-US/docs/Web/API/HTMLLabelElement/htmlFor) To avoid conflicts between multiple instances of one component, generate such an ID with [`useId`.](/reference/react/useId)

```
import { useId } from 'react';

export default function Form() {
  const vegetableSelectId = useId();
  return (
    <>
      <label>
        Pick a fruit:
        <select name="selectedFruit">
          <option value="apple">Apple</option>
          <option value="banana">Banana</option>
          <option value="orange">Orange</option>
        </select>
      </label>
      <hr />
      <label htmlFor={vegetableSelectId}>
        Pick a vegetable:
      </label>
      <select id={vegetableSelectId} name="selectedVegetable">
        <option value="cucumber">Cucumber</option>
        <option value="corn">Corn</option>
        <option value="tomato">Tomato</option>
      </select>
    </>
  );
}
```

***

### Providing an initially selected option[](#providing-an-initially-selected-option "Link for Providing an initially selected option ")

By default, the browser will select the first `<option>` in the list. To select a different option by default, pass that `<option>`’s `value` as the `defaultValue` to the `<select>` element.

```
export default function FruitPicker() {
  return (
    <label>
      Pick a fruit:
      <select name="selectedFruit" defaultValue="orange">
        <option value="apple">Apple</option>
        <option value="banana">Banana</option>
        <option value="orange">Orange</option>
      </select>
    </label>
  );
}
```

### Pitfall

Unlike in HTML, passing a `selected` attribute to an individual `<option>` is not supported.

***

### Enabling multiple selection[](#enabling-multiple-selection "Link for Enabling multiple selection ")

Pass `multiple={true}` to the `<select>` to let the user select multiple options. In that case, if you also specify `defaultValue` to choose the initially selected options, it must be an array.

```
export default function FruitPicker() {
  return (
    <label>
      Pick some fruits:
      <select
        name="selectedFruit"
        defaultValue={['orange', 'banana']}
        multiple={true}
      >
        <option value="apple">Apple</option>
        <option value="banana">Banana</option>
        <option value="orange">Orange</option>
      </select>
    </label>
  );
}
```

***

### Reading the select box value when submitting a form[](#reading-the-select-box-value-when-submitting-a-form "Link for Reading the select box value when submitting a form ")

Add a [`<form>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form) around your select box with a [`<button type="submit">`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) inside. It will call your `<form onSubmit>` event handler. By default, the browser will send the form data to the current URL and refresh the page. You can override that behavior by calling `e.preventDefault()`. Read the form data with [`new FormData(e.target)`](https://developer.mozilla.org/en-US/docs/Web/API/FormData).

```
export default function EditPost() {
  function handleSubmit(e) {
    // Prevent the browser from reloading the page
    e.preventDefault();
    // Read the form data
    const form = e.target;
    const formData = new FormData(form);
    // You can pass formData as a fetch body directly:
    fetch('/some-api', { method: form.method, body: formData });
    // You can generate a URL out of it, as the browser does by default:
    console.log(new URLSearchParams(formData).toString());
    // You can work with it as a plain object.
    const formJson = Object.fromEntries(formData.entries());
    console.log(formJson); // (!) This doesn't include multiple select values
    // Or you can get an array of name-value pairs.
    console.log([...formData.entries()]);
  }

  return (
    <form method="post" onSubmit={handleSubmit}>
      <label>
        Pick your favorite fruit:
        <select name="selectedFruit" defaultValue="orange">
          <option value="apple">Apple</option>
          <option value="banana">Banana</option>
          <option value="orange">Orange</option>
        </select>
      </label>
      <label>
        Pick all your favorite vegetables:
        <select
          name="selectedVegetables"
          multiple={true}
          defaultValue={['corn', 'tomato']}
        >
          <option value="cucumber">Cucumber</option>
          <option value="corn">Corn</option>
          <option value="tomato">Tomato</option>
        </select>
      </label>
      <hr />
      <button type="reset">Reset</button>
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Note

Give a `name` to your `<select>`, for example `<select name="selectedFruit" />`. The `name` you specified will be used as a key in the form data, for example `{ selectedFruit: "orange" }`.

If you use `<select multiple={true}>`, the [`FormData`](https://developer.mozilla.org/en-US/docs/Web/API/FormData) you’ll read from the form will include each selected value as a separate name-value pair. Look closely at the console logs in the example above.

### Pitfall

By default, *any* `<button>` inside a `<form>` will submit it. This can be surprising! If you have your own custom `Button` React component, consider returning [`<button type="button">`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/button) instead of `<button>`. Then, to be explicit, use `<button type="submit">` for buttons that *are* supposed to submit the form.

***

### Controlling a select box with a state variable[](#controlling-a-select-box-with-a-state-variable "Link for Controlling a select box with a state variable ")

A select box like `<select />` is *uncontrolled.* Even if you [pass an initially selected value](#providing-an-initially-selected-option) like `<select defaultValue="orange" />`, your JSX only specifies the initial value, not the value right now.

**To render a *controlled* select box, pass the `value` prop to it.** React will force the select box to always have the `value` you passed. Typically, you will control a select box by declaring a [state variable:](/reference/react/useState)

```
function FruitPicker() {

  const [selectedFruit, setSelectedFruit] = useState('orange'); // Declare a state variable...

  // ...

  return (

    <select

      value={selectedFruit} // ...force the select's value to match the state variable...

      onChange={e => setSelectedFruit(e.target.value)} // ... and update the state variable on any change!

    >

      <option value="apple">Apple</option>

      <option value="banana">Banana</option>

      <option value="orange">Orange</option>

    </select>

  );

}
```

This is useful if you want to re-render some part of the UI in response to every selection.

```
import { useState } from 'react';

export default function FruitPicker() {
  const [selectedFruit, setSelectedFruit] = useState('orange');
  const [selectedVegs, setSelectedVegs] = useState(['corn', 'tomato']);
  return (
    <>
      <label>
        Pick a fruit:
        <select
          value={selectedFruit}
          onChange={e => setSelectedFruit(e.target.value)}
        >
          <option value="apple">Apple</option>
          <option value="banana">Banana</option>
          <option value="orange">Orange</option>
        </select>
      </label>
      <hr />
      <label>
        Pick all your favorite vegetables:
        <select
          multiple={true}
          value={selectedVegs}
          onChange={e => {
            const options = [...e.target.selectedOptions];
            const values = options.map(option => option.value);
            setSelectedVegs(values);
          }}
        >
          <option value="cucumber">Cucumber</option>
          <option value="corn">Corn</option>
          <option value="tomato">Tomato</option>
        </select>
      </label>
      <hr />
      <p>Your favorite fruit: {selectedFruit}</p>
      <p>Your favorite vegetables: {selectedVegs.join(', ')}</p>
    </>
  );
}
```

### Pitfall

**If you pass `value` without `onChange`, it will be impossible to select an option.** When you control a select box by passing some `value` to it, you *force* it to always have the value you passed. So if you pass a state variable as a `value` but forget to update that state variable synchronously during the `onChange` event handler, React will revert the select box after every keystroke back to the `value` that you specified.

Unlike in HTML, passing a `selected` attribute to an individual `<option>` is not supported.

[Previous\<progress>](/reference/react-dom/components/progress)

[Next\<textarea>](/reference/react-dom/components/textarea)

***

----
