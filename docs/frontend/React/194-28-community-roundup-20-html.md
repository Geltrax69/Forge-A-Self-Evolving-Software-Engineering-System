url: https://legacy.reactjs.org/blog/2014/07/28/community-roundup-20.html
----

July 28, 2014 by [Lou Husson](https://twitter.com/loukan42)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

It’s an exciting time for React as there are now more commits from open source contributors than from Facebook engineers! Keep up the good work :)

## [](#atom-moves-to-react)Atom moves to React

[Atom, GitHub’s code editor, is now using React](http://blog.atom.io/2014/07/02/moving-atom-to-react.html) to build the editing experience. They made the move in order to improve performance. By default, React helped them eliminate unnecessary reflows, enabling them to focus on architecting the rendering pipeline in order to minimize repaints by using hardware acceleration. This is a testament to the fact that React’s architecture is perfect for high performant applications.

[](http://blog.atom.io/2014/07/02/moving-atom-to-react.html)

## [](#why-does-react-scale)Why Does React Scale?

At the last [JSConf.us](http://2014.jsconf.us/), Vjeux talked about the design decisions made in the API that allows it to scale to a large number of developers. If you don’t have 20 minutes, take a look at the [annotated slides](https://speakerdeck.com/vjeux/why-does-react-scale-jsconf-2014).

## [](#live-editing)Live Editing

One of the best features of React is that it provides the foundations to implement concepts that were otherwise extremely difficult, like server-side rendering, undo-redo, rendering to non-DOM environments like canvas… [Dan Abramov](https://twitter.com/dan_abramov) got hot code reloading working with webpack in order to [live edit a React project](https://gaearon.github.io/react-hot-loader/)!

## [](#reactintl-mixin-by-yahoo)ReactIntl Mixin by Yahoo

There are a couple of React-related projects that recently appeared on Yahoo’s GitHub, the first one being an [internationalization mixin](https://github.com/yahoo/react-intl). It’s great to see them getting excited about React and contributing back to the community.

```
var MyComponent = React.createClass({
  mixins: [ReactIntlMixin],
  render: function() {
    return (
      <div>
        <p>{this.intlDate(1390518044403, { hour: 'numeric', minute: 'numeric' })}</p>
        <p>{this.intlNumber(400, { style: 'percent' })}</p>
      </div>
    );
  }
});

React.renderComponent(
  <MyComponent locales={['fr-FR']} />,
  document.getElementById('example')
);
```

## [](#thinking-and-learning-react)Thinking and Learning React

Josephine Hall, working at Icelab, used React to write a mobile-focused application. She wrote a blog post [“Thinking and Learning React.js”](http://icelab.com.au/articles/thinking-and-learning-reactjs/) to share her experience with elements they had to use. You’ll learn about routing, event dispatch, touchable components, and basic animations.

## [](#london-react-meetup)London React Meetup

If you missed the last [London React Meetup](http://www.meetup.com/London-React-User-Group/events/191406572/), the video is available, with lots of great content.

* What’s new in React 0.11 and how to improve performance by guaranteeing immutability
* State handling in React with Morearty.JS
* React on Rails - How to use React with Ruby on Rails to build isomorphic apps
* Building an isomorphic, real-time to-do list with moped and node.js

In related news, the next [React SF Meetup](http://www.meetup.com/ReactJS-San-Francisco/events/195518392/) will be from Prezi: [“Immediate Mode on the Web: How We Implemented the Prezi Viewer in JavaScript”](https://medium.com/prezi-engineering/how-and-why-prezi-turned-to-javascript-56e0ca57d135). While not in React, their tech is really awesome and shares a lot of React’s design principles and perf optimizations.

## [](#using-react-and-kendoui-together)Using React and KendoUI Together

One of the strengths of React is that it plays nicely with other libraries. Jim Cowart proved it by writing a tutorial that explains how to write [React component adapters for KendoUI](http://www.ifandelse.com/using-reactjs-and-kendoui-together/).

[](http://www.ifandelse.com/using-reactjs-and-kendoui-together/)

## [](#acorn-jsx)Acorn JSX

Ingvar Stepanyan extended the Acorn JavaScript parser to support JSX. The result is a [JSX parser](https://github.com/RReverser/acorn-jsx) that’s 1.5–2.0x faster than the official JSX implementation. It is an experiment and is not meant to be used for serious things, but it’s always a good thing to get competition on performance!

## [](#reactscriptloader)ReactScriptLoader

Yariv Sadan created [ReactScriptLoader](https://github.com/yariv/ReactScriptLoader) to make it easier to write components that require an external script.

```
var Foo = React.createClass({
  mixins: [ReactScriptLoaderMixin],
  getScriptURL: function() {
    return 'http://d3js.org/d3.v3.min.js';
  },
  getInitialState: function() {
    return { scriptLoading: true, scriptLoadError: false };
  },
  onScriptLoaded: function() {
    this.setState({scriptLoading: false});
  },
  onScriptError: function() {
    this.setState({scriptLoading: false, scriptLoadError: true});
  },
  render: function() {
    var message =
      this.state.scriptLoading ? 'Loading script...' :
      this.state.scriptLoadError ? 'Loading failed' :
      'Loading succeeded';
    return <span>{message}</span>;
  }
});
```

## [](#random-tweet)Random Tweet

> “[@apphacker](https://twitter.com/apphacker): I take back the mean things I said about [@reactjs](https://twitter.com/reactjs) I actually like it.” Summarizing the life of ReactJS in a single tweet.
>
> — Jordan (@jordwalke) [July 20, 2014](https://twitter.com/jordwalke/statuses/490747339607265280)

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2014-07-28-community-roundup-20.md)

----
