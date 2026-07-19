url: https://docs.docker.com/reference/api/extensions-sdk/Dialog/
----

# Interface: Dialog

***

Table of contents

***

Allows opening native dialog boxes.

**`Since`**

0.2.3

## [Methods](#methods)

### [showOpenDialog](#showopendialog)

▸ **showOpenDialog**(`dialogProperties`): `Promise`<[`OpenDialogResult`](https://docs.docker.com/reference/api/extensions-sdk/OpenDialogResult/)>

Display a native open dialog. Lets you select a file or a folder.

```typescript
ddClient.desktopUI.dialog.showOpenDialog({properties: ['openFile']});
```

#### [Parameters](#parameters)

| Name               | Type  | Description                                                                                                                                         |
| ------------------ | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dialogProperties` | `any` | Properties to specify the open dialog behaviour, see <https://www.electronjs.org/docs/latest/api/dialog#dialogshowopendialogbrowserwindow-options>. |

#### [Returns](#returns)

`Promise`<[`OpenDialogResult`](https://docs.docker.com/reference/api/extensions-sdk/OpenDialogResult/)>

----
