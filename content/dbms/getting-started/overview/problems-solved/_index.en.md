---
type: docs
title: '1.1.2 Problems Machbase Solves'
weight: 20
toc: true
---

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
