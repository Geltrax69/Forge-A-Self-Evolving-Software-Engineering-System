url: https://18.react.dev/learn/add-react-to-an-existing-project
----

1. **Build the React part of your app** using one of the [React-based frameworks](/learn/start-a-new-react-project).
2. **Specify `/some-app` as the *base path*** in your framework’s configuration (here’s how: [Next.js](https://nextjs.org/docs/api-reference/next.config.js/basepath), [Gatsby](https://www.gatsbyjs.com/docs/how-to/previews-deploys-hosting/path-prefix/)).
3. **Configure your server or a proxy** so that all requests under `/some-app/` are handled by your React app.

This ensures the React part of your app can [benefit from the best practices](/learn/start-a-new-react-project#can-i-use-react-without-a-framework) baked into those frameworks.

* **If your app doesn’t have an existing setup for compiling JavaScript modules,** set it up with [Vite](https://vitejs.dev/). The Vite community maintains [many integrations with backend frameworks](https://github.com/vitejs/awesome-vite#integrations-with-backends), including Rails, Django, and Laravel. If your backend framework is not listed, [follow this guide](https://vitejs.dev/guide/backend-integration.html) to manually integrate Vite builds with your backend.

To check whether your setup works, run this command in your project folder:

Terminal

npm install react react-dom

Then add these lines of code at the top of your main JavaScript file (it might be called `index.js` or `main.js`):

[Fork](https://codesandbox.io/api/v1/sandboxes/define?parameters=N4IgZglgNgpgziAXKOAnAxgeggOwCYwAeAdAFYLIjoD2OALjPUiBALYAO1qdABMD-lQwAhgwBK1arwC-PMKmqseAciHD0dALR5FmdFAiM6ygNwAdHBcyYeAYVjDUPOgAsYPIhDh1cAcx4AEgAqALIAMgK0DPQWOugArqxGxABG1HgAnsS4ODCoweE8ALwqADx4EABuPBB4RWYgwuzsDQB8pZgVla2mFlY2YowEThnU8U6D6rw0HLRGNTjeIngWNIu8ClLFAmriknQAFHGJyb4wdACisEn0AEIZAJJ4B8pN7MoAlB_mOJt0xEJ8HkDqUXABGVoBGBQKDUAA0PAA7lwoHgOuDWt8LCA4Sw4LdcI4MkgwMIoHAYNJcex1ABrYRnMhwWhIUBraJ0ZjACw8HgNHDCJINRB8kBqDTEAiVBpwnmiyp5OAQWjC0UABmIGrVMrlDVYwlwqoamDQWFwBBI5B1OF5DTgggg7DocFV3JtvNF3kcdCNYpEGk09tQjudPC93GtHtFKXi0BWSFF4q0QZDcB4MbjkY9DQY3l9ScDDqdadzvE0mkYlSK5B0rCztpAMFIMA0-f9yaLoabLZ9IDlVN1IAI7CGjHQhhdCbdUYaSd9AD0wQAOTWa-uJ9vaRQL5er7U4uUNgsp4sLgCse4a_dl7oaUoAIjAR0CcOP4K7pBZpDi8QSBahiUQUlyUpal4hSAwzSBEgXDoVgoFZKgoiMZhSgAQnvAB5WwggATQABQuHhYPg1oLFBOCoB4KBhBwXx6kbSwQDInBQWWFjeVKJI6GEAQXEcCk6AYgBVIIADFNCXNo5S485eIFJIGMqQxEU4CMQEiegjAYxFalcIopQgdAYE0XS8FcBFcAgHwyULMkYCKME12YmSfDoWBWnvagEhuOgOjcjzyMwNxhDwFjSjSTIOJ4coqhqOpZ32NoOi6cLMEijI0pIqBWh_Lw_yJEkyQpKkWGg4hssQ9kUMQEB0KwnCCKI7LwpamSQrC0oApgVoQgyHg3n86yPPRdiZIy6LOLQ8seFwsYnE8bw_B4Gkzk0jkeAOXBnBcLwPEIQV2FgSzeDOUMhCO9QYDwD4eHLaKOgmoK2pwPL8UJACipA0rTRNOgMlgOBiHQOAKDZZCmFqgAqPg5TSQhAwgAAvPwRTSVBhk0eGfk_SwcAy2H3TAKJNFJVhoAyEU4FouBAzyCAwB-Xl9VQXxcBFAAmNV2EIJmVtCio6JFNUcb6HBwUJ5nHDZnBNDoah2GFvnifoRGkZgTmOZ50W8ZcDnJZ4FmZblhWlblFXk2RjWeC57WvzFlwAGYDaN3ATcVngRfNkmlXVkVlztnBcYsFwABYXelt35Y9r2iZ9q3_YANkD4PxbPCPWaj03PeV-O_Z4MFQ5Th3E4z43o7NuPVd962wS13n7bxmgCANi21dr4gOZgVgdYseIqOnfm8EF3xNFwAxckDHjuE57mG6DsW3oKz6gOKylSoYDgaIYZhBBEBhNALN4QGkIA\&query=file%3D%252Fsrc%252Findex.js%26utm_medium%3Dsandpack\&environment=create-react-app "Open in CodeSandbox")

```
import { createRoot } from 'react-dom/client';

// Clear the existing HTML content
document.body.innerHTML = '<div id="app"></div>';

// Render your React component instead
const root = createRoot(document.getElementById('app'));
root.render(<h1>Hello, world</h1>);
```

If the entire content of your page was replaced by a “Hello, world!”, everything worked! Keep reading.

### Note

Integrating a modular JavaScript environment into an existing project for the first time can feel intimidating, but it’s worth it! If you get stuck, try our [community resources](/community) or the [Vite Chat](https://chat.vitejs.dev/).

### Step 2: Render React components anywhere on the page[](#step-2-render-react-components-anywhere-on-the-page "Link for Step 2: Render React components anywhere on the page ")

In the previous step, you put this code at the top of your main file:

```
import { createRoot } from 'react-dom/client';



// Clear the existing HTML content

document.body.innerHTML = '<div id="app"></div>';



// Render your React component instead

const root = createRoot(document.getElementById('app'));

root.render(<h1>Hello, world</h1>);
```

Of course, you don’t actually want to clear the existing HTML content!

Delete this code.

Instead, you probably want to render your React components in specific places in your HTML. Open your HTML page (or the server templates that generate it) and add a unique [`id`](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id) attribute to any tag, for example:

```
<!-- ... somewhere in your html ... -->

<nav id="navigation"></nav>

<!-- ... more html ... -->
```

This lets you find that HTML element with [`document.getElementById`](https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById) and pass it to [`createRoot`](/reference/react-dom/client/createRoot) so that you can render your own React component inside:

```
import { createRoot } from 'react-dom/client';

function NavigationBar() {
  // TODO: Actually implement a navigation bar
  return <h1>Hello from React!</h1>;
}

const domNode = document.getElementById('navigation');
const root = createRoot(domNode);
root.render(<NavigationBar />);
```

Notice how the original HTML content from `index.html` is preserved, but your own `NavigationBar` React component now appears inside the `<nav id="navigation">` from your HTML. Read the [`createRoot` usage documentation](/reference/react-dom/client/createRoot#rendering-a-page-partially-built-with-react) to learn more about rendering React components inside an existing HTML page.

When you adopt React in an existing project, it’s common to start with small interactive components (like buttons), and then gradually keep “moving upwards” until eventually your entire page is built with React. If you ever reach that point, we recommend migrating to [a React framework](/learn/start-a-new-react-project) right after to get the most out of React.

## Using React Native in an existing native mobile app[](#using-react-native-in-an-existing-native-mobile-app "Link for Using React Native in an existing native mobile app ")

[React Native](https://reactnative.dev/) can also be integrated into existing native apps incrementally. If you have an existing native app for Android (Java or Kotlin) or iOS (Objective-C or Swift), [follow this guide](https://reactnative.dev/docs/integration-with-existing-apps) to add a React Native screen to it.

[PreviousStart a New React Project](/learn/start-a-new-react-project)

[NextEditor Setup](/learn/editor-setup)

***

----
