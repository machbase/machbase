---
type: docs
title: 'TAG data UPDATE WHERE/SET constraints'
weight: 20
toc: true
---

TAG data UPDATE requires an explicit target scope. WHERE must contain both tag selection and
BASETIME predicates, and SET can target only actual data columns.

<span class="badge-since">Supported since Machbase 8.7.0</span>

## SET Restrictions

| Column role | SET allowed | Description |
|-----------|:------------:|------|
| Data column | Yes | value and auxiliary numeric/string columns |
| SUMMARIZED data column | Yes | Changes source TAG row values |
| BASETIME column | No | Time-axis column cannot change |
| PRIMARY KEY column (name) | No | Tag name cannot change |
| Metadata column | No | Use UPDATE ... METADATA separately |
| Hidden/system column | No | Internal columns are not SET targets |

SET expressions allow constants, bind variables, arithmetic/string/CASE expressions without
existing-row references, supported conversion functions, and NULL. Existing-row column references,
subqueries, and aggregates are unsupported on the right-hand side.

## WHERE Restrictions

```sql
UPDATE table_name
   SET col = expr
 WHERE name = 'tag-name'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

| WHERE predicate | Supported |
|-----------|:---------:|
| `name = '...'` | Yes |
| `name = ?`, `name = :tag_name` | Yes |
| `? = name`, `:tag_name = name` | Yes |
| `name IN ('...', '...')` | Yes |
| `name LIKE '...'` | Yes |
| `time = t1` | Yes |
| `time = ?`, `time = :base_time` | Yes |
| `? = time`, `:base_time = time` | Yes |
| `time BETWEEN t1 AND t2` | Yes |
| `time >= t1 AND time < t2` | Yes |
| `time >= ? AND time < ?` | Yes |
| One-sided time predicate | Yes |
| Data-column predicate | Yes |
| No tag selector | No |
| No time predicate | No |
| OR | No |
| IN (SELECT ...) | No |
| Tag/axis column wrapped in a function or expression | No |

Use bind parameters only in predicate value positions. Markers cannot replace tag-name or BASETIME
column identifiers, and both tag selection and time predicates remain mandatory. Reexecution selects
targets using newly bound values; no match succeeds with 0 affected rows.

For NAME/TIME parameter metadata and SDK APIs, see
[Bind Parameters in TAG Data UPDATE](../tag-data-update-syntax/#tag-data-update-predicate-bind) and
[Named Bind Parameters](../../named-bind-parameter-syntax/).

## Metadata UPDATE

```sql
UPDATE table_name METADATA
   SET meta_col = value
 WHERE condition;
```

Metadata UPDATE modifies the tag-attribute area. Its syntax and targets differ from TAG data UPDATE,
which modifies data columns in actual time-series rows.

## Checking Column Roles

Use DESC to inspect column attributes.

```sql
DESC sensor_tag;
```

Alternatively, query column FLAG values in system tables.

```sql
SELECT NAME, TYPE, FLAG
  FROM M$SYS_COLUMNS
 WHERE TABLE_ID = (
     SELECT ID FROM M$SYS_TABLES WHERE NAME = 'SENSOR_TAG'
 );
```

| FLAG value | Meaning |
|---------|------|
| 134217728 | Tag Name |
| 16777216 | Base Time / Base Distance |
| 33554432 | Summarized |
| 67108864 | Metadata |

## Error Examples

```sql
-- Error: BASETIME column used as a SET target
UPDATE sensor_tag
   SET time = TO_DATE('2026-07-01', 'YYYY-MM-DD')
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- Error: missing time predicate
UPDATE sensor_tag
   SET value = 0.0
 WHERE name = 'TEMP-01';

-- Error: OR predicate
UPDATE sensor_tag
   SET value = 0.0
 WHERE name = 'TEMP-01'
    OR name = 'TEMP-02';
```

## Related Documentation

- [TAG data UPDATE syntax](../tag-data-update-syntax/)
- [Named Bind Parameter](../../named-bind-parameter-syntax/)
- [ROLLUP_REBUILD syntax](../../rollup-rebuild-syntax/)
