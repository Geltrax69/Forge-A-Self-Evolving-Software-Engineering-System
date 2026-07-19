url: https://www.postgresql.org/docs/current/dml-insert.html, dml-update.html, dml-delete.html, dml-returning.html
----

# 6.1. Inserting Data

```sql
CREATE TABLE products (
    product_no integer,
    name text,
    price numeric
);

INSERT INTO products VALUES (1, 'Cheese', 9.99);
INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', 9.99);
INSERT INTO products (name, price, product_no) VALUES ('Cheese', 9.99, 1);
```

Omitted columns get their default value:

```sql
INSERT INTO products (product_no, name) VALUES (1, 'Cheese');
INSERT INTO products VALUES (1, 'Cheese');   -- fills remaining columns from the left, PostgreSQL extension
INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', DEFAULT);
INSERT INTO products DEFAULT VALUES;
```

Multiple rows in one command:

```sql
INSERT INTO products (product_no, name, price) VALUES
    (1, 'Cheese', 9.99),
    (2, 'Bread', 1.99),
    (3, 'Milk', 2.99);
```

Insert from a query:

```sql
INSERT INTO products (product_no, name, price)
  SELECT product_no, name, price FROM new_products
    WHERE release_date = 'today';
```

### Tip
For bulk loading, prefer `COPY` — less flexible than `INSERT` but more efficient.

# 6.2. Updating Data

```sql
UPDATE products SET price = 10 WHERE price = 5;
UPDATE products SET price = price * 1.10;   -- no WHERE => all rows
UPDATE mytable SET a = 5, b = 3, c = 1 WHERE a > 0;   -- multiple columns
```

Without a primary key there is no guaranteed way to address an individual row — target rows via a matching `WHERE` condition.

# 6.3. Deleting Data

```sql
DELETE FROM products WHERE price = 10;
DELETE FROM products;   -- deletes ALL rows, caveat programmer
```

# 6.4. Returning Data from Modified Rows

`INSERT`, `UPDATE`, `DELETE`, and `MERGE` all support an optional `RETURNING` clause with the same syntax as a `SELECT` output list. `RETURNING *` returns all columns of the target table.

```sql
CREATE TABLE users (firstname text, lastname text, id serial primary key);
INSERT INTO users (firstname, lastname) VALUES ('Joe', 'Cool') RETURNING id;

UPDATE products SET price = price * 1.10
  WHERE price <= 99.99
  RETURNING name, price AS new_price;

DELETE FROM products
  WHERE obsoletion_date = 'today'
  RETURNING *;

MERGE INTO products p USING new_products n ON p.product_no = n.product_no
  WHEN NOT MATCHED THEN INSERT VALUES (n.product_no, n.name, n.price)
  WHEN MATCHED THEN UPDATE SET name = n.name, price = n.price
  RETURNING p.*;
```

You can explicitly return old and new values:

```sql
UPDATE products SET price = price * 1.10
  WHERE price <= 99.99
  RETURNING name, old.price AS old_price, new.price AS new_price,
            new.price - old.price AS price_change;
```

If the target table has triggers, `RETURNING` sees the row as modified by those triggers — useful for inspecting trigger-computed columns.

----
