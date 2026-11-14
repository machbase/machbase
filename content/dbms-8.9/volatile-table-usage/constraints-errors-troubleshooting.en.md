---
type: docs
title: '10.8 Constraints, Errors, and Troubleshooting'
weight: 80
toc: true
---

This section covers VOLATILE table limitations, possible errors, and troubleshooting. Most issues
involve memory limits, primary key design, unsupported column types, or data loss after restart.

<a id="limitations-volatile"></a>

## Limitations

Consider the following limitations when using VOLATILE tables.

| Item | Limitation |
|------|------|
| Storage | Memory |
| Data after restart | Lost |
| Backup and mount | Not supported |
| JSON columns | Not supported |
| PRIMARY KEY | Optional; only one column |
| UPDATE/DELETE | Only `PRIMARY KEY = value` predicates are supported |
| Memory limit | Subject to the total memory limit for Volatile/Lookup tables |

```sql
-- Expected failure: VOLATILE tables do not support JSON columns.
CREATE VOLATILE TABLE ch10_err_json (
    session_id VARCHAR(64) PRIMARY KEY,
    payload    JSON
);
```

For flexible attributes, extract frequently queried values into ordinary columns. If persistent JSON
columns are needed, consider TRANSACTION or TAG tables.

<a id="error-volatile-memory"></a>

## Insufficient Memory

VOLATILE table data and indexes consume memory. Increasing row counts or too many indexes can
exhaust the memory limit.

Diagnose the issue in the following order. The example tables are cleaned up at the end of this page.

```sql
-- Create a table for the diagnostic example.
CREATE VOLATILE TABLE ch10_diag (
    device_id VARCHAR(64) PRIMARY KEY,
    value     DOUBLE
);
INSERT INTO ch10_diag VALUES ('DEV-01', 10.0);

-- 1. Check the target table row count.
SELECT COUNT(*) FROM ch10_diag;
```

```sql
-- 2. Check memory usage across VOLATILE tables.
SELECT *
FROM V$STORAGE_DC_VOLATILE_TABLE;
```

If needed, check the `VOLATILE_TABLESPACE_MEMORY_MAX_SIZE` setting.

```sql
SELECT NAME, VALUE
FROM V$PROPERTY
WHERE NAME = 'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE';
```

To resolve the issue:

- Delete unnecessary rows.
- Reduce the amount of data retained in the cache.
- Remove unused indexes.
- Move important data to persistent tables before rebuilding the VOLATILE table.
- Consider adjusting the memory limit according to operational policy.

<a id="error-volatile-primary-key"></a>

## PRIMARY KEY Errors

A PRIMARY KEY is required for `ON DUPLICATE KEY UPDATE`,
[primary key UPDATE](../data-input-mutation/#volatile-primary-key-update), and primary key DELETE.

```sql
CREATE VOLATILE TABLE ch10_err_device (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    updated_at DATETIME
);
```

PRIMARY KEY values must be unique. Use `ON DUPLICATE KEY UPDATE` to treat duplicate inserts as updates.

```sql
INSERT INTO ch10_err_device VALUES ('DEV-01', 'ONLINE', NOW)
ON DUPLICATE KEY UPDATE SET status = 'ONLINE', updated_at = NOW;
```

The PRIMARY KEY column itself cannot be updated. To change a key, delete the existing row and insert
it with the new key.

<a id="error-volatile-restart-loss"></a>

## Data Loss After Restart

VOLATILE table data is lost on normal shutdown, abnormal termination, or restart. This is a
characteristic of the table type, not an error.

When an issue occurs, check the following.

1. Check whether the server has restarted.
2. Check whether the VOLATILE table creation script was executed.
3. Check whether the initial load query completed successfully.
4. Rebuild the cache from the source TAG/LOG/TRANSACTION table.

```sql
SELECT COUNT(*) FROM ch10_diag;
```

If the result is 0, run the initial load procedure again.

Clean up the example tables as follows.

```sql
DROP TABLE ch10_diag;
DROP TABLE ch10_err_device;
```

<a id="troubleshooting-volatile-checklist"></a>

## Troubleshooting Checklist

- Confirm that the stored data can be rebuilt.
- Check whether the operation requires a PRIMARY KEY.
- Use `COUNT(*)` and `V$STORAGE_DC_VOLATILE_TABLE` to check size and memory usage.
- Run the initial load SQL again after restart. The table does not need to be recreated.
- For persistent retention, use TAG, LOG, LOOKUP, or TRANSACTION tables instead of VOLATILE.
