url: https://legacy.reactjs.org/blog/2016/03/29/react-v0.14.8.html
----

March 29, 2016 by [Dan Abramov](https://twitter.com/dan_abramov)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

We have already released two release candidates for React 15, and the final version is coming soon.

However [Ian Christian Myers](https://github.com/iancmyers) discovered a memory leak related to server rendering in React 0.14 and [contributed a fix](https://github.com/facebook/react/pull/6060). While this memory leak has already been fixed in a different way in the React 15 release candidates, we decided to cut another 0.14 release that contains just this fix.

The release is now available for download:

* **React**\
  Dev build with warnings: <https://fb.me/react-0.14.8.js>\
  Minified build for production: <https://fb.me/react-0.14.8.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.14.8.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.14.8.min.js>
* **React DOM** (include React in the page before React DOM)\
  Dev build with warnings: <https://fb.me/react-dom-0.14.8.js>\
  Minified build for production: <https://fb.me/react-dom-0.14.8.min.js>
* **React DOM Server** (include React in the page before React DOM Server)\
  Dev build with warnings: <https://fb.me/react-dom-server-0.14.8.js>\
  Minified build for production: <https://fb.me/react-dom-server-0.14.8.min.js>

We’ve also published version `0.14.8` of the `react`, `react-dom`, and addons packages on npm and the `react` package on bower.

***

## [](#changelog)Changelog

### [](#react)React

* Fixed memory leak when rendering on the server

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2016-03-29-react-v0.14.8.md)

----
