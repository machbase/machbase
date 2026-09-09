---
type: docs
title: '16.1.4 Relative Time Expressions'
weight: 40
toc: true
---

Relative time expressions specify offsets from a reference such as `NOW` or `SYSDATE` directly in
SQL. They provide concise time-series windows without separate function calls.

> Relative time literals such as `now - 1h` are supported from Machbase 8.0.50. Use `ADD_TIME` for month/year adjustments and `TO_DATE` for string conversion.

## Quick Reference

| Expression | Example | Description |
|------|------|------|
| `NOW` / `now` | `now` | Current time with nanosecond precision |
| `SYSDATE` / `sysdate` | `sysdate` | Current time (same as `NOW`) |
| `now - offset` | `now - 1h` | Subtract an offset from the current time |
| `now + offset` | `now + 30m` | Add an offset to the current time |
| Direct nanosecond integer | `value + 1000000000` | Add an integer number of nanoseconds to DATETIME |

## Relative Time Units (Literal Suffixes)

| Suffix | Meaning | Example |
|--------|------|------|
| `ns` | Nanoseconds | `500ns` |
| `us` | Microseconds | `20us` |
| `ms` | Milliseconds | `15ms` |
| `s` | Seconds | `45s` |
| `m` | Minutes | `30m` |
| `h` | Hours | `12h` |
| `d` | Days | `7d` |
| `w` | Weeks | `2w` (= 14 days) |

> Month (`month`, `mo`) and year (`year`, `y`) suffixes are not supported. Use `ADD_TIME()`
> to move by calendar months or years. `30d` and `365d` are fixed day counts and do not
> always equal a calendar month or year.

## ADD_TIME Function

Use `ADD_TIME()` for calendar adjustments such as months and years that relative time literals
cannot express. For arguments, format, and errors, see the
[SQL Function Dictionary](../functions/functions-full/#add_time).

## TO_DATE Function

Use `TO_DATE()` to create DATETIME values when specifying query boundaries as date strings.
For formats and conversion errors, see the [SQL Function Dictionary](../functions/functions-full/#to_date).

## Usage Patterns

### Filtering Time Windows

```sql
-- Last hour with a relative time literal
SELECT * FROM sensor_tag WHERE time > now - 1h;

-- Last hour with ADD_TIME
SELECT * FROM sensor_tag WHERE time > ADD_TIME(now, '0/0/0 -1:0:0');

-- Records from the last 24 hours
SELECT * FROM app_log WHERE _arrival_time BETWEEN now - 1d AND now;

-- Alarms from the last 10 minutes
SELECT alert_id, level, occurred_at FROM alert_log
 WHERE occurred_at >= sysdate - 10m;
```

### Compound Time Expressions

```sql
-- 2 days, 6 hours, and 15 minutes from now
SELECT * FROM maintenance_plan WHERE planned_at < now + 2d6h15m;

-- Combined subsecond units
SELECT TO_CHAR(now + 3s125ms10us4ns, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn');
```

### Applying Offsets to TO_DATE Results

```sql
-- Add 3 days to a date string
SELECT TO_CHAR(TO_DATE('2024-05-01', 'YYYY-MM-DD') + 3d, 'YYYY-MM-DD');
-- Result: 2024-05-04

-- Subtract 4 hours and 15 minutes from a date string
SELECT TO_CHAR(
    TO_DATE('2024-05-01 08:00:00', 'YYYY-MM-DD HH24:MI:SS') - 4h15m,
    'YYYY-MM-DD HH24:MI:SS'
);
-- Result: 2024-05-01 03:45:00
```

### Using Nanosecond Integers Directly

Numeric literals are interpreted as nanoseconds.

```sql
-- 1 second = 1,000,000,000 nanoseconds
SELECT event_time + 1000000000 AS event_time_plus_1s FROM events;

-- Subtract 250 nanoseconds
SELECT event_time - 250 AS event_time_minus_250ns FROM events;
```

## Constraints

- Relative time literals such as `1h` and `30m` require Machbase 8.0.50 or later.
- Month (`mo`) and year (`y`) literals are not supported. Use the year/month positions in `ADD_TIME()`.
- String literals are not implicitly converted to DATETIME in interval arithmetic. Convert them with `TO_DATE()` first.
- An interval itself cannot be used in `ORDER BY`.

## Error Handling

| Situation | Error | Resolution |
|------|------|-----------|
| Unsupported suffix (`1y`, `5mo`) | `ERR-02034` invalid time expression | Use `ADD_TIME()` for calendar units or supported suffixes such as `d` for fixed durations |
| Missing unit (`now + 10`) | Interpreted as nanoseconds | Specify the intended unit suffix |
| Excessive value (`1000000d`) | `ERR_OVERFLOW_INTERVAL` | Reduce the value |

<a id="log-duration"></a>

## DURATION for LOG Tables

Relative time literals and DURATION serve different purposes.
`event_time >= now - 1h` is a WHERE predicate on the selected column;
DURATION specifies the LOG `_arrival_time` range.
Use WHERE for TAG time columns and user-defined DATETIME columns.

```text
SELECT ... FROM log_table
 [WHERE ...]
 DURATION n unit [BEFORE base_time | AFTER base_time]
 [GROUP BY ...] [HAVING ...] [ORDER BY ...] [LIMIT ...]

SELECT ... FROM log_table
 [WHERE ...]
 DURATION FROM from_time TO to_time
 [GROUP BY ...] [HAVING ...] [ORDER BY ...] [LIMIT ...]
```

These are the basic forms. Durations use units such as `HOUR`, `MINUTE`, and `DAY`.
`ALL` can also specify the entire range.
Place DURATION after WHERE and before GROUP BY/ORDER BY.

| Form | Range | Specified Scan Direction |
|---|---|---|
| DURATION 1 HOUR | Last hour relative to the current time | Newest first |
| DURATION 1 HOUR BEFORE t | From t−1 hour to t | Newest first |
| DURATION 1 HOUR AFTER t | From t to t+1 hour | Oldest first |
| DURATION FROM a TO b, a < b | From a to b | Oldest first |
| DURATION FROM a TO b, a > b | From b to a | Newest first |

Both endpoints are inclusive. If FROM and TO are equal, rows at that timestamp are selected.
Distinguish scan direction from final output order after joins or aggregation.
Specify ORDER BY when order matters, with additional sort keys for rows sharing a timestamp.

The following example also selects row 2 at the end timestamp.

```sql
CREATE LOG TABLE ch7_ref_duration (event_id INTEGER);
INSERT INTO ch7_ref_duration(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1);
INSERT INTO ch7_ref_duration(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2);

SELECT event_id FROM ch7_ref_duration
 DURATION 1 HOUR BEFORE TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;

DROP TABLE ch7_ref_duration;
```

The result contains rows 1 and 2. When dividing data into consecutive daily ranges, use
half-open predicates such as `WHERE _arrival_time >= start_time AND _arrival_time < end_time`
to avoid counting boundary rows twice.
For queries combining LOG and LOOKUP, use a WHERE range on the LOG column instead of DURATION.

## Related Documentation

- [LOG Time-range Exercise](/dbms/log-table-usage/query-analysis/) — Compare boundaries, ordering, and joins
- [Relative Time Expressions](/dbms-8.5/sql-reference/time-expressions/) — Detailed 8.5 reference
