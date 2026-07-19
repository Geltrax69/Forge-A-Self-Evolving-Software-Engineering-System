url: https://18.react.dev/reference/react-dom/components/common
----

***

## Reference[](#reference "Link for Reference ")

### Common components (e.g. `<div>`)[](#common "Link for this heading")

```
<div className="wrapper">Some content</div>
```

***

### `ref` callback function[](#ref-callback "Link for this heading")

Instead of a ref object (like the one returned by [`useRef`](/reference/react/useRef#manipulating-the-dom-with-a-ref)), you may pass a function to the `ref` attribute.

```
<div ref={(node) => console.log(node)} />
```

[See an example of using the `ref` callback.](/learn/manipulating-the-dom-with-refs#how-to-manage-a-list-of-refs-using-a-ref-callback)

When the `<div>` DOM node is added to the screen, React will call your `ref` callback with the DOM `node` as the argument. When that `<div>` DOM node is removed, React will call your `ref` callback with `null`.

React will also call your `ref` callback whenever you pass a *different* `ref` callback. In the above example, `(node) => { ... }` is a different function on every render. When your component re-renders, the *previous* function will be called with `null` as the argument, and the *next* function will be called with the DOM node.

#### Parameters[](#ref-callback-parameters "Link for Parameters ")

* `node`: A DOM node or `null`. React will pass you the DOM node when the ref gets attached, and `null` when the `ref` gets detached. Unless you pass the same function reference for the `ref` callback on every render, the callback will get temporarily detached and re-attached during every re-render of the component.

### Canary

#### Returns[](#returns "Link for Returns ")

* **optional** `cleanup function`: When the `ref` is detached, React will call the cleanup function. If a function is not returned by the `ref` callback, React will call the callback again with `null` as the argument when the `ref` gets detached.

```


<div ref={(node) => {

  console.log(node);



  return () => {

    console.log('Clean up', node)

  }

}}>
```

#### Caveats[](#caveats "Link for Caveats ")

* When Strict Mode is on, React will **run one extra development-only setup+cleanup cycle** before the first real setup. This is a stress-test that ensures that your cleanup logic “mirrors” your setup logic and that it stops or undoes whatever the setup is doing. If this causes a problem, implement the cleanup function.
* When you pass a *different* `ref` callback, React will call the *previous* callback’s cleanup function if provided. If not cleanup function is defined, the `ref` callback will be called with `null` as the argument. The *next* function will be called with the DOM node.

***

### React event object[](#react-event-object "Link for React event object ")

Your event handlers will receive a *React event object.* It is also sometimes known as a “synthetic event”.

```
<button onClick={e => {

  console.log(e); // React event object

}} />
```

***

### `AnimationEvent` handler function[](#animationevent-handler "Link for this heading")

An event handler type for the [CSS animation](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations/Using_CSS_animations) events.

```
<div

  onAnimationStart={e => console.log('onAnimationStart')}

  onAnimationIteration={e => console.log('onAnimationIteration')}

  onAnimationEnd={e => console.log('onAnimationEnd')}

/>
```

#### Parameters[](#animationevent-handler-parameters "Link for Parameters ")

* `e`: A [React event object](#react-event-object) with these extra [`AnimationEvent`](https://developer.mozilla.org/en-US/docs/Web/API/AnimationEvent) properties:

  * [`animationName`](https://developer.mozilla.org/en-US/docs/Web/API/AnimationEvent/animationName)
  * [`elapsedTime`](https://developer.mozilla.org/en-US/docs/Web/API/AnimationEvent/elapsedTime)
  * [`pseudoElement`](https://developer.mozilla.org/en-US/docs/Web/API/AnimationEvent/pseudoElement)

***

### `ClipboardEvent` handler function[](#clipboadevent-handler "Link for this heading")

An event handler type for the [Clipboard API](https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API) events.

```
<input

  onCopy={e => console.log('onCopy')}

  onCut={e => console.log('onCut')}

  onPaste={e => console.log('onPaste')}

/>
```

#### Parameters[](#clipboadevent-handler-parameters "Link for Parameters ")

* `e`: A [React event object](#react-event-object) with these extra [`ClipboardEvent`](https://developer.mozilla.org/en-US/docs/Web/API/ClipboardEvent) properties:

  * [`clipboardData`](https://developer.mozilla.org/en-US/docs/Web/API/ClipboardEvent/clipboardData)

***

### `CompositionEvent` handler function[](#compositionevent-handler "Link for this heading")

An event handler type for the [input method editor (IME)](https://developer.mozilla.org/en-US/docs/Glossary/Input_method_editor) events.

```
<input

  onCompositionStart={e => console.log('onCompositionStart')}

  onCompositionUpdate={e => console.log('onCompositionUpdate')}

  onCompositionEnd={e => console.log('onCompositionEnd')}

/>
```

#### Parameters[](#compositionevent-handler-parameters "Link for Parameters ")

* `e`: A [React event object](#react-event-object) with these extra [`CompositionEvent`](https://developer.mozilla.org/en-US/docs/Web/API/CompositionEvent) properties:
  * [`data`](https://developer.mozilla.org/en-US/docs/Web/API/CompositionEvent/data)

***

### `DragEvent` handler function[](#dragevent-handler "Link for this heading")

An event handler type for the [HTML Drag and Drop API](https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API) events.

```
<>

  <div

    draggable={true}

    onDragStart={e => console.log('onDragStart')}

    onDragEnd={e => console.log('onDragEnd')}

  >

    Drag source

  </div>



  <div

    onDragEnter={e => console.log('onDragEnter')}

    onDragLeave={e => console.log('onDragLeave')}

    onDragOver={e => { e.preventDefault(); console.log('onDragOver'); }}

    onDrop={e => console.log('onDrop')}

  >

    Drop target

  </div>

</>
```

***

### `FocusEvent` handler function[](#focusevent-handler "Link for this heading")

An event handler type for the focus events.

```
<input

  onFocus={e => console.log('onFocus')}

  onBlur={e => console.log('onBlur')}

/>
```

***

### `Event` handler function[](#event-handler "Link for this heading")

An event handler type for generic events.

#### Parameters[](#event-handler-parameters "Link for Parameters ")

* `e`: A [React event object](#react-event-object) with no additional properties.

***

### `InputEvent` handler function[](#inputevent-handler "Link for this heading")

An event handler type for the `onBeforeInput` event.

```
<input onBeforeInput={e => console.log('onBeforeInput')} />
```

#### Parameters[](#inputevent-handler-parameters "Link for Parameters ")

* `e`: A [React event object](#react-event-object) with these extra [`InputEvent`](https://developer.mozilla.org/en-US/docs/Web/API/InputEvent) properties:
  * [`data`](https://developer.mozilla.org/en-US/docs/Web/API/InputEvent/data)

***

### `KeyboardEvent` handler function[](#keyboardevent-handler "Link for this heading")

An event handler type for keyboard events.

```
<input

  onKeyDown={e => console.log('onKeyDown')}

  onKeyUp={e => console.log('onKeyUp')}

/>
```

***

### `MouseEvent` handler function[](#mouseevent-handler "Link for this heading")

An event handler type for mouse events.

```
<div

  onClick={e => console.log('onClick')}

  onMouseEnter={e => console.log('onMouseEnter')}

  onMouseOver={e => console.log('onMouseOver')}

  onMouseDown={e => console.log('onMouseDown')}

  onMouseUp={e => console.log('onMouseUp')}

  onMouseLeave={e => console.log('onMouseLeave')}

/>
```

***

### `PointerEvent` handler function[](#pointerevent-handler "Link for this heading")

An event handler type for [pointer events.](https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events)

```
<div

  onPointerEnter={e => console.log('onPointerEnter')}

  onPointerMove={e => console.log('onPointerMove')}

  onPointerDown={e => console.log('onPointerDown')}

  onPointerUp={e => console.log('onPointerUp')}

  onPointerLeave={e => console.log('onPointerLeave')}

/>
```

***

### `TouchEvent` handler function[](#touchevent-handler "Link for this heading")

An event handler type for [touch events.](https://developer.mozilla.org/en-US/docs/Web/API/Touch_events)

```
<div

  onTouchStart={e => console.log('onTouchStart')}

  onTouchMove={e => console.log('onTouchMove')}

  onTouchEnd={e => console.log('onTouchEnd')}

  onTouchCancel={e => console.log('onTouchCancel')}

/>
```

***

### `TransitionEvent` handler function[](#transitionevent-handler "Link for this heading")

An event handler type for the CSS transition events.

```
<div

  onTransitionEnd={e => console.log('onTransitionEnd')}

/>
```

#### Parameters[](#transitionevent-handler-parameters "Link for Parameters ")

* `e`: A [React event object](#react-event-object) with these extra [`TransitionEvent`](https://developer.mozilla.org/en-US/docs/Web/API/TransitionEvent) properties:

  * [`elapsedTime`](https://developer.mozilla.org/en-US/docs/Web/API/TransitionEvent/elapsedTime)
  * [`propertyName`](https://developer.mozilla.org/en-US/docs/Web/API/TransitionEvent/propertyName)
  * [`pseudoElement`](https://developer.mozilla.org/en-US/docs/Web/API/TransitionEvent/pseudoElement)

***

### `UIEvent` handler function[](#uievent-handler "Link for this heading")

An event handler type for generic UI events.

```
<div

  onScroll={e => console.log('onScroll')}

/>
```

#### Parameters[](#uievent-handler-parameters "Link for Parameters ")

* `e`: A [React event object](#react-event-object) with these extra [`UIEvent`](https://developer.mozilla.org/en-US/docs/Web/API/UIEvent) properties:

  * [`detail`](https://developer.mozilla.org/en-US/docs/Web/API/UIEvent/detail)
  * [`view`](https://developer.mozilla.org/en-US/docs/Web/API/UIEvent/view)

***

### `WheelEvent` handler function[](#wheelevent-handler "Link for this heading")

An event handler type for the `onWheel` event.

```
<div

  onWheel={e => console.log('onWheel')}

/>
```

***

## Usage[](#usage "Link for Usage ")

### Applying CSS styles[](#applying-css-styles "Link for Applying CSS styles ")

In React, you specify a CSS class with [`className`.](https://developer.mozilla.org/en-US/docs/Web/API/Element/className) It works like the `class` attribute in HTML:

```
<img className="avatar" />
```

Then you write the CSS rules for it in a separate CSS file:

```
/* In your CSS */

.avatar {

  border-radius: 50%;

}
```

React does not prescribe how you add CSS files. In the simplest case, you’ll add a [`<link>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link) tag to your HTML. If you use a build tool or a framework, consult its documentation to learn how to add a CSS file to your project.

Sometimes, the style values depend on data. Use the `style` attribute to pass some styles dynamically:

```
<img

  className="avatar"

  style={{

    width: user.imageSize,

    height: user.imageSize

  }}

/>
```

In the above example, `style={{}}` is not a special syntax, but a regular `{}` object inside the `style={ }` [JSX curly braces.](/learn/javascript-in-jsx-with-curly-braces) We recommend only using the `style` attribute when your styles depend on JavaScript variables.

```
export default function Avatar({ user }) {
  return (
    <img
      src={user.imageUrl}
      alt={'Photo of ' + user.name}
      className="avatar"
      style={{
        width: user.imageSize,
        height: user.imageSize
      }}
    />
  );
}
```

##### Deep Dive#### How to apply multiple CSS classes conditionally?[](#how-to-apply-multiple-css-classes-conditionally "Link for How to apply multiple CSS classes conditionally? ")

To apply CSS classes conditionally, you need to produce the `className` string yourself using JavaScript.

For example, `className={'row ' + (isSelected ? 'selected': '')}` will produce either `className="row"` or `className="row selected"` depending on whether `isSelected` is `true`.

To make this more readable, you can use a tiny helper library like [`classnames`:](https://github.com/JedWatson/classnames)

```
import cn from 'classnames';



function Row({ isSelected }) {

  return (

    <div className={cn('row', isSelected && 'selected')}>

      ...

    </div>

  );

}
```

It is especially convenient if you have multiple conditional classes:

```
import cn from 'classnames';



function Row({ isSelected, size }) {

  return (

    <div className={cn('row', {

      selected: isSelected,

      large: size === 'large',

      small: size === 'small',

    })}>

      ...

    </div>

  );

}
```

***

### Manipulating a DOM node with a ref[](#manipulating-a-dom-node-with-a-ref "Link for Manipulating a DOM node with a ref ")

Sometimes, you’ll need to get the browser DOM node associated with a tag in JSX. For example, if you want to focus an `<input>` when a button is clicked, you need to call [`focus()`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus) on the browser `<input>` DOM node.

To obtain the browser DOM node for a tag, [declare a ref](/reference/react/useRef) and pass it as the `ref` attribute to that tag:

```
import { useRef } from 'react';



export default function Form() {

  const inputRef = useRef(null);

  // ...

  return (

    <input ref={inputRef} />

    // ...
```

React will put the DOM node into `inputRef.current` after it’s been rendered to the screen.

```
import { useRef } from 'react';

export default function Form() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <input ref={inputRef} />
      <button onClick={handleClick}>
        Focus the input
      </button>
    </>
  );
}
```

Read more about [manipulating DOM with refs](/learn/manipulating-the-dom-with-refs) and [check out more examples.](/reference/react/useRef#examples-dom)

For more advanced use cases, the `ref` attribute also accepts a [callback function.](#ref-callback)

***

### Dangerously setting the inner HTML[](#dangerously-setting-the-inner-html "Link for Dangerously setting the inner HTML ")

You can pass a raw HTML string to an element like so:

```
const markup = { __html: '<p>some raw html</p>' };

return <div dangerouslySetInnerHTML={markup} />;
```

**This is dangerous. As with the underlying DOM [`innerHTML`](https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML) property, you must exercise extreme caution! Unless the markup is coming from a completely trusted source, it is trivial to introduce an [XSS](https://en.wikipedia.org/wiki/Cross-site_scripting) vulnerability this way.**

For example, if you use a Markdown library that converts Markdown to HTML, you trust that its parser doesn’t contain bugs, and the user only sees their own input, you can display the resulting HTML like this:

```
import { Remarkable } from 'remarkable';

const md = new Remarkable();

function renderMarkdownToHTML(markdown) {
  // This is ONLY safe because the output HTML
  // is shown to the same user, and because you
  // trust this Markdown parser to not have bugs.
  const renderedHTML = md.render(markdown);
  return {__html: renderedHTML};
}

export default function MarkdownPreview({ markdown }) {
  const markup = renderMarkdownToHTML(markdown);
  return <div dangerouslySetInnerHTML={markup} />;
}
```

The `{__html}` object should be created as close to where the HTML is generated as possible, like the above example does in the `renderMarkdownToHTML` function. This ensures that all raw HTML being used in your code is explicitly marked as such, and that only variables that you expect to contain HTML are passed to `dangerouslySetInnerHTML`. It is not recommended to create the object inline like `<div dangerouslySetInnerHTML={{__html: markup}} />`.

To see why rendering arbitrary HTML is dangerous, replace the code above with this:

```
const post = {

  // Imagine this content is stored in the database.

  content: `<img src="" onerror='alert("you were hacked")'>`

};



export default function MarkdownPreview() {

  // 🔴 SECURITY HOLE: passing untrusted input to dangerouslySetInnerHTML

  const markup = { __html: post.content };

  return <div dangerouslySetInnerHTML={markup} />;

}
```

The code embedded in the HTML will run. A hacker could use this security hole to steal user information or to perform actions on their behalf. **Only use `dangerouslySetInnerHTML` with trusted and sanitized data.**

***

### Handling mouse events[](#handling-mouse-events "Link for Handling mouse events ")

This example shows some common [mouse events](#mouseevent-handler) and when they fire.

```
export default function MouseExample() {
  return (
    <div
      onMouseEnter={e => console.log('onMouseEnter (parent)')}
      onMouseLeave={e => console.log('onMouseLeave (parent)')}
    >
      <button
        onClick={e => console.log('onClick (first button)')}
        onMouseDown={e => console.log('onMouseDown (first button)')}
        onMouseEnter={e => console.log('onMouseEnter (first button)')}
        onMouseLeave={e => console.log('onMouseLeave (first button)')}
        onMouseOver={e => console.log('onMouseOver (first button)')}
        onMouseUp={e => console.log('onMouseUp (first button)')}
      >
        First button
      </button>
      <button
        onClick={e => console.log('onClick (second button)')}
        onMouseDown={e => console.log('onMouseDown (second button)')}
        onMouseEnter={e => console.log('onMouseEnter (second button)')}
        onMouseLeave={e => console.log('onMouseLeave (second button)')}
        onMouseOver={e => console.log('onMouseOver (second button)')}
        onMouseUp={e => console.log('onMouseUp (second button)')}
      >
        Second button
      </button>
    </div>
  );
}
```

***

### Handling pointer events[](#handling-pointer-events "Link for Handling pointer events ")

This example shows some common [pointer events](#pointerevent-handler) and when they fire.

```
export default function PointerExample() {
  return (
    <div
      onPointerEnter={e => console.log('onPointerEnter (parent)')}
      onPointerLeave={e => console.log('onPointerLeave (parent)')}
      style={{ padding: 20, backgroundColor: '#ddd' }}
    >
      <div
        onPointerDown={e => console.log('onPointerDown (first child)')}
        onPointerEnter={e => console.log('onPointerEnter (first child)')}
        onPointerLeave={e => console.log('onPointerLeave (first child)')}
        onPointerMove={e => console.log('onPointerMove (first child)')}
        onPointerUp={e => console.log('onPointerUp (first child)')}
        style={{ padding: 20, backgroundColor: 'lightyellow' }}
      >
        First child
      </div>
      <div
        onPointerDown={e => console.log('onPointerDown (second child)')}
        onPointerEnter={e => console.log('onPointerEnter (second child)')}
        onPointerLeave={e => console.log('onPointerLeave (second child)')}
        onPointerMove={e => console.log('onPointerMove (second child)')}
        onPointerUp={e => console.log('onPointerUp (second child)')}
        style={{ padding: 20, backgroundColor: 'lightblue' }}
      >
        Second child
      </div>
    </div>
  );
}
```

***

### Handling focus events[](#handling-focus-events "Link for Handling focus events ")

In React, [focus events](#focusevent-handler) bubble. You can use the `currentTarget` and `relatedTarget` to differentiate if the focusing or blurring events originated from outside of the parent element. The example shows how to detect focusing a child, focusing the parent element, and how to detect focus entering or leaving the whole subtree.

```
export default function FocusExample() {
  return (
    <div
      tabIndex={1}
      onFocus={(e) => {
        if (e.currentTarget === e.target) {
          console.log('focused parent');
        } else {
          console.log('focused child', e.target.name);
        }
        if (!e.currentTarget.contains(e.relatedTarget)) {
          // Not triggered when swapping focus between children
          console.log('focus entered parent');
        }
      }}
      onBlur={(e) => {
        if (e.currentTarget === e.target) {
          console.log('unfocused parent');
        } else {
          console.log('unfocused child', e.target.name);
        }
        if (!e.currentTarget.contains(e.relatedTarget)) {
          // Not triggered when swapping focus between children
          console.log('focus left parent');
        }
      }}
    >
      <label>
        First name:
        <input name="firstName" />
      </label>
      <label>
        Last name:
        <input name="lastName" />
      </label>
    </div>
  );
}
```

***

### Handling keyboard events[](#handling-keyboard-events "Link for Handling keyboard events ")

This example shows some common [keyboard events](#keyboardevent-handler) and when they fire.

```
export default function KeyboardExample() {
  return (
    <label>
      First name:
      <input
        name="firstName"
        onKeyDown={e => console.log('onKeyDown:', e.key, e.code)}
        onKeyUp={e => console.log('onKeyUp:', e.key, e.code)}
      />
    </label>
  );
}
```

[PreviousComponents](/reference/react-dom/components)

[Next\<form>](/reference/react-dom/components/form)

***

----
