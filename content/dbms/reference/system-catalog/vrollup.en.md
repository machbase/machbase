---
type: docs
title: '16.3.3 V$ROLLUP Dictionary'
weight: 30
toc: true
---

`V$ROLLUP` is a virtual table that shows the current status of Tag data rollup jobs. Use it to check
rollup operation and monitor execution intervals and elapsed time.

## Column Details

| Column | Type | Description |
|----------|------|------|
| `ID` | INTEGER | Rollup job ID |
| `ROLLUP_NAME` | VARCHAR | Rollup job name |
| `ROLLUP_TABLE` | VARCHAR | Table that stores rollup results |
| `SOURCE_TABLE` | VARCHAR | Source TAG table to aggregate |
| `COLUMN_NAME` | VARCHAR | Column to aggregate |
| `INTERVAL_TIME` | ULONG | Data aggregation interval in milliseconds |
| `WAKEUP_INTERVAL` | ULONG | Rollup job execution interval in milliseconds |
| `LAST_WAKEUP_TIME` | DATETIME | Most recent execution timestamp |
| `ENABLED` | INTEGER | Whether enabled (1: enabled, 0: disabled) |
| `LAST_ELAPSED_MSEC` | DOUBLE | Duration of the previous execution in milliseconds |
| `RUN_STATE` | VARCHAR | Thread state (I: initializing, S: sleeping, R: running) |

## RUN_STATE Values

| Value | Description |
|----|------|
| `I` | Initializing |
| `S` | Sleeping until the next execution |
| `R` | Currently running |

## SQL Examples

```sql
-- Check all rollup job statuses
SELECT rollup_name, rollup_table, source_table, column_name,
       interval_time, wakeup_interval, enabled, last_elapsed_msec, run_state
  FROM v$rollup
 ORDER BY rollup_table;

-- Check the most recent execution timestamp
SELECT rollup_name, rollup_table, last_wakeup_time, last_elapsed_msec, run_state
  FROM v$rollup;

-- Check disabled rollups
SELECT rollup_name, rollup_table, source_table, enabled
  FROM v$rollup
 WHERE enabled = 0;

-- Check long-running rollups
SELECT rollup_name, rollup_table, wakeup_interval, last_elapsed_msec,
       last_elapsed_msec * 100.0 / wakeup_interval AS usage_ratio
  FROM v$rollup
 WHERE last_elapsed_msec > 0
   AND wakeup_interval > 0
 ORDER BY last_elapsed_msec DESC;
```

## Notes

- `INTERVAL_TIME` is the data aggregation interval; `WAKEUP_INTERVAL` is the rollup job execution interval.
- If `LAST_ELAPSED_MSEC` exceeds `WAKEUP_INTERVAL`, the previous execution took longer than the configured interval.
  Check the amount of source data and the execution interval. The example's `usage_ratio` is the
  previous execution duration as a percentage of the interval.
- `ENABLED = 0` means the rollup is disabled. Re-enable it with `ALTER ROLLUP rollup_name START`.
  Set `rollup_name` to the queried `ROLLUP_NAME` value.
- For rollup creation and management, see [TAG Tables and Rollup](/dbms/tag-rollup-usage/overview-use-criteria/#rollup).
