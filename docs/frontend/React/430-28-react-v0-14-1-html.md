url: https://legacy.reactjs.org/blog/2015/10/28/react-v0.14.1.html
----

October 28, 2015 by [Paul O’Shannessy](https://twitter.com/zpao)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

After a couple weeks of having more people use v0.14, we’re ready to ship a patch release addressing a few issues. Thanks to everybody who has reported issues and written patches!

The release is now available for download:

* **React**\
  Dev build with warnings: <https://fb.me/react-0.14.1.js>\
  Minified build for production: <https://fb.me/react-0.14.1.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.14.1.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.14.1.min.js>
* **React DOM** (include React in the page before React DOM)\
  Dev build with warnings: <https://fb.me/react-dom-0.14.1.js>\
  Minified build for production: <https://fb.me/react-dom-0.14.1.min.js>

We’ve also published version `0.14.1` of the `react`, `react-dom`, and addons packages on npm and the `react` package on bower.

***

## [](#changelog)Changelog

### [](#react-dom)React DOM

* Fixed bug where events wouldn’t fire in old browsers when using React in development mode
* Fixed bug preventing use of `dangerouslySetInnerHTML` with Closure Compiler Advanced mode
* Added support for `srcLang`, `default`, and `kind` attributes for `<track>` elements
* Added support for `color` attribute
* Ensured legacy `.props` access on DOM nodes is updated on re-renders

### [](#react-testutils-add-on)React TestUtils Add-on

* Fixed `scryRenderedDOMComponentsWithClass` so it works with SVG

### [](#react-csstransitiongroup-add-on)React CSSTransitionGroup Add-on

* Fix bug preventing `0` to be used as a timeout value

### [](#react-on-bower)React on Bower

* Added `react-dom.js` to `main` to improve compatibility with tooling

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2015-10-28-react-v0.14.1.md)

----
