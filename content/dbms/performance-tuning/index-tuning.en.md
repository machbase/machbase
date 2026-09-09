---
type: docs
title: '12.3 Index Tuning'
weight: 30
toc: true
---

Add indexes only when they reduce read costs for actual predicates and join keys. Measure
query latency, ingestion throughput, memory, and storage before and after creation.

<a id="table별-확인"></a>

## Checks by table type

| Table type | Primary key or access path | Additional indexes |
|------------|--------------------|------------|
| TAG | Name and BASETIME access | Supported value and metadata indexes |
| LOG | `_ARRIVAL_TIME` range | LSM, BITMAP, KEYWORD |
| LOOKUP | PRIMARY KEY | Supported secondary indexes |
| VOLATILE | Optional PRIMARY KEY | REDBLACK secondary indexes |
| TRANSACTION | PRIMARY KEY | Relational secondary indexes |

For supported index types and syntax, see each table type's chapter and
[Index Syntax](/dbms/reference/sql/syntax/index-syntax/).

## Procedure

1. Record `EXPLAIN` and the result count for the slow SQL.
2. Check predicate selectivity and value distribution.
3. Check for an existing index with the same leading column.
4. Create one candidate index and verify that its build completes.
5. Remeasure queries and ingestion under the same conditions.
6. Remove indexes that provide no benefit or impose excessive write costs.

```sql
SHOW INDEXES;
SHOW INDEXGAP;
```

Do not assume a fixed throughput reduction per index. Results depend on row size, key
distribution, concurrency, and storage. Measure with data representative of production.

## Considerations

- Compare against a scan before indexing a column with low selectivity.
- Check whether functions or casts around indexed columns prevent key-range access.
- Design composite indexes around frequent predicate combinations and leading columns.
- During index creation, monitor ingestion and query load and `SHOW INDEXGAP`.
- Before removing an unused index, verify that peak and batch workloads do not need it.

For details, see the index and performance pages in the TAG, LOG, LOOKUP, VOLATILE, and
TRANSACTION chapters.
