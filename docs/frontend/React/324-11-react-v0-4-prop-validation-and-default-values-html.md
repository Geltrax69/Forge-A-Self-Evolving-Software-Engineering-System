url: https://legacy.reactjs.org/blog/2013/07/11/react-v0-4-prop-validation-and-default-values.html
----

July 11, 2013 by [Paul O’Shannessy](https://twitter.com/zpao)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

Many of the questions we got following the public launch of React revolved around `props`, specifically that people wanted to do validation and to make sure their components had sensible defaults.

## [](#validation)Validation

Oftentimes you want to validate your `props` before you use them. Perhaps you want to ensure they are a specific type. Or maybe you want to restrict your prop to specific values. Or maybe you want to make a specific prop required. This was always possible — you could have written validations in your `render` or `componentWillReceiveProps` functions, but that gets clunky fast.

React v0.4 will provide a nice easy way for you to use built-in validators, or to even write your own.

```
React.createClass({
  propTypes: {
    // An optional string prop named "description".
    description: React.PropTypes.string,

    // A required enum prop named "category".
    category: React.PropTypes.oneOf(['News','Photos']).isRequired,

    // A prop named "dialog" that requires an instance of Dialog.
    dialog: React.PropTypes.instanceOf(Dialog).isRequired
  },
  ...
});
```

## [](#default-values)Default Values

One common pattern we’ve seen with our React code is to do something like this:

```
React.createClass({
  render: function() {
    var value = this.props.value || 'default value';
    return <div>{value}</div>;
  }
});
```

Do this for a few `props` across a few components and now you have a lot of redundant code. Starting with React v0.4, you can provide default values in a declarative way:

```
React.createClass({
  getDefaultProps: function() {
    return {
      value: 'default value'
    };
  }
  ...
});
```

We will use the cached result of this function before each `render`. We also perform all validations before each `render` to ensure that you have all of the data you need in the right form before you try to use it.

***

Both of these features are entirely optional. We’ve found them to be increasingly valuable at Facebook as our applications grow and evolve, and we hope others find them useful as well.

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2013-07-11-react-v0-4-prop-validation-and-default-values.md)

----
