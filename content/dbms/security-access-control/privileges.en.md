---
type: docs
title: '14.3 Privilege Management'
weight: 30
toc: true
---

Machbase separates administrative privileges scoped to active databases from DML privileges
on specific tables. Users need both `CONNECT` on the database and the privileges required
for the target operation.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

<a id="privileges"></a>

## Privilege model

| Scope | Privilege | Purpose |
|---|---|---|
| Active database | `CONNECT` | Connect and `USE` |
| Active database | `CREATE`, `DROP`, `ALTER` | Create, drop, and alter objects |
| Active database | `BACKUP` | Back up the database |
| Active database | `DDL` | Combined `CREATE` and `DROP` |
| Active database | `ALL` | `CONNECT`, `CREATE`, `DROP`, `ALTER`, `BACKUP` |
| Mounted database | `USAGE` | Browse a mounted database |
| Administrative database | `MOUNT` | `MOUNT DATABASE`, `UMOUNT DATABASE` |
| Table | `SELECT`, `INSERT`, `DELETE`, `UPDATE` | DML on a specific table |
| Table | `ALL` | All four table DML privileges |

Database `ALL` does not include table DML or `MOUNT`. Table `ALL` does not include database
administration. A privilege does not enable DML unsupported by the table type; for example,
LOG tables do not support `UPDATE`.

<a id="grant-revoke"></a>

## GRANT / REVOKE

```sql
GRANT privilege_list ON target TO user_name;
REVOKE privilege_list ON target FROM user_name;
```

The following example grants database access and read/write access to one table.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;

REVOKE INSERT ON TABLE factory_a.sys.sensor_log FROM app_user;
REVOKE CONNECT ON DATABASE factory_a FROM app_user;
```

Specify a table as `owner.table` in the current database or as `database.owner.table`.
Database-wide grants of DML privileges such as `SELECT` are not supported.

Inspect current privilege records in `M$SYS_USER_ACCESS`.

```sql
SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 WHERE USER_NAME = 'APP_USER'
 ORDER BY DB_NAME, OWNER_NAME, TABLE_NAME;
```

A record is database-scoped when `OWNER_NAME` and `TABLE_NAME` are `NULL`, and table-scoped
when they have values. `PRIV` is a bitmask representing multiple privileges. Do not interpret
a displayed number as a single privilege name or hardcode it in operational scripts.

<a id="database-privileges"></a>

## Database privileges

Creating a user alone does not grant access to a logical database. Explicitly grant `CONNECT`
on the target database, then add only the required administrative privileges.

```sql
GRANT CONNECT ON DATABASE factory_a TO deploy_user;
GRANT DDL ON DATABASE factory_a TO deploy_user;
GRANT ALTER ON DATABASE factory_a TO deploy_user;
```

Default compatibility privilege records for new users are scoped to the default database,
`MACHBASEDB`. They do not automatically extend to other logical databases.

<a id="select-insert-delete-update"></a>
<a id="database-privileges-select-insert-delete-update"></a>

### SELECT / INSERT / DELETE / UPDATE

Grant DML privileges on specific tables.

```sql
GRANT SELECT ON sys.sensor_log TO reader_user;
GRANT INSERT ON sys.sensor_log TO writer_user;
GRANT DELETE ON sys.device_config TO maint_user;
GRANT UPDATE ON sys.device_config TO maint_user;
```

Before granting `DELETE` or `UPDATE`, check the target table type's predicate restrictions.
TAG data changes require tag and time predicates; VOLATILE changes require primary-key predicates.

<a id="create-drop"></a>
<a id="database-privileges-create-drop"></a>

### CREATE / DROP

```sql
GRANT CREATE ON DATABASE factory_a TO deploy_user;
GRANT DROP ON DATABASE factory_a TO deploy_user;
```

`DROP` permits changes that can be difficult to recover from. Do not grant it to accounts
used only for loading or querying. Object ownership alone does not grant access to another database.

<a id="database-privileges-alter"></a>

### ALTER

```sql
GRANT ALTER ON DATABASE factory_a TO deploy_user;
```

`ALTER` can affect table structures and operational settings. Grant it only to deployment
or operations accounts separate from application accounts. After a change, query the current
settings and schema again.

<a id="database-privileges-backup"></a>

### BACKUP

```sql
GRANT BACKUP ON DATABASE factory_a TO backup_user;
```

The Machbase server process's OS account also needs write access to the backup path and
sufficient free space, separately from SQL privileges. Prefer a backup database user without
additional DML or DDL privileges.

<a id="database-privileges-mount"></a>

### MOUNT

```sql
GRANT MOUNT ON DATABASE MACHBASEDB TO recovery_user;
```

MOUNT/UMOUNT are administrative operations. `USAGE` to browse a mounted database and `SELECT`
to read its tables are separate privileges. Follow
[Backup, Restore, and Mount](/dbms/operations-configuration-recovery/backup-restore-mount/)
for actual recovery procedures.

<a id="privileges-ddl-all"></a>
<a id="database-privileges-privileges-ddl-all"></a>

### Combined DDL / ALL privileges

```sql
-- CREATE + DROP
GRANT DDL ON DATABASE factory_a TO deploy_user;

-- CONNECT, CREATE, DROP, ALTER, and BACKUP on an active database
GRANT ALL ON DATABASE factory_a TO database_admin;

-- SELECT, INSERT, DELETE, and UPDATE on one table
GRANT ALL ON TABLE factory_a.sys.sensor_log TO table_admin;
```

Combined privileges are convenient but can make least-privilege review harder. Grant individual
privileges to automation accounts where possible.

<a id="privileges-grant-exclude"></a>

## Default grants and exclusions

A user created with `CREATE USER` has default compatibility privilege records for `MACHBASEDB`.
For logical databases, explicitly define the required scope as follows.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

Grant `ALTER`, `BACKUP`, `MOUNT`, `USAGE`, and privileges on other logical databases separately
after reviewing the account's role.

<a id="privileges-2"></a>

## Table privileges

Always manage table privileges together with their target objects.

```sql
GRANT SELECT ON TABLE factory_a.sys.sensor_log TO reader_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO ingest_user;

REVOKE INSERT ON TABLE factory_a.sys.sensor_log FROM ingest_user;
```

Dropping a table removes its existing grants. A new object with the same name does not inherit
them. Regrant the required privileges and verify them in `M$SYS_USER_ACCESS`.

<a id="checklist-diagnosis-privileges"></a>

## Privilege diagnostic checklist

Review users and privileges in the following order.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 ORDER BY USER_ID;

SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 ORDER BY USER_NAME, DB_NAME, OWNER_NAME, TABLE_NAME;
```

- Check for unused accounts.
- Ensure read-only accounts have no write, DDL, or administrative privileges.
- `REVOKE` temporary privileges when the approved period ends, then query the results again.
- Before dropping a user, check owned objects and active sessions.
- Validate audit tools that decode numeric `PRIV` values against the privilege definitions for the deployed version.
