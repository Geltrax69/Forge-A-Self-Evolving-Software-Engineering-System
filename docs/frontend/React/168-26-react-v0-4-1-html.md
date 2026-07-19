url: https://legacy.reactjs.org/blog/2013/07/26/react-v0-4-1.html
----

July 26, 2013 by [Paul O’Shannessy](https://twitter.com/zpao)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

React v0.4.1 is a small update, mostly containing correctness fixes. Some code has been restructured internally but those changes do not impact any of our public APIs.

## [](#react)React

* `setState` callbacks are now executed in the scope of your component.
* `click` events now work on Mobile Safari.
* Prevent a potential error in event handling if `Object.prototype` is extended.
* Don’t set DOM attributes to the string `"undefined"` on update when previously defined.
* Improved support for `<iframe>` attributes.
* Added checksums to detect and correct cases where server-side rendering markup mismatches what React expects client-side.

## [](#jsxtransformer)JSXTransformer

* Improved environment detection so it can be run in a non-browser environment.

[Download it now!](/downloads.html)

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2013-07-26-react-v0-4-1.md)

----
