---
type: docs
title: '9.5 Query and Analysis'
weight: 50
toc: true
---
This section provides runnable examples of key lookups, general predicate queries, and joins with TAG data.


<a id="original-85-querying-data"></a>

## Prepare Example Data

Prepare the following LOOKUP and TAG tables.

```sql
CREATE LOOKUP TABLE ch9_query_master (
    sensor_id VARCHAR(32) PRIMARY KEY,
    site      VARCHAR(32),
    unit      VARCHAR(16),
    status    VARCHAR(16)
);

INSERT INTO ch9_query_master VALUES ('TEMP-01', 'SEOUL', 'C', 'ACTIVE');
INSERT INTO ch9_query_master VALUES ('TEMP-02', 'BUSAN', 'C', 'INACTIVE');

CREATE TAG TABLE ch9_query_data (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

INSERT INTO ch9_query_data VALUES ('TEMP-01', TO_DATE('2026-01-01 00:00:00'), 23.5);
INSERT INTO ch9_query_data VALUES ('TEMP-02', TO_DATE('2026-01-01 00:00:00'), 19.0);
```

<a id="query-lookup-primary-key"></a>

## PRIMARY KEY Lookups

Use a `PRIMARY KEY` predicate for single-row queries.

```sql
SELECT sensor_id, site, unit, status
FROM ch9_query_master
WHERE sensor_id = 'TEMP-01';
```

<a id="query-lookup-condition"></a>

## General Predicate Queries

LOOKUP tables also support queries on ordinary columns. Add indexes to frequently used predicate columns.

```sql
SELECT sensor_id, site, unit
FROM ch9_query_master
WHERE site = 'SEOUL'
  AND status = 'ACTIVE';
```

Indexes can be added to frequently used ordinary predicate columns. For design and creation, see
[Indexes](/dbms/lookup-table-usage/index-performance/).

<a id="query-lookup-join"></a>

## Joining TAG and LOG Tables

LOOKUP tables commonly add descriptive information to source data in TAG or LOG tables.

```sql
SELECT d.name, m.site, m.unit, d.time, d.value
FROM ch9_query_data d
JOIN ch9_query_master m ON d.name = m.sensor_id
WHERE m.status = 'ACTIVE';
```

<a id="query-lookup-analysis-pattern"></a>

## Analysis Patterns

LOOKUP tables provide analysis criteria rather than storing source data. They suit the following patterns.

| Pattern | Description |
|------|------|
| Code translation | Convert status codes, alarm codes, and device types to labels |
| Reference-value comparison | Join sensor values with thresholds to detect exceedances |
| Grouping criteria | Provide aggregation keys such as location, department, or line |
| Current settings | Apply settings that change during operation at query time |

Similarly, join a threshold LOOKUP table with source TAG data to detect values above a threshold.
Restrict large TAG or LOG time ranges before joining.

```sql
DROP TABLE ch9_query_data CASCADE;
DROP TABLE ch9_query_master;
```

<a id="query-lookup-performance"></a>

## Query Performance Criteria

- Use `PRIMARY KEY` or indexed columns for single-row lookups and join keys.
- Consider secondary indexes for ordinary columns frequently used in predicates.
- Narrow the source time range before joining large source datasets.
- Store reference data in LOOKUP and long-term source data in TAG or LOG.
