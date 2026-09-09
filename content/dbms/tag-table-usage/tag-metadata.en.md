---
type: docs
title: '5.10 TAG Metadata'
weight: 100
toc: true
---


<a id="original-85-tag-metadata"></a>

## Tag Metadata


### Overview

METADATA stores one row of current attributes per tag. Ordinary TAG queries repeat
those attributes with each DATA row. Changing a current attribute may also change
what historical DATA queries display. Preserve event-time attributes in DATA or a
separate attribute history when required.

The basic, JSON, and complete examples below use separate tables. Use metadata for
static tag attributes such as sensor location, equipment status, installation
details, external identifiers, and JSON documents.

Metadata-specific SQL supports the following operations. `TAG` in these examples
is a table name; replace it with your actual TAG table name.

- Query metadata only
- `UPDATE` / `DELETE` using metadata predicates
- Query the last modification time of a metadata row
- ADD/DROP ARRAY metadata columns and set DEFAULT for existing rows
- Declare `JSON` metadata columns
- Query and index JSON paths
- Update part of a JSON document

Use `TAG METADATA` syntax without accessing internal storage tables directly.

### Define Metadata Columns

Define metadata columns in the `METADATA (...)` clause of `CREATE TAG TABLE`.

```sql
CREATE TAG TABLE ch5_meta (
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

Metadata stores only one row per tag name.

### Add and Drop ARRAY Metadata Columns

Standard Edition can add and drop fixed-length numeric ARRAY columns in the METADATA
area of an existing TAG table.

```sql
INSERT INTO ch5_meta (name, time, value)
VALUES ('TEMP_OLD', TO_DATE('2026-09-05 00:00:00'), 10.0);

ALTER TABLE ch5_meta METADATA
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

INSERT INTO ch5_meta (name, time, value)
VALUES ('TEMP_NEW', TO_DATE('2026-09-05 00:00:01'), 20.0);

SELECT name, limits
  FROM ch5_meta METADATA
 ORDER BY name;
```

The existing `TEMP_OLD` metadata row is backfilled with `[0.0000, NULL]`. The
`TEMP_NEW` row automatically registered by TAG DATA input after ALTER does not
reapply the ADD COLUMN DEFAULT; `limits` is whole NULL. Without a DEFAULT,
pre-ALTER rows also receive whole NULL.

Added ARRAY metadata columns appear in explicit projections and `SELECT *` in
ordinary TAG queries. ARRAY metadata columns have no automatic indexes and do
not support explicit indexes such as:

```sql
-- Unsupported; raises an error.
CREATE INDEX idx_sensor_limits ON ch5_meta METADATA(limits);
```

Specify `METADATA` when dropping a column as well.

```sql
ALTER TABLE ch5_meta METADATA DROP COLUMN (limits);
```

Ordinary ARRAY columns in TAG DATA can be declared in `CREATE TAG TABLE`, but
cannot be added with ALTER. See [Numeric ARRAY Types](/dbms/reference/sql/types/array/)
for element types, cardinality, and DEFAULT rules.

### Insert Metadata

Use `INSERT INTO ... METADATA` to insert metadata.

```sql
INSERT INTO ch5_meta METADATA VALUES (
    'TEMP_001',
    'Building-A/F1',
    'READY',
    '192.168.0.11'
);
```

You can also specify a column list.

```sql
INSERT INTO ch5_meta METADATA (name, status, srcip, location)
VALUES ('TEMP_002', 'STOP', '192.168.0.12', 'Building-A/F2');
```

Notes:

- Without a column list, VALUES follow the tag name and metadata declaration order.
- With a column list, values follow that list.
- NULL/DEFAULT handling for omitted input follows the DDL and input-path rules.
- The identifier is the TAG name column, declared as `name` in this example.
- Creating a metadata row automatically records server time in `_LAST_UPDATE_TIME`.

<a id="metadata-query-tag"></a>

### Query Metadata

#### Query Metadata Only

Use `FROM TAG METADATA` for metadata-only queries.

```sql
SELECT name, location, status, srcip
  FROM ch5_meta METADATA
 ORDER BY name;
```

This returns one row per tag name.

```sql
SELECT *
  FROM ch5_meta METADATA
 ORDER BY name;
```

`SELECT *` and `table_alias.*` return only `NAME` and metadata columns.

System-managed columns such as `_LAST_UPDATE_TIME` do not appear in `SELECT *`.
Specify their names explicitly when needed.

#### Query the Last Modification Time

TAG metadata has a system-managed `_LAST_UPDATE_TIME` column recording each
metadata row's last modification time.

`_LAST_UPDATE_TIME` records metadata row creation or an actual metadata value
change, not the latest tag DATA insertion.

##### Query Methods

Query `_LAST_UPDATE_TIME` explicitly by name.

```sql
SELECT name, _last_update_time
  FROM ch5_meta METADATA;
```

It can be selected with other metadata columns or used in predicates.

```sql
SELECT name, location, status, _last_update_time
  FROM ch5_meta METADATA
 WHERE name = 'TEMP_001';
```

`SELECT *` and `table_alias.*` omit `_LAST_UPDATE_TIME`.

##### Automatic Recording and Update Rules

Creating a metadata row records `_LAST_UPDATE_TIME` automatically.

```sql
INSERT INTO ch5_meta METADATA(name, location, status)
VALUES('TEMP_003', 'Building-A/F3', 'READY');
```

An actual user metadata value change updates `_LAST_UPDATE_TIME`.

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

Updating to the same value, or removing a missing JSON path without changing
the stored result, is not an actual change. `_LAST_UPDATE_TIME` remains unchanged.

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

Removing a nonexistent JSON path is also a no-op if the stored value does not
change. Run the example after creating the JSON table below.

##### Restrictions on Direct Writes

`_LAST_UPDATE_TIME` is system-managed. Users cannot insert or modify it directly.

The following statements are not allowed:

```sql
INSERT INTO ch5_meta METADATA(name, location, status, _last_update_time)
VALUES('TEMP_004', 'Building-A/F4', 'READY', now);
```

```sql
UPDATE ch5_meta METADATA
   SET _last_update_time = now
 WHERE name = 'TEMP_003';
```

`_LAST_UPDATE_TIME` is also prohibited as a TAG name column, TAG metadata column,
or target of `ALTER TABLE ... METADATA ADD COLUMN`. It cannot be removed with
`ALTER TABLE ... METADATA DROP COLUMN`.

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

Names sharing only the prefix, such as `_LAST_UPDATE_TIME2`, are allowed as user columns.

##### Time Predicates and Automatic Index

An index on `_LAST_UPDATE_TIME` is provided automatically for time predicates.

```sql
SELECT name, location, _last_update_time
  FROM ch5_meta METADATA
 WHERE _last_update_time >= TO_DATE('2026-06-08 00:00:00')
 ORDER BY _last_update_time;
```

There is no need to create another index on the same column.

##### machloader / tagmetaimport Considerations

When importing TAG metadata, include only `NAME` and user metadata columns in
input/form files. Internal `_ID` and system-managed `_LAST_UPDATE_TIME` are not input targets.

For metadata columns `location` and `status`, use this input form:

```text
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
```

The server fills `_LAST_UPDATE_TIME` automatically during import.

A user-defined `_LAST_UPDATE_TIME` in an ordinary LOG, LOOKUP, or VOLATILE table
behaves as an ordinary column. Reserved behavior applies only to the TAG metadata
system column.

#### Query with Data

Use ordinary `FROM TAG` to query time-series data using metadata predicates.

```sql
SELECT name, status, time, value
  FROM ch5_meta
 WHERE status = 'READY'
 ORDER BY name, time;
```

Results are DATA-row based, so a tag's metadata values repeat with each DATA row.

Notes:

- `FROM TAG METADATA` cannot select DATA columns such as `TIME` or `VALUE`.
- `FROM TAG` selects DATA mode; `FROM TAG METADATA` selects metadata mode.
- Internal `_ID` and `_RID` columns are unavailable in `TAG METADATA`.

### Update Metadata

Use `UPDATE TAG METADATA` to change metadata.

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE',
       srcip = '10.0.0.20'
 WHERE name = 'TEMP_001';
```

Metadata predicates can update multiple tags at once.

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```

Notes:

- Update targets are `NAME` and metadata columns.
- `UPDATE ... METADATA` cannot change DATA columns such as `TIME` or `VALUE`.
- Internal columns cannot be changed.
- `_LAST_UPDATE_TIME` changes only when metadata values actually change.

### Delete Metadata

Use `DELETE FROM TAG METADATA` to delete metadata.

To delete one tag's metadata, specify its name in `WHERE`.

```sql
DELETE FROM ch5_meta METADATA
 WHERE name = 'TEMP_002';
```

Metadata predicates can delete multiple tags at once.

```sql
DELETE FROM ch5_meta METADATA
 WHERE status = 'STOP';
```

Without `WHERE`, all metadata is targeted. The exercise still contains DATA for
TEMP_OLD and TEMP_NEW, so the following full deletion intentionally fails.

```sql
DELETE FROM ch5_meta METADATA;
```

Notes:

- If any target has DATA rows, the entire statement fails.
- Metadata for a tag in use cannot be deleted.
- Full deletion also fails entirely if any tag is in use; it does not delete only unused tags.

To delete metadata for a tag in use, delete its DATA rows first, then retry the
metadata deletion.

```sql
DELETE FROM ch5_meta
 WHERE name = 'TEMP_001';

DELETE FROM ch5_meta METADATA
 WHERE name = 'TEMP_001';
```

<a id="metadata-design-json"></a>

### JSON Metadata Columns

Metadata can contain `JSON` columns.

```sql
CREATE TAG TABLE ch5_meta_json (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON
);
```

Example JSON metadata input:

```sql
INSERT INTO ch5_meta_json METADATA VALUES (
    'SHIP_001',
    'READY',
    '{"name":"alpha","ship":{"status":"READY"}}'
);
```

Notes:

- Do not specify a length for `JSON` metadata columns.
- Invalid JSON strings raise errors.
- The raw JSON column itself is not indexed automatically.

### When a JSON Value Does Not Change

```sql
SELECT name, _last_update_time FROM ch5_meta_json METADATA;
UPDATE ch5_meta_json METADATA
   SET info = JSON_REMOVE(info, '$.missing')
 WHERE name = 'SHIP_001';
SELECT name, _last_update_time FROM ch5_meta_json METADATA;
```

If a missing path leaves the stored value unchanged, the modification time also remains unchanged.

### Query JSON Paths

Query JSON metadata with the `->` operator.

```sql
SELECT name,
       info->'$.name',
       info->'$.ship.status'
  FROM ch5_meta_json METADATA
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name;
```

Use the same syntax in DATA queries.

```sql
SELECT name, time, value
  FROM ch5_meta_json
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name, time;
```

#### Path Notation

Queries and partial updates use full JSONPath syntax.

- Ordinary key: `$.name`
- Nested key: `$.ship.status`
- Use bracket notation for keys containing `.` or `-`.

```sql
SELECT info->'$[''ship.owner'']'
  FROM ch5_meta_json METADATA;

SELECT info->'$[''ship-owner'']'
  FROM ch5_meta_json METADATA;
```

### JSON Path Indexes

#### Declare Indexes at Table Creation

Index frequently queried JSON paths in the metadata definition.

```sql
CREATE TAG TABLE ch5_meta_json_indexed (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON INDEX('name', 'ship.status')
);
```

Strings inside `INDEX(...)` are interpreted as follows:

- `'name'` means `$.name`.
- `'ship.status'` means `$.ship.status`.
- Use full JSONPath for special-character keys or complex paths.

```sql
INFO JSON INDEX('$[''ship.owner'']')
```

#### Add Indexes After Creation

JSON path indexes can also be added after table creation.

```sql
CREATE INDEX idx_ship_owner
ON ch5_meta_json METADATA (info->'$.owner');
```

#### Drop an Index

Drop an index by its name.

```sql
SHOW INDEX idx_ship_owner;
DROP INDEX idx_ship_owner;
```

Manage explicitly created indexes by their declared names. Run
`SHOW INDEX idx_ship_owner;` before DROP. After deletion, the same name refers
to a nonexistent object.

#### Index Considerations

Current JSON path indexes primarily support string comparisons.

```sql
SELECT name
  FROM ch5_meta_json METADATA
 WHERE info->'$.status' = 'READY';
```

String-literal comparisons can use indexes. Numeric-literal comparisons may use a full scan.

Examples:

- `info->'$.num' = '10'`: May use an index
- `info->'$.num' = 10`: May use a full scan

### Partial JSON Updates

JSON functions return a new document value with the specified path changed.
UPDATE stores that result in the column. This is a logical path-level update,
not a performance guarantee of modifying only part of a storage file in place.

#### JSON_SET

Stores an SQL scalar as a JSON scalar.

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';
```

#### JSON_SET_JSON

Parses the input string as JSON and stores an object or array.

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_SET_JSON(info, '$.owner', '{"name":"machbase","team":"db"}')
 WHERE name = 'SHIP_001';
```

#### JSON_REMOVE

Removes a member or nested path.

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_REMOVE(info, '$.owner.team')
 WHERE name = 'SHIP_001';
```

#### Partial Update Rules

- `JSON_SET(..., path, NULL)` stores JSON `null`.
- `JSON_SET_JSON(..., path, NULL)` returns SQL `NULL`.
- A `NULL` JSON document argument returns SQL `NULL`.
- A `NULL` or empty path raises an error.
- `JSON_REMOVE` of a nonexistent path is a no-op, not an error.
- `JSON_REMOVE(..., '$')` is not allowed.
- Partial updates primarily support object paths.
- Array-element path updates, such as `$.items[0]`, are unsupported.

### Complete Example

```sql
CREATE TAG TABLE ch5_meta_complete (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    srcip IPV4,
    info JSON INDEX('name', 'ship.status')
);

INSERT INTO ch5_meta_complete METADATA VALUES (
    'SHIP_001',
    'READY',
    '192.168.0.11',
    '{"name":"alpha","ship":{"status":"READY"}}'
);

INSERT INTO ch5_meta_complete VALUES ('SHIP_001', '2026-04-01 00:00:00', 10.5);

SELECT name, status, info
  FROM ch5_meta_complete METADATA;

SELECT name, time, value
  FROM ch5_meta_complete
 WHERE info->'$.ship.status' = 'READY';

CREATE INDEX idx_ship_owner
ON ch5_meta_complete METADATA (info->'$.owner');

UPDATE ch5_meta_complete METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';

DROP INDEX idx_ship_owner;
```

### Summary

- Metadata-only queries: `FROM TAG METADATA`
- DATA queries: `FROM TAG`
- Metadata updates/deletions: `UPDATE/DELETE ... METADATA`
- ARRAY metadata changes: `ALTER TABLE ... METADATA ADD/DROP COLUMN`
- JSON metadata: `INFO JSON`
- `_LAST_UPDATE_TIME` is the metadata row's last modification time and can be queried explicitly.
- JSON path indexes: `INFO JSON INDEX(...)` or `CREATE INDEX ... ON TAG METADATA (...)`
- Partial JSON updates: `JSON_SET`, `JSON_SET_JSON`, `JSON_REMOVE`
- The server manages `_LAST_UPDATE_TIME` identically in Standard and Cluster environments.

<a id="metadata-design-tag"></a>

## Clean Up the Exercise

Unlike the full-deletion failure example, DROP removes the table, DATA, and METADATA.
Verify that these names belong to objects created for this exercise before executing.

```sql
DROP TABLE ch5_meta;
DROP TABLE ch5_meta_json;
DROP TABLE ch5_meta_json_indexed;
DROP TABLE ch5_meta_complete;
```
