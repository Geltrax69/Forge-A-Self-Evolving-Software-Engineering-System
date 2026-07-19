url: https://legacy.reactjs.org/blog/2015/09/10/react-v0.14-rc1.html
----

September 10, 2015 by [Sophie Alpert](https://sophiebits.com/)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

We’re happy to announce our first release candidate for React 0.14! We gave you a [sneak peek in July](/blog/2015/07/03/react-v0.14-beta-1.html) at the upcoming changes but we’ve now stabilized the release more and we’d love for you to try it out before we release the final version.

Let us know if you run into any problems by filing issues on our [GitHub repo](https://github.com/facebook/react).

## [](#installation)Installation

We recommend using React from `npm` and using a tool like browserify or webpack to build your code into a single package:

* `npm install --save react@0.14.0-rc1`
* `npm install --save react-dom@0.14.0-rc1`

Remember that by default, React runs extra checks and provides helpful warnings in development mode. When deploying your app, set the `NODE_ENV` environment variable to `production` to use the production build of React which does not include the development warnings and runs significantly faster.

If you can’t use `npm` yet, we also provide pre-built browser builds for your convenience:

* **React**\
  Dev build with warnings: <https://fb.me/react-0.14.0-rc1.js>\
  Minified build for production: <https://fb.me/react-0.14.0-rc1.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.14.0-rc1.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.14.0-rc1.min.js>
* **React DOM** (include React in the page before React DOM)\
  Dev build with warnings: <https://fb.me/react-dom-0.14.0-rc1.js>\
  Minified build for production: <https://fb.me/react-dom-0.14.0-rc1.min.js>

These builds are also available in the `react` package on bower.

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

  We’ve published the [automated codemod script](https://github.com/reactjs/react-codemod/blob/master/README.md) we used at Facebook to help you with this transition.

  The add-ons have moved to separate packages as well: `react-addons-clone-with-props`, `react-addons-create-fragment`, `react-addons-css-transition-group`, `react-addons-linked-state-mixin`, `react-addons-perf`, `react-addons-pure-render-mixin`, `react-addons-shallow-compare`, `react-addons-test-utils`, `react-addons-transition-group`, and `react-addons-update`, plus `ReactDOM.unstable_batchedUpdates` in `react-dom`.

  For now, please use matching versions of `react` and `react-dom` in your apps to avoid versioning problems.

* #### [](#dom-node-refs)DOM node refs

  The other big change we’re making in this release is exposing refs to DOM components as the DOM node itself. That means: we looked at what you can do with a `ref` to a React DOM component and realized that the only useful thing you can do with it is call `this.refs.giraffe.getDOMNode()` to get the underlying DOM node. In this release, `this.refs.giraffe` *is* the actual DOM node. **Note that refs to custom (user-defined) components work exactly as before; only the built-in DOM components are affected by this change.**

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

  This change also applies to the return result of `ReactDOM.render` when passing a DOM node as the top component. As with refs, this change does not affect custom components. With these changes, we’re deprecating `.getDOMNode()` and replacing it with `ReactDOM.findDOMNode` (see below).

* #### [](#stateless-function-components)Stateless function components

  In idiomatic React code, most of the components you write will be stateless, simply composing other components. We’re introducing a new, simpler syntax for these components where you can take `props` as an argument and return the element you want to render:

  ```
  // Using an ES2015 (ES6) arrow function:
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

  This pattern is designed to encourage the creation of these simple components that should comprise large portions of your apps. In the future, we’ll also be able to make performance optimizations specific to these components by avoiding unnecessary checks and memory allocations.

* #### [](#deprecation-of-react-tools)Deprecation of react-tools

  The `react-tools` package and `JSXTransformer.js` browser file [have been deprecated](/blog/2015/06/12/deprecating-jstransform-and-react-tools.html). You can continue using version `0.13.3` of both, but we no longer support them and recommend migrating to [Babel](http://babeljs.io/), which has built-in support for React and JSX.

* #### [](#compiler-optimizations)Compiler optimizations

  React now supports two compiler optimizations that can be enabled in Babel 5.8.23 and newer. Both of these transforms **should be enabled only in production** (e.g., just before minifying your code) because although they improve runtime performance, they make warning messages more cryptic and skip important checks that happen in development mode, including propTypes.

  **Inlining React elements:** The `optimisation.react.inlineElements` transform converts JSX elements to object literals like `{type: 'div', props: ...}` instead of calls to `React.createElement`.

  **Constant hoisting for React elements:** The `optimisation.react.constantElements` transform hoists element creation to the top level for subtrees that are fully static, which reduces calls to `React.createElement` and the resulting allocations. More importantly, it tells React that the subtree hasn’t changed so React can completely skip it when reconciling.

### [](#breaking-changes)Breaking changes

As always, we have a few breaking changes in this release. Whenever we make large changes, we warn for at least one release so you have time to update your code. The Facebook codebase has over 15,000 React components, so on the React team, we always try to minimize the pain of breaking changes.

These three breaking changes had a warning in 0.13, so you shouldn’t have to do anything if your code is already free of warnings:

* The `props` object is now frozen, so mutating props after creating a component element is no longer supported. In most cases, [`React.cloneElement`](/docs/top-level-api.html#react.cloneelement) should be used instead. This change makes your components easier to reason about and enables the compiler optimizations mentioned above.
* Plain objects are no longer supported as React children; arrays should be used instead. You can use the [`createFragment`](/docs/create-fragment.html) helper to migrate, which now returns an array.
* Add-Ons: `classSet` has been removed. Use [classnames](https://github.com/JedWatson/classnames) instead.

And these two changes did not warn in 0.13 but should be easy to find and clean up:

* `React.initializeTouchEvents` is no longer necessary and has been removed completely. Touch events now work automatically.
* Add-Ons: Due to the DOM node refs change mentioned above, `TestUtils.findAllInRenderedTree` and related helpers are no longer able to take a DOM component, only a custom component.

### [](#new-deprecations-introduced-with-a-warning)New deprecations, introduced with a warning

* Due to the DOM node refs change mentioned above, `this.getDOMNode()` is now deprecated and `ReactDOM.findDOMNode(this)` can be used instead. Note that in most cases, calling `findDOMNode` is now unnecessary – see the example above in the “DOM node refs” section.

  If you have a large codebase, you can use our [automated codemod script](https://github.com/facebook/react/blob/main/packages/react-codemod/README.md) to change your code automatically.

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2015-09-10-react-v0.14-rc1.md)

----
