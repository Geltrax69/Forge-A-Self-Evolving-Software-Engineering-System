url: https://legacy.reactjs.org/blog/2014/02/20/react-v0.9.html
----

February 20, 2014 by [Sophie Alpert](https://sophiebits.com/)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

I’m excited to announce that today we’re releasing React v0.9, which incorporates many bug fixes and several new features since the last release. This release contains almost four months of work, including over 800 commits from over 70 committers!

Thanks to everyone who tested the release candidate; we were able to find and fix an error in the event handling code, we upgraded envify to make running browserify on React faster, and we added support for five new attributes.

As always, the release is available for download from the CDN:

* **React**\
  Dev build with warnings: <https://fb.me/react-0.9.0.js>\
  Minified build for production: <https://fb.me/react-0.9.0.min.js>
* **React with Add-Ons**\
  Dev build with warnings: <https://fb.me/react-with-addons-0.9.0.js>\
  Minified build for production: <https://fb.me/react-with-addons-0.9.0.min.js>
* **In-Browser JSX Transformer**\
  <https://fb.me/JSXTransformer-0.9.0.js>

We’ve also published version `0.9.0` of the `react` and `react-tools` packages on npm and the `react` package on bower.

## [](#whats-new)What’s New?

This version includes better support for normalizing event properties across all supported browsers so that you need to worry even less about cross-browser differences. We’ve also made many improvements to error messages and have refactored the core to never rethrow errors, so stack traces are more accurate and Chrome’s purple break-on-error stop sign now works properly.

We’ve also added to the add-ons build [React.addons.TestUtils](/docs/test-utils.html), a set of new utilities to help you write unit tests for React components. You can now simulate events on your components, and several helpers are provided to help make assertions about the rendered DOM tree.

We’ve also made several other improvements and a few breaking changes; the full changelog is provided below.

## [](#jsx-whitespace)JSX Whitespace

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

In cases where you want to preserve the space adjacent to a newline, you can write `{'Monkeys: '}` or `Monkeys:{' '}` in your JSX source. We’ve included a script to do an automated codemod of your JSX source tree that preserves the old whitespace behavior by adding and removing spaces appropriately. You can [install jsx\_whitespace\_transformer from npm](https://github.com/facebook/react/blob/main/npm-jsx_whitespace_transformer/README.md) and run it over your source tree to modify files in place. The transformed JSX files will preserve your code’s existing whitespace behavior.

* When prop types validation fails, a warning is logged instead of an error thrown (with the production build of React, type checks are now skipped for performance)
* On `input`, `select`, and `textarea` elements, `.getValue()` is no longer supported; use `.getDOMNode().value` instead
* `this.context` on components is now reserved for internal use by React

#### [](#new-features)New Features

* React now never rethrows errors, so stack traces are more accurate and Chrome’s purple break-on-error stop sign now works properly

* Added support for SVG tags `defs`, `linearGradient`, `polygon`, `radialGradient`, `stop`

* Added support for more attributes:

  * `crossOrigin` for CORS requests
  * `download` and `hrefLang` for `<a>` tags
  * `mediaGroup` and `muted` for `<audio>` and `<video>` tags

* Boolean attributes such as `disabled` are rendered without a value (previously `disabled="true"`, now simply `disabled`)

* `React.addons.TestUtils` was added to help write unit tests

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2014-02-20-react-v0.9.md)

----
