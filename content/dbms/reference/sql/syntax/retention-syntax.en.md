---
type: docs
title: 'RETENTION syntax'
weight: 160
toc: true
---

RETENTION policies periodically delete expired data from TAG, KV, and LOG tables. They do not apply
to TRANSACTION, LOOKUP, or VOLATILE.

<a id="create-retention"></a>

## Creating a RETENTION Policy

```sql
create_retention_stmt ::=
    'CREATE RETENTION' policy_name
    'DURATION' positive_integer ( 'MONTH' | 'DAY' | 'HOUR' | 'MIN' | 'SEC' )
    'INTERVAL' positive_integer ( 'DAY' | 'HOUR' | 'MIN' | 'SEC' )
```

| Parameter | Description |
|----------|------|
| `policy_name` | Policy name |
| `DURATION duration MONTH\|DAY\|HOUR\|MIN\|SEC` | Data retention period (MONTH is a fixed 30 days) |
| `INTERVAL interval DAY\|HOUR\|MIN\|SEC` | Deletion execution interval |

```sql
-- Retain 1 day; delete every hour
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;

-- Retain 30 days; delete daily
CREATE RETENTION policy_30d_1d DURATION 30 DAY INTERVAL 1 DAY;

-- Retain 3 months; delete daily
CREATE RETENTION policy_3m_1d DURATION 3 MONTH INTERVAL 1 DAY;
```

<a id="drop-retention"></a>

## Dropping a RETENTION Policy

```sql
drop_retention_stmt ::= 'DROP RETENTION' policy_name
```

```sql
DROP RETENTION policy_1d_1h;
```

## Assigning a RETENTION Policy to a Table

```sql
alter_table_add_retention_stmt ::=
    'ALTER TABLE' table_name 'ADD RETENTION' policy_name
```

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h;
```

## Detaching a RETENTION Policy from a Table

```sql
alter_table_drop_retention_stmt ::=
    'ALTER TABLE' table_name 'DROP RETENTION'
```

```sql
ALTER TABLE sensor_tag DROP RETENTION;
```

## Listing RETENTION Policies

Query system tables for registered policies and their assignments.

```sql
-- Query all RETENTION policies
SELECT * FROM M$RETENTION;

-- Check assigned jobs and the last deletion cutoff by table
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB
 ORDER BY USER_NAME, TABLE_NAME;
```

## Complete Example

```sql
-- 1. Create a policy: retain 1 day and delete hourly
CREATE RETENTION ret_1d DURATION 1 DAY INTERVAL 1 HOUR;

-- 2. Create a TAG table
CREATE TAG TABLE sensor_tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 3. Assign the policy to the table
ALTER TABLE sensor_tag ADD RETENTION ret_1d;

-- 4. Check policy assignment
SELECT * FROM M$RETENTION;

-- 5. Detach the policy
ALTER TABLE sensor_tag DROP RETENTION;

-- 6. Drop the policy
DROP RETENTION ret_1d;
```

## Considerations

- RETENTION policies apply to LOG and TAG tables.
- KV tables are also supported.
- Only one policy can be assigned to a table.
- MONTH means a fixed 30 days, not a calendar month. If calendar boundaries matter, convert to DAY units and verify actual deletion cutoffs.
- Deleted rows cannot be recovered, so choose retention periods and execution intervals carefully. DROP RETENTION removes only the policy object after detachment from every table.
- INTERVAL determines how often deletion runs; actual deletion can be slightly delayed.
- Missing policies, unsupported table types, and duplicate policy assignments to one table cause errors.
- Detach an in-use policy from every table before dropping it.

## Related Documentation

- [Role of Retention Policy](/dbms/core-concepts/features-concepts/#role-retention-policy) — Automatic data deletion concepts
