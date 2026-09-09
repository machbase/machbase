---
type: docs
title: '8.1 Overview and Use Criteria'
weight: 10
toc: true
aliases:
  - /dbms/rdb-table-usage/patterns-scenarios/
---

Device measurements accumulate continuously, while inspection state and inventory quantities require
updates to existing values. Using one model for both can mix source-retention requirements with
state changes. Start with TRANSACTION for mutable business data and TAG/LOG for source time series.

<a id="overview-rdb-characteristics"></a>

<a id="수정과-관계형-조회가-필요한-데이터에-사용합니다"></a>

## TRANSACTION Table Characteristics

TRANSACTION supports SELECT, INSERT, UPDATE, DELETE, PRIMARY KEY, UNIQUE INDEX, and secondary
indexes. It is Standard Edition only. The following three forms create the same table type.

| Syntax | Meaning |
|---|---|
| CREATE TABLE | Default TRANSACTION creation with the type omitted |
| CREATE TRANSACTION TABLE | Explicit type |
| CREATE TXN TABLE | Abbreviated type |

Use CREATE TRANSACTION TABLE in public documentation and operational scripts to make the type
explicit. CREATE RDB TABLE and CREATE TRX TABLE are unsupported. None of the three supported
creation forms is available in Cluster. Specify CREATE LOG TABLE explicitly for LOG.

<a id="overview-rdb-use-criteria"></a>
<a id="use-cases-rdb"></a>

<a id="상태-변경을-작은-예제로-확인합니다"></a>

## State Changes and Rollback

```sql
CREATE TRANSACTION TABLE ch8_overview (
    item_id LONG PRIMARY KEY,
    qty     INTEGER NOT NULL
);
INSERT INTO ch8_overview VALUES (42, 10);

BEGIN;
UPDATE ch8_overview SET qty = qty - 3 WHERE item_id = 42 AND qty >= 3;
SELECT item_id, qty FROM ch8_overview;
ROLLBACK;

SELECT item_id, qty FROM ch8_overview;
DROP TABLE ch8_overview;
```

On the same connection, the query inside the transaction shows quantity 7; after ROLLBACK, it shows
10. `qty >= 3` is the business predicate that prevents a change when stock is insufficient.

Do not interpret an error-free UPDATE as business success. If no row matches, the affected row count
can be 0. The application must check that the expected one row was affected before deciding to
continue or roll back. This check matters more than simply substituting numbers in the SQL example.

<a id="overview-rdb-not-use"></a>

<a id="원본-참조-정보-업무-상태를-구분합니다"></a>

## Comparison with Other Tables

| Main requirement | Table to consider first |
|---|---|
| Measurements by sensor name and ROLLUP | TAG |
| Immutable source logs/events | LOG |
| Small current reference datasets | LOOKUP |
| Relational DML and explicit transactions | TRANSACTION |
| In-memory state that may be lost on restart | VOLATILE |

TRANSACTION can hold equipment inspection state, business history, and separate summary results. For
bulk source collection, compare throughput and ingestion paths with TAG/LOG. TRANSACTION also
supports Append, but do not assume identical throughput or batch boundaries. See
[Ingestion Methods](../data-input-mutation/).

LOOKUP does not replace every TRANSACTION feature. If relational transactions are required in
Cluster, consider an architecture that includes a separate RDBMS.

<a id="overview-rdb-design-flow"></a>

<a id="키와-실패-처리부터-설계합니다"></a>

## Design Criteria

Distinguish the row identifier from the business key used to prevent duplicates. An internal number
may use PRIMARY KEY, while a separate unique value such as an external-system code may need UNIQUE
INDEX. Automatic numbering does not eliminate duplicate business keys.

Next, define frequent WHERE predicates and business success criteria. Decide where transactions end
and what to check after errors so concurrent requests or connection failures have clear handling.
Read [Schema](../table-structure-schema/) together with [Transactions](../transaction/).
