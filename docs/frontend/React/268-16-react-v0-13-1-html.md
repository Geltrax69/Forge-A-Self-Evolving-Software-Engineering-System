url: https://legacy.reactjs.org/blog/2015/03/16/react-v0.13.1.html
----

March 16, 2015 by [Paul O’Shannessy](https://twitter.com/zpao)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

It’s been less than a week since we shipped v0.13.0 but it’s time to do another quick release. We just released v0.13.1 which contains bugfixes for a number of small issues.

Thanks all of you who have been upgrading your applications and taking the time to report issues. And a huge thank you to those of you who submitted pull requests for the issues you found! 2 of the 6 fixes that went out today came from people who aren’t on the core team!

The release is now available for download:

* **React**\
  Dev build with warnings: <https://fb.me/react-0.13.1.js>\
  Minified build for production: <https://fb.me/react-0.13.1.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.13.1.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.13.1.min.js>
* **In-Browser JSX transformer**\
  <https://fb.me/JSXTransformer-0.13.1.js>

We’ve also published version `0.13.1` of the `react` and `react-tools` packages on npm and the `react` package on bower.

***

## [](#changelog)Changelog

### [](#react-core)React Core

#### [](#bug-fixes)Bug Fixes

* Don’t throw when rendering empty `<select>` elements
* Ensure updating `style` works when transitioning from `null`

### [](#react-with-add-ons)React with Add-Ons

#### [](#bug-fixes-1)Bug Fixes

* TestUtils: Don’t warn about `getDOMNode` for ES6 classes
* TestUtils: Ensure wrapped full page components (`<html>`, `<head>`, `<body>`) are treated as DOM components
* Perf: Stop double-counting DOM components

### [](#react-tools)React Tools

#### [](#bug-fixes-2)Bug Fixes

* Fix option parsing for `--non-strict-es6module`

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2015-03-16-react-v0.13.1.md)

----
