---
type: docs
title: '17.1.1.10.1 TAG data UPDATE syntax'
weight: 10
---

TAG time-series rows are updated with the normal `UPDATE` statement. There is no
separate `UPDATE TAG TABLE` keyword form.

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
   SET value = value + 10,
       status = status + 1
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
- Rebuild affected rollups with `ROLLUP_REBUILD` when corrected intervals are
  served from rollup tables.
