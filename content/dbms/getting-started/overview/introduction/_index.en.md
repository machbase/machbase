---
type: docs
title: '1.1.1 Introduction to Machbase DBMS'
weight: 10
toc: true
---

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

## Core View

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
in [10-Minute Quick Start](../../quick-start/) first, then move to the TAG, LOOKUP,
RDB, or VOLATILE documents according to your data. If `SHOW TABLES` later displays
`KEYVALUE` tables whose names start with `_TAG_DATA_`, treat them as DBMS-managed
internal tables for TAG data, not as a first design choice.
