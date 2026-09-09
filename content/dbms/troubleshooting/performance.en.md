---
type: docs
title: '15.4 Query and Performance Problems'
weight: 40
toc: true
---

<a id="slow"></a>

## A query is slow

Record the affected SQL, bind value ranges, start and end times, and expected and actual row counts.

```sql
SELECT ID, SESS_ID, STATE, QUERY
  FROM V$STMT
 ORDER BY ID;

EXPLAIN SELECT ...;
```

Check the execution plan for the following:

- Are time and tag predicates applied early enough?
- Are large tables scanned repeatedly without need?
- Do join key types and value formats match?
- Is the required index or ROLLUP actually used?
- Are unnecessary columns or rows being read?

The current MINMAX cache property is `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE`. Record
the current value and execution plan before changing it, then compare in an isolated
environment. Follow [Performance Tuning](/dbms/performance-tuning/) for the detailed procedure.

<a id="search-results"></a>

## Query results differ from expectations

```sql
SELECT COUNT(*), MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME)
  FROM target_log;
```

1. Verify the target database, owner, and table name.
2. Read a small sample without filters to check data presence and actual timestamps.
3. Check the connection time zone and how input string time zones are interpreted.
4. Check tag names, case, and boundary operators (`>`, `>=`, `<`, `<=`).
5. For ROLLUP results, check the gap and update state.

Do not look for a server property named `DEFAULT_TIMEZONE`. Specify the time zone through
client connections and sessions, and record the source data's reference time zone.

```sql
SHOW ROLLUPGAP;
SELECT * FROM V$ROLLUP;
```

<a id="memory-out-of"></a>

## Insufficient memory

```sql
SELECT * FROM V$SYSMEM;
SELECT ID, SESS_ID, STATE, QUERY FROM V$STMT ORDER BY ID;
```

Check OS memory, swap, and OOM records alongside Machbase logs from the same time. Separately
reproduce queries fetching large results at once, large joins and sorts, excessive concurrency,
and large client fetch or Append buffers.

Query current settings in `V$PROPERTY`. Check allowed ranges and change procedures in the
[Configuration Reference](/dbms/reference/configuration/configuration/), then load-test
each change individually before applying it.
