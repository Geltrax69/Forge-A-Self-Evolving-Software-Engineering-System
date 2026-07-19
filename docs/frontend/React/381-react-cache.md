url: https://18.react.dev/reference/react/cache
----

[API Reference](/reference/react)

[APIs](/reference/react/apis)

# cache[](#undefined "Link for this heading")

### Canary

* `cache` is only for use with [React Server Components](/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-server-components). See [frameworks](/learn/start-a-new-react-project#bleeding-edge-react-frameworks) that support React Server Components.

* `cache` is only available in React’s [Canary](/community/versioning-policy#canary-channel) and [experimental](/community/versioning-policy#experimental-channel) channels. Please ensure you understand the limitations before using `cache` in production. Learn more about [React’s release channels here](/community/versioning-policy#all-release-channels).

`cache` lets you cache the result of a data fetch or computation.

```
const cachedFn = cache(fn);
```

***

## Reference[](#reference "Link for Reference ")

### `cache(fn)`[](#cache "Link for this heading")

Call `cache` outside of any components to create a version of the function with caching.

```
import {cache} from 'react';

import calculateMetrics from 'lib/metrics';



const getMetrics = cache(calculateMetrics);



function Chart({data}) {

  const report = getMetrics(data);

  // ...

}
```

* `cache` is for use in [Server Components](/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-server-components) only.

***

## Usage[](#usage "Link for Usage ")

### Cache an expensive computation[](#cache-expensive-computation "Link for Cache an expensive computation ")

Use `cache` to skip duplicate work.

```
import {cache} from 'react';

import calculateUserMetrics from 'lib/user';



const getUserMetrics = cache(calculateUserMetrics);



function Profile({user}) {

  const metrics = getUserMetrics(user);

  // ...

}



function TeamReport({users}) {

  for (let user in users) {

    const metrics = getUserMetrics(user);

    // ...

  }

  // ...

}
```

If the same `user` object is rendered in both `Profile` and `TeamReport`, the two components can share work and only call `calculateUserMetrics` once for that `user`.

Assume `Profile` is rendered first. It will call `getUserMetrics`, and check if there is a cached result. Since it is the first time `getUserMetrics` is called with that `user`, there will be a cache miss. `getUserMetrics` will then call `calculateUserMetrics` with that `user` and write the result to cache.

When `TeamReport` renders its list of `users` and reaches the same `user` object, it will call `getUserMetrics` and read the result from cache.

### Pitfall

##### Calling different memoized functions will read from different caches.[](#pitfall-different-memoized-functions "Link for Calling different memoized functions will read from different caches. ")

To access the same cache, components must call the same memoized function.

```
// Temperature.js

import {cache} from 'react';

import {calculateWeekReport} from './report';



export function Temperature({cityData}) {

  // 🚩 Wrong: Calling `cache` in component creates new `getWeekReport` for each render

  const getWeekReport = cache(calculateWeekReport);

  const report = getWeekReport(cityData);

  // ...

}
```

```
// Precipitation.js

import {cache} from 'react';

import {calculateWeekReport} from './report';



// 🚩 Wrong: `getWeekReport` is only accessible for `Precipitation` component.

const getWeekReport = cache(calculateWeekReport);



export function Precipitation({cityData}) {

  const report = getWeekReport(cityData);

  // ...

}
```

In the above example, `Precipitation` and `Temperature` each call `cache` to create a new memoized function with their own cache look-up. If both components render for the same `cityData`, they will do duplicate work to call `calculateWeekReport`.

In addition, `Temperature` creates a new memoized function each time the component is rendered which doesn’t allow for any cache sharing.

To maximize cache hits and reduce work, the two components should call the same memoized function to access the same cache. Instead, define the memoized function in a dedicated module that can be [`import`-ed](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) across components.

```
// getWeekReport.js

import {cache} from 'react';

import {calculateWeekReport} from './report';



export default cache(calculateWeekReport);
```

```
// Temperature.js

import getWeekReport from './getWeekReport';



export default function Temperature({cityData}) {

	const report = getWeekReport(cityData);

  // ...

}
```

```
// Precipitation.js

import getWeekReport from './getWeekReport';



export default function Precipitation({cityData}) {

  const report = getWeekReport(cityData);

  // ...

}
```

Here, both components call the same memoized function exported from `./getWeekReport.js` to read and write to the same cache.

### Share a snapshot of data[](#take-and-share-snapshot-of-data "Link for Share a snapshot of data ")

To share a snapshot of data between components, call `cache` with a data-fetching function like `fetch`. When multiple components make the same data fetch, only one request is made and the data returned is cached and shared across components. All components refer to the same snapshot of data across the server render.

```
import {cache} from 'react';

import {fetchTemperature} from './api.js';



const getTemperature = cache(async (city) => {

	return await fetchTemperature(city);

});



async function AnimatedWeatherCard({city}) {

	const temperature = await getTemperature(city);

	// ...

}



async function MinimalWeatherCard({city}) {

	const temperature = await getTemperature(city);

	// ...

}
```

If `AnimatedWeatherCard` and `MinimalWeatherCard` both render for the same city, they will receive the same snapshot of data from the memoized function.

If `AnimatedWeatherCard` and `MinimalWeatherCard` supply different city arguments to `getTemperature`, then `fetchTemperature` will be called twice and each call site will receive different data.

The city acts as a cache key.

### Note

Asynchronous rendering is only supported for Server Components.

```
async function AnimatedWeatherCard({city}) {

	const temperature = await getTemperature(city);

	// ...

}
```

### Preload data[](#preload-data "Link for Preload data ")

By caching a long-running data fetch, you can kick off asynchronous work prior to rendering the component.

```
const getUser = cache(async (id) => {

  return await db.user.query(id);

});



async function Profile({id}) {

  const user = await getUser(id);

  return (

    <section>

      <img src={user.profilePic} />

      <h2>{user.name}</h2>

    </section>

  );

}



function Page({id}) {

  // ✅ Good: start fetching the user data

  getUser(id);

  // ... some computational work

  return (

    <>

      <Profile id={id} />

    </>

  );

}
```

When rendering `Page`, the component calls `getUser` but note that it doesn’t use the returned data. This early `getUser` call kicks off the asynchronous database query that occurs while `Page` is doing other computational work and rendering children.

When rendering `Profile`, we call `getUser` again. If the initial `getUser` call has already returned and cached the user data, when `Profile` asks and waits for this data, it can simply read from the cache without requiring another remote procedure call. If the initial data request hasn’t been completed, preloading data in this pattern reduces delay in data-fetching.

##### Deep Dive#### Caching asynchronous work[](#caching-asynchronous-work "Link for Caching asynchronous work ")

When evaluating an [asynchronous function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function), you will receive a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) for that work. The promise holds the state of that work (*pending*, *fulfilled*, *failed*) and its eventual settled result.

In this example, the asynchronous function `fetchData` returns a promise that is awaiting the `fetch`.

```
async function fetchData() {

  return await fetch(`https://...`);

}



const getData = cache(fetchData);



async function MyComponent() {

  getData();

  // ... some computational work  

  await getData();

  // ...

}
```

In calling `getData` the first time, the promise returned from `fetchData` is cached. Subsequent look-ups will then return the same promise.

Notice that the first `getData` call does not `await` whereas the second does. [`await`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await) is a JavaScript operator that will wait and return the settled result of the promise. The first `getData` call simply initiates the `fetch` to cache the promise for the second `getData` to look-up.

If by the second call the promise is still *pending*, then `await` will pause for the result. The optimization is that while we wait on the `fetch`, React can continue with computational work, thus reducing the wait time for the second call.

If the promise is already settled, either to an error or the *fulfilled* result, `await` will return that value immediately. In both outcomes, there is a performance benefit.

### Pitfall

##### Calling a memoized function outside of a component will not use the cache.[](#pitfall-memoized-call-outside-component "Link for Calling a memoized function outside of a component will not use the cache. ")

```
import {cache} from 'react';



const getUser = cache(async (userId) => {

  return await db.user.query(userId);

});



// 🚩 Wrong: Calling memoized function outside of component will not memoize.

getUser('demo-id');



async function DemoProfile() {

  // ✅ Good: `getUser` will memoize.

  const user = await getUser('demo-id');

  return <Profile user={user} />;

}
```

React only provides cache access to the memoized function in a component. When calling `getUser` outside of a component, it will still evaluate the function but not read or update the cache.

This is because cache access is provided through a [context](/learn/passing-data-deeply-with-context) which is only accessible from a component.

##### Deep Dive#### When should I use `cache`, [`memo`](/reference/react/memo), or [`useMemo`](/reference/react/useMemo)?[](#cache-memo-usememo "Link for this heading")

All mentioned APIs offer memoization but the difference is what they’re intended to memoize, who can access the cache, and when their cache is invalidated.

#### `useMemo`[](#deep-dive-use-memo "Link for this heading")

In general, you should use [`useMemo`](/reference/react/useMemo) for caching a expensive computation in a Client Component across renders. As an example, to memoize a transformation of data within a component.

```
'use client';



function WeatherReport({record}) {

  const avgTemp = useMemo(() => calculateAvg(record), record);

  // ...

}



function App() {

  const record = getRecord();

  return (

    <>

      <WeatherReport record={record} />

      <WeatherReport record={record} />

    </>

  );

}
```

In this example, `App` renders two `WeatherReport`s with the same record. Even though both components do the same work, they cannot share work. `useMemo`’s cache is only local to the component.

However, `useMemo` does ensure that if `App` re-renders and the `record` object doesn’t change, each component instance would skip work and use the memoized value of `avgTemp`. `useMemo` will only cache the last computation of `avgTemp` with the given dependencies.

#### `cache`[](#deep-dive-cache "Link for this heading")

In general, you should use `cache` in Server Components to memoize work that can be shared across components.

```
const cachedFetchReport = cache(fetchReport);



function WeatherReport({city}) {

  const report = cachedFetchReport(city);

  // ...

}



function App() {

  const city = "Los Angeles";

  return (

    <>

      <WeatherReport city={city} />

      <WeatherReport city={city} />

    </>

  );

}
```

Re-writing the previous example to use `cache`, in this case the second instance of `WeatherReport` will be able to skip duplicate work and read from the same cache as the first `WeatherReport`. Another difference from the previous example is that `cache` is also recommended for memoizing data fetches, unlike `useMemo` which should only be used for computations.

At this time, `cache` should only be used in Server Components and the cache will be invalidated across server requests.

#### `memo`[](#deep-dive-memo "Link for this heading")

You should use [`memo`](/reference/react/memo) to prevent a component re-rendering if its props are unchanged.

```
'use client';



function WeatherReport({record}) {

  const avgTemp = calculateAvg(record); 

  // ...

}



const MemoWeatherReport = memo(WeatherReport);



function App() {

  const record = getRecord();

  return (

    <>

      <MemoWeatherReport record={record} />

      <MemoWeatherReport record={record} />

    </>

  );

}
```

In this example, both `MemoWeatherReport` components will call `calculateAvg` when first rendered. However, if `App` re-renders, with no changes to `record`, none of the props have changed and `MemoWeatherReport` will not re-render.

Compared to `useMemo`, `memo` memoizes the component render based on props vs. specific computations. Similar to `useMemo`, the memoized component only caches the last render with the last prop values. Once the props change, the cache invalidates and the component re-renders.

***

```
import {cache} from 'react';



const calculateNorm = cache((vector) => {

  // ...

});



function MapMarker(props) {

  // 🚩 Wrong: props is an object that changes every render.

  const length = calculateNorm(props);

  // ...

}



function App() {

  return (

    <>

      <MapMarker x={10} y={10} z={10} />

      <MapMarker x={10} y={10} z={10} />

    </>

  );

}
```

In this case the two `MapMarker`s look like they’re doing the same work and calling `calculateNorm` with the same value of `{x: 10, y: 10, z:10}`. Even though the objects contain the same values, they are not the same object reference as each component creates its own `props` object.

React will call [`Object.is`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) on the input to verify if there is a cache hit.

```
import {cache} from 'react';



const calculateNorm = cache((x, y, z) => {

  // ...

});



function MapMarker(props) {

  // ✅ Good: Pass primitives to memoized function

  const length = calculateNorm(props.x, props.y, props.z);

  // ...

}



function App() {

  return (

    <>

      <MapMarker x={10} y={10} z={10} />

      <MapMarker x={10} y={10} z={10} />

    </>

  );

}
```

One way to address this could be to pass the vector dimensions to `calculateNorm`. This works because the dimensions themselves are primitives.

Another solution may be to pass the vector object itself as a prop to the component. We’ll need to pass the same object to both component instances.

```
import {cache} from 'react';



const calculateNorm = cache((vector) => {

  // ...

});



function MapMarker(props) {

  // ✅ Good: Pass the same `vector` object

  const length = calculateNorm(props.vector);

  // ...

}



function App() {

  const vector = [10, 10, 10];

  return (

    <>

      <MapMarker vector={vector} />

      <MapMarker vector={vector} />

    </>

  );

}
```

[Previousact](/reference/react/act)

[NextcreateContext](/reference/react/createContext)

***

----
