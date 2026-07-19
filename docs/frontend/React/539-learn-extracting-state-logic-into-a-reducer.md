url: https://18.react.dev/learn/extracting-state-logic-into-a-reducer
----

```
import { useState } from 'react';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';

export default function TaskApp() {
  const [tasks, setTasks] = useState(initialTasks);

  function handleAddTask(text) {
    setTasks([
      ...tasks,
      {
        id: nextId++,
        text: text,
        done: false,
      },
    ]);
  }

  function handleChangeTask(task) {
    setTasks(
      tasks.map((t) => {
        if (t.id === task.id) {
          return task;
        } else {
          return t;
        }
      })
    );
  }

  function handleDeleteTask(taskId) {
    setTasks(tasks.filter((t) => t.id !== taskId));
  }

  return (
    <>
      <h1>Prague itinerary</h1>
      <AddTask onAddTask={handleAddTask} />
      <TaskList
        tasks={tasks}
        onChangeTask={handleChangeTask}
        onDeleteTask={handleDeleteTask}
      />
    </>
  );
}

let nextId = 3;
const initialTasks = [
  {id: 0, text: 'Visit Kafka Museum', done: true},
  {id: 1, text: 'Watch a puppet show', done: false},
  {id: 2, text: 'Lennon Wall pic', done: false},
];
```

```
function handleAddTask(text) {

  setTasks([

    ...tasks,

    {

      id: nextId++,

      text: text,

      done: false,

    },

  ]);

}



function handleChangeTask(task) {

  setTasks(

    tasks.map((t) => {

      if (t.id === task.id) {

        return task;

      } else {

        return t;

      }

    })

  );

}



function handleDeleteTask(taskId) {

  setTasks(tasks.filter((t) => t.id !== taskId));

}
```

Remove all the state setting logic. What you are left with are three event handlers:

* `handleAddTask(text)` is called when the user presses “Add”.
* `handleChangeTask(task)` is called when the user toggles a task or presses “Save”.
* `handleDeleteTask(taskId)` is called when the user presses “Delete”.

Managing state with reducers is slightly different from directly setting state. Instead of telling React “what to do” by setting state, you specify “what the user just did” by dispatching “actions” from your event handlers. (The state update logic will live elsewhere!) So instead of “setting `tasks`” via an event handler, you’re dispatching an “added/changed/deleted a task” action. This is more descriptive of the user’s intent.

```
function handleAddTask(text) {

  dispatch({

    type: 'added',

    id: nextId++,

    text: text,

  });

}



function handleChangeTask(task) {

  dispatch({

    type: 'changed',

    task: task,

  });

}



function handleDeleteTask(taskId) {

  dispatch({

    type: 'deleted',

    id: taskId,

  });

}
```

The object you pass to `dispatch` is called an “action”:

```
function handleDeleteTask(taskId) {

  dispatch(

    // "action" object:

    {

      type: 'deleted',

      id: taskId,

    }

  );

}
```

It is a regular JavaScript object. You decide what to put in it, but generally it should contain the minimal information about *what happened*. (You will add the `dispatch` function itself in a later step.)

### Note

An action object can have any shape.

By convention, it is common to give it a string `type` that describes what happened, and pass any additional information in other fields. The `type` is specific to a component, so in this example either `'added'` or `'added_task'` would be fine. Choose a name that says what happened!

```
dispatch({

  // specific to component

  type: 'what_happened',

  // other fields go here

});
```

### Step 2: Write a reducer function[](#step-2-write-a-reducer-function "Link for Step 2: Write a reducer function ")

A reducer function is where you will put your state logic. It takes two arguments, the current state and the action object, and it returns the next state:

```
function yourReducer(state, action) {

  // return next state for React to set

}
```

React will set the state to what you return from the reducer.

To move your state setting logic from your event handlers to a reducer function in this example, you will:

1. Declare the current state (`tasks`) as the first argument.
2. Declare the `action` object as the second argument.
3. Return the *next* state from the reducer (which React will set the state to).

Here is all the state setting logic migrated to a reducer function:

```
function tasksReducer(tasks, action) {

  if (action.type === 'added') {

    return [

      ...tasks,

      {

        id: action.id,

        text: action.text,

        done: false,

      },

    ];

  } else if (action.type === 'changed') {

    return tasks.map((t) => {

      if (t.id === action.task.id) {

        return action.task;

      } else {

        return t;

      }

    });

  } else if (action.type === 'deleted') {

    return tasks.filter((t) => t.id !== action.id);

  } else {

    throw Error('Unknown action: ' + action.type);

  }

}
```

Because the reducer function takes state (`tasks`) as an argument, you can **declare it outside of your component.** This decreases the indentation level and can make your code easier to read.

### Note

The code above uses if/else statements, but it’s a convention to use [switch statements](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/switch) inside reducers. The result is the same, but it can be easier to read switch statements at a glance.

We’ll be using them throughout the rest of this documentation like so:

```
function tasksReducer(tasks, action) {

  switch (action.type) {

    case 'added': {

      return [

        ...tasks,

        {

          id: action.id,

          text: action.text,

          done: false,

        },

      ];

    }

    case 'changed': {

      return tasks.map((t) => {

        if (t.id === action.task.id) {

          return action.task;

        } else {

          return t;

        }

      });

    }

    case 'deleted': {

      return tasks.filter((t) => t.id !== action.id);

    }

    default: {

      throw Error('Unknown action: ' + action.type);

    }

  }

}
```

We recommend wrapping each `case` block into the `{` and `}` curly braces so that variables declared inside of different `case`s don’t clash with each other. Also, a `case` should usually end with a `return`. If you forget to `return`, the code will “fall through” to the next `case`, which can lead to mistakes!

If you’re not yet comfortable with switch statements, using if/else is completely fine.

##### Deep Dive#### Why are reducers called this way?[](#why-are-reducers-called-this-way "Link for Why are reducers called this way? ")

Although reducers can “reduce” the amount of code inside your component, they are actually named after the [`reduce()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/Reduce) operation that you can perform on arrays.

The `reduce()` operation lets you take an array and “accumulate” a single value out of many:

```
const arr = [1, 2, 3, 4, 5];

const sum = arr.reduce(

  (result, number) => result + number

); // 1 + 2 + 3 + 4 + 5
```

The function you pass to `reduce` is known as a “reducer”. It takes the *result so far* and the *current item,* then it returns the *next result.* React reducers are an example of the same idea: they take the *state so far* and the *action*, and return the *next state.* In this way, they accumulate actions over time into state.

You could even use the `reduce()` method with an `initialState` and an array of `actions` to calculate the final state by passing your reducer function to it:

```
import tasksReducer from './tasksReducer.js';

let initialState = [];
let actions = [
  {type: 'added', id: 1, text: 'Visit Kafka Museum'},
  {type: 'added', id: 2, text: 'Watch a puppet show'},
  {type: 'deleted', id: 1},
  {type: 'added', id: 3, text: 'Lennon Wall pic'},
];

let finalState = actions.reduce(tasksReducer, initialState);

const output = document.getElementById('output');
output.textContent = JSON.stringify(finalState, null, 2);
```

You probably won’t need to do this yourself, but this is similar to what React does!

### Step 3: Use the reducer from your component[](#step-3-use-the-reducer-from-your-component "Link for Step 3: Use the reducer from your component ")

Finally, you need to hook up the `tasksReducer` to your component. Import the `useReducer` Hook from React:

```
import { useReducer } from 'react';
```

Then you can replace `useState`:

```
const [tasks, setTasks] = useState(initialTasks);
```

with `useReducer` like so:

```
const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
```

```
import { useReducer } from 'react';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';

export default function TaskApp() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);

  function handleAddTask(text) {
    dispatch({
      type: 'added',
      id: nextId++,
      text: text,
    });
  }

  function handleChangeTask(task) {
    dispatch({
      type: 'changed',
      task: task,
    });
  }

  function handleDeleteTask(taskId) {
    dispatch({
      type: 'deleted',
      id: taskId,
    });
  }

  return (
    <>
      <h1>Prague itinerary</h1>
      <AddTask onAddTask={handleAddTask} />
      <TaskList
        tasks={tasks}
        onChangeTask={handleChangeTask}
        onDeleteTask={handleDeleteTask}
      />
    </>
  );
}

function tasksReducer(tasks, action) {
  switch (action.type) {
    case 'added': {
      return [
        ...tasks,
        {
          id: action.id,
          text: action.text,
          done: false,
        },
      ];
    }
    case 'changed': {
      return tasks.map((t) => {
        if (t.id === action.task.id) {
          return action.task;
        } else {
          return t;
        }
      });
    }
    case 'deleted': {
      return tasks.filter((t) => t.id !== action.id);
    }
    default: {
      throw Error('Unknown action: ' + action.type);
    }
  }
}

let nextId = 3;
const initialTasks = [
  {id: 0, text: 'Visit Kafka Museum', done: true},
  {id: 1, text: 'Watch a puppet show', done: false},
  {id: 2, text: 'Lennon Wall pic', done: false},
];
```

If you want, you can even move the reducer to a different file:

```
import { useReducer } from 'react';
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';
import tasksReducer from './tasksReducer.js';

export default function TaskApp() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);

  function handleAddTask(text) {
    dispatch({
      type: 'added',
      id: nextId++,
      text: text,
    });
  }

  function handleChangeTask(task) {
    dispatch({
      type: 'changed',
      task: task,
    });
  }

  function handleDeleteTask(taskId) {
    dispatch({
      type: 'deleted',
      id: taskId,
    });
  }

  return (
    <>
      <h1>Prague itinerary</h1>
      <AddTask onAddTask={handleAddTask} />
      <TaskList
        tasks={tasks}
        onChangeTask={handleChangeTask}
        onDeleteTask={handleDeleteTask}
      />
    </>
  );
}

let nextId = 3;
const initialTasks = [
  {id: 0, text: 'Visit Kafka Museum', done: true},
  {id: 1, text: 'Watch a puppet show', done: false},
  {id: 2, text: 'Lennon Wall pic', done: false},
];
```

```
{
  "dependencies": {
    "immer": "1.7.3",
    "react": "latest",
    "react-dom": "latest",
    "react-scripts": "latest",
    "use-immer": "0.5.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test --env=jsdom",
    "eject": "react-scripts eject"
  },
  "devDependencies": {}
}
```

```
import { useReducer } from 'react';
import Chat from './Chat.js';
import ContactList from './ContactList.js';
import { initialState, messengerReducer } from './messengerReducer';

export default function Messenger() {
  const [state, dispatch] = useReducer(messengerReducer, initialState);
  const message = state.message;
  const contact = contacts.find((c) => c.id === state.selectedId);
  return (
    <div>
      <ContactList
        contacts={contacts}
        selectedId={state.selectedId}
        dispatch={dispatch}
      />
      <Chat
        key={contact.id}
        message={message}
        contact={contact}
        dispatch={dispatch}
      />
    </div>
  );
}

const contacts = [
  {id: 0, name: 'Taylor', email: 'taylor@mail.com'},
  {id: 1, name: 'Alice', email: 'alice@mail.com'},
  {id: 2, name: 'Bob', email: 'bob@mail.com'},
];
```

[PreviousPreserving and Resetting State](/learn/preserving-and-resetting-state)

[NextPassing Data Deeply with Context](/learn/passing-data-deeply-with-context)

***

----
