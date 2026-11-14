---
type: docs
title: '8.5 Query and Analysis'
weight: 50
toc: true
---

Even syntactically valid SQL returns no rows when predicates differ from stored state values.
Insufficient sort keys can also make equal-timestamp rows appear in a different order between
queries. Check filtering, sorting, and aggregation with samples covering multiple states and time
boundaries.

<a id="query-rdb-basic-select"></a>

<a id="확인할-결과가-있는-표본을-준비합니다"></a>

## Prepare Example Data

```sql
CREATE TRANSACTION TABLE ch8_query (
    order_id LONG PRIMARY KEY,
    customer VARCHAR(32),
    item_id  LONG,
    amount   DECIMAL(18,2),
    status   VARCHAR(16),
    ordered  DATETIME
);
CREATE TRANSACTION TABLE ch8_query_product (id LONG PRIMARY KEY, name VARCHAR(64));
INSERT INTO ch8_query_product VALUES (42, 'Pump');
INSERT INTO ch8_query_product VALUES (43, 'Valve');

INSERT INTO ch8_query VALUES (
    1001, 'C-01', 42, 10.25, 'PENDING', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO ch8_query VALUES (
    1002, 'C-01', 43, 20.50, 'PENDING', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO ch8_query VALUES (
    1003, 'C-02', 42, 30.75, 'SHIPPED', TO_DATE('2026-01-02', 'YYYY-MM-DD'));

SELECT order_id, amount, status FROM ch8_query WHERE order_id = 1001;
```

The query returns 1001, 10.25, PENDING.

<a id="query-rdb-filter-sort-limit"></a>

<a id="시간-경계와-같은-시각의-순서를-명시합니다"></a>

## Time Predicates and Sorting

```sql
SELECT order_id, amount FROM ch8_query
 WHERE ordered >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
   AND ordered <  TO_DATE('2026-01-02', 'YYYY-MM-DD')
   AND status = 'PENDING'
 ORDER BY ordered DESC, order_id DESC
 LIMIT 1;
```

Only 1002 is selected. order_id fixes ordering even when ordered timestamps match. Do not expect a
desired order from LIMIT alone. Use inclusive-start/exclusive-end predicates for consecutive daily
aggregates to avoid boundary duplicates. LOG-specific DURATION and automatic _arrival_time do not
apply to TRANSACTION.

<a id="query-rdb-join"></a>

<a id="기준-정보를-붙일-때-누락과-중복을-확인합니다"></a>

## Joining Reference Data

```sql
SELECT o.order_id, p.name, o.amount
  FROM ch8_query o JOIN ch8_query_product p ON o.item_id = p.id
 WHERE o.customer = 'C-01'
 ORDER BY o.order_id;
```

Results are (1001, Pump, 10.25) and (1002, Valve, 20.50). This INNER JOIN excludes orders without
reference data. Duplicate keys on the other side multiply results, so also check key uniqueness. For
joins with other table types, see [JOIN Examples](../join-relational-query/).

<a id="query-rdb-aggregation"></a>

<a id="합계는-원본-건수와-함께-확인합니다"></a>

## Aggregate Queries

```sql
SELECT status, COUNT(*) AS cnt, SUM(amount) AS total_amount
  FROM ch8_query GROUP BY status ORDER BY status;
```

PENDING has 2 rows totaling 30.75; SHIPPED has 1 row totaling 30.75. An index does not automatically
accelerate every aggregate. Check ranges, group counts, and result volume; consider separate
summaries for repeated workloads.

<a id="query-rdb-json"></a>

<a id="json-값이-실제로-들어-있는지부터-확인합니다"></a>

## JSON Path Queries

```sql
CREATE TRANSACTION TABLE ch8_query_json (id INTEGER PRIMARY KEY, state JSON);
INSERT INTO ch8_query_json VALUES (1, '{"status":"ALARM","score":90}');
INSERT INTO ch8_query_json VALUES (2, '{"status":"NORMAL","score":10}');
INSERT INTO ch8_query_json VALUES (3, '{"score":20}');

SELECT id, state->'$.status' AS status FROM ch8_query_json
 WHERE state->'$.status' = 'ALARM'
 ORDER BY id;
```

Only row 1 is selected. Include separate samples for missing paths and differing predicate values.
Distinguish arrow-path string comparisons from numeric extraction function comparisons. For
frequently used paths, consider
[JSON Path Indexes](../index-performance/#index-strategy-rdb-json-path).

<a id="query-rdb-performance"></a>

<a id="실행-계획은-지원되는-조건-모양까지-확인합니다"></a>

## Indexes and Execution Plans

```sql
CREATE INDEX ch8_query_status_time ON ch8_query(status, ordered);
EXPLAIN SELECT order_id FROM ch8_query
 WHERE status = 'PENDING'
   AND ordered >= TO_DATE('2026-01-01', 'YYYY-MM-DD');
```

Align predicates with leading composite-index columns, but verify actual usage with EXPLAIN.
Assuming Machbase delegates entire relational queries unchanged to internal SQLite can lead to
incorrect interpretations of index selection and function predicates.

```sql
DROP TABLE ch8_query_json;
DROP TABLE ch8_query_product;
DROP TABLE ch8_query;
```

If results differ, check source row counts, WHERE predicates, and sort keys in order before
analyzing complex aggregates or joins.
