---
type: docs
title: '1.1 Machbase DBMS Overview'
weight: 10
toc: true
---
Machbase DBMS is a time-series database for processing data that continuously arrives
in time order, such as industrial IoT data and financial tick data. When sensor values
arrive like a factory conveyor belt, or market prices and volumes change in short
intervals, the first design question is where to store that data. In Machbase DBMS,
that starts with choosing a table type that matches the shape and lifecycle of the
data.

Time-series data usually appears in two shapes. The first is regular measurement data,
such as a sensor reporting temperature every second. The second is irregular event
data, such as an order execution, alert, log record, or received tick. Real systems
usually contain both. In industrial IoT, temperature and vibration are measurements,
while alarms and maintenance records are events. In finance, quote and trade ticks
arrive rapidly, while receive status and processing delays remain as events.

## Table Types to Separate First

| Table | Main use | First selection rule |
| --- | --- | --- |
| LOG | Append-heavy events, logs, and histories | Use it for high-volume records such as industrial equipment events or financial tick receive histories that are frequently queried by time. |
| TAG | Sensor, equipment, and measurement values with tag names and time | Use it when queries are centered on tag-based time series and aggregation. |
| LOOKUP | Codes, equipment metadata, and mapping data | Use it for small reference data that must be joined or looked up quickly. |
| RDB | Relational business data, state data, and larger reference or dimension data | In Standard Edition versions that support RDB, create it with `CREATE RDB TABLE`; it supports row-level `INSERT`, `UPDATE`, `DELETE`, and joins with other table types. |
| VOLATILE | Temporary session data | Use it for in-memory data that may disappear when the server stops. |

LOG and TAG are append-oriented tables for high-volume time-series ingest. If no table
type keyword is specified, `CREATE TABLE` creates a LOG table for backward
compatibility. Versions that support TAG data UPDATE can correct values by narrowing
the target range with tag names, time predicates, and data-column predicates. Do not
read this as a general row update that changes the TAG name, time axis, or system
columns. If general row-level updates are central to the workload, read the RDB,
LOOKUP, or VOLATILE documents first. RDB is a Standard Edition v1 feature in 8.6;
Cluster Edition does not support creating RDB tables.

Think of table types as storage areas with different roles. A LOG table receives
records that keep piling up, while a TAG table organizes values by tag name and time
axis. For example, an equipment temperature value naturally fits a TAG table, while an
event saying that a tick was received fits a LOG table. Small reference data belongs
in LOOKUP, and relational business data with important relationships and constraints
belongs in an RDB table. RDB tables are covered in a later chapter.

When designing a time-series system, also think about the lifecycle of the data.
Recent raw data often needs high resolution and fast queries, while older data is
often useful as summarized data. Retention, rollup, downsampling, and compression are
therefore not secondary details; they directly affect operating cost and query
performance.

After this overview, run the representative LOG-table workflow in
[10-Minute Quick Start](../quick-start/). That single sample verifies that bare
`CREATE TABLE` creates a LOG table and that create, insert, query, and cleanup work
together.


<a id="introduction"></a>

## Introduction to Machbase DBMS

Machbase DBMS is a time-series database designed to process time-series data such as
industrial IoT data and financial tick data as quickly and conveniently as possible.
Users still create tables and query data with SQL, but ingestion, storage, and query
behavior depend on the table type.

Traditional business data is often centered on finding and updating individual
records or joining business tables. Time-series data is different: it is usually
append-heavy, queried by time range, and interpreted through aggregations such as
average, maximum, minimum, and sum. Typical questions include "how did temperature
change during the last 10 minutes," "how many ticks arrived near market close," and
"which hours had the most equipment alarms last month."

### Core View

- Start with a LOG table when data continuously arrives, such as application logs,
  event histories, equipment status records, or financial tick receive logs.
- Start with a TAG table when the data clearly has tag name, time, and value columns.
- Start with LOOKUP for small, read-heavy reference data.
- Read the RDB-oriented documents for relational business entities and reference data
  where updates and relationships matter. In Standard Edition versions that support
  RDB, create RDB tables with `CREATE RDB TABLE`.
- Use VOLATILE tables for temporary working data.

This point of view matters when learning Machbase. The basic unit is not only "one
current value," but a flow of values over time. When designing a schema, consider
ingest rate, time predicates, aggregation interval, retention period, and reference
data relationships together.

You do not need to create every table type at the beginning. Run the LOG-table sample
in [10-Minute Quick Start](/dbms/getting-started/quick-start/) first, then move to the TAG, LOOKUP,
RDB, or VOLATILE documents according to your data. If `SHOW TABLES` later displays
`KEYVALUE` tables whose names start with `_TAG_DATA_`, treat them as DBMS-managed
internal tables for TAG data, not as a first design choice.

<a id="problems-solved"></a>

## Problems Machbase Solves

Machbase DBMS is most useful when data keeps flowing in rather than quietly sitting
still. Examples include factory equipment status, application access logs, urban
infrastructure sensor values, and financial market ticks. This data must not only be
stored, but also checked immediately and analyzed again later.

A time-series database does more than store a large number of rows. It must keep up
with fast ingest, make recent and historical data searchable by time, and support an
operational strategy for long-term storage. As raw data ages, systems often summarize
it or apply retention rules so storage growth remains manageable.

Machbase DBMS is useful when the following requirements appear together:

- Devices, sensors, applications, or market data feeds continuously generate data at
  sub-second or second-level intervals.
- Recent data must be queried immediately, while older data must remain available for
  long-term analysis.
- Ingestion performance, SQL, aggregation, joins, and retention policies must work
  together.
- Raw time-series data and reference data must be managed in the same system.
- Sub-second or millisecond raw data and minute, hour, or day-level aggregates often
  need to coexist.

Table types are the interface for separating these problems. LOG handles append-heavy
raw events, TAG handles tag-based measurements, and LOOKUP/RDB handles reference data.

This separation clarifies both ingest paths and query patterns. Raw events can be
appended quickly, tag measurements can be found by tag name and time, and reference
data can be used for joins and interpretation. The value of a time-series system
appears when these parts work together.

The representative sample in this chapter checks only the smallest version of the
problem: store one event and read it back. Real designs start by deciding whether the
data is an event, a tag-based measurement, or reference data, then moving to the
corresponding table-type document.
