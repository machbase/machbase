---
type: docs
title: '4.1 Choose a Table Type'
weight: 10
toc: true
---

Read [Data model concepts](/dbms/core-concepts/concepts/) for the role of each table. This page makes
the implementation decision from mutation, query, persistence, and transaction requirements.

<a id="table-types-type"></a>

Start with the meaning of a row, not the table name. A sensor observation, a device's current state,
and a maintenance job have different identifiers, lifetimes, and mutation requirements.

### Describe the data before choosing

| Question | Decision to record |
|---|---|
| What does one row represent? | One observation, one event, or the current state of an entity |
| How is it found? | Sensor and measurement time, equipment ID, or job number |
| How does it change? | Append history, correct a measurement, or overwrite current state |
| Which changes must commit together? | For example, registering a job and changing spare-part stock |
| How long is it needed? | Raw and aggregate retention; whether restart loss is acceptable |
| What is its size? | Tag count, rows per second, row width, and memory for reference rows and indexes |

In equipment monitoring, TAG is a candidate for temperature history, LOG for alarm events, and
LOOKUP for equipment codes. If a job and stock change must commit together, consider TRANSACTION
in Standard Edition. A VOLATILE current-state cache is optional when it can be rebuilt from history.

<a id="selection-decision"></a>

## Decision flow

1. Use TAG for measurements addressed by tag name and a time or distance axis.
2. Use LOG for append-oriented events and logs; its default arrival timestamp records server receipt.
3. Use LOOKUP for persistent, memory-resident reference data.
4. Use VOLATILE for shared in-memory state that can be rebuilt after restart.
5. Use TRANSACTION for relational business data requiring general DML and transactions.

If two choices remain, decide from the required UPDATE and DELETE predicates, restart behavior,
working-set size, transaction boundary, and dominant query key.

<a id="comparison-tag-log-rdb-volatile-lookup"></a>

## Comparison

| Requirement | Start with |
|---|---|
| Repeated measurements by name and axis | TAG |
| Append-only event history | LOG |
| General relational DML and transaction | TRANSACTION |
| Persistent reference lookup | LOOKUP |
| Rebuildable in-memory state | VOLATILE |

### Function and storage constraints

| Item | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|---|---|---|---|---|---|
| Primary key | Identifies a tag | Not supported | Optional row key | Optional row key | Required row key |
| UPDATE | Standard DATA correction with tag and BASETIME predicates | Not supported | General predicates | Primary-key equality | General predicates; key immutable |
| DELETE | BEFORE, tag/axis conditions, or all rows | BEFORE, OLDEST, EXCEPT, or all rows | General predicates or all rows | Primary-key equality or all rows | General predicates or all rows |
| Explicit transaction | No | No | Yes | No | No |
| Persistence | Yes | Yes | Yes | No | Yes |
| Cluster Edition | Yes, with feature limits | Yes | No | Yes, with node-local lifetime | Yes |

For LOG, use `CREATE LOG TABLE`. In 8.7.0, unqualified `CREATE TABLE` creates a TRANSACTION table,
as do `CREATE TRANSACTION TABLE` and `CREATE TXN TABLE`; these require Standard Edition.

LOG has BITMAP, KEYWORD, and LSM index paths; TAG uses tag/axis access and supported secondary
indexes. TRANSACTION uses primary, unique, and ordinary BTREE indexes. LOOKUP and VOLATILE keep
rows and indexes in memory. Check exact index support before creating an index.

Append support depends on both table type and SDK path. Consult the
[SDK Append matrix](../../development-tools-integration/sdk-support-scope/#append-table-type-matrix).

For TAG and LOG, estimate raw data, indexes, aggregates, and retention together. For TRANSACTION,
measure row/index size and transaction load. For LOOKUP and VOLATILE, measure complete rows and
indexes in memory; LOOKUP also has restart loading costs. A small table is not a fixed row count.

Exact DML conditions belong to [Data mutation policy](../alter-data-mutation-policy/) and hard
feature support belongs to [Support scope](/dbms/reference/support-scope-constraints/).

<a id="comparison-rdb-vs-lookup"></a>

## TRANSACTION versus LOOKUP

Choose TRANSACTION for relational changes, transactions, and larger business sets. Choose LOOKUP for
small persistent reference data whose complete runtime rows and indexes can reside in memory. Measure
the expected row set and update pattern instead of selecting by table name alone.

LOOKUP supports general UPDATE predicates, but WHERE is required and the primary key cannot be
updated. Its statements do not join a multi-statement TRANSACTION transaction. TRANSACTION can
update or delete all rows without WHERE and supports explicit COMMIT/ROLLBACK.

### Example

```sql
CREATE LOOKUP TABLE country_code (
    code VARCHAR(4) PRIMARY KEY,
    name VARCHAR(64)
);
INSERT INTO country_code VALUES ('KR', 'Republic of Korea');
UPDATE country_code SET name = 'Korea' WHERE code = 'KR';
SELECT code, name FROM country_code WHERE code = 'KR';

CREATE TRANSACTION TABLE order_history (
    order_id LONG PRIMARY KEY,
    item_id INTEGER,
    qty INTEGER,
    amount DECIMAL(18,2)
);
INSERT INTO order_history VALUES (12345, 501, 1, 12000.00);
UPDATE order_history SET qty = 10 WHERE order_id = 12345;
SELECT order_id, qty, amount FROM order_history WHERE order_id = 12345;
DELETE FROM order_history WHERE order_id = 12345;
SELECT COUNT(*) FROM order_history WHERE order_id = 12345;
```

The first query returns the updated country name. The order query returns quantity `10`, and the
final count is `0`. Here `amount` is maintained separately and is not recalculated automatically.
In a real order model, define the relationship between quantity, unit price, and total, and update
the required columns together. After the exercise, drop only the tables created for this example.
