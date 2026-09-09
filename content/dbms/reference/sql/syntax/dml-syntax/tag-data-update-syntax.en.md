---
type: docs
title: 'TAG data UPDATE'
weight: 10
toc: true
---

Modify TAG time-series data with ordinary UPDATE. There is no separate UPDATE TAG TABLE keyword sequence.

<span class="badge-since">Supported since Machbase 8.7.0</span>

TAG data UPDATE is supported only on logical TAG tables in Standard Edition.

## Syntax

```sql
UPDATE table_name
   SET data_column = expression [, data_column = expression ...]
 WHERE tag_selector
   AND time_condition
   [AND data_predicate ...];
```

tag_selector supports name = ..., name IN (...), and name LIKE ... predicates. time_condition
supports BASETIME equality, BETWEEN, and bounded or one-sided ranges.

## Examples

### Single Tag and Time Range

```sql
UPDATE sensor_tag
   SET value = 110,
       status = 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### Multiple Tags

```sql
UPDATE sensor_tag
   SET note = 'corrected'
 WHERE name IN ('TEMP-01', 'TEMP-02')
   AND time BETWEEN TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2026-07-01 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
```

### LIKE and Data-Column Predicates

```sql
UPDATE sensor_tag
   SET status = 7
 WHERE name LIKE 'TEMP-%'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND value > 100;
```

### CASE Expressions

```sql
UPDATE sensor_tag
   SET grade = CASE
                 WHEN 1 = 1 THEN 'HIGH'
                 ELSE 'LOW'
               END
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

<a id="tag-data-update-predicate-bind"></a>

### Bind Parameters in NAME and TIME Predicates

Tag-name and BASETIME values in WHERE support positional ? or named :name markers. Do not mix marker
styles in one statement.

Positional markers bind SET values, tag names, and reference times in SQL occurrence order.

```sql
UPDATE sensor_tag
   SET value = ?,
       status = ?,
       note = ?
 WHERE name = ?
   AND time = ?;
```

Named markers allow SDK name-based APIs to supply values independently of SQL order.

```sql
UPDATE sensor_tag
   SET value = :value,
       status = :status,
       note = :note
 WHERE name = :name
   AND time = :time;
```

Reexecuting the same prepared statement selects targets using newly bound SET, NAME, and TIME
values. NAME parameters retain VARCHAR metadata and TIME parameters DATETIME metadata. No matching
rows returns 0 affected rows without an error.

Reversed equality with the column on the right, such as ? = name, :name = name, ? = time, or :time =
time, is also supported. Prefer columns on the left for readability. Markers can also replace values
in existing supported BASETIME range predicates.

For SDK name-based APIs and ordinal rules, see [Named Bind Parameters](../../named-bind-parameter-syntax/).

## Metadata UPDATE

TAG metadata columns are not SET targets for TAG data UPDATE. Modify metadata with UPDATE ... METADATA.

```sql
UPDATE sensor_tag METADATA
   SET location = 'zone-2',
       owner = 'ops'
 WHERE name = 'TEMP-01';
```

## Restrictions

- WHERE requires one tag selector and at least one BASETIME predicate. Supported forms include name equality, IN, LIKE, and time equality, BETWEEN, bounded ranges, or one-sided ranges. Add data-column predicates with AND.
- OR, subqueries, aggregates, and tag/axis expressions that are not bare columns are unsupported as target predicates.
- name (PRIMARY KEY), time (BASETIME), metadata, and hidden/system columns cannot be data UPDATE SET targets.
- SET right-hand sides allow constants, bind variables, functions/operations/CASE that do not reference existing row columns, and NULL. Existing-column expressions such as value = value + 1 are unsupported.
- Bind parameters replace only values; tag-selector, BASETIME, and SET-target restrictions remain unchanged.
- UPDATE does not automatically correct already materialized ROLLUP rows. Rebuild affected intervals with ROLLUP_REBUILD before querying those aggregates.


## Related

- [TAG data UPDATE WHERE/SET constraints](../tag-data-update-where-set-constraints/)
- [Named Bind Parameter](../../named-bind-parameter-syntax/)
- [ROLLUP_REBUILD syntax](../../rollup-rebuild-syntax/)
