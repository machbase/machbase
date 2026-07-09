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
