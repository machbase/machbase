---
type: docs
title: '9.7 Operations and Data Lifecycle'
weight: 70
toc: true
---
This section covers LOOKUP backup, recovery, and data persistence.

LOOKUP tables persist reference data on disk. Because values can change during operation, manage
change procedures, backups, recovery, and query visibility together.

Distinguish persistent storage from the data location used by queries. At startup, the server
restores all persisted LOOKUP rows into in-memory tables and builds PRIMARY KEY and secondary
indexes. SQL queries use this memory structure during service.

<a id="lifecycle-lookup-data"></a>

## Data Lifecycle

Manage LOOKUP data through creation, insertion, updates, reference, backup, and recovery.

```
Create table
  └── Insert reference data
        └── Join or reference in TAG/LOG/TRANSACTION queries
              └── UPDATE/DELETE during operation
                    └── Backup / Recovery / Mount
```

Reference data is smaller than source events but directly affects how query results are interpreted.
Establish procedures to record before/after values and the time changes take effect.

<a id="operate-lookup-change"></a>

## Reference-Data Change Procedure

Use the following sequence to change LOOKUP data during operation.

1. Query the rows to change.
2. Check the impact scope.
3. Execute UPDATE or DELETE.
4. Execute `EXEC TABLE_REFRESH(table_name)` if needed.
5. Verify visibility with representative queries.

`TABLE_REFRESH` is not required after every ordinary SQL DML operation. Use it when persistent
LOOKUP content must be reloaded into the runtime memory table. For name resolution, permissions, and
errors, see the
[EXEC Procedure Reference](/dbms/reference/sql/syntax/execute-procedure-syntax/#table-refresh).

The following exercise follows this procedure.

```sql
CREATE LOOKUP TABLE ch9_ops_sensor (
    sensor_id  VARCHAR(32) PRIMARY KEY,
    site       VARCHAR(16),
    status     VARCHAR(16),
    updated_at DATETIME
);

INSERT INTO ch9_ops_sensor VALUES ('TEMP-01', 'SEOUL', 'READY', NOW);
INSERT INTO ch9_ops_sensor VALUES ('TEMP-02', 'SEOUL', 'READY', NOW);
INSERT INTO ch9_ops_sensor VALUES ('TEMP-03', 'BUSAN', 'READY', NOW);

-- Query the rows to change.
SELECT sensor_id, site, status FROM ch9_ops_sensor WHERE sensor_id = 'TEMP-01';

-- Apply the change.
UPDATE ch9_ops_sensor
   SET status = 'INACTIVE', updated_at = NOW
 WHERE sensor_id = 'TEMP-01';

-- Reload the memory table if needed.
EXEC TABLE_REFRESH(ch9_ops_sensor);

-- Verify with a representative query.
SELECT sensor_id, status FROM ch9_ops_sensor ORDER BY sensor_id;
```

Only TEMP-01 becomes `INACTIVE`; the other two rows remain `READY`.

Always check the target count before bulk changes.

```sql
SELECT COUNT(*) FROM ch9_ops_sensor
 WHERE site = 'SEOUL' AND status = 'READY';
```

COUNT is 1 because TEMP-01 has already changed. Counting after the change gives a different target set.

```sql
DROP TABLE ch9_ops_sensor;
```


<a id="recovery-support-scope-backup-lookup"></a>

## Backup and Recovery Support

LOOKUP data is persisted on disk and included in database backups. After restore, rows are
reconstructed as memory tables and indexes. Use
[Backup, Restore, and Mount](/dbms/operations-configuration-recovery/backup-restore-mount/) as the
authoritative reference for common BACKUP/RESTORE/MOUNT commands and Edition scope. Validate
representative keys and JOIN results after recovery.

<a id="lifecycle-lookup-monitoring"></a>

## Operational Checks

- Keep reference-data change history in a separate log or operational procedure.
- Check the target count before bulk UPDATE/DELETE.
- Consider indexes on frequent join columns.
- Check startup time and LOOKUP row/index memory usage at actual data scale.
- Check `LOOKUP_APPEND_UPDATE_ON_DUPKEY` when using Append duplicate-key handling.
- Verify reference results with representative JOIN queries after backup recovery.
