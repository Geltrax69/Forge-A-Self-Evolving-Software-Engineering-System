url: https://18.react.dev/reference/react/experimental_taintObjectReference
----

[API Reference](/reference/react)

[APIs](/reference/react/apis)

# experimental\_taintObjectReference[](#undefined "Link for this heading")

### Under Construction

```
experimental_taintObjectReference(message, object);
```

To prevent passing a key, hash or token, see [`taintUniqueValue`](/reference/react/experimental_taintUniqueValue).

* [Reference](#reference)
  * [`taintObjectReference(message, object)`](#taintobjectreference)
* [Usage](#usage)
  * [Prevent user data from unintentionally reaching the client](#prevent-user-data-from-unintentionally-reaching-the-client)

***

## Reference[](#reference "Link for Reference ")

### `taintObjectReference(message, object)`[](#taintobjectreference "Link for this heading")

Call `taintObjectReference` with an object to register it with React as something that should not be allowed to be passed to the Client as is:

```
import {experimental_taintObjectReference} from 'react';



experimental_taintObjectReference(

  'Do not pass ALL environment variables to the client.',

  process.env

);
```

***

## Usage[](#usage "Link for Usage ")

### Prevent user data from unintentionally reaching the client[](#prevent-user-data-from-unintentionally-reaching-the-client "Link for Prevent user data from unintentionally reaching the client ")

A Client Component should never accept objects that carry sensitive data. Ideally, the data fetching functions should not expose data that the current user should not have access to. Sometimes mistakes happen during refactoring. To protect against these mistakes happening down the line we can “taint” the user object in our data API.

```
import {experimental_taintObjectReference} from 'react';



export async function getUser(id) {

  const user = await db`SELECT * FROM users WHERE id = ${id}`;

  experimental_taintObjectReference(

    'Do not pass the entire user object to the client. ' +

      'Instead, pick off the specific properties you need for this use case.',

    user,

  );

  return user;

}
```

Now whenever anyone tries to pass this object to a Client Component, an error will be thrown with the passed in error message instead.

##### Deep Dive#### Protecting against leaks in data fetching[](#protecting-against-leaks-in-data-fetching "Link for Protecting against leaks in data fetching ")

If you’re running a Server Components environment that has access to sensitive data, you have to be careful not to pass objects straight through:

```
// api.js

export async function getUser(id) {

  const user = await db`SELECT * FROM users WHERE id = ${id}`;

  return user;

}
```

```
import { getUser } from 'api.js';

import { InfoCard } from 'components.js';



export async function Profile(props) {

  const user = await getUser(props.userId);

  // DO NOT DO THIS

  return <InfoCard user={user} />;

}
```

```
// components.js

"use client";



export async function InfoCard({ user }) {

  return <div>{user.name}</div>;

}
```

Ideally, the `getUser` should not expose data that the current user should not have access to. To prevent passing the `user` object to a Client Component down the line we can “taint” the user object:

```
// api.js

import {experimental_taintObjectReference} from 'react';



export async function getUser(id) {

  const user = await db`SELECT * FROM users WHERE id = ${id}`;

  experimental_taintObjectReference(

    'Do not pass the entire user object to the client. ' +

      'Instead, pick off the specific properties you need for this use case.',

    user,

  );

  return user;

}
```

Now if anyone tries to pass the `user` object to a Client Component, an error will be thrown with the passed in error message.

[Previoususe](/reference/react/use)

[Nextexperimental\_taintUniqueValue](/reference/react/experimental_taintUniqueValue)

***

----
