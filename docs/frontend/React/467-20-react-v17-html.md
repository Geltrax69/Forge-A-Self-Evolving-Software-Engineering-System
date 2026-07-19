url: https://legacy.reactjs.org/blog/2020/10/20/react-v17.html
----

October 20, 2020 by [Dan Abramov](https://twitter.com/dan_abramov) and [Rachel Nabors](https://twitter.com/rachelnabors)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

Today, we are releasing React 17! We’ve written at length about the role of the React 17 release and the changes it contains in [the React 17 RC blog post](/blog/2020/08/10/react-v17-rc.html). This post is a brief summary of it, so if you’ve already read the RC post, you can skip this one.

## [](#no-new-features)No New Features

The React 17 release is unusual because it doesn’t add any new developer-facing features. Instead, this release is primarily focused on **making it easier to upgrade React itself**.

In particular, React 17 is a “stepping stone” release that makes it safer to embed a tree managed by one version of React inside a tree managed by a different version of React.

It also makes it easier to embed React into apps built with other technologies.

## [](#gradual-upgrades)Gradual Upgrades

**React 17 enables gradual React upgrades.** When you upgrade from React 15 to 16 (or, this time, from React 16 to 17), you would usually upgrade your whole app at once. This works well for many apps. But it can get increasingly challenging if the codebase was written more than a few years ago and isn’t actively maintained. And while it’s possible to use two versions of React on the page, until React 17 this has been fragile and caused problems with events.

We’re fixing many of those problems with React 17. This means that **when React 18 and the next future versions come out, you will now have more options**. The first option will be to upgrade your whole app at once, like you might have done before. But you will also have an option to upgrade your app piece by piece. For example, you might decide to migrate most of your app to React 18, but keep some lazy-loaded dialog or a subroute on React 17.

This doesn’t mean you *have to* do gradual upgrades. **For most apps, upgrading all at once is still the best solution.** Loading two versions of React — even if one of them is loaded lazily on demand — is still not ideal. However, for larger apps that aren’t actively maintained, this option makes sense to consider, and React 17 lets those apps not get left behind.

We’ve prepared an [example repository](https://github.com/reactjs/react-gradual-upgrade-demo/) demonstrating how to lazy-load an older version of React if necessary. This demo uses Create React App, but it should be possible to follow a similar approach with any other tool. We welcome demos using other tooling as pull requests.

> Note
>
> We’ve **postponed other changes** until after React 17. The goal of this release is to enable gradual upgrades. If upgrading to React 17 were too difficult, it would defeat its purpose.

## [](#changes-to-event-delegation)Changes to Event Delegation

To enable gradual updates, we’ve needed to make some changes to the React event system. React 17 is a major release because these changes are potentially breaking. You can check out our [versioning FAQ](/docs/faq-versioning.html#breaking-changes) to learn more about our commitment to stability.

In React 17, React will no longer attach event handlers at the `document` level under the hood. Instead, it will attach them to the root DOM container into which your React tree is rendered:

```
const rootNode = document.getElementById('root');
ReactDOM.render(<App />, rootNode);
```

In React 16 and earlier, React would do `document.addEventListener()` for most events. React 17 will call `rootNode.addEventListener()` under the hood instead.

[](/static/bb4b10114882a50090b8ff61b3c4d0fd/31868/react_17_delegation.png)

We’ve confirmed that [numerous](https://github.com/facebook/react/issues/7094) [problems](https://github.com/facebook/react/issues/8693) [reported](https://github.com/facebook/react/issues/12518) [over](https://github.com/facebook/react/issues/13451) [the](https://github.com/facebook/react/issues/4335) [years](https://github.com/facebook/react/issues/1691) [on](https://github.com/facebook/react/issues/285#issuecomment-253502585) [our](https://github.com/facebook/react/pull/8117) [issue](https://github.com/facebook/react/issues/11530) [tracker](https://github.com/facebook/react/issues/7128) related to integrating React with non-React code have been fixed by the new behavior.

If you run into issues with this change, [here’s a common way to resolve them](/blog/2020/08/10/react-v17-rc.html#fixing-potential-issues).

## [](#other-breaking-changes)Other Breaking Changes

[The React 17 RC blog post](/blog/2020/08/10/react-v17-rc.html#other-breaking-changes) describes the rest of the breaking changes in React 17.

We’ve only had to change fewer than twenty components out of 100,000+ in the Facebook product code to work with these changes, so **we expect that most apps can upgrade to React 17 without too much trouble**. Please [tell us](https://github.com/facebook/react/issues) if you run into problems.

## [](#new-jsx-transform)New JSX Transform

React 17 supports the [new JSX transform](/blog/2020/09/22/introducing-the-new-jsx-transform.html). We’ve also backported support for it to React 16.14.0, React 15.7.0, and 0.14.10. Note that it is completely opt-in, and you don’t have to use it. The classic JSX transform will keep working, and there are no plans to stop supporting it.

## [](#react-native)React Native

React Native has a separate release schedule. We landed the support for React 17 in React Native 0.64. As always, you can track the release discussions on the React Native Community releases [issue tracker](https://github.com/react-native-community/releases).

## [](#installation)Installation

To install React 17 with npm, run:

```
npm install react@17.0.0 react-dom@17.0.0
```

To install React 17 with Yarn, run:

```
yarn add react@17.0.0 react-dom@17.0.0
```

We also provide UMD builds of React via a CDN:

```
<script crossorigin src="https://unpkg.com/react@17.0.0/umd/react.production.min.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@17.0.0/umd/react-dom.production.min.js"></script>
```

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2020-10-20-react-v17.md)

----
