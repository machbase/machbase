---
type: docs
title: '5. Using TAG Tables'
weight: 50
toc: true
---

TAG tables store measurement histories by repeatedly observed entity name
and a time or distance axis. This chapter covers Machbase DBMS 8.7.0
TAG structure, ingestion, queries, metadata, correction, and operations.
It validates the deployment and data-model choices from Chapters 3 and 4
through practical SQL.

A tag is an observed entity; a DATA row is one observation. METADATA holds
one attribute row per tag, not separate attributes per historical
observation. Distinguish original measurements, current attributes,
interval aggregates, and ingestion times to interpret results and
correction scope consistently.

## Chapter Contents

| Section | Content |
|---|---|
| [Overview and Selection Criteria](./overview-use-criteria/) | Tag identifiers, observation rows, time/distance axes |
| [Table Structure and Schema](./table-structure-schema/) | Column order/types, LSL/USL, BINARY, storage design |
| [Create, Alter, and Drop](./create-alter-drop/) | Basic DDL, METADATA expansion, object cleanup |
| [Data Ingestion and Changes](./data-input-mutation/) | Automatic registration, SQL/Append/file input |
| [Queries and Analysis](./query-analysis/) | Range/latest-value/STAT queries and interpretation |
| [Indexes and Performance](./index-performance/) | Validate access paths with actual data |
| [Operations and Data Lifecycle](./operations-lifecycle/) | Deletion, retention, deduplication completion |
| [Constraints, Errors, and Troubleshooting](./constraints-errors-troubleshooting/) | Valid conditions and intentional failure examples |
| [Usage Patterns and Scenarios](./patterns-scenarios/) | Observation granularity, units, missing-data models |
| [TAG Metadata](./tag-metadata/) | Registration, queries, changes, deletion, JSON, ARRAY |
| [TAG Data UPDATE and Correction](./tag-data-update-correction/) | Direct correction, NULL correction, audit history |
| [tagmetaimport and Bulk Metadata Registration](./tagmetaimport/) | CSV setup, input targets, rerun errors |

## Exercises and Support Scope

Each page is an independent exercise. If a setup table exists, determine
whether it belongs to another workload; do not delete it arbitrarily.
Run success examples separately from intentional failures. Apply cleanup
SQL only to objects created for that exercise.

TAG DATA UPDATE is Standard Edition only. Check Edition-specific scope
for duplicate-check intervals, METADATA ALTER, and individual LSL/USL
operations. SQL INSERT, Append responses, storage-buffer flush, and
index/statistics completion are different events.

[Chapter 6](../tag-rollup-usage/) covers full ROLLUP creation, query, and
rebuild procedures. This chapter addresses only how TAG corrections and
deletions relate to aggregates.
