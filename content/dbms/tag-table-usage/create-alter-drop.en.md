---
type: docs
title: '5.3 Create, Alter, and Drop'
weight: 30
toc: true
---
TAG tables require a tag identifier and one axis column. This page provides runnable
basic examples and links to the SQL reference for complete options.

<a id="original-85-creating-tag-tables"></a>

## Create a TAG Table

The first two columns have fixed roles. The name and axis columns are required;
changing their order or placing them elsewhere causes creation to fail.

| Position | Purpose and properties |
| --- | --- |
| First | Tag name: `VARCHAR` with `PRIMARY KEY`; no other type is allowed. Identifies a repeatedly observed entity such as a sensor, equipment item, or inspection run. Multiple DATA rows can share a tag name, unlike a relational per-row unique key. |
| Second | Orders and queries observations by time or distance/position. Use `DATETIME BASETIME` for time or `DOUBLE`, `LONG`, or `ULONG` with `BASEDISTANCE` for distance. A TAG table has only one of these axes. |
| Third and later | DATA columns that vary per observation, such as temperature, pressure, status, or quality code. Support numeric types, `VARCHAR`, `DATETIME`, JSON, numeric ARRAY, and BINARY. Choose one representative value for per-tag statistics and automatic ROLLUP by marking it `SUMMARIZED`. This is optional and allowed only on the third column. |

ARRAY is allowed only in other DATA columns, not the name, axis, or `SUMMARIZED`
column. Unlike LOG, TAG DATA does not support `TEXT`, `CLOB`, or `BLOB`; use
`VARCHAR` for long strings and `BINARY` for binary data. See the
[Data Type Reference](/dbms/reference/sql/types/) for syntax and ranges.

Declare attributes stored once per tag separately in `METADATA`, outside those
column positions. `location` in the time-axis example is one such attribute.

The two tables below are independent exercises. Check for existing objects,
then execute in order. Choose an axis matching the data meaning. Distance-axis
TAG tables do not support ROLLUP.

### Time-Axis TAG

```sql
CREATE TAG TABLE ch5_tag_ddl (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(64)
);
```

`SUMMARIZED` has two effects. First, per-tag STAT views collect value statistics
such as `MIN_VALUE` and `MAX_VALUE` for this column. Without it, STAT retains
only row counts and axis ranges. Second, automatic `WITH ROLLUP` creation and
whole-JSON-document ROLLUP use this column.

Ordinary numeric ROLLUP specifies a column explicitly in
`CREATE ROLLUP ... ON table(column)`, so it does not require `SUMMARIZED`. Omit
it if value statistics are unnecessary and you plan to create ROLLUP manually.
Supported types are the supported numeric types and JSON. See
[Chapter 6](../../tag-rollup-usage/) for ROLLUP creation requirements.

Store per-tag attributes such as location and units in `METADATA`; define
values that change per measurement as ordinary DATA columns.

### Distance-Axis TAG

```sql
CREATE TAG TABLE ch5_distance_ddl (
    name     VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```

Use `DOUBLE` for fractional distances, or `LONG`/`ULONG` for integer axes according to range.

## Alter a TAG Table

The METADATA ADD/DROP exercise requires Standard Edition. Arbitrary TAG DATA
column changes are restricted. Consider migrating to a new table for schema
expansion. Metadata columns can be added or dropped with supported syntax.

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

Standard Edition can add fixed-length numeric ARRAY columns to TAG METADATA.
Existing metadata rows receive the specified ARRAY DEFAULT. Rows automatically
registered by TAG DATA input after ALTER do not reapply that DEFAULT; the new
ARRAY column is whole NULL.

Ordinary TAG DATA ARRAY columns can be declared at `CREATE TABLE` but not added
with ALTER. TAG METADATA ARRAY columns have no automatic indexes and do not
support explicit indexes. See [TAG Metadata](../tag-metadata/) and
[Numeric ARRAY Types](/dbms/reference/sql/types/array/) for details.

Before changing a populated production table, check dependent queries, SDK
column order, and reingestion paths. After ALTER, verify with `DESC ch5_tag_ddl;`
and METADATA queries.

## Drop a TAG Table

`DROP TABLE` removes raw data and metadata together. Remove dependent objects
such as ROLLUP in dependency order first. TAG `DROP TABLE ... CASCADE` can also
remove associated ROLLUPs, so do not use it as a routine cleanup default. Check
additional dependency restrictions on custom ROLLUP target tables.

```sql
DROP TABLE ch5_distance_ddl;
DROP TABLE ch5_tag_ddl;
```

See the [DDL Syntax Reference](/dbms/reference/sql/syntax/ddl-syntax/) for exact
properties, supported scope, and DDL.

Read next:

- [TAG Table Structure and Schema](../table-structure-schema/)
- [TAG Data Ingestion and Changes](../data-input-mutation/)
- [TAG Metadata](../tag-metadata/)
