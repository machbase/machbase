---
type: docs
title: '13.5 Data Retention Policies'
weight: 50
toc: true
---

A retention policy periodically deletes data older than a cutoff time from TAG, KV, and LOG
tables. `DURATION` specifies the retention period; `INTERVAL` specifies the deletion job frequency.
Retention policies cannot be applied to TRANSACTION, VOLATILE, or LOOKUP tables.

```text
Create policy → Attach to table → Check job status → Detach from table → Drop policy
```

<a id="retention-policy"></a>

## Retention Policy

Before defining a production policy, review legal retention obligations, recovery requirements,
hourly ingestion volume, and deletion load together. Do not choose `INTERVAL` using a fixed ratio.
Use an interval sufficiently longer than the deletion time measured in production.

Check policies and their attachment state in these views:

```sql
SELECT * FROM M$RETENTION;
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB;
```

<a id="create-retention-policy"></a>
<a id="retention-policy-create-retention-policy"></a>

### Create a retention policy

```sql
CREATE RETENTION policy_name
    DURATION duration_value {MONTH|DAY|HOUR|MIN|SEC}
    INTERVAL interval_value {DAY|HOUR|MIN|SEC};
```

`DURATION` accepts units from months to seconds; `INTERVAL` accepts `DAY` through `SEC`. `MONTH`
means a fixed 30 days, not a calendar month. For policies where calendar boundaries matter, such
as legal retention, convert the period to `DAY` and verify the actual deletion cutoff. For exact
parser syntax and supported table types, see
[RETENTION Syntax](/dbms/reference/sql/syntax/retention-syntax/).

For example, this policy retains 30 days of data and processes eligible deletions once a day.

```sql
CREATE RETENTION policy_30d DURATION 30 DAY INTERVAL 1 DAY;
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_30D';
```

Creating and dropping policies requires the appropriate administrative privileges. Check
privileges and the approved change scope before using a production account.

<a id="retention-policy-retention-policy"></a>

### Attach a policy to a table

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_30d;

SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE
  FROM V$RETENTION_JOB
 WHERE TABLE_NAME = 'SENSOR_TAG';
```

A table can have only one policy. TAG tables determine data age using `BASETIME`; LOG tables
use `_ARRIVAL_TIME`. Deletion runs at the configured interval, not immediately upon attachment.

<a id="detach-retention-policy"></a>
<a id="retention-policy-detach-retention-policy"></a>

### Detach a policy from a table

```sql
ALTER TABLE sensor_tag DROP RETENTION;
```

Detaching stops automatic deletion but does not recover data already deleted. After detaching,
verify that the target table no longer appears in `V$RETENTION_JOB`.

<a id="delete-retention-policy"></a>
<a id="retention-policy-delete-retention-policy"></a>

### Drop a retention policy

First detach the policy from every table that uses it, then drop the policy object.

```sql
SELECT USER_NAME, TABLE_NAME
  FROM V$RETENTION_JOB
 WHERE POLICY_NAME = 'POLICY_30D';

-- Run after detaching the policy from each returned table
DROP RETENTION policy_30d;
```

`ALTER TABLE ... DROP RETENTION` detaches the policy from a table; `DROP RETENTION` deletes the
policy object. A policy still in use cannot be dropped.

<a id="applicable-privileges-retention-sys"></a>
<a id="retention-policy-applicable-privileges-retention-sys"></a>

### Scope and privileges

| Table type | Supported |
|---|---|
| TAG, KV, LOG | Yes |
| TRANSACTION, VOLATILE, LOOKUP | No |

If the policy administrator and table owner are different accounts, validate the actual
privilege configuration before production use. For another owner's table, explicitly grant
only the required privileges.

<a id="execution-status-check-state-retention"></a>
<a id="retention-policy-execution-status-check-state-retention"></a>

### Check job status

```sql
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB
 ORDER BY USER_NAME, TABLE_NAME;
```

`STATE` is the job's current state. `LAST_DELETED_TIME` is the cutoff used by the last deletion
job, not its wall-clock completion time. To verify actual deletion, check both the oldest
timestamp in the target table and the row count trend.
