url: https://legacy.reactjs.org/blog/2015/10/07/react-v0.14.html
----

October 07, 2015 by [Sophie Alpert](https://sophiebits.com/)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

We’re happy to announce the release of React 0.14 today! This release has a few major changes, primarily designed to simplify the code you write every day and to better support environments like React Native.

If you tried the release candidate, thank you – your support is invaluable and we’ve fixed a few bugs that you reported.

As with all of our releases, we consider this version to be stable enough to use in production and recommend that you upgrade in order to take advantage of our latest improvements.

## [](#upgrade-guide)Upgrade Guide

Like always, we have a few breaking changes in this release. We know changes can be painful (the Facebook codebase has over 15,000 React components), so we always try to make changes gradually in order to minimize the pain.

If your code is free of warnings when running under React 0.13, upgrading should be easy. We have two new small breaking changes that didn’t give a warning in 0.13 (see below). Every new change in 0.14, including the major changes below, is introduced with a runtime warning and will work as before until 0.15, so you don’t have to worry about your app breaking with this upgrade.

For the two major changes which require significant code changes, we’ve included [codemod scripts](https://github.com/reactjs/react-codemod/blob/master/README.md) to help you upgrade your code automatically.

  Dev build with warnings: <https://fb.me/react-0.14.0.js>\
  Minified build for production: <https://fb.me/react-0.14.0.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.14.0.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.14.0.min.js>
* **React DOM** (include React in the page before React DOM)\
  Dev build with warnings: <https://fb.me/react-dom-0.14.0.js>\
  Minified build for production: <https://fb.me/react-dom-0.14.0.min.js>

  ```
  var React = require('react');
  var ReactDOM = require('react-dom');

  var MyComponent = React.createClass({
    render: function() {
      return <div>Hello World</div>;
    }
  });

  ReactDOM.render(<MyComponent />, node);
  ```

  The old names will continue to work with a warning until 0.15 is released, and we’ve published the [automated codemod script](https://github.com/reactjs/react-codemod/blob/master/README.md) we used at Facebook to help you with this transition.

  The add-ons have moved to separate packages as well:

  * `react-addons-clone-with-props`
  * `react-addons-create-fragment`
  * `react-addons-css-transition-group`
  * `react-addons-linked-state-mixin`
  * `react-addons-perf`
  * `react-addons-pure-render-mixin`
  * `react-addons-shallow-compare`
  * `react-addons-test-utils`
  * `react-addons-transition-group`
  * `react-addons-update`
  * `ReactDOM.unstable_batchedUpdates` in `react-dom`.

  For now, please use matching versions of `react` and `react-dom` (and the add-ons, if you use them) in your apps to avoid versioning problems.

* #### [](#dom-node-refs)DOM node refs

  The other big change we’re making in this release is exposing refs to DOM components as the DOM node itself. That means: we looked at what you can do with a `ref` to a React DOM component and realized that the only useful thing you can do with it is call `this.refs.giraffe.getDOMNode()` to get the underlying DOM node. Starting with this release, `this.refs.giraffe` *is* the actual DOM node. **Note that refs to custom (user-defined) components work exactly as before; only the built-in DOM components are affected by this change.**

  ```
  var Zoo = React.createClass({
    render: function() {
      return <div>Giraffe name: <input ref="giraffe" /></div>;
    },
    showName: function() {
      // Previously: var input = this.refs.giraffe.getDOMNode();
      var input = this.refs.giraffe;
      alert(input.value);
    }
  });
  ```

  This change also applies to the return result of `ReactDOM.render` when passing a DOM node as the top component. As with refs, this change does not affect custom components.

  With this change, we’re deprecating `.getDOMNode()` and replacing it with `ReactDOM.findDOMNode` (see below). If your components are currently using `.getDOMNode()`, they will continue to work with a warning until 0.15.

* #### [](#stateless-function-components)Stateless function components

  In idiomatic React code, most of the components you write will be stateless, simply composing other components. We’re introducing a new, simpler syntax for these components where you can take `props` as an argument and return the element you want to render:

  ```
  // A function component using an ES2015 (ES6) arrow function:
  var Aquarium = (props) => {
    var fish = getFish(props.species);
    return <Tank>{fish}</Tank>;
  };

  // Or with destructuring and an implicit return, simply:
  var Aquarium = ({species}) => (
    <Tank>
      {getFish(species)}
    </Tank>
  );

  // Then use: <Aquarium species="rainbowfish" />
  ```

  These components behave just like a React class with only a `render` method defined. Since no component instance is created for a function component, any `ref` added to one will evaluate to `null`. Function components do not have lifecycle methods, but you can set `.propTypes` and `.defaultProps` as properties on the function.

  This pattern is designed to encourage the creation of these simple components that should comprise large portions of your apps. In the future, we’ll also be able to make performance optimizations specific to these components by avoiding unnecessary checks and memory allocations.

* #### [](#deprecation-of-react-tools)Deprecation of react-tools

  The `react-tools` package and `JSXTransformer.js` browser file [have been deprecated](/blog/2015/06/12/deprecating-jstransform-and-react-tools.html). You can continue using version `0.13.3` of both, but we no longer support them and recommend migrating to [Babel](http://babeljs.io/), which has built-in support for React and JSX.

* #### [](#compiler-optimizations)Compiler optimizations

  React now supports two compiler optimizations that can be enabled in Babel 5.8.24 and newer. Both of these transforms **should be enabled only in production** (e.g., just before minifying your code) because although they improve runtime performance, they make warning messages more cryptic and skip important checks that happen in development mode, including propTypes.

  **Inlining React elements:** The `optimisation.react.inlineElements` transform converts JSX elements to object literals like `{type: 'div', props: ...}` instead of calls to `React.createElement`.

  **Constant hoisting for React elements:** The `optimisation.react.constantElements` transform hoists element creation to the top level for subtrees that are fully static, which reduces calls to `React.createElement` and the resulting allocations. More importantly, it tells React that the subtree hasn’t changed so React can completely skip it when reconciling.

### [](#breaking-changes)Breaking changes

In almost all cases, we change our APIs gradually and warn for at least one release to give you time to clean up your code. These two breaking changes did not have a warning in 0.13 but should be easy to find and clean up:

* `React.initializeTouchEvents` is no longer necessary and has been removed completely. Touch events now work automatically.
* Add-Ons: Due to the DOM node refs change mentioned above, `TestUtils.findAllInRenderedTree` and related helpers are no longer able to take a DOM component, only a custom component.

These three breaking changes had a warning in 0.13, so you shouldn’t have to do anything if your code is already free of warnings:

* The `props` object is now frozen, so mutating props after creating a component element is no longer supported. In most cases, [`React.cloneElement`](/docs/top-level-api.html#react.cloneelement) should be used instead. This change makes your components easier to reason about and enables the compiler optimizations mentioned above.
* Plain objects are no longer supported as React children; arrays should be used instead. You can use the [`createFragment`](/docs/create-fragment.html) helper to migrate, which now returns an array.
* Add-Ons: `classSet` has been removed. Use [classnames](https://github.com/JedWatson/classnames) instead.

### [](#new-deprecations-introduced-with-a-warning)New deprecations, introduced with a warning

Each of these changes will continue to work as before with a new warning until the release of 0.15 so you can upgrade your code gradually.

* Due to the DOM node refs change mentioned above, `this.getDOMNode()` is now deprecated and `ReactDOM.findDOMNode(this)` can be used instead. Note that in most cases, calling `findDOMNode` is now unnecessary – see the example above in the “DOM node refs” section.

  With each returned DOM node, we’ve added a `getDOMNode` method for backwards compatibility that will work with a warning until 0.15. If you have a large codebase, you can use our [automated codemod script](https://github.com/reactjs/react-codemod/blob/master/README.md) to change your code automatically.

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2015-10-07-react-v0.14.md)

----
