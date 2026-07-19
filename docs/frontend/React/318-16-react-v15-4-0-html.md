url: https://legacy.reactjs.org/blog/2016/11/16/react-v15.4.0.html
----

November 16, 2016 by [Dan Abramov](https://twitter.com/dan_abramov)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

Today we are releasing React 15.4.0.

We didn’t announce the [previous](https://github.com/facebook/react/blob/main/CHANGELOG.md#1510-may-20-2016) [minor](https://github.com/facebook/react/blob/main/CHANGELOG.md#1520-july-1-2016) [releases](https://github.com/facebook/react/blob/main/CHANGELOG.md#1530-july-29-2016) on the blog because most of the changes were bug fixes. However, 15.4.0 is a special release, and we would like to highlight a few notable changes in it.

### [](#separating-react-and-react-dom)Separating React and React DOM

[More than a year ago](/blog/2015/09/10/react-v0.14-rc1.html#two-packages-react-and-react-dom), we started separating React and React DOM into separate packages. We deprecated `React.render()` in favor of `ReactDOM.render()` in React 0.14, and removed DOM-specific APIs from `React` completely in React 15. However, the React DOM implementation still [secretly lived inside the React package](https://www.reddit.com/r/javascript/comments/3m6wyu/found_this_line_in_the_react_codebase_made_me/cvcyo4a/).

In React 15.4.0, we are finally moving React DOM implementation to the React DOM package. The React package will now contain only the renderer-agnostic code such as `React.Component` and `React.createElement()`.

This solves a few long-standing issues, such as [errors](https://github.com/facebook/react/issues/7386) when you import React DOM in the same file as the [snapshot testing](https://facebook.github.io/jest/blog/2016/07/27/jest-14.html) renderer.

**If you only use the official and documented React APIs you won’t need to change anything in your application.**

However, there is a possibility that you imported private APIs from `react/lib/*`, or that a package you rely on might use them. We would like to remind you that this was never supported, and that your apps should not rely on internal APIs. The React internals will keep changing as we work to make React better.

Another thing to watch out for is that React DOM Server is now about the same size as React DOM since it contains its own copy of the React reconciler. We don’t recommend using React DOM Server on the client in most cases.

### [](#profiling-components-with-chrome-timeline)Profiling Components with Chrome Timeline

You can now visualize React components in the Chrome Timeline. This lets you see which components exactly get mounted, updated, and unmounted, how much time they take relative to each other.

[](/static/64d522b74fb585f1abada9801f85fa9d/1ac66/react-perf-chrome-timeline.png)

To use it:

1. Load your app with `?react_perf` in the query string (for example, `http://localhost:3000/?react_perf`).
2. Open the Chrome DevTools **Timeline** tab and press **Record**.
3. Perform the actions you want to profile. Don’t record more than 20 seconds or Chrome might hang.
4. Stop recording.
5. React events will be grouped under the **User Timing** label.

Note that the numbers are relative so components will render faster in production. Still, this should help you realize when unrelated UI gets updated by mistake, and how deep and how often your UI updates occur.

Currently Chrome, Edge, and IE are the only browsers supporting this feature, but we use the standard [User Timing API](https://developer.mozilla.org/en-US/docs/Web/API/User_Timing_API) so we expect more browsers to add support for it.

### [](#mocking-refs-for-snapshot-testing)Mocking Refs for Snapshot Testing

If you’re using Jest [snapshot testing](https://facebook.github.io/jest/blog/2016/07/27/jest-14.html), you might have had [issues](https://github.com/facebook/react/issues/7371) with components that rely on refs. With React 15.4.0, we introduce a way to provide mock refs to the test renderer. For example, consider this component using a ref in `componentDidMount`:

```
import React from 'react';

export default class MyInput extends React.Component {
  componentDidMount() {
    this.input.focus();  }

  render() {
    return (
      <input
        ref={node => this.input = node}      />
    );
  }
}
```

With snapshot renderer, `this.input` will be `null` because there is no DOM. React 15.4.0 lets us avoid such crashes by passing a custom `createNodeMock` function to the snapshot renderer in an `options` argument:

```
import React from 'react';
import MyInput from './MyInput';
import renderer from 'react-test-renderer';

function createNodeMock(element) {  if (element.type === 'input') {    return {      focus() {},    };  }  return null;}
it('renders correctly', () => {
  const options = {createNodeMock};
  const tree = renderer.create(<MyInput />, options);  expect(tree).toMatchSnapshot();
});
```

We would like to thank [Brandon Dail](https://github.com/Aweary) for implementing this feature.

You can learn more about snapshot testing in [this Jest blog post](https://facebook.github.io/jest/blog/2016/07/27/jest-14.html).

***

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

## [](#installation)Installation

We recommend using [Yarn](https://yarnpkg.com/) or [npm](https://www.npmjs.com/) for managing front-end dependencies. If you’re new to package managers, the [Yarn documentation](https://yarnpkg.com/en/docs/getting-started) is a good place to get started.

To install React with Yarn, run:

```
yarn add react@15.4.0 react-dom@15.4.0
```

To install React with npm, run:

```
npm install --save react@15.4.0 react-dom@15.4.0
```

We recommend using a bundler like [webpack](https://webpack.js.org/) or [Browserify](http://browserify.org/) so you can write modular code and bundle it together into small packages to optimize load time.

Remember that by default, React runs extra checks and provides helpful warnings in development mode. When deploying your app, make sure to [compile it in production mode](/docs/installation.html#development-and-production-versions).

In case you don’t use a bundler, we also provide pre-built bundles in the npm packages which you can [include as script tags](/docs/installation.html#using-a-cdn) on your page:

* **React**\
  Dev build with warnings: [react/dist/react.js](https://unpkg.com/react@15.4.0/dist/react.js)\
  Minified build for production: [react/dist/react.min.js](https://unpkg.com/react@15.4.0/dist/react.min.js)
* **React with Add-Ons**\
  Dev build with warnings: [react/dist/react-with-addons.js](https://unpkg.com/react@15.4.0/dist/react-with-addons.js)\
  Minified build for production: [react/dist/react-with-addons.min.js](https://unpkg.com/react@15.4.0/dist/react-with-addons.min.js)
* **React DOM** (include React in the page before React DOM)\
  Dev build with warnings: [react-dom/dist/react-dom.js](https://unpkg.com/react-dom@15.4.0/dist/react-dom.js)\
  Minified build for production: [react-dom/dist/react-dom.min.js](https://unpkg.com/react-dom@15.4.0/dist/react-dom.min.js)
* **React DOM Server** (include React in the page before React DOM Server)\
  Dev build with warnings: [react-dom/dist/react-dom-server.js](https://unpkg.com/react-dom@15.4.0/dist/react-dom-server.js)\
  Minified build for production: [react-dom/dist/react-dom-server.min.js](https://unpkg.com/react-dom@15.4.0/dist/react-dom-server.min.js)

We’ve also published version `15.4.0` of the `react`, `react-dom`, and addons packages on npm and the `react` package on bower.

***

## [](#changelog)Changelog

### [](#react)React

* React package and browser build no longer “secretly” includes React DOM.\
  ([@sebmarkbage](https://github.com/sebmarkbage) in [#7164](https://github.com/facebook/react/pull/7164) and [#7168](https://github.com/facebook/react/pull/7168))
* Required PropTypes now fail with specific messages for null and undefined.\
  ([@chenglou](https://github.com/chenglou) in [#7291](https://github.com/facebook/react/pull/7291))
* Improved development performance by freezing children instead of copying.\
  ([@keyanzhang](https://github.com/keyanzhang) in [#7455](https://github.com/facebook/react/pull/7455))

### [](#react-dom)React DOM

* Fixed occasional test failures when React DOM is used together with shallow renderer.\
  ([@goatslacker](https://github.com/goatslacker) in [#8097](https://github.com/facebook/react/pull/8097))
* Added a warning for invalid `aria-` attributes.\
  ([@jessebeach](https://github.com/jessebeach) in [#7744](https://github.com/facebook/react/pull/7744))
* Added a warning for using `autofocus` rather than `autoFocus`.\
  ([@hkal](https://github.com/hkal) in [#7694](https://github.com/facebook/react/pull/7694))
* Removed an unnecessary warning about polyfilling `String.prototype.split`.\
  ([@nhunzaker](https://github.com/nhunzaker) in [#7629](https://github.com/facebook/react/pull/7629))
* Clarified the warning about not calling PropTypes manually.\
  ([@jedwards1211](https://github.com/jedwards1211) in [#7777](https://github.com/facebook/react/pull/7777))
* The unstable `batchedUpdates` API now passes the wrapped function’s return value through.\
  ([@bgnorlov](https://github.com/bgnorlov) in [#7444](https://github.com/facebook/react/pull/7444))
* Fixed a bug with updating text in IE 8.\
  ([@mnpenner](https://github.com/mnpenner) in [#7832](https://github.com/facebook/react/pull/7832))

### [](#react-perf)React Perf

* When ReactPerf is started, you can now view the relative time spent in components as a chart in Chrome Timeline.\
  ([@gaearon](https://github.com/gaearon) in [#7549](https://github.com/facebook/react/pull/7549))

### [](#react-test-utils)React Test Utils

* If you call `Simulate.click()` on a `<input disabled onClick={foo} />` then `foo` will get called whereas it didn’t before.\
  ([@nhunzaker](https://github.com/nhunzaker) in [#7642](https://github.com/facebook/react/pull/7642))

### [](#react-test-renderer)React Test Renderer

* Due to packaging changes, it no longer crashes when imported together with React DOM in the same file.\
  ([@sebmarkbage](https://github.com/sebmarkbage) in [#7164](https://github.com/facebook/react/pull/7164) and [#7168](https://github.com/facebook/react/pull/7168))
* `ReactTestRenderer.create()` now accepts `{createNodeMock: element => mock}` as an optional argument so you can mock refs with snapshot testing.\
  ([@Aweary](https://github.com/Aweary) in [#7649](https://github.com/facebook/react/pull/7649) and [#8261](https://github.com/facebook/react/pull/8261))

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2016-11-16-react-v15.4.0.md)

----
