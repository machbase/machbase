---
type: docs
title: '2.2 Storage and Execution Architecture'
weight: 20
toc: true
---

This page explains storage and execution principles. Schema and index decisions belong to Chapter 4
and measured tuning belongs to Chapter 12.

<a id="architecture-machbase"></a>

## Architecture overview

Standard Edition runs one database server. Cluster Edition separates coordination, deployment,
routing, reference-data, and warehouse roles. Use the Edition and deployment chapters for supported
topologies and procedures.

<a id="storage-columnar-compression-column"></a>

## Columnar storage and compression

Time-series storage groups similar column values and partitions data by time so range queries can
avoid unrelated data. This differs from row-oriented relational storage used for mutable business
records.

<a id="indexing-basics"></a>

## Indexing principles

| Category | Principle |
|---|---|
| TAG | Restrict time-series partitions by tag and axis |
| LOG | Use arrival-time access and verified search indexes when needed |
| TRANSACTION | Use primary, unique, and general indexes for relational keys |
| LOOKUP and VOLATILE | Use memory-resident keys and supported secondary indexes |

See [Schema objects](/dbms/data-modeling-table-design/schema-objects-definition/) for design and
[Index tuning](/dbms/performance-tuning/index-tuning/) for measurement.

<a id="execution-concepts-plan-cache"></a>

## Cache and execution plans

Parsing, optimization, storage access, and result production form the query path. Plan, PVO, and
Min-Max caches address different costs. Their properties and defaults belong to
[Cache and memory tuning](/dbms/performance-tuning/cache-tuning-memory/).
