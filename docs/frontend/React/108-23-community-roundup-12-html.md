url: https://legacy.reactjs.org/blog/2013/12/23/community-roundup-12.html
----

December 23, 2013 by [Vjeux](https://twitter.com/vjeux)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

React got featured on the front-page of Hacker News thanks to the Om library. If you try it out for the first time, take a look at the [docs](/docs/getting-started.html) and do not hesitate to ask questions on the [Google Group](https://groups.google.com/group/reactjs), [IRC](irc://chat.freenode.net/reactjs) or [Stack Overflow](http://stackoverflow.com/questions/tagged/reactjs). We are trying our best to help you out!

## [](#the-future-of-javascript-mvc)The Future of JavaScript MVC

[David Nolen](https://swannodette.github.io/) announced Om, a thin wrapper on-top of React in ClojureScript. It stands out by only using immutable data structures. This unlocks the ability to write a very efficient [shouldComponentUpdate](/docs/component-specs.html#updating-shouldcomponentupdate) and get huge performance improvements on some tasks.

> We’ve known this for some time over here in the ClojureScript corner of the world - all of our collections are immutable and modeled directly on the original Clojure versions written in Java. Modern JavaScript engines have now been tuned to the point that it’s no longer uncommon to see collection performance within 2.5X of the Java Virtual Machine.
>
> Wait, wait, wait. What does the performance of persistent data structures have to do with the future of JavaScript MVCs?
>
> A whole lot.
>
> [](https://swannodette.github.io/2013/12/17/the-future-of-javascript-mvcs/)
>
> [Read the full article…](https://swannodette.github.io/2013/12/17/the-future-of-javascript-mvcs/)

## [](#scroll-position-with-react)Scroll Position with React

Managing the scroll position when new content is inserted is usually very tricky to get right. [Vjeux](http://blog.vjeux.com/) discovered that [componentWillUpdate](/docs/component-specs.html#updating-componentwillupdate) and [componentDidUpdate](/docs/component-specs.html#updating-componentdidupdate) were triggered exactly at the right time to manage the scroll position.

> We can check the scroll position before the component has updated with componentWillUpdate and scroll if necessary at componentDidUpdate
>
> ```
> componentWillUpdate: function() {
>   var node = this.getDOMNode();
>   this.shouldScrollBottom =
>     (node.scrollTop + node.offsetHeight) === node.scrollHeight;
> },
> componentDidUpdate: function() {
>   if (this.shouldScrollBottom) {
>     var node = this.getDOMNode();
>     node.scrollTop = node.scrollHeight
>   }
> },
> ```
>
> [Check out the blog article…](http://blog.vjeux.com/2013/javascript/scroll-position-with-react.html)

## [](#lights-out)Lights Out

React declarative approach is well suited to write games. [Cheng Lou](https://github.com/chenglou) wrote the famous Lights Out game in React. It’s a good example of use of [TransitionGroup](/docs/animation.html) to implement animations.

[](https://chenglou.github.io/react-lights-out/)

[Try it out!](https://chenglou.github.io/react-lights-out/)

## [](#reactive-table-bookmarklet)Reactive Table Bookmarklet

[Stoyan Stefanov](http://www.phpied.com/) wrote a bookmarklet to process tables on the internet. It adds a little “pop” button that expands to a full-screen view with sorting, editing and export to csv and json.

[](http://www.phpied.com/reactivetable-bookmarklet/)

[Check out the blog post…](http://www.phpied.com/reactivetable-bookmarklet/)

## [](#montagejs-tutorial-in-react)MontageJS Tutorial in React

[Ross Allen](https://twitter.com/ssorallen) implemented [MontageJS](http://montagejs.org/)’s [Reddit tutorial](http://montagejs.org/docs/tutorial-reddit-client-with-montagejs.html) in React. This is a good opportunity to compare the philosophies of the two libraries.

[View the source on JSFiddle…](https://jsfiddle.net/ssorallen/fEsYt/)

## [](#writing-good-react-components)Writing Good React Components

[William Högman Rudenmalm](http://blog.whn.se/) wrote an article on how to write good React components. This is full of good advice.

> The idea of dividing software into smaller parts or components is hardly new - It is the essance of good software. The same principles that apply to software in general apply to building React components. That doesn’t mean that writing good React components is just about applying general rules.
>
> The web offers a unique set of challenges, which React offers interesting solutions to. First and foremost among these solutions is the what is called the Mock DOM. Rather than having user code interface with the DOM in a direct fashion, as is the case with most DOM manipulation libraries.
>
> You build a model of how you want the DOM end up like. React then inserts this model into the DOM. This is very useful for updates because React simply compares the model or mock DOM against the actual DOM, and then only updates based on the difference between the two states.
>
> [Read the full article …](http://blog.whn.se/post/69621609605/writing-good-react-components)

## [](#hoodie-react-todomvc)Hoodie React TodoMVC

[Sven Lito](http://svenlito.com/) integrated the React TodoMVC example within an [Hoodie](http://hood.ie/) web app environment. This should let you get started using Hoodie and React.

```
hoodie new todomvc -t "hoodiehq/hoodie-react-todomvc"
```

[Check out on GitHub…](https://github.com/hoodiehq/hoodie-react-todomvc)

## [](#jsx-compiler)JSX Compiler

Ever wanted to have a quick way to see what a JSX tag would be converted to? [Tim Yung](http://www.yungsters.com/) made a page for it.

[](/react/jsx-compiler.html)

[Try it out!](/jsx-compiler.html)

## [](#random-tweet)Random Tweet

> .[@jordwalke](https://twitter.com/jordwalke) lays down some truth <http://t.co/AXAn0UlUe3>, optimizing your JS application shouldn't force you to rewrite so much code [#reactjs](https://twitter.com/search?q=%23reactjs\&src=hash)
>
> — David Nolen (@swannodette) [December 19, 2013](https://twitter.com/swannodette/statuses/413780079249215488)

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2013-12-23-community-roundup-12.md)

----
