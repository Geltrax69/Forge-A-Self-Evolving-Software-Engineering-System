url: https://legacy.reactjs.org/blog/2015/03/30/community-roundup-26.html
----

March 30, 2015 by [Vjeux](https://twitter.com/vjeux)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

We open sourced React Native last week and the community reception blew away all our expectations! So many of you tried it, made cool stuff with it, raised many issues and even submitted pull requests to fix them! The entire team wants to say thank you!

> [#reactnative](https://twitter.com/hashtag/reactnative?src=hash) is like when you get a new expansion pack, and everybody is running around clueless about which NPC to talk to for the quests
>
> — Ryan Florence (@ryanflorence) [March 28, 2015](https://twitter.com/ryanflorence/status/581810423554543616)

## [](#when-is-react-native-android-coming)When is React Native Android coming?

**Give us 6 months**. At Facebook, we strive to only open-source projects that we are using in production. While the Android backend for React Native is starting to work (see video below at 37min), it hasn’t been shipped to any users yet. There’s a lot of work that goes into open-sourcing a project, and we want to do it right so that you have a great experience when using it.

## [](#ray-wenderlich---property-finder)Ray Wenderlich - Property Finder

If you are getting started with React Native, you should absolutely [use this tutorial](http://www.raywenderlich.com/99473/introducing-react-native-building-apps-javascript) from Colin Eberhardt. It goes through all the steps to make a reasonably complete app.

[](http://www.raywenderlich.com/99473/introducing-react-native-building-apps-javascript)

Colin also [blogged about his experience using React Native](http://blog.scottlogic.com/2015/03/26/react-native-retrospective.html) for a few weeks and gives his thoughts on why you would or wouldn’t use it.

## [](#the-changelog)The Changelog

Spencer Ahrens and I had the great pleasure to talk about React Native on [The Changelog](https://thechangelog.com/149/) podcast. It was really fun to chat for an hour, I hope that you’ll enjoy listening to it. :)

## [](#hacker-news)Hacker News

Less than 24 hours after React Native was open sourced, Simarpreet Singh built an [Hacker News reader app from scratch](https://github.com/iSimar/HackerNews-React-Native). It’s unbelievable how fast he was able to pull it off!

[](https://github.com/iSimar/HackerNews-React-Native)

## [](#parse--react)Parse + React

There’s a huge ecosystem of JavaScript modules on npm and React Native was designed to work well with the ones that don’t have DOM dependencies. Parse is a great example; you can `npm install parse` on your React Native project and it’ll work as is. :) We still have [a](https://github.com/facebook/react-native/issues/406) [few](https://github.com/facebook/react-native/issues/370) [issues](https://github.com/facebook/react-native/issues/316) to solve; please create an issue if your favorite library doesn’t work out of the box.

[](http://blog.parse.com/2015/03/25/parse-and-react-shared-chemistry/)

## [](#tcomb-form-native)tcomb-form-native

Giulio Canti is the author of the [tcomb-form library](https://github.com/gcanti/tcomb-form) for React. He already [ported it to React Native](https://github.com/gcanti/tcomb-form-native) and it looks great!

[](https://github.com/gcanti/tcomb-form-native)

## [](#facebook-login-with-react-native)Facebook Login with React Native

One of the reason we built React Native is to be able to use all the libraries in the native ecosystem. Brent Vatne leads the way and explains [how to use Facebook Login with React Native](http://brentvatne.ca/facebook-login-with-react-native/).

## [](#modus-create)Modus Create

Jay Garcia spent a lot of time during the beta working on a NES music player with React Native. He wrote a blog post to share his experience and explains some code snippets.

[](http://moduscreate.com/react-native-has-landed/)

## [](#react-native-with-babel-and-webpack)React Native with Babel and webpack

React Native ships with a custom packager and custom ES6 transforms instead of using what the open source community settled on such as [webpack](https://webpack.js.org/) and [Babel](https://babeljs.io/). The main reason for this is performance – we couldn’t get those tools to have sub-second reload time on a large codebase.

Roman Liutikov found a way to [use webpack and Babel to run on React Native](https://github.com/roman01la/react-native-babel)! In the future, we want to work with those projects to provide cleaner extension mechanisms.

## [](#a-dynamic-crazy-native-mobile-futurepowered-by-javascript)A Dynamic, Crazy, Native Mobile Future—Powered by JavaScript

Clay Allsopp wrote a post about [all the crazy things you could do with a JavaScript engine that renders native views](https://medium.com/@clayallsopp/a-dynamic-crazy-native-mobile-future-powered-by-javascript-70f2d56b1987). What about native embeds, seamless native browser, native search engine or even app generation…

## [](#random-tweet)Random Tweet

We’ve spent a lot of efforts getting the onboarding as easy as possible and we’re really happy that people noticed. We still have a lot of work to do on documentation, stay tuned!

> Wow. Getting started with React Native might have been the smoothest experience I’ve ever had with a new developer product.
>
> — Andreas Eldh (@eldh) [March 26, 2015](https://twitter.com/eldh/status/581186172094980096)

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2015-03-30-community-roundup-26.md)

----
