---
title: '5.3 Create, Alter, and Drop'
weight: 30
toc: true
---

Create independent exercise tables whose names do not collide with existing objects. A TAG table
has one VARCHAR name column first, one time or distance axis second, and an optional SUMMARIZED
column third.

<a id="original-85-creating-tag-tables"></a>

## Create a TAG Table

A time axis uses DATETIME BASETIME. A distance axis uses DOUBLE, LONG, or ULONG BASEDISTANCE.
Distance-axis TAG does not support ROLLUP.

### Time-Axis Table

```sql
CREATE TAG TABLE ch5_tag_ddl (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(64)
);
```


SUMMARIZED accepts supported numeric types or JSON, not ARRAY. Numeric and JSON summaries have
different aggregation rules. The flag alone does not create a ROLLUP. Store per-observation values
in DATA and current per-tag attributes such as location in METADATA.

### Distance-Axis Table

```sql
CREATE TAG TABLE ch5_distance_ddl (
    name     VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```


Choose DOUBLE for fractional positions and LONG/ULONG for integer ranges. Define units and the
identity of an inspection run rather than mixing repeated runs under an ambiguous tag.

## Alter Metadata

The following ADD/DROP exercise uses Standard Edition. TAG DATA does not support arbitrary schema
mutation; consider a validated table migration when needed. METADATA supports the declared forms.

```sql
ALTER TABLE ch5_tag_ddl
    METADATA ADD COLUMN (team VARCHAR(32));

ALTER TABLE ch5_tag_ddl METADATA
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE ch5_tag_ddl
    METADATA DROP COLUMN (team);

ALTER TABLE ch5_tag_ddl METADATA
    DROP COLUMN (limits);
```


Existing metadata rows receive the specified ARRAY DEFAULT at ALTER time. Tags automatically
registered by later DATA inserts do not receive that ADD COLUMN DEFAULT; the new ARRAY is whole
NULL. Without a DEFAULT, old rows are also whole NULL. ARRAY metadata has no automatic or explicit
index. See [Metadata](../tag-metadata/) and [Numeric ARRAY](/kr/dbms/reference/sql/type-data-types-dictionary/array/)
for detailed contracts.

Check DESC, metadata results, dependent queries, and positional SDK mappings after changing schema.

## Drop the Exercise Tables

DROP removes raw data and metadata. Inspect dependent ROLLUPs and other objects before removing
an operational table. TAG DROP with CASCADE can remove related ROLLUPs and is not the default
cleanup choice. Custom ROLLUP destination dependencies also need separate handling.

```sql
DROP TABLE ch5_distance_ddl;
DROP TABLE ch5_tag_ddl;
```


See [DDL Reference](../../reference/sql/syntax-dictionary-sql/ddl-syntax/) for complete syntax.
