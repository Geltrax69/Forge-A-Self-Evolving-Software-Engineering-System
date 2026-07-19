url: https://react.dev/learn/react-developer-tools
----

[Learn React](/learn)

[Setup](/learn/setup)

```
# Yarn

yarn global add react-devtools



# Npm

npm install -g react-devtools
```

Next open the developer tools from the terminal:

```
react-devtools
```

Then connect your website by adding the following `<script>` tag to the beginning of your website’s `<head>`:

```
<html>

  <head>

    <script src="http://localhost:8097"></script>
```

Reload your website in the browser now to view it in developer tools.

## Mobile (React Native)[](#mobile-react-native "Link for Mobile (React Native) ")

To inspect apps built with [React Native](https://reactnative.dev/), you can use [React Native DevTools](https://reactnative.dev/docs/react-native-devtools), the built-in debugger that deeply integrates React Developer Tools. All features work identically to the browser extension, including native element highlighting and selection.

[Learn more about debugging in React Native.](https://reactnative.dev/docs/debugging)

> For versions of React Native earlier than 0.76, please use the standalone build of React DevTools by following the [Safari and other browsers](#safari-and-other-browsers) guide above.

[PreviousUsing TypeScript](/learn/typescript)

[NextReact Compiler](/learn/react-compiler)

***

----
