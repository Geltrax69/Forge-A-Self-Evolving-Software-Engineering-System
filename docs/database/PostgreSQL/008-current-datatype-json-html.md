url: https://www.postgresql.org/docs/current/datatype-json.html
----

# 8.14. JSON Types

PostgreSQL offers `json` (stores exact input text, reparsed on every use, preserves whitespace/key order/duplicate keys) and `jsonb` (decomposed binary storage, faster to process, supports indexing, does not preserve whitespace/key order/duplicates — last value wins). **Prefer `jsonb`** unless you need `json`'s ordering/duplicate-preservation semantics.

JSON primitive → PostgreSQL type mapping: `string`→`text`, `number`→`numeric` (no NaN/infinity), `boolean`→`boolean` (lowercase `true`/`false` only), `null` is JSON null (distinct from SQL `NULL`).

```sql
SELECT '5'::json;
SELECT '[1, 2, "foo", null]'::json;
SELECT '{"bar": "baz", "balance": 7.77, "active": false}'::json;
SELECT '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::json;
```

`jsonb` reformats output (e.g. drops trailing `e` notation, reorders/dedupes keys); `json` echoes the input verbatim.

## 8.14.3. jsonb Containment and Existence

Containment operator `@>` (works for `jsonb` only, not `json`):

```sql
SELECT '[1, 2, 3]'::jsonb @> '[1, 3]'::jsonb;                 -- true, array order/dupes irrelevant
SELECT '{"product":"PostgreSQL","version":9.4}'::jsonb @> '{"version":9.4}'::jsonb; -- true
SELECT '[1, 2, [1, 3]]'::jsonb @> '[1, 3]'::jsonb;            -- false, not contained one level down
SELECT '["foo", "bar"]'::jsonb @> '"bar"'::jsonb;             -- true, array may contain a scalar
```

Existence operator `?` (top-level key or array element only):

```sql
SELECT '["foo", "bar", "baz"]'::jsonb ? 'bar';    -- true
SELECT '{"foo": "bar"}'::jsonb ? 'foo';           -- true (checks keys, not values)
SELECT '{"foo": {"bar": "baz"}}'::jsonb ? 'bar';  -- false, not top-level
```

Also `?|` (any key in array matches) and `?&` (all keys match).

## 8.14.4. jsonb Indexing

GIN indexes support `jsonb`. Default operator class supports `?`, `?|`, `?&`, `@>`, `@?`, `@@`:

```sql
CREATE INDEX idxgin ON api USING GIN (jdoc);
```

`jsonb_path_ops` operator class supports only `@>`, `@?`, `@@` but produces a smaller, more selective index (hashes value+key-path together instead of indexing keys and values separately):

```sql
CREATE INDEX idxginp ON api USING GIN (jdoc jsonb_path_ops);
```

Expression index for a specific key path (smaller/faster than indexing the whole document):

```sql
CREATE INDEX idxgintags ON api USING GIN ((jdoc -> 'tags'));
-- enables: WHERE jdoc -> 'tags' ? 'qui'
```

Containment query using the whole-document GIN index:

```sql
SELECT jdoc->'guid' FROM api WHERE jdoc @> '{"tags": ["qui"]}';
```

`jsonpath` match operators usable with GIN: `@?` and `@@`:

```sql
SELECT jdoc->'guid' FROM api WHERE jdoc @? '$.tags[*] ? (@ == "qui")';
SELECT jdoc->'guid' FROM api WHERE jdoc @@ '$.tags[*] == "qui"';
```

`btree`/`hash` indexes on `jsonb` are usable too, mainly for whole-document equality checks (ordering: Object > Array > Boolean > Number > String > null).

## 8.14.5. jsonb Subscripting

```sql
SELECT ('{"a": 1}'::jsonb)['a'];
SELECT ('{"a": {"b": {"c": 1}}}'::jsonb)['a']['b']['c'];
SELECT ('[1, "2", null]'::jsonb)[1];

UPDATE table_name SET jsonb_field['key'] = '1';               -- value must be jsonb-typed text
UPDATE table_name SET jsonb_field['a']['b']['c'] = '1';
SELECT * FROM table_name WHERE jsonb_field['key'] = '"value"';
```

If the source is SQL `NULL`, assignment creates an empty object/array as implied by the subscript. Assigning past an array's end pads with JSON `null`s. Missing intermediate objects/arrays along the path are auto-created; an existing non-object/array value along the path raises an error.

## 8.14.7. jsonpath Type

Implements the SQL/JSON path language for querying JSON with JavaScript-like syntax (`.` for member access, `[]` for 0-based array access).

Variables: `$` (context item), `$varname` (named parameter), `@` (current filter-expression result).

Accessors: `.key`, `.*` (wildcard member), `.**` (recursive wildcard, PostgreSQL extension), `[index]`, `[start to end]` (slice), `[*]` (all array elements). Use the `last` keyword for the final array index.

```sql
SELECT jsonb_path_query(jdoc, '$.tags[*] ? (@ == "qui")') FROM api;
```

----
