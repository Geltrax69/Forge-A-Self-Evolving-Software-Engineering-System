url: https://legacy.reactjs.org/blog/2014/07/17/react-v0.11.html
----

July 17, 2014 by [Paul O’Shannessy](https://twitter.com/zpao)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

**Update:** We missed a few important changes in our initial post and changelog. We’ve updated this post with details about [Descriptors](#descriptors) and [Prop Type Validation](#prop-type-validation).

***

We’re really happy to announce the availability of React v0.11. There seems to be a lot of excitement already and we appreciate everybody who gave the release candidate a try over the weekend. We made a couple small changes in response to the feedback and issues filed. We enabled the destructuring assignment transform when using `jsx --harmony`, fixed a small regression with `statics`, and made sure we actually exposed the new API we said we were shipping: `React.Children.count`.

This version has been cooking for a couple months now and includes a wide array of bug fixes and features. We highlighted some of the most important changes below, along with the full changelog.

The release is available for download from the CDN:

* **React**\
  Dev build with warnings: <https://fb.me/react-0.11.0.js>\
  Minified build for production: <https://fb.me/react-0.11.0.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.11.0.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.11.0.min.js>
* **In-Browser JSX transformer**\
  <https://fb.me/JSXTransformer-0.11.0.js>

We’ve also published version `0.11.0` of the `react` and `react-tools` packages on npm and the `react` package on bower.

Please try these builds out and [file an issue on GitHub](https://github.com/facebook/react/issues/new) if you see anything awry.

## [](#getdefaultprops)`getDefaultProps`

Starting in React 0.11, `getDefaultProps()` is called only once when `React.createClass()` is called, instead of each time a component is rendered. This means that `getDefaultProps()` can no longer vary its return value based on `this.props` and any objects will be shared across all instances. This change improves performance and will make it possible in the future to do PropTypes checks earlier in the rendering process, allowing us to give better error messages.

## [](#rendering-to-null)Rendering to `null`

Since React’s release, people have been using work arounds to “render nothing”. Usually this means returning an empty `<div/>` or `<span/>`. Some people even got clever and started returning `<noscript/>` to avoid extraneous DOM nodes. We finally provided a “blessed” solution that allows developers to write meaningful code. Returning `null` is an explicit indication to React that you do not want anything rendered. Behind the scenes we make this work with a `<noscript>` element, though in the future we hope to not put anything in the document. In the mean time, `<noscript>` elements do not affect layout in any way, so you can feel safe using `null` today!

```
// Before
render: function() {
  if (!this.state.visible) {
    return <span/>;
  }
  // ...
}

// After
render: function() {
  if (!this.state.visible) {
    return null;
  }
  // ...
}
```

## [](#jsx-namespacing)JSX Namespacing

Another feature request we’ve been hearing for a long time is the ability to have namespaces in JSX. Given that JSX is just JavaScript, we didn’t want to use XML namespacing. Instead we opted for a standard JS approach: object property access. Instead of assigning variables to access components stored in an object (such as a component library), you can now use the component directly as `<Namespace.Component/>`.

```
// Before
var UI = require('UI');
var UILayout = UI.Layout;
var UIButton = UI.Button;
var UILabel = UI.Label;

render: function() {
  return <UILayout><UIButton /><UILabel>text</UILabel></UILayout>;
}

// After
var UI = require('UI');

render: function() {
  return <UI.Layout><UI.Button /><UI.Label>text</UI.Label></UI.Layout>;
}
```

## [](#improved-keyboard-event-normalization)Improved keyboard event normalization

Keyboard events now contain a normalized `e.key` value according to the [DOM Level 3 Events spec](http://www.w3.org/TR/DOM-Level-3-Events/#keys-special), allowing you to write simpler key handling code that works in all browsers, such as:

```
handleKeyDown: function(e) {
  if (e.key === 'Enter') {
    // Handle enter key
  } else if (e.key === ' ') {
    // Handle spacebar
  } else if (e.key === 'ArrowLeft') {
    // Handle left arrow
  }
},
```

Keyboard and mouse events also now include a normalized `e.getModifierState()` that works consistently across browsers.

## [](#descriptors)Descriptors

In our [v0.10 release notes](/blog/2014/03/21/react-v0.10.html#clone-on-mount), we called out that we were deprecating the existing behavior of the component function call (eg `component = MyComponent(props, ...children)` or `component = <MyComponent prop={...}/>`). Previously that would create an instance and React would modify that internally. You could store that reference and then call functions on it (eg `component.setProps(...)`). This no longer works. `component` in the above examples will be a descriptor and not an instance that can be operated on. The v0.10 release notes provide a complete example along with a migration path. The development builds also provided warnings if you called functions on descriptors.

Along with this change to descriptors, `React.isValidComponent` and `React.PropTypes.component` now actually validate that the value is a descriptor. Overwhelmingly, these functions are used to validate the value of `MyComponent()`, which as mentioned is now a descriptor, not a component instance. We opted to reduce code churn and make the migration to 0.11 as easy as possible. However, we realize this is has caused some confusion and we’re working to make sure we are consistent with our terminology.

## [](#prop-type-validation)Prop Type Validation

Previously `React.PropTypes` validation worked by simply logging to the console. Internally, each validator was responsible for doing this itself. Additionally, you could write a custom validator and the expectation was that you would also simply `console.log` your error message. Very shortly into the 0.11 cycle we changed this so that our validators return (*not throw*) an `Error` object. We then log the `error.message` property in a central place in ReactCompositeComponent. Overall the result is the same, but this provides a clearer intent in validation. In addition, to better transition into our descriptor factory changes, we also currently run prop type validation twice in development builds. As a result, custom validators doing their own logging result in duplicate messages. To update, simply return an `Error` with your message instead.

## [](#changelog)Changelog

### [](#react-core)React Core

#### [](#breaking-changes)Breaking Changes

* `getDefaultProps()` is now called once per class and shared across all instances
* `MyComponent()` now returns a descriptor, not an instance
* `React.isValidComponent` and `React.PropTypes.component` validate *descriptors*, not component instances.
* Custom `propType` validators should return an `Error` instead of logging directly

* PureRenderMixin: a mixin which helps optimize “pure” components

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2014-07-17-react-v0.11.md)

----
