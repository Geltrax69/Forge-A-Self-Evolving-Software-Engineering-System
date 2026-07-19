url: https://legacy.reactjs.org/blog/2018/08/01/react-v-16-4-2.html
----

August 01, 2018 by [Dan Abramov](https://twitter.com/dan_abramov)

> This blog site has been archived. Go to [react.dev/blog](https://react.dev/blog) to see the recent posts.

We discovered a minor vulnerability that might affect some apps using ReactDOMServer. We are releasing a patch version for every affected React minor release so that you can upgrade with no friction. Read on for more details.

## [](#short-description)Short Description

Today, we are releasing a fix for a vulnerability we discovered in the `react-dom/server` implementation. It was introduced with the version 16.0.0 and has existed in all subsequent releases until today.

This vulnerability **can only affect some server-rendered React apps.** Purely client-rendered apps are **not** affected. Additionally, we expect that most server-rendered apps don’t contain the vulnerable pattern described below. Nevertheless, we recommend to follow the mitigation instructions at the earliest opportunity.

While we were investigating this vulnerability, we found similar vulnerabilities in a few other popular front-end libraries. We have coordinated this release together with [Vue](https://github.com/vuejs/vue/releases/tag/v2.5.17) and [Preact](https://github.com/developit/preact-render-to-string/releases/tag/3.7.1) releases fixing the same issue. The tracking number for this vulnerability is `CVE-2018-6341`.

## [](#mitigation)Mitigation

**We have prepared a patch release with a fix for every affected minor version.**

### [](#160x)16.0.x

If you’re using `react-dom/server` with this version:

* `react-dom@16.0.0`

Update to this version instead:

* `react-dom@16.0.1` **(contains the mitigation)**

### [](#161x)16.1.x

If you’re using `react-dom/server` with one of these versions:

* `react-dom@16.1.0`
* `react-dom@16.1.1`

Update to this version instead:

* `react-dom@16.1.2` **(contains the mitigation)**

### [](#162x)16.2.x

If you’re using `react-dom/server` with this version:

* `react-dom@16.2.0`

Update to this version instead:

* `react-dom@16.2.1` **(contains the mitigation)**

### [](#163x)16.3.x

If you’re using `react-dom/server` with one of these versions:

* `react-dom@16.3.0`
* `react-dom@16.3.1`
* `react-dom@16.3.2`

Update to this version instead:

* `react-dom@16.3.3` **(contains the mitigation)**

### [](#164x)16.4.x

If you’re using `react-dom/server` with one of these versions:

* `react-dom@16.4.0`
* `react-dom@16.4.1`

Update to this version instead:

* `react-dom@16.4.2` **(contains the mitigation)**

If you’re using a newer version of `react-dom`, no action is required.

Note that only the `react-dom` package needs to be updated.

## [](#detailed-description)Detailed Description

Your app might be affected by this vulnerability only if both of these two conditions are true:

* Your app is **being rendered to HTML using [ReactDOMServer API](/docs/react-dom-server.html)**, and
* Your app **includes a user-supplied attribute name in an HTML tag.**

Specifically, the vulnerable pattern looks like this:

```
let props = {};
props[userProvidedData] = "hello";let element = <div {...props} />;
let html = ReactDOMServer.renderToString(element);
```

In order to exploit it, the attacker would need to craft a special attribute name that triggers an [XSS](https://en.wikipedia.org/wiki/Cross-site_scripting) vulnerability. For example:

```
let userProvidedData = '></div><script>alert("hi")</script>';
```

In the vulnerable versions of `react-dom/server`, the output would let the attacker inject arbitrary markup:

```
<div ></div><script>alert("hi")</script>
```

In the versions after the vulnerability was [fixed](https://github.com/facebook/react/pull/13302) (and before it was introduced), attributes with invalid names are skipped:

```
<div></div>
```

You would also see a warning about an invalid attribute name.

Note that **we expect attribute names based on user input to be very rare in practice.** It doesn’t serve any common practical use case, and has other potential security implications that React can’t guard against.

## [](#installation)Installation

React v16.4.2 is available on the npm registry.

To install React 16 with Yarn, run:

```
yarn add react@^16.4.2 react-dom@^16.4.2
```

To install React 16 with npm, run:

```
npm install --save react@^16.4.2 react-dom@^16.4.2
```

We also provide UMD builds of React via a CDN:

```
<script crossorigin src="https://unpkg.com/react@16/umd/react.production.min.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@16/umd/react-dom.production.min.js"></script>
```

Refer to the documentation for [detailed installation instructions](/docs/installation.html).

## [](#changelog)Changelog

### [](#react-dom-server)React DOM Server

* Fix a potential XSS vulnerability when the attacker controls an attribute name (`CVE-2018-6341`). This fix is available in the latest `react-dom@16.4.2`, as well as in previous affected minor versions: `react-dom@16.0.1`, `react-dom@16.1.2`, `react-dom@16.2.1`, and `react-dom@16.3.3`. ([@gaearon](https://github.com/gaearon) in [#13302](https://github.com/facebook/react/pull/13302))
* Fix a crash in the server renderer when an attribute is called `hasOwnProperty`. This fix is only available in `react-dom@16.4.2`. ([@gaearon](https://github.com/gaearon) in [#13303](https://github.com/facebook/react/pull/13303))

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/blog/2018-08-01-react-v-16-4-2.md)

----
