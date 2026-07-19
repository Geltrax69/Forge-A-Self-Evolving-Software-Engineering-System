url: https://legacy.reactjs.org/blog/2017/07/26/error-handling-in-react-16.html
----

July 26, 2017 by [Dan Abramov](https://twitter.com/dan_abramov)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

As React 16 release is getting closer, we would like to announce a few changes to how React handles JavaScript errors inside components. These changes are included in React 16 beta versions, and will be a part of React 16.

**By the way, [we just released the first beta of React 16 for you to try!](https://github.com/facebook/react/issues/10294)**

## [](#behavior-in-react-15-and-earlier)Behavior in React 15 and Earlier

In the past, JavaScript errors inside components used to corrupt React’s internal state and cause it to [emit](https://github.com/facebook/react/issues/4026) [cryptic](https://github.com/facebook/react/issues/6895) [errors](https://github.com/facebook/react/issues/8579) on next renders. These errors were always caused by an earlier error in the application code, but React did not provide a way to handle them gracefully in components, and could not recover from them.

## [](#introducing-error-boundaries)Introducing Error Boundaries

A JavaScript error in a part of the UI shouldn’t break the whole app. To solve this problem for React users, React 16 introduces a new concept of an “error boundary”.

Error boundaries are React components that **catch JavaScript errors anywhere in their child component tree, log those errors, and display a fallback UI** instead of the component tree that crashed. Error boundaries catch errors during rendering, in lifecycle methods, and in constructors of the whole tree below them.

A class component becomes an error boundary if it defines a new lifecycle method called `componentDidCatch(error, info)`:

```
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  componentDidCatch(error, info) {    // Display fallback UI    this.setState({ hasError: true });    // You can also log the error to an error reporting service    logErrorToMyService(error, info);  }
  render() {
    if (this.state.hasError) {      // You can render any custom fallback UI      return <h1>Something went wrong.</h1>;    }    return this.props.children;
  }
}
```

Then you can use it as a regular component:

```
<ErrorBoundary>
  <MyWidget />
</ErrorBoundary>
```

The `componentDidCatch()` method works like a JavaScript `catch {}` block, but for components. Only class components can be error boundaries. In practice, most of the time you’ll want to declare an error boundary component once and use it throughout your application.

Note that **error boundaries only catch errors in the components below them in the tree**. An error boundary can’t catch an error within itself. If an error boundary fails trying to render the error message, the error will propagate to the closest error boundary above it. This, too, is similar to how `catch {}` block works in JavaScript.

## [](#live-demo)Live Demo

Check out [this example of declaring and using an error boundary](https://codepen.io/gaearon/pen/wqvxGa?editors=0010) with [React 16 beta](https://github.com/facebook/react/issues/10294).

## [](#where-to-place-error-boundaries)Where to Place Error Boundaries

The granularity of error boundaries is up to you. You may wrap top-level route components to display a “Something went wrong” message to the user, just like server-side frameworks often handle crashes. You may also wrap individual widgets in an error boundary to protect them from crashing the rest of the application.

If you don’t use Create React App, you can add [this plugin](https://www.npmjs.com/package/babel-plugin-transform-react-jsx-source) manually to your Babel configuration. Note that it’s intended only for development and **must be disabled in production**.

## [](#why-not-use-try--catch)Why Not Use `try` / `catch`?

`try` / `catch` is great but it only works for imperative code:

```
try {
  showButton();
} catch (error) {
  // ...
}
```

However, React components are declarative and specify *what* should be rendered:

```
<Button />
```

Error boundaries preserve the declarative nature of React, and behave as you would expect. For example, even if an error occurs in a `componentDidUpdate` method caused by a `setState` somewhere deep in the tree, it will still correctly propagate to the closest error boundary.

## [](#naming-changes-from-react-15)Naming Changes from React 15

React 15 included a very limited support for error boundaries under a different method name: `unstable_handleError`. This method no longer works, and you will need to change it to `componentDidCatch` in your code starting from the first 16 beta release.

For this change, we’ve provided a [codemod](https://github.com/reactjs/react-codemod#error-boundaries) to automatically migrate your code.

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2017-07-26-error-handling-in-react-16.md)

----
