url: https://18.react.dev/reference/react/Profiler
----

[API Reference](/reference/react)

[Components](/reference/react/components)

# \<Profiler>[](#undefined "Link for this heading")

`<Profiler>` lets you measure rendering performance of a React tree programmatically.

```
<Profiler id="App" onRender={onRender}>

  <App />

</Profiler>
```

* [Reference](#reference)

  * [`<Profiler>`](#profiler)
  * [`onRender` callback](#onrender-callback)

* [Usage](#usage)

  * [Measuring rendering performance programmatically](#measuring-rendering-performance-programmatically)
  * [Measuring different parts of the application](#measuring-different-parts-of-the-application)

***

## Reference[](#reference "Link for Reference ")

### `<Profiler>`[](#profiler "Link for this heading")

Wrap a component tree in a `<Profiler>` to measure its rendering performance.

```
<Profiler id="App" onRender={onRender}>

  <App />

</Profiler>
```

#### Props[](#props "Link for Props ")

* `id`: A string identifying the part of the UI you are measuring.
* `onRender`: An [`onRender` callback](#onrender-callback) that React calls every time components within the profiled tree update. It receives information about what was rendered and how much time it took.

#### Caveats[](#caveats "Link for Caveats ")

* Profiling adds some additional overhead, so **it is disabled in the production build by default.** To opt into production profiling, you need to enable a [special production build with profiling enabled.](https://fb.me/react-profiling)

***

### `onRender` callback[](#onrender-callback "Link for this heading")

React will call your `onRender` callback with information about what was rendered.

```
function onRender(id, phase, actualDuration, baseDuration, startTime, commitTime) {

  // Aggregate or log render timings...

}
```

***

## Usage[](#usage "Link for Usage ")

### Measuring rendering performance programmatically[](#measuring-rendering-performance-programmatically "Link for Measuring rendering performance programmatically ")

Wrap the `<Profiler>` component around a React tree to measure its rendering performance.

```
<App>

  <Profiler id="Sidebar" onRender={onRender}>

    <Sidebar />

  </Profiler>

  <PageContent />

</App>
```

It requires two props: an `id` (string) and an `onRender` callback (function) which React calls any time a component within the tree “commits” an update.

### Pitfall

Profiling adds some additional overhead, so **it is disabled in the production build by default.** To opt into production profiling, you need to enable a [special production build with profiling enabled.](https://fb.me/react-profiling)

### Note

`<Profiler>` lets you gather measurements programmatically. If you’re looking for an interactive profiler, try the Profiler tab in [React Developer Tools](/learn/react-developer-tools). It exposes similar functionality as a browser extension.

***

### Measuring different parts of the application[](#measuring-different-parts-of-the-application "Link for Measuring different parts of the application ")

You can use multiple `<Profiler>` components to measure different parts of your application:

```
<App>

  <Profiler id="Sidebar" onRender={onRender}>

    <Sidebar />

  </Profiler>

  <Profiler id="Content" onRender={onRender}>

    <Content />

  </Profiler>

</App>
```

You can also nest `<Profiler>` components:

```
<App>

  <Profiler id="Sidebar" onRender={onRender}>

    <Sidebar />

  </Profiler>

  <Profiler id="Content" onRender={onRender}>

    <Content>

      <Profiler id="Editor" onRender={onRender}>

        <Editor />

      </Profiler>

      <Preview />

    </Content>

  </Profiler>

</App>
```

Although `<Profiler>` is a lightweight component, it should be used only when necessary. Each use adds some CPU and memory overhead to an application.

***

[Previous\<Fragment> (<>)](/reference/react/Fragment)

[Next\<StrictMode>](/reference/react/StrictMode)

***

----
