---
type: docs
title: '16.3 System Catalog Reference'
weight: 30
toc: true
---

The system catalog is a set of read-only tables for querying Machbase server metadata and current
operational status with SQL. It contains two types of tables.

| Type | Prefix | Description |
|------|--------|------|
| Metadata tables | `M$` | Schema information, including table definitions, columns, indexes, and users |
| Virtual tables (dynamic views) | `V$` | Current operational status, including sessions, running queries, memory, and storage |

## General Rules

- All system catalog tables are **read-only**. `INSERT`, `UPDATE`, and `DELETE` return errors.
- `M$` tables automatically reflect DDL operations (`CREATE`, `ALTER`, and `DROP`).
- `V$` tables reflect live server status and return current values on each query.
- Use the following queries to list all tables.

```sql
-- List all metadata tables
SELECT name FROM m$tables ORDER BY name;

-- List all virtual tables
SELECT name FROM v$tables WHERE name LIKE 'V$%' ORDER BY name;
```

## Subsections

| Section | Description |
|------|------|
| [Metadata Table Dictionary](./meta/) | Schema metadata tables such as M$SYS_TABLES and M$SYS_COLUMNS |
| [Virtual Table Dictionary](./virtual/) | Dynamic views such as V$SESSION, V$STMT, and V$PROPERTY |
| [Per-tag Statistics Views](/dbms/tag-table-usage/query-analysis/#tag-stat-axis-schema) | Time- and distance-axis schemas and queries for `V$<TABLE>_STAT` |
| [V$ROLLUP Dictionary](./vrollup/) | Rollup job status view columns |
| [V$STORAGE_MOUNT_* Dictionary](./vstorage-mount/) | Mounted backup database view columns |
| [Complete Virtual Table Reference](./virtual-table-full/) | All entries from the original 8.5 virtual table reference |
