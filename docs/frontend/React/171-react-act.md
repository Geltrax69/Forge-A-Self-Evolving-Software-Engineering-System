url: https://react.dev/reference/react/act
----

[API Reference](/reference/react)

[APIs](/reference/react/apis)

# act[](#undefined "Link for this heading")

`act` is a test helper to apply pending React updates before making assertions.

```
await act(async actFn)
```

  * [I’m getting an error: “The current testing environment is not configured to support act(…)”](#error-the-current-testing-environment-is-not-configured-to-support-act)

***

## Reference[](#reference "Link for Reference ")

### `await act(async actFn)`[](#await-act-async-actfn "Link for this heading")

When writing UI tests, tasks like rendering, user events, or data fetching can be considered as “units” of interaction with a user interface. React provides a helper called `act()` that makes sure all updates related to these “units” have been processed and applied to the DOM before you make any assertions.

The name `act` comes from the [Arrange-Act-Assert](https://wiki.c2.com/?ArrangeActAssert) pattern.

```
it ('renders with button disabled', async () => {

  await act(async () => {

    root.render(<TestComponent />)

  });

  expect(container.querySelector('button')).toBeDisabled();

});
```

```
function Counter() {

  const [count, setCount] = useState(0);

  const handleClick = () => {

    setCount(prev => prev + 1);

  }



  useEffect(() => {

    document.title = `You clicked ${count} times`;

  }, [count]);



  return (

    <div>

      <p>You clicked {count} times</p>

      <button onClick={handleClick}>

        Click me

      </button>

    </div>

  )

}
```

### Rendering components in tests[](#rendering-components-in-tests "Link for Rendering components in tests ")

To test the render output of a component, wrap the render inside `act()`:

```
import {act} from 'react';

import ReactDOMClient from 'react-dom/client';

import Counter from './Counter';



it('can render and update a counter', async () => {

  container = document.createElement('div');

  document.body.appendChild(container);



  // ✅ Render the component inside act().

  await act(() => {

    ReactDOMClient.createRoot(container).render(<Counter />);

  });



  const button = container.querySelector('button');

  const label = container.querySelector('p');

  expect(label.textContent).toBe('You clicked 0 times');

  expect(document.title).toBe('You clicked 0 times');

});
```

Here, we create a container, append it to the document, and render the `Counter` component inside `act()`. This ensures that the component is rendered and its effects are applied before making assertions.

Using `act` ensures that all updates have been applied before we make assertions.

### Dispatching events in tests[](#dispatching-events-in-tests "Link for Dispatching events in tests ")

To test events, wrap the event dispatch inside `act()`:

```
import {act} from 'react';

import ReactDOMClient from 'react-dom/client';

import Counter from './Counter';



it.only('can render and update a counter', async () => {

  const container = document.createElement('div');

  document.body.appendChild(container);



  await act( async () => {

    ReactDOMClient.createRoot(container).render(<Counter />);

  });



  // ✅ Dispatch the event inside act().

  await act(async () => {

    button.dispatchEvent(new MouseEvent('click', { bubbles: true }));

  });



  const button = container.querySelector('button');

  const label = container.querySelector('p');

  expect(label.textContent).toBe('You clicked 1 times');

  expect(document.title).toBe('You clicked 1 times');

});
```

Here, we render the component with `act`, and then dispatch the event inside another `act()`. This ensures that all updates from the event are applied before making assertions.

### Pitfall

Don’t forget that dispatching DOM events only works when the DOM container is added to the document. You can use a library like [React Testing Library](https://testing-library.com/docs/react-testing-library/intro) to reduce the boilerplate code.

## Troubleshooting[](#troubleshooting "Link for Troubleshooting ")

### I’m getting an error: “The current testing environment is not configured to support act(…)”[](#error-the-current-testing-environment-is-not-configured-to-support-act "Link for I’m getting an error: “The current testing environment is not configured to support act(…)” ")

Using `act` requires setting `global.IS_REACT_ACT_ENVIRONMENT=true` in your test environment. This is to ensure that `act` is only used in the correct environment.

If you don’t set the global, you will see an error like this:

Console

Warning: The current testing environment is not configured to support act(…)

To fix, add this to your global setup file for React tests:

```
global.IS_REACT_ACT_ENVIRONMENT=true
```

### Note

In testing frameworks like [React Testing Library](https://testing-library.com/docs/react-testing-library/intro), `IS_REACT_ACT_ENVIRONMENT` is already set for you.

[PreviousAPIs](/reference/react/apis)

[NextaddTransitionType](/reference/react/addTransitionType)

***

----
