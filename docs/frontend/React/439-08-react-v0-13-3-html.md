url: https://legacy.reactjs.org/blog/2015/05/08/react-v0.13.3.html
----

May 08, 2015 by [Paul O’Shannessy](https://twitter.com/zpao)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

Today we’re sharing another patch release in the v0.13 branch. There are only a few small changes, with a couple to address some issues that arose around that undocumented feature so many of you are already using: `context`. We also improved developer ergonomics just a little bit, making some warnings better.

The release is now available for download:

* **React**\
  Dev build with warnings: <https://fb.me/react-0.13.3.js>\
  Minified build for production: <https://fb.me/react-0.13.3.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.13.3.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.13.3.min.js>
* **In-Browser JSX transformer**\
  <https://fb.me/JSXTransformer-0.13.3.js>

We’ve also published version `0.13.3` of the `react` and `react-tools` packages on npm and the `react` package on bower.

***

## [](#changelog)Changelog

### [](#react-core)React Core

#### [](#new-features)New Features

* Added `clipPath` element and attribute for SVG
* Improved warnings for deprecated methods in plain JS classes

#### [](#bug-fixes)Bug Fixes

* Loosened `dangerouslySetInnerHTML` restrictions so `{__html: undefined}` will no longer throw
* Fixed extraneous context warning with non-pure `getChildContext`
* Ensure `replaceState(obj)` retains prototype of `obj`

### [](#react-with-add-ons)React with Add-ons

### [](#bug-fixes-1)Bug Fixes

* Test Utils: Ensure that shallow rendering works when components define `contextTypes`

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2015-05-08-react-v0.13.3.md)

----
