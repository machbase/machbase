---
type: docs
title: 'Named Bind Parameter'
weight: 30
toc: true
---

Named Bind Parameters use :name markers in SQL value positions and bind values at execution. Names
express the meaning of repeated parameters and keep the SQL/application mapping clear.

```sql
SELECT ID, NAME
FROM SENSOR_DATA
WHERE ID = :id;
```

## Name Syntax

Named markers use the following form.

```text
:[A-Za-z_$][A-Za-z0-9_$]*
```

| Category | Examples |
|---|---|
| Valid names | :id, :sensor_id, :value2, :_from_time, :select |
| Invalid names | :1id, :, ::id |

For SQL shared across SDKs, prefer names matching `[A-Za-z][A-Za-z0-9_]*`.

Parameter names are case-sensitive: :VALUE, :value, and :VaLuE are different names. .NET
MachParameterCollection performs case-insensitive lookup for compatibility with the existing
provider.

## Allowed Positions

Use named markers where a value or expression is allowed.

```sql
SELECT ID, NAME, VALUE
FROM SENSOR_DATA
WHERE CREATED_AT >= :from_time
  AND CREATED_AT < :to_time
  AND VALUE >= :minimum_value
ORDER BY CREATED_AT
LIMIT :row_count OFFSET :start_row;
```

Parameters cannot replace identifiers or SQL structure such as the following.

```sql
SELECT * FROM :table_name;               -- Unsupported
SELECT :column_name FROM SENSOR_DATA;     -- Does not replace a column identifier
SELECT * FROM SENSOR_DATA ORDER BY ID :direction; -- Unsupported
```

For dynamic identifiers, validate against an application allowlist before constructing SQL.

Colons inside strings and SQL comments are not recognized as parameters.

```sql
SELECT ':not_a_parameter'
FROM SENSOR_DATA
WHERE ID = :id /* :ignored */;
```

## Parameter Occurrence Order

Parameters are counted by occurrences in SQL, not unique names. In the following SQL, target appears
twice, so there are two parameters.

```sql
SELECT ID, NAME
FROM SENSOR_DATA
WHERE ID = :target
   OR PARENT_ID = :target;
```

- SQLNumParams() returns 2.
- Ordinal APIs bind the first and second positions separately.
- Name-based APIs apply one target value to both matching positions.
- Parameter metadata contains a separate entry for each position.

A statement supports at most 256 parameter occurrences.

## Relationship to Positional Markers

Low-level ordinal APIs can bind ? and :name in SQL occurrence order. Name-, object-, or
mapping-based APIs reject mixed anonymous ? and named markers. Use one marker style per SQL
statement.

| Method | SQL marker | Binding |
|---|---|---|
| Positional | ? | 1-based ordinal in SQL occurrence order |
| Named SQL with ordinal API | :name | 1-based ordinal in SQL occurrence order |
| Named API | :name | Parameter name |

## DML Examples

Named Bind Parameters use the existing prepared-statement type rules.

```sql
INSERT INTO SENSOR_DATA
    (ID, PARENT_ID, NAME, VALUE, CREATED_AT)
VALUES
    (:id, :parent_id, :name, :value, :created_at);
```

Named Bind Parameters do not change table-specific DML policies or Edition restrictions. For
supported DML and predicates, see [DML Syntax](../dml-syntax/) and
[Support Scope and Constraints](../../../support-scope-constraints/).

Standard and Cluster Editions use the same :name syntax and ordinal rules. Executable SQL and table
types remain subject to each Edition's existing support scope.

<a id="named-bind-tag-data-update"></a>

### TAG Data UPDATE

Since Machbase 8.7.0, Standard Edition TAG data UPDATE supports named markers for NAME and BASETIME
predicate values in WHERE.

```sql
UPDATE sensor_tag
   SET value = :value,
       status = :status,
       note = :note
 WHERE name = :name
   AND time = :time;
```

Reexecuting the same prepared statement can bind new SET, NAME, and TIME values. No matching row
succeeds with 0 affected rows. Tag selection and BASETIME predicates remain required regardless of
binding, and SET column restrictions still apply.

For supported predicate forms and parameter metadata, see
[TAG Data UPDATE](../dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind).

## Use in CTEs

Standard Edition permits named parameters in CTE bodies and the main SELECT.

```sql
WITH FILTERED AS (
    SELECT ID, NAME, VALUE
    FROM SENSOR_DATA
    WHERE ID > :minimum_id
      AND NAME = :label
)
SELECT ID, NAME, VALUE
FROM FILTERED
WHERE ID = :target_id
ORDER BY ID;
```

Parameter ordinals above are minimum_id, label, and target_id in that order. For CTE scope and
Standard Edition restrictions, see [WITH / CTE Syntax](../cte-syntax/).

## NULL and Data Types

Pass NULL using the SDK's standard NULL value or indicator.

| SDK | NULL value |
|---|---|
| Machbase SQLCLI | SQL_NULL_DATA indicator |
| ODBC | SQL_NULL_DATA indicator |
| JDBC | null |
| Node.js/TypeScript | null |
| Python | None |
| .NET | DBNull.Value |

Binding NULL to column = :value does not make it equivalent to column IS NULL. Use IS NULL according
to SQL NULL comparison rules.

Existing prepared-statement types such as INTEGER, VARCHAR, DOUBLE, DECIMAL, NUMERIC, and DATETIME
are supported. Use an SDK decimal type or string representation to preserve DECIMAL/NUMERIC
precision.

## Binding by SDK

| SDK or tool | Name-based usage |
|---|---|
| Machbase SQLCLI | SQLBindParameterByName(), SQLBindParameterByNameW() |
| ODBC | Bind :name SQL through SQLBindParameter() ordinals |
| JDBC | MachPreparedStatement.setObject(String name, Object value) |
| Node.js/TypeScript | Arrays for positional input; objects for named input |
| Python DB-API | Pass a mapping; the 2.4 prepared cursor reuses :name and %(name)s across calls |
| .NET | MachCommand.Parameters.AddWithValue(":name", value) |
| Go native | api.Named("name", value) |
| Go database/sql | sql.Named("name", value) |
| machsql | :name in SQL; values assigned in $1, $2 order |

For API details and error handling, see
[Development Integration](../../../../development-tools-integration/) and
[machsql Commands and Options](../../../command-line-tools/machsql/).

## Compatibility and Errors

Machbase 8.7.0 name-based SDK APIs require both a client and server supporting the feature. Use ?
with ordinal APIs for older-version compatibility.

| Situation | Typical error |
|---|---|
| Required name missing | missing parameter |
| Name absent from SQL supplied | unknown or extra parameter |
| Named and positional styles mixed | sequence or mixed error |
| Value type incompatible with SQL type | type or conversion error |
| Name-based API used against an older server | unsupported |

In production, prioritize SQLSTATE, error codes, and exception types over message text. For version
combinations and SDK error codes, see
[Client/Server Protocol Compatibility](../../../support-scope-constraints/compatibility-xma-protocol/).
