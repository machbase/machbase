---
title: '5.10 TAG Metadata'
weight: 100
toc: true
---

<a id="original-85-tag-metadata"></a>
<a id="metadata-design-tag"></a>

## Current Attributes and Observation History

METADATA contains one current attribute row per tag. Ordinary TAG queries join those attributes
to each DATA row. Changing a location can therefore change how old observations are displayed.
Retain event-time attributes in DATA or a separate history if historical interpretation must not
change. Sensor location, units, thresholds, and external identifiers are typical metadata.

The basic, JSON, and complete fixtures below have distinct table names. Use unused names and run
each section's setup before its dependent statements.

## Define the Basic Metadata Table

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


The tag-name column identifies each metadata row. It is called name in this fixture, but its SQL
name is whatever the TAG declaration specifies.

## ARRAY ADD/DROP in Standard Edition

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


TEMP_OLD existed before ALTER and receives [0.0000,NULL]. TEMP_NEW is automatically registered by
a later DATA insert and receives whole NULL for limits. Without a DEFAULT, old rows also receive
whole NULL. This ADD COLUMN DEFAULT is not reapplied to later automatic registrations.

The new metadata column appears in explicit projections and ordinary TAG SELECT *. ARRAY metadata
has neither an automatic nor an explicitly supported index. The following is an intentional error:

```sql
-- Unsupported: this statement must fail.
CREATE INDEX idx_sensor_limits ON ch5_meta METADATA(limits);
```


Remove the exercise column before the subsequent positional inserts:

```sql
ALTER TABLE ch5_meta METADATA DROP COLUMN (limits);
```


TAG DATA ARRAY columns can be declared at CREATE time, but cannot be added with ALTER.
See [ARRAY Rules](/kr/dbms/reference/sql/type-data-types-dictionary/array/).

## Register Metadata

```sql
INSERT INTO ch5_meta METADATA VALUES (
    'TEMP_001',
    'Building-A/F1',
    'READY',
    '192.168.0.11'
);
```

```sql
INSERT INTO ch5_meta METADATA (name, status, srcip, location)
VALUES ('TEMP_002', 'STOP', '192.168.0.12', 'Building-A/F2');
```


Without a column list, VALUES follows tag name then metadata declaration order. With a list, use
that list's order. Omitted values follow the relevant NULL/DEFAULT contract. New metadata rows
receive a server-managed _LAST_UPDATE_TIME.

<a id="metadata-query-tag"></a>

## Query Metadata

### Metadata Only

```sql
SELECT name, location, status, srcip
  FROM ch5_meta METADATA
 ORDER BY name;
```

```sql
SELECT *
  FROM ch5_meta METADATA
 ORDER BY name;
```


FROM table METADATA returns one row per tag. SELECT * and alias.* expose the tag name and user
metadata, not system-managed _LAST_UPDATE_TIME. DATA time/value columns cannot be selected in
this mode, and internal _ID/_RID are not public metadata projections.

### Last Actual Change

```sql
SELECT name, _last_update_time
  FROM ch5_meta METADATA;
```

```sql
SELECT name, location, status, _last_update_time
  FROM ch5_meta METADATA
 WHERE name = 'TEMP_001';
```

```sql
INSERT INTO ch5_meta METADATA(name, location, status)
VALUES('TEMP_003', 'Building-A/F3', 'READY');
```

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```


The insertion creates TEMP_003. Setting status to DONE changes it; repeating the same update is a
no-op and preserves the timestamp. _LAST_UPDATE_TIME tracks metadata creation and actual attribute
changes, not the most recent measurement time.

### Protected System Column: Intentional Failures

Users cannot supply or SET _LAST_UPDATE_TIME or use it as a tag/metadata column name. These
statements intentionally fail and should be run separately from successful examples.

```sql
INSERT INTO ch5_meta METADATA(name, location, status, _last_update_time)
VALUES('TEMP_004', 'Building-A/F4', 'READY', now);
```

```sql
UPDATE ch5_meta METADATA
   SET _last_update_time = now
 WHERE name = 'TEMP_003';
```

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


It also cannot be dropped or added through metadata ALTER. A different name such as
_LAST_UPDATE_TIME2 is a user column; an identically named column in an ordinary non-TAG table
does not acquire TAG metadata's special behavior.

### Time Predicate and Import

```sql
SELECT name, location, _last_update_time
  FROM ch5_meta METADATA
 WHERE _last_update_time >= TO_DATE('2026-06-08 00:00:00')
 ORDER BY _last_update_time;
```


The system-managed timestamp has an automatic time-search index. Do not create a duplicate index
for it. Import files contain the tag name and user metadata, not _ID or _LAST_UPDATE_TIME.
[Bulk Import](../tagmetaimport/) explains the tool-specific target and reimport behavior.

## Query DATA with Current Metadata

```sql
SELECT name, status, time, value
  FROM ch5_meta
 WHERE status = 'READY'
 ORDER BY name, time;
```


FROM table is DATA mode, so current attributes repeat on each observation row. Tags with metadata
but no observations do not manufacture DATA rows. Compare this result with FROM table METADATA
rather than expecting equal row counts.

## Update Attributes

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE',
       srcip = '10.0.0.20'
 WHERE name = 'TEMP_001';
```

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```


Use UPDATE table METADATA for tag attributes. DATA columns are not SET targets in this mode.
Only actual stored-value changes refresh _LAST_UPDATE_TIME. Name changes and system-protected
columns must follow TAG metadata rules rather than generic business-key assumptions.

## Delete Attributes

```sql
DELETE FROM ch5_meta METADATA
 WHERE name = 'TEMP_002';
```

```sql
DELETE FROM ch5_meta METADATA
 WHERE status = 'STOP';
```


A target tag must have no DATA rows. If any selected tag still has data, the entire metadata
deletion fails. The following whole-metadata deletion is an intentional failure in this fixture
because TEMP_OLD and TEMP_NEW still have DATA:

```sql
DELETE FROM ch5_meta METADATA;
```


When removing one subject, keep the DATA and METADATA scopes aligned:

```sql
DELETE FROM ch5_meta
 WHERE name = 'TEMP_001';

DELETE FROM ch5_meta METADATA
 WHERE name = 'TEMP_001';
```


Do not replace the second predicate with an unconditional metadata deletion unless all remaining
tags are intended targets and satisfy the precondition.

<a id="metadata-design-json"></a>

## JSON Metadata

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

```sql
INSERT INTO ch5_meta_json METADATA VALUES (
    'SHIP_001',
    'READY',
    '{"name":"alpha","ship":{"status":"READY"}}'
);
```


JSON is declared without a length modifier. Invalid JSON input fails, and the raw JSON column
does not automatically receive a whole-document index.

### No-Op Path Removal

```sql
SELECT name, _last_update_time FROM ch5_meta_json METADATA;
UPDATE ch5_meta_json METADATA
   SET info = JSON_REMOVE(info, '$.missing')
 WHERE name = 'SHIP_001';
SELECT name, _last_update_time FROM ch5_meta_json METADATA;
```


Removing a missing path leaves the document and metadata timestamp unchanged.

### Query Paths

```sql
SELECT name,
       info->'$.name',
       info->'$.ship.status'
  FROM ch5_meta_json METADATA
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name;
```

```sql
SELECT name, time, value
  FROM ch5_meta_json
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name, time;
```

```sql
SELECT info->'$[''ship.owner'']'
  FROM ch5_meta_json METADATA;

SELECT info->'$[''ship-owner'']'
  FROM ch5_meta_json METADATA;
```


Use full JSONPath in queries and mutations. A simple key is $.name; a nested key is $.ship.status.
Bracket quoting handles keys containing punctuation. The DATA query returns observations matching
current metadata; without DATA for SHIP_001, it returns no rows.

### Declare or Add Path Indexes

This is a separate DDL alternative and does not recreate ch5_meta_json:

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


In the declaration, 'name' means $.name and 'ship.status' means $.ship.status. Complex keys can
use a full path. The following is a column-declaration fragment, not a standalone SQL statement:

```sql
INFO JSON INDEX('$[''ship.owner'']')
```


Add an index to the first JSON table, inspect it before dropping, then remove it:

```sql
CREATE INDEX idx_ship_owner
ON ch5_meta_json METADATA (info->'$.owner');
```

```sql
SHOW INDEX idx_ship_owner;
DROP INDEX idx_ship_owner;
```


Metadata JSON path indexes are primarily for supported string comparisons. A numeric SQL literal
can have different comparison/index behavior from the string '10'. Use EXPLAIN on the actual
predicate; do not infer index use merely because a path index exists.

## Logical JSON Updates

JSON functions return a new document value with the specified path changed. UPDATE stores that
value; this is not a guarantee of in-place partial-file writes.

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';
```

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_SET_JSON(info, '$.owner', '{"name":"machbase","team":"db"}')
 WHERE name = 'SHIP_001';
```

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_REMOVE(info, '$.owner.team')
 WHERE name = 'SHIP_001';
```


| Operation | Meaning |
|---|---|
| JSON_SET | Store a SQL scalar as a JSON scalar |
| JSON_SET_JSON | Parse a JSON text value and store that subtree |
| JSON_REMOVE | Remove a supported object path |

JSON_SET with SQL NULL stores JSON null. JSON_SET_JSON with SQL NULL returns SQL NULL.
A NULL document returns SQL NULL. A NULL/empty path is invalid. Removing a missing path is a no-op;
removing root $ is not allowed. Mutations support object paths, not array-element mutation.

## Complete JSON Exercise

This third JSON fixture combines registration, DATA, predicates, an index, and an attribute change.

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


The first DATA query matches SHIP_001 while ship.status is READY. After JSON_SET it becomes DONE.
Inspect metadata again to confirm the change rather than treating index creation or DROP as a
data mutation. System-managed timestamps follow the same change/no-op distinction in both Editions.

## Cleanup

DROP removes DATA and METADATA together. Remove only tables created for these exercises.

```sql
DROP TABLE ch5_meta;
DROP TABLE ch5_meta_json;
DROP TABLE ch5_meta_json_indexed;
DROP TABLE ch5_meta_complete;
```
