---
type: docs
title: '16.1 SQL Reference'
weight: 10
toc: true
---

Precise definitions of SQL syntax, functions, data types, query hints, and relative time expressions.

## Subsections

| Section | Description |
|------|------|
| [SQL Syntax Dictionary](./syntax/) | BNF syntax and examples for CREATE, DROP, ALTER, SELECT, WITH/CTE, INSERT, DELETE, UPDATE, BACKUP, MOUNT, and other statements |
| [Function Dictionary](./functions/) | Aggregate, mathematical, string, date/time, type conversion, and TAG-specific functions |
| [Data Type Dictionary](./types/) | Sizes, ranges, defaults, and availability by table type |
| [SELECT Hint Syntax](./syntax/select-hint-syntax/) | SELECT hint syntax, usage, and applicable targets |
| [Relative Time Expressions](./relative-time/) | Relative time literals such as `now - 1h` and their suffixes |
| [ROWID](./rowid/) | ROWID meaning, predicates, and INSERT results by table type |

## SQL Features

Based on ANSI SQL, with extensions optimized for time-series processing.

- **TAG time-series features**: BASETIME, METADATA, `FIRST`/`LAST`, `SERIES BY`, ROLLUP
- **Time-range queries**: `DURATION`, `BEFORE`, `AFTER`, and `RANGE` clauses
- **Common table expressions**: Nonrecursive `WITH`/CTE in Standard Edition
- **Bulk ingestion integration**: Client SDK Append APIs (separate ingestion APIs, not SQL statements)
- **Text search**: `SEARCH`, `ESEARCH`, and `REGEXP` operators
- **Set operations**: `UNION ALL` (UNION, INTERSECT, and EXCEPT are not supported)
