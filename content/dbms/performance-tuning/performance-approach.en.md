---
type: docs
title: '12.1 Performance Diagnosis'
weight: 10
toc: true
aliases:
  - /dbms/performance-tuning/checklist-performance-diagnosis/
---

Establish reproduction conditions and baselines before narrowing down a performance bottleneck.
Changing several properties or indexes at once without evidence makes causes and effects hard
to distinguish.

## 1. Record reproduction conditions

- Slow SQL or ingestion path
- Start and end times, database, and user
- Target table, time range, row count, and result count
- Concurrent sessions, queries, and Appenders
- Latency and throughput during normal operation and the incident
- Recent deployment, schema, configuration, or data distribution changes

## 2. Check resource bottlenecks

```bash
iostat -x 1 5
top -b -n 1
free -h
```

Compare CPU, I/O, and memory metrics with normal baselines rather than fixed thresholds.
Distinguish brief spikes from sustained saturation, and align OS metric timestamps with
server traces and query times.

## 3. Inspect active operations

```sql
SELECT sess_id, id AS stmt_id, state, record_size, query
FROM V$STMT
ORDER BY sess_id, id;

SELECT id, user_name, user_ip, login_time, client_type
FROM V$SESSION
ORDER BY login_time DESC;
```

Look for long-running statements, abnormal session growth, and concurrent copies of the same
query. Use `DESC` to check system view columns in the deployed version.

## 4. Check execution plans and query ranges

For a slow SELECT, use `EXPLAIN` to inspect tables, scan types, key ranges, filters, and joins.
Check that TAG and LOG queries include a time range and that functions or casts do not prevent
predicates from using index ranges.

For details, see [Query and Analysis Tuning](../performance-query-tuning/).

## 5. Change one item and remeasure

Narrow candidates in this order: query, index, batch size, concurrency, then caches and
configuration. Change one item at a time and compare the following under the same conditions.

| Area | Compare |
|------|--------|
| Queries | Response time distribution, result rows, execution plans |
| Ingestion | Rows/s, server processing response latency, failure counts |
| Server | CPU, I/O, memory, sessions |
| Side effects | Other query latency, reduced ingestion, restart impact |

Revert to the recorded previous value if a change provides no benefit or causes substantial
side effects. Consider schema or storage structure changes last, after preparing a test
environment and recovery procedure.

## Final diagnostic checklist

- Have you compared current operations and sessions with normal baselines?
- Have you checked the execution plan using the actual SQL and time range?
- Have you assessed the ingestion cost of index and ROLLUP changes?
- Have you aligned OS and server metrics with the same operation?
- Have you applied configuration and schema changes one at a time?
- Have you recorded rollback values and remeasurement results?
