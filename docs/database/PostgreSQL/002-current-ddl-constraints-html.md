url: https://www.postgresql.org/docs/current/ddl-constraints.html and https://www.postgresql.org/docs/current/ddl-alter.html
----

# 5.5. Constraints

Data types are a way to limit the kind of data that can be stored in a table. For many applications, however, the constraint they provide is too coarse. SQL allows you to define constraints on columns and tables. If a user attempts to store data that would violate a constraint, an error is raised.

## 5.5.1. Check Constraints

A check constraint allows you to specify that the value in a certain column must satisfy a Boolean expression:

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0)
);
```

Named constraint:

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CONSTRAINT positive_price CHECK (price > 0)
);
```

A check constraint can refer to several columns (table constraint):

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric CHECK (price > 0),
    discounted_price numeric CHECK (discounted_price > 0),
    CHECK (price > discounted_price)
);
```

A check constraint is satisfied if the check expression evaluates to true or null — so a check constraint alone will not prevent nulls; use a not-null constraint for that.

PostgreSQL does not support `CHECK` constraints that reference table data other than the new/updated row being checked. Use `UNIQUE`, `EXCLUDE`, or `FOREIGN KEY` constraints to express cross-row/cross-table restrictions, or a trigger for one-time checks.

## 5.5.2. Not-Null Constraints

```sql
CREATE TABLE products (
    product_no integer NOT NULL,
    name text NOT NULL,
    price numeric
);
```

A not-null constraint is functionally equivalent to `CHECK (column_name IS NOT NULL)`, but PostgreSQL's explicit not-null constraint is more efficient. A column can have at most one explicit not-null constraint. The inverse `NULL` constraint exists for toggling convenience but is not standard SQL.

### Tip
In most database designs the majority of columns should be marked not null.

## 5.5.3. Unique Constraints

```sql
CREATE TABLE products (
    product_no integer UNIQUE,
    name text,
    price numeric
);
```

Multi-column unique constraint (table constraint):

```sql
CREATE TABLE example (
    a integer,
    b integer,
    c integer,
    UNIQUE (a, c)
);
```

Adding a unique constraint automatically creates a unique B-tree index. By default, two nulls are not considered equal, so duplicate rows with nulls in constrained columns can still exist unless you add `NULLS NOT DISTINCT`:

```sql
CREATE TABLE products (
    product_no integer UNIQUE NULLS NOT DISTINCT,
    name text,
    price numeric
);
```

## 5.5.4. Primary Keys

```sql
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);
```

Equivalent to `UNIQUE NOT NULL`. Primary keys can span multiple columns:

```sql
CREATE TABLE example (
    a integer,
    b integer,
    c integer,
    PRIMARY KEY (a, c)
);
```

Adding a primary key automatically creates a unique B-tree index and forces `NOT NULL`. A table can have at most one primary key.

## 5.5.5. Foreign Keys

```sql
CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric
);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products (product_no),
    quantity integer
);
```

Shortened form (references the referenced table's primary key by default):

```sql
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products,
    quantity integer
);
```

Multi-column foreign key:

```sql
CREATE TABLE t1 (
  a integer PRIMARY KEY,
  b integer,
  c integer,
  FOREIGN KEY (b, c) REFERENCES other_table (c1, c2)
);
```

Self-referential foreign key:

```sql
CREATE TABLE tree (
    node_id integer PRIMARY KEY,
    parent_id integer REFERENCES tree,
    name text
);
```

Many-to-many via a join table:

```sql
CREATE TABLE order_items (
    product_no integer REFERENCES products,
    order_id integer REFERENCES orders,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);
```

`ON DELETE` / `ON UPDATE` actions: `NO ACTION` (default), `RESTRICT`, `CASCADE`, `SET NULL`, `SET DEFAULT`:

```sql
CREATE TABLE order_items (
    product_no integer REFERENCES products ON DELETE RESTRICT,
    order_id integer REFERENCES orders ON DELETE CASCADE,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);
```

`SET NULL`/`SET DEFAULT` can take a column list to specify which columns to set, e.g. `ON DELETE SET NULL (author_id)`.

A foreign key must reference columns that are a primary key, unique constraint, or non-partial unique index. `MATCH FULL` requires all referencing columns be null together or all non-null (mixed null/non-null fails).

## 5.5.6. Exclusion Constraints

```sql
CREATE TABLE circles (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);
```

Ensures that for any two rows, at least one operator comparison on the specified columns/expressions returns false or null. Adding an exclusion constraint automatically creates an index of the specified type.

---

# 5.7. Modifying Tables

All modifications to an existing table's structure are done with `ALTER TABLE`.

## 5.7.1. Adding a Column

```sql
ALTER TABLE products ADD COLUMN description text;
```

Adding a column with a constant default is fast even on large tables (the default is applied lazily). A *volatile* default (e.g. `clock_timestamp()`) requires rewriting every row.

```sql
ALTER TABLE products ADD COLUMN description text CHECK (description <> '');
```

## 5.7.2. Removing a Column

```sql
ALTER TABLE products DROP COLUMN description;
ALTER TABLE products DROP COLUMN description CASCADE;
```

## 5.7.3. Adding a Constraint

```sql
ALTER TABLE products ADD CHECK (name <> '');
ALTER TABLE products ADD CONSTRAINT some_name UNIQUE (product_no);
ALTER TABLE products ADD FOREIGN KEY (product_group_id) REFERENCES product_groups;
ALTER TABLE products ALTER COLUMN product_no SET NOT NULL;
```

The constraint is checked immediately; existing data must satisfy it.

## 5.7.4. Removing a Constraint

```sql
ALTER TABLE products DROP CONSTRAINT some_name;
ALTER TABLE products ALTER COLUMN product_no DROP NOT NULL;
```

Use `\d tablename` in psql to find generated constraint names. Add `CASCADE` to drop dependents too.

## 5.7.5. Changing a Column's Default Value

```sql
ALTER TABLE products ALTER COLUMN price SET DEFAULT 7.77;
ALTER TABLE products ALTER COLUMN price DROP DEFAULT;
```

Only affects future inserts, not existing rows.

## 5.7.6. Changing a Column's Data Type

```sql
ALTER TABLE products ALTER COLUMN price TYPE numeric(10,2);
```

Succeeds only if existing values can be implicitly cast; use `USING` for more complex conversions. Consider dropping/re-adding constraints around type changes.

## 5.7.7. Renaming a Column

```sql
ALTER TABLE products RENAME COLUMN product_no TO product_number;
```

## 5.7.8. Renaming a Table

```sql
ALTER TABLE products RENAME TO items;
```

----
