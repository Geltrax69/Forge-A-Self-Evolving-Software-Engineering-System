url: https://18.react.dev/reference/react/memo
----

[API Reference](/reference/react)

[APIs](/reference/react/apis)

# memo[](#undefined "Link for this heading")

`memo` lets you skip re-rendering a component when its props are unchanged.

```
const MemoizedComponent = memo(SomeComponent, arePropsEqual?)
```


* [Troubleshooting](#troubleshooting)
  * [My component re-renders when a prop is an object, array, or function](#my-component-rerenders-when-a-prop-is-an-object-or-array)

***

## Reference[](#reference "Link for Reference ")

### `memo(Component, arePropsEqual?)`[](#memo "Link for this heading")

Wrap a component in `memo` to get a *memoized* version of that component. This memoized version of your component will usually not be re-rendered when its parent component is re-rendered as long as its props have not changed. But React may still re-render it: memoization is a performance optimization, not a guarantee.

```
import { memo } from 'react';



const SomeComponent = memo(function SomeComponent(props) {

  // ...

});
```

[See more examples below.](#usage)

#### Parameters[](#parameters "Link for Parameters ")

* `Component`: The component that you want to memoize. The `memo` does not modify this component, but returns a new, memoized component instead. Any valid React component, including functions and [`forwardRef`](/reference/react/forwardRef) components, is accepted.

* **optional** `arePropsEqual`: A function that accepts two arguments: the component’s previous props, and its new props. It should return `true` if the old and new props are equal: that is, if the component will render the same output and behave in the same way with the new props as with the old. Otherwise it should return `false`. Usually, you will not specify this function. By default, React will compare each prop with [`Object.is`.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is)

#### Returns[](#returns "Link for Returns ")

`memo` returns a new React component. It behaves the same as the component provided to `memo` except that React will not always re-render it when its parent is being re-rendered unless its props have changed.

***

## Usage[](#usage "Link for Usage ")

### Skipping re-rendering when props are unchanged[](#skipping-re-rendering-when-props-are-unchanged "Link for Skipping re-rendering when props are unchanged ")

React normally re-renders a component whenever its parent re-renders. With `memo`, you can create a component that React will not re-render when its parent re-renders so long as its new props are the same as the old props. Such a component is said to be *memoized*.

To memoize a component, wrap it in `memo` and use the value that it returns in place of your original component:

```
const Greeting = memo(function Greeting({ name }) {

  return <h1>Hello, {name}!</h1>;

});



export default Greeting;
```

A React component should always have [pure rendering logic.](/learn/keeping-components-pure) This means that it must return the same output if its props, state, and context haven’t changed. By using `memo`, you are telling React that your component complies with this requirement, so React doesn’t need to re-render as long as its props haven’t changed. Even with `memo`, your component will re-render if its own state changes or if a context that it’s using changes.

In this example, notice that the `Greeting` component re-renders whenever `name` is changed (because that’s one of its props), but not when `address` is changed (because it’s not passed to `Greeting` as a prop):

```
import { memo, useState } from 'react';

export default function MyApp() {
  const [name, setName] = useState('');
  const [address, setAddress] = useState('');
  return (
    <>
      <label>
        Name{': '}
        <input value={name} onChange={e => setName(e.target.value)} />
      </label>
      <label>
        Address{': '}
        <input value={address} onChange={e => setAddress(e.target.value)} />
      </label>
      <Greeting name={name} />
    </>
  );
}

const Greeting = memo(function Greeting({ name }) {
  console.log("Greeting was rendered at", new Date().toLocaleTimeString());
  return <h3>Hello{name && ', '}{name}!</h3>;
});
```

***

### Updating a memoized component using state[](#updating-a-memoized-component-using-state "Link for Updating a memoized component using state ")

Even when a component is memoized, it will still re-render when its own state changes. Memoization only has to do with props that are passed to the component from its parent.

```
import { memo, useState } from 'react';

export default function MyApp() {
  const [name, setName] = useState('');
  const [address, setAddress] = useState('');
  return (
    <>
      <label>
        Name{': '}
        <input value={name} onChange={e => setName(e.target.value)} />
      </label>
      <label>
        Address{': '}
        <input value={address} onChange={e => setAddress(e.target.value)} />
      </label>
      <Greeting name={name} />
    </>
  );
}

const Greeting = memo(function Greeting({ name }) {
  console.log('Greeting was rendered at', new Date().toLocaleTimeString());
  const [greeting, setGreeting] = useState('Hello');
  return (
    <>
      <h3>{greeting}{name && ', '}{name}!</h3>
      <GreetingSelector value={greeting} onChange={setGreeting} />
    </>
  );
});

function GreetingSelector({ value, onChange }) {
  return (
    <>
      <label>
        <input
          type="radio"
          checked={value === 'Hello'}
          onChange={e => onChange('Hello')}
        />
        Regular greeting
      </label>
      <label>
        <input
          type="radio"
          checked={value === 'Hello and welcome'}
          onChange={e => onChange('Hello and welcome')}
        />
        Enthusiastic greeting
      </label>
    </>
  );
}
```

If you set a state variable to its current value, React will skip re-rendering your component even without `memo`. You may still see your component function being called an extra time, but the result will be discarded.

***

### Updating a memoized component using a context[](#updating-a-memoized-component-using-a-context "Link for Updating a memoized component using a context ")

Even when a component is memoized, it will still re-render when a context that it’s using changes. Memoization only has to do with props that are passed to the component from its parent.

```
import { createContext, memo, useContext, useState } from 'react';

const ThemeContext = createContext(null);

export default function MyApp() {
  const [theme, setTheme] = useState('dark');

  function handleClick() {
    setTheme(theme === 'dark' ? 'light' : 'dark'); 
  }

  return (
    <ThemeContext.Provider value={theme}>
      <button onClick={handleClick}>
        Switch theme
      </button>
      <Greeting name="Taylor" />
    </ThemeContext.Provider>
  );
}

const Greeting = memo(function Greeting({ name }) {
  console.log("Greeting was rendered at", new Date().toLocaleTimeString());
  const theme = useContext(ThemeContext);
  return (
    <h3 className={theme}>Hello, {name}!</h3>
  );
});
```

To make your component re-render only when a *part* of some context changes, split your component in two. Read what you need from the context in the outer component, and pass it down to a memoized child as a prop.

***

### Minimizing props changes[](#minimizing-props-changes "Link for Minimizing props changes ")

When you use `memo`, your component re-renders whenever any prop is not *shallowly equal* to what it was previously. This means that React compares every prop in your component with its previous value using the [`Object.is`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) comparison. Note that `Object.is(3, 3)` is `true`, but `Object.is({}, {})` is `false`.

To get the most out of `memo`, minimize the times that the props change. For example, if the prop is an object, prevent the parent component from re-creating that object every time by using [`useMemo`:](/reference/react/useMemo)

```
function Page() {

  const [name, setName] = useState('Taylor');

  const [age, setAge] = useState(42);



  const person = useMemo(

    () => ({ name, age }),

    [name, age]

  );



  return <Profile person={person} />;

}



const Profile = memo(function Profile({ person }) {

  // ...

});
```

A better way to minimize props changes is to make sure the component accepts the minimum necessary information in its props. For example, it could accept individual values instead of a whole object:

```
function Page() {

  const [name, setName] = useState('Taylor');

  const [age, setAge] = useState(42);

  return <Profile name={name} age={age} />;

}



const Profile = memo(function Profile({ name, age }) {

  // ...

});
```

Even individual values can sometimes be projected to ones that change less frequently. For example, here a component accepts a boolean indicating the presence of a value rather than the value itself:

```
function GroupsLanding({ person }) {

  const hasGroups = person.groups !== null;

  return <CallToAction hasGroups={hasGroups} />;

}



const CallToAction = memo(function CallToAction({ hasGroups }) {

  // ...

});
```

When you need to pass a function to memoized component, either declare it outside your component so that it never changes, or [`useCallback`](/reference/react/useCallback#skipping-re-rendering-of-components) to cache its definition between re-renders.

***

### Specifying a custom comparison function[](#specifying-a-custom-comparison-function "Link for Specifying a custom comparison function ")

In rare cases it may be infeasible to minimize the props changes of a memoized component. In that case, you can provide a custom comparison function, which React will use to compare the old and new props instead of using shallow equality. This function is passed as a second argument to `memo`. It should return `true` only if the new props would result in the same output as the old props; otherwise it should return `false`.

```
const Chart = memo(function Chart({ dataPoints }) {

  // ...

}, arePropsEqual);



function arePropsEqual(oldProps, newProps) {

  return (

    oldProps.dataPoints.length === newProps.dataPoints.length &&

    oldProps.dataPoints.every((oldPoint, index) => {

      const newPoint = newProps.dataPoints[index];

      return oldPoint.x === newPoint.x && oldPoint.y === newPoint.y;

    })

  );

}
```

If you do this, use the Performance panel in your browser developer tools to make sure that your comparison function is actually faster than re-rendering the component. You might be surprised.

When you do performance measurements, make sure that React is running in the production mode.

### Pitfall

If you provide a custom `arePropsEqual` implementation, **you must compare every prop, including functions.** Functions often [close over](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures) the props and state of parent components. If you return `true` when `oldProps.onClick !== newProps.onClick`, your component will keep “seeing” the props and state from a previous render inside its `onClick` handler, leading to very confusing bugs.

Avoid doing deep equality checks inside `arePropsEqual` unless you are 100% sure that the data structure you’re working with has a known limited depth. **Deep equality checks can become incredibly slow** and can freeze your app for many seconds if someone changes the data structure later.

***

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### My component re-renders when a prop is an object, array, or function[](#my-component-rerenders-when-a-prop-is-an-object-or-array "Link for My component re-renders when a prop is an object, array, or function ")

React compares old and new props by shallow equality: that is, it considers whether each new prop is reference-equal to the old prop. If you create a new object or array each time the parent is re-rendered, even if the individual elements are each the same, React will still consider it to be changed. Similarly, if you create a new function when rendering the parent component, React will consider it to have changed even if the function has the same definition. To avoid this, [simplify props or memoize props in the parent component](#minimizing-props-changes).

[Previouslazy](/reference/react/lazy)

[NextstartTransition](/reference/react/startTransition)

***

----
