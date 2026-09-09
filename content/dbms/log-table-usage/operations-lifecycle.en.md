---
type: docs
title: '7.7 Operations and Data Lifecycle'
weight: 70
toc: true
---

If ingestion works but disk usage keeps growing, check the deletion criteria. LOG removes older data
regions rather than selecting individual rows by business predicates. Check both the retention
period and the actual deletion boundary.

<a id="original-85-deleting-data"></a>
<a id="delete-log-syntax"></a>

<a id="지우려는-목적에-맞게-명령을-고릅니다"></a>

## Choosing a Deletion Method

| Goal | Command | Basis |
|---|---|---|
| Delete the oldest N rows | OLDEST n ROWS | Oldest ingested rows first |
| Keep only the latest N rows | EXCEPT n ROWS | Number of rows to retain |
| Keep only a recent period | EXCEPT n DAY, etc. | Current server time minus the period |
| Delete through a fixed timestamp | BEFORE datetime_expr | Includes the specified _arrival_time boundary |
| Delete all data | DELETE without a predicate, or TRUNCATE | All rows |
| Manage retention periodically | Retention Policy | Retention period and execution interval |

Caution: do not assume deletion can be undone. LOG data is outside TRANSACTION table ROLLBACK. In
production, verify backups and the actual target range before executing deletion.

<a id="delete-log-examples"></a>

<a id="같은-원본으로-세-가지-삭제를-비교합니다"></a>

## Comparing Deletion Methods

When commands run sequentially, earlier deletions affect later results. Here, copy the same three
rows into separate tables for comparison.

```sql
CREATE LOG TABLE ch7_lifecycle (event_id INTEGER);
CREATE LOG TABLE ch7_oldest (event_id INTEGER);
CREATE LOG TABLE ch7_keep (event_id INTEGER);
CREATE LOG TABLE ch7_before (event_id INTEGER);

INSERT INTO ch7_lifecycle(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-01', 'YYYY-MM-DD'), 1);
INSERT INTO ch7_lifecycle(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-02', 'YYYY-MM-DD'), 2);
INSERT INTO ch7_lifecycle(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-03', 'YYYY-MM-DD'), 3);

INSERT INTO ch7_oldest(_arrival_time, event_id)
SELECT _arrival_time, event_id FROM ch7_lifecycle ORDER BY _arrival_time;
INSERT INTO ch7_keep(_arrival_time, event_id)
SELECT _arrival_time, event_id FROM ch7_lifecycle ORDER BY _arrival_time;
INSERT INTO ch7_before(_arrival_time, event_id)
SELECT _arrival_time, event_id FROM ch7_lifecycle ORDER BY _arrival_time;

SELECT COUNT(*) AS delete_candidates FROM ch7_before
 WHERE _arrival_time <= TO_DATE('2026-01-02', 'YYYY-MM-DD');

DELETE FROM ch7_oldest OLDEST 1 ROWS;
DELETE FROM ch7_keep EXCEPT 1 ROWS;
DELETE FROM ch7_before BEFORE TO_DATE('2026-01-02', 'YYYY-MM-DD');

SELECT event_id FROM ch7_oldest ORDER BY event_id;
SELECT event_id FROM ch7_keep ORDER BY event_id;
SELECT event_id FROM ch7_before ORDER BY event_id;
```

The pre-deletion count is 2. The following events remain in each table.

| Table | Remaining event_id values |
|---|---|
| ch7_oldest | 2, 3 |
| ch7_keep | 3 |
| ch7_before | 3 |

The name BEFORE can be misleading. Current LOG deletion includes rows equal to the specified
timestamp. A preliminary count with `WHERE _arrival_time < boundary` can therefore differ from the
deletion target. Use `<=` as shown.

```sql
DELETE FROM ch7_lifecycle;
SELECT COUNT(*) AS remaining_rows FROM ch7_lifecycle;

DROP TABLE ch7_before;
DROP TABLE ch7_keep;
DROP TABLE ch7_oldest;
DROP TABLE ch7_lifecycle;
```

After DELETE without a predicate, the count is 0 and the table definition remains.

<a id="상대-기간-삭제는-현재-시각을-기준으로-합니다"></a>

## Deletion by Relative Period

```sql
CREATE LOG TABLE ch7_period (event_id INTEGER);
INSERT INTO ch7_period(_arrival_time, event_id) VALUES (SYSDATE - 2d, 1);
INSERT INTO ch7_period(_arrival_time, event_id) VALUES (SYSDATE, 2);

DELETE FROM ch7_period EXCEPT 1 DAY;
SELECT event_id FROM ch7_period ORDER BY event_id;

DROP TABLE ch7_period;
```

If the steps from creation through querying run immediately, only row 2 remains. The reference is
the current server time, not the timestamp of the last ingested row. Account for time continuing to
pass even when ingestion stops.

<a id="retention-log-policy"></a>

<a id="반복-삭제는-retention-policy로-관리합니다"></a>

## Retention Policy

The following validation example retains one day of data and runs every minute. These are not
production recommendations. Use an account authorized to create policies and assign them to tables.

```sql
CREATE LOG TABLE ch7_retention (event_id INTEGER);
INSERT INTO ch7_retention(_arrival_time, event_id) VALUES (SYSDATE - 2d, 1);
INSERT INTO ch7_retention(_arrival_time, event_id) VALUES (SYSDATE, 2);

CREATE RETENTION ch7_policy DURATION 1 DAY INTERVAL 1 MIN;
ALTER TABLE ch7_retention ADD RETENTION ch7_policy;

SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'CH7_POLICY';
SELECT TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB WHERE TABLE_NAME = 'CH7_RETENTION';
SELECT event_id FROM ch7_retention ORDER BY event_id;
```

DURATION is the period to retain; INTERVAL is how often deletion runs. Both rows may be visible
immediately after assignment. After one interval plus processing time, rerun the query below and
verify that only row 2 remains. LAST_DELETED_TIME is the deletion cutoff, not the wall-clock
completion time.

```sql
SELECT TABLE_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB WHERE TABLE_NAME = 'CH7_RETENTION';
SELECT event_id FROM ch7_retention ORDER BY event_id;
```

After the exercise, detach the policy before dropping the policy and table.

```sql
ALTER TABLE ch7_retention DROP RETENTION;
SELECT TABLE_NAME FROM V$RETENTION_JOB WHERE TABLE_NAME = 'CH7_RETENTION';
DROP RETENTION ch7_policy;
DROP TABLE ch7_retention;
```

After detachment, the job query returns 0 rows. Previously deleted rows are not restored. One policy
can be assigned to a table, and a policy in use must be detached before it can be dropped. For full
operational guidance, see
[Data Retention Policies](/dbms/operations-configuration-recovery/policy-data-retention/).

<a id="lifecycle-log-backup"></a>

<a id="삭제-전에-조회-가능한-백업인지-확인합니다"></a>

## Verifying Backups Before Deletion

Having a backup file alone does not establish recoverability. Query the period to be deleted through
Mount or in an isolated Restore environment. Define retention periods separately for source data,
backups, and independently aggregated data. For environment-specific commands, see
[Backup, Restore, and Mount](/dbms/operations-configuration-recovery/backup-restore-mount/).

<a id="lifecycle-log-monitoring"></a>

<a id="조회-건수와-디스크-공간은-별도로-봅니다"></a>

## Data and Disk Space

Rows may disappear from queries before the operating system reclaims file space. Check ingestion
volume, the oldest remaining timestamp, index/storage cleanup state, and disk usage together. Do not
delete a wider period simply because disk usage does not decrease immediately.

If deletion results differ from expectations, first check the cutoff timestamp and assigned policy.
For data subject to retention obligations, stop further deletion and agree on the scope with the
responsible owner.
