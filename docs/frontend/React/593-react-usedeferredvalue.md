url: https://18.react.dev/reference/react/useDeferredValue
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useDeferredValue[](#undefined "Link for this heading")

`useDeferredValue` is a React Hook that lets you defer updating a part of the UI.

```
const deferredValue = useDeferredValue(value)
```

* [Reference](#reference)
  * [`useDeferredValue(value, initialValue?)`](#usedeferredvalue)

* [Usage](#usage)

  * [Showing stale content while fresh content is loading](#showing-stale-content-while-fresh-content-is-loading)
  * [Indicating that the content is stale](#indicating-that-the-content-is-stale)
  * [Deferring re-rendering for a part of the UI](#deferring-re-rendering-for-a-part-of-the-ui)

***

## Reference[](#reference "Link for Reference ")

### `useDeferredValue(value, initialValue?)`[](#usedeferredvalue "Link for this heading")

Call `useDeferredValue` at the top level of your component to get a deferred version of that value.

```
import { useState, useDeferredValue } from 'react';



function SearchPage() {

  const [query, setQuery] = useState('');

  const deferredQuery = useDeferredValue(query);

  // ...

}
```

[See more examples below.](#usage)

#### Parameters[](#parameters "Link for Parameters ")

* `value`: The value you want to defer. It can have any type.
* Canary only **optional** `initialValue`: A value to use during the initial render of a component. If this option is omitted, `useDeferredValue` will not defer during the initial render, because there’s no previous version of `value` that it can render instead.

#### Returns[](#returns "Link for Returns ")

* `currentValue`: During the initial render, the returned deferred value will be the same as the value you provided. During updates, React will first attempt a re-render with the old value (so it will return the old value), and then try another re-render in the background with the new value (so it will return the updated value).

### Canary

In the latest React Canary versions, `useDeferredValue` returns the `initialValue` on initial render, and schedules a re-render in the background with the `value` returned.

***

## Usage[](#usage "Link for Usage ")

### Showing stale content while fresh content is loading[](#showing-stale-content-while-fresh-content-is-loading "Link for Showing stale content while fresh content is loading ")

Call `useDeferredValue` at the top level of your component to defer updating some part of your UI.

```
import { useState, useDeferredValue } from 'react';



function SearchPage() {

  const [query, setQuery] = useState('');

  const deferredQuery = useDeferredValue(query);

  // ...

}
```

During the initial render, the deferred value will be the same as the value you provided.

During updates, the deferred value will “lag behind” the latest value. In particular, React will first re-render *without* updating the deferred value, and then try to re-render with the newly received value in the background.

**Let’s walk through an example to see when this is useful.**

### Note

This example assumes you use a Suspense-enabled data source:

* Data fetching with Suspense-enabled frameworks like [Relay](https://relay.dev/docs/guided-tour/rendering/loading-states/) and [Next.js](https://nextjs.org/docs/getting-started/react-essentials)
* Lazy-loading component code with [`lazy`](/reference/react/lazy)
* Reading the value of a Promise with [`use`](/reference/react/use)

[Learn more about Suspense and its limitations.](/reference/react/Suspense)

In this example, the `SearchResults` component [suspends](/reference/react/Suspense#displaying-a-fallback-while-content-is-loading) while fetching the search results. Try typing `"a"`, waiting for the results, and then editing it to `"ab"`. The results for `"a"` get replaced by the loading fallback.

```
import { Suspense, useState } from 'react';
import SearchResults from './SearchResults.js';

export default function App() {
  const [query, setQuery] = useState('');
  return (
    <>
      <label>
        Search albums:
        <input value={query} onChange={e => setQuery(e.target.value)} />
      </label>
      <Suspense fallback={<h2>Loading...</h2>}>
        <SearchResults query={query} />
      </Suspense>
    </>
  );
}
```

A common alternative UI pattern is to *defer* updating the list of results and to keep showing the previous results until the new results are ready. Call `useDeferredValue` to pass a deferred version of the query down:

```
export default function App() {

  const [query, setQuery] = useState('');

  const deferredQuery = useDeferredValue(query);

  return (

    <>

      <label>

        Search albums:

        <input value={query} onChange={e => setQuery(e.target.value)} />

      </label>

      <Suspense fallback={<h2>Loading...</h2>}>

        <SearchResults query={deferredQuery} />

      </Suspense>

    </>

  );

}
```

The `query` will update immediately, so the input will display the new value. However, the `deferredQuery` will keep its previous value until the data has loaded, so `SearchResults` will show the stale results for a bit.

Enter `"a"` in the example below, wait for the results to load, and then edit the input to `"ab"`. Notice how instead of the Suspense fallback, you now see the stale result list until the new results have loaded:

```
import { Suspense, useState, useDeferredValue } from 'react';
import SearchResults from './SearchResults.js';

export default function App() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  return (
    <>
      <label>
        Search albums:
        <input value={query} onChange={e => setQuery(e.target.value)} />
      </label>
      <Suspense fallback={<h2>Loading...</h2>}>
        <SearchResults query={deferredQuery} />
      </Suspense>
    </>
  );
}
```

##### Deep Dive#### How does deferring a value work under the hood?[](#how-does-deferring-a-value-work-under-the-hood "Link for How does deferring a value work under the hood? ")

You can think of it as happening in two steps:

1. **First, React re-renders with the new `query` (`"ab"`) but with the old `deferredQuery` (still `"a")`.** The `deferredQuery` value, which you pass to the result list, is *deferred:* it “lags behind” the `query` value.

2. **In the background, React tries to re-render with *both* `query` and `deferredQuery` updated to `"ab"`.** If this re-render completes, React will show it on the screen. However, if it suspends (the results for `"ab"` have not loaded yet), React will abandon this rendering attempt, and retry this re-render again after the data has loaded. The user will keep seeing the stale deferred value until the data is ready.

The deferred “background” rendering is interruptible. For example, if you type into the input again, React will abandon it and restart with the new value. React will always use the latest provided value.

Note that there is still a network request per each keystroke. What’s being deferred here is displaying results (until they’re ready), not the network requests themselves. Even if the user continues typing, responses for each keystroke get cached, so pressing Backspace is instant and doesn’t fetch again.

***

### Indicating that the content is stale[](#indicating-that-the-content-is-stale "Link for Indicating that the content is stale ")

In the example above, there is no indication that the result list for the latest query is still loading. This can be confusing to the user if the new results take a while to load. To make it more obvious to the user that the result list does not match the latest query, you can add a visual indication when the stale result list is displayed:

```
<div style={{

  opacity: query !== deferredQuery ? 0.5 : 1,

}}>

  <SearchResults query={deferredQuery} />

</div>
```

With this change, as soon as you start typing, the stale result list gets slightly dimmed until the new result list loads. You can also add a CSS transition to delay dimming so that it feels gradual, like in the example below:

```
import { Suspense, useState, useDeferredValue } from 'react';
import SearchResults from './SearchResults.js';

export default function App() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;
  return (
    <>
      <label>
        Search albums:
        <input value={query} onChange={e => setQuery(e.target.value)} />
      </label>
      <Suspense fallback={<h2>Loading...</h2>}>
        <div style={{
          opacity: isStale ? 0.5 : 1,
          transition: isStale ? 'opacity 0.2s 0.2s linear' : 'opacity 0s 0s linear'
        }}>
          <SearchResults query={deferredQuery} />
        </div>
      </Suspense>
    </>
  );
}
```

***

### Deferring re-rendering for a part of the UI[](#deferring-re-rendering-for-a-part-of-the-ui "Link for Deferring re-rendering for a part of the UI ")

You can also apply `useDeferredValue` as a performance optimization. It is useful when a part of your UI is slow to re-render, there’s no easy way to optimize it, and you want to prevent it from blocking the rest of the UI.

Imagine you have a text field and a component (like a chart or a long list) that re-renders on every keystroke:

```
function App() {

  const [text, setText] = useState('');

  return (

    <>

      <input value={text} onChange={e => setText(e.target.value)} />

      <SlowList text={text} />

    </>

  );

}
```

First, optimize `SlowList` to skip re-rendering when its props are the same. To do this, [wrap it in `memo`:](/reference/react/memo#skipping-re-rendering-when-props-are-unchanged)

```
const SlowList = memo(function SlowList({ text }) {

  // ...

});
```

However, this only helps if the `SlowList` props are *the same* as during the previous render. The problem you’re facing now is that it’s slow when they’re *different,* and when you actually need to show different visual output.

Concretely, the main performance problem is that whenever you type into the input, the `SlowList` receives new props, and re-rendering its entire tree makes the typing feel janky. In this case, `useDeferredValue` lets you prioritize updating the input (which must be fast) over updating the result list (which is allowed to be slower):

```
function App() {

  const [text, setText] = useState('');

  const deferredText = useDeferredValue(text);

  return (

    <>

      <input value={text} onChange={e => setText(e.target.value)} />

      <SlowList text={deferredText} />

    </>

  );

}
```

This does not make re-rendering of the `SlowList` faster. However, it tells React that re-rendering the list can be deprioritized so that it doesn’t block the keystrokes. The list will “lag behind” the input and then “catch up”. Like before, React will attempt to update the list as soon as possible, but will not block the user from typing.

#### The difference between useDeferredValue and unoptimized re-rendering[](#examples "Link for The difference between useDeferredValue and unoptimized re-rendering")

#### Example 1 of 2:Deferred re-rendering of the list[](#deferred-re-rendering-of-the-list "Link for this heading")

In this example, each item in the `SlowList` component is **artificially slowed down** so that you can see how `useDeferredValue` lets you keep the input responsive. Type into the input and notice that typing feels snappy while the list “lags behind” it.

```
import { useState, useDeferredValue } from 'react';
import SlowList from './SlowList.js';

export default function App() {
  const [text, setText] = useState('');
  const deferredText = useDeferredValue(text);
  return (
    <>
      <input value={text} onChange={e => setText(e.target.value)} />
      <SlowList text={deferredText} />
    </>
  );
}
```

***