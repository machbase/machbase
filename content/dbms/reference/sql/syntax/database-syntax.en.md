---
type: docs
title: 'DATABASE'
weight: 220
toc: true
---

This reference covers logical database lifecycle and session-selection syntax in Machbase 8.7.0
Standard Edition. Database names identify catalogs, distinct from `machadmin -c` and `machadmin -d`,
which manage physical server-instance storage.

## CREATE DATABASE

```sql
create_database_stmt ::=
    'CREATE DATABASE' ['IF NOT EXISTS'] database_name
```

CREATE DATABASE creates an active logical database in the current Machbase instance. The default
access mode is READ WRITE. Users and authentication information are shared instance-wide; tables,
views, indexes, and object privileges are managed per database.

```sql
CREATE DATABASE factory_a;
CREATE DATABASE IF NOT EXISTS factory_b;
```

## ALTER DATABASE

```sql
alter_database_stmt ::=
    'ALTER DATABASE' database_name ( 'READ ONLY' | 'READ WRITE' )
```

READ ONLY databases permit queries but reject write DML, Append, and modifying DDL. Finish active
writes before changing the mode.

```sql
ALTER DATABASE factory_a READ ONLY;
ALTER DATABASE factory_a READ WRITE;
```

## DROP DATABASE

```sql
drop_database_stmt ::=
    'DROP DATABASE' ['IF EXISTS'] database_name
    [ 'RESTRICT' | 'CASCADE' | 'FORCE' | 'CASCADE FORCE' | 'FORCE CASCADE' ]
```

- RESTRICT refuses deletion when objects or active references exist.
- CASCADE removes the target database objects, metadata, and database-local grants.
- FORCE clears terminable session, statement, cursor, and job references before deletion.
- Use CASCADE FORCE to clear both objects and references.

The default MACHBASEDB database cannot be dropped. The current session database cannot be dropped
either; first execute USE MACHBASEDB or switch to another active database.

## USE

```sql
use_database_stmt ::= 'USE' ['DATABASE'] database_name
```

USE and USE DATABASE are equivalent. They change only the current session database and do not affect
other connections. They fail during an active transaction or when the target is a mounted database.

```sql
USE factory_a;
USE DATABASE factory_b;
```

## Checking the Current Database

```sql
SELECT CURRENT_DATABASE();
SELECT DATABASE();
SELECT CURRENT_CATALOG;
SHOW CURRENT DATABASE;
SHOW DATABASES;
```

CURRENT_DATABASE() is the recommended check. Even if client connection options specify an initial
database, query it immediately after connection to verify the actual server catalog.

## Object Names

Tables, views, and DML targets accept these forms.

```text
table_name                         -- Current database, current user
owner.table_name                   -- Current database, specified owner
database_name.owner.table_name    -- Specified database, specified owner
```

Two-part names always mean owner.table. Thus factory_a.sensor_log is not interpreted as
database.table. To explicitly reference another database, use three parts, such as
factory_a.sys.sensor_log.

```sql
SELECT * FROM factory_a.sys.sensor_log;
INSERT INTO factory_b.app.orders VALUES (1, 'ready');
```

Direct cross-database access requires both CONNECT on the target database and the necessary DML
privileges on the target table. Index names, LOAD DATA targets, and other statements follow their
own qualifier restrictions.

## Privilege Syntax and Database Scope

Database and table privileges are separate. The basic forms are:

```sql
GRANT CONNECT ON DATABASE factory_a TO app_a;
GRANT CREATE, ALTER ON DATABASE factory_a TO deployer;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_a;
REVOKE CONNECT ON DATABASE factory_a FROM app_a;
```

Querying a mounted database requires both USAGE on that database and SELECT on the table. For
operational MOUNT DATABASE/UMOUNT DATABASE privileges, see
[USER/AUTH Syntax](../user-auth-syntax/#grant-revoke) and
[Multidatabase Operations](/dbms/operations-configuration-recovery/multi-database/).

## Relationship to BACKUP/RESTORE

Logical database backup/restore syntax is covered in
[BACKUP / RESTORE / MOUNT](../backup-restore-mount-syntax/). Only a named backup of one active
catalog can be input to logical MOUNT or RESTORE. A full-instance image containing multiple active
databases cannot be mounted/restored as a logical catalog.
