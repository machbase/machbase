---
type: docs
title: '17.1.1.22 DATABASE'
weight: 220
toc: true
---

Logical database lifecycle and session selection syntax for Machbase 8.7.0 Standard Edition.

## Syntax

```sql
CREATE DATABASE [IF NOT EXISTS] database_name;
ALTER DATABASE database_name READ ONLY;
ALTER DATABASE database_name READ WRITE;
DROP DATABASE [IF EXISTS] database_name [RESTRICT | CASCADE | FORCE | CASCADE FORCE];
USE [DATABASE] database_name;
```

`MACHBASEDB` cannot be dropped. Change to another active database before dropping the current one.
`USE` changes only the current connection and fails during a transaction or for a mounted database.

## Current database and object names

```sql
SELECT CURRENT_DATABASE();
SHOW DATABASES;
SELECT * FROM factory_a.sys.sensor_log;
```

Two-part names mean `owner.object`. Use `database.owner.object` for another database. Access requires
both database connection permission and the required object privilege.

See [Multiple databases](/dbms/operations-configuration-recovery/multi-database/) for operational
guidance and [Backup, restore, and mount](../backup-restore-mount-syntax/) for protected data paths.
