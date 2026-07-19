url: https://www.postgresql.org/docs/current/indexes-types.html
----

# 11.2. Index Types

PostgreSQL provides several index types: B-tree, Hash, GiST, SP-GiST, GIN, BRIN (plus the `bloom` extension). `CREATE INDEX` defaults to B-tree. Select another type with `USING`:

```sql
CREATE INDEX name ON table USING HASH (column);
```

## 11.2.1. B-Tree

Handles equality and range queries: `<  <=  =  >=  >`, plus `BETWEEN`, `IN`, `IS NULL`/`IS NOT NULL`. Also usable for anchored pattern matching (`col LIKE 'foo%'`, `col ~ '^foo'`) — needs a special operator class for non-C locales. Can also satisfy `ORDER BY` directly, avoiding a sort step.

## 11.2.2. Hash

Stores a 32-bit hash of the column value; supports only `=` comparisons.

## 11.2.3. GiST

Not a single index type but infrastructure for many strategies (operator classes) — e.g. built-in 2D geometric operators: `<<  &<  &>  >>  <<|  &<|  |&>  |>>  @>  <@  ~=  &&`. Also supports nearest-neighbor search:

```sql
SELECT * FROM places ORDER BY location <-> point '(101,456)' LIMIT 10;
```

## 11.2.4. SP-GiST

Infrastructure for non-balanced disk-based structures (quadtrees, k-d trees, tries). Built-in 2D point operators: `<<  >>  ~=  <@  <<|  |>>`. Also supports nearest-neighbor search for operator classes that provide it.

## 11.2.5. GIN

"Inverted index" for values containing multiple components (e.g. arrays), one entry per component value. Built-in array operator class supports: `<@  @>  =  &&`.

## 11.2.6. BRIN

Block Range INdexes — store per-block-range summaries (e.g. min/max), most effective when column values correlate with physical row order. Supports `<  <=  =  >=  >` for linearly-ordered types. Much smaller than B-tree but less precise; great for append-mostly time-series tables.

----
