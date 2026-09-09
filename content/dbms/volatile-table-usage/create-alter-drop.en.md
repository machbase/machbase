---
type: docs
title: '10.3 Create, Alter, and Drop'
weight: 30
toc: true
---

This section explains how to create and drop VOLATILE tables and how their persistence differs from
other table types.


<a id="original-85-creating-volatile-tables"></a>

## Creating and Managing VOLATILE Tables


Use the following statements to create and drop a VOLATILE table.

### Create

```sql
create volatile table vtable (id1 integer, name varchar(20));
```


### Drop

```sql
drop table vtable;
```

<a id="differences-persistence-ddl"></a>

## Persistence Differences and DDL

Unlike other table types, VOLATILE tables store data only in memory.

### Persistence Comparison

| Item | VOLATILE | LOOKUP | TRANSACTION | TAG | LOG |
|------|----------|--------|-----|-----|-----|
| Storage | Memory | Disk | Disk | Disk | Disk |
| Data retained after server restart | No | Yes | Yes | Yes | Yes |
| Table structure (DDL) retained | Yes | Yes | Yes | Yes | Yes |

### DDL Behavior

Only the data in a VOLATILE table is lost. Its definition is stored persistently, as with other
table types. After a restart, perform an initial load; the table does not need to be recreated.

```sql
-- Create the table definition only once.
CREATE VOLATILE TABLE ch10_ddl (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
```

### Creation Syntax

The basic syntax is `CREATE VOLATILE TABLE table_name (column_definition, ...)`. Designate one
column as `PRIMARY KEY` when key-based updates or deletes are required.

- `PRIMARY KEY` is optional.
- Only one column can be designated as the PRIMARY KEY.

### AUTO_INCREMENT PRIMARY KEY

To have the server generate a numeric PRIMARY KEY, specify `AUTO_INCREMENT` on a single `LONG` or
`INT64` column.

```sql
CREATE VOLATILE TABLE ch10_ddl_seq (
    request_id LONG PRIMARY KEY AUTO_INCREMENT,
    payload    VARCHAR(256)
);

INSERT INTO ch10_ddl_seq(payload) VALUES('refresh');
```

The server generates a value when the primary key column is omitted or set to NULL. A single
`INSERT ... VALUES` statement can also specify a primary key value in the range `0..INT64_MAX`. If
the specified value is at least the next automatic value, the next automatic value advances to
`specified value + 1`. A smaller value does not move it backward.
VOLATILE tables with AUTO_INCREMENT do not support `INSERT ... SELECT` or `ON DUPLICATE KEY UPDATE`.

Because VOLATILE table data is lost on server restart, the next automatic value also restarts at 1.
The table definition remains and does not need to be recreated. For obtaining the inserted ID
through an SDK, see [ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/).

### Adding and Dropping Columns

In Standard Edition, you can add and drop fixed-length numeric ARRAY columns in VOLATILE tables.

```sql
ALTER TABLE ch10_ddl
    ADD COLUMN (thresholds DOUBLE[2] DEFAULT [10.0, 20.0]);

ALTER TABLE ch10_ddl
    DROP COLUMN (thresholds);
```

As with scalar `ADD COLUMN`, VOLATILE does not backfill rows that existed before ALTER with the
DEFAULT value. Even with an ARRAY DEFAULT, the new column is a whole-array NULL in existing rows.
This differs from the backfill rules for LOG, LOOKUP, TRANSACTION, and TAG METADATA.

For supported ARRAY element types, cardinality, and DEFAULT rules, see
[Numeric ARRAY Types](/dbms/reference/sql/types/array/).

### Drop

```sql
DROP TABLE ch10_ddl;
DROP TABLE ch10_ddl_seq;
```

### Considerations

- VOLATILE table DDL is stored in the database and survives server restart.
- Data is not restored automatically after restart. Configure an initial load script, for example by running machsql at startup.
