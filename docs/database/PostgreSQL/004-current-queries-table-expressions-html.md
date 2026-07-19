url: https://www.postgresql.org/docs/current/queries-table-expressions.html
----

# 7.2. Table Expressions

A table expression computes a table: a `FROM` clause optionally followed by `WHERE`, `GROUP BY`, and `HAVING` clauses, forming a pipeline of transformations that produces the virtual table passed to the select list.

## 7.2.1. The FROM Clause

```
FROM table_reference [, table_reference [, ...]]
```

Multiple table references are cross-joined (Cartesian product).

### Joined Tables

```
T1 join_type T2 [ join_condition ]
```

**Cross join**: `T1 CROSS JOIN T2` — every combination of rows (N*M rows). Equivalent to `T1 INNER JOIN T2 ON TRUE`, and to `FROM T1, T2`.

**Qualified joins**:
```
T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 ON boolean_expression
T1 { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2 USING ( join column list )
T1 NATURAL { [INNER] | { LEFT | RIGHT | FULL } [OUTER] } JOIN T2
```

- `INNER JOIN`: rows from T1 matched with rows in T2 satisfying the condition.
- `LEFT OUTER JOIN`: inner join plus one row per unmatched T1 row (T2 columns null).
- `RIGHT OUTER JOIN`: inner join plus one row per unmatched T2 row (T1 columns null).
- `FULL OUTER JOIN`: unmatched rows from both sides included with nulls on the other side.

`ON` takes any boolean expression. `USING (a, b)` is shorthand for `ON T1.a = T2.a AND T1.b = T2.b`, and also de-duplicates the shared columns in the output (unlike `ON`, which outputs all of T1's columns then all of T2's columns). `NATURAL` auto-matches on all identically named columns in both tables — risky if the schema changes.

A restriction in the `ON` clause is applied *before* the join (matters for outer joins); a restriction in `WHERE` is applied *after* the join.

```sql
SELECT ... FROM t1 LEFT JOIN t2 ON t1.id = t2.id AND t2.val > 100;   -- different from:
SELECT ... FROM t1 LEFT JOIN t2 ON t1.id = t2.id WHERE t2.val > 100;
```

### Table and Column Aliases

```
FROM table_reference [AS] alias
FROM table_reference [AS] alias ( column1 [, column2 [, ...]] )
```

Required for self-joins:

```sql
SELECT * FROM people AS mother JOIN people AS child ON mother.id = child.mother_id;
```

### Subqueries

```sql
FROM (SELECT * FROM table1) AS alias_name
FROM (VALUES ('anne','smith'), ('bob','jones')) AS names(first, last)
```

A subquery in `FROM` must be aliased in standard SQL (PostgreSQL allows omitting it, but don't for portability).

### Table Functions

Functions producing a set of rows, usable like a table. Combine several with `ROWS FROM(...)`, optionally with `WITH ORDINALITY` to add a row-number column.

```sql
CREATE FUNCTION getfoo(int) RETURNS SETOF foo AS $$
    SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;

SELECT * FROM getfoo(1) AS t1;
```

For functions returning `record` with no `OUT` params, the caller must specify the row structure:

```sql
SELECT *
    FROM dblink('dbname=mydb', 'SELECT proname, prosrc FROM pg_proc')
      AS t1(proname name, prosrc text)
    WHERE proname LIKE 'bytea%';
```

### LATERAL Subqueries

`LATERAL` lets a subquery/function in `FROM` reference columns from preceding `FROM` items:

```sql
SELECT * FROM foo, LATERAL (SELECT * FROM bar WHERE bar.id = foo.bar_id) ss;

SELECT p1.id, p2.id, v1, v2
FROM polygons p1, polygons p2,
     LATERAL vertices(p1.poly) v1,
     LATERAL vertices(p2.poly) v2
WHERE (v1 <-> v2) < 10 AND p1.id != p2.id;
```

`LEFT JOIN LATERAL` is handy so source rows survive even when the lateral subquery yields nothing:

```sql
SELECT m.name
FROM manufacturers m LEFT JOIN LATERAL get_product_names(m.id) pname ON true
WHERE pname IS NULL;
```

## 7.2.2. The WHERE Clause

```
WHERE search_condition
```

Rows for which the condition is true survive; false/null rows are discarded. An inner join's condition can live in `WHERE` or `ON` — equivalent for inner joins, but outer joins must put the join condition in `ON` (a `WHERE` condition on the outer side would effectively cancel the outer-join semantics).

```sql
SELECT ... FROM fdt WHERE c1 IN (SELECT c1 FROM t2)
SELECT ... FROM fdt WHERE EXISTS (SELECT c1 FROM t2 WHERE c2 > fdt.c1)
```

## 7.2.3. GROUP BY and HAVING

```sql
SELECT x, sum(y) FROM test1 GROUP BY x;
```

Rows sharing the same grouped-by values collapse into one row; non-grouped columns can only appear inside aggregate expressions.

```sql
SELECT product_id, p.name, (sum(s.units) * p.price) AS sales
    FROM products p LEFT JOIN sales s USING (product_id)
    GROUP BY product_id, p.name, p.price;
```

PostgreSQL extends standard SQL by allowing `GROUP BY` on select-list aliases and arbitrary value expressions.

`HAVING` filters *groups* (post-aggregation), unlike `WHERE` which filters rows pre-aggregation:

```sql
SELECT product_id, p.name, (sum(s.units) * (p.price - p.cost)) AS profit
    FROM products p LEFT JOIN sales s USING (product_id)
    WHERE s.date > CURRENT_DATE - INTERVAL '4 weeks'
    GROUP BY product_id, p.name, p.price, p.cost
    HAVING sum(p.price * s.units) > 5000;
```

Aggregate calls with no `GROUP BY` collapse the whole input into a single group row.

## 7.2.4. GROUPING SETS, CUBE, and ROLLUP

```sql
SELECT * FROM ... GROUP BY GROUPING SETS ((a), (b), ());
```

`ROLLUP (e1, e2, e3)` = all prefixes: `(e1,e2,e3), (e1,e2), (e1), ()` — good for hierarchical subtotals (dept → division → company).

`CUBE (a, b, c)` = the full power set of the given columns (all 2^n combinations).

`GROUP BY DISTINCT ...` removes duplicate grouping sets that would otherwise arise from combining multiple `ROLLUP`/`CUBE`/`GROUPING SETS` items (Cartesian product of grouping items).

## 7.2.5. Window Function Processing

Window functions are evaluated *after* grouping, aggregation, and `HAVING` — they see group rows, not raw rows, when the query also aggregates. Functions sharing identical `PARTITION BY`/`ORDER BY` are guaranteed a consistent row ordering; functions with differing specs are not. Use an explicit top-level `ORDER BY` if you need a specific final row order — window functions require presorted input internally but that doesn't guarantee your output order.

----
