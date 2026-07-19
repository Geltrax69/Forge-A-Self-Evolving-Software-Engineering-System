url: https://react.dev/reference/react/useInsertionEffect
----

[API Reference](/reference/react)

[Hooks](/reference/react/hooks)

# useInsertionEffect[](#undefined "Link for this heading")

### Pitfall

`useInsertionEffect` is for CSS-in-JS library authors. Unless you are working on a CSS-in-JS library and need a place to inject the styles, you probably want [`useEffect`](/reference/react/useEffect) or [`useLayoutEffect`](/reference/react/useLayoutEffect) instead.

`useInsertionEffect` allows inserting elements into the DOM before any layout Effects fire.

```
useInsertionEffect(setup, dependencies?)
```

* [Reference](#reference)
  * [`useInsertionEffect(setup, dependencies?)`](#useinsertioneffect)
* [Usage](#usage)
  * [Injecting dynamic styles from CSS-in-JS libraries](#injecting-dynamic-styles-from-css-in-js-libraries)

***

## Reference[](#reference "Link for Reference ")

### `useInsertionEffect(setup, dependencies?)`[](#useinsertioneffect "Link for this heading")

Call `useInsertionEffect` to insert styles before any Effects fire that may need to read layout:

```
import { useInsertionEffect } from 'react';



// Inside your CSS-in-JS library

function useCSS(rule) {

  useInsertionEffect(() => {

    // ... inject <style> tags here ...

  });

  return rule;

}
```

***

## Usage[](#usage "Link for Usage ")

### Injecting dynamic styles from CSS-in-JS libraries[](#injecting-dynamic-styles-from-css-in-js-libraries "Link for Injecting dynamic styles from CSS-in-JS libraries ")

Traditionally, you would style React components using plain CSS.

```
// In your JS file:

<button className="success" />



// In your CSS file:

.success { color: green; }
```

```
// Inside your CSS-in-JS library

let isInserted = new Set();

function useCSS(rule) {

  useInsertionEffect(() => {

    // As explained earlier, we don't recommend runtime injection of <style> tags.

    // But if you have to do it, then it's important to do in useInsertionEffect.

    if (!isInserted.has(rule)) {

      isInserted.add(rule);

      document.head.appendChild(getStyleForRule(rule));

    }

  });

  return rule;

}



function Button() {

  const className = useCSS('...');

  return <div className={className} />;

}
```

Similarly to `useEffect`, `useInsertionEffect` does not run on the server. If you need to collect which CSS rules have been used on the server, you can do it during rendering:

```
let collectedRulesSet = new Set();



function useCSS(rule) {

  if (typeof window === 'undefined') {

    collectedRulesSet.add(rule);

  }

  useInsertionEffect(() => {

    // ...

  });

  return rule;

}
```

[Read more about upgrading CSS-in-JS libraries with runtime injection to `useInsertionEffect`.](https://github.com/reactwg/react-18/discussions/110)

##### Deep Dive#### How is this better than injecting styles during rendering or useLayoutEffect?[](#how-is-this-better-than-injecting-styles-during-rendering-or-uselayouteffect "Link for How is this better than injecting styles during rendering or useLayoutEffect? ")

If you insert styles during rendering and React is processing a [non-blocking update,](/reference/react/useTransition#perform-non-blocking-updates-with-actions) the browser will recalculate the styles every single frame while rendering a component tree, which can be **extremely slow.**

`useInsertionEffect` is better than inserting styles during [`useLayoutEffect`](/reference/react/useLayoutEffect) or [`useEffect`](/reference/react/useEffect) because it ensures that by the time other Effects run in your components, the `<style>` tags have already been inserted. Otherwise, layout calculations in regular Effects would be wrong due to outdated styles.

[PrevioususeImperativeHandle](/reference/react/useImperativeHandle)

[NextuseLayoutEffect](/reference/react/useLayoutEffect)

***

----
