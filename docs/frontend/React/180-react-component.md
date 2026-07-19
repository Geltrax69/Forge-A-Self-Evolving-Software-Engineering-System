url: https://18.react.dev/reference/react/Component
----

[API Reference](/reference/react)

[Legacy React APIs](/reference/react/legacy)

# Component[](#undefined "Link for this heading")

### Pitfall

We recommend defining components as functions instead of classes. [See how to migrate.](#alternatives)

`Component` is the base class for the React components defined as [JavaScript classes.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes) Class components are still supported by React, but we don’t recommend using them in new code.

```
class Greeting extends Component {

  render() {

    return <h1>Hello, {this.props.name}!</h1>;

  }

}
```

* [Reference](#reference)

  * [`Component`](#component)
  * [`context`](#context)
  * [`props`](#props)
  * [`refs`](#refs)
  * [`getChildContext()`](#getchildcontext)
  * [`static childContextTypes`](#static-childcontexttypes)
  * [`static contextTypes`](#static-contexttypes)
  * [`static contextType`](#static-contexttype)
  * [`static defaultProps`](#static-defaultprops)
  * [`static propTypes`](#static-proptypes)
  * [`static getDerivedStateFromError(error)`](#static-getderivedstatefromerror)
  * [`static getDerivedStateFromProps(props, state)`](#static-getderivedstatefromprops)

* [Usage](#usage)

  * [Defining a class component](#defining-a-class-component)
  * [Adding state to a class component](#adding-state-to-a-class-component)
  * [Adding lifecycle methods to a class component](#adding-lifecycle-methods-to-a-class-component)
  * [Catching rendering errors with an error boundary](#catching-rendering-errors-with-an-error-boundary)

* [Alternatives](#alternatives)

  * [Migrating a simple component from a class to a function](#migrating-a-simple-component-from-a-class-to-a-function)
  * [Migrating a component with state from a class to a function](#migrating-a-component-with-state-from-a-class-to-a-function)
  * [Migrating a component with lifecycle methods from a class to a function](#migrating-a-component-with-lifecycle-methods-from-a-class-to-a-function)
  * [Migrating a component with context from a class to a function](#migrating-a-component-with-context-from-a-class-to-a-function)

***

## Reference[](#reference "Link for Reference ")

### `Component`[](#component "Link for this heading")

To define a React component as a class, extend the built-in `Component` class and define a [`render` method:](#render)

```
import { Component } from 'react';



class Greeting extends Component {

  render() {

    return <h1>Hello, {this.props.name}!</h1>;

  }

}
```

Only the `render` method is required, other methods are optional.

[See more examples below.](#usage)

***

### `context`[](#context "Link for this heading")

The [context](/learn/passing-data-deeply-with-context) of a class component is available as `this.context`. It is only available if you specify *which* context you want to receive using [`static contextType`](#static-contexttype) (modern) or [`static contextTypes`](#static-contexttypes) (deprecated).

A class component can only read one context at a time.

```
class Button extends Component {

  static contextType = ThemeContext;



  render() {

    const theme = this.context;

    const className = 'button-' + theme;

    return (

      <button className={className}>

        {this.props.children}

      </button>

    );

  }

}
```

### Note

Reading `this.context` in class components is equivalent to [`useContext`](/reference/react/useContext) in function components.

[See how to migrate.](#migrating-a-component-with-context-from-a-class-to-a-function)

***

### `props`[](#props "Link for this heading")

The props passed to a class component are available as `this.props`.

```
class Greeting extends Component {

  render() {

    return <h1>Hello, {this.props.name}!</h1>;

  }

}



<Greeting name="Taylor" />
```

### Note

Reading `this.props` in class components is equivalent to [declaring props](/learn/passing-props-to-a-component#step-2-read-props-inside-the-child-component) in function components.

[See how to migrate.](#migrating-a-simple-component-from-a-class-to-a-function)

***

### `refs`[](#refs "Link for this heading")

### Deprecated

This API will be removed in a future major version of React. [Use `createRef` instead.](/reference/react/createRef)

Lets you access [legacy string refs](https://reactjs.org/docs/refs-and-the-dom.html#legacy-api-string-refs) for this component.

***

### `state`[](#state "Link for this heading")

The state of a class component is available as `this.state`. The `state` field must be an object. Do not mutate the state directly. If you wish to change the state, call `setState` with the new state.

```
class Counter extends Component {

  state = {

    age: 42,

  };



  handleAgeChange = () => {

    this.setState({

      age: this.state.age + 1 

    });

  };



  render() {

    return (

      <>

        <button onClick={this.handleAgeChange}>

        Increment age

        </button>

        <p>You are {this.state.age}.</p>

      </>

    );

  }

}
```

### Note

Defining `state` in class components is equivalent to calling [`useState`](/reference/react/useState) in function components.

[See how to migrate.](#migrating-a-component-with-state-from-a-class-to-a-function)

***

### `constructor(props)`[](#constructor "Link for this heading")

The [constructor](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/constructor) runs before your class component *mounts* (gets added to the screen). Typically, a constructor is only used for two purposes in React. It lets you declare state and [bind](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_objects/Function/bind) your class methods to the class instance:

```
class Counter extends Component {

  constructor(props) {

    super(props);

    this.state = { counter: 0 };

    this.handleClick = this.handleClick.bind(this);

  }



  handleClick() {

    // ...

  }
```

If you use modern JavaScript syntax, constructors are rarely needed. Instead, you can rewrite this code above using the [public class field syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Public_class_fields) which is supported both by modern browsers and tools like [Babel:](https://babeljs.io/)

```
class Counter extends Component {

  state = { counter: 0 };



  handleClick = () => {

    // ...

  }
```

***

### `componentDidCatch(error, info)`[](#componentdidcatch "Link for this heading")

If you define `componentDidCatch`, React will call it when some child component (including distant children) throws an error during rendering. This lets you log that error to an error reporting service in production.

Typically, it is used together with [`static getDerivedStateFromError`](#static-getderivedstatefromerror) which lets you update state in response to an error and display an error message to the user. A component with these methods is called an *error boundary.*

***

### `componentDidMount()`[](#componentdidmount "Link for this heading")

If you define the `componentDidMount` method, React will call it when your component is added *(mounted)* to the screen. This is a common place to start data fetching, set up subscriptions, or manipulate the DOM nodes.

If you implement `componentDidMount`, you usually need to implement other lifecycle methods to avoid bugs. For example, if `componentDidMount` reads some state or props, you also have to implement [`componentDidUpdate`](#componentdidupdate) to handle their changes, and [`componentWillUnmount`](#componentwillunmount) to clean up whatever `componentDidMount` was doing.

```
class ChatRoom extends Component {

  state = {

    serverUrl: 'https://localhost:1234'

  };



  componentDidMount() {

    this.setupConnection();

  }



  componentDidUpdate(prevProps, prevState) {

    if (

      this.props.roomId !== prevProps.roomId ||

      this.state.serverUrl !== prevState.serverUrl

    ) {

      this.destroyConnection();

      this.setupConnection();

    }

  }



  componentWillUnmount() {

    this.destroyConnection();

  }



  // ...

}
```

***

### `componentDidUpdate(prevProps, prevState, snapshot?)`[](#componentdidupdate "Link for this heading")

If you define the `componentDidUpdate` method, React will call it immediately after your component has been re-rendered with updated props or state. This method is not called for the initial render.

You can use it to manipulate the DOM after an update. This is also a common place to do network requests as long as you compare the current props to previous props (e.g. a network request may not be necessary if the props have not changed). Typically, you’d use it together with [`componentDidMount`](#componentdidmount) and [`componentWillUnmount`:](#componentwillunmount)

```
class ChatRoom extends Component {

  state = {

    serverUrl: 'https://localhost:1234'

  };



  componentDidMount() {

    this.setupConnection();

  }



  componentDidUpdate(prevProps, prevState) {

    if (

      this.props.roomId !== prevProps.roomId ||

      this.state.serverUrl !== prevState.serverUrl

    ) {

      this.destroyConnection();

      this.setupConnection();

    }

  }



  componentWillUnmount() {

    this.destroyConnection();

  }



  // ...

}
```

***

### `componentWillMount()`[](#componentwillmount "Link for this heading")

### Deprecated

This API has been renamed from `componentWillMount` to [`UNSAFE_componentWillMount`.](#unsafe_componentwillmount) The old name has been deprecated. In a future major version of React, only the new name will work.

Run the [`rename-unsafe-lifecycles` codemod](https://github.com/reactjs/react-codemod#rename-unsafe-lifecycles) to automatically update your components.

***

### `componentWillReceiveProps(nextProps)`[](#componentwillreceiveprops "Link for this heading")

### Deprecated

This API has been renamed from `componentWillReceiveProps` to [`UNSAFE_componentWillReceiveProps`.](#unsafe_componentwillreceiveprops) The old name has been deprecated. In a future major version of React, only the new name will work.

Run the [`rename-unsafe-lifecycles` codemod](https://github.com/reactjs/react-codemod#rename-unsafe-lifecycles) to automatically update your components.

***

### `componentWillUpdate(nextProps, nextState)`[](#componentwillupdate "Link for this heading")

### Deprecated

This API has been renamed from `componentWillUpdate` to [`UNSAFE_componentWillUpdate`.](#unsafe_componentwillupdate) The old name has been deprecated. In a future major version of React, only the new name will work.

Run the [`rename-unsafe-lifecycles` codemod](https://github.com/reactjs/react-codemod#rename-unsafe-lifecycles) to automatically update your components.

***

### `componentWillUnmount()`[](#componentwillunmount "Link for this heading")

If you define the `componentWillUnmount` method, React will call it before your component is removed *(unmounted)* from the screen. This is a common place to cancel data fetching or remove subscriptions.

The logic inside `componentWillUnmount` should “mirror” the logic inside [`componentDidMount`.](#componentdidmount) For example, if `componentDidMount` sets up a subscription, `componentWillUnmount` should clean up that subscription. If the cleanup logic in your `componentWillUnmount` reads some props or state, you will usually also need to implement [`componentDidUpdate`](#componentdidupdate) to clean up resources (such as subscriptions) corresponding to the old props and state.

```
class ChatRoom extends Component {

  state = {

    serverUrl: 'https://localhost:1234'

  };



  componentDidMount() {

    this.setupConnection();

  }



  componentDidUpdate(prevProps, prevState) {

    if (

      this.props.roomId !== prevProps.roomId ||

      this.state.serverUrl !== prevState.serverUrl

    ) {

      this.destroyConnection();

      this.setupConnection();

    }

  }



  componentWillUnmount() {

    this.destroyConnection();

  }



  // ...

}
```

***

***

### `getChildContext()`[](#getchildcontext "Link for this heading")

### Deprecated

This API will be removed in a future major version of React. [Use `Context.Provider` instead.](/reference/react/createContext#provider)

Lets you specify the values for the [legacy context](https://reactjs.org/docs/legacy-context.html) is provided by this component.

***

### `getSnapshotBeforeUpdate(prevProps, prevState)`[](#getsnapshotbeforeupdate "Link for this heading")

If you implement `getSnapshotBeforeUpdate`, React will call it immediately before React updates the DOM. It enables your component to capture some information from the DOM (e.g. scroll position) before it is potentially changed. Any value returned by this lifecycle method will be passed as a parameter to [`componentDidUpdate`.](#componentdidupdate)

For example, you can use it in a UI like a chat thread that needs to preserve its scroll position during updates:

```
class ScrollingList extends React.Component {

  constructor(props) {

    super(props);

    this.listRef = React.createRef();

  }



  getSnapshotBeforeUpdate(prevProps, prevState) {

    // Are we adding new items to the list?

    // Capture the scroll position so we can adjust scroll later.

    if (prevProps.list.length < this.props.list.length) {

      const list = this.listRef.current;

      return list.scrollHeight - list.scrollTop;

    }

    return null;

  }



  componentDidUpdate(prevProps, prevState, snapshot) {

    // If we have a snapshot value, we've just added new items.

    // Adjust scroll so these new items don't push the old ones out of view.

    // (snapshot here is the value returned from getSnapshotBeforeUpdate)

    if (snapshot !== null) {

      const list = this.listRef.current;

      list.scrollTop = list.scrollHeight - snapshot;

    }

  }



  render() {

    return (

      <div ref={this.listRef}>{/* ...contents... */}</div>

    );

  }

}
```

***

### `render()`[](#render "Link for this heading")

The `render` method is the only required method in a class component.

The `render` method should specify what you want to appear on the screen, for example:

```
import { Component } from 'react';



class Greeting extends Component {

  render() {

    return <h1>Hello, {this.props.name}!</h1>;

  }

}
```

***

### `setState(nextState, callback?)`[](#setstate "Link for this heading")

Call `setState` to update the state of your React component.

```
class Form extends Component {

  state = {

    name: 'Taylor',

  };



  handleNameChange = (e) => {

    const newName = e.target.value;

    this.setState({

      name: newName

    });

  }



  render() {

    return (

      <>

        <input value={this.state.name} onChange={this.handleNameChange} />

        <p>Hello, {this.state.name}.</p>

      </>

    );

  }

}
```

`setState` enqueues changes to the component state. It tells React that this component and its children need to re-render with the new state. This is the main way you’ll update the user interface in response to interactions.

### Pitfall

Calling `setState` **does not** change the current state in the already executing code:

```
function handleClick() {

  console.log(this.state.name); // "Taylor"

  this.setState({

    name: 'Robin'

  });

  console.log(this.state.name); // Still "Taylor"!

}
```

It only affects what `this.state` will return starting from the *next* render.

You can also pass a function to `setState`. It lets you update state based on the previous state:

```
  handleIncreaseAge = () => {

    this.setState(prevState => {

      return {

        age: prevState.age + 1

      };

    });

  }
```

***

### `shouldComponentUpdate(nextProps, nextState, nextContext)`[](#shouldcomponentupdate "Link for this heading")

If you define `shouldComponentUpdate`, React will call it to determine whether a re-render can be skipped.

If you are confident you want to write it by hand, you may compare `this.props` with `nextProps` and `this.state` with `nextState` and return `false` to tell React the update can be skipped.

```
class Rectangle extends Component {

  state = {

    isHovered: false

  };



  shouldComponentUpdate(nextProps, nextState) {

    if (

      nextProps.position.x === this.props.position.x &&

      nextProps.position.y === this.props.position.y &&

      nextProps.size.width === this.props.size.width &&

      nextProps.size.height === this.props.size.height &&

      nextState.isHovered === this.state.isHovered

    ) {

      // Nothing has changed, so a re-render is unnecessary

      return false;

    }

    return true;

  }



  // ...

}
```

React calls `shouldComponentUpdate` before rendering when new props or state are being received. Defaults to `true`. This method is not called for the initial render or when [`forceUpdate`](#forceupdate) is used.

#### Parameters[](#shouldcomponentupdate-parameters "Link for Parameters ")

* `nextProps`: The next props that the component is about to render with. Compare `nextProps` to [`this.props`](#props) to determine what changed.
* `nextState`: The next state that the component is about to render with. Compare `nextState` to [`this.state`](#props) to determine what changed.
* `nextContext`: The next context that the component is about to render with. Compare `nextContext` to [`this.context`](#context) to determine what changed. Only available if you specify [`static contextType`](#static-contexttype) (modern) or [`static contextTypes`](#static-contexttypes) (legacy).

***

***

* `nextContext`: The next context that the component is about to receive from the closest provider. Compare `nextContext` to [`this.context`](#context) to determine what changed. Only available if you specify [`static contextType`](#static-contexttype) (modern) or [`static contextTypes`](#static-contexttypes) (legacy).

***

***

### `static childContextTypes`[](#static-childcontexttypes "Link for this heading")

### Deprecated

This API will be removed in a future major version of React. [Use `static contextType` instead.](#static-contexttype)

Lets you specify which [legacy context](https://reactjs.org/docs/legacy-context.html) is provided by this component.

***

### `static contextTypes`[](#static-contexttypes "Link for this heading")

### Deprecated

This API will be removed in a future major version of React. [Use `static contextType` instead.](#static-contexttype)

Lets you specify which [legacy context](https://reactjs.org/docs/legacy-context.html) is consumed by this component.

***

### `static contextType`[](#static-contexttype "Link for this heading")

If you want to read [`this.context`](#context-instance-field) from your class component, you must specify which context it needs to read. The context you specify as the `static contextType` must be a value previously created by [`createContext`.](/reference/react/createContext)

```
class Button extends Component {

  static contextType = ThemeContext;



  render() {

    const theme = this.context;

    const className = 'button-' + theme;

    return (

      <button className={className}>

        {this.props.children}

      </button>

    );

  }

}
```

### Note

Reading `this.context` in class components is equivalent to [`useContext`](/reference/react/useContext) in function components.

[See how to migrate.](#migrating-a-component-with-context-from-a-class-to-a-function)

***

### `static defaultProps`[](#static-defaultprops "Link for this heading")

You can define `static defaultProps` to set the default props for the class. They will be used for `undefined` and missing props, but not for `null` props.

For example, here is how you define that the `color` prop should default to `'blue'`:

```
class Button extends Component {

  static defaultProps = {

    color: 'blue'

  };



  render() {

    return <button className={this.props.color}>click me</button>;

  }

}
```

If the `color` prop is not provided or is `undefined`, it will be set by default to `'blue'`:

```
<>

  {/* this.props.color is "blue" */}

  <Button />



  {/* this.props.color is "blue" */}

  <Button color={undefined} />



  {/* this.props.color is null */}

  <Button color={null} />



  {/* this.props.color is "red" */}

  <Button color="red" />

</>
```

### Note

Defining `defaultProps` in class components is similar to using [default values](/learn/passing-props-to-a-component#specifying-a-default-value-for-a-prop) in function components.

***

### `static propTypes`[](#static-proptypes "Link for this heading")

You can define `static propTypes` together with the [`prop-types`](https://www.npmjs.com/package/prop-types) library to declare the types of the props accepted by your component. These types will be checked during rendering and in development only.

```
import PropTypes from 'prop-types';



class Greeting extends React.Component {

  static propTypes = {

    name: PropTypes.string

  };



  render() {

    return (

      <h1>Hello, {this.props.name}</h1>

    );

  }

}
```

### Note

We recommend using [TypeScript](https://www.typescriptlang.org/) instead of checking prop types at runtime.

***

### `static getDerivedStateFromError(error)`[](#static-getderivedstatefromerror "Link for this heading")

If you define `static getDerivedStateFromError`, React will call it when a child component (including distant children) throws an error during rendering. This lets you display an error message instead of clearing the UI.

Typically, it is used together with [`componentDidCatch`](#componentdidcatch) which lets you send the error report to some analytics service. A component with these methods is called an *error boundary.*

***

### `static getDerivedStateFromProps(props, state)`[](#static-getderivedstatefromprops "Link for this heading")

If you define `static getDerivedStateFromProps`, React will call it right before calling [`render`,](#render) both on the initial mount and on subsequent updates. It should return an object to update the state, or `null` to update nothing.

This method exists for [rare use cases](https://legacy.reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html#when-to-use-derived-state) where the state depends on changes in props over time. For example, this `Form` component resets the `email` state when the `userID` prop changes:

```
class Form extends Component {

  state = {

    email: this.props.defaultEmail,

    prevUserID: this.props.userID

  };



  static getDerivedStateFromProps(props, state) {

    // Any time the current user changes,

    // Reset any parts of state that are tied to that user.

    // In this simple example, that's just the email.

    if (props.userID !== state.prevUserID) {

      return {

        prevUserID: props.userID,

        email: props.defaultEmail

      };

    }

    return null;

  }



  // ...

}
```

***

## Usage[](#usage "Link for Usage ")

### Defining a class component[](#defining-a-class-component "Link for Defining a class component ")

To define a React component as a class, extend the built-in `Component` class and define a [`render` method:](#render)

```
import { Component } from 'react';



class Greeting extends Component {

  render() {

    return <h1>Hello, {this.props.name}!</h1>;

  }

}
```

React will call your [`render`](#render) method whenever it needs to figure out what to display on the screen. Usually, you will return some [JSX](/learn/writing-markup-with-jsx) from it. Your `render` method should be a [pure function:](https://en.wikipedia.org/wiki/Pure_function) it should only calculate the JSX.

Similarly to [function components,](/learn/your-first-component#defining-a-component) a class component can [receive information by props](/learn/your-first-component#defining-a-component) from its parent component. However, the syntax for reading props is different. For example, if the parent component renders `<Greeting name="Taylor" />`, then you can read the `name` prop from [`this.props`](#props), like `this.props.name`:

```
import { Component } from 'react';

class Greeting extends Component {
  render() {
    return <h1>Hello, {this.props.name}!</h1>;
  }
}

export default function App() {
  return (
    <>
      <Greeting name="Sara" />
      <Greeting name="Cahal" />
      <Greeting name="Edite" />
    </>
  );
}
```

Note that Hooks (functions starting with `use`, like [`useState`](/reference/react/useState)) are not supported inside class components.

### Pitfall

We recommend defining components as functions instead of classes. [See how to migrate.](#migrating-a-simple-component-from-a-class-to-a-function)

***

### Adding state to a class component[](#adding-state-to-a-class-component "Link for Adding state to a class component ")

To add [state](/learn/state-a-components-memory) to a class, assign an object to a property called [`state`](#state). To update state, call [`this.setState`](#setstate).

```
import { Component } from 'react';

export default class Counter extends Component {
  state = {
    name: 'Taylor',
    age: 42,
  };

  handleNameChange = (e) => {
    this.setState({
      name: e.target.value
    });
  }

  handleAgeChange = () => {
    this.setState({
      age: this.state.age + 1 
    });
  };

  render() {
    return (
      <>
        <input
          value={this.state.name}
          onChange={this.handleNameChange}
        />
        <button onClick={this.handleAgeChange}>
          Increment age
        </button>
        <p>Hello, {this.state.name}. You are {this.state.age}.</p>
      </>
    );
  }
}
```

### Pitfall

We recommend defining components as functions instead of classes. [See how to migrate.](#migrating-a-component-with-state-from-a-class-to-a-function)

***

### Adding lifecycle methods to a class component[](#adding-lifecycle-methods-to-a-class-component "Link for Adding lifecycle methods to a class component ")

There are a few special methods you can define on your class.

If you define the [`componentDidMount`](#componentdidmount) method, React will call it when your component is added *(mounted)* to the screen. React will call [`componentDidUpdate`](#componentdidupdate) after your component re-renders due to changed props or state. React will call [`componentWillUnmount`](#componentwillunmount) after your component has been removed *(unmounted)* from the screen.

If you implement `componentDidMount`, you usually need to implement all three lifecycles to avoid bugs. For example, if `componentDidMount` reads some state or props, you also have to implement `componentDidUpdate` to handle their changes, and `componentWillUnmount` to clean up whatever `componentDidMount` was doing.

For example, this `ChatRoom` component keeps a chat connection synchronized with props and state:

```
import { Component } from 'react';
import { createConnection } from './chat.js';

export default class ChatRoom extends Component {
  state = {
    serverUrl: 'https://localhost:1234'
  };

  componentDidMount() {
    this.setupConnection();
  }

  componentDidUpdate(prevProps, prevState) {
    if (
      this.props.roomId !== prevProps.roomId ||
      this.state.serverUrl !== prevState.serverUrl
    ) {
      this.destroyConnection();
      this.setupConnection();
    }
  }

  componentWillUnmount() {
    this.destroyConnection();
  }

  setupConnection() {
    this.connection = createConnection(
      this.state.serverUrl,
      this.props.roomId
    );
    this.connection.connect();    
  }

  destroyConnection() {
    this.connection.disconnect();
    this.connection = null;
  }

  render() {
    return (
      <>
        <label>
          Server URL:{' '}
          <input
            value={this.state.serverUrl}
            onChange={e => {
              this.setState({
                serverUrl: e.target.value
              });
            }}
          />
        </label>
        <h1>Welcome to the {this.props.roomId} room!</h1>
      </>
    );
  }
}
```

Note that in development when [Strict Mode](/reference/react/StrictMode) is on, React will call `componentDidMount`, immediately call `componentWillUnmount`, and then call `componentDidMount` again. This helps you notice if you forgot to implement `componentWillUnmount` or if its logic doesn’t fully “mirror” what `componentDidMount` does.

### Pitfall

We recommend defining components as functions instead of classes. [See how to migrate.](#migrating-a-component-with-lifecycle-methods-from-a-class-to-a-function)

***

### Catching rendering errors with an error boundary[](#catching-rendering-errors-with-an-error-boundary "Link for Catching rendering errors with an error boundary ")

By default, if your application throws an error during rendering, React will remove its UI from the screen. To prevent this, you can wrap a part of your UI into an *error boundary*. An error boundary is a special component that lets you display some fallback UI instead of the part that crashed—for example, an error message.

To implement an error boundary component, you need to provide [`static getDerivedStateFromError`](#static-getderivedstatefromerror) which lets you update state in response to an error and display an error message to the user. You can also optionally implement [`componentDidCatch`](#componentdidcatch) to add some extra logic, for example, to log the error to an analytics service.

```
class ErrorBoundary extends React.Component {

  constructor(props) {

    super(props);

    this.state = { hasError: false };

  }



  static getDerivedStateFromError(error) {

    // Update state so the next render will show the fallback UI.

    return { hasError: true };

  }



  componentDidCatch(error, info) {

    // Example "componentStack":

    //   in ComponentThatThrows (created by App)

    //   in ErrorBoundary (created by App)

    //   in div (created by App)

    //   in App

    logErrorToMyService(error, info.componentStack);

  }



  render() {

    if (this.state.hasError) {

      // You can render any custom fallback UI

      return this.props.fallback;

    }



    return this.props.children;

  }

}
```

Then you can wrap a part of your component tree with it:

```
<ErrorBoundary fallback={<p>Something went wrong</p>}>

  <Profile />

</ErrorBoundary>
```

If `Profile` or its child component throws an error, `ErrorBoundary` will “catch” that error, display a fallback UI with the error message you’ve provided, and send a production error report to your error reporting service.

You don’t need to wrap every component into a separate error boundary. When you think about the [granularity of error boundaries,](https://www.brandondail.com/posts/fault-tolerance-react) consider where it makes sense to display an error message. For example, in a messaging app, it makes sense to place an error boundary around the list of conversations. It also makes sense to place one around every individual message. However, it wouldn’t make sense to place a boundary around every avatar.

### Note

There is currently no way to write an error boundary as a function component. However, you don’t have to write the error boundary class yourself. For example, you can use [`react-error-boundary`](https://github.com/bvaughn/react-error-boundary) instead.

***

## Alternatives[](#alternatives "Link for Alternatives ")

### Migrating a simple component from a class to a function[](#migrating-a-simple-component-from-a-class-to-a-function "Link for Migrating a simple component from a class to a function ")

Typically, you will [define components as functions](/learn/your-first-component#defining-a-component) instead.

For example, suppose you’re converting this `Greeting` class component to a function:

```
import { Component } from 'react';

class Greeting extends Component {
  render() {
    return <h1>Hello, {this.props.name}!</h1>;
  }
}

export default function App() {
  return (
    <>
      <Greeting name="Sara" />
      <Greeting name="Cahal" />
      <Greeting name="Edite" />
    </>
  );
}
```

Define a function called `Greeting`. This is where you will move the body of your `render` function.

```
function Greeting() {

  // ... move the code from the render method here ...

}
```

Instead of `this.props.name`, define the `name` prop [using the destructuring syntax](/learn/passing-props-to-a-component) and read it directly:

```
function Greeting({ name }) {

  return <h1>Hello, {name}!</h1>;

}
```

Here is a complete example:

```
function Greeting({ name }) {
  return <h1>Hello, {name}!</h1>;
}

export default function App() {
  return (
    <>
      <Greeting name="Sara" />
      <Greeting name="Cahal" />
      <Greeting name="Edite" />
    </>
  );
}
```

***

### Migrating a component with state from a class to a function[](#migrating-a-component-with-state-from-a-class-to-a-function "Link for Migrating a component with state from a class to a function ")

Suppose you’re converting this `Counter` class component to a function:

```
import { Component } from 'react';

export default class Counter extends Component {
  state = {
    name: 'Taylor',
    age: 42,
  };

  handleNameChange = (e) => {
    this.setState({
      name: e.target.value
    });
  }

  handleAgeChange = (e) => {
    this.setState({
      age: this.state.age + 1 
    });
  };

  render() {
    return (
      <>
        <input
          value={this.state.name}
          onChange={this.handleNameChange}
        />
        <button onClick={this.handleAgeChange}>
          Increment age
        </button>
        <p>Hello, {this.state.name}. You are {this.state.age}.</p>
      </>
    );
  }
}
```

Start by declaring a function with the necessary [state variables:](/reference/react/useState#adding-state-to-a-component)

```
import { useState } from 'react';



function Counter() {

  const [name, setName] = useState('Taylor');

  const [age, setAge] = useState(42);

  // ...
```

Next, convert the event handlers:

```
function Counter() {

  const [name, setName] = useState('Taylor');

  const [age, setAge] = useState(42);



  function handleNameChange(e) {

    setName(e.target.value);

  }



  function handleAgeChange() {

    setAge(age + 1);

  }

  // ...
```

Finally, replace all references starting with `this` with the variables and functions you defined in your component. For example, replace `this.state.age` with `age`, and replace `this.handleNameChange` with `handleNameChange`.

Here is a fully converted component:

```
import { useState } from 'react';

export default function Counter() {
  const [name, setName] = useState('Taylor');
  const [age, setAge] = useState(42);

  function handleNameChange(e) {
    setName(e.target.value);
  }

  function handleAgeChange() {
    setAge(age + 1);
  }

  return (
    <>
      <input
        value={name}
        onChange={handleNameChange}
      />
      <button onClick={handleAgeChange}>
        Increment age
      </button>
      <p>Hello, {name}. You are {age}.</p>
    </>
  )
}
```

***

### Migrating a component with lifecycle methods from a class to a function[](#migrating-a-component-with-lifecycle-methods-from-a-class-to-a-function "Link for Migrating a component with lifecycle methods from a class to a function ")

Suppose you’re converting this `ChatRoom` class component with lifecycle methods to a function:

```
import { Component } from 'react';
import { createConnection } from './chat.js';

export default class ChatRoom extends Component {
  state = {
    serverUrl: 'https://localhost:1234'
  };

  componentDidMount() {
    this.setupConnection();
  }

  componentDidUpdate(prevProps, prevState) {
    if (
      this.props.roomId !== prevProps.roomId ||
      this.state.serverUrl !== prevState.serverUrl
    ) {
      this.destroyConnection();
      this.setupConnection();
    }
  }

  componentWillUnmount() {
    this.destroyConnection();
  }

  setupConnection() {
    this.connection = createConnection(
      this.state.serverUrl,
      this.props.roomId
    );
    this.connection.connect();    
  }

  destroyConnection() {
    this.connection.disconnect();
    this.connection = null;
  }

  render() {
    return (
      <>
        <label>
          Server URL:{' '}
          <input
            value={this.state.serverUrl}
            onChange={e => {
              this.setState({
                serverUrl: e.target.value
              });
            }}
          />
        </label>
        <h1>Welcome to the {this.props.roomId} room!</h1>
      </>
    );
  }
}
```

First, verify that your [`componentWillUnmount`](#componentwillunmount) does the opposite of [`componentDidMount`.](#componentdidmount) In the above example, that’s true: it disconnects the connection that `componentDidMount` sets up. If such logic is missing, add it first.

Next, verify that your [`componentDidUpdate`](#componentdidupdate) method handles changes to any props and state you’re using in `componentDidMount`. In the above example, `componentDidMount` calls `setupConnection` which reads `this.state.serverUrl` and `this.props.roomId`. This is why `componentDidUpdate` checks whether `this.state.serverUrl` and `this.props.roomId` have changed, and resets the connection if they did. If your `componentDidUpdate` logic is missing or doesn’t handle changes to all relevant props and state, fix that first.

In the above example, the logic inside the lifecycle methods connects the component to a system outside of React (a chat server). To connect a component to an external system, [describe this logic as a single Effect:](/reference/react/useEffect#connecting-to-an-external-system)

```
import { useState, useEffect } from 'react';



function ChatRoom({ roomId }) {

  const [serverUrl, setServerUrl] = useState('https://localhost:1234');



  useEffect(() => {

    const connection = createConnection(serverUrl, roomId);

    connection.connect();

    return () => {

      connection.disconnect();

    };

  }, [serverUrl, roomId]);



  // ...

}
```

This [`useEffect`](/reference/react/useEffect) call is equivalent to the logic in the lifecycle methods above. If your lifecycle methods do multiple unrelated things, [split them into multiple independent Effects.](/learn/removing-effect-dependencies#is-your-effect-doing-several-unrelated-things) Here is a complete example you can play with:

```
import { useState, useEffect } from 'react';
import { createConnection } from './chat.js';

export default function ChatRoom({ roomId }) {
  const [serverUrl, setServerUrl] = useState('https://localhost:1234');

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, [roomId, serverUrl]);

  return (
    <>
      <label>
        Server URL:{' '}
        <input
          value={serverUrl}
          onChange={e => setServerUrl(e.target.value)}
        />
      </label>
      <h1>Welcome to the {roomId} room!</h1>
    </>
  );
}
```

### Note

If your component does not synchronize with any external systems, [you might not need an Effect.](/learn/you-might-not-need-an-effect)

***

### Migrating a component with context from a class to a function[](#migrating-a-component-with-context-from-a-class-to-a-function "Link for Migrating a component with context from a class to a function ")

In this example, the `Panel` and `Button` class components read [context](/learn/passing-data-deeply-with-context) from [`this.context`:](#context)

```
import { createContext, Component } from 'react';

const ThemeContext = createContext(null);

class Panel extends Component {
  static contextType = ThemeContext;

  render() {
    const theme = this.context;
    const className = 'panel-' + theme;
    return (
      <section className={className}>
        <h1>{this.props.title}</h1>
        {this.props.children}
      </section>
    );    
  }
}

class Button extends Component {
  static contextType = ThemeContext;

  render() {
    const theme = this.context;
    const className = 'button-' + theme;
    return (
      <button className={className}>
        {this.props.children}
      </button>
    );
  }
}

function Form() {
  return (
    <Panel title="Welcome">
      <Button>Sign up</Button>
      <Button>Log in</Button>
    </Panel>
  );
}

export default function MyApp() {
  return (
    <ThemeContext.Provider value="dark">
      <Form />
    </ThemeContext.Provider>
  )
}
```

When you convert them to function components, replace `this.context` with [`useContext`](/reference/react/useContext) calls:

```
import { createContext, useContext } from 'react';

const ThemeContext = createContext(null);

function Panel({ title, children }) {
  const theme = useContext(ThemeContext);
  const className = 'panel-' + theme;
  return (
    <section className={className}>
      <h1>{title}</h1>
      {children}
    </section>
  )
}

function Button({ children }) {
  const theme = useContext(ThemeContext);
  const className = 'button-' + theme;
  return (
    <button className={className}>
      {children}
    </button>
  );
}

function Form() {
  return (
    <Panel title="Welcome">
      <Button>Sign up</Button>
      <Button>Log in</Button>
    </Panel>
  );
}

export default function MyApp() {
  return (
    <ThemeContext.Provider value="dark">
      <Form />
    </ThemeContext.Provider>
  )
}
```

[PreviouscloneElement](/reference/react/cloneElement)

[NextcreateElement](/reference/react/createElement)

***

----
