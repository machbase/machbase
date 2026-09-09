---
type: docs
title: '7.10 _arrival_time Time Model'
weight: 100
toc: true
---

A source log may contain yesterday's timestamp while a query treats it as data collected today.
Mixing event time and collection time can make valid ingestion look like missing data.
Distinguishing them is fundamental to LOG queries and retention policies.

<a id="time-model-arrival-time"></a>

<a id="두-시각은-서로-다른-질문에-답합니다"></a>

## Event Time and Arrival Time

A user-defined DATETIME column such as `event_time` answers when the event occurred. The
automatically created `_arrival_time` is the basis for LOG time-range access and retention deletion.
If omitted, it uses the server time. However, explicit input and out-of-order adjustment mean that
it does not always represent the actual network reception time.

DATETIME represents values in nanoseconds. This does not mean the server clock measures every
timestamp with nanosecond precision. Once stored, a timestamp cannot be corrected with UPDATE on a
LOG table.

<a id="늦게-도착한-이벤트를-확인해-봅니다"></a>

## Querying Late Events

This example inserts explicit arrival timestamps in ascending order into an empty table.

```sql
CREATE LOG TABLE ch7_time (
    event_id   INTEGER,
    event_time DATETIME,
    message    VARCHAR(64)
);

INSERT INTO ch7_time(_arrival_time, event_id, event_time, message)
VALUES (TO_DATE('2026-01-02 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1,
        TO_DATE('2026-01-02 09:59:00', 'YYYY-MM-DD HH24:MI:SS'), 'normal arrival');
INSERT INTO ch7_time(_arrival_time, event_id, event_time, message)
VALUES (TO_DATE('2026-01-02 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 2,
        TO_DATE('2026-01-01 23:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'delayed arrival');

SELECT event_id
  FROM ch7_time
 WHERE event_time >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
   AND event_time <  TO_DATE('2026-01-02', 'YYYY-MM-DD')
 ORDER BY event_id;

SELECT event_id
  FROM ch7_time
 DURATION FROM TO_DATE('2026-01-02 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-02 10:01:00', 'YYYY-MM-DD HH24:MI:SS');
```

The event-time query selects only event 2; the arrival-time query selects both events 1 and 2. There
is no need to alter the event timestamp of a late arrival.

<a id="역전-입력은-그대로-저장되지-않을-수-있습니다"></a>

## Out-of-Order Timestamps and Adjustment

`DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE` controls how a timestamp earlier than the previous arrival
timestamp is handled. The current Standard implementation behaves as follows.

| Value | Handling of out-of-order input |
|---|---|
| 1 (default) | Adjust to 1 ns after the previously stored `_arrival_time` |
| 0 | Reject the insert with a time-inversion error |

Equal timestamps are not out of order, so this rule does not guarantee a unique timestamp for every
row. To guarantee ordering when timestamps are equal, add another key, such as an event number, to
ORDER BY.

The following optional exercise uses the same table. Check the setting first and run it only in a
validation environment where the value is 1. Do not change a production server setting for this
example.

```sql
SELECT NAME, VALUE FROM V$PROPERTY
 WHERE NAME = 'DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE';
```

```sql
-- Run with setting 1. Setting 0 is expected to reject the insert.
INSERT INTO ch7_time(_arrival_time, event_id, event_time, message)
VALUES (TO_DATE('2026-01-02 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3,
        TO_DATE('2026-01-02 08:59:00', 'YYYY-MM-DD HH24:MI:SS'), 'inverted arrival');

SELECT event_id,
       TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn') AS stored_time
  FROM ch7_time
 ORDER BY event_id;
```

With setting 1, event 3 is stored at `2026-01-02 10:01:00 000:000:001`, not the supplied 09:00
timestamp. The event time remains unchanged. Allowing time inversion therefore does not mean
preserving every historical timestamp as supplied.

<a id="이관에서는-정렬과-대상-상태를-함께-확인하세요"></a>

## Data Migration Considerations

To preserve source `_arrival_time` values, normally insert into an empty target in ascending order.
Even sorted input can be adjusted or rejected if the target already contains newer rows or
concurrent ingestion intervenes. Do not mix migration and ordinary real-time collection in the same
table.

`DURATION` uses `_arrival_time`, not `event_time`. If the range differs even after matching time
zones and date formats, check which time column the query uses. For boundaries and output order,
continue to [Query Examples](../query-analysis/).

```sql
DROP TABLE ch7_time;
```

When reporting a time-related issue, provide the source timestamp, stored timestamp, and setting
value. Comparing all three helps distinguish conversion from adjustment.
