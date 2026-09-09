---
type: docs
title: 'JSON Functions and Dot Notation'
weight: 40
toc: true
---

Machbase provides functions and JSON dot notation for querying and modifying data in `JSON` columns.

## Quick Reference

| Function/Notation | Syntax | Description |
|-------------|------|------|
| JSON dot notation | `col.key` | Extract an object key's value |
| `JSON_EXTRACT` | `JSON_EXTRACT(doc, path)` | Extract a path value as a JSON string |
| `JSON_EXTRACT_STRING` | `JSON_EXTRACT_STRING(doc, path)` | Extract a path value as a string |
| `JSON_EXTRACT_INTEGER` | `JSON_EXTRACT_INTEGER(doc, path)` | Extract a path value as an integer |
| `JSON_EXTRACT_DOUBLE` | `JSON_EXTRACT_DOUBLE(doc, path)` | Extract a path value as a floating-point number |
| `JSON_TYPEOF` | `JSON_TYPEOF(doc, path)` | Check the type at a JSON path |
| `JSON_IS_VALID` | `JSON_IS_VALID(json_text)` | Validate a JSON string |
| `JSON_SET` | `JSON_SET(doc, path, scalar)` | Set a scalar value at a JSON path |
| `JSON_SET_JSON` | `JSON_SET_JSON(doc, path, json_text)` | Set a JSON subtree at a path |
| `JSON_REMOVE` | `JSON_REMOVE(doc, path)` | Remove a member at a JSON path |

The `path` argument to `JSON_TYPEOF` is required. Use `JSON_TYPEOF(doc, '$')` to check the type of
the entire document.

---

## JSON Dot Notation

Append a dot (`.`) and key name to a JSON column to query that key's value.
Use this to access JSON members without writing a JSONPath string.

```sql
json_column.key
```

```sql
-- Extract a key from a JSON column
SELECT data.temperature AS temp FROM sensor_log;

-- Use in WHERE
SELECT * FROM sensor_log
 WHERE data.status = 'active';
```

To specify a JSONPath string explicitly, use the `->` operator, as in `data -> '$.temperature'`.
Keep this distinct from dot notation above.

---

## JSON_SET

Stores a SQL scalar as a JSON scalar at the specified document path.

```sql
JSON_SET(json_doc, path, scalar)
```

- `path` must be a full JSONPath, such as `$.key.subkey`.
- `JSON_SET(..., path, NULL)` stores JSON `null`.
- If the JSON document argument is SQL `NULL`, the result is SQL `NULL`.
- Array element updates such as `$.items[0]` are not supported.

```sql
Mach> SELECT JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE') FROM dual;
{"ship":{"status":"DONE"}}

Mach> SELECT JSON_SET('{"count":0}', '$.count', 42) FROM dual;
{"count":42}
```

---

## JSON_SET_JSON

Parses the third argument as JSON text and stores an object or array subtree.

```sql
JSON_SET_JSON(json_doc, path, json_text)
```

- If the third argument is SQL `NULL`, the result is SQL `NULL`.
- Invalid JSON text causes an error.
- Array element updates are not supported.

```sql
Mach> SELECT JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}') FROM dual;
{"ship":{"owner":{"name":"machbase"}}}

Mach> SELECT JSON_SET_JSON('{"tags":{}}', '$.tags.sensors', '[1,2,3]') FROM dual;
{"tags":{"sensors":[1,2,3]}}
```

---

## JSON_REMOVE

Removes a member or subpath from a JSON document.

```sql
JSON_REMOVE(json_doc, path)
```

- `path` must be a full JSONPath.
- A missing path is a no-op.
- `JSON_REMOVE(..., '$')` is not allowed.
- If the JSON document argument is SQL `NULL`, the result is SQL `NULL`.

```sql
Mach> SELECT JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team') FROM dual;
{"owner":{"name":"machbase"}}

Mach> SELECT JSON_REMOVE('{"a":1,"b":2}', '$.a') FROM dual;
{"b":2}
```

---

## JSON Insertion Example

```sql
-- LOG table with a JSON column
CREATE LOG TABLE device_log (
    ts    DATETIME,
    data  JSON
);

-- Insert JSON data
INSERT INTO device_log VALUES (NOW, '{"temperature":23.5,"humidity":60,"status":"active"}');

-- Extract values with JSON dot notation
SELECT ts, data.temperature AS temp
  FROM device_log
 WHERE data.status = 'active';
```

---

## JSON Support by Table Type

| Table Type | JSON Columns | JSON Path Queries | Notes |
|------------|:---------:|:---------------:|------|
| TAG | O | O | JSON columns and functions supported; JSON PK not supported |
| LOG | O | O | Fully supported |
| LOOKUP | O | O | Ordinary columns supported; JSON path indexes not supported |
| VOLATILE | X | X | Cannot create JSON columns |
| TRANSACTION | O | O | Fully supported |

For details, see [JSON Support by Table Type](/dbms/lookup-table-usage/json-column-query/).
