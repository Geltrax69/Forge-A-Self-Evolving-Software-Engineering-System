url: https://docs.docker.com/reference/api/extensions-sdk/Host/
----

# Interface: Host

***

Table of contents

***

**`Since`**

0.2.0

## [Methods](#methods)

### [openExternal](#openexternal)

▸ **openExternal**(`url`): `void`

Opens an external URL with the system default browser.

**`Since`**

0.2.0

```typescript
ddClient.host.openExternal("https://docker.com");
```

#### [Parameters](#parameters)

| Name  | Type     | Description                                                               |
| ----- | -------- | ------------------------------------------------------------------------- |
| `url` | `string` | The URL the browser will open (must have the protocol `http` or `https`). |

#### [Returns](#returns)

`void`

## [Properties](#properties)

### [platform](#platform)

• **platform**: `string`

Returns a string identifying the operating system platform. See <https://nodejs.org/api/os.html#osplatform>

**`Since`**

0.2.2

***

### [arch](#arch)

• **arch**: `string`

Returns the operating system CPU architecture. See <https://nodejs.org/api/os.html#osarch>

**`Since`**

0.2.2

***

### [hostname](#hostname)

• **hostname**: `string`

Returns the host name of the operating system. See <https://nodejs.org/api/os.html#oshostname>

**`Since`**

0.2.2

----
