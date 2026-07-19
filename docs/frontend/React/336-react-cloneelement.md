url: https://18.react.dev/reference/react/cloneElement
----

[API Reference](/reference/react)

[Legacy React APIs](/reference/react/legacy)

# cloneElement[](#undefined "Link for this heading")

### Pitfall

Using `cloneElement` is uncommon and can lead to fragile code. [See common alternatives.](#alternatives)

`cloneElement` lets you create a new React element using another element as a starting point.

```
const clonedElement = cloneElement(element, props, ...children)
```

***

## Reference[](#reference "Link for Reference ")

### `cloneElement(element, props, ...children)`[](#cloneelement "Link for this heading")

Call `cloneElement` to create a React element based on the `element`, but with different `props` and `children`:

```
import { cloneElement } from 'react';



// ...

const clonedElement = cloneElement(

  <Row title="Cabbage">

    Hello

  </Row>,

  { isHighlighted: true },

  'Goodbye'

);



console.log(clonedElement); // <Row title="Cabbage" isHighlighted={true}>Goodbye</Row>
```

***

## Usage[](#usage "Link for Usage ")

### Overriding props of an element[](#overriding-props-of-an-element "Link for Overriding props of an element ")

To override the props of some React element, pass it to `cloneElement` with the props you want to override:

```
import { cloneElement } from 'react';



// ...

const clonedElement = cloneElement(

  <Row title="Cabbage" />,

  { isHighlighted: true }

);
```

Here, the resulting cloned element will be `<Row title="Cabbage" isHighlighted={true} />`.

**Let’s walk through an example to see when it’s useful.**

Imagine a `List` component that renders its [`children`](/learn/passing-props-to-a-component#passing-jsx-as-children) as a list of selectable rows with a “Next” button that changes which row is selected. The `List` component needs to render the selected `Row` differently, so it clones every `<Row>` child that it has received, and adds an extra `isHighlighted: true` or `isHighlighted: false` prop:

```
export default function List({ children }) {

  const [selectedIndex, setSelectedIndex] = useState(0);

  return (

    <div className="List">

      {Children.map(children, (child, index) =>

        cloneElement(child, {

          isHighlighted: index === selectedIndex 

        })

      )}
```

Let’s say the original JSX received by `List` looks like this:

```
<List>

  <Row title="Cabbage" />

  <Row title="Garlic" />

  <Row title="Apple" />

</List>
```

By cloning its children, the `List` can pass extra information to every `Row` inside. The result looks like this:

```
<List>

  <Row

    title="Cabbage"

    isHighlighted={true} 

  />

  <Row

    title="Garlic"

    isHighlighted={false} 

  />

  <Row

    title="Apple"

    isHighlighted={false} 

  />

</List>
```

Notice how pressing “Next” updates the state of the `List`, and highlights a different row:

```
import { Children, cloneElement, useState } from 'react';

export default function List({ children }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  return (
    <div className="List">
      {Children.map(children, (child, index) =>
        cloneElement(child, {
          isHighlighted: index === selectedIndex 
        })
      )}
      <hr />
      <button onClick={() => {
        setSelectedIndex(i =>
          (i + 1) % Children.count(children)
        );
      }}>
        Next
      </button>
    </div>
  );
}
```

To summarize, the `List` cloned the `<Row />` elements it received and added an extra prop to them.

### Pitfall

Cloning children makes it hard to tell how the data flows through your app. Try one of the [alternatives.](#alternatives)

***

## Alternatives[](#alternatives "Link for Alternatives ")

### Passing data with a render prop[](#passing-data-with-a-render-prop "Link for Passing data with a render prop ")

Instead of using `cloneElement`, consider accepting a *render prop* like `renderItem`. Here, `List` receives `renderItem` as a prop. `List` calls `renderItem` for every item and passes `isHighlighted` as an argument:

```
export default function List({ items, renderItem }) {

  const [selectedIndex, setSelectedIndex] = useState(0);

  return (

    <div className="List">

      {items.map((item, index) => {

        const isHighlighted = index === selectedIndex;

        return renderItem(item, isHighlighted);

      })}
```

The `renderItem` prop is called a “render prop” because it’s a prop that specifies how to render something. For example, you can pass a `renderItem` implementation that renders a `<Row>` with the given `isHighlighted` value:

```
<List

  items={products}

  renderItem={(product, isHighlighted) =>

    <Row

      key={product.id}

      title={product.title}

      isHighlighted={isHighlighted}

    />

  }

/>
```

The end result is the same as with `cloneElement`:

```
<List>

  <Row

    title="Cabbage"

    isHighlighted={true} 

  />

  <Row

    title="Garlic"

    isHighlighted={false} 

  />

  <Row

    title="Apple"

    isHighlighted={false} 

  />

</List>
```

However, you can clearly trace where the `isHighlighted` value is coming from.

```
import { useState } from 'react';

export default function List({ items, renderItem }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  return (
    <div className="List">
      {items.map((item, index) => {
        const isHighlighted = index === selectedIndex;
        return renderItem(item, isHighlighted);
      })}
      <hr />
      <button onClick={() => {
        setSelectedIndex(i =>
          (i + 1) % items.length
        );
      }}>
        Next
      </button>
    </div>
  );
}
```

This pattern is preferred to `cloneElement` because it is more explicit.

***

### Passing data through context[](#passing-data-through-context "Link for Passing data through context ")

Another alternative to `cloneElement` is to [pass data through context.](/learn/passing-data-deeply-with-context)

For example, you can call [`createContext`](/reference/react/createContext) to define a `HighlightContext`:

```
export const HighlightContext = createContext(false);
```

Your `List` component can wrap every item it renders into a `HighlightContext` provider:

```
export default function List({ items, renderItem }) {

  const [selectedIndex, setSelectedIndex] = useState(0);

  return (

    <div className="List">

      {items.map((item, index) => {

        const isHighlighted = index === selectedIndex;

        return (

          <HighlightContext.Provider key={item.id} value={isHighlighted}>

            {renderItem(item)}

          </HighlightContext.Provider>

        );

      })}
```

With this approach, `Row` does not need to receive an `isHighlighted` prop at all. Instead, it reads the context:

```
export default function Row({ title }) {

  const isHighlighted = useContext(HighlightContext);

  // ...
```

This allows the calling component to not know or worry about passing `isHighlighted` to `<Row>`:

```
<List

  items={products}

  renderItem={product =>

    <Row title={product.title} />

  }

/>
```

Instead, `List` and `Row` coordinate the highlighting logic through context.

```
import { useState } from 'react';
import { HighlightContext } from './HighlightContext.js';

export default function List({ items, renderItem }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  return (
    <div className="List">
      {items.map((item, index) => {
        const isHighlighted = index === selectedIndex;
        return (
          <HighlightContext.Provider
            key={item.id}
            value={isHighlighted}
          >
            {renderItem(item)}
          </HighlightContext.Provider>
        );
      })}
      <hr />
      <button onClick={() => {
        setSelectedIndex(i =>
          (i + 1) % items.length
        );
      }}>
        Next
      </button>
    </div>
  );
}
```

[Learn more about passing data through context.](/reference/react/useContext#passing-data-deeply-into-the-tree)

***

### Extracting logic into a custom Hook[](#extracting-logic-into-a-custom-hook "Link for Extracting logic into a custom Hook ")

Another approach you can try is to extract the “non-visual” logic into your own Hook, and use the information returned by your Hook to decide what to render. For example, you could write a `useList` custom Hook like this:

```
import { useState } from 'react';



export default function useList(items) {

  const [selectedIndex, setSelectedIndex] = useState(0);



  function onNext() {

    setSelectedIndex(i =>

      (i + 1) % items.length

    );

  }



  const selected = items[selectedIndex];

  return [selected, onNext];

}
```

Then you could use it like this:

```
export default function App() {

  const [selected, onNext] = useList(products);

  return (

    <div className="List">

      {products.map(product =>

        <Row

          key={product.id}

          title={product.title}

          isHighlighted={selected === product}

        />

      )}

      <hr />

      <button onClick={onNext}>

        Next

      </button>

    </div>

  );

}
```

The data flow is explicit, but the state is inside the `useList` custom Hook that you can use from any component:

```
import Row from './Row.js';
import useList from './useList.js';
import { products } from './data.js';

export default function App() {
  const [selected, onNext] = useList(products);
  return (
    <div className="List">
      {products.map(product =>
        <Row
          key={product.id}
          title={product.title}
          isHighlighted={selected === product}
        />
      )}
      <hr />
      <button onClick={onNext}>
        Next
      </button>
    </div>
  );
}
```

This approach is particularly useful if you want to reuse this logic between different components.

[PreviousChildren](/reference/react/Children)

[NextComponent](/reference/react/Component)

***

----
