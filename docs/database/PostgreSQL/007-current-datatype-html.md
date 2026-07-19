url: https://www.postgresql.org/docs/current/datatype.html
----

# Chapter 8. Data Types

PostgreSQL has a rich set of native data types. Users can add new types with `CREATE TYPE`.

## Table 8.1. Built-in General-Purpose Data Types

| Name | Aliases | Description |
|------|---------|-------------|
| `bigint` | `int8` | signed eight-byte integer |
| `bigserial` | `serial8` | autoincrementing eight-byte integer |
| `bit [ (n) ]` | | fixed-length bit string |
| `bit varying [ (n) ]` | `varbit [ (n) ]` | variable-length bit string |
| `boolean` | `bool` | logical Boolean (true/false) |
| `box` | | rectangular box on a plane |
| `bytea` | | binary data ("byte array") |
| `character [ (n) ]` | `char [ (n) ]` | fixed-length character string |
| `character varying [ (n) ]` | `varchar [ (n) ]` | variable-length character string |
| `cidr` | | IPv4 or IPv6 network address |
| `circle` | | circle on a plane |
| `date` | | calendar date (year, month, day) |
| `double precision` | `float`, `float8` | double precision floating-point number (8 bytes) |
| `inet` | | IPv4 or IPv6 host address |
| `integer` | `int`, `int4` | signed four-byte integer |
| `interval [ fields ] [ (p) ]` | | time span |
| `json` | | textual JSON data |
| `jsonb` | | binary JSON data, decomposed |
| `line` | | infinite line on a plane |
| `lseg` | | line segment on a plane |
| `macaddr` | | MAC address |
| `macaddr8` | | MAC address (EUI-64 format) |
| `money` | | currency amount |
| `numeric [ (p, s) ]` | `decimal [ (p, s) ]` | exact numeric of selectable precision |
| `path` | | geometric path on a plane |
| `pg_lsn` | | PostgreSQL Log Sequence Number |
| `pg_snapshot` | | user-level transaction ID snapshot |
| `point` | | geometric point on a plane |
| `polygon` | | closed geometric path on a plane |
| `real` | `float4` | single precision floating-point number (4 bytes) |
| `smallint` | `int2` | signed two-byte integer |
| `smallserial` | `serial2` | autoincrementing two-byte integer |
| `serial` | `serial4` | autoincrementing four-byte integer |
| `text` | | variable-length character string |
| `time [ (p) ] [ without time zone ]` | | time of day (no time zone) |
| `time [ (p) ] with time zone` | `timetz` | time of day, including time zone |
| `timestamp [ (p) ] [ without time zone ]` | | date and time (no time zone) |
| `timestamp [ (p) ] with time zone` | `timestamptz` | date and time, including time zone |
| `tsquery` | | text search query |
| `tsvector` | | text search document |
| `uuid` | | universally unique identifier |
| `xml` | | XML data |

Types specified by the SQL standard: `bigint`, `bit`, `bit varying`, `boolean`, `char`, `character varying`, `character`, `varchar`, `date`, `double precision`, `integer`, `interval`, `numeric`, `decimal`, `real`, `smallint`, `time` (with/without time zone), `timestamp` (with/without time zone), `xml`. Other categories not shown in the table above (documented in later sections of Chapter 8): geometric types, network address types, bit string types, text search types (`tsvector`/`tsquery`), enumerated types (`CREATE TYPE ... AS ENUM`), arrays (`type[]`), composite/row types, range and multirange types, domain types, object identifier types (`oid` and friends), and pseudo-types.

----
