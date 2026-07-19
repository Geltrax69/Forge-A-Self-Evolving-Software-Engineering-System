url: https://legacy.reactjs.org/blog/2014/07/13/react-v0.11-rc1.html
----

July 13, 2014 by [Paul O’Shannessy](https://twitter.com/zpao)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

It’s that time again… we’re just about ready to ship a new React release! v0.11 includes a wide array of bug fixes and features. We highlighted some of the most important changes below, along with the full changelog.

The release candidate is available for download from the CDN:

* **React**\
  Dev build with warnings: <https://fb.me/react-0.11.0-rc1.js>\
  Minified build for production: <https://fb.me/react-0.11.0-rc1.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.11.0-rc1.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.11.0-rc1.min.js>
* **In-Browser JSX transformer**\
  <https://fb.me/JSXTransformer-0.11.0-rc1.js>

We’ve also published version `0.11.0-rc1` of the `react` and `react-tools` packages on npm and the `react` package on bower.

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

## [](#changelog)Changelog

### [](#react-core)React Core

#### [](#breaking-changes)Breaking Changes

* `getDefaultProps()` is now called once per class and shared across all instances

* PureRenderMixin

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2014-07-13-react-v0.11-rc1.md)

----
