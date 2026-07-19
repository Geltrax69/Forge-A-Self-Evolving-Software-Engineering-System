url: https://www.postgresql.org/docs/current/queries-select-lists.html, queries-union.html, queries-order.html, queries-limit.html
----

# 7.3. Select Lists

## 7.3.1. Select-List Items

`*` emits all columns. Otherwise a comma-separated list of value expressions:

```sql
SELECT a, b, c FROM ...
SELECT tbl1.a, tbl2.a, tbl1.b FROM ...   -- disambiguate same-named columns
SELECT tbl1.*, tbl2.a FROM ...
```

Expressions don't need to reference `FROM` columns at all — constants and arbitrary expressions are fine.

## 7.3.2. Column Labels

```sql
SELECT a AS value, b + c AS sum FROM ...
SELECT a AS from, b + c AS sum FROM ...   -- AS or quoting needed if the label collides with a keyword
SELECT a "from", b + c AS sum FROM ...
```

Always write `AS` or double-quote the output name for future-proofing against new keywords.

## 7.3.3. DISTINCT

```sql
SELECT DISTINCT select_list ...
```

Two rows are distinct if they differ in any column; nulls are considered equal for this purpose. `ALL` is the (default) opposite of `DISTINCT`.

```sql
SELECT DISTINCT ON (expression [, expression ...]) select_list ...
```

Keeps only the first row of each group of rows sharing equal `expression` values — "first" is unpredictable unless the query is also sorted to guarantee it. (`DISTINCT ON` runs after `ORDER BY` sorting.) Not standard SQL; can be avoided with `GROUP BY` and subqueries, but is often the most convenient option.

# 7.4. Combining Queries (UNION, INTERSECT, EXCEPT)

```
query1 UNION [ALL] query2
query1 INTERSECT [ALL] query2
query1 EXCEPT [ALL] query2
```

`UNION` appends and de-duplicates (unless `ALL`). `INTERSECT` keeps rows present in both. `EXCEPT` keeps rows in query1 not in query2. Queries must be "union compatible" (same number of columns, compatible types).

Precedence: `UNION`/`EXCEPT` associate left-to-right; `INTERSECT` binds tighter than both, so `q1 UNION q2 INTERSECT q3` means `q1 UNION (q2 INTERSECT q3)`. Use parentheses around an individual query if it needs its own `LIMIT`/`ORDER BY`, otherwise those clauses apply to the whole combined result:

```sql
SELECT a FROM b UNION SELECT x FROM y LIMIT 10;
-- means (SELECT a FROM b UNION SELECT x FROM y) LIMIT 10, not the other grouping
```

# 7.5. Sorting Rows (ORDER BY)

```sql
SELECT select_list
    FROM table_expression
    ORDER BY sort_expression1 [ASC | DESC] [NULLS { FIRST | LAST }]
             [, sort_expression2 ...];
```

Default is `ASC`; nulls sort as larger than any non-null value by default (`NULLS FIRST` is default for `DESC`, `NULLS LAST` otherwise). Ordering options apply independently per column — `ORDER BY x, y DESC` means `x ASC, y DESC`.

Sort by output column label or position:

```sql
SELECT a + b AS sum, c FROM table1 ORDER BY sum;
SELECT a, max(b) FROM table1 GROUP BY a ORDER BY 1;
```

An output column name must stand alone in `ORDER BY` (can't be embedded in an expression). `ORDER BY` on a `UNION`/`INTERSECT`/`EXCEPT` result can only reference output names/numbers, not arbitrary expressions.

# 7.6. LIMIT and OFFSET

```sql
SELECT select_list
    FROM table_expression
    [ ORDER BY ... ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start ];
```

`OFFSET` rows are skipped before counting `LIMIT` rows. Without `ORDER BY`, LIMIT/OFFSET pagination is unpredictable — the planner may choose different plans (and thus different row orders) for different LIMIT/OFFSET values. Rows skipped by OFFSET are still computed server-side, so large OFFSETs can be inefficient — prefer keyset pagination (`WHERE id > last_seen_id ORDER BY id LIMIT n`) for deep pagination.

----
