---
type: docs
title: '17.1.1.10.1 TAG data UPDATE syntax'
weight: 10
toc: true
---

TAG time-series rows are updated with the normal `UPDATE` statement. There is no
separate `UPDATE TAG TABLE` keyword form.

<span class="badge-since">Supported since Machbase 8.7.0</span>

TAG data UPDATE is supported only for logical TAG tables in Standard Edition.

## Syntax

```sql
UPDATE table_name
   SET data_column = expression [, data_column = expression ...]
 WHERE tag_selector
   AND time_condition
   [AND data_predicate ...];
```

`tag_selector` can be `name = ...`, `name IN (...)`, or `name LIKE ...`.
`time_condition` uses the BASETIME column and can be equality, `BETWEEN`, a
two-sided range, or a one-sided range.

## Examples

```sql
UPDATE sensor_tag
   SET value = 110,
       status = 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE sensor_tag
   SET note = 'corrected'
 WHERE name IN ('TEMP-01', 'TEMP-02')
   AND time BETWEEN TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2026-07-01 23:59:59', 'YYYY-MM-DD HH24:MI:SS');

UPDATE sensor_tag
   SET status = 7
 WHERE name LIKE 'TEMP-%'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND value > 100;
```

<a id="tag-data-update-predicate-bind"></a>

### Bind parameters in NAME and TIME conditions

The tag name and BASETIME condition values can use positional `?` or named `:name`
markers. Do not mix marker styles in one statement.

```sql
UPDATE sensor_tag
   SET value = ?,
       status = ?,
       note = ?
 WHERE name = ?
   AND time = ?;
```

```sql
UPDATE sensor_tag
   SET value = :value,
       status = :status,
       note = :note
 WHERE name = :name
   AND time = :time;
```

Reexecuting the same prepared statement uses the latest SET, NAME, and TIME bind values.
The NAME parameter retains `VARCHAR` metadata and the TIME parameter retains `DATETIME`
metadata. If no row matches, the statement succeeds with affected rows `0`.

Equality predicates with the column on the right, such as `? = name` and `? = time`,
are also supported. Prefer the column-left form for readability. Markers can also be
used as values in the supported BASETIME range conditions.

See [Named bind parameters](../../named-bind-parameter-syntax/) for SDK-specific named
and ordinal APIs.

## Metadata UPDATE

TAG metadata columns are not SET targets of TAG data UPDATE. Use
`UPDATE ... METADATA` for metadata columns.

```sql
UPDATE sensor_tag METADATA
   SET location = 'zone-2'
 WHERE name = 'TEMP-01';
```

## Restrictions

- The WHERE clause must include both a tag selector and a BASETIME condition.
- `OR`, subqueries, aggregates, and volatile predicates are not allowed for
  selecting the update target.
- `name` (PRIMARY KEY), `time` (BASETIME), metadata columns, and hidden/system
  columns cannot be SET targets of TAG data UPDATE.
- The SET right-hand side can use constants, bind parameters, and expressions that do
  not reference an existing row column. Expressions such as `value = value + 1` are
  not supported.
- Bind parameters replace values only; they do not relax the required tag selector,
  BASETIME condition, or SET-target restrictions.
- Rebuild affected rollups with `ROLLUP_REBUILD` when corrected intervals are
  served from rollup tables.

## Related

- [TAG data UPDATE WHERE/SET constraints](../tag-data-update-where-set-constraints/)
- [Named bind parameters](../../named-bind-parameter-syntax/)
- [ROLLUP_REBUILD syntax](../../rollup-rebuild-syntax/)
