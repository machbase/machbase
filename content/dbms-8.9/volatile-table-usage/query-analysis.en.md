---
type: docs
title: '10.5 Query and Analysis'
weight: 50
toc: true
---

This section provides runnable examples of key lookups, general predicate queries, and temporary
aggregates for VOLATILE tables.

<a id="original-85-querying-data"></a>

## Prepare Example Data

Query VOLATILE tables with `SELECT`, as with other table types. Run the following examples in order
through the final cleanup statements.

```sql
CREATE VOLATILE TABLE ch10_query (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

INSERT INTO ch10_query VALUES ('DEV-01', 'RUNNING', 42.5, NOW);
INSERT INTO ch10_query VALUES ('DEV-02', 'STOPPED', 0, NOW);
```

<a id="query-volatile-primary-key"></a>

## PRIMARY KEY Lookups

A key predicate is suitable for retrieving a single row from a current-state cache.

```sql
SELECT device_id, status, value, updated_at
FROM ch10_query
WHERE device_id = 'DEV-01';
```

<a id="query-volatile-index"></a>

## General Predicate Queries

Consider a secondary index for repeated queries on columns other than the `PRIMARY KEY`.

```sql
CREATE INDEX ch10_query_status_idx ON ch10_query(status);

SELECT device_id, value, updated_at
FROM ch10_query
WHERE status = 'RUNNING';
```

Indexes also consume memory. Create them only on columns needed by actual queries.

<a id="query-volatile-temporary-analysis"></a>

## Querying Temporary Aggregates

Storing aggregates for short intervals reduces repeated calculations for dashboards and alarm evaluation.

```sql
CREATE VOLATILE TABLE ch10_query_summary (
    summary_key VARCHAR(96) PRIMARY KEY,
    sensor_id   VARCHAR(64),
    bucket_time DATETIME,
    avg_value   DOUBLE,
    max_value   DOUBLE,
    sample_cnt  LONG
);

INSERT INTO ch10_query_summary
VALUES ('TEMP-01:2026-01-01T00:00', 'TEMP-01', TO_DATE('2026-01-01 00:00:00'),
        21.5, 23.0, 60);

SELECT sensor_id, bucket_time, avg_value, max_value
FROM ch10_query_summary
WHERE sensor_id = 'TEMP-01'
ORDER BY bucket_time DESC
LIMIT 10;

DROP TABLE ch10_query_summary;
DROP TABLE ch10_query;
```

If aggregate results require long-term retention, copy them periodically to a LOG or TRANSACTION table.

<a id="query-volatile-limitations"></a>

## Query Considerations

- Data is empty after a server restart. First check whether the initial load has completed.
- Define a `PRIMARY KEY` when key lookups are the primary access pattern.
- Consider secondary indexes for columns frequently used in range queries or sorting.
- Store important source data in persistent tables and use VOLATILE as a cache.
