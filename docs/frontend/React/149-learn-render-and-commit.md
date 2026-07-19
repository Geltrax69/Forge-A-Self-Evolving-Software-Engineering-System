url: https://18.react.dev/learn/render-and-commit
----

[Fork](https://codesandbox.io/api/v1/sandboxes/define?parameters=N4IgZglgNgpgziAXKOAnAxgeggOwCYwAeAdAFYLIjoD2OALjPUiBALYAO1qdABAJKsAhgHMYPMKmqseAcmKYBImGTgyA3AB0cbTtx7Ae6VDEEMAStWq8AvuMnSZxwejoBaPFMzooERnXVaWjQ4cLySVjwAvIZO5pZ0ABQe6ACurH7EonQAorDp9ABCAJ58eAmO8TIAlFVa4XTExvgwqAkAPIqiPJgAfFWaOCAANCxwBbiCqEVIYIJQcDDWI-zOANZKKrRIoMEMTIggwFo8PBogOILpZ4inIE4uxAQAbmdDx7dPLXAQtNe3AAzEQH_V7vM5CXB_M6YNBYXAEEjkUE4E5nOBGCDsOhwP5HFEnW6hSZ0KF3EwuVzo1CY7E8IncZEE24AIxS0DwpPubipNLgPFZ7MZBLODFCnPJ3IxWL5ot4rlcjCekXIHlYQtRIBgpBgLnFzkl1OlPC1OpJIHeSzBIAI7EYBBw6F8OKQ-neGq5pIAegBGAAcQKB6tuXPcUi9foDIOGbuDEspUuxXoArJGzha3vizs8ACIwW3NB1O3HWLTWYajcYXKYzOYLJYgdgpZk-OHNEgACzorCg2yotD2dGYbQAhNmAPIAYQAKgBNAAK2R4ne7PS0bWXUB4UEEOGEkTOjDOq5w65MeGPJza6TogkM7cmCzo-5AAFUpwAxVy-o_vK8wG88Bc6TPk8vgAO66Gahj9n4z5gRAeB0O2kTPBA6AwK48GIe2Qw8LgEB0BAczxnMMCRN6gYgBePBtIRdCwD02bUKk-R0G0mB0Qxa6YO2Z7Hm0zLUHgRTUW0eAQE8eF4M-9RHux4lPPxmCCcJSkbj05YQGMEzVogszzIsIywgoQiiCova7H4zBEJBPAELMKRQLwYApA6hG0PwpkwAkVSuvixh0CkqAogkMZtGwwgxicsLPp2dDsHAiCYNgxARUFxA0KwmAAFrvgAbHA3oAJwAExkOwkXmviTJzE-ZwyO-UBcHMWk8AA4owACX1LoIIMj8kUPDZHgKSTB4PATqYcw7tQNy3sIEDCDuhHoDw15zC24hNWBLR0qkUBYkFYjwUhPDGGAsAuBJYi2je8xptV3TUf0pZaJp2lVtMem1oZIDGaERSwHAGVwBQOwwfsIAAFR-ScgmEJSEAAF64MINyCagBCoK48MDCWOBaCpg14icYD9q4sysNARQ3HAO5wJSLQQGAAwnEIqALTgNwlf87CEKzPArHg4m7jc_x44EODtt6sNrZMnOuHQ1DsGLAtk_QiNIzA3MlXzEsE1LJWy-zCtKyrPDi-86vcsj2s8DzeuvQb7YAMzG_LuCK8rqtW-T3xazcfqOzg-NaO2AAs7sc57Zs-_i1ua3b3p5cHodS0mUem97Ftq37tuB-HqeS-2eWZzH2eW_HecBzw3q6_zTtBEJYgk-I1dJ8QJUwKw-taI5stCyLwiuLgPg4Bh9J0NzvMNyHkvvZWkxffpdb1gwHDbgwzBGCYDCuCGgjsOwIDWEAA\&query=file%3D%252Fsrc%252Findex.js%26utm_medium%3Dsandpack\&environment=create-react-app "Open in CodeSandbox")

```
import Image from './Image.js';
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'))
root.render(<Image />);
```

```
export default function Gallery() {
  return (
    <section>
      <h1>Inspiring Sculptures</h1>
      <Image />
      <Image />
      <Image />
    </section>
  );
}

function Image() {
  return (
    <img
      src="https://i.imgur.com/ZF6s192.jpg"
      alt="'Floralis Genérica' by Eduardo Catalano: a gigantic metallic flower sculpture with reflective petals"
    />
  );
}
```

```
export default function Clock({ time }) {
  return (
    <>
      <h1>{time}</h1>
      <input />
    </>
  );
}
```

***

----
