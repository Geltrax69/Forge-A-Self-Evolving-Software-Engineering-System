url: https://18.react.dev/learn/writing-markup-with-jsx
----

```
<h1>Hedy Lamarr's Todos</h1>

<img 

  src="https://i.imgur.com/yXOvdOSs.jpg" 

  alt="Hedy Lamarr" 

  class="photo"

>

<ul>

    <li>Invent new traffic lights

    <li>Rehearse a movie scene

    <li>Improve the spectrum technology

</ul>
```

And you want to put it into your component:

```
export default function TodoList() {

  return (

    // ???

  )

}
```

If you copy and paste it as is, it will not work:

```
export default function TodoList() {
  return (
    // This doesn't quite work!
    <h1>Hedy Lamarr's Todos</h1>
    <img 
      src="https://i.imgur.com/yXOvdOSs.jpg" 
      alt="Hedy Lamarr" 
      class="photo"
    >
    <ul>
      <li>Invent new traffic lights
      <li>Rehearse a movie scene
      <li>Improve the spectrum technology
    </ul>
```

```
<div>

  <h1>Hedy Lamarr's Todos</h1>

  <img 

    src="https://i.imgur.com/yXOvdOSs.jpg" 

    alt="Hedy Lamarr" 

    class="photo"

  >

  <ul>

    ...

  </ul>

</div>
```

If you don’t want to add an extra `<div>` to your markup, you can write `<>` and `</>` instead:

```
<>

  <h1>Hedy Lamarr's Todos</h1>

  <img 

    src="https://i.imgur.com/yXOvdOSs.jpg" 

    alt="Hedy Lamarr" 

    class="photo"

  >

  <ul>

    ...

  </ul>

</>
```

This empty tag is called a *[Fragment.](/reference/react/Fragment)* Fragments let you group things without leaving any trace in the browser HTML tree.

##### Deep Dive#### Why do multiple JSX tags need to be wrapped?[](#why-do-multiple-jsx-tags-need-to-be-wrapped "Link for Why do multiple JSX tags need to be wrapped? ")

JSX looks like HTML, but under the hood it is transformed into plain JavaScript objects. You can’t return two objects from a function without wrapping them into an array. This explains why you also can’t return two JSX tags without wrapping them into another tag or a Fragment.

### 2. Close all the tags[](#2-close-all-the-tags "Link for 2. Close all the tags ")

JSX requires tags to be explicitly closed: self-closing tags like `<img>` must become `<img />`, and wrapping tags like `<li>oranges` must be written as `<li>oranges</li>`.

This is how Hedy Lamarr’s image and list items look closed:

```
<>

  <img 

    src="https://i.imgur.com/yXOvdOSs.jpg" 

    alt="Hedy Lamarr" 

    class="photo"

   />

  <ul>

    <li>Invent new traffic lights</li>

    <li>Rehearse a movie scene</li>

    <li>Improve the spectrum technology</li>

  </ul>

</>
```

### 3. camelCase ~~all~~ most of the things\![](#3-camelcase-salls-most-of-the-things "Link for this heading")

JSX turns into JavaScript and attributes written in JSX become keys of JavaScript objects. In your own components, you will often want to read those attributes into variables. But JavaScript has limitations on variable names. For example, their names can’t contain dashes or be reserved words like `class`.

This is why, in React, many HTML and SVG attributes are written in camelCase. For example, instead of `stroke-width` you use `strokeWidth`. Since `class` is a reserved word, in React you write `className` instead, named after the [corresponding DOM property](https://developer.mozilla.org/en-US/docs/Web/API/Element/className):

```
<img 

  src="https://i.imgur.com/yXOvdOSs.jpg" 

  alt="Hedy Lamarr" 

  className="photo"

/>
```

You can [find all these attributes in the list of DOM component props.](/reference/react-dom/components/common) If you get one wrong, don’t worry—React will print a message with a possible correction to the [browser console.](https://developer.mozilla.org/docs/Tools/Browser_Console)

### Pitfall

For historical reasons, [`aria-*`](https://developer.mozilla.org/docs/Web/Accessibility/ARIA) and [`data-*`](https://developer.mozilla.org/docs/Learn/HTML/Howto/Use_data_attributes) attributes are written as in HTML with dashes.

### Pro-tip: Use a JSX Converter[](#pro-tip-use-a-jsx-converter "Link for Pro-tip: Use a JSX Converter ")

Converting all these attributes in existing markup can be tedious! We recommend using a [converter](https://transform.tools/html-to-jsx) to translate your existing HTML and SVG to JSX. Converters are very useful in practice, but it’s still worth understanding what is going on so that you can comfortably write JSX on your own.

Here is your final result:

```
export default function TodoList() {
  return (
    <>
      <h1>Hedy Lamarr's Todos</h1>
      <img 
        src="https://i.imgur.com/yXOvdOSs.jpg" 
        alt="Hedy Lamarr" 
        className="photo" 
      />
      <ul>
        <li>Invent new traffic lights</li>
        <li>Rehearse a movie scene</li>
        <li>Improve the spectrum technology</li>
      </ul>
    </>
  );
}
```

```
export default function Bio() {
  return (
    <div class="intro">
      <h1>Welcome to my website!</h1>
    </div>
    <p class="summary">
      You can find my thoughts here.
      <br><br>
      <b>And <i>pictures</b></i> of scientists!
    </p>
  );
}
```

Whether to do it by hand or using the converter is up to you!

[PreviousImporting and Exporting Components](/learn/importing-and-exporting-components)

[NextJavaScript in JSX with Curly Braces](/learn/javascript-in-jsx-with-curly-braces)

***

----
