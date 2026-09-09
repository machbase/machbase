---
type: docs
title: 'DDL'
weight: 110
toc: true
---

Data Definition Language (DDL) creates, modifies, and drops database objects such as tables,
indexes, views, and ROLLUPs.

> **Privileges**: Ordinary users need `GRANT DDL ON DATABASE database_name TO user_name;` or `GRANT CREATE ON DATABASE database_name TO user_name;` to execute DDL in an active database. See [GRANT/REVOKE](../user-auth-syntax/#grant-revoke).

## CREATE TABLE

```sql
create_table_stmt ::=
    'CREATE' table_type? 'TABLE' ['IF NOT EXISTS'] table_name
    '(' column_def ( ',' column_def )* ')'
    [ 'METADATA' '(' column_def ( ',' column_def )* ')' ]
    [ table_property_list ]
    [ 'TABLESPACE' tablespace_name ]
    [ 'WITH ROLLUP' rollup_interval_spec ]

table_type ::= 'LOG' | 'TAG' | 'VOLATILE' | 'LOOKUP' | 'TRANSACTION' | 'TXN'
-- Omitting table_type creates a TRANSACTION table.

column_def ::= column_name column_type
               [ 'PRIMARY KEY' ]
               [ 'NOT NULL' ]
               [ column_axis ]
               [ 'SUMMARIZED' ]
               [ 'DEFAULT' value ]
               [ 'PROPERTY' '(' column_property_list ')' ]

decimal_type ::= ( 'DECIMAL' | 'NUMERIC' | 'DEC' | 'FIXED' | 'NUMBER' )
                 [ '(' precision [ ',' scale ] ')' ]

array_type ::= ( 'SHORT' | 'INT16' | 'USHORT' | 'UINT16'
               | 'INTEGER' | 'INT' | 'INT32' | 'UINTEGER' | 'UINT32'
               | 'LONG' | 'INT64' | 'ULONG' | 'UINT64'
               | 'FLOAT' | 'DOUBLE' | decimal_type )
             '[' cardinality ']'

column_axis ::= 'BASETIME' | 'BASE TIME' | 'BASE DISTANCE' | 'BASEDISTANCE'

column_property_list ::=
    ( 'MINMAX_CACHE_SIZE' '=' number
    | 'PART_PAGE_COUNT'   '=' number
    | 'PAGE_VALUE_COUNT'  '=' number
    | 'MAX_CACHE_PART_COUNT' '=' number
    | 'SEQUENCE' '=' number )
    ( ',' column_property_list )*

table_property_list ::=
    ( 'TAG_PARTITION_COUNT'           '=' number
    | 'TAG_DATA_PART_SIZE'            '=' number
    | 'TAG_STAT_ENABLE'               '=' ( '0' | '1' )
    | 'TAG_DUPLICATE_CHECK_DURATION'  '=' number
    | 'VARCHAR_FIXED_LENGTH_MAX'      '=' number )
    ( ',' table_property_list )*
```

### Table Types

| Keyword | Description |
|--------|------|
| (omitted) | **TRANSACTION** — Relational data and transactions |
| `LOG` | **LOG** — Time-series logs; append-oriented, no general UPDATE |
| `TAG` | **TAG** — Name/time/value time series; BASETIME required |
| `LOOKUP` | **LOOKUP** — Memory-resident; PRIMARY KEY required; full DML support |
| `VOLATILE` | **VOLATILE** — Memory-resident; data lost on restart; optional PRIMARY KEY |
| `TRANSACTION`, `TXN` | **TRANSACTION** — Full and abbreviated names create the same type |

CREATE TABLE without a type, CREATE TRANSACTION TABLE, and CREATE TXN TABLE all create TRANSACTION
tables. Use CREATE LOG TABLE for LOG. Previous public names RDB and TRX are unsupported as
table-type aliases. TRANSACTION is Standard Edition only; Cluster rejects all three creation forms.

DECIMAL is available for every table type. Precision is 1–65, scale is 0–30, and scale cannot exceed
precision. See
[DECIMAL and NUMERIC Fixed-Point Types](/dbms/reference/sql/types/decimal-numeric-fixed-point/).

Machbase DBMS 8.7.0 ARRAY specifies a cardinality from 1..1024 after a numeric element type. For
supported types and table-specific restrictions, see
[Numeric ARRAY Types](/dbms/reference/sql/types/array/).

### Examples

```sql
-- Create a LOG table with the explicit LOG keyword.
CREATE LOG TABLE sensor_log (
    id      INTEGER,
    name    VARCHAR(64),
    value   DOUBLE,
    status  VARCHAR(20)
);

-- Create a TAG table: BASETIME required; SUMMARIZED marks the ROLLUP column.
CREATE TAG TABLE tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- TAG table with metadata and properties
CREATE TAG TABLE sensors (
    name     VARCHAR(40) PRIMARY KEY,
    time     DATETIME BASETIME,
    value    DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(100),
    unit     VARCHAR(20)
) TAG_PARTITION_COUNT = 4;

-- LOOKUP table (PRIMARY KEY required)
CREATE LOOKUP TABLE devices (
    device_id  VARCHAR(40) PRIMARY KEY,
    ip         IPV4,
    status     VARCHAR(20)
);

-- VOLATILE table
CREATE VOLATILE TABLE cache_data (
    id    INTEGER PRIMARY KEY,
    value DOUBLE
);

-- Exact fixed-point columns in a TRANSACTION table
CREATE TRANSACTION TABLE invoice (
    id      LONG PRIMARY KEY,
    amount  DECIMAL(18,2),
    tax     NUMERIC(18,4)
);

-- Use IF NOT EXISTS
CREATE TAG TABLE IF NOT EXISTS tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- NOT NULL constraint
CREATE TABLE t1 (
    c1 INTEGER NOT NULL,
    c2 VARCHAR(200)
);
```

### Predefined System Columns

The following system columns are provided.

| Column | Type | Description |
|------|------|------|
| `_ARRIVAL_TIME` | DATETIME | LOG only; row insertion time and basis for DURATION queries |
| `_RID` | LONG | LOG and internal TAG data tables; unique row identifier that users cannot assign directly |

---

## DROP TABLE

```sql
drop_table_stmt ::= 'DROP TABLE' table_name
```

Drops the specified table and all its data and indexes. Returns an error if another session is
querying the table.

```sql
DROP TABLE sensor_log;
```

---

## ALTER TABLE

ALTER TABLE changes a table schema. Available subclauses depend on table type. TRANSACTION supports
ADD COLUMN, DROP COLUMN, RENAME COLUMN, and RENAME TO. Use METADATA ADD COLUMN and METADATA DROP
COLUMN for TAG metadata columns.

### ADD COLUMN

```sql
alter_table_add_stmt ::=
    'ALTER TABLE' table_name [ 'METADATA' ] 'ADD COLUMN'
    '(' column_name column_type [ 'DEFAULT' value ] ')'
```

```sql
-- Add a column
ALTER TABLE sensor_log ADD COLUMN (quality FLOAT);

-- Add a TRANSACTION column
ALTER TABLE product_master ADD COLUMN (stock_qty INTEGER DEFAULT 0);

-- Add columns with defaults
ALTER TABLE sensor_log ADD COLUMN (flag INTEGER DEFAULT 0);
ALTER TABLE sensor_log ADD COLUMN (tag_ip IPV4 DEFAULT '192.168.0.1');

-- Add an ARRAY column with DEFAULT
ALTER TABLE sensor_log
    ADD COLUMN (channels INT32[3] DEFAULT [1, NULL, 3]);

-- Add a TAG METADATA ARRAY column
ALTER TABLE sensor_tag METADATA
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);
```

Omitting scale in DECIMAL(p)[n] ARRAY means scale 0. ARRAY DEFAULT must contain exactly the declared
number of elements. Invalid element types, cardinality, precision, scale, nested/multidimensional
declarations, or a DEFAULT of the wrong length fail the entire statement without partially creating
columns.

#### ARRAY ADD COLUMN Support

| Edition | Table or column area | Supported | Explicit DEFAULT for existing rows |
|---|---|:---:|---|
| Standard | LOG | Yes | Applied |
| Standard | VOLATILE | Yes | Not applied; whole-array NULL retained |
| Standard | LOOKUP | Yes | Applied |
| Standard | TRANSACTION | Yes | Applied |
| Standard | TAG METADATA | Yes | Applied |
| Standard | Ordinary TAG DATA columns | No | - |
| Cluster | LOG | Yes | Applied |
| Cluster | Other tables or TAG METADATA | No | - |

Without DEFAULT, the new ARRAY column is a whole-array NULL in pre-ALTER rows for every supported
table. Ordinary TAG DATA ARRAY columns can be declared in CREATE TABLE but cannot be added with
ALTER. For types and NULL semantics, see [Numeric ARRAY Types](/dbms/reference/sql/types/array/).

### DROP COLUMN

```sql
alter_table_drop_stmt ::=
    'ALTER TABLE' table_name [ 'METADATA' ]
    'DROP COLUMN' '(' column_name ')'
```

```sql
ALTER TABLE sensor_log DROP COLUMN (quality);
ALTER TABLE product_master DROP COLUMN (stock_qty);
ALTER TABLE sensor_log DROP COLUMN (channels);
ALTER TABLE sensor_tag METADATA DROP COLUMN (limits);
```

### RENAME COLUMN

```sql
alter_table_column_rename_stmt ::=
    'ALTER TABLE' table_name 'RENAME COLUMN' old_column_name 'TO' new_column_name
```

```sql
ALTER TABLE sensor_log RENAME COLUMN status TO device_status;
ALTER TABLE product_master RENAME COLUMN name TO product_name;
```

### MODIFY COLUMN

```sql
alter_table_modify_stmt ::=
    'ALTER TABLE' table_name 'MODIFY COLUMN'
    ( '(' column_name 'VARCHAR' '(' new_size ')' ')'
    | column_name ( 'NOT NULL' [ 'NOCHECK' ] | 'NULL'
                  | 'SET' 'MINMAX_CACHE_SIZE' '=' value ) )
```

The length-extension and MINMAX examples below target LOG. Existing VARCHAR length can be increased,
but not decreased, and other types cannot be converted to VARCHAR. The new LOG length cannot exceed
32,767 bytes. MINMAX_CACHE_SIZE applies to supported fixed-length LOG columns, not variable-length
columns such as VARCHAR/TEXT.

In LOG, NOT NULL without an option checks existing rows. NOCHECK only skips that check; it does not
fill existing NULL values. NULL removes the constraint. Do not apply this entire scope to TAG; check
[TAG Column Changes](/dbms/tag-table-usage/create-alter-drop/). TRANSACTION does not support MODIFY
COLUMN.

```sql
-- Increase VARCHAR length (decreasing is unsupported)
ALTER TABLE sensor_log MODIFY COLUMN (name VARCHAR(128));

-- Add NOT NULL
ALTER TABLE sensor_log MODIFY COLUMN id NOT NULL;

-- Remove NOT NULL
ALTER TABLE sensor_log MODIFY COLUMN id NULL;

-- Change MINMAX_CACHE_SIZE
ALTER TABLE sensor_log MODIFY COLUMN id SET MINMAX_CACHE_SIZE = 10240;
```

### RENAME TO

```sql
alter_table_rename_stmt ::=
    'ALTER TABLE' table_name 'RENAME TO' new_name
```

```sql
-- Supported for TRANSACTION tables
ALTER TABLE product_master RENAME TO product_catalog;
```

### ADD / DROP RETENTION

For retention assignment/detachment, see [RETENTION Syntax](../retention-syntax/).

---

## TRUNCATE TABLE

```sql
truncate_table_stmt ::= 'TRUNCATE TABLE' table_name
```

Deletes all table data. Returns an error if another session is querying the table.

```sql
TRUNCATE TABLE sensor_log;
```

---

## CREATE INDEX

For index types, table support, JSON paths, and properties, see [INDEX Syntax](../index-syntax/).

---

## DROP INDEX

For drop syntax and restrictions, see [INDEX Syntax](../index-syntax/#drop-index).

---

## CREATE TABLESPACE

```sql
create_tablespace_stmt ::=
    'CREATE TABLESPACE' tablespace_name 'DATADISK' datadisk_list

datadisk_list ::= data_disk ( ',' data_disk )*

data_disk ::= disk_name
    '(' 'DISK_PATH' '=' '"' path '"'
        [ ',' 'PARALLEL_IO' '=' number ]
    ')'
```

```sql
-- Single-disk tablespace
CREATE TABLESPACE tbs1 DATADISK disk1 (DISK_PATH="tbs1_disk1");

-- Configure parallel I/O
CREATE TABLESPACE tbs2 DATADISK disk1 (DISK_PATH="tbs2_disk1", PARALLEL_IO = 5);

-- Multiple disks
CREATE TABLESPACE tbs3
  DATADISK disk1 (DISK_PATH="tbs3_d1", PARALLEL_IO = 10),
           disk2 (DISK_PATH="tbs3_d2"),
           disk3 (DISK_PATH="tbs3_d3");
```

---

## DROP TABLESPACE

```sql
drop_tablespace_stmt ::= 'DROP TABLESPACE' tablespace_name
```

```sql
DROP TABLESPACE tbs1;
```

A tablespace cannot be dropped while it contains objects.

---

## CREATE ROLLUP

For basic, conditional, and Custom ROLLUP syntax, see [ROLLUP Syntax](../rollup-syntax/).

---

## DROP ROLLUP

For deletion syntax, see [ROLLUP Syntax](../rollup-syntax/#drop-rollup).

---

## ALTER ROLLUP

For start, stop, force, and interval changes, see [ROLLUP Syntax](../rollup-syntax/#alter-rollup).

---

## CREATE RETENTION

For creation and table assignment, see [RETENTION Syntax](../retention-syntax/).

---

## DROP RETENTION

For deletion syntax and detachment order, see [RETENTION Syntax](../retention-syntax/#drop-retention).

---

## DDL Concurrency and Locks {#ddl-concurrency}

Machbase 8.7.0 Standard Edition coordinates DDL at object level for independent objects. DDL
creating or changing differently named LOG, TAG, VOLATILE, LOOKUP, and TRANSACTION tables in the
same database can therefore proceed concurrently.

| Edition | DDL on independent objects | Conflict scope | Conflict wait setting |
|---------|-----------------|-----------|-------------------|
| Standard | Can proceed concurrently | Same object and directly related objects | DDL_LOCK_TIMEOUT |
| Cluster | Serialized under existing policy | Catalog scope | DDL_LOCK_TIMEOUT unavailable |

Even concurrently started DDL on independent objects can share work such as metadata processing and
storage I/O. Throughput scaling with client count and simultaneous completion of all DDL are not
guaranteed.

### Conflicting Objects

| Concurrent operations | Behavior |
|----------------|------|
| Independent tables with different names | Can proceed concurrently regardless of table type |
| Same object or same object name | One DDL proceeds; the other waits or errors |
| Table alter/drop and its index DDL | Treated as related objects |
| View DDL and alter/drop of its referenced table | Treated as related objects |
| TAG alter/drop and its ROLLUP/RETENTION DDL | Treated as related objects |
| DROP VIEW, CREATE OR REPLACE VIEW, system-wide DDL | Can serialize at broader scope |

Table names share one namespace across table types. Concurrent LOG and TAG creation with the same
name creates only one of them.

### DDL Lock Wait Time

In Standard Edition, DDL_LOCK_TIMEOUT sets the wait for conflicting DDL locks in seconds.

| Value | Behavior |
|---:|------|
| 0 | Immediately return `ERR-02031: Resource busy (<object>)` without waiting |
| Positive | Wait up to the specified time; return ERR-02031 if the lock is not acquired |

The parentheses in the error identify a representative conflicting object. Broad-scope conflicts can
show DDL instead of an object name.

The default is 0 and the range is 0–1000000. Change the current session value as follows.

```sql
ALTER SESSION SET DDL_LOCK_TIMEOUT = 10;
```

Wait time does not restart at each lock stage of one DDL statement. After locking, objects and
dependencies are checked again, so preceding DDL can cause ordinary errors such as already exists or
table not found.

DDL_LOCK_TIMEOUT limits only lock waits, not total SQL execution time. Running DDL keeps its startup
value; ALTER SESSION changes apply from the next DDL. DDL commit/recovery behavior remains the same
as earlier versions; no new implicit commits are introduced.

| Setting | Unit | Limit target |
|------|------|-----------|
| DDL_LOCK_TIMEOUT | Seconds | Standard Edition DDL lock waits |
| SESSION_QUERY_TIMEOUT_SEC / QUERY_TIMEOUT | Seconds | Query execution and response waits |
| TRANSACTION_BUSY_TIMEOUT_MS | Milliseconds | Concurrent TRANSACTION write conflicts |

---

## Related Documentation

- [Table Types](/dbms/data-modeling-table-design/) — Characteristics and usage of LOG, TAG, LOOKUP, VOLATILE, and TRANSACTION
- [TAG Table ROLLUP](/dbms/tag-table-usage/create-alter-drop/#original-85-creating-tag-tables) — ROLLUP creation and operation
- [GRANT/REVOKE](../user-auth-syntax/#grant-revoke) — DDL privileges
- [ALTER SESSION](../system-session-alter-syntax/#alter-session) — Current-session DDL lock wait settings
- [Schema Change Checklist](/dbms/operations-configuration-recovery/checklist-schema-alter/) — Operational DDL and conflict handling
