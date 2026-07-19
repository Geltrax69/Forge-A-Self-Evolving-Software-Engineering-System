url: https://legacy.reactjs.org/blog/2014/09/12/community-round-up-22.html
----

September 12, 2014 by [Lou Husson](https://twitter.com/loukan42)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

This has been an exciting summer as four big companies: Yahoo, Mozilla, Airbnb and Reddit announced that they were using React!

|                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| > Our friends at [@yahoo](https://twitter.com/Yahoo) talk about migrating Yahoo! Mail from YUI to ReactJS at the next [#ReactJS](https://twitter.com/hashtag/ReactJS?src=hash) meetup! <http://t.co/Cu2AaE0sVE>
>
> — Facebook Open Source (@fbOpenSource) [September 12, 2014](https://twitter.com/fbOpenSource/status/510258065900572672) | > I guess [@reactjs](https://twitter.com/reactjs) is getting into Firefox :-) Thanks [@n1k0](https://twitter.com/n1k0) ! <https://t.co/kipfUS0hu4>
>
> — David Bruant (@DavidBruant) [July 4, 2014](https://twitter.com/DavidBruant/status/484956929933213696) |
| > .[@AirbnbNerds](https://twitter.com/AirbnbNerds) just launched our first user-facing React.js feature to production! We love it so far. <https://t.co/KtyudemcIW> /[@floydophone](https://twitter.com/floydophone)
>
> — spikebrehm (@spikebrehm) [July 22, 2014](https://twitter.com/spikebrehm/statuses/491645223643013121)             | > We shipped reddit's first production [@reactjs](https://twitter.com/reactjs) code last week, our checkout process. <https://t.co/KUInwsCmAF>
>
> — Brian Holt (@holtbt) [July 28, 2014](https://twitter.com/holtbt/statuses/493852312604254208)              |

## [](#reacts-architecture)React’s Architecture

[Vjeux](http://blog.vjeux.com/), from the React team, gave a talk at OSCON on the history of React and the various optimizations strategies that are implemented. You can also check out the [annotated slides](https://speakerdeck.com/vjeux/oscon-react-architecture) or [Chris Dawson](http://thenewstack.io/author/chrisdawson/)’s notes titled [JavaScript’s History and How it Led To React](http://thenewstack.io/javascripts-history-and-how-it-led-to-reactjs/).

## [](#v8-optimizations)v8 optimizations

Jakob Kummerow landed [two optimizations to V8](http://www.chromium.org/developers/speed-hall-of-fame#TOC-2014-06-18) specifically targeted at optimizing React. That’s really exciting to see browser vendors helping out on performance!

## [](#reusable-components-by-khan-academy)Reusable Components by Khan Academy

[Khan Academy](https://www.khanacademy.org/) released [many high quality standalone components](https://khan.github.io/react-components/) they are using. This is a good opportunity to see what React code used in production look like.

```
var TeX = require('react-components/js/tex.jsx');
React.renderComponent(<TeX>\nabla \cdot E = 4 \pi \rho</TeX>, domNode);

var translated = (
  <$_ first="Motoko" last="Kusanagi">
    Hello, %(first)s %(last)s!
  </$_>
);
```

## [](#react--browserify--gulp)React + Browserify + Gulp

[Trường](http://truongtx.me/) wrote a little guide to help your [getting started using React, Browserify and Gulp](http://truongtx.me/2014/07/18/using-reactjs-with-browserify-and-gulp/).

[](http://truongtx.me/2014/07/18/using-reactjs-with-browserify-and-gulp/)

## [](#react-style)React Style

After React put HTML inside of JavaScript, Sander Spies takes the same approach with CSS: [IntegratedCSS](https://github.com/SanderSpies/react-style). It seems weird at first but this is the direction where React is heading.

```
var Button = React.createClass({
  normalStyle: ReactStyle(function() {
    return { backgroundColor: vars.orange };
  }),
  activeStyle: ReactStyle(function() {
    if (this.state.active) {
      return { color: 'yellow', padding: '10px' };
    }
  }),
  render: function() {
    return (
      <div styles={[this.normalStyle(), this.activeStyle()]}>
        Hello, I'm styled
      </div>
    );
  }
});
```

## [](#virtual-dom-in-elm)Virtual DOM in Elm

[Evan Czaplicki](http://evan.czaplicki.us) explains how Elm implements the idea of a Virtual DOM and a diffing algorithm. This is great to see React ideas spread to other languages.

> Performance is a good hook, but the real benefit is that this approach leads to code that is easier to understand and maintain. In short, it becomes very simple to create reusable HTML widgets and abstract out common patterns. This is why people with larger code bases should be interested in virtual DOM approaches.
>
> [Read the full article](http://elm-lang.org/blog/Blazing-Fast-Html.elm)

## [](#components-tutorial)Components Tutorial

If you are getting started with React, [Joe Maddalone](http://www.joemaddalone.com/) made a good tutorial on how to build your first component.

## [](#saving-time--staying-sane)Saving time & staying sane?

When [Kent William Innholt](http://http://kentwilliam.com/) who works at [M>Path](http://mpath.com/) summed up his experience using React in an [article](http://kentwilliam.com/articles/saving-time-staying-sane-pros-cons-of-react-js).

> We’re building an ambitious new web app, where the UI complexity represents most of the app’s complexity overall. It includes a tremendous amount of UI widgets as well as a lot rules on what-to-show-when. This is exactly the sort of situation React.js was built to simplify.
>
> * **Big win**: Tighter coupling of markup and behavior
> * **Jury’s still out**: CSS lives outside React.js
> * **Big win**: Cascading updates and functional thinking
> * **Jury’s still out**: Verbose propagation
>
> [Read the article…](http://kentwilliam.com/articles/saving-time-staying-sane-pros-cons-of-react-js)

## [](#weather)Weather

To finish this round-up, Andrew Gleave made a page that displays the [Weather](https://github.com/andrewgleave/react-weather). It’s great to see that React is also used for small prototypes.

[](https://github.com/andrewgleave/react-weather)

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2014-09-12-community-round-up-22.md)

----
