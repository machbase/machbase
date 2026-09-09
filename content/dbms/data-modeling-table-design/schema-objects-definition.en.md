---
type: docs
title: '4.2 Schema Object Definitions'
weight: 20
toc: true
---
This page covers decisions for designing tables, columns, indexes, and views. Use the
[SQL Syntax Reference](/dbms/reference/sql/syntax/) as the authoritative source for syntax
and options rather than duplicating them here.

- **[Create and drop tables](#create-delete)**
- **[Alter tables](#alter)**
- **[Choose columns and data types](#selection-type-column-data-types)**
- **[Constraints and defaults](#constraints-defaults-condition)**
- **[Index design](#index-create-delete)**
- **[View design](#create-view)**

<a id="create-delete"></a>

## Create and drop tables

First complete [Table Type Selection](../table-types-selection-type/). Then define table
names, columns, keys, constraints, indexes, and views for the selected type.

### Row granularity and column roles

Keep row granularity consistent within a table. Mixing daily equipment summaries and
second-level raw data as equivalent rows makes `COUNT` and `AVG` hard to interpret. Define
clear row granularity and query names for raw data and aggregates separately.

| Column role | Example | Design principle |
|---|---|---|
| Target identity | `sensor_id`, `equipment_id` | Use stable values separate from display names |
| Event timing | `measured_at`, `event_time` | Specify whether this is event time or arrival time |
| Measurement | `temperature_c`, `pressure_kpa` | Define units, valid ranges, and correction methods |
| Quality | `quality_code` | Distinguish missing values, measurement failures, and valid zero |
| Reference attributes | Location, equipment type | Decide between tag metadata and a separate reference table |

An existing business identifier, such as an external equipment code, is a natural key; a
separately assigned number is a surrogate key. If codes can change or be reused by different
sources, define their identity scope or consider a surrogate key. An auto-increment number
provides generation order; it does not automatically guarantee event time or duplicate-free
ingestion. A TAG name identifies a tag, not an individual measurement row.

Use table names that begin with a letter and contain letters, digits, and underscores. Avoid
reserved words and names that resemble system objects. Before dropping a table, check
dependent views, indexes, ROLLUPs, and retention policies.

For creation examples by type, see:

- [Create TAG Tables](/dbms/tag-table-usage/create-alter-drop/)
- [Create LOG Tables](/dbms/log-table-usage/create-alter-drop/)
- [TRANSACTION Tables](/dbms/rdb-table-usage/)
- [LOOKUP Tables](/dbms/lookup-table-usage/)
- [VOLATILE Tables](/dbms/volatile-table-usage/)

<a id="alter"></a>

## Alter tables

Support for adding, dropping, renaming, and changing column types depends on the table type
and whether data exists. Before changing a production table, proceed in this order:

1. Check that the edition and table type support the intended `ALTER TABLE` operation.
2. Check dependencies on existing data, indexes, views, and application column order.
3. Measure execution time and locking effects with production-equivalent schemas and data volume.
4. If rollback is difficult, create a new table, validate it, and then switch over.

After adding a column, query both existing and newly inserted rows to check NULL and DEFAULT
behavior. Not all table types backfill existing rows with DEFAULT. Existing VOLATILE rows
and automatically registered TAG metadata rows, for example, have separate rules. Check the
actual type's DDL contract, including
[ARRAY DEFAULT Rules](/dbms/reference/sql/types/array/#default와-기존-row).

Also define application deployment and schema change order. Specify column lists where the
ingestion path supports them, and compare positional Append and binding code with the new
schema. For migration to a new table, compare per-key counts, time ranges, NULL rates, and
representative aggregates as well as total rows. Define how to prevent missing or duplicate
rows arriving during the switch.

For exact support and syntax, see the [ALTER TABLE Reference](/dbms/reference/sql/syntax/)
and [Support by Table Type](/dbms/reference/support-scope-constraints/table-types-type/).

<a id="selection-type-column-data-types"></a>

## Choose columns and data types

Choose the smallest suitable type based on actual value ranges and operations. Distinguish
display formats from storage types.

| Data | Types to consider | Considerations |
| --- | --- | --- |
| Integer measurements and codes | `SHORT`, `INTEGER`, `LONG` families | Check reserved NULL values and ranges |
| Floating-point measurements | `FLOAT`, `DOUBLE` | Check precision, aggregate error, and reserved NULL values |
| Values requiring exact decimal arithmetic | `DECIMAL` | Define precision, scale, and rounding rules first |
| Timestamps | `DATETIME` | Design representable ranges and time zones with client/session policies |
| Short strings | `VARCHAR` | Check maximum length and encoding |
| Long text | `TEXT` | Check table support, sorting/aggregation restrictions, and index cost |
| Network addresses | `IPV4`, `IPV6` | Consider address types instead of strings |
| Structured documents | `JSON` | Check size limits, column promotion criteria, and table support |
| Binary data | `BINARY` | Variable or fixed length depends on table type |
| Fixed-size numeric collections | Numeric `ARRAY` | Distinguish element type/length, element NULLs, and whole-array NULL |

`VARCHAR(n)` measures bytes, which may differ from character counts for Korean text or emoji.
Integer types reserve some boundary values for NULL, so do not assume general-purpose
programming-language integer ranges. FLOAT and DOUBLE also recognize their positive maximum
values as NULL. Valid ranges and operation semantics take priority over choosing a small type.

### Exact decimal values: DECIMAL

Use `DECIMAL` when decimal accuracy matters, such as monetary amounts, tax rates, and
settlement values. Use `FLOAT` or `DOUBLE` for measurements that tolerate approximation and
need a wide exponent range. The distinction is semantic, not just storage size: choose
DECIMAL when rounded results directly drive business rules.

Define the following first:

| Decision | Rule |
|---|---|
| precision | Total significant digits, 1–65 |
| scale | Fractional digits, 0–30; cannot exceed precision |
| Omitted parameters | `DECIMAL` means `DECIMAL(10,0)`; `DECIMAL(M)` means `DECIMAL(M,0)` |

Input with more fractional digits than scale is rounded to the nearest value, with ties
away from zero. Rounding is final at storage time, so verify that it matches business rules.
Values exceeding precision produce an error rather than being truncated or converted to
floating point. Allow sufficient digits.

`SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, `ORDER BY`, and `DISTINCT` use exact processing.
Operations without an exact DECIMAL path, such as percentiles or advanced statistics, convert
to DOUBLE and return approximate results. Distinguish exact aggregates from informational statistics.

Passing a value through floating point in the application loses accuracy regardless of the
storage type. Use decimal representations or strings: JDBC `BigDecimal`, Python
`decimal.Decimal`, or ODBC `SQL_NUMERIC`. For declarations, indexes, and client mappings, see
[DECIMAL and NUMERIC Fixed-Point Types](/dbms/reference/sql/types/decimal-numeric-fixed-point/).

### Structured documents: JSON

Use `JSON` for supplementary attributes whose keys vary by source or grow over time; fields
can be added without schema changes. Promote values frequently used in `WHERE` or `GROUP BY`
to separate columns. JSON columns cannot be primary keys, and LOOKUP does not support JSON
path indexes.

Account for size limits: a document is at most 32,768 bytes, and a JSON path is at most
512 bytes. Use JSON for attributes needed by queries rather than entire raw payloads.

| Table type | JSON column | Considerations |
|---|:---:|---|
| TAG, LOG, TRANSACTION | Yes | JSON functions and path queries supported |
| LOOKUP | Yes | Supported as an ordinary column; JSON path indexes unsupported |
| VOLATILE | No | JSON columns cannot be created |

Use `->` and `JSON_EXTRACT_*` for queries, and the `JSON_SET` family for changes. Mutation
functions are useful only when the table type supports `UPDATE`; for tables without row
updates, such as LOG or TAG, construct the document at ingestion time. For function support,
see [JSON Support by Table Type](/dbms/reference/sql/types/table-types-type-support-scope-json/).

### Restrictions to check before choosing a type

| Type | Design considerations |
|---|---|
| `TEXT` | Supported only in LOG and Standard Edition TRANSACTION. LOG TEXT columns cannot be used in `ORDER BY` or `GROUP BY`, or converted to VARCHAR with `MODIFY COLUMN`. Store sortable or aggregatable values separately as VARCHAR or numeric columns. |
| `BINARY` | LOG supports variable-length values up to 64MB; TAG uses fixed-length `BINARY(n)` of 1–32,767 bytes. LOOKUP and VOLATILE do not support it. |
| `DATETIME` | Represents 1970-01-01 through 2262-04-11 with nanosecond precision. Do not use arbitrary far-future dates to mean expiration or no expiration. |
| `ARRAY` | Fixed-length, one-dimensional numeric arrays with cardinality 1–1024. Distinguish whole-array NULL from element NULL. |

For complete ranges and table support, use the [Data Type Reference](/dbms/reference/sql/types/).

<a id="constraints-defaults-condition"></a>

## Constraints and defaults

`PRIMARY KEY`, `NOT NULL`, and `DEFAULT` support differs by table type. A TAG `PRIMARY KEY`
identifies a tag; LOOKUP, VOLATILE, and TRANSACTION `PRIMARY KEY` columns determine row identity
and update access paths.

NULL represents an unknown or absent value, unlike zero or an empty time range. Replacing
measurement failures with DEFAULT 0 can distort averages and validity checks. `COUNT(*)`
counts rows; `COUNT(value)` counts rows where that column is non-NULL. Distinguish them when
reporting sample counts.

Defaults define behavior for omitted inputs; they do not replace validation. Validate
constraints unsupported by a table in ingestion or business applications. Do not assume
support for constraints such as foreign keys merely because another DBMS provides them.
Check [TRANSACTION Support](/dbms/reference/support-scope-constraints/rdb/).

Do not use system columns such as `_ARRIVAL_TIME` or `_RID` as application business keys.
Reference them only for documented query semantics, without depending on their storage
structure or generation mechanism.

<a id="index-create-delete"></a>

## Index design

Indexes reduce query costs but add ingestion and storage costs.

First list representative queries and check predicate selectivity, the proportion of matching
rows. A monthly average across all equipment differs from a specific order lookup for one
device. Instead of indexing every filter or join column, compare `EXPLAIN` and actual
execution times, then retain useful indexes.

- Do not start with extra indexes when tag and time-range access is sufficient for TAG queries.
- For frequently filtered LOG columns, measure plans and selectivity before adding indexes.
- Design LOOKUP, VOLATILE, and TRANSACTION indexes around key lookups and joins.
- For word searches in long text, consider `KEYWORD` indexes supported by the table type.

For creation/deletion syntax and supported types, see the
[Index SQL Reference](/dbms/reference/sql/syntax/).

<a id="create-view"></a>

## View design

A view names a reusable query but does not store its results. Avoid unintended fixed time
ranges or unnecessary all-column reads in view definitions. Check dependent views before
changing base tables or columns.

Views can consistently expose frequently used columns and unit conversions. Creating a
view alone does not copy data or reduce query cost. A view joining historical events to
current reference data can change historical results when the reference data changes.
For attributes as they were at event time, use versioned reference data or attributes
recorded with the original event.

For view creation, querying, deletion, and restrictions, see the
[VIEW SQL Reference](/dbms/reference/sql/syntax/).
