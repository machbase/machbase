---
type: docs
title: 'DML'
weight: 120
toc: true
---

Data Manipulation Language (DML) inserts, updates, and deletes table data.

## DML Support by Table Type

| Statement | LOG | TAG | LOOKUP | VOLATILE | TRANSACTION |
|------|:---:|:---:|:------:|:--------:|:---:|
| INSERT | Yes | Yes | Yes | Yes | Yes |
| INSERT SELECT | Yes | Yes | Yes | Yes | Yes |
| UPDATE | - | Yes (tag/axis predicates or metadata) | Yes (general predicates) | Yes (PK predicates) | Yes |
| DELETE | Yes (retention/all) | Yes (time/name predicates) | Yes (general predicates/all) | Yes (PK predicates) | Yes |
| DELETE WHERE | - | Yes (tag/axis predicates) | Yes (general predicates) | Yes (PK equality) | Yes |
| TRUNCATE | Yes | - | - | - | Yes |

> LOG does not support UPDATE. For mutable data, use LOOKUP, VOLATILE, or TRANSACTION.

---

## INSERT INTO

```sql
insert_stmt ::=
    'INSERT INTO' table_name
    [ 'METADATA' ]
    [ '(' insert_column_list ')' ]
    'VALUES' '(' value_list ')'
    [ 'ON DUPLICATE KEY UPDATE' [ 'SET' set_list ] ]

insert_column_list ::= insert_target ( ',' insert_target )*
insert_target      ::= column_name | array_column_name '[' position ']'
value_list         ::= value ( ',' value )*
set_list           ::= column_name '=' value ( ',' column_name '=' value )*
```

Omitted columns receive NULL. METADATA inserts into TAG metadata columns.

```sql
-- Basic insert
INSERT INTO sensor_log VALUES (1, 'sensor-01', 23.5, 'OK');

-- Insert into specified columns
INSERT INTO sensor_log (name, value) VALUES ('sensor-01', 23.5);

-- Insert TAG metadata
INSERT INTO sensors METADATA (name, location, unit)
VALUES ('sensor-01', 'building-A', 'celsius');
```

### ARRAY element target

Machbase DBMS 8.7.0 permits fixed-length ARRAY positions in an INSERT ... VALUES column list.
Positions start at 0. Unspecified elements are stored as element NULL.

```sql
CREATE LOG TABLE array_input (
    id INTEGER,
    channels INT32[4]
);

INSERT INTO array_input (id, channels[0], channels[3])
VALUES (1, 10, 40);
```

A statement cannot mix a whole-ARRAY target with element targets or specify the same position twice.
Scalar columns and out-of-range positions are invalid element targets. Indexed targets are
unsupported in INSERT ... SELECT and UPDATE SET.

For ARRAY construction, sparse input, and selected Append targets, see
[Numeric ARRAY Types](/dbms/reference/sql/types/array/) and
[Sparse ARRAY and Selected-Column Append APIs](/dbms/development-tools-integration/data-input-load-export/array-append/).

### ON DUPLICATE KEY UPDATE

Updates an existing row when INSERT ... VALUES encounters a duplicate key. It cannot be combined
with INSERT ... SELECT.

| Table type | Duplicate key | Support |
|---|---|---|
| TRANSACTION | PRIMARY KEY, single/composite UNIQUE INDEX | Standard Edition |
| LOOKUP | PRIMARY KEY | Supported |
| VOLATILE | PRIMARY KEY | Supported |
| TAG METADATA | Tag-name PRIMARY KEY | Supported |
| TAG data, LOG | - | Unsupported |

Without SET, INSERT input values update existing non-key columns. With SET, right-hand expressions
use the conflicting existing row. LOOKUP, VOLATILE, and TRANSACTION cannot update the PRIMARY KEY
itself. TAG METADATA tag names and system-managed columns follow
[TAG Metadata](/dbms/tag-table-usage/tag-metadata/) change rules.

```sql
-- On a duplicate key, update only the value column
INSERT INTO devices (device_id, ip, status)
VALUES ('dev-001', '192.168.1.1', 'ONLINE')
ON DUPLICATE KEY UPDATE SET status = 'ONLINE';

-- Without SET, update all columns with insert values
INSERT INTO devices (device_id, ip, status)
VALUES ('dev-001', '192.168.1.2', 'ONLINE')
ON DUPLICATE KEY UPDATE;
```

UPSERT without a duplicate-detection key, key changes, and DBMS-specific expressions such as
VALUES(col)/EXCLUDED.col cause errors. For TRANSACTION UNIQUE conflicts and transactions, see
[TRANSACTION UPSERT](/dbms/rdb-table-usage/insert-on-duplicate-key-update/).

---

## INSERT SELECT

```sql
insert_select_stmt ::=
    'INSERT INTO' table_name
    [ '(' insert_column_list ')' ]
    [ with_clause ]
    select_stmt
```

Inserts SELECT results into a table. Standard Edition allows WITH after the target table and column
list. Leading WITH ... INSERT INTO ... syntax is unsupported.

```sql
-- Copy query results to another table
INSERT INTO sensor_log_copy SELECT * FROM sensor_log;

-- Insert explicit _arrival_time values in chronological order
INSERT INTO sensor_log_copy (_arrival_time, id, name, value)
SELECT _arrival_time, id, name, value FROM sensor_log ORDER BY _arrival_time;

-- Insert CTE results
INSERT INTO sensor_log_copy (id, name, value)
WITH filtered AS (
    SELECT id, name, value
    FROM sensor_log
    WHERE value >= 80
)
SELECT id, name, value FROM filtered;
```

Considerations:
- Omitting _ARRIVAL_TIME automatically uses the INSERT execution time.
- For explicit LOG timestamp copies, insert into an empty target in ascending order, separately from other ingestion. Existing newer timestamps make input out of order even when the source is sorted. The default DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE=1 adjusts inverted timestamps to the previous stored time + 1 ns; 0 rejects them. Explicit input therefore does not unconditionally preserve source timestamps.
- Values exceeding a VARCHAR maximum length are automatically truncated on insertion.
- LOG/TAG ingestion is outside TRANSACTION table ROLLBACK.

---

## UPDATE

```sql
update_stmt ::=
    'UPDATE' table_name [ 'METADATA' ]
    'SET' update_expr_list
    [ 'WHERE' predicate ]

update_expr_list ::= column_name '=' value ( ',' column_name '=' value )*
```

TRANSACTION updates all rows if WHERE is omitted. LOOKUP uses primary key or general predicates;
VOLATILE uses primary key equality. TAG data UPDATE combines a tag selector with a time-axis
predicate.

```sql
-- Update a LOOKUP row
UPDATE devices SET status = 'OFFLINE' WHERE device_id = 'dev-001';

-- Update multiple columns
UPDATE devices SET ip = '10.0.0.1', status = 'ONLINE' WHERE device_id = 'dev-002';

-- Update multiple LOOKUP rows with a general predicate
UPDATE devices SET status = 'OFFLINE' WHERE site = 'SEOUL' AND status = 'READY';

```

### TAG data UPDATE

Update actual TAG time-series data using both tag-selection and BASETIME predicates.

```sql
UPDATE sensors
   SET value = 101,
       status = 1
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

name (PRIMARY KEY), time (BASETIME), and metadata columns cannot be SET targets in data UPDATE.

### UPDATE METADATA (TAG Tables)

Use the separate UPDATE ... METADATA form to modify TAG metadata columns.

```sql
-- Update multiple rows with a metadata predicate
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE status = 'READY';

-- Update by tag name
UPDATE sensors METADATA
   SET location = 'building-B'
 WHERE name = 'sensor-01';
```

---

## DELETE

```sql
-- LOG deletion by time or row count
delete_stmt ::=
    'DELETE FROM' table_name
    [ 'OLDEST' number 'ROWS'
    | 'EXCEPT' number ( 'ROWS' | time_unit )
    | 'BEFORE' datetime_expression ]
    [ 'NO WAIT' ]

time_unit ::= 'YEAR' | 'MONTH' | 'WEEK' | 'DAY' | 'HOUR' | 'MINUTE' | 'SECOND'
```

LOG does not support arbitrary-position deletion; it can delete only a continuous range starting
from the oldest data.

Current LOG BEFORE t deletes rows with _arrival_time <= t. Do not infer exclusive boundaries from
its name; use the same comparison for preliminary queries. EXCEPT n DAY and similar periods use
current server time, not the last ingestion timestamp. User-defined DATETIME values are not the
deletion basis. See actual before/after results in
[LOG Retention Deletion](/dbms/log-table-usage/operations-lifecycle/).

```sql
-- Delete all data
DELETE FROM sensor_log;

-- Delete the oldest N rows
DELETE FROM sensor_log OLDEST 1000 ROWS;

-- Delete all but the latest N rows
DELETE FROM sensor_log EXCEPT 10000 ROWS;

-- Delete all but the latest N days
DELETE FROM sensor_log EXCEPT 7 DAY;

-- Delete through a timestamp, including the boundary
DELETE FROM sensor_log BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');
```

### DELETE WHERE (LOOKUP/VOLATILE Tables)

```sql
delete_where_stmt ::=
    'DELETE FROM' table_name 'WHERE' predicate
```

LOOKUP supports primary key or general predicates. VOLATILE uses primary key equality. LOOKUP also
permits omitting WHERE to delete every row.

```sql
DELETE FROM devices WHERE device_id = 'dev-001';

-- Delete multiple LOOKUP rows with a general predicate
DELETE FROM devices WHERE status = 'EXPIRED' OR site = 'RETIRED';

-- Delete all LOOKUP rows
DELETE FROM devices;
```

### DELETE (TAG Tables)

```sql
-- TAG: delete by name or time predicates
delete_from_tag_where_stmt ::=
    'DELETE FROM' table_name [ 'ROLLUP' ]
    'WHERE' predicate
    -- predicate: tag_name, tag_time, or both combined with AND
```

Time predicates support =, <, <=, and BETWEEN.

```sql
-- Delete by TAG name
DELETE FROM tag WHERE name = 'sensor-01';

-- Delete by TAG name and time
DELETE FROM tag WHERE name = 'sensor-01' AND time < TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- Delete by time only
DELETE FROM tag WHERE time <= TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- Delete ROLLUP data
DELETE FROM tag ROLLUP WHERE name = 'sensor-01';
DELETE FROM tag ROLLUP WHERE time BETWEEN TO_DATE('2024-01-01','YYYY-MM-DD') AND TO_DATE('2024-02-01','YYYY-MM-DD');
```

### DELETE FROM TAG METADATA

```sql
DELETE FROM table_name METADATA [ WHERE predicate ]
```

Deletes TAG metadata rows. Omitting WHERE deletes all metadata. Metadata cannot be deleted for tags
that still have actual data.

```sql
DELETE FROM sensors METADATA WHERE name = 'sensor-01';
DELETE FROM sensors METADATA WHERE status = 'STOP';
DELETE FROM sensors METADATA;  -- Delete all metadata (only tags without actual data)
```

---

<a id="dml-update-delete-affected-rows"></a>

## UPDATE/DELETE Affected Rows

Clients executing UPDATE/DELETE can obtain the statement affected row count. Direct execution and
prepared statements use the same rules.

UPDATE returns the number of rows matching WHERE, not the number whose values actually changed.
Setting the same value still counts a matching row. Where omitting WHERE is supported, every target
row counts as matched.

DELETE returns the number of matching rows actually deleted. Repeating the same DELETE returns 0
after the first execution has removed them.

```sql
CREATE LOOKUP TABLE device_state (
    id INTEGER PRIMARY KEY,
    value INTEGER
);

INSERT INTO device_state VALUES (1, 10);
INSERT INTO device_state VALUES (2, 10);

UPDATE device_state SET value = 20 WHERE id >= 1 AND id <= 2;
-- 2 row(s) updated.

UPDATE device_state SET value = 20 WHERE id >= 1 AND id <= 2;
-- 2 row(s) updated. (Repeated UPDATE with identical values)

UPDATE device_state SET value = 20 WHERE id = 999;
-- No row updated.

DELETE FROM device_state WHERE id = 1;
-- 1 row(s) deleted.

DELETE FROM device_state WHERE id = 1;
-- No row deleted.
```

No row updated. or 0 affected rows means no row matched the predicate, not that assigned values
equaled existing values.

Affected counts within a transaction reflect each statement at execution time. A later ROLLBACK does
not change the meaning of counts already returned.

---

## Related Documentation

- [DDL Syntax Dictionary](../ddl-syntax/) — Table creation and schema changes
- [SELECT Syntax Dictionary](../select-syntax/) — Data queries
- [WITH / CTE Syntax](../cte-syntax/) — INSERT SELECT with CTEs
- [LOOKUP Predicate UPDATE](./lookup-predicate-update-syntax/) — General-predicate updates
- [LOOKUP Predicate DELETE](./lookup-predicate-delete-syntax/) — General-predicate deletion
- [LOAD DATA INFILE](../load-data-infile-syntax/) — Bulk CSV loading
