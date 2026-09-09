---
type: docs
title: '5.1 Overview and Selection Criteria'
weight: 10
toc: true
---

Consider TAG for histories of repeated observations of sensors, equipment,
or similar entities. Start by distinguishing one tag from one row. Multiple
rows at different times can share a name; a shared name alone does not
remove duplicate rows.

<a id="overview-tag-characteristics"></a>

## TAG Table Characteristics

`PRIMARY KEY` identifies the tag name, unlike a relational per-row unique
key. One table has either a time axis or a distance axis.

```sql
-- Time-axis TAG for observations over time.
CREATE TAG TABLE ch5_overview_time (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- Distance-axis TAG for observations over distance or position.
-- Distance-axis TAG does not support ROLLUP.
CREATE TAG TABLE ch5_overview_distance (
    name     VARCHAR(64) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```

In both examples, the name is first and the axis second. Time axes use
`DATETIME BASETIME`; distance axes use `DOUBLE`, `LONG`, or `ULONG` with
`BASEDISTANCE`. Optional `SUMMARIZED` belongs on the third column. See
[Create, Alter, and Drop](../create-alter-drop/) for column order/types and
[Table Structure and Schema](../table-structure-schema/) for design choices.

`SUMMARIZED` marks a representative statistics/aggregation column. It does
not automatically create a ROLLUP object.

The following lists data scopes to distinguish, not columns of the sample
table. DATA consists of user-supplied observations; METADATA and STAT are
separate scopes for per-tag attributes and statistics.

| Scope | Meaning |
|---|---|
| Tag name | First column identifying a sensor or repeatedly observed entity |
| DATA | User-supplied observation rows: axis values and DATA columns |
| METADATA | Current per-tag attributes such as location, units, and settings; separate from ordinary DATA |
| STAT | Per-tag ingestion statistics from `V$<TABLE>_STAT`, not direct sample-table columns |

<a id="overview-tag-use-criteria"></a>

## When TAG Fits

- Continuously append histories of multiple entities using one schema.
- Frequently query time/distance ranges for specific tags.
- Select tags by current attributes and analyze their histories.
- Store and query repeated interval statistics on a time axis. See
  [TAG ROLLUP](../../tag-rollup-usage/) for aggregation design.

A single-value model uses a tag per measurement; a multi-value model groups
temperature, pressure, and other simultaneous measurements in one row. Do
not force readings from different times into one row; define missing-data
and quality policies. Equal timestamps may reflect duplicate collection,
so define duplicate handling for name, time, and values separately.

<a id="overview-tag-not-use"></a>

## When to Consider Other Tables

| Requirement | Alternative |
|---|---|
| Event searches centered on events rather than observed entities | LOG |
| General predicates and changes on persistent reference data | LOOKUP |
| Explicit multi-DML transactions and relational changes | TRANSACTION (Standard Edition only) |
| Shared state cache rebuildable from a source | VOLATILE |

TAG also supports JOIN and limited value correction. Do not assume that JOIN
requirements rule out TAG or that every measurement must use TAG.

DATA UPDATE is Standard Edition only. Cluster supports only METADATA UPDATE;
plan reingestion and reaggregation when measurement correction is required.

<a id="overview-tag-design-flow"></a>

## Design Sequence

1. Define whether a tag identifies a sensor, equipment item, or inspection run.
2. Define the meaning and units of measurement time or distance/position.
3. Define value types, NULL/quality indicators, and observation frequency.
4. Separate per-observation attributes from current METADATA.
5. Compare range-query, aggregation, correction, and retention needs with Edition support.

Verify and remove the example tables as follows:

```sql
-- Inspect the example schemas.
DESC ch5_overview_time;
DESC ch5_overview_distance;

-- Clean up to avoid name conflicts with later examples.
DROP TABLE ch5_overview_distance;
DROP TABLE ch5_overview_time;
```

Continue with [Schema Design](../table-structure-schema/) and
[Ingestion and Query Exercises](../data-input-mutation/).
