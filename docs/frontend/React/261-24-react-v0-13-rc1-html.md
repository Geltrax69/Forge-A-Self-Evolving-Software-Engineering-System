url: https://legacy.reactjs.org/blog/2015/02/24/react-v0.13-rc1.html
----

February 24, 2015 by [Paul O’Shannessy](https://twitter.com/zpao)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

Over the weekend we pushed out our first (and hopefully only) release candidate for React v0.13!

We’ve talked a little bit about the changes that are coming. The splashiest of these changes is support for ES6 Classes. You can read more about this in [our beta announcement](/blog/2015/01/27/react-v0.13.0-beta-1.html). We’re really excited about this! Sebastian also posted earlier this morning about [some of the other changes coming focused around ReactElement](/blog/2015/02/24/streamlining-react-elements.html). The changes we’ve been working on there will hopefully enable lots of improvements to performance and developer experience.

The release candidate is available for download:

* **React**\
  Dev build with warnings: <https://fb.me/react-0.13.0-rc1.js>\
  Minified build for production: <https://fb.me/react-0.13.0-rc1.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.13.0-rc1.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.13.0-rc1.min.js>
* **In-Browser JSX transformer**\
  <https://fb.me/JSXTransformer-0.13.0-rc1.js>

We’ve also published version `0.13.0-rc1` of the `react` and `react-tools` packages on npm and the `react` package on bower.

***

## [](#changelog)Changelog

### [](#react-core)React Core

#### [](#breaking-changes)Breaking Changes


* Support for using ES6 classes to build React components; see the [v0.13.0 beta 1 notes](/blog/2015/01/27/react-v0.13.0-beta-1.html) for details
* Added new top-level API `React.findDOMNode(component)`, which should be used in place of `component.getDOMNode()`. The base class for ES6-based components will not have `getDOMNode`. This change will enable some more patterns moving forward.
* New `ref` style, allowing a callback to be used in place of a name: `<Photo ref={(c) => this._photo = c} />` allows you to reference the component with `this._photo` (as opposed to `ref="photo"` which gives `this.refs.photo`)
* `this.setState()` can now take a function as the first argument for transactional state updates, such as `this.setState((state, props) => ({count: state.count + 1}));` — this means that you no longer need to use `this._pendingState`, which is now gone.
* Support for iterators and immutable-js sequences as children

#### [](#deprecations)Deprecations

* `ComponentClass.type` is deprecated. Just use `ComponentClass` (usually as `element.type === ComponentClass`)
* Some methods that are available on `createClass`-based components are removed or deprecated from ES6 classes (for example, `getDOMNode`, `setProps`, `replaceState`).

### [](#react-with-add-ons)React with Add-Ons

#### [](#deprecations-1)Deprecations

* `React.addons.classSet` is now deprecated. This functionality can be replaced with several freely available modules. [classnames](https://www.npmjs.com/package/classnames) is one such module.

### [](#react-tools)React Tools

#### [](#breaking-changes-1)Breaking Changes

* When transforming ES6 syntax, `class` methods are no longer enumerable by default, which requires `Object.defineProperty`; if you support browsers such as IE8, you can pass `--target es3` to mirror the old behavior

#### [](#new-features-1)New Features

* `--target` option is available on the jsx command, allowing users to specify and ECMAScript version to target.

  * `es5` is the default.
  * `es3` restored the previous default behavior. An additional transform is added here to ensure the use of reserved words as properties is safe (eg `this.static` will become `this['static']` for IE8 compatibility).

* The transform for the call spread syntax has also been enabled.

### [](#jsx)JSX

#### [](#breaking-changes-2)Breaking Changes

* A change was made to how some JSX was parsed, specifically around the use of `>` or `}` when inside an element. Previously it would be treated as a string but now it will be treated as a parse error. We will be releasing a standalone executable to find and fix potential issues in your JSX code.

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2015-02-24-react-v0.13-rc1.md)

----
