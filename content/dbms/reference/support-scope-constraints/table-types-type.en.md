---
type: docs
title: '16.6.2 Feature Support by Table Type'
weight: 20
toc: true
aliases:
  - /dbms/data-modeling-table-design/table-types-type-manageable/
---

Machbase provides five table types for different uses. Each supports features according to its design goals.

## Table Type Overview

| Table Type | Primary Use |
|------------|----------|
| **TAG** | High-speed time-series sensor ingestion and aggregation (ROLLUP) |
| **LOG** | Sequential storage of logs/events in defined columns and text search |
| **LOOKUP** | Metadata, code tables, and reference data (supports UPDATE/DELETE) |
| **VOLATILE** | In-memory server state and caches; data is lost on restart |
| **TRANSACTION** | General relational data requiring transactions |

## Feature Support Matrix

| Feature | TAG | LOG | LOOKUP | VOLATILE | TRANSACTION |
|------|:---:|:---:|:------:|:--------:|:---:|
| **Writes** | | | | | |
| INSERT (SQL) | O | O | O | O | O |
| **Updates/Deletes** | | | | | |
| UPDATE | △ | X | O | O | O |
| DELETE | O | O | O | O | O |
| **Transactions** | | | | | |
| Transaction (COMMIT/ROLLBACK) | X | X | X | X | O |
| **Aggregation and Search** | | | | | |
| ROLLUP | O | X | X | X | X |
| Text search (KEYWORD INDEX) | X | O | X | X | X |
| **JSON** | | | | | |
| JSON columns | O | O | O | X | O |
| JSON path query | O | O | O | X | O |
| **Fixed-point Numbers** | | | | | |
| DECIMAL / NUMERIC columns | O | O | O | O | O |
| **Fixed-length ARRAY** | | | | | |
| ARRAY column creation | O | O | O | O | O |
| ARRAY ADD/DROP COLUMN | △ | O | O | O | O |
| **Indexes** | | | | | |
| Default indexes | O | O | O | O | O |
| LSM indexes | X | O | X | X | X |
| **Queries** | | | | | |
| SELECT | O | O | O | O | O |
| Latest-value queries (`SCAN_BACKWARD`, TAG stat) | O | X | X | X | X |
| JOIN (with other tables) | △ | △ | O | O | O |
| Subquery | O | O | O | O | O |
| VIEW | O | O | O | O | O |

> Symbols: O = supported, X = not supported, △ = partially supported or constrained

Append support by table type depends on the client API. For the language and API you use,
check the
[SDK Append Support Matrix](/dbms/development-tools-integration/sdk-support-scope/#append-table-type-matrix).


DECIMAL is an exact fixed-point type available in all five table types.
`NUMERIC`, `DEC`, `FIXED`, and `NUMBER` are aliases for DECIMAL. Maximum precision is 65
and maximum scale is 30. For details, see
[DECIMAL and NUMERIC Fixed-point Types](../../sql/types/decimal-numeric-fixed-point/).


ARRAY ADD/DROP is supported for LOG, VOLATILE, LOOKUP, TRANSACTION, and TAG METADATA in Standard Edition.
The TAG column's `△` means that ALTER supports TAG METADATA only; ordinary TAG DATA columns
cannot be added. Cluster Edition supports only the LOG path. For exact syntax and DEFAULT rules
for existing rows, see [DDL Syntax](../../sql/syntax/ddl-syntax/#add-column) and
[Numeric ARRAY Types](../../sql/types/array/).

## Main Constraints

### TAG Table UPDATE Constraints (△, Standard Edition)

TAG table UPDATE must satisfy all of the following conditions.

TAG data UPDATE is not available in Cluster Edition.

- Include a tag selection predicate (`name =`, `name IN`, or `name LIKE`) in `WHERE`
- Include a BASETIME column predicate in `WHERE`
- SET targets must be actual data columns
- Data UPDATE cannot modify `time` (BASETIME), `name`, or metadata columns
- SET right-hand expressions cannot reference existing row columns; use constants, binds, or column-free expressions

```sql
-- Allowed: update a data column using tag and time predicates
UPDATE sensor_data
   SET value = 101
 WHERE name = 'sensor01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- Not allowed: update the BASETIME column
UPDATE sensor_data
   SET time = SYSDATE
 WHERE name = 'sensor01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

For details, see [TAG Data UPDATE Support](../tag-data-update/).

### Transaction Scope of LOOKUP and VOLATILE

Each DML statement on LOOKUP and VOLATILE tables is applied independently. These tables do not
participate in TRANSACTION table transactions grouping multiple statements with `BEGIN` and
`COMMIT`/`ROLLBACK`.

### JSON Column Support

JSON columns are supported in TAG, LOG, LOOKUP, and TRANSACTION tables. VOLATILE does not support
JSON columns. LOOKUP JSON columns can be ordinary columns but cannot be primary keys. See
[JSON Support by Table Type](../../sql/types/table-types-type-support-scope-json/).

## TAG Latest-value and Time-range Queries

TAG tables use reverse scans and time predicates to query recent values and time ranges.

```sql
-- Query the five latest values for a specific tag
SELECT /*+ SCAN_BACKWARD(sensor_data) */ *
  FROM sensor_data
 WHERE name = 'sensor01'
 LIMIT 5;

-- Query a time range
SELECT * FROM sensor_data
WHERE name = 'sensor01'
  AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```
