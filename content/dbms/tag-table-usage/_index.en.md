---
title: '5. TAG Table Usage'
weight: 50
toc: true
---

TAG tables store observations identified by a recurring subject's name and a time or distance axis.
This chapter covers Machbase DBMS 8.7.0 TAG structure, ingestion, queries, metadata, corrections,
and operations. It applies the deployment and modeling decisions from Chapters 3 and 4 to SQL.

A tag identifies a subject; a DATA row represents one observation. METADATA stores one attribute
row per tag, not a separate attribute snapshot for each historical observation. Distinguish raw
measurements, current attributes, interval aggregates, and ingestion time when interpreting results.

## Contents

| Section | Purpose |
|---|---|
| [Overview and Usage Criteria](./overview-use-criteria/) | Tag identity, observation rows, and axis selection |
| [Table Structure and Schema](./table-structure-schema/) | Column order/types, LSL/USL, BINARY, and storage |
| [Create, Alter, and Drop](./create-alter-drop/) | DDL, metadata extension, and cleanup |
| [Data Input and Mutation](./data-input-mutation/) | Automatic registration and SQL/Append/file input |
| [Query and Analysis](./query-analysis/) | Ranges, latest values, and STAT interpretation |
| [Indexes and Performance](./index-performance/) | Inspect access paths with actual data |
| [Operations and Data Lifecycle](./operations-lifecycle/) | Deletion, retention, and duplicate-removal completion |
| [Constraints and Troubleshooting](./constraints-errors-troubleshooting/) | Valid conditions and intentional failures |
| [Patterns and Scenarios](./patterns-scenarios/) | Observation granularity, units, and missing data |
| [TAG Metadata](./tag-metadata/) | Registration, CRUD, JSON, and ARRAY |
| [TAG Data Corrections](./tag-data-update-correction/) | Direct correction, NULL corrections, and audit history |
| [Bulk Metadata Import](./tagmetaimport/) | CSV preparation, target selection, and reimport errors |

## Exercises and Support Scope

Each page is an independent exercise. If a setup table already exists, identify its owner and
purpose rather than dropping it blindly. Run successful and intentionally failing examples
separately; cleanup applies only to objects created for that exercise.

TAG DATA UPDATE is a Standard Edition feature. Check Edition-specific scope for duplicate-check
periods, METADATA ALTER, and individual LSL/USL operations. SQL INSERT, Append acknowledgements,
storage flush, and completion of index/statistics processing have different meanings.

[Chapter 6](../tag-rollup-usage/) covers ROLLUP creation, queries, and rebuilding. This chapter
explains its relationship to TAG corrections and deletion.
