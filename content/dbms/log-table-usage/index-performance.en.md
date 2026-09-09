---
type: docs
title: '7.6 Indexes and Performance'
weight: 60
toc: true
---

If a query does not become faster after adding an index, first check whether it can use that index.
Indexes reduce read cost but increase ingestion, storage, and background processing costs. Start
with representative predicates rather than creating an index on every column.

<a id="index-tuning-log"></a>

<a id="조회-조건에-맞춰-선택합니다"></a>

## Choosing Indexes

| Query predicate | Index to consider | What to check |
|---|---|---|
| Values and ranges for numeric, DATETIME, and other supported types | LSM | Supported types and the actual execution plan |
| Words and token patterns in VARCHAR or TEXT | KEYWORD | Uses SEARCH/ESEARCH; result semantics differ from LIKE |
| Repeated-value analysis on supported types | BITMAP | Value distribution, encoding, ingestion cost, and storage cost |

For LOG `_arrival_time` ranges, use the built-in time access path first. Do not add an index for the
same purpose by habit. Check supported types and properties in
[INDEX Syntax](/dbms/reference/sql/syntax/index-syntax/). Do not directly apply conventional RDBMS
composite-index designs.

<a id="같은-데이터에서-생성-전후를-비교합니다"></a>

## Comparing Before and After Index Creation

```sql
CREATE LOG TABLE ch7_index (
    event_id   INTEGER,
    event_time DATETIME,
    severity   SHORT,
    message    VARCHAR(256)
);
INSERT INTO ch7_index VALUES (
    1, TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1, 'service started');
INSERT INTO ch7_index VALUES (
    2, TO_DATE('2026-01-01 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 'database timeout');
INSERT INTO ch7_index VALUES (
    3, TO_DATE('2026-01-01 10:02:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 'connection timeout');

EXPLAIN SELECT event_id FROM ch7_index WHERE severity = 3;

CREATE INDEX ch7_index_time ON ch7_index(event_time) INDEX_TYPE LSM;
CREATE INDEX ch7_index_message ON ch7_index(message) INDEX_TYPE KEYWORD;
CREATE INDEX ch7_index_severity ON ch7_index(severity)
    INDEX_TYPE BITMAP BITMAP_ENCODE = RANGE;

EXEC TABLE_FLUSH(ch7_index);
EXEC INDEX_FLUSH(ch7_index);

EXPLAIN SELECT event_id FROM ch7_index WHERE severity = 3;
EXPLAIN SELECT event_id FROM ch7_index WHERE message SEARCH 'timeout';

SELECT event_id FROM ch7_index
 WHERE message SEARCH 'timeout'
 ORDER BY event_id;
SHOW INDEXES;
```

The search returns rows 2 and 3. Compare the execution-plan access paths for the value predicate and
SEARCH, and use SHOW INDEXES to check the created names. These three rows illustrate behavior; they
are not a performance benchmark.

<a id="저장-반영과-인덱스-반영은-별도-단계입니다"></a>

## Data and Index Synchronization

`TABLE_FLUSH` flushes table data, whereas `INDEX_FLUSH` waits for index building to progress. Use
them separately as shown when comparing plans and timings before and after index creation.

An index can exist before all ingested data has been indexed. Build lag can affect search cost.
However, calling both commands for every inserted row reduces the benefit of batch ingestion. In
production, monitor ingestion rate and background processing rate together, and synchronize only at
required points.

Do not reinsert data simply because indexing is delayed. Check the source row count and index state
separately before retrying to avoid duplicates.

<a id="실제-성능은-대표-부하에서-판단합니다"></a>

## Performance Measurement Criteria

Compare with the same data volume, predicate values, and concurrent ingestion load. Record repeated
query timings, ingestion throughput, index space, and build lag, rather than a single execution
time. LIKE and REGEXP evaluate predicates against raw strings; narrowing the time range first
reduces the candidates. A KEYWORD index does not turn LIKE into SEARCH.

```sql
DROP INDEX ch7_index_severity;
DROP INDEX ch7_index_message;
DROP INDEX ch7_index_time;
DROP TABLE ch7_index;
```

If the plan is difficult to interpret, compare the query and EXPLAIN output together. The diagnostic
sequence in [Index Tuning](/dbms/performance-tuning/index-tuning/) helps identify the next checks.
