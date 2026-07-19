url: https://18.react.dev/reference/react/startTransition
----

[API Reference](/reference/react)

[APIs](/reference/react/apis)

# startTransition[](#undefined "Link for this heading")

`startTransition` lets you update the state without blocking the UI.

```
startTransition(scope)
```

* [Reference](#reference)
  * [`startTransition(scope)`](#starttransitionscope)
* [Usage](#usage)
  * [Marking a state update as a non-blocking Transition](#marking-a-state-update-as-a-non-blocking-transition)

***

## Reference[](#reference "Link for Reference ")

### `startTransition(scope)`[](#starttransitionscope "Link for this heading")

The `startTransition` function lets you mark a state update as a Transition.

```
import { startTransition } from 'react';



function TabContainer() {

  const [tab, setTab] = useState('about');



  function selectTab(nextTab) {

    startTransition(() => {

      setTab(nextTab);

    });

  }

  // ...

}
```

[See more examples below.](#usage)

#### Parameters[](#parameters "Link for Parameters ")

* `scope`: A function that updates some state by calling one or more [`set` functions.](/reference/react/useState#setstate) React immediately calls `scope` with no arguments and marks all state updates scheduled synchronously during the `scope` function call as Transitions. They will be [non-blocking](/reference/react/useTransition#marking-a-state-update-as-a-non-blocking-transition) and [will not display unwanted loading indicators.](/reference/react/useTransition#preventing-unwanted-loading-indicators)

#### Returns[](#returns "Link for Returns ")

`startTransition` does not return anything.

#### Caveats[](#caveats "Link for Caveats ")

* `startTransition` does not provide a way to track whether a Transition is pending. To show a pending indicator while the Transition is ongoing, you need [`useTransition`](/reference/react/useTransition) instead.

* You can wrap an update into a Transition only if you have access to the `set` function of that state. If you want to start a Transition in response to some prop or a custom Hook return value, try [`useDeferredValue`](/reference/react/useDeferredValue) instead.

* The function you pass to `startTransition` must be synchronous. React immediately executes this function, marking all state updates that happen while it executes as Transitions. If you try to perform more state updates later (for example, in a timeout), they won’t be marked as Transitions.

* A state update marked as a Transition will be interrupted by other state updates. For example, if you update a chart component inside a Transition, but then start typing into an input while the chart is in the middle of a re-render, React will restart the rendering work on the chart component after handling the input state update.

* Transition updates can’t be used to control text inputs.

* If there are multiple ongoing Transitions, React currently batches them together. This is a limitation that will likely be removed in a future release.

***

## Usage[](#usage "Link for Usage ")

### Marking a state update as a non-blocking Transition[](#marking-a-state-update-as-a-non-blocking-transition "Link for Marking a state update as a non-blocking Transition ")

You can mark a state update as a *Transition* by wrapping it in a `startTransition` call:

```
import { startTransition } from 'react';



function TabContainer() {

  const [tab, setTab] = useState('about');



  function selectTab(nextTab) {

    startTransition(() => {

      setTab(nextTab);

    });

  }

  // ...

}
```

***

----
