url: https://18.react.dev/learn/javascript-in-jsx-with-curly-braces
----

```
export default function Avatar() {
  return (
    <img
      className="avatar"
      src="https://i.imgur.com/7vQD0fPs.jpg"
      alt="Gregorio Y. Zara"
    />
  );
}
```

Here, `"https://i.imgur.com/7vQD0fPs.jpg"` and `"Gregorio Y. Zara"` are being passed as strings.

But what if you want to dynamically specify the `src` or `alt` text? You could **use a value from JavaScript by replacing `"` and `"` with `{` and `}`**:

```
export default function Avatar() {
  const avatar = 'https://i.imgur.com/7vQD0fPs.jpg';
  const description = 'Gregorio Y. Zara';
  return (
    <img
      className="avatar"
      src={avatar}
      alt={description}
    />
  );
}
```

Notice the difference between `className="avatar"`, which specifies an `"avatar"` CSS class name that makes the image round, and `src={avatar}` that reads the value of the JavaScript variable called `avatar`. That’s because curly braces let you work with JavaScript right there in your markup!

## Using curly braces: A window into the JavaScript world[](#using-curly-braces-a-window-into-the-javascript-world "Link for Using curly braces: A window into the JavaScript world ")

JSX is a special way of writing JavaScript. That means it’s possible to use JavaScript inside it—with curly braces `{ }`. The example below first declares a name for the scientist, `name`, then embeds it with curly braces inside the `<h1>`:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?parameters=N4IgZglgNgpgziAXKOAnAxgeggOwCYwAeAdAFYLIjoD2OALjPUiBALYAO1qdABAEowAhujoAaHsB4BlOqggiAstQI8AvjzCpqrHgB0QqISP0BuXTjaduEnukOCGfatV7rN2vQaN0AtHm2Y6FAQjHSm5pZcvPrEmHB0AJ6wcMTocHDhOBEcUTwAguzsGlo6MZgF7JnmNDjxPFouPAC8tvaOznQAFP7oAK6socQA5jB0AKKwA_QAQgkAknid-g1hIACUa2Y4K8SG-DCoSzg8PAA8MnKKyjAAfOYnJ6cVPJh3x2eYF_J0SgRvmyBRCw4NNcIJUAkkGBBFA4DBVED2MIANaCEZkOC0JCgGoMJiIEDAe6eHCCAb6RCeewiYgEABu-lExP0dIOcAgtApngADMRedzGcyQKxBLgufo4hhsPsSORBe99HA7BB2HQMkgJMSToq6ODVpTlt4fEq5Kq4Dx4nr5Q9PAAjXrQPDirzCXwmlVqnj2x3Wh76BjxZ3Ut3Ks08AO8Hw-Rh0prkfysX3akAwUgwYwaw2u42hz2p9OrYkIoUEdiMAg4dAhdWUonvZPB50APQAjAAOPl8pNUo0J5vtzsCwFanvZ91m5sAVkH-iLTIVIHpABEYGX9pXq1zgKpzKpAcDQaSIVCYXCESB2L1bcEsLgCCQABZ0VhQbFUWh4ujMU4AQiXAHkAGEABUAE0AAUxh4J8XzeU4YKgHgoEEHAhiafRGH0OCHyEPA3keAZdVsB9wThOh0JAABVYCADEfDbLDiVOQjBB4UkBgoukQgAdysVZbA_UIKO4iA8DoB8mnpeQYB8ESxIfcRcAgOgIBhHMYRgJoWy7EB8LOFS6FgG4l2oPopjoU5MAMozzEsnDBDw2zbWUBI9NOPAIDpHhRIolYsMsjy6TgzBnLwVzbMwBCbn3CAQTBY9EGhWF4SBNAsAqDE31xUJmCIPieAIaFeigXgwF6SsVNoHhgOUagABlYq6NZNXeGo6nYmBmh4AByABxQwhi4DkeFA4geAALXBQRuq2E5DDoXpUGOI4bXglsbmADrVG680ap4EyeAa-I7PW4lNl3cwYrio9IUS08UpANK4kSZJUnSLLBPxEAACoWpOZzCGNCAAC9cCGSlnNQAhUB8AGth3LIcFChI_o0D8fGhVhoASSk4BQuBjQOCAwFmngRVQIZcEpAAmbl2EIUmkTwDzUMpbl4fMcwHxbVHycpnAfDoah2DZ0mwHR9lgZgGnqfpjnEYfanefBfnBeF0XiXF-ggalmm6YZi6FYAZmVincDVkWeHZzWJZB6WeHbOXDa5gAWU3VaFy3rfeLW3TtykWwANidnAEa5yd3fNz2NZ923dYdl2Q7DnAH0DyOBejq2xbj-2W1lg3Q85ytrlR32ddz4hqZgVh5fMYrUaZlmhh8XBghwGTLW4PWk6Lq7D3BW6krPc8GA4ZCGGYOwhAYHxgx8QRChAVQgA\&query=file%3D%252Fsrc%252FApp.js%26utm_medium%3Dsandpack\&environment=create-react-app "Open in CodeSandbox")

```
export default function TodoList() {
  const name = 'Gregorio Y. Zara';
  return (
    <h1>{name}'s To Do List</h1>
  );
}
```

Try changing the `name`’s value from `'Gregorio Y. Zara'` to `'Hedy Lamarr'`. See how the list title changes?

Any JavaScript expression will work between curly braces, including function calls like `formatDate()`:

```
const today = new Date();

function formatDate(date) {
  return new Intl.DateTimeFormat(
    'en-US',
    { weekday: 'long' }
  ).format(date);
}

export default function TodoList() {
  return (
    <h1>To Do List for {formatDate(today)}</h1>
  );
}
```

```
export default function TodoList() {
  return (
    <ul style={{
      backgroundColor: 'black',
      color: 'pink'
    }}>
      <li>Improve the videophone</li>
      <li>Prepare aeronautics lectures</li>
      <li>Work on the alcohol-fuelled engine</li>
    </ul>
  );
}
```

Try changing the values of `backgroundColor` and `color`.

You can really see the JavaScript object inside the curly braces when you write it like this:

```
<ul style={

  {

    backgroundColor: 'black',

    color: 'pink'

  }

}>
```

The next time you see `{{` and `}}` in JSX, know that it’s nothing more than an object inside the JSX curlies!

### Pitfall

Inline `style` properties are written in camelCase. For example, HTML `<ul style="background-color: black">` would be written as `<ul style={{ backgroundColor: 'black' }}>` in your component.

## More fun with JavaScript objects and curly braces[](#more-fun-with-javascript-objects-and-curly-braces "Link for More fun with JavaScript objects and curly braces ")

You can move several expressions into one object, and reference them in your JSX inside curly braces:

```
const person = {
  name: 'Gregorio Y. Zara',
  theme: {
    backgroundColor: 'black',
    color: 'pink'
  }
};

export default function TodoList() {
  return (
    <div style={person.theme}>
      <h1>{person.name}'s Todos</h1>
      <img
        className="avatar"
        src="https://i.imgur.com/7vQD0fPs.jpg"
        alt="Gregorio Y. Zara"
      />
      <ul>
        <li>Improve the videophone</li>
        <li>Prepare aeronautics lectures</li>
        <li>Work on the alcohol-fuelled engine</li>
      </ul>
    </div>
  );
}
```

In this example, the `person` JavaScript object contains a `name` string and a `theme` object:

```
const person = {

  name: 'Gregorio Y. Zara',

  theme: {

    backgroundColor: 'black',

    color: 'pink'

  }

};
```

The component can use these values from `person` like so:

```
<div style={person.theme}>

  <h1>{person.name}'s Todos</h1>
```

```
const person = {
  name: 'Gregorio Y. Zara',
  theme: {
    backgroundColor: 'black',
    color: 'pink'
  }
};

export default function TodoList() {
  return (
    <div style={person.theme}>
      <h1>{person}'s Todos</h1>
      <img
        className="avatar"
        src="https://i.imgur.com/7vQD0fPs.jpg"
        alt="Gregorio Y. Zara"
      />
      <ul>
        <li>Improve the videophone</li>
        <li>Prepare aeronautics lectures</li>
        <li>Work on the alcohol-fuelled engine</li>
      </ul>
    </div>
  );
}
```

Can you find the problem?

[PreviousWriting Markup with JSX](/learn/writing-markup-with-jsx)

[NextPassing Props to a Component](/learn/passing-props-to-a-component)

***

----
