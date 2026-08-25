---
type: docs
title: '4.3 Data Mutation Policy'
weight: 30
toc: true
---



<a id="policy-update"></a>

## UPDATE 정책

<a id="policy-update-policy-tag-data-update"></a>

### TAG data UPDATE policy

TAG time-series rows can be updated under explicit target conditions. The UPDATE
must be limited by tag selection and the BASETIME column, and metadata updates use
a separate syntax.

#### Policy

1. The WHERE clause must include a tag selector: `name =`, `name IN`, or `name LIKE`.
2. The WHERE clause must include a BASETIME condition.
3. SET targets must be data columns.
4. `name` (PRIMARY KEY), `time` (BASETIME), and metadata columns cannot be updated
   by TAG data UPDATE.

```sql
UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

Metadata columns use `UPDATE ... METADATA`.

```sql
UPDATE tag METADATA
   SET location = 'zone-2'
 WHERE name = 'TEMP-01';
```

Before large corrections, verify the target row count with the same WHERE clause.
If rollup data is queried for the corrected interval, rebuild affected rollups
with `ROLLUP_REBUILD`.

<a id="policy-update-distinction-tag-data-update-metadata"></a>

### TAG data UPDATE와 UPDATE ... METADATA 구분

<a id="policy-update-tag-data-update-where-set-standard-only"></a>

### TAG data UPDATE WHERE/SET support scope

TAG data UPDATE is supported with constraints that keep the update target explicit.

#### Supported form

```sql
UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-15 11:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

#### Allowed WHERE/SET scope

- Tag selector: `name =`, `name IN (...)`, `name LIKE ...`
- Time condition: `time =`, `BETWEEN`, two-sided ranges, one-sided ranges
- Additional filters: data-column predicates
- SET targets: data columns, including `SUMMARIZED` data columns

#### Not allowed

- UPDATE without a WHERE clause
- UPDATE without a tag selector
- UPDATE without a time condition
- `OR`, subqueries, and aggregate predicates
- SET targets such as `name`, `time`, or metadata columns

Metadata columns use `UPDATE tag METADATA SET ...`.

<a id="policy-delete"></a>

## DELETE 정책

<a id="policy-delete-delete-tag-metadata"></a>

### TAG Metadata Delete

<a id="condition-tag-kv-delete-before"></a>

## TAG/KV DELETE 허용 조건과 BEFORE 조건

<a id="policy-truncate"></a>

## TRUNCATE 정책
