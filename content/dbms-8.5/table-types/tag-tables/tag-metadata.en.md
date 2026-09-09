---
title: 'Tag Metadata'
type: docs
weight: 20
---

## Overview

Tag metadata stores static attributes for each tag. You can keep sensor location, device status, installation information, external identifiers, and JSON document-based properties in metadata.

With the current feature set, you can use the following directly through `TAG METADATA` syntax.

- Metadata-only queries
- Metadata predicate based `UPDATE` and `DELETE`
- Last update time queries for metadata rows
- `JSON` metadata columns
- JSON path queries and JSON path indexes
- Partial updates for JSON documents

You do not need to access any internal metadata table directly.

## Define Metadata Columns

Define metadata columns in the `METADATA (...)` clause of `CREATE TAG TABLE`.

```sql
CREATE TAG TABLE sensors (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    location VARCHAR(100),
    status VARCHAR(20),
    srcip IPV4
);
```

Metadata is stored as one row per tag name.

## Insert Metadata

Use `INSERT INTO ... METADATA` to insert metadata.

```sql
INSERT INTO sensors METADATA VALUES (
    'TEMP_001',
    'Building-A/F1',
    'READY',
    '192.168.0.11'
);
```

You can also specify the column list.

```sql
INSERT INTO sensors METADATA (name, status, srcip, location)
VALUES ('TEMP_002', 'STOP', '192.168.0.12', 'Building-A/F2');
```

Notes:

- In `VALUES (...)`, the order is always `NAME` followed by metadata columns in declaration order.
- Unspecified metadata columns are stored as `NULL`.
- The row identity of tag metadata is always `NAME`.
- When a metadata row is created, `_LAST_UPDATE_TIME` is recorded automatically with the server time.

## Query Metadata

### Query Metadata Only

Use `FROM TAG METADATA` for metadata-only queries.

```sql
SELECT name, location, status, srcip
  FROM sensors METADATA
 ORDER BY name;
```

This returns one row per tag name.

```sql
SELECT *
  FROM sensors METADATA
 ORDER BY name;
```

`SELECT *` and `table_alias.*` return only `NAME` and user-defined metadata columns.

System-managed columns such as `_LAST_UPDATE_TIME` are not included in `SELECT *`. Specify the column name explicitly when you need it.

### Query Last Update Time

TAG metadata provides the system-managed `_LAST_UPDATE_TIME` column, which stores the last changed time of each metadata row.

`_LAST_UPDATE_TIME` is not the last insert time of a tag data row. It is the time when the tag metadata row was created or when its metadata value actually changed.

#### Query Syntax

Specify `_LAST_UPDATE_TIME` explicitly in the select list.

```sql
SELECT name, _last_update_time
  FROM sensors METADATA;
```

You can query it together with user-defined metadata columns or use it in predicates.

```sql
SELECT name, location, status, _last_update_time
  FROM sensors METADATA
 WHERE name = 'TEMP_001';
```

`SELECT *` and `table_alias.*` do not include `_LAST_UPDATE_TIME`.

#### Automatic Recording and Update Rules

When a metadata row is created, `_LAST_UPDATE_TIME` is recorded automatically.

```sql
INSERT INTO sensors METADATA(name, location, status)
VALUES('TEMP_003', 'Building-A/F3', 'READY');
```

When a user-defined metadata value actually changes, `_LAST_UPDATE_TIME` is updated.

```sql
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

An update that does not change the stored value, such as setting the same value again, is treated as a no-op. In that case, `_LAST_UPDATE_TIME` is preserved.

```sql
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

For a table with a JSON metadata column named `info`, removing a missing path is also treated as a no-op if the stored value does not change.

```sql
UPDATE sensors METADATA
   SET info = JSON_REMOVE(info, '$.missing')
 WHERE name = 'TEMP_003';
```

#### Direct Write Restrictions

`_LAST_UPDATE_TIME` is managed by the server. You cannot insert or update it directly.

The following statements are not allowed.

```sql
INSERT INTO sensors METADATA(name, location, status, _last_update_time)
VALUES('TEMP_004', 'Building-A/F4', 'READY', now);
```

```sql
UPDATE sensors METADATA
   SET _last_update_time = now
 WHERE name = 'TEMP_003';
```

You also cannot use `_LAST_UPDATE_TIME` as the TAG name column, a user-defined TAG metadata column, or a target column name for `ALTER TABLE ... METADATA ADD COLUMN`. You cannot drop `_LAST_UPDATE_TIME` with `ALTER TABLE ... METADATA DROP COLUMN` either.

```sql
CREATE TAG TABLE invalid_sensor (
    _last_update_time VARCHAR(128) PRIMARY KEY,
    time              DATETIME BASETIME,
    value             DOUBLE
);
```

```sql
CREATE TAG TABLE invalid_sensor_meta (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    _last_update_time DATETIME
);
```

Names that only share the prefix, such as `_LAST_UPDATE_TIME2`, can be used as normal user-defined columns.

#### Time Predicate Queries and Automatic Index

An index for time predicate queries is provided automatically on `_LAST_UPDATE_TIME`.

```sql
SELECT name, location, _last_update_time
  FROM sensors METADATA
 WHERE _last_update_time >= TO_DATE('2026-06-08 00:00:00')
 ORDER BY _last_update_time;
```

You do not need to create a duplicate user index on the same column.

#### Notes for machloader / tagmetaimport

When importing TAG metadata, input files and form files should include only `NAME` and user-defined metadata columns. Internal columns such as `_ID` and the system-managed `_LAST_UPDATE_TIME` are not input targets.

If the metadata columns are `location` and `status`, use input data like this.

```text
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
```

`_LAST_UPDATE_TIME` is filled automatically by the server during import.

If a user defines a column named `_LAST_UPDATE_TIME` in a normal LOG, LOOKUP, or VOLATILE table, it behaves as a normal user-defined column. The reserved behavior applies only to the TAG metadata system column.

### Query Data with Metadata Filters

Use normal `FROM TAG` when you want time-series rows filtered by metadata conditions.

```sql
SELECT name, status, time, value
  FROM sensors
 WHERE status = 'READY'
 ORDER BY name, time;
```

This query returns data rows, so the same metadata value is repeated for each data row of the tag.

Notes:

- `FROM TAG METADATA` does not allow data columns such as `TIME` or `VALUE`.
- `FROM TAG` is data query mode, and `FROM TAG METADATA` is metadata query mode.
- Internal columns such as `_ID` and `_RID` are not available through `TAG METADATA`.

## Update Metadata

Use `UPDATE TAG METADATA` to update metadata.

```sql
UPDATE sensors METADATA
   SET status = 'DONE',
       srcip = '10.0.0.20'
 WHERE name = 'TEMP_001';
```

You can also update multiple tags with a metadata predicate.

```sql
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```

Notes:

- Only `NAME` and metadata columns can be updated.
- Data columns such as `TIME` and `VALUE` cannot be updated through `UPDATE ... METADATA`.
- Internal columns cannot be updated.
- `_LAST_UPDATE_TIME` is updated only when the stored metadata value actually changes.

## Delete Metadata

Use `DELETE FROM TAG METADATA` to delete metadata.

To delete metadata for a specific tag, specify the tag name predicate in the `WHERE` clause.

```sql
DELETE FROM sensors METADATA
 WHERE name = 'TEMP_002';
```

You can also delete multiple tags with a metadata predicate.

```sql
DELETE FROM sensors METADATA
 WHERE status = 'STOP';
```

If the `WHERE` clause is omitted, all metadata rows in the TAG table are deleted.

```sql
DELETE FROM sensors METADATA;
```

Notes:

- If any matched tag still has data rows, the whole statement fails.
- Metadata for tags that are still in use cannot be deleted.
- Even for a full metadata delete, if any target tag is still in use, the whole statement fails
  without partially deleting metadata rows.

To delete metadata for a tag that is still in use, delete the data rows for that tag first,
then run the metadata delete again.

```sql
DELETE FROM sensors
 WHERE name = 'TEMP_001';

DELETE FROM sensors METADATA;
```

## JSON Metadata Columns

You can define a `JSON` metadata column.

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON
);
```

Example insert:

```sql
INSERT INTO ships METADATA VALUES (
    'SHIP_001',
    'READY',
    '{"name":"alpha","ship":{"status":"READY"}}'
);
```

Notes:

- Do not specify a length for a `JSON` metadata column.
- Invalid JSON text raises an error.
- No automatic index is created for the raw JSON metadata column itself.

## Query JSON Paths

Use the `->` operator to query JSON metadata.

```sql
SELECT name,
       info->'$.name',
       info->'$.ship.status'
  FROM ships METADATA
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name;
```

The same path expression can be used in normal tag queries.

```sql
SELECT name, time, value
  FROM ships
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name, time;
```

### Path Notation Rules

Use full JSONPath syntax for query and mutation paths.

- Simple key: `$.name`
- Nested object key: `$.ship.status`
- Use bracket notation if the key name contains `.` or `-`

```sql
SELECT info->'$[''ship.owner'']'
  FROM ships METADATA;

SELECT info->'$[''ship-owner'']'
  FROM ships METADATA;
```

## JSON Path Indexes

### Define Indexes When Creating the Table

If you frequently query specific JSON paths, define them at table creation time.

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON INDEX('name', 'ship.status')
);
```

Strings inside `INDEX(...)` are interpreted as follows.

- `'name'` becomes `$.name`
- `'ship.status'` becomes `$.ship.status`
- Use full JSONPath directly for special keys or complex paths

```sql
INFO JSON INDEX('$[''ship.owner'']')
```

### Add an Index After Table Creation

You can also add a JSON path index later.

```sql
CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');
```

### Drop an Index

Drop the index by name.

```sql
DROP INDEX idx_ship_owner;
```

For indexes created automatically by `INFO JSON INDEX(...)`, use `SHOW INDEX` to confirm the generated index name.

```sql
SHOW INDEX idx_ship_owner;
```

### Notes on Index Usage

Current JSON path indexes work mainly for string comparisons.

```sql
SELECT name
  FROM ships METADATA
 WHERE info->'$.status' = 'READY';
```

String literal comparison can use the index. Numeric literal comparison may still fall back to a full scan.

Examples:

- `info->'$.num' = '10'` : index can be used
- `info->'$.num' = 10` : full scan may be used

## Partial JSON Updates

You can update part of a JSON metadata document without rewriting the whole document.

### JSON_SET

Stores a SQL scalar value as a JSON scalar.

```sql
UPDATE ships METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';
```

### JSON_SET_JSON

Parses the input string as JSON and stores it as an object or array.

```sql
UPDATE ships METADATA
   SET info = JSON_SET_JSON(info, '$.owner', '{"name":"machbase","team":"db"}')
 WHERE name = 'SHIP_001';
```

### JSON_REMOVE

Removes a member or subtree.

```sql
UPDATE ships METADATA
   SET info = JSON_REMOVE(info, '$.owner.team')
 WHERE name = 'SHIP_001';
```

### Partial Update Rules

- `JSON_SET(..., path, NULL)` stores JSON `null`.
- `JSON_SET_JSON(..., path, NULL)` returns SQL `NULL`.
- If the JSON document argument is `NULL`, the function result is SQL `NULL`.
- If the path is `NULL` or an empty string, the function raises an error.
- `JSON_REMOVE` on a missing path is a no-op.
- `JSON_REMOVE(..., '$')` is not allowed.
- Partial mutation is supported for object paths.
- Array element mutation such as `$.items[0]` is not supported.

## Full Example

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    srcip IPV4,
    info JSON INDEX('name', 'ship.status')
);

INSERT INTO ships METADATA VALUES (
    'SHIP_001',
    'READY',
    '192.168.0.11',
    '{"name":"alpha","ship":{"status":"READY"}}'
);

INSERT INTO ships VALUES ('SHIP_001', '2026-04-01 00:00:00', 10.5);

SELECT name, status, info
  FROM ships METADATA;

SELECT name, time, value
  FROM ships
 WHERE info->'$.ship.status' = 'READY';

CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');

UPDATE ships METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';

DROP INDEX idx_ship_owner;
```

## Summary

- Use `FROM TAG METADATA` for metadata-only queries
- Use `FROM TAG` for time-series data queries
- Use `UPDATE/DELETE ... METADATA` for metadata changes
- Use `INFO JSON` for JSON metadata
- `_LAST_UPDATE_TIME` stores the last changed time of a metadata row and can be queried explicitly
- Use `INFO JSON INDEX(...)` or `CREATE INDEX ... ON TAG METADATA (...)` for JSON path indexes
- Use `JSON_SET`, `JSON_SET_JSON`, and `JSON_REMOVE` for partial JSON updates
- `_LAST_UPDATE_TIME` is managed automatically by the server and behaves the same in standard and cluster environments
