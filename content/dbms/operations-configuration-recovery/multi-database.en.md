---
type: docs
title: '13.2 Multiple Databases'
weight: 20
toc: true
---

Standard Edition lets you create multiple logical databases in one server to separate objects
and access privileges. This page covers adoption and operations. Use the linked references for
SQL syntax, privileges, SDK options, and backup procedures.

## Scope

- Multiple databases are a Standard Edition feature.
- A logical database does not create a separate server process or resource quota.
- Object names have up to three parts: `object`, `owner.object`, or `database.owner.object`.
- Include the owner when specifying another database.
- Mounted databases provide read-only access to backups, separate from active databases.

## Decisions before adoption

1. Define owners and application users for each database.
2. Define `CONNECT` and minimum object privileges.
3. Check how connection pools initialize and reset the current database.
4. Define backup units, recovery order, and naming rules for mounted databases.
5. Establish monitoring that distinguishes usage and failures by database.

## Quick verification

The following example verifies that two databases are separate, then removes both.

```sql
CREATE DATABASE IF NOT EXISTS manual_multidb_a;
CREATE DATABASE IF NOT EXISTS manual_multidb_b;

USE manual_multidb_a;
CREATE LOG TABLE sensor_event (
    event_time DATETIME,
    message    VARCHAR(100)
);
INSERT INTO sensor_event VALUES (SYSDATE, 'from-a');

USE manual_multidb_b;
CREATE LOG TABLE sensor_event (
    event_time DATETIME,
    message    VARCHAR(100)
);
INSERT INTO sensor_event VALUES (SYSDATE, 'from-b');

SELECT message FROM manual_multidb_a.SYS.sensor_event;
SELECT message FROM manual_multidb_b.SYS.sensor_event;

USE MACHBASEDB;
DROP DATABASE manual_multidb_a CASCADE FORCE;
DROP DATABASE manual_multidb_b CASCADE FORCE;
```

`USE database_name` changes the current connection's database. Do not switch with an active
transaction, open cursor, prepared statement, or Appender. Address objects in another database
as `database.owner.object`.

## Privilege boundaries

Users need both `CONNECT` on the target database and the privileges required for the actual
object operation. For SQL to create or drop databases and manage privileges, see
[Accounts and Privileges](/dbms/security-access-control/privileges/). Do not grant blanket
administrator privileges to production accounts.

## Application connections

<a id="94-python"></a>
<a id="95-nodejs"></a>
<a id="97-net"></a>

SDKs differ in the option name for the initial database and in connection pool initialization
behavior. Check support in each SDK's connection documentation, and verify the following
immediately after borrowing a connection.

```sql
SELECT CURRENT_DATABASE();
```

For language-specific settings, see
[Development and Application Integration](/dbms/development-tools-integration/). For version
requirements, see
[Server and SDK Compatibility](/dbms/reference/support-scope-constraints/compatibility-xma-protocol/).

## Backup and recovery

Before backup, record the active databases to include and their recovery order. You can `USE`
a mounted database, but it is read-only and permits only `SELECT`. For exact commands and
validation steps, use [Backup, Restore, and Mount](../backup-restore-mount/).

## Operations checklist

- Does `CURRENT_DATABASE()` return the expected value after connecting and after pool reuse?
- Do SQL and monitoring distinguish same-named objects in different databases?
- Does each user have only the required database and object privileges?
- Have backup and recovery drills verified every target database?
- Before dropping a database, have you checked open connections, objects, and backup retention requirements?

For exact `CREATE/DROP/USE DATABASE` syntax, see
[DATABASE Syntax](/dbms/reference/sql/syntax/database-syntax/).
