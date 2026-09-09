---
type: docs
title: '7.5 Query and Analysis'
weight: 50
toc: true
---

Small changes to a time range can change the row count. When aggregating consecutive days, including
the endpoint in both intervals counts boundary rows twice. This section uses fixed timestamps to
check ranges and result order, then joins reference data.

<a id="original-85-select-data"></a>

<a id="경계에-걸리는-데이터를-준비합니다"></a>

## Prepare Example Data

```sql
CREATE LOG TABLE ch7_query (
    event_id INTEGER,
    device   VARCHAR(32),
    value    DOUBLE
);

INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1, 'DEV-01', 10);
INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 'DEV-01', 20);
INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 'DEV-02', 30);
INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 4, 'DEV-02', 40);

SELECT _arrival_time, event_id, device, value
  FROM ch7_query
 ORDER BY _arrival_time, event_id;
```

Results appear in the order 1, 2, 3, 4. Because rows 2 and 3 share a timestamp, include the event
number as well as time in ORDER BY to guarantee the order. This number is managed explicitly in the
example, not an automatic LOG unique key.

<a id="연속-구간에는-시작-포함끝-제외-조건이-편리합니다"></a>

## Consecutive Intervals and Time Boundaries

```sql
SELECT event_id, value
  FROM ch7_query
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;
```

Rows 1, 2, and 3 are selected. Starting the next interval at 12:00 counts row 4 only in that
interval. `BETWEEN` includes both endpoints and therefore has different semantics. Use the same
WHERE pattern when analyzing a user-defined `event_time` column.

<a id="original-85-select-time-data"></a>

<a id="duration은-log의-도착-시각을-사용합니다"></a>

## DURATION Queries

```sql
SELECT event_id FROM ch7_query
 DURATION 1 HOUR BEFORE TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;

SELECT event_id FROM ch7_query
 DURATION 1 HOUR AFTER TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;

SELECT event_id FROM ch7_query
 DURATION FROM TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;
```

| Query | Time range | Selected event_id values |
|---|---|---|
| 1 hour before 12:00 | 11:00–12:00, inclusive | 2, 3, 4 |
| 1 hour after 10:00 | 10:00–11:00, inclusive | 1, 2, 3 |
| From 10:00 to 12:00 | Both endpoints included | 1, 2, 3, 4 |

If the reference time is omitted, as in `DURATION 1 HOUR`, the current time is used. This may return
no rows for an exercise with old fixed timestamps. Place DURATION after WHERE and before GROUP BY or
ORDER BY.

Do not assume DURATION applies to every time column. It is LOG-specific and uses `_arrival_time`.
Use WHERE for TAG time columns or user-defined DATETIME predicates. For syntax details, see
[Relative Time and DURATION Dictionary](/dbms/reference/sql/relative-time/#log-duration).

<a id="스캔-방향과-최종-정렬을-구분합니다"></a>

## Scan Direction and Sorting

DURATION BEFORE reads from newest to oldest; AFTER reads from oldest to newest. FROM … TO changes
direction according to the order of its two timestamps. The following examples check a reversed
range and a range whose endpoints are equal.

```sql
SELECT event_id FROM ch7_query
 DURATION FROM TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id DESC;

SELECT event_id FROM ch7_query
 DURATION FROM TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;
```

The first result is ordered 4, 3, 2, 1; the second, with equal endpoints, returns 2 and 3. Explicit
ORDER BY clauses fix the output order independently of scan direction.

Use ORDER BY whenever the final result order matters, including results with aggregates or joins. In
particular, do not infer which rows will be returned from LIMIT alone.

The global `TABLE_SCAN_DIRECTION` setting can affect other queries. Do not start by changing server
settings to alter display order. Check the execution plan in
[Query Tuning](/dbms/performance-tuning/performance-query-tuning/) before adjusting access paths.

<a id="original-85-simple-join"></a>

<a id="작은-lookup-테이블로-장치-설명을-붙입니다"></a>

## Joining LOOKUP Tables

```sql
CREATE LOOKUP TABLE ch7_query_device (
    device VARCHAR(32) PRIMARY KEY,
    label  VARCHAR(64)
);
INSERT INTO ch7_query_device VALUES ('DEV-01', 'Boiler');
INSERT INTO ch7_query_device VALUES ('DEV-02', 'Pump');

SELECT q.event_id, d.label, q.value
  FROM ch7_query q
  JOIN ch7_query_device d ON q.device = d.device
 WHERE q._arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND q._arrival_time <  TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY q.event_id;
```

The results are `(1, Boiler, 10)`, `(2, Boiler, 20)`, and `(3, Pump, 30)`. Because this query
combines LOG and LOOKUP, it uses a WHERE range on the LOG column instead of DURATION. This INNER
JOIN also excludes events without matching reference data.

Joining current LOOKUP values does not reconstruct a device description from the time of an event.
For historical descriptions, store the description in the event or design a separate history with
validity periods.

```sql
DROP TABLE ch7_query_device;
DROP TABLE ch7_query;
```

If the row count differs from expectations, first check time boundaries and the count before the
join. Add predicates one at a time to locate where rows are excluded.
