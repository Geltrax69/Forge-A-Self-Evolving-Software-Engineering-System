url: https://18.react.dev/learn/rendering-lists
----

```
<ul>

  <li>Creola Katherine Johnson: mathematician</li>

  <li>Mario José Molina-Pasquel Henríquez: chemist</li>

  <li>Mohammad Abdus Salam: physicist</li>

  <li>Percy Lavon Julian: chemist</li>

  <li>Subrahmanyan Chandrasekhar: astrophysicist</li>

</ul>
```

The only difference among those list items is their contents, their data. You will often need to show several instances of the same component using different data when building interfaces: from lists of comments to galleries of profile images. In these situations, you can store that data in JavaScript objects and arrays and use methods like [`map()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map) and [`filter()`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) to render lists of components from them.

Here’s a short example of how to generate a list of items from an array:

1. **Move** the data into an array:

```
const people = [

  'Creola Katherine Johnson: mathematician',

  'Mario José Molina-Pasquel Henríquez: chemist',

  'Mohammad Abdus Salam: physicist',

  'Percy Lavon Julian: chemist',

  'Subrahmanyan Chandrasekhar: astrophysicist'

];
```

2. **Map** the `people` members into a new array of JSX nodes, `listItems`:

```
const listItems = people.map(person => <li>{person}</li>);
```

3. **Return** `listItems` from your component wrapped in a `<ul>`:

```
return <ul>{listItems}</ul>;
```

Here is the result:

```
const people = [
  'Creola Katherine Johnson: mathematician',
  'Mario José Molina-Pasquel Henríquez: chemist',
  'Mohammad Abdus Salam: physicist',
  'Percy Lavon Julian: chemist',
  'Subrahmanyan Chandrasekhar: astrophysicist'
];

export default function List() {
  const listItems = people.map(person =>
    <li>{person}</li>
  );
  return <ul>{listItems}</ul>;
}
```

Notice the sandbox above displays a console error:

Console

Warning: Each child in a list should have a unique “key” prop.

You’ll learn how to fix this error later on this page. Before we get to that, let’s add some structure to your data.

## Filtering arrays of items[](#filtering-arrays-of-items "Link for Filtering arrays of items ")

This data can be structured even more.

```
const people = [{

  id: 0,

  name: 'Creola Katherine Johnson',

  profession: 'mathematician',

}, {

  id: 1,

  name: 'Mario José Molina-Pasquel Henríquez',

  profession: 'chemist',

}, {

  id: 2,

  name: 'Mohammad Abdus Salam',

  profession: 'physicist',

}, {

  id: 3,

  name: 'Percy Lavon Julian',

  profession: 'chemist',  

}, {

  id: 4,

  name: 'Subrahmanyan Chandrasekhar',

  profession: 'astrophysicist',

}];
```

Let’s say you want a way to only show people whose profession is `'chemist'`. You can use JavaScript’s `filter()` method to return just those people. This method takes an array of items, passes them through a “test” (a function that returns `true` or `false`), and returns a new array of only those items that passed the test (returned `true`).

You only want the items where `profession` is `'chemist'`. The “test” function for this looks like `(person) => person.profession === 'chemist'`. Here’s how to put it together:

1. **Create** a new array of just “chemist” people, `chemists`, by calling `filter()` on the `people` filtering by `person.profession === 'chemist'`:

```
const chemists = people.filter(person =>

  person.profession === 'chemist'

);
```

2. Now **map** over `chemists`:

```
const listItems = chemists.map(person =>

  <li>

     <img

       src={getImageUrl(person)}

       alt={person.name}

     />

     <p>

       <b>{person.name}:</b>

       {' ' + person.profession + ' '}

       known for {person.accomplishment}

     </p>

  </li>

);
```

3. Lastly, **return** the `listItems` from your component:

```
return <ul>{listItems}</ul>;
```

```
import { people } from './data.js';
import { getImageUrl } from './utils.js';

export default function List() {
  const chemists = people.filter(person =>
    person.profession === 'chemist'
  );
  const listItems = chemists.map(person =>
    <li>
      <img
        src={getImageUrl(person)}
        alt={person.name}
      />
      <p>
        <b>{person.name}:</b>
        {' ' + person.profession + ' '}
        known for {person.accomplishment}
      </p>
    </li>
  );
  return <ul>{listItems}</ul>;
}
```

### Pitfall

Arrow functions implicitly return the expression right after `=>`, so you didn’t need a `return` statement:

```
const listItems = chemists.map(person =>

  <li>...</li> // Implicit return!

);
```

However, **you must write `return` explicitly if your `=>` is followed by a `{` curly brace!**

```
const listItems = chemists.map(person => { // Curly brace

  return <li>...</li>;

});
```

Arrow functions containing `=> {` are said to have a [“block body”.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions#function_body) They let you write more than a single line of code, but you *have to* write a `return` statement yourself. If you forget it, nothing gets returned!

## Keeping list items in order with `key`[](#keeping-list-items-in-order-with-key "Link for this heading")

Notice that all the sandboxes above show an error in the console:

Console

Warning: Each child in a list should have a unique “key” prop.

You need to give each array item a `key` — a string or a number that uniquely identifies it among other items in that array:

```
<li key={person.id}>...</li>
```

### Note

JSX elements directly inside a `map()` call always need keys!

Keys tell React which array item each component corresponds to, so that it can match them up later. This becomes important if your array items can move (e.g. due to sorting), get inserted, or get deleted. A well-chosen `key` helps React infer what exactly has happened, and make the correct updates to the DOM tree.

Rather than generating keys on the fly, you should include them in your data:

```
export const people = [{
  id: 0, // Used in JSX as a key
  name: 'Creola Katherine Johnson',
  profession: 'mathematician',
  accomplishment: 'spaceflight calculations',
  imageId: 'MK3eW3A'
}, {
  id: 1, // Used in JSX as a key
  name: 'Mario José Molina-Pasquel Henríquez',
  profession: 'chemist',
  accomplishment: 'discovery of Arctic ozone hole',
  imageId: 'mynHUSa'
}, {
  id: 2, // Used in JSX as a key
  name: 'Mohammad Abdus Salam',
  profession: 'physicist',
  accomplishment: 'electromagnetism theory',
  imageId: 'bE7W1ji'
}, {
  id: 3, // Used in JSX as a key
  name: 'Percy Lavon Julian',
  profession: 'chemist',
  accomplishment: 'pioneering cortisone drugs, steroids and birth control pills',
  imageId: 'IOjWm71'
}, {
  id: 4, // Used in JSX as a key
  name: 'Subrahmanyan Chandrasekhar',
  profession: 'astrophysicist',
  accomplishment: 'white dwarf star mass calculations',
  imageId: 'lrWQx8l'
}];
```

##### Deep Dive#### Displaying several DOM nodes for each list item[](#displaying-several-dom-nodes-for-each-list-item "Link for Displaying several DOM nodes for each list item ")

What do you do when each item needs to render not one, but several DOM nodes?

The short [`<>...</>` Fragment](/reference/react/Fragment) syntax won’t let you pass a key, so you need to either group them into a single `<div>`, or use the slightly longer and [more explicit `<Fragment>` syntax:](/reference/react/Fragment#rendering-a-list-of-fragments)

```
import { Fragment } from 'react';



// ...



const listItems = people.map(person =>

  <Fragment key={person.id}>

    <h1>{person.name}</h1>

    <p>{person.bio}</p>

  </Fragment>

);
```

```
import { people } from './data.js';
import { getImageUrl } from './utils.js';

export default function List() {
  const listItems = people.map(person =>
    <li key={person.id}>
      <img
        src={getImageUrl(person)}
        alt={person.name}
      />
      <p>
        <b>{person.name}:</b>
        {' ' + person.profession + ' '}
        known for {person.accomplishment}
      </p>
    </li>
  );
  return (
    <article>
      <h1>Scientists</h1>
      <ul>{listItems}</ul>
    </article>
  );
}
```

[PreviousConditional Rendering](/learn/conditional-rendering)

[NextKeeping Components Pure](/learn/keeping-components-pure)

***

----
