---
type: docs
title: '13.7 Schema Change Checklist'
weight: 80
toc: true
---

Before changing a production schema, check the following items in order.

## Pre-change checks

### 1. Check the table type

```sql
SELECT NAME AS TABLE_NAME, TYPE AS TABLE_TYPE
  FROM M$SYS_TABLES
 WHERE NAME = 'TARGET_TABLE';
```

ALTER TABLE support differs by table type. First check
[Management Support by Table Type](/dbms/reference/support-scope-constraints/table-types-type/).

### 2. Inspect the current schema

```sql
-- Inspect columns
DESC target_table;

-- Inspect indexes
SELECT i.NAME AS INDEX_NAME, i.TYPE AS INDEX_TYPE
  FROM M$SYS_INDEXES i
  JOIN M$SYS_TABLES t
    ON i.DATABASE_ID = t.DATABASE_ID
   AND i.TABLE_ID = t.ID
 WHERE t.NAME = 'TARGET_TABLE';
```

### 3. Check data volume

```sql
SELECT COUNT(*) FROM target_table;
```

Schema changes on large tables can take time. Measure duration and locking effects in a test
environment, then execute during the service's maintenance window.

### 4. Check retention policy activity

```sql
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'TARGET_TABLE';
```

If a retention job is running, wait for it to finish before changing the schema.

### 5. Configure the DDL conflict policy

Standard Edition can execute DDL concurrently on different objects. DDL on the same or directly
related objects conflicts, so first set the permitted wait time for the production deployment session.

```sql
-- Wait up to 10 seconds for a conflicting DDL lock
ALTER SESSION SET DDL_LOCK_TIMEOUT = 10;

-- Check each session's setting
SELECT id, user_name, ddl_lock_timeout
  FROM v$session
 WHERE closed = 0
 ORDER BY id;
```

| Concurrent targets | Result |
|----------------|------|
| Independent tables with different names | Can run concurrently |
| Same object or same name | Conflict |
| Table ALTER/DROP DDL and index DDL for that table | Conflict |
| View DDL and ALTER/DROP DDL on its source table | Conflict |
| TAG table ALTER/DROP DDL and its ROLLUP or retention DDL | Conflict |

Cluster Edition does not provide `DDL_LOCK_TIMEOUT` and uses the existing serialized DDL
policy. See [DDL Concurrency and Locking](/dbms/reference/sql/syntax/ddl-syntax/#ddl-concurrency)
for details.

---

## Checklist for adding columns

- [ ] Is the new column's data type supported by this table type?
- [ ] For LOG/TRANSACTION tables, are you aware that the new column is NULL in existing rows?
- [ ] Check for duplicate column names.

```sql
ALTER TABLE sensor_log ADD COLUMN (new_col DOUBLE);
```

---

## Checklist for dropping columns

- [ ] Is the column included in an index? Drop the index first.
- [ ] Do application queries reference the column?
- [ ] Data in a dropped column cannot be recovered.

```sql
ALTER TABLE sensor_log DROP COLUMN (old_col);
```

---

## Checklist for index changes

- [ ] Creating or dropping an index directly affects query performance.
- [ ] Index creation also indexes existing data and can take time on large tables.
- [ ] Consider dropping unused indexes because they slow INSERT operations.
- [ ] With `IF NOT EXISTS`, separately verify the existing index definition for the same name.

```sql
-- Create conditionally during repeat deployments
CREATE INDEX IF NOT EXISTS idx_new ON sensor_log (sensor_id);

-- Verify the actual mapping; a name match may cause a no-op
SHOW INDEX idx_new;

-- Drop an unnecessary index
DROP INDEX idx_old;
```

`IF NOT EXISTS` checks only the index name within the same database and owner. Separately verify
that the existing table, columns, index type, and properties match the intended deployment,
following [INDEX Syntax](/dbms/reference/sql/syntax/index-syntax/#create-index-if-not-exists).

---

## Checklist for retention policy changes

- [ ] To change a policy: detach the existing policy, then create and attach the new policy.
- [ ] Shortening retention can increase the next deletion job's scope. Assess possible data loss.

```sql
-- Detach the existing policy
ALTER TABLE sensor_tag DROP RETENTION;

-- Attach the new policy
ALTER TABLE sensor_tag ADD RETENTION new_policy;
```

---

## Handle DDL conflicts

With the default `DDL_LOCK_TIMEOUT=0`, a conflict immediately returns
`ERR-02031: Resource busy (<object>)`.

1. Retry only `ERR-02031`, with a bounded retry count and wait intervals.
2. Before retrying, query the current state of the target and dependent objects again.
3. After waiting, `already exists` or `table not found` may be returned depending on the preceding DDL.
4. Do not repeatedly retry the same SQL for syntax errors, privilege errors, `already exists`, or `table not found`.
5. Automation using `machsql` must check output for `ERR-` as well as the process exit code.

You can execute DDL again after a lock wait expires or an operation is canceled, but first
check whether the preceding operation took effect.

---

## Post-change validation

```sql
-- Verify the schema change
DESC target_table;

-- Check data consistency
SELECT COUNT(*) FROM target_table;

-- Inspect index state
SELECT i.NAME AS INDEX_NAME, i.TYPE AS INDEX_TYPE
  FROM M$SYS_INDEXES i
  JOIN M$SYS_TABLES t
    ON i.DATABASE_ID = t.DATABASE_ID
   AND i.TABLE_ID = t.ID
 WHERE t.NAME = 'TARGET_TABLE';
```

---

**Read next:**

- [Data Retention Policies](/dbms/operations-configuration-recovery/policy-data-retention/)
- [Operations and Configuration](/dbms/operations-configuration-recovery/)
