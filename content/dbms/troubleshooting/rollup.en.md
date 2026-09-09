---
type: docs
title: '15.7 ROLLUP Problems'
weight: 70
toc: true
aliases:
  - /dbms/tag-rollup-usage/constraints-errors-troubleshooting/rollup-troubleshooting/
---

When ROLLUP results lag or differ from raw data, first distinguish processing delay from
differences in aggregation semantics. Replace sample names with the actual tables and jobs
being diagnosed. Do not start by dropping and recreating them.

## 1. Check state and scope

```sql
SELECT ROLLUP_NAME, ROLLUP_TABLE, ROOT_TABLE, EXT_TYPE,
       INTERVAL_TIME, WAKEUP_INTERVAL, ENABLED, RUN_STATE, LAST_ELAPSED_MSEC
  FROM V$ROLLUP ORDER BY ROLLUP_NAME;
SHOW ROLLUPGAP;
```

SHOW ROLLUPGAP is a machsql command; do not send it through an SDK SQL API. The gap is a
difference in processed RIDs, not a direct measure of time lag or completion of raw-data
corrections. Record state across all levels and Cluster nodes, along with the server build,
database, and owner.

## 2. Compare the same dataset

| Symptom | Check |
|---|---|
| Some samples are missing | Whether a conditional ROLLUP candidate was selected and matches the raw-data filter |
| FIRST/LAST error | Whether the selected candidate is EXTENSION |
| No candidate for monthly/daily queries | Whether stored-interval selection rules were confused with query buckets |
| Average differs | NULL handling, valid counts, reaggregation of partial averages, and tag grouping |
| Values unchanged after raw-data correction | Whether FORCE was incorrectly used to revisit history and REBUILD is needed |
| JSON counts differ | Distinction among source documents, SQL NULL, per-path counts, and document aggregate counts |

Query raw data with DATE_TRUNC/DATE_BIN and GROUP BY, and stored aggregates with rollup().
Keep tags, timestamps, origin, end boundaries, and aggregate functions identical. Do not
assume rollup() falls back to a raw-data scan when no applicable ROLLUP exists.

## 3. Catch up with new input

Verify that the target job is active and specify the required job by name.

```sql
ALTER ROLLUP rollup_name FORCE;
SHOW ROLLUPGAP;
```

WAKEUP only wakes a job; FORCE waits for it to catch up to the processing range. After
checking a stopped job's state, START it. Process multiple levels from the lowest upward.
`ALTER SYSTEM FLUSH ROLLUP` is unsupported and must not be used as a diagnostic command.

## 4. Historical corrections and rebuilding

Even in Standard Edition, not every ROLLUP configuration supports REBUILD. First check for
a complete automatic hierarchy, supported Custom intervals and buckets, and retained raw
data. Use supported constant strings or TO_DATE expressions for time arguments. The entire
bucket containing the specified timestamp is recalculated.

Account for stopping and restarting related jobs and for partial failures. After success or
failure, verify results and actual active state. Follow the
[REBUILD Tutorial](../../tag-rollup-usage/rollup-rebuild/) and
[Argument Contract](../../reference/sql/syntax/rollup-rebuild-syntax/).

## 5. Information for support

- Server build, edition, client, and connection target
- TAG schema, ROLLUP definitions, predicates, and dependencies
- State, gap, and observation time
- Compared raw-data and ROLLUP SQL, time zone, origin, expected and actual results
- First error and recent raw-data corrections, deletions, bulk ingestion, or configuration changes
