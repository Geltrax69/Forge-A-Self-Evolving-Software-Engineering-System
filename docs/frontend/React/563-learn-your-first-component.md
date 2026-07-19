url: https://18.react.dev/learn/your-first-component
----

```
<article>

  <h1>My First Component</h1>

  <ol>

    <li>Components: UI Building Blocks</li>

    <li>Defining a Component</li>

    <li>Using a Component</li>

  </ol>

</article>
```

This markup represents this article `<article>`, its heading `<h1>`, and an (abbreviated) table of contents as an ordered list `<ol>`. Markup like this, combined with CSS for style, and JavaScript for interactivity, lies behind every sidebar, avatar, modal, dropdown—every piece of UI you see on the Web.

React lets you combine your markup, CSS, and JavaScript into custom “components”, **reusable UI elements for your app.** The table of contents code you saw above could be turned into a `<TableOfContents />` component you could render on every page. Under the hood, it still uses the same HTML tags like `<article>`, `<h1>`, etc.

Just like with HTML tags, you can compose, order and nest components to design whole pages. For example, the documentation page you’re reading is made out of React components:

```
<PageLayout>

  <NavigationHeader>

    <SearchBar />

    <Link to="/docs">Docs</Link>

  </NavigationHeader>

  <Sidebar />

  <PageContent>

    <TableOfContents />

    <DocumentationText />

  </PageContent>

</PageLayout>
```

As your project grows, you will notice that many of your designs can be composed by reusing components you already wrote, speeding up your development. Our table of contents above could be added to any screen with `<TableOfContents />`! You can even jumpstart your project with the thousands of components shared by the React open source community like [Chakra UI](https://chakra-ui.com/) and [Material UI.](https://material-ui.com/)

## Defining a component[](#defining-a-component "Link for Defining a component ")

Traditionally when creating web pages, web developers marked up their content and then added interaction by sprinkling on some JavaScript. This worked great when interaction was a nice-to-have on the web. Now it is expected for many sites and all apps. React puts interactivity first while still using the same technology: **a React component is a JavaScript function that you can *sprinkle with markup*.** Here’s what that looks like (you can edit the example below):

```
export default function Profile() {
  return (
    <img
      src="https://i.imgur.com/MK3eW3Am.jpg"
      alt="Katherine Johnson"
    />
  )
}
```

```
return <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />;
```

But if your markup isn’t all on the same line as the `return` keyword, you must wrap it in a pair of parentheses:

```
return (

  <div>

    <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />

  </div>

);
```

### Pitfall

Without parentheses, any code on the lines after `return` [will be ignored](https://stackoverflow.com/questions/2846283/what-are-the-rules-for-javascripts-automatic-semicolon-insertion-asi)!

## Using a component[](#using-a-component "Link for Using a component ")

Now that you’ve defined your `Profile` component, you can nest it inside other components. For example, you can export a `Gallery` component that uses multiple `Profile` components:

```
function Profile() {
  return (
    <img
      src="https://i.imgur.com/MK3eW3As.jpg"
      alt="Katherine Johnson"
    />
  );
}

export default function Gallery() {
  return (
    <section>
      <h1>Amazing scientists</h1>
      <Profile />
      <Profile />
      <Profile />
    </section>
  );
}
```

### What the browser sees[](#what-the-browser-sees "Link for What the browser sees ")

Notice the difference in casing:

* `<section>` is lowercase, so React knows we refer to an HTML tag.
* `<Profile />` starts with a capital `P`, so React knows that we want to use our component called `Profile`.

And `Profile` contains even more HTML: `<img />`. In the end, this is what the browser sees:

```
<section>

  <h1>Amazing scientists</h1>

  <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />

  <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />

  <img src="https://i.imgur.com/MK3eW3As.jpg" alt="Katherine Johnson" />

</section>
```

### Nesting and organizing components[](#nesting-and-organizing-components "Link for Nesting and organizing components ")

Components are regular JavaScript functions, so you can keep multiple components in the same file. This is convenient when components are relatively small or tightly related to each other. If this file gets crowded, you can always move `Profile` to a separate file. You will learn how to do this shortly on the [page about imports.](/learn/importing-and-exporting-components)

Because the `Profile` components are rendered inside `Gallery`—even several times!—we can say that `Gallery` is a **parent component,** rendering each `Profile` as a “child”. This is part of the magic of React: you can define a component once, and then use it in as many places and as many times as you like.

### Pitfall

Components can render other components, but **you must never nest their definitions:**

```
export default function Gallery() {

  // 🔴 Never define a component inside another component!

  function Profile() {

    // ...

  }

  // ...

}
```

The snippet above is [very slow and causes bugs.](/learn/preserving-and-resetting-state#different-components-at-the-same-position-reset-state) Instead, define every component at the top level:

```
export default function Gallery() {

  // ...

}



// ✅ Declare components at the top level

function Profile() {

  // ...

}
```

When a child component needs some data from a parent, [pass it by props](/learn/passing-props-to-a-component) instead of nesting definitions.

##### Deep Dive#### Components all the way down[](#components-all-the-way-down "Link for Components all the way down ")

Your React application begins at a “root” component. Usually, it is created automatically when you start a new project. For example, if you use [CodeSandbox](https://codesandbox.io/) or if you use the framework [Next.js](https://nextjs.org/), the root component is defined in `pages/index.js`. In these examples, you’ve been exporting root components.

Most React apps use components all the way down. This means that you won’t only use components for reusable pieces like buttons, but also for larger pieces like sidebars, lists, and ultimately, complete pages! Components are a handy way to organize UI code and markup, even if some of them are only used once.

[React-based frameworks](/learn/start-a-new-react-project) take this a step further. Instead of using an empty HTML file and letting React “take over” managing the page with JavaScript, they *also* generate the HTML automatically from your React components. This allows your app to show some content before the JavaScript code loads.

[Fork](https://codesandbox.io/api/v1/sandboxes/define?parameters=N4IgZglgNgpgziAXKOAnAxgeggOwCYwAeAdAFYLIjoD2OALjPUiBALYAO1qdABAEowAhujoAaHsB4BlOqggiAstQI8AvjzCpqrHgB0QqISP0BuXTjaduEnukOCGfatV7rN2vQaN0AtHm2Y6FAQjHSm5pZcvPrEmHB0AJ6wcMTocHDhOBEcUTwAguzsGlo6MZgF7JnmNDjxPFouPAC8tvaOznQAFP7oAK6socQA5jB0AKKwA_QAQgkAknid-g1hIACUa2Y4K8SG-DCoSzg8PAA8MnKKyjAAfOYnJ6cVPJh3x2eYF_J0SgRvmyBRCw4NNcIJUAkkGBBFA4DBVED2MIANaCEZkOC0JCgGoMJiIEDAe6eHCCAb6RCeewiYgEABu-lExP0dIOcAgtApngADMRedzGcyQKxBLgufo4hhsPsSORBe99HA7BB2HQMkgJMSToq6ODVpTlt4fEq5Kq4Dx4nr5Q9PAAjXrQPDirzCXwmlVqnj2x3Wh76BjxZ3Ut3Ks08AO8Hw-Rh0prkfysX3akAwUgwYwaw2u42hz2p9OrYkIoUEdiMAg4dAhdWUonvZPB50APQAjAAOPl8pNUo0J5vtzsCwFanvZ91m5sAVkH-iLTIVIHpABEYGX9pXq1zgKpzKpAcDQaSIVCYXCESB2L1bcEsLgCCQABZ0VhQbFUWh4ujMU4AQiXAHkAGEABUAE0AAUxh4J8XzeU4YKgHgoEEHAhiafRGH0OCHyEPA3keAZdVsB9wThOh0JAABVYCADEfDbLDiVOQjBB4UkBgoukQgAdysVZbA_UIKO4iA8DoB8mnpeQYB8ESxIfcRcAgOgIBhHMYRgJoWy7EB8LOFS6FgG4l2oPopjoU5MAMozzEsnDBDw2zbWUBI9NOPAIDpHhRIolYsMsjy6TgzBnLwVzbMwBCbn3CAQTBY9EGhWF4SBNAsAqDE31xUJmDAXpKxU2geHArRIFgTo1k1d5DDoXpUGOI4bVONghhHE40oop86HYOBEEwbBiBaurUgCKA5kAsA6VtJcyHYVqQDangYXI_Q8mRYIoF6HgABkYFYEVZ3rF49M2XdzBiuKj0hRLTxSkA0riRJklSdIssE_EQAAKiqk5nMIY0IAAL1wIZKWc1ACFQHw_q2HcshwUKEh-jQPx8aFWGgBJKTgFC4GNA4IDALYThFVAhlwSkACZuXYQhiZ4JE8A81DKW5WHzHMB8W2R0nyZwHw6GodhWfpsBUfZQGYCpynafZ-GH0pnnwT5gWhZF4kxfoAHJapmm6bO-WAGYlbJ3BVeFng2Y18Wgalnh21lg3OYAFhNlXBYtq33k1t1bcpFsADZHZwOHOcnN2zY99XvZtnX7ed4PQ5wB8A4j_mo8t0XY7tlsZf1kOOcra5kZ97Wc-ISm9rl8xekQusTkZ5mhh8XBghwGTLW4XXE8LlqbBwiAhiff22xbWW1HOoFYsPcFrqSs9zwYDhkIYZg7CEBgfGDHxBEKEBVCAA\&query=file%3D%252Fsrc%252FApp.js%26utm_medium%3Dsandpack\&environment=create-react-app "Open in CodeSandbox")

```
function Profile() {
  return (
    <img
      src="https://i.imgur.com/lICfvbD.jpg"
      alt="Aklilu Lemma"
    />
  );
}
```

Try to fix it yourself before looking at the solution!

[PreviousDescribing the UI](/learn/describing-the-ui)

[NextImporting and Exporting Components](/learn/importing-and-exporting-components)

***

----
