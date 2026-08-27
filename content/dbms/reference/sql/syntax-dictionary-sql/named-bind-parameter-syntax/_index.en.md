---
type: docs
title: '17.1.1.3 Named Bind Parameter'
weight: 30
toc: true
---

Named bind parameters use `:name` markers for SQL values.

```sql
SELECT ID, NAME
  FROM SENSOR_DATA
 WHERE ID = :id;
```

## Rules

- Names are case-sensitive and follow `:[A-Za-z_$][A-Za-z0-9_$]*`.
- Markers replace values, not table names, column names, keywords, or sort directions.
- Parameter occurrence count includes repeated names.
- Ordinal APIs bind each occurrence; named APIs apply one value to occurrences with the same name.
- Do not mix anonymous `?` and named markers in one statement when using a named API.
- NULL binding does not change `column = :value` into `IS NULL`.

```sql
INSERT INTO SENSOR_DATA(ID, NAME, VALUE, CREATED_AT)
VALUES (:id, :name, :value, :created_at);
```

Prepared-statement types and table DML constraints still apply. See
[Development and application integration](/dbms/development-tools-integration/) for SDK APIs and
[DML syntax](../dml-syntax/) for supported statements.

<a id="named-bind-tag-data-update"></a>

## TAG data UPDATE

Starting with Machbase 8.7.0, TAG data UPDATE in Standard Edition accepts named
markers for NAME and BASETIME condition values.

```sql
UPDATE sensor_tag
   SET value = :value,
       status = :status,
       note = :note
 WHERE name = :name
   AND time = :time;
```

Reexecuting the prepared statement can use new SET, NAME, and TIME values. A no-match
execution succeeds with affected rows `0`. Bind parameters do not relax the required
tag selector, BASETIME condition, or SET-target restrictions.

See [TAG data UPDATE predicate binds](../dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind)
for supported condition forms and parameter metadata.
