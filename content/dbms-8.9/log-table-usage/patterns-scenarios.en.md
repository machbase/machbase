---
type: docs
title: '7.9 Patterns and Scenarios'
weight: 90
toc: true
---

Real analysis combines time, host, severity, and message. After trying each feature separately, use
them together to answer which errors are increasing on which server. This exercise runs
independently of tables from earlier sections.

<a id="use-cases-log"></a>

<a id="먼저-원본-이벤트와-현재-상태를-구분합니다"></a>

## Source Events and Current State

Append a new LOG row whenever an event occurs. Mutable reference data, such as a device's current
name or location, can be kept in LOOKUP. If historical state is required, retain the values in the
event or design separate history.

The same approach applies to security events and job tracking. Consider TAG first for measurement
aggregation by sensor name, or TRANSACTION for business-row updates and transactions.

<a id="storage-log-text-search-logs"></a>

<a id="분석할-로그와-인덱스를-준비합니다"></a>

## Creating Logs and Indexes

Explicit arrival timestamps make time predicates comparable regardless of the execution date. This
exercise inserts in ascending order into an empty table. For ordinary collection, keep the source
event time in a separate DATETIME column.

```sql
CREATE LOG TABLE ch7_app (
    event_id INTEGER,
    host     VARCHAR(32),
    level    VARCHAR(16),
    message  TEXT
);
CREATE INDEX ch7_app_message ON ch7_app(message) INDEX_TYPE KEYWORD;

INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        1, 'web-01', 'INFO', 'service started');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:10:00', 'YYYY-MM-DD HH24:MI:SS'),
        2, 'web-01', 'WARN', 'slow response');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:20:00', 'YYYY-MM-DD HH24:MI:SS'),
        3, 'web-02', 'ERROR', 'database timeout');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:30:00', 'YYYY-MM-DD HH24:MI:SS'),
        4, 'web-02', 'ERROR', 'connection refused');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        5, 'web-01', 'INFO', 'normal service');

EXEC TABLE_FLUSH(ch7_app);
EXEC INDEX_FLUSH(ch7_app);
SELECT COUNT(*) AS received_rows FROM ch7_app;
```

The inserted row count is 5. Before repeating the exercise, confirm that the final DROP ran. Simply
resending data can create duplicate rows.

<a id="특정-오류를-찾고-같은-시간대의-상황을-봅니다"></a>

## Querying Errors and Time Ranges

```sql
SELECT event_id, host, message FROM ch7_app
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND message SEARCH 'timeout'
 ORDER BY event_id;

SELECT event_id, host, level, message FROM ch7_app
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND level = 'ERROR'
 ORDER BY event_id;
```

The first query selects event 3 on web-02; the second selects events 3 and 4. This workflow starts
with a word search, then examines other errors for the same host and period. Expand only the needed
interval instead of removing the time predicate entirely.

<a id="시간별등급별-건수를-비교합니다"></a>

## Aggregating by Hour and Severity

```sql
SELECT TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24') AS event_hour,
       level, COUNT(*) AS event_count
  FROM ch7_app
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24'), level
 ORDER BY event_hour, level;
```

| event_hour | level | event_count |
|---|---|---|
| 2026-01-01 10 | ERROR | 2 |
| 2026-01-01 10 | INFO | 1 |
| 2026-01-01 10 | WARN | 1 |
| 2026-01-01 11 | INFO | 1 |

This query aggregates source LOG rows. It does not automatically use TAG ROLLUP. As data grows,
check the query range and execution plan, then separately assess whether preaggregation is needed.

A common mistake is applying `DURATION 1 HOUR` to data with fixed timestamps. That predicate uses
the current time and may exclude the samples on another execution date. Distinguish recent-log
queries in production from reproducible fixed-time queries.

<a id="수집과-보존을-연결합니다"></a>

## Collection and Retention Management

Continue with [Append Ingestion](../data-input-mutation/) for continuous collection. For long-term
operation, also define a [Retention Policy](../operations-lifecycle/). Source logs, backups, and
separate aggregates can require different retention periods.

```sql
DROP TABLE ch7_app;
```

Once the results match, substitute fields and messages from a few actual logs. Testing whether a
small sample answers the same questions makes issues easier to identify before migrating the full
collection pipeline.
