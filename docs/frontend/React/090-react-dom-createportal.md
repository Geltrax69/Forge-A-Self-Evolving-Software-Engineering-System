url: https://18.react.dev/reference/react-dom/createPortal
----

[API Reference](/reference/react)

[APIs](/reference/react-dom)

# createPortal[](#undefined "Link for this heading")

`createPortal` lets you render some children into a different part of the DOM.

```
<div>

  <SomeComponent />

  {createPortal(children, domNode, key?)}

</div>
```

***

## Reference[](#reference "Link for Reference ")

### `createPortal(children, domNode, key?)`[](#createportal "Link for this heading")

To create a portal, call `createPortal`, passing some JSX, and the DOM node where it should be rendered:

```
import { createPortal } from 'react-dom';



// ...



<div>

  <p>This child is placed in the parent div.</p>

  {createPortal(

    <p>This child is placed in the document body.</p>,

    document.body

  )}

</div>
```

***

## Usage[](#usage "Link for Usage ")

### Rendering to a different part of the DOM[](#rendering-to-a-different-part-of-the-dom "Link for Rendering to a different part of the DOM ")

*Portals* let your components render some of their children into a different place in the DOM. This lets a part of your component “escape” from whatever containers it may be in. For example, a component can display a modal dialog or a tooltip that appears above and outside of the rest of the page.

To create a portal, render the result of `createPortal` with some JSX and the DOM node where it should go:

```
import { createPortal } from 'react-dom';



function MyComponent() {

  return (

    <div style={{ border: '2px solid black' }}>

      <p>This child is placed in the parent div.</p>

      {createPortal(

        <p>This child is placed in the document body.</p>,

        document.body

      )}

    </div>

  );

}
```

React will put the DOM nodes for the JSX you passed inside of the DOM node you provided.

Without a portal, the second `<p>` would be placed inside the parent `<div>`, but the portal “teleported” it into the [`document.body`:](https://developer.mozilla.org/en-US/docs/Web/API/Document/body)

```
import { createPortal } from 'react-dom';

export default function MyComponent() {
  return (
    <div style={{ border: '2px solid black' }}>
      <p>This child is placed in the parent div.</p>
      {createPortal(
        <p>This child is placed in the document body.</p>,
        document.body
      )}
    </div>
  );
}
```

Notice how the second paragraph visually appears outside the parent `<div>` with the border. If you inspect the DOM structure with developer tools, you’ll see that the second `<p>` got placed directly into the `<body>`:

```
<body>

  <div id="root">

    ...

      <div style="border: 2px solid black">

        <p>This child is placed inside the parent div.</p>

      </div>

    ...

  </div>

  <p>This child is placed in the document body.</p>

</body>
```

A portal only changes the physical placement of the DOM node. In every other way, the JSX you render into a portal acts as a child node of the React component that renders it. For example, the child can access the context provided by the parent tree, and events still bubble up from children to parents according to the React tree.

***

### Rendering a modal dialog with a portal[](#rendering-a-modal-dialog-with-a-portal "Link for Rendering a modal dialog with a portal ")

You can use a portal to create a modal dialog that floats above the rest of the page, even if the component that summons the dialog is inside a container with `overflow: hidden` or other styles that interfere with the dialog.

In this example, the two containers have styles that disrupt the modal dialog, but the one rendered into a portal is unaffected because, in the DOM, the modal is not contained within the parent JSX elements.

```
import NoPortalExample from './NoPortalExample';
import PortalExample from './PortalExample';

export default function App() {
  return (
    <>
      <div className="clipping-container">
        <NoPortalExample  />
      </div>
      <div className="clipping-container">
        <PortalExample />
      </div>
    </>
  );
}
```

### Pitfall

It’s important to make sure that your app is accessible when using portals. For instance, you may need to manage keyboard focus so that the user can move the focus in and out of the portal in a natural way.

Follow the [WAI-ARIA Modal Authoring Practices](https://www.w3.org/WAI/ARIA/apg/#dialog_modal) when creating modals. If you use a community package, ensure that it is accessible and follows these guidelines.

***

### Rendering React components into non-React server markup[](#rendering-react-components-into-non-react-server-markup "Link for Rendering React components into non-React server markup ")

Portals can be useful if your React root is only part of a static or server-rendered page that isn’t built with React. For example, if your page is built with a server framework like Rails, you can create areas of interactivity within static areas such as sidebars. Compared with having [multiple separate React roots,](/reference/react-dom/client/createRoot#rendering-a-page-partially-built-with-react) portals let you treat the app as a single React tree with shared state even though its parts render to different parts of the DOM.

```
import { createPortal } from 'react-dom';

const sidebarContentEl = document.getElementById('sidebar-content');

export default function App() {
  return (
    <>
      <MainContent />
      {createPortal(
        <SidebarContent />,
        sidebarContentEl
      )}
    </>
  );
}

function MainContent() {
  return <p>This part is rendered by React</p>;
}

function SidebarContent() {
  return <p>This part is also rendered by React!</p>;
}
```

***

### Rendering React components into non-React DOM nodes[](#rendering-react-components-into-non-react-dom-nodes "Link for Rendering React components into non-React DOM nodes ")

You can also use a portal to manage the content of a DOM node that’s managed outside of React. For example, suppose you’re integrating with a non-React map widget and you want to render React content inside a popup. To do this, declare a `popupContainer` state variable to store the DOM node you’re going to render into:

```
const [popupContainer, setPopupContainer] = useState(null);
```

When you create the third-party widget, store the DOM node returned by the widget so you can render into it:

```
useEffect(() => {

  if (mapRef.current === null) {

    const map = createMapWidget(containerRef.current);

    mapRef.current = map;

    const popupDiv = addPopupToMapWidget(map);

    setPopupContainer(popupDiv);

  }

}, []);
```

This lets you use `createPortal` to render React content into `popupContainer` once it becomes available:

```
return (

  <div style={{ width: 250, height: 250 }} ref={containerRef}>

    {popupContainer !== null && createPortal(

      <p>Hello from React!</p>,

      popupContainer

    )}

  </div>

);
```

Here is a complete example you can play with:

```
import { useRef, useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { createMapWidget, addPopupToMapWidget } from './map-widget.js';

export default function Map() {
  const containerRef = useRef(null);
  const mapRef = useRef(null);
  const [popupContainer, setPopupContainer] = useState(null);

  useEffect(() => {
    if (mapRef.current === null) {
      const map = createMapWidget(containerRef.current);
      mapRef.current = map;
      const popupDiv = addPopupToMapWidget(map);
      setPopupContainer(popupDiv);
    }
  }, []);

  return (
    <div style={{ width: 250, height: 250 }} ref={containerRef}>
      {popupContainer !== null && createPortal(
        <p>Hello from React!</p>,
        popupContainer
      )}
    </div>
  );
}
```

[PreviousAPIs](/reference/react-dom)

[NextflushSync](/reference/react-dom/flushSync)

***

----
