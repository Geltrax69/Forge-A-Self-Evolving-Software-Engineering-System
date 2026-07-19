url: https://legacy.reactjs.org/blog/2014/02/16/react-v0.9-rc1.html
----

February 16, 2014 by [Sophie Alpert](https://sophiebits.com/)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

We’re almost ready to release React v0.9! We’re posting a release candidate so that you can test your apps on it; we’d much prefer to find show-stopping bugs now rather than after we release.

The release candidate is available for download from the CDN:

* **React**\
  Dev build with warnings: <https://fb.me/react-0.9.0-rc1.js>\
  Minified build for production: <https://fb.me/react-0.9.0-rc1.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.9.0-rc1.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.9.0-rc1.min.js>
* **In-Browser JSX transformer**\
  <https://fb.me/JSXTransformer-0.9.0-rc1.js>

We’ve also published version `0.9.0-rc1` of the `react` and `react-tools` packages on npm and the `react` package on bower.

Please try these builds out and [file an issue on GitHub](https://github.com/facebook/react/issues/new) if you see anything awry.

## [](#upgrade-notes)Upgrade Notes

In addition to the changes to React core listed below, we’ve made a small change to the way JSX interprets whitespace to make things more consistent. With this release, space between two components on the same line will be preserved, while a newline separating a text node from a tag will be eliminated in the output. Consider the code:

```
<div>
  Monkeys:
  {listOfMonkeys} {submitButton}
</div>
```

In v0.8 and below, it was transformed to the following:

```
React.DOM.div(null,
  " Monkeys: ",
  listOfMonkeys, submitButton
)
```

In v0.9, it will be transformed to this JS instead:

```
React.DOM.div(null,
  "Monkeys:",  listOfMonkeys, " ", submitButton)
```

We believe this new behavior is more helpful and eliminates cases where unwanted whitespace was previously added.

In cases where you want to preserve the space adjacent to a newline, you can write a JS string like `{"Monkeys: "}` in your JSX source. We’ve included a script to do an automated codemod of your JSX source tree that preserves the old whitespace behavior by adding and removing spaces appropriately. You can [install jsx\_whitespace\_transformer from npm](https://github.com/facebook/react/blob/main/npm-jsx_whitespace_transformer/README.md) and run it over your source tree to modify files in place. The transformed JSX files will preserve your code’s existing whitespace behavior.

* When prop types validation fails, a warning is logged instead of an error thrown (with the production build of React, the type checks are now skipped for performance)
* On `input`, `select`, and `textarea` elements, `.getValue()` is no longer supported; use `.getDOMNode().value` instead
* `this.context` on components is now reserved for internal use by React

#### [](#new-features)New Features

* React now never rethrows errors, so stack traces are more accurate and Chrome’s purple break-on-error stop sign now works properly

* Added a new tool for profiling React components and identifying places where defining `shouldComponentUpdate` can give performance improvements

* Added support for SVG tags `defs`, `linearGradient`, `polygon`, `radialGradient`, `stop`

* Added support for more attributes:


Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2014-02-16-react-v0.9-rc1.md)

----
