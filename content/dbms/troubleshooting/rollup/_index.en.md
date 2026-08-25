---
type: docs
title: '16.7 ROLLUP Problems'
weight: 70
toc: true
aliases:
  - /dbms/tag-rollup-usage/constraints-errors-troubleshooting/rollup-troubleshooting/
---

When ROLLUP results are delayed or differ from a raw-data aggregation, inspect state, gap, time
boundaries, and rebuild requirements in that order.

## Check state and gap

```sql
SHOW ROLLUPGAP;

SELECT ROLLUP_TABLE,
       INTERVAL_TIME,
       WAKEUP_INTERVAL,
       LAST_ELAPSED_MSEC,
       RUN_STATE
  FROM V$ROLLUP
 ORDER BY ROLLUP_TABLE;
```

Use the [V$ROLLUP reference](/dbms/reference/log-logs-system-catalog/dictionary-vrollup/) for exact
columns. A remaining gap can mean that recent data is still being aggregated.

## Compare identical ranges

Use the same tag, start and end boundaries, timezone, and bucket for raw and ROLLUP queries. After
normal new input, `ALTER SYSTEM FLUSH ROLLUP` can request immediate processing; verify that the gap
decreases instead of repeating the command blindly.

## Rebuild corrected data

After correcting historical TAG rows, verify whether Standard Edition `ROLLUP_REBUILD` applies.
Cluster Edition does not support it. See
[ROLLUP_REBUILD](/dbms/tag-rollup-usage/rollup-rebuild/) for arguments and verification.

Collect the server build and Edition, ROLLUP definition, TAG schema, gap and state output, exact SQL
range, first server error, and recent data or configuration changes before requesting support.
