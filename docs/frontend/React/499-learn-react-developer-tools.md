url: https://18.react.dev/learn/react-developer-tools
----

[Learn React](/learn)

[Installation](/learn/installation)

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

React Developer Tools can be used to inspect apps built with [React Native](https://reactnative.dev/) as well.

The easiest way to use React Developer Tools is to install it globally:

```
# Yarn

yarn global add react-devtools



# Npm

npm install -g react-devtools
```

Next open the developer tools from the terminal.

```
react-devtools
```

It should connect to any local React Native app that’s running.

> Try reloading the app if developer tools doesn’t connect after a few seconds.

[Learn more about debugging React Native.](https://reactnative.dev/docs/debugging)

[PreviousUsing TypeScript](/learn/typescript)

[NextReact Compiler](/learn/react-compiler)

***

----
