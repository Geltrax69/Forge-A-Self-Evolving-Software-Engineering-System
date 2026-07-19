url: https://www.postgresql.org/docs/current/transaction-iso.html
----

# 13.2. Transaction Isolation

The SQL standard defines four isolation levels; the strictest, Serializable, guarantees concurrent Serializable transactions produce the same effect as running them one at a time in some order.

## Prohibited Phenomena

- **dirty read** — reads uncommitted data from a concurrent transaction.
- **nonrepeatable read** — re-reading data finds it changed by a since-committed transaction.
- **phantom read** — re-running a query finds the matching row set changed by a since-committed transaction.
- **serialization anomaly** — the result of committing a group of transactions is inconsistent with all possible serial orderings.

## Isolation Levels

| Isolation Level | Dirty Read | Nonrepeatable Read | Phantom Read | Serialization Anomaly |
|---|---|---|---|---|
| Read uncommitted | Allowed, but not in PG | Possible | Possible | Possible |
| Read committed | Not possible | Possible | Possible | Possible |
| Repeatable read | Not possible | Not possible | Allowed, but not in PG | Possible |
| Serializable | Not possible | Not possible | Not possible | Not possible |

PostgreSQL implements only three distinct levels internally: Read Uncommitted behaves like Read Committed, and Repeatable Read forbids phantom reads (stronger than the standard requires). Set with `SET TRANSACTION`.

Sequences (and `serial` columns) are not transactional: changes are visible immediately to other transactions and not rolled back on abort.

## 13.2.1. Read Committed (the default)

A `SELECT` sees a snapshot as of the instant the *statement* began — not uncommitted data, not concurrent commits during its own run — but does see its own transaction's earlier uncommitted writes. Two `SELECT`s in the same transaction can see different data if another transaction commits in between.

`UPDATE`/`DELETE`/`SELECT FOR UPDATE`/`SELECT FOR SHARE` search using a snapshot as of statement start, but if a matched row was concurrently updated by another still-in-progress transaction, the command waits for that transaction to finish; if it commits, the search condition is re-evaluated against the new row version. `INSERT ... ON CONFLICT DO UPDATE/NOTHING` and `MERGE` have analogous re-evaluation behavior in Read Committed mode.

Simple, single-row-targeted updates behave intuitively:

```sql
BEGIN;
UPDATE accounts SET balance = balance + 100.00 WHERE acctnum = 12345;
UPDATE accounts SET balance = balance - 100.00 WHERE acctnum = 7534;
COMMIT;
```

But commands with complex search conditions can produce surprising results, because each command only sees a fully-consistent snapshot at its own start, not across the whole transaction — Read Committed offers no cross-statement point-in-time consistency guarantee.

## 13.2.2. Repeatable Read

A transaction sees a snapshot as of the start of its first non-control statement — stable across the whole transaction, not just each statement — preventing dirty reads, nonrepeatable reads, and (unlike the SQL minimum) phantom reads.

`UPDATE`/`DELETE`/`MERGE`/`SELECT FOR UPDATE`/`SELECT FOR SHARE` against a row changed by a since-started concurrent transaction that has since committed will abort with:

```
ERROR:  could not serialize access due to concurrent update
```

The application must retry the whole transaction from the start. Read-only transactions never hit this. Implemented via Snapshot Isolation — a rigorous but not strictly serializable guarantee (a read-only transaction may see a control record marked "batch complete" without seeing all of that batch's detail rows).

Note: prior to PostgreSQL 9.1, "Serializable" meant what "Repeatable Read" means now; request Repeatable Read explicitly if you want that legacy behavior.

## 13.2.3. Serializable

The strictest level: behaves like Repeatable Read plus monitoring for read/write dependency cycles among concurrent Serializable transactions that would make their combined effect inconsistent with any serial execution order. A detected anomaly aborts one transaction with:

```
ERROR:  could not serialize access due to read/write dependencies among transactions
```

Implemented via Serializable Snapshot Isolation (SSI) using non-blocking *predicate locks* (visible in `pg_locks` as `SIReadLock`) — these never cause blocking or deadlocks themselves, just flag dependency conditions. `SELECT FOR UPDATE`/`FOR SHARE` or explicit table locks under Read Committed/Repeatable Read can block and cause disk-visible locking overhead that Serializable's predicate locks avoid — but Serializable pays monitoring overhead and restart costs instead.

Data read during a transaction that later aborts must never be treated as valid — retry until success, except in a `SERIALIZABLE READ ONLY DEFERRABLE` transaction, which blocks at start until it obtains a guaranteed-safe snapshot, then never aborts for serialization reasons.

Even under Serializable, unique-constraint violations can occur from overlapping transactions that each checked "does this key exist?" before inserting — Serializable guarantees a consistent *serial order* exists, not that every possible business-logic race is impossible; explicit existence checks in every inserting transaction avoid this.

Tuning/usage tips for Serializable-heavy workloads:
- Mark transactions `READ ONLY` when possible.
- Bound the number of active connections (use a pool).
- Keep transactions minimal — no more than integrity requires.
- Avoid leaving connections "idle in transaction" (`idle_in_transaction_session_timeout`).
- Drop now-redundant explicit locks / `SELECT FOR UPDATE`/`FOR SHARE`.
- Raise `max_pred_locks_per_transaction` / `_per_relation` / `_per_page` if predicate-lock promotion (page → relation level) is inflating false-positive serialization failures.
- Favor index scans over sequential scans (which always take a relation-level predicate lock) by tuning `random_page_cost` / `cpu_tuple_cost`.

