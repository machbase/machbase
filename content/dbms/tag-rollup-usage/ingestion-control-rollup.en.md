---
type: docs
title: '6.9 ROLLUP Control and State'
weight: 90
toc: true
aliases:
  - /dbms/tag-rollup-usage/state-check-rollup/
  - /dbms/tag-rollup-usage/operational-notes-rollup/
---

<a id="ingestion-start-stop-immediate-collect-rollup"></a>

## Job State and Processing Completion

ROLLUP starts automatically at creation. Repeating START immediately or stopping an already stopped
job can cause a state error. This exercise separates states in the sequence create → STOP → insert →
START → WAKEUP → FORCE.

```sql
CREATE TAG TABLE ch6_control (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_control_ru ON ch6_control(value)
  INTERVAL 1 MIN WAKEUP INTERVAL 10 SEC;
ALTER ROLLUP ch6_control_ru STOP;
INSERT INTO ch6_control VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_control VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_control VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_control VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_control);

SELECT DISTINCT ROLLUP_NAME, ENABLED, INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CONTROL_RU';

ALTER ROLLUP ch6_control_ru START;
ALTER ROLLUP ch6_control_ru WAKEUP;
ALTER ROLLUP ch6_control_ru FORCE;

SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_control WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

While stopped, ENABLED is 0, INTERVAL_TIME is 60000 ms, and WAKEUP_INTERVAL is 10000 ms. The final
query returns TEMP_01 averages of 15 at 00:00 and 30 at 00:01.

| Command | Purpose | Completion meaning |
|---|---|---|
| STOP | Stop the job | Unprocessed input remains |
| START | Resume a stopped job | Continue from the processing position |
| WAKEUP | Wake the job | Does not wait for processing completion |
| FORCE | Wait for the target source processing range to catch up | Does not recalculate historical corrections or complete future input |
| ROLLUP_REBUILD | Recalculate historical buckets for supported targets | Rebuild aggregates after source corrections |

Instead of SQL ALTER, you can use named `EXEC ROLLUP_START(name)`, `ROLLUP_STOP(name)`, and
`ROLLUP_FORCE(name)` calls. Do not execute the same transition consecutively using both forms.
Distinguish unnamed bulk control from control of a specific job.

## WAKEUP INTERVAL

If omitted, WAKEUP INTERVAL equals the creation INTERVAL. It must be positive, no greater than the
aggregation interval, and divide that interval exactly. More frequent wakeups can reduce lag but
increase processing load.

```sql
ALTER ROLLUP ch6_control_ru SET WAKEUP INTERVAL 5 SEC;
SELECT DISTINCT ROLLUP_NAME, INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CONTROL_RU';
```

WAKEUP_INTERVAL becomes 5000 ms. The next statement intentionally fails because its interval does
not divide 60 seconds.

```sql
ALTER ROLLUP ch6_control_ru SET WAKEUP INTERVAL 7 SEC;
```

<a id="state-status-rollup-wakeup-interval-vrollup"></a>

## Reading V$ROLLUP

| Column | Meaning |
|---|---|
| ROLLUP_NAME | Job name used for control |
| ROLLUP_TABLE | Aggregate target table; user target TAG for Custom |
| SOURCE_TABLE, ROOT_TABLE | Direct source and root-source relationship |
| COLUMN_NAME | Column aggregated in general/path mode |
| INTERVAL_TIME, WAKEUP_INTERVAL | Creation and wakeup intervals in milliseconds |
| LAST_WAKEUP_TIME, NEXT_WAKEUP_TIME | Previous wakeup and next scheduled wakeup |
| EXT_TYPE | 0 general, 1 extension, 2 Custom |
| PREDICATE | General predicate or Custom SELECT body |
| ENABLED | Whether the job is enabled |
| RUN_STATE | `I` initial, `S` waiting, `R` processing |
| END_RID | Source processing position |
| LAST_ELAPSED_MSEC | Previous processing time in ms |
| DATABASE_NAME, USER_ID | Database and owner identifiers |

```sql
SELECT ROLLUP_NAME, ROLLUP_TABLE, SOURCE_TABLE, ROOT_TABLE,
       INTERVAL_TIME, WAKEUP_INTERVAL, LAST_WAKEUP_TIME, NEXT_WAKEUP_TIME,
       ENABLED, RUN_STATE, LAST_ELAPSED_MSEC
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CONTROL_RU'
 ORDER BY ROLLUP_NAME;
SHOW ROLLUPGAP;
```

SHOW ROLLUPGAP is a machsql-only client command; do not send it to an SDK's ordinary SQL API. GAP is
the difference between source and ROLLUP processing RIDs, not elapsed time lag. Check it alongside
all hierarchy levels and relevant nodes. gap=0 does not mean corrections to already aggregated
source data are reflected. During continuous input it changes with observation time, so pause input
for reproducible comparisons.

If retention deletes source data while a job is stopped, START cannot restore it. Run FORCE from
lower to upper levels. On failure, check the first error, state, and source accessibility.

## Clean Up

```sql
DROP ROLLUP ch6_control_ru;
DROP TABLE ch6_control;
```

For detailed command contracts, see the
[EXEC Reference](../../reference/sql/syntax/execute-procedure-syntax/) and
[ROLLUP Troubleshooting](../../troubleshooting/rollup/).
