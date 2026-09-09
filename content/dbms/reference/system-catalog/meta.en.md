---
type: docs
title: '16.3.1 Metadata Table Dictionary'
weight: 10
toc: true
---

Metadata tables use the `M$` prefix and expose Machbase schema information, including table
definitions, columns, indexes, and users. They are read-only and automatically reflect DDL
operations.

In 8.7.0 Standard Edition with multiple databases, joins between catalog-local metadata must use
`DATABASE_ID`, `TABLESPACE_ID`, and the parent object ID together. Logical
`DATABASE_ID` and physical `TABLESPACE_ID` are not interchangeable. For database operation boundaries,
see the [Multiple Database Operations Guide](/dbms/operations-configuration-recovery/multi-database/).


## Metadata Tables

| Table | Description |
|------------|------|
| `M$SYS_TABLES` | User-created tables and their types |
| `M$SYS_TABLE_PROPERTY` | Properties applied to tables |
| `M$SYS_COLUMNS` | Table column definitions (type, length, and other attributes) |
| `M$SYS_INDEXES` | Index definitions |
| `M$SYS_INDEX_COLUMNS` | Columns that make up each index |
| `M$SYS_TABLESPACES` | Tablespaces |
| `M$SYS_TABLESPACE_DISKS` | Disk paths used by tablespaces |
| `M$SYS_USERS` | Registered users |
| `M$SYS_VIEWS` | SQL text defining views |
| `M$SYS_USER_ACCESS` | User privileges per table |
| `M$RETENTION` | Retention policy information |
| `M$TABLES` | The M$ metadata tables themselves |
| `M$COLUMNS` | Columns of M$ metadata tables |

## M$SYS_TABLES

Lists user-created tables and their types.

| Column | Type | Description |
|--------|------|------|
| `NAME` | VARCHAR | Table name |
| `TYPE` | INTEGER | Table type |
| `ID` | LONG | Table identifier |
| `DATABASE_ID` | LONG | Logical database identifier |
| `TABLESPACE_ID` | LONG | Physical tablespace identifier |
| `USER_ID` | INTEGER | Identifier of the user who created the table |
| `COLCOUNT` | INTEGER | Number of columns |
| `FLAG` | INTEGER | Subtype (1: Tag Data, 2: Rollup, 4: Tag Meta, 8: Tag Stat) |

**TYPE values:**

| Value | Table Type |
|----|------------|
| `0` | Log table |
| `1` | Fixed table |
| `3` | Volatile table |
| `4` | Lookup table |
| `5` | Key Value table |
| `6` | Tag table |
| `7` | View |
| `8` | TRANSACTION table |

## M$SYS_COLUMNS

Lists table column definitions.

| Column | Type | Description |
|--------|------|------|
| `NAME` | VARCHAR | Column name |
| `TYPE` | INTEGER | Column data type |
| `TABLE_ID` | LONG | Parent table identifier |
| `DATABASE_ID` | LONG | Logical database identifier |
| `TABLESPACE_ID` | LONG | Physical tablespace identifier |
| `LENGTH` | INTEGER | Maximum column length |
| `PART_PAGE_COUNT` | INTEGER | Pages per partition |
| `MINMAX_CACHE_SIZE` | LONG | MIN-MAX cache size |

## M$SYS_INDEXES

Lists index definitions.

| Column | Type | Description |
|--------|------|------|
| `NAME` | VARCHAR | Index name |
| `TYPE` | INTEGER | Index type |
| `TABLE_ID` | LONG | Parent table identifier |
| `DATABASE_ID` | LONG | Logical database identifier |
| `TABLESPACE_ID` | LONG | Physical tablespace identifier |
| `COLCOUNT` | INTEGER | Number of index columns |
| `MAX_LEVEL` | INTEGER | Maximum LSM level |

## M$SYS_USERS

Lists registered users.

| Column | Type | Description |
|--------|------|------|
| `USER_ID` | INTEGER | User identifier |
| `NAME` | VARCHAR | Username |
| `PWD_POLICY_LEVEL` | INTEGER | Password policy level |
| `VALID_BEFORE` | VARCHAR | Account validity period |

## M$RETENTION

Lists retention policy information.

| Column | Type | Description |
|--------|------|------|
| `POLICY_NAME` | VARCHAR | Policy name |
| `DURATION` | LONG | Retention period in seconds |
| `INTERVAL` | LONG | Deletion interval in seconds |

## SQL Examples

```sql
-- List all tables, including their types
SELECT name, type, colcount
  FROM m$sys_tables
 ORDER BY name;

-- List Tag tables only (type = 6)
SELECT name FROM m$sys_tables WHERE type = 6;

-- List columns of a specific table
SELECT c.name AS col_name, c.type AS col_type, c.length
  FROM m$sys_columns c
  JOIN m$sys_tables  t
    ON c.database_id = t.database_id
   AND c.tablespace_id = t.tablespace_id
   AND c.table_id = t.id
 WHERE t.name = 'SENSOR_TAG'
 ORDER BY c.id;

-- List indexes of a specific table
SELECT i.name AS idx_name, i.type AS idx_type, i.colcount
  FROM m$sys_indexes i
  JOIN m$sys_tables  t
    ON i.database_id = t.database_id
   AND i.tablespace_id = t.tablespace_id
   AND i.table_id = t.id
 WHERE t.name = 'SENSOR_TAG';

-- Check the columns that make up an index
SELECT ic.name AS col_name, ic.index_type
  FROM m$sys_index_columns ic
  JOIN m$sys_indexes i ON ic.index_id = i.id
  JOIN m$sys_tables  t ON i.table_id = t.id
 WHERE t.name = 'SENSOR_TAG';

-- Check tablespace disk paths
SELECT ts.name AS tbs_name, d.path, d.io_thread_count
  FROM m$sys_tablespace_disks d
  JOIN m$sys_tablespaces ts ON d.tablespace_id = ts.id;

-- List users
SELECT user_id, name, pwd_policy_level, valid_before
  FROM m$sys_users;

-- List retention policies
SELECT * FROM m$retention;
```

> Metadata tables are read-only. `INSERT`, `UPDATE`, and `DELETE` return errors. Use DDL such as `CREATE TABLE`, `ALTER TABLE`, and `DROP TABLE` to change schemas.
