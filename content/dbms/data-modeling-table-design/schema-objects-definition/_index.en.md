---
type: docs
title: '4.2 Schema Object Definition'
weight: 20
toc: true
---



<a id="create-delete"></a>

## Create and drop tables

Complete [table-type selection](../table-types-selection-type/) first, then define names, columns,
keys, constraints, indexes, and views. Use names that distinguish application objects from system
objects and reserved words. Before dropping a table, check dependent views, indexes, rollups, and
retention policies.

### Row grain and column roles

Keep one meaning for a row within a table. Mixing daily summaries and individual observations as
equivalent rows makes COUNT and AVG difficult to interpret. Give raw and aggregate tables explicit
row grains and query names.

| Role | Example | Design decision |
|---|---|---|
| Entity identifier | `sensor_id`, `equipment_id` | Stable value separate from a display name |
| Event reference | `measured_at`, `event_time` | Measurement/event time versus receipt time |
| Measurement | `temperature_c`, `pressure_kpa` | Unit, valid range, and correction policy |
| Quality | `quality_code` | Missing value, failed measurement, and valid zero |
| Reference attribute | Location, equipment class | Tag metadata versus a separate reference table |

A natural key comes from the business domain; a surrogate key is a separately issued identifier.
If device codes can change or repeat across sites, define their scope or consider a surrogate key.
An automatically generated number does not establish event-time order or prevent duplicate
ingestion. A TAG primary key identifies a tag, not each measurement row.

See the [TAG](../../tag-table-usage/create-alter-drop/),
[LOG](../../log-table-usage/create-alter-drop/), [TRANSACTION](../../rdb-table-usage/),
[LOOKUP](../../lookup-table-usage/), and [VOLATILE](../../volatile-table-usage/) chapters for DDL examples.

<a id="alter"></a>

## Evolve the schema

Column addition, removal, renaming, and type changes have different support constraints.

1. Check the Edition, table type, and DATA/METADATA area against the requested ALTER operation.
2. Find dependencies in existing rows, indexes, views, applications, and positional bindings.
3. Measure execution time and locking effects on representative data in a test environment.
4. If the change is hard to reverse, consider a new table, validated migration, and controlled cutover.

Query both existing and newly inserted rows after adding a column. DEFAULT does not backfill every
table identically: VOLATILE existing rows and automatically registered TAG metadata have specific
rules. Check the [ADD COLUMN rules (Korean)](/kr/dbms/reference/sql/syntax-dictionary-sql/ddl-syntax/#add-column)
and the relevant type's DDL contract rather than assuming generic SQL behavior.

Coordinate application deployment with schema changes. Specify input columns where supported and
review Append or binding code that depends on column order. During migration, compare key-level
counts, time ranges, NULL proportions, and representative aggregates, not just total row counts.
Plan how to handle rows arriving during cutover so they are neither lost nor duplicated.

See [DDL syntax](../../reference/sql/syntax-dictionary-sql/ddl-syntax/) for exact support.

<a id="selection-type-column-data-types"></a>

## Select columns and data types

Choose types from valid ranges and required operations before minimizing storage size.

| Data | Type to consider | Check |
|---|---|---|
| Integer measurements or codes | SHORT/INTEGER/LONG families | Reserved NULL values and range |
| Approximate measurements | FLOAT/DOUBLE | Precision and aggregation error |
| Exact decimal values | DECIMAL | Precision, scale, and rounding |
| Instants | DATETIME | Input/output time zone and clock accuracy |
| Strings | VARCHAR or TEXT | Byte length and search requirements |
| Network addresses | IPV4/IPV6 | Address rather than string operations |
| Structured attributes | JSON | Table support, functions, and size limits |
| Binary values | BINARY | Table-specific length rules |
| Fixed numeric tuples | Numeric ARRAY | Element type/count; whole versus element NULL |

VARCHAR length is in bytes, not characters. Integer types reserve boundary values for NULL, so their
usable range differs from similarly sized programming-language integers. Use DECIMAL for amounts
requiring exact decimal representation within the declared precision and scale. Consult the
[data type dictionary](../../reference/sql/type-data-types-dictionary/) for limits and table support.

<a id="constraints-defaults-condition"></a>

## Constraints and defaults

PRIMARY KEY, NOT NULL, and DEFAULT support varies by table type. TAG's key identifies a tag;
LOOKUP, VOLATILE, and TRANSACTION keys identify rows and influence mutation paths. Do not use
internal system-column structure or `_arrival_time` as a permanent business key.

NULL represents an unknown or absent value, not zero. A missing interval may contain no row at all.
Replacing failed measurements with DEFAULT 0 can distort averages and quality checks. COUNT(*)
counts rows, while COUNT(value) counts rows with non-NULL values in that column.

A default defines omitted input; it does not replace validation. Validate constraints that the
chosen table does not enforce in the application. In particular, do not assume foreign-key or other
RDBMS features are supported; consult [TRANSACTION support](../../reference/support-scope-constraints/rdb/).

<a id="index-create-delete"></a>

## Design indexes

Write representative queries first. An index can reduce access costs when predicates select a small
part of the table, but maintaining it adds storage and write work. Compare EXPLAIN and measured
execution times before keeping an index.

- TAG queries already addressed by tag and axis may not need another index.
- For LOG, test indexes on frequently filtered columns; word searches use supported KEYWORD indexes.
- For LOOKUP, VOLATILE, and TRANSACTION, start from key lookups and join predicates.
- Match join-key types and review filtered row counts, not only total table sizes.

See [index syntax](../../reference/sql/syntax-dictionary-sql/index-syntax/) for allowed forms.

<a id="create-view"></a>

## Design views

A view names a reusable query; it does not store its result or automatically make the query faster.
Use explicit columns and clear time conditions. Review dependencies before changing base tables.

Views can centralize column lists or unit conversions. However, a view joining historical events to
the current master data will show changed master attributes for old events too. If attributes at
event time matter, model versioned reference data or retain those attributes in the original row.
See [VIEW syntax](../../reference/sql/syntax-dictionary-sql/view-syntax/) for constraints.
