url: https://18.react.dev/reference/react-dom/components/progress
----

[API Reference](/reference/react)

[Components](/reference/react-dom/components)

# \<progress>[](#undefined "Link for this heading")

The [built-in browser `<progress>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/progress) lets you render a progress indicator.

```
<progress value={0.5} />
```

* [Reference](#reference)
  * [`<progress>`](#progress)
* [Usage](#usage)
  * [Controlling a progress indicator](#controlling-a-progress-indicator)

***

## Reference[](#reference "Link for Reference ")

### `<progress>`[](#progress "Link for this heading")

To display a progress indicator, render the [built-in browser `<progress>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/progress) component.

```
<progress value={0.5} />
```

[See more examples below.](#usage)

#### Props[](#props "Link for Props ")

`<progress>` supports all [common element props.](/reference/react-dom/components/common#props)

Additionally, `<progress>` supports these props:

* [`max`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/progress#max): A number. Specifies the maximum `value`. Defaults to `1`.
* [`value`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/progress#value): A number between `0` and `max`, or `null` for indeterminate progress. Specifies how much was done.

***

## Usage[](#usage "Link for Usage ")

### Controlling a progress indicator[](#controlling-a-progress-indicator "Link for Controlling a progress indicator ")

To display a progress indicator, render a `<progress>` component. You can pass a number `value` between `0` and the `max` value you specify. If you don’t pass a `max` value, it will assumed to be `1` by default.

If the operation is not ongoing, pass `value={null}` to put the progress indicator into an indeterminate state.

```
export default function App() {
  return (
    <>
      <progress value={0} />
      <progress value={0.5} />
      <progress value={0.7} />
      <progress value={75} max={100} />
      <progress value={1} />
      <progress value={null} />
    </>
  );
}
```

[Previous\<option>](/reference/react-dom/components/option)

[Next\<select>](/reference/react-dom/components/select)

***

----
