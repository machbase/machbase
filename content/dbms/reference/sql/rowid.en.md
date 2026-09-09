---
type: docs
title: '16.1.6 ROWID'
weight: 60
toc: true
aliases:
  - /dbms/application-integration/rowid-generated-id/
  - /dbms/development-tools-integration/rowid-generated-id/
---

<span class="badge-since">Available since Machbase 8.7.0</span>

`ROWID` is a 64-bit identifier used to locate a row within a table. This page defines its SQL
meaning, per-table predicates, INSERT results, and lifetime. For SDK access APIs and code,
see [SDK Feature Support](/dbms/development-tools-integration/sdk-support-scope/) and the relevant
language page.

This feature is supported in Standard Edition. Update both the server and SDK to versions
supporting ROWID. It is unavailable in Cluster Edition.

## ROWID and Business Keys

ROWID identifies a stored row's location in the current table. It is not a permanent business key
such as an order number or device ID.

- It is not an ordinary column and is excluded from `SELECT *`. Select it explicitly when needed.
- Do not compare ROWIDs across tables or use one table's ROWID to query another table.
- Do not decompose ROWID values or use them in arithmetic.
- Numeric order does not indicate ingestion order across the entire table.
- New tables cannot define a real column named `ROWID`.
- For legacy tables with a real `ROWID` column, that column takes precedence. Rename the existing
  column to use the ROWID pseudocolumn.

```sql
SELECT ROWID, name, time, value
  FROM sensor_tag
 WHERE name = 'TAG-01';
```

## Support by Table Type

| Table | ROWID Meaning | Predicates | Single-row INSERT Result |
|--------|--------------|-----------|------------------|
| LOG | Identifier of a stored log row | `=`, `<`, `<=`, `>`, `>=`, `BETWEEN`, `ORDER BY` | Returns generated ROWID |
| TAG | Identifier of a stored original TAG row | One `ROWID = value` within a top-level `AND` | Returns generated ROWID |
| TRANSACTION | Single `LONG`/`INT64` PRIMARY KEY value | Predicates supported by the existing PK | Returns PK as ROWID |
| LOOKUP | Single `LONG`/`INT64` PRIMARY KEY value | Predicates supported by the existing PK | Returns PK as ROWID |
| VOLATILE | Single `LONG`/`INT64` PRIMARY KEY value | Predicates supported by the existing PK | Returns PK as ROWID |

TRANSACTION, LOOKUP, and VOLATILE use a single `LONG`/`INT64` PRIMARY KEY with a value of `0`
or greater as ROWID, regardless of `AUTO_INCREMENT`. If the application supplies the PK, that
value is returned. If an `AUTO_INCREMENT` PK is omitted or NULL, the server-generated value
is returned. Negative PK values cannot be used as ROWIDs.

LOG and TAG ROWIDs range from `0..UINT64_MAX-1`; the three PRIMARY KEY-based table types use
`0..INT64_MAX`. `0` is valid. `UINT64_MAX` cannot be used as
ROWID.

### LOG Queries

LOG ROWIDs support range queries and ordering. Because `_ARRIVAL_TIME` can be equal in multiple
rows, use ROWID to locate a specific row again.

```sql
SELECT ROWID, message
  FROM app_log
 WHERE ROWID >= ?
   AND ROWID < ?
 ORDER BY ROWID;
```

`ROWID IN (...)` is not supported.

### TAG Queries

TAG supports only single-ROWID equality lookup. You can combine tag name, time, and value predicates
with `AND`; a row is returned only when every condition matches.

```sql
SELECT ROWID, name, time, value
  FROM sensor_tag
 WHERE ROWID = ?
   AND name = 'TAG-01'
   AND time >= TO_DATE('2026-08-10 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

The following conditions cannot be used with TAG ROWID.

| Usage | Support |
|--------|:---------:|
| `ROWID = ?` | O |
| `ROWID > ?`, `BETWEEN`, and other ranges | X |
| `ROWID IN (...)` | X |
| `ROWID = ? OR ...` | X |
| `ORDER BY ROWID` | X |
| `DELETE ... WHERE ROWID = ?` | X |
| Combined with rollup, custom rollup, or stat results | X |

### Comparing TRANSACTION, LOOKUP, and VOLATILE

The following three tables support the same `AUTO_INCREMENT` declaration, but differ in restart
behavior and ingestion features.

```sql
CREATE TRANSACTION TABLE orders (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);

CREATE LOOKUP TABLE lookup_orders (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);

CREATE VOLATILE TABLE volatile_orders (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);
```

| Feature | TRANSACTION | LOOKUP | VOLATILE |
|------|-------------|--------|----------|
| Rows and next automatic value survive restart | O | O | X |
| Explicit transactions | O | X | X |
| Generate automatic values with `INSERT ... SELECT` | O | X | X |
| UPSERT on AUTO_INCREMENT tables | O (no ROWID return) | X | X |
| ROWID result from single `INSERT ... VALUES` | O | O | O |

LOOKUP `PROPERTY(SEQUENCE)` and `NEXTVAL()` are separate from `AUTO_INCREMENT`. Do not configure
both mechanisms on the same column.

TRANSACTION table DDL cannot run during an explicit transaction.
If `CREATE TRANSACTION TABLE` fails with `ERR-02362`, run `COMMIT` or `ROLLBACK` first,
then retry.

### JOIN, Aggregation, and Views

JOIN results have no ROWID representing the entire result. Select the ROWID of each required
source table alias separately.

```sql
SELECT a.ROWID AS order_rowid,
       b.ROWID AS item_rowid,
       a.customer, b.item
  FROM orders a JOIN order_items b ON a.id = b.order_id;
```

| Query Form | ROWID Handling |
|-----------|------------|
| JOIN | Specify `alias.ROWID` for each required source table |
| Aggregation, `GROUP BY`, `DISTINCT`, set operations | No new ROWID is generated for result rows |
| View, CTE, inline view | Passed through only when explicitly selected in the inner SELECT |

## Conditions for Receiving ROWID from INSERT

Do not use `INSERT ... RETURNING ROWID`. Supported SDKs return ROWID with the execution result
of a successful single-row `INSERT ... VALUES`.

| Ingestion Method | Generated ROWID | Description |
|-----------|:---------------:|------|
| Single direct `INSERT ... VALUES` | O | One row successfully created |
| Single prepared INSERT | O | Returns the current result on each execution |
| `INSERT ... SELECT` | X | May create multiple rows; returns no single value |
| execute-array, batch, `executemany()` | X | Does not expose the last internal row as a representative value |
| Append API, append batch | X | Not returned on the high-speed ingestion path |
| loader | X | Not returned on the file ingestion path |
| UPSERT | X | A single ROWID does not represent both INSERT and UPDATE outcomes |
| Failed INSERT | X | Also clears ROWID from the previous execution |

Generated ROWID is a per-statement result. There is no SQL function that retrieves the latest
value for the entire connection.

## Empty Results and Errors

A valid ROWID absent from the current table returns zero rows, not an error. This includes deleted
rows and rows failing additional predicates. In contrast, NULL, negative PKs, `UINT64_MAX`, values
that cannot convert to numbers, and unsupported TAG ranges/IN/OR/ordering are errors.

## Lifetime and Retries

Do not use ROWID as a long-term business key.

| Situation | Existing ROWID |
|------|------------|
| Normal restart | Retained for preserved rows |
| Product backup/restore supporting ROWID preservation | Retained for preserved rows |
| Row DELETE | Invalid |
| Transaction ROLLBACK | ROWID of that INSERT becomes invalid |
| Row discarded by snapshot recovery | Invalid |
| LOG TRUNCATE | Old values may be reused |
| Table DROP and recreation | Old values may identify different rows |
| Export/import or row reinsertion | Not preserved |

An INSERT may succeed without the application receiving its ROWID if the network response is lost.
Automatically repeating the INSERT can create duplicate rows. First verify whether it was applied
using a business key or a separate idempotency policy.

## Related Documentation

- [SDK Feature Support](/dbms/development-tools-integration/sdk-support-scope/)
- [AUTO_INCREMENT](/dbms/reference/sql/syntax/auto-increment-syntax/)
- [LOG Data Ingestion](/dbms/log-table-usage/data-input-mutation/)
- [TAG Data Ingestion](/dbms/tag-table-usage/data-input-mutation/)
