url: https://legacy.reactjs.org/blog/2014/08/03/community-roundup-21.html
----

August 03, 2014 by [Lou Husson](https://twitter.com/loukan42)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

## [](#react-router)React Router

[Ryan Florence](http://ryanflorence.com/) and [Michael Jackson](https://twitter.com/mjackson) ported Ember’s router to React in a project called [React Router](https://github.com/rackt/react-router). This is a very good example of both communities working together to make the web better!

```
React.renderComponent((
  <Routes>
    <Route handler={App}>
      <Route name="about" handler={About}/>
      <Route name="users" handler={Users}>
        <Route name="user" path="/user/:userId" handler={User}/>
      </Route>
    </Route>
  </Routes>
), document.getElementById('example'));
```

## [](#going-big-with-react)Going Big with React

Areeb Malik, from Facebook, talks about his experience using React. “On paper, all those JS frameworks look promising: clean implementations, quick code design, flawless execution. But what happens when you stress test JavaScript? What happens when you throw 6 megabytes of code at it? In this talk, we’ll investigate how React performs in a high stress situation, and how it has helped our team build safe code on a massive scale”

[](https://skillsmatter.com/skillscasts/5429-going-big-with-react)

## [](#what-is-react)What is React?

[Craig McKeachie](http://www.funnyant.com/author/admin/) author of [JavaScript Framework Guide](http://www.funnyant.com/javascript-framework-guide/) wrote an excellent news named [“What is React.js? Another Template Library?](http://www.funnyant.com/reactjs-what-is-it/)

* Is React a template library?
* Is React similar to Web Components?
* Are the Virtual DOM and Shadow DOM the same?
* Can React be used with other JavaScript MVC frameworks?
* Who uses React?
* Is React a premature optimization if you aren’t Facebook or Instagram?
* Can I work with designers?
* Will React hurt my search engine optimizations (SEO)?
* Is React a framework for building applications or a library with one feature?
* Are components a better way to build an application?
* Can I build something complex with React?

## [](#referencing-dynamic-children)Referencing Dynamic Children

While Matt Zabriskie was working on [react-tabs](https://www.npmjs.com/package/react-tabs) he discovered how to use React.Children.map and React.addons.cloneWithProps in order to [reference dynamic children](http://www.mattzabriskie.com/blog/react-referencing-dynamic-children).

```
var App = React.createClass({
  render: function () {
    var children = React.Children.map(this.props.children, function(child, index) {
      return React.addons.cloneWithProps(child, {
        ref: 'child-' + index
      });
    });
    return <div>{children}</div>;
  }
});
```

## [](#jsx-with-sweetjs-using-readtables)JSX with Sweet.js using Readtables

Have you ever wondered how JSX was implemented? James Long wrote a very instructive blog post that explains how to [compile JSX with Sweet.js using Readtables](http://jlongster.com/Compiling-JSX-with-Sweet.js-using-Readtables).

[](http://jlongster.com/Compiling-JSX-with-Sweet.js-using-Readtables)

## [](#first-look-getting-started-with-react)First Look: Getting Started with React

[Kirill Buga](http://modernweb.com/authors/kirill-buga/) wrote an article on Modern Web explaining how [React is different from traditional MVC](http://modernweb.com/2014/07/23/getting-started-reactjs/) used by most JavaScript applications

[](http://modernweb.com/2014/07/23/getting-started-reactjs)

## [](#react-draggable)React Draggable

[Matt Zabriskie](https://github.com/mzabriskie) released a [project](https://github.com/mzabriskie/react-draggable) to make your react components draggable.

[](https://mzabriskie.github.io/react-draggable/example/)

## [](#html-parser2-react)HTML Parser2 React

[Jason Brown](https://browniefed.github.io/) adapted htmlparser2 to React: [htmlparser2-react](https://www.npmjs.com/package/htmlparser2-react). That allows you to convert raw HTML to the virtual DOM. This is not the intended way to use React but can be useful as last resort if you have an existing piece of HTML.

```
var html = '<div data-id="1" class="hey this is a class" ' +
  'style="width:100%;height: 100%;"><article id="this-article">' +
  '<p>hey this is a paragraph</p><div><ul><li>1</li><li>2</li>' +
  '<li>3</li></ul></div></article></div>';
var parsedComponent = reactParser(html, React);
```

## [](#building-uis-with-react)Building UIs with React

If you haven’t yet tried out React, Jacob Rios did a Hangout where he covers the most important aspects and thankfully he recorded it!

## [](#random-tweets)Random Tweets

> We shipped reddit's first production [@reactjs](https://twitter.com/reactjs) code last week, our checkout process. <https://t.co/KUInwsCmAF>
>
> — Brian Holt (@holtbt) [July 28, 2014](https://twitter.com/holtbt/statuses/493852312604254208)

> .[@AirbnbNerds](https://twitter.com/AirbnbNerds) just launched our first user-facing React.js feature to production! We love it so far. <https://t.co/KtyudemcIW> /[@floydophone](https://twitter.com/floydophone)
>
> — spikebrehm (@spikebrehm) [July 22, 2014](https://twitter.com/spikebrehm/statuses/491645223643013121)

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2014-08-03-community-roundup-21.md)

----
