---
type: docs
title: '13.2 Multiple Databases'
weight: 20
toc: true
---

Standard Edition can separate objects and access privileges across multiple logical databases in
one server. This page owns the adoption and operational workflow. Use the linked references for SQL
syntax, privileges, SDK options, and backup procedures.

## Scope

- Multiple databases are a Standard Edition feature.
- A logical database does not create a separate server process or resource quota.
- Object names have up to three parts: `object`, `owner.object`, or `database.owner.object`.
- Include the owner when addressing an object in another database.
- A mounted database is a read-only backup view, not an active logical database.

## Before adoption

1. Define owners and application users for each database.
2. Define `CONNECT` and minimum object privileges.
3. Verify how the connection pool initializes and resets the current database.
4. Define backup units, restore order, and mounted-database naming.
5. Establish monitoring that distinguishes database usage and failures.

## Quick verification

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

`USE database_name` changes the database of the current connection. Do not switch while a
transaction, cursor, prepared statement, or Appender is active.

## Operational ownership

- See [Privileges](../../security-access-control/privileges/) for `CONNECT` and object privileges.
- See [Development and application integration](../../development-tools-integration/) for initial
  database and pool behavior by SDK.
- See [Server and SDK compatibility](../../reference/support-scope-constraints/compatibility-xma-protocol/)
  for version requirements.
- See [Backup, restore, and mount](../backup-restore-mount/) for protected operations.
- See [DATABASE syntax](../../reference/sql/syntax-dictionary-sql/database-syntax/) for exact SQL.

Verify `CURRENT_DATABASE()` immediately after connecting and after borrowing a pooled connection.
