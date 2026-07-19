url: https://www.postgresql.org/docs/current/queries-with.html
----

# 7.8. WITH Queries (Common Table Expressions)

`WITH` defines auxiliary statements (CTEs) usable by a larger query. Each auxiliary statement can be `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `MERGE`; so can the primary statement.

## 7.8.1. SELECT in WITH

```sql
WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
), top_regions AS (
    SELECT region
    FROM regional_sales
    WHERE total_sales > (SELECT SUM(total_sales)/10 FROM regional_sales)
)
SELECT region, product, SUM(quantity) AS product_units, SUM(amount) AS product_sales
FROM orders
WHERE region IN (SELECT region FROM top_regions)
GROUP BY region, product;
```

## 7.8.2. Recursive Queries

`WITH RECURSIVE` lets a CTE refer to its own output:

```sql
WITH RECURSIVE t(n) AS (
    VALUES (1)
  UNION ALL
    SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;
```

Form: non-recursive term, `UNION`/`UNION ALL`, recursive term (only the recursive term may reference the CTE's own output). Evaluation: run the non-recursive term into a working table and the result set; then repeatedly run the recursive term against the current working table's contents, appending new rows to the result and to a new working table, until the working table comes up empty.

Hierarchical example — all sub-parts of a product:

```sql
WITH RECURSIVE included_parts(sub_part, part, quantity) AS (
    SELECT sub_part, part, quantity FROM parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part, p.quantity * pr.quantity
    FROM included_parts pr, parts p
    WHERE p.part = pr.sub_part
)
SELECT sub_part, SUM(quantity) as total_quantity
FROM included_parts
GROUP BY sub_part;
```

### Search order (depth/breadth-first)

Built-in syntax to compute an ordering column:

```sql
WITH RECURSIVE search_tree(id, link, data) AS (
    SELECT t.id, t.link, t.data FROM tree t
  UNION ALL
    SELECT t.id, t.link, t.data FROM tree t, search_tree st WHERE t.id = st.link
) SEARCH DEPTH FIRST BY id SET ordercol
SELECT * FROM search_tree ORDER BY ordercol;
```

(replace with `SEARCH BREADTH FIRST BY id SET ordercol` for breadth-first).

### Cycle detection

Built-in syntax:

```sql
WITH RECURSIVE search_graph(id, link, data, depth) AS (
    SELECT g.id, g.link, g.data, 1 FROM graph g
  UNION ALL
    SELECT g.id, g.link, g.data, sg.depth + 1
    FROM graph g, search_graph sg
    WHERE g.id = sg.link
) CYCLE id SET is_cycle USING path
SELECT * FROM search_graph;
```

`CYCLE` names the columns to track for cycle detection, a boolean output column flagging a detected cycle, and a path-tracking column — internally expanded to an array-of-visited-values check (`g.id = ANY(path)`), with `NOT is_cycle` added to the recursive term's `WHERE`.

Testing tip: put a `LIMIT` on the *parent* query while developing a possibly-looping recursive CTE — PostgreSQL only evaluates as many rows as the parent actually fetches (don't rely on this in production; other engines differ, and it stops helping once you add sorting/joins on the CTE output).

## 7.8.3. CTE Materialization

A `WITH` query used more than once is evaluated only once by default (materialized) — good for expensive/side-effecting sub-queries used multiple times, but the optimizer cannot push parent-query restrictions into a multiply-referenced CTE.

A non-recursive, side-effect-free (no volatile functions) CTE referenced exactly once is folded into the parent query by default, enabling joint optimization (e.g. index usage). Override with `MATERIALIZED` (force separate evaluation) or `NOT MATERIALIZED` (force folding, risking duplicate computation):

```sql
WITH w AS NOT MATERIALIZED (
    SELECT * FROM big_table
)
SELECT * FROM w AS w1 JOIN w AS w2 ON w1.key = w2.ref
WHERE w2.key = 123;
```

lets `w2.key = 123` push down into scans of `big_table`. Conversely, keep `MATERIALIZED` (the default when referenced twice) when the CTE body does expensive work you don't want repeated, e.g. `very_expensive_function(val)`.

## 7.8.4. Data-Modifying Statements in WITH

```sql
WITH moved_rows AS (
    DELETE FROM products
    WHERE "date" >= '2010-10-01' AND "date" < '2010-11-01'
    RETURNING *
)
INSERT INTO products_log
SELECT * FROM moved_rows;
```

Key rules:
- The `WITH` clause attaches to the top-level statement (data-modifying CTEs aren't allowed nested inside a plain sub-`SELECT`).
- It's the `RETURNING` output — not the target table — that forms the "temporary table" other parts of the query see. No `RETURNING` means no way to reference that CTE's output (but it still executes).
- All sibling `WITH` sub-statements run with the *same snapshot* and execute concurrently/unpredictably relative to each other — they cannot see one another's writes; only `RETURNING` communicates data between them and the main query.
- Recursive self-reference in a data-modifying CTE isn't allowed directly, but you can `DELETE ... WHERE x IN (SELECT ... FROM a_recursive_with_cte)`.
- Trying to modify the same row twice within one statement (across CTEs) is unsupported / unpredictable — avoid overlapping target rows between sibling data-modifying CTEs and the main statement.
- Data-modifying CTEs always run to completion exactly once, regardless of whether the primary query reads their output (unlike plain `SELECT` CTEs, which may stop early once the parent has enough rows).

----
