url: https://18.react.dev/learn/queueing-a-series-of-state-updates
----

99

9

10

11

12

13

14

15

16

17

import { useState } from 'react';



export default function Counter() {

const \[number, setNumber] = useState(0);



return (

<>

\<h1>{number}\</h1>

\<button onClick={() => {

setNumber(number + 1);

setNumber(number + 1);

setNumber(number + 1);

}}>+3\</button>

\</>

)

}



However, as you might recall from the previous section, [each render’s state values are fixed](/learn/state-as-a-snapshot#rendering-takes-a-snapshot-in-time), so the value of `number` inside the first render’s event handler is always `0`, no matter how many times you call `setNumber(1)`:

```
setNumber(0 + 1);

setNumber(0 + 1);

setNumber(0 + 1);
```

```
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(n => n + 1);
        setNumber(n => n + 1);
        setNumber(n => n + 1);
      }}>+3</button>
    </>
  )
}
```

Here, `n => n + 1` is called an **updater function.** When you pass it to a state setter:

1. React queues this function to be processed after all the other code in the event handler has run.
2. During the next render, React goes through the queue and gives you the final updated state.

```
setNumber(n => n + 1);

setNumber(n => n + 1);

setNumber(n => n + 1);
```

Here’s how React works through these lines of code while executing the event handler:

1. `setNumber(n => n + 1)`: `n => n + 1` is a function. React adds it to a queue.
2. `setNumber(n => n + 1)`: `n => n + 1` is a function. React adds it to a queue.
3. `setNumber(n => n + 1)`: `n => n + 1` is a function. React adds it to a queue.

When you call `useState` during the next render, React goes through the queue. The previous `number` state was `0`, so that’s what React passes to the first updater function as the `n` argument. Then React takes the return value of your previous updater function and passes it to the next updater as `n`, and so on:

| queued update | `n` | returns     |
| ------------- | --- | ----------- |
| `n => n + 1`  | `0` | `0 + 1 = 1` |
| `n => n + 1`  | `1` | `1 + 1 = 2` |
| `n => n + 1`  | `2` | `2 + 1 = 3` |

React stores `3` as the final result and returns it from `useState`.

This is why clicking “+3” in the above example correctly increments the value by 3.

### What happens if you update state after replacing it[](#what-happens-if-you-update-state-after-replacing-it "Link for What happens if you update state after replacing it ")

What about this event handler? What do you think `number` will be in the next render?

```
<button onClick={() => {

  setNumber(number + 5);

  setNumber(n => n + 1);

}}>
```

```
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(number + 5);
        setNumber(n => n + 1);
      }}>Increase the number</button>
    </>
  )
}
```

Here’s what this event handler tells React to do:

1. `setNumber(number + 5)`: `number` is `0`, so `setNumber(0 + 5)`. React adds *“replace with `5`”* to its queue.
2. `setNumber(n => n + 1)`: `n => n + 1` is an updater function. React adds *that function* to its queue.

During the next render, React goes through the state queue:

| queued update      | `n`          | returns     |
| ------------------ | ------------ | ----------- |
| ”replace with `5`” | `0` (unused) | `5`         |
| `n => n + 1`       | `5`          | `5 + 1 = 6` |

React stores `6` as the final result and returns it from `useState`.

### Note

You may have noticed that `setState(5)` actually works like `setState(n => 5)`, but `n` is unused!

### What happens if you replace state after updating it[](#what-happens-if-you-replace-state-after-updating-it "Link for What happens if you replace state after updating it ")

Let’s try one more example. What do you think `number` will be in the next render?

```
<button onClick={() => {

  setNumber(number + 5);

  setNumber(n => n + 1);

  setNumber(42);

}}>
```

```
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(number + 5);
        setNumber(n => n + 1);
        setNumber(42);
      }}>Increase the number</button>
    </>
  )
}
```

Here’s how React works through these lines of code while executing this event handler:

1. `setNumber(number + 5)`: `number` is `0`, so `setNumber(0 + 5)`. React adds *“replace with `5`”* to its queue.
2. `setNumber(n => n + 1)`: `n => n + 1` is an updater function. React adds *that function* to its queue.
3. `setNumber(42)`: React adds *“replace with `42`”* to its queue.

During the next render, React goes through the state queue:

| queued update       | `n`          | returns     |
| ------------------- | ------------ | ----------- |
| ”replace with `5`”  | `0` (unused) | `5`         |
| `n => n + 1`        | `5`          | `5 + 1 = 6` |
| ”replace with `42`” | `6` (unused) | `42`        |

```
setEnabled(e => !e);

setLastName(ln => ln.reverse());

setFriendCount(fc => fc * 2);
```

```
import { useState } from 'react';

export default function RequestTracker() {
  const [pending, setPending] = useState(0);
  const [completed, setCompleted] = useState(0);

  async function handleClick() {
    setPending(pending + 1);
    await delay(3000);
    setPending(pending - 1);
    setCompleted(completed + 1);
  }

  return (
    <>
      <h3>
        Pending: {pending}
      </h3>
      <h3>
        Completed: {completed}
      </h3>
      <button onClick={handleClick}>
        Buy     
      </button>
    </>
  );
}

function delay(ms) {
  return new Promise(resolve => {
    setTimeout(resolve, ms);
  });
}
```

[PreviousState as a Snapshot](/learn/state-as-a-snapshot)

[NextUpdating Objects in State](/learn/updating-objects-in-state)

***

----
