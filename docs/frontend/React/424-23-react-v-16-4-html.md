url: https://legacy.reactjs.org/blog/2018/05/23/react-v-16-4.html
----

May 23, 2018 by [Andrew Clark](https://twitter.com/acdlite)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

The latest minor release adds support for an oft-requested feature: pointer events!

It also includes a bugfix for `getDerivedStateFromProps`. Check out the full [changelog](#changelog) below.

## [](#pointer-events)Pointer Events

The following event types are now available in React DOM:

* `onPointerDown`
* `onPointerMove`
* `onPointerUp`
* `onPointerCancel`
* `onGotPointerCapture`
* `onLostPointerCapture`
* `onPointerEnter`
* `onPointerLeave`
* `onPointerOver`
* `onPointerOut`

Please note that these events will only work in browsers that support the [Pointer Events](https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events) specification. (At the time of this writing, this includes the latest versions of Chrome, Firefox, Edge, and Internet Explorer.) If your application depends on pointer events, we recommend using a third-party pointer events polyfill. We have opted not to include such a polyfill in React DOM, to avoid an increase in bundle size.

[Check out this example on CodeSandbox.](https://codesandbox.io/api/v1/sandboxes/define?parameters=N4IgZglgNgpgziAXKADgQwMYGs0HMYB0AVnAPYB2SoGFALjObVSACYwoNvkYTxUC-AGhABbNBEqIQARgBsAWgAs8gE4xYaODHkAjKKVzyUpOLQD0xifRXyYANwa04tgB5oRKWMQT8hICWwuBAAWtCJQzDSMjkggADwsEHYABBAsALwAOiAqpKS02QB8cWaJdoUgfnJKquowmtp6BkYm5pbRNvaOzjBuHl4kkXQxUhAepCq0yQBK9RhTYLkiyQDkapi0KwDcmeRjxpMzc7QAIgDyALLJi6TLa8fyLLfbu7tRpskAwgCS058AMgBRAD6AGVvgAtQHJdLJAAcAFYduQ3lBNHBkicVHgAEKkFzJXr0cgsDGzDYET63YzkRzJYC7ZLJUxoegw-mMpnJYKaT5oFC0ACuakQ1zQUC0gk5TJ4KgwsH-MDAtFFcIADFLyFzkrL5TAACqkFCqjWc_jIpkQOBYvC4CS4dlgcVaC3JFBqOwQUiCuCK5XstWu932L0-w0oAPIzkUE6kADuWthXUYMMKHK1XNowStBCtNtwdvIDthtBUgpgrqZydoBFoaBU-BrWloAAVSFYYCo-QLhTAABTVgjtazfFgASijGaZZjMyQA6jBmbQJous4uJBBaBBxTq8ipEuRWfBksvkjpF2g9KvSDrxRhBWi2WudTyi_BpckZ8lH53khQCB-WY5kS2LzG2cCbl65AnOodYDg4jATmak5MhQFykA47LVqm6bahAYDJH2ACEQFwLm1rYgW9pjrh2rJGoQoqOQlbJPwH7vFMwCwMqggnka_DsqRBAgRs4GQTGsFoPBjhISiU4ntmZHNqCdb0H2fbALqCpKrQvFaQa_E0ekaYaR-MoQHK2nKqK-l-lMADU346ZqdE6hZerhjZ7mwOGySOcuKAuVy_BjrJTLmq8GYUAAqhGSYIVMxmEUJeaUYWxZihKMBhX-5AAOL5N2jGLvFdJJUJymqf2wA8nARW9qKpbliFroUP8rT1WoWEJamgGKQQlVHhptWdTAopOllLWRVWLilqJJjidBkndWVaYMvJHFOf6pWMEOeAwAAGixm0BStu3oPgACax0UB8bBQHW7Lra53EqltUzyApObBp63q-s5Zl8caQPJJ9Qk_aGcDhkF4UseDHqQ3Z7KvXD_UQ39vklkaLEMcKWr3XWroRXJTJqCSnZ9jRz1cptNW8vyxV6d5MB2UzlkGSgAklv1LL0ChNO3VMOj4ipACesBPYDwv7p2oorNIKAEmQUBpMkADELAAJxa1rKww1yYgNhIcvSGqivJGqyQAExmy4euAyIEgABIwBAuChKKihqqa8lMnGaRZib3sAKT277boLVuFBy2oj5JDAYfasT7GC257NixLsLU9q_ssIHXy_ACILglC-tMsErvu29Px_ECYKQoCZdnhMbAqNMaCJD6oo10X9dQp-1tN8YEFR-QcuXsrgr0IndGvV57Os4DAXzx5RpNzomBYLguSCiSVL6CooojQzvbJAA_KsejlisyRy9vMAMDP2rLoKGDBAAgvMUFy-QFAJ_ryd5K4yYoRQGCQkhLnFjAdIwBhYuAzjAfghRAZMnAXYFBXJTBQJgfpBBbFw7agoG2DsKhYwJhgUJGM8ZyD4NcoQ8gxCOjoQcBQ_qaEMKIIwahBh7YOixVYTmGKnMuG5UYdYPk3B1ACLIkI2hdDuEFVbLw8RJ81DSIIBQRRo05HyLaq0MRnZRrqL0aYbRGCzDIPDiUMoljtQ5Xwfg3Y5J5jnAuAQMmrc-ycjiPmPEBILFBSePeEQjgCCNkBLAEJjAcSi1HH2NYeRNhjl2LJSovggA)

Huge thanks to [Philipp Spiess](https://github.com/philipp-spiess) for contributing this change!

## [](#bugfix-for-getderivedstatefromprops)Bugfix for `getDerivedStateFromProps`

`getDerivedStateFromProps` is now called every time a component is rendered, regardless of the cause of the update. Previously, it was only called if the component was re-rendered by its parent, and would not fire as the result of a local `setState`. This was an oversight in the initial implementation that has now been corrected. The previous behavior was more similar to `componentWillReceiveProps`, but the improved behavior ensures compatibility with React’s upcoming asynchronous rendering mode.

**This bug fix will not affect most apps**, but it may cause issues with a small fraction of components. The rare cases where it does matter fall into one of two categories:

### [](#1-avoid-side-effects-in-getderivedstatefromprops)1. Avoid Side Effects in `getDerivedStateFromProps`

Like the render method, `getDerivedStateFromProps` should be a pure function of props and state. Side effects in `getDerivedStateFromProps` were never supported, but since it now fires more often than it used to, the recent change may expose previously undiscovered bugs.

Side effectful code should be moved to other methods: for example, Flux dispatches typically belong inside the originating event handler, and manual DOM mutations belong inside componentDidMount or componentDidUpdate. You can read more about this in our recent post about [preparing for asynchronous rendering](/blog/2018/03/27/update-on-async-rendering.html).

### [](#2-compare-incoming-props-to-previous-props-when-computing-controlled-values)2. Compare Incoming Props to Previous Props When Computing Controlled Values

The following code assumes `getDerivedStateFromProps` only fires on prop changes:

```
static getDerivedStateFromProps(props, state) {
  if (props.value !== state.controlledValue) {
    return {
      // Since this method fires on both props and state changes, local updates
      // to the controlled value will be ignored, because the props version
      // always overrides it. Oops!
      controlledValue: props.value,
    };
  }
  return null;
}
```

One possible way to fix this is to compare the incoming value to the previous value by storing the previous props in state:

```
static getDerivedStateFromProps(props, state) {
  const prevProps = state.prevProps || {};
  // Compare the incoming prop to previous prop
  const controlledValue =
    prevProps.value !== props.value
      ? props.value
      : state.controlledValue;
  return {
    // Store the previous props in state
    prevProps: props,
    controlledValue,
  };
}
```

However, **code that “mirrors” props in state usually contains bugs**, whether you use the newer `getDerivedStateFromProps` or the legacy `componentWillReceiveProps`. We published a follow-up blog post that explains these problems in more detail, and suggests [simpler solutions that don’t involve `getDerivedStateFromProps()`](/blog/2018/06/07/you-probably-dont-need-derived-state.html).

## [](#installation)Installation

React v16.4.0 is available on the npm registry.

To install React 16 with Yarn, run:

```
yarn add react@^16.4.0 react-dom@^16.4.0
```

To install React 16 with npm, run:

```
npm install --save react@^16.4.0 react-dom@^16.4.0
```

We also provide UMD builds of React via a CDN:

```
<script crossorigin src="https://unpkg.com/react@16/umd/react.production.min.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@16/umd/react-dom.production.min.js"></script>
```

Refer to the documentation for [detailed installation instructions](/docs/installation.html).

## [](#changelog)Changelog

### [](#react)React

* Add a new [experimental](https://github.com/reactjs/rfcs/pull/51) `React.unstable_Profiler` component for measuring performance. ([@bvaughn](https://github.com/bvaughn) in [#12745](https://github.com/facebook/react/pull/12745))

### [](#react-dom)React DOM

* Add support for the Pointer Events specification. ([@philipp-spiess](https://github.com/philipp-spiess) in [#12507](https://github.com/facebook/react/pull/12507))
* Properly call `getDerivedStateFromProps()` regardless of the reason for re-rendering. ([@acdlite](https://github.com/acdlite) in [#12600](https://github.com/facebook/react/pull/12600) and [#12802](https://github.com/facebook/react/pull/12802))
* Fix a bug that prevented context propagation in some cases. ([@gaearon](https://github.com/gaearon) in [#12708](https://github.com/facebook/react/pull/12708))
* Fix re-rendering of components using `forwardRef()` on a deeper `setState()`. ([@gaearon](https://github.com/gaearon) in [#12690](https://github.com/facebook/react/pull/12690))
* Fix some attributes incorrectly getting removed from custom element nodes. ([@airamrguez](https://github.com/airamrguez) in [#12702](https://github.com/facebook/react/pull/12702))
* Fix context providers to not bail out on children if there’s a legacy context provider above. ([@gaearon](https://github.com/gaearon) in [#12586](https://github.com/facebook/react/pull/12586))
* Add the ability to specify `propTypes` on a context provider component. ([@nicolevy](https://github.com/nicolevy) in [#12658](https://github.com/facebook/react/pull/12658))
* Fix a false positive warning when using `react-lifecycles-compat` in `<StrictMode>`. ([@bvaughn](https://github.com/bvaughn) in [#12644](https://github.com/facebook/react/pull/12644))
* Warn when the `forwardRef()` render function has `propTypes` or `defaultProps`. ([@bvaughn](https://github.com/bvaughn) in [#12644](https://github.com/facebook/react/pull/12644))
* Improve how `forwardRef()` and context consumers are displayed in the component stack. ([@sophiebits](https://github.com/sophiebits) in [#12777](https://github.com/facebook/react/pull/12777))
* Change internal event names. This can break third-party packages that rely on React internals in unsupported ways. ([@philipp-spiess](https://github.com/philipp-spiess) in [#12629](https://github.com/facebook/react/pull/12629))

### [](#react-test-renderer)React Test Renderer

* Fix the `getDerivedStateFromProps()` support to match the new React DOM behavior. ([@koba04](https://github.com/koba04) in [#12676](https://github.com/facebook/react/pull/12676))
* Fix a `testInstance.parent` crash when the parent is a fragment or another special node. ([@gaearon](https://github.com/gaearon) in [#12813](https://github.com/facebook/react/pull/12813))
* `forwardRef()` components are now discoverable by the test renderer traversal methods. ([@gaearon](https://github.com/gaearon) in [#12725](https://github.com/facebook/react/pull/12725))
* Shallow renderer now ignores `setState()` updaters that return `null` or `undefined`. ([@koba04](https://github.com/koba04) in [#12756](https://github.com/facebook/react/pull/12756))

### [](#react-art)React ART

* Fix reading context provided from the tree managed by React DOM. ([@acdlite](https://github.com/acdlite) in [#12779](https://github.com/facebook/react/pull/12779))

### [](#react-call-return-experimental)React Call Return (Experimental)

* This experiment was deleted because it was affecting the bundle size and the API wasn’t good enough. It’s likely to come back in the future in some other form. ([@gaearon](https://github.com/gaearon) in [#12820](https://github.com/facebook/react/pull/12820))

### [](#react-reconciler-experimental)React Reconciler (Experimental)

* The [new host config shape](https://github.com/facebook/react/blob/c601f7a64640290af85c9f0e33c78480656b46bc/packages/react-noop-renderer/src/createReactNoop.js#L82-L285) is flat and doesn’t use nested objects. ([@gaearon](https://github.com/gaearon) in [#12792](https://github.com/facebook/react/pull/12792))

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2018-05-23-react-v-16-4.md)

----
