---
type: docs
title: '10.7 Operations and Data Lifecycle'
weight: 70
toc: true
aliases:
  - /dbms/volatile-table-usage/memory-lifecycle/
  - /dbms/volatile-table-usage/restart-data-loss/
  - /dbms/volatile-table-usage/memory-monitoring-cache-rebuild/
---

This section describes the procedures for creating, loading, using, discarding, and rebuilding
VOLATILE table data.

<a id="operations-volatile-lifecycle"></a>
<a id="lifecycle-memory"></a>

## Data Lifecycle

1. Run the table creation SQL after the server starts.
2. Load initial data from a persistent source if needed.
3. Start application queries and updates.
4. Write results that must be retained to persistent tables.
5. Data is lost when the server shuts down. Table definitions remain.

<a id="operations-volatile-session-scope"></a>

## Sharing Across Sessions

VOLATILE tables are shared server-wide. A row inserted by one session can be queried by another.
Closing a connection alone does not remove data.

<a id="operations-volatile-flush"></a>

## Separating Temporary and Persistent Data

Store only current state or intermediate results that can be rebuilt from source data in VOLATILE.
Store audit records, source events, and results that cannot be recreated in TAG, LOG, LOOKUP, or
TRANSACTION tables. Manage copy SQL as a separate job, including source and target columns,
duplicate handling, and execution frequency.

<a id="operations-volatile-restart"></a>
<a id="data-loss"></a>

## Restart Procedure

- Check whether the table exists. A restart preserves its definition, so recreation is usually unnecessary.
- If a persistent source exists, load only data for the defined reference point in time.
- Check the expected row count and latest timestamp.
- Resume collector and application writes after validation.
- If rebuilding fails, confirm that the service operates safely with an empty cache.

<a id="operations-volatile-checklist"></a>

## Operations Checklist

- Keep initial load SQL in version control, together with creation SQL for the first deployment.
- Validate scripts in advance using the operational account and actual connection settings.
- Monitor row counts and memory limits.
- Check that data requiring retention is not stored only in VOLATILE.
- Verify the loading and validation sequence during restart drills.

## Checking Memory and Rebuilding Caches

```sql
SELECT * FROM V$STORAGE_DC_VOLATILE_TABLE;
SELECT * FROM V$SYSMEM;
SELECT * FROM V$SESMEM;

SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME = 'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE';
```

Check the view definitions for your deployed version instead of relying on specific internal column
names. When rebuilding a cache, record the row count and sample values, redirect its consumers, and
then create the table, load initial data, and validate it in that order. The service must be able to
operate safely with an empty cache if rebuilding fails.
