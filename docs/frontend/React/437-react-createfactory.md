url: https://18.react.dev/reference/react/createFactory
----

[API Reference](/reference/react)

[Legacy React APIs](/reference/react/legacy)

# createFactory[](#undefined "Link for this heading")

### Deprecated

This API will be removed in a future major version of React. [See the alternatives.](#alternatives)

`createFactory` lets you create a function that produces React elements of a given type.

```
const factory = createFactory(type)
```

* [Reference](#reference)
  * [`createFactory(type)`](#createfactory)

* [Usage](#usage)
  * [Creating React elements with a factory](#creating-react-elements-with-a-factory)

* [Alternatives](#alternatives)

  * [Copying `createFactory` into your project](#copying-createfactory-into-your-project)
  * [Replacing `createFactory` with `createElement`](#replacing-createfactory-with-createelement)
  * [Replacing `createFactory` with JSX](#replacing-createfactory-with-jsx)

***

## Reference[](#reference "Link for Reference ")

### `createFactory(type)`[](#createfactory "Link for this heading")

Call `createFactory(type)` to create a factory function which produces React elements of a given `type`.

```
import { createFactory } from 'react';



const button = createFactory('button');
```

Then you can use it to create React elements without JSX:

```
export default function App() {

  return button({

    onClick: () => {

      alert('Clicked!')

    }

  }, 'Click me');

}
```

[See more examples below.](#usage)

#### Parameters[](#parameters "Link for Parameters ")

* `type`: The `type` argument must be a valid React component type. For example, it could be a tag name string (such as `'div'` or `'span'`), or a React component (a function, a class, or a special component like [`Fragment`](/reference/react/Fragment)).

#### Returns[](#returns "Link for Returns ")

Returns a factory function. That factory function receives a `props` object as the first argument, followed by a list of `...children` arguments, and returns a React element with the given `type`, `props` and `children`.

***

## Usage[](#usage "Link for Usage ")

### Creating React elements with a factory[](#creating-react-elements-with-a-factory "Link for Creating React elements with a factory ")

Although most React projects use [JSX](/learn/writing-markup-with-jsx) to describe the user interface, JSX is not required. In the past, `createFactory` used to be one of the ways you could describe the user interface without JSX.

Call `createFactory` to create a *factory function* for a specific element type like `'button'`:

```
import { createFactory } from 'react';



const button = createFactory('button');
```

Calling that factory function will produce React elements with the props and children you have provided:

```
import { createFactory } from 'react';

const button = createFactory('button');

export default function App() {
  return button({
    onClick: () => {
      alert('Clicked!')
    }
  }, 'Click me');
}
```

This is how `createFactory` was used as an alternative to JSX. However, `createFactory` is deprecated, and you should not call `createFactory` in any new code. See how to migrate away from `createFactory` below.

***

## Alternatives[](#alternatives "Link for Alternatives ")

### Copying `createFactory` into your project[](#copying-createfactory-into-your-project "Link for this heading")

If your project has many `createFactory` calls, copy this `createFactory.js` implementation into your project:

```
import { createFactory } from './createFactory.js';

const button = createFactory('button');

export default function App() {
  return button({
    onClick: () => {
      alert('Clicked!')
    }
  }, 'Click me');
}
```

This lets you keep all of your code unchanged except the imports.

***

### Replacing `createFactory` with `createElement`[](#replacing-createfactory-with-createelement "Link for this heading")

If you have a few `createFactory` calls that you don’t mind porting manually, and you don’t want to use JSX, you can replace every call a factory function with a [`createElement`](/reference/react/createElement) call. For example, you can replace this code:

```
import { createFactory } from 'react';



const button = createFactory('button');



export default function App() {

  return button({

    onClick: () => {

      alert('Clicked!')

    }

  }, 'Click me');

}
```

with this code:

```
import { createElement } from 'react';



export default function App() {

  return createElement('button', {

    onClick: () => {

      alert('Clicked!')

    }

  }, 'Click me');

}
```

Here is a complete example of using React without JSX:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?parameters=N4IgZglgNgpgziAXKOAnAxgeggOwCYwAeAdAFYLIjoD2OALjPUiBALYAO1qdABAEowAhujoAaHsB4BlOqggiAstQI8AvjzCpqrHgB0QqISP0BuXTjaduEnukOCGfatV7rN2vQaN0AtHm2Y6FAQjHSm5pZcvPrEmHB0AJ6wcMTocHDhOBEcUTwAguzsGlo6MZgF7JnmNDjxPFouPAC8tvaOznQAFP7oAK6socQA5jB0AKKwA_QAQgkAknid-g1hIACUa2Y4K8SG-DCoSzg8PAA8MnKKyjAAfOYnJ6cVPJh3x2eYF_J0SgRvmyBRCw4NNcIJUAkkGBBFA4DBVED2MIANaCEZkOC0JCgGoMJiIEDAe6eHCCAb6RCeewiYgEABu-lExP0dIOcAgtApngADMRedzGcyQKxBLgufo4hhsPsSORBe99HA7BB2HQMkgJMSToq6ODVpTlt4fEq5Kq4Dx4nr5Q9PAAjXrQPDirzCXwmlVqnj2x3Wh76BjxZ3Ut3Ks08AO8Hw-Rh0prkfysX3akAwUgwYwaw2u42hz2p9OrYkIoUEdiMAg4dAhdWUonvZPB50APQAjAAOPl8pNUo0J5vtzsCwFanvZ91m5sAVkH-iLTIVIHpABEYGX9pXq1zgKpzKpAcDQaSIVCYXCESB2L1bcEsLgCCQABZ0VhQbFUWh4ujMU4AQiXAHkAGEABUAE0AAUxh4J8XzeU4YKgHgoEEHAhiafRGH0OCHyEPA3keAZdVsB9wThOh0JAABVYCADEfDbLDiVOQjBB4UkBgoukQgAdysVZbA_UIKO4iA8DoB8mnpeQYB8ESxIfcRcAgOgIBhHMYRgJoWy7EB8LOFS6FgG4l2oPopjoU5MAMozzEsnDBDw2zbWUBI9NOPAIDpHhRIolYsMsjy6TgzBnLwVzbMwBCbn3CAQTBY9EGhWF4SBNAsAqDE31xUJmEiaxJDsIQGAmGBzLUYoPAAcmDSqtnMIg-J4AhoV6KBeDAXpKxU2h8kKTo1k1d5DDoXpUGOQqHBgErzM6Sr7ToOhaEq8Q6xtWhAJvZFKX65obkGm0Tg07hZo2-RkRgPAf0qtYRx3d4ER4SrTvQZEeAGa6tjumK4qPSFEtPFKQDSuJEmSVJ0iywT8RAAAqfavWoQhjQgAAvXAhkpZzUAIVAfGcwhPvMcxQoSeGwA_HxoVYaAEkpOAULgY0DggMAthOEVUCGXBKQAJm5dgCeJJE8A81DKW5QmshwB8W3hjmuZwHxFvYcW2Y0Cn2RRmBeZ5gXJfMB8ebl8EFaV6gVZ4CXiXJ-hka13n-cFnA7oNgBmY3OdwM2Lat94bbdVHtZ4ds9d3InpYAFg903ldV62NcDykWwANlD53w4fSdo692PLbV_27aDlsI7Tl3peT7PFdz32TgLzWi91p2y5oFRVvV2366T4gedK_WcFa-HhdFoYfFwYIcBky1uAd0vw--w9wT-pKz3PBgOGQhhmAmhgfGDHxBEKEBVCAA\&query=file%3D%252Fsrc%252FApp.js%26utm_medium%3Dsandpack\&environment=create-react-app "Open in CodeSandbox")

```
import { createElement } from 'react';

export default function App() {
  return createElement('button', {
    onClick: () => {
      alert('Clicked!')
    }
  }, 'Click me');
}
```

***

### Replacing `createFactory` with JSX[](#replacing-createfactory-with-jsx "Link for this heading")

Finally, you can use JSX instead of `createFactory`. This is the most common way to use React:

[Fork](https://codesandbox.io/api/v1/sandboxes/define?parameters=N4IgZglgNgpgziAXKOAnAxgeggOwCYwAeAdAFYLIjoD2OALjPUiBALYAO1qdABAEowAhujoAaHsB4BlOqggiAstQI8AvjzCpqrHgB0QqISP0BuXTjaduEnukOCGfatV7rN2vQaN0AtHm2Y6FAQjHSm5pZcvPrEmHB0AJ6wcMTocHDhOBEcUTwAguzsGlo6MZgF7JnmNDjxPFouPAC8tvaOznQAFP7oAK6socQA5jB0AKKwA_QAQgkAknid-g1hIACUa2Y4K8SG-DCoSzg8PAA8MnKKyjAAfOYnJ6cVPJh3x2eYF_J0SgRvmyBRCw4NNcIJUAkkGBBFA4DBVED2MIANaCEZkOC0JCgGoMJiIEDAe6eHCCAb6RCeewiYgEABu-lExP0dIOcAgtApngADMRedzGcyQKxBLgufo4hhsPsSORBe99HA7BB2HQMkgJMSToq6ODVpTlt4fEq5Kq4Dx4nr5Q9PAAjXrQPDirzCXwmlVqnj2x3Wh76BjxZ3Ut3Ks08AO8Hw-Rh0prkfysX3akAwUgwYwaw2u42hz2p9OrYkIoUEdiMAg4dAhdWUonvZPB50APQAjAAOPl8pNUo0J5vtzsCwFanvZ91m5sAVkH-iLTIVIHpABEYGX9pXq1zgKpzKpAcDQaSIVCYXCESB2L1bcEsLgCCQABZ0VhQbFUWh4ujMU4AQiXAHkAGEABUAE0AAUxh4J8XzeU4YKgHgoEEHAhiafRGH0OCHyEPA3keAZdVsB9wThOh0JAABVYCADEfDbLDiVOQjBB4UkBgoukQgAdysVZbA_UIKO4iA8DoB8mnpeQYB8ESxIfcRcAgOgIBhHMYRgJoWy7EB8LOFS6FgG4l2oPopjoU5MAMozzEsnDBDw2zbWUBI9NOPAIDpHhRIolYsMsjy6TgzBnLwVzbMwBCbn3CAQTBY9EGhWF4SBNAsAqDE31xUJmCIPieAIaFeigXgwF6SsVNofJCk6NZNXeQw6F6VBjiOG1TntOg6Cq2hAJvZEmmAWrmhueqbRODTuE6AByPr5GRGA8B_abNhHVRVD0m05vQZEeHJesPk67qcD01acFULYYrio9IUS08UpANK4kSZJUnSLLBPxEAACoxq9ahCGNCAAC9cCGSlnNQAhUB8ZzCC2HcshwUKEj-sAPx8aFWGgBJKTgFC4GNA4IDALYThFVAhlwSkACZuXYeHiSRPAPNQyluQR8xzAfFs_opqmcB8br2HZsmNAx9lgZgWmaYZzmkYfGm-fBAWheoEWeA54l0foIGpdp-nGfOrmcAfABmZXKdwNWNa194dbdEHpZ4ds5d3E2HwAFkt1XhdF7WJadykWwANjd42FcnH3rb9zWxYdvXnZbT3w8R7mQ-jwXY7tk4E8lpPZaNtPK2uNHA_1l3iBpmBWHl8xir-5nWaGHxcGCHAZMtbgDdTk2rsPcFbqSs9zwYDhkIYZg7CEBgfGDHxBEKEBVCAA\&query=file%3D%252Fsrc%252FApp.js%26utm_medium%3Dsandpack\&environment=create-react-app "Open in CodeSandbox")

```
export default function App() {
  return (
    <button onClick={() => {
      alert('Clicked!');
    }}>
      Click me
    </button>
  );
};
```

### Pitfall

Sometimes, your existing code might pass some variable as a `type` instead of a constant like `'button'`:

```
function Heading({ isSubheading, ...props }) {

  const type = isSubheading ? 'h2' : 'h1';

  const factory = createFactory(type);

  return factory(props);

}
```

To do the same in JSX, you need to rename your variable to start with an uppercase letter like `Type`:

```
function Heading({ isSubheading, ...props }) {

  const Type = isSubheading ? 'h2' : 'h1';

  return <Type {...props} />;

}
```

Otherwise React will interpret `<type>` as a built-in HTML tag because it is lowercase.

[PreviouscreateElement](/reference/react/createElement)

[NextcreateRef](/reference/react/createRef)

***

----
