---
type: docs
title: '8.4 Data Input and Mutation'
weight: 40
toc: true
aliases:
  - /dbms/rdb-table-usage/sdk-append-scope/
---

A successful UPDATE response does not necessarily mean an order reached the intended state. No
matching row can yield 0 affected rows without an error. Check the target before modification,
affected row count, and resulting values together.

<a id="modeling-rdb-update-delete"></a>

<a id="현재-상태를-조건에-넣어-변경합니다"></a>

## Conditional UPDATE and DELETE

```sql
CREATE TRANSACTION TABLE ch8_mutation (
    order_id LONG PRIMARY KEY,
    amount   DECIMAL(18,2),
    status   VARCHAR(16),
    ordered  DATETIME
);
INSERT INTO ch8_mutation VALUES (
    1001, 19900.25, 'PENDING', TO_DATE('2026-01-01', 'YYYY-MM-DD'));
INSERT INTO ch8_mutation VALUES (
    1002, 29900.50, 'CANCELLED', TO_DATE('2026-01-02', 'YYYY-MM-DD'));

BEGIN;
UPDATE ch8_mutation SET status = 'SHIPPED'
 WHERE order_id = 1001 AND status = 'PENDING';
SELECT order_id, status FROM ch8_mutation ORDER BY order_id;
COMMIT;
```

1001 is SHIPPED and 1002 is CANCELLED. Repeating the UPDATE affects 0 rows because the row is no
longer PENDING. Use the SDK's affected row count to distinguish success, already processed, and
missing targets according to business rules.

For the deletion below, also check the target count before executing it in a transaction.

```sql
BEGIN;
SELECT COUNT(*) AS delete_candidates FROM ch8_mutation WHERE status = 'CANCELLED';
DELETE FROM ch8_mutation WHERE status = 'CANCELLED';
SELECT order_id, amount, status FROM ch8_mutation ORDER BY order_id;
COMMIT;
```

One row is targeted; after deletion, only 1001 remains. UPDATE/DELETE without WHERE affect all rows.
In production, another session can change data between a preliminary SELECT and the actual
modification, so the preliminary count alone does not establish success.

<a id="reference-self-rdb-insert-select"></a>

<a id="복사할-컬럼과-자기-참조-범위를-명시합니다"></a>

## INSERT SELECT and Self-Reference

```sql
CREATE TRANSACTION TABLE ch8_archive (
    order_id LONG PRIMARY KEY,
    amount   DECIMAL(18,2),
    status   VARCHAR(16),
    ordered  DATETIME
);
INSERT INTO ch8_archive(order_id, amount, status, ordered)
SELECT order_id, amount, status, ordered FROM ch8_mutation
 WHERE ordered < TO_DATE('2026-02-01', 'YYYY-MM-DD');

INSERT INTO ch8_mutation(order_id, amount, status, ordered)
SELECT order_id + 10000, amount, status, ordered FROM ch8_mutation
 WHERE order_id = 1001;

SELECT order_id FROM ch8_archive ORDER BY order_id;
SELECT order_id FROM ch8_mutation ORDER BY order_id;
```

The archive contains 1001; the source contains 1001 and 11001. Reading from and inserting into the
same table does not endlessly reinsert new rows in this example. Copying without changing keys can
still violate uniqueness. Match target column counts/types and partition copy ranges for safe
reruns.

Distinguish ordinary constraint errors from connection failures. Statement failure does not
automatically roll back the entire BEGIN transaction. If the commit response is lost, query again to
determine whether changes were applied. See [Transactions](../transaction/) for boundaries.

```sql
DROP TABLE ch8_archive;
DROP TABLE ch8_mutation;
```

<a id="unsupported-rejected-rdb-append-api"></a>
<a id="support-scope-rdb-sdk"></a>

<a id="대량-입력에서는-배치의-실제-경계를-확인합니다"></a>

## Bulk Ingestion and Batch Boundaries

TRANSACTION also supports the Append API. Old filenames or anchors containing reject/unsupported do
not indicate current lack of support. Choose public language APIs using
[SDK Feature Support](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-append).

| Ingestion method | What to check |
|---|---|
| SQL INSERT/prepared execution | Statement errors and explicit transaction boundaries |
| Driver batch | Actual transmission units, partial success, and autocommit |
| Append | SDK buffers/server batch boundaries, error callbacks, and return values |
| machloader | Mappings, rejected rows, and processed-range records |

The current SQLCLI SQLAppendBatch path processes a server batch as a transaction when no separate
active transaction exists. Constraint-error regression tests for this path roll back the entire
failing batch. Do not extend this guarantee to every SDK logical batch, multiple flushes, or an
Appender's entire lifetime as one atomic operation.

For AUTO_INCREMENT and DECIMAL input, also check the dedicated rules in
[SQLCLI and ODBC](/dbms/development-tools-integration/cli-odbc/). The Append protocol arrival-time
field does not create a LOG-style automatic timestamp column in TRANSACTION.

Before adoption, mix one duplicate-key or NULL-error row with valid rows and verify success/failure
counts and stored results. Retransmission after network errors must also account for duplicates of
already committed data.
