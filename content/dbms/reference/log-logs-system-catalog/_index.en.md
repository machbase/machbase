---
type: docs
title: '17.3 시스템 카탈로그 레퍼런스'
weight: 30
toc: true
---

System catalogs are read-only tables for querying Machbase metadata and runtime
status through SQL.

| Section | Description |
|---------|-------------|
| [Meta table dictionary](./dictionary/) | Schema metadata tables such as M$SYS_TABLES and M$SYS_COLUMNS |
| [Virtual table dictionary](./dictionary-2/) | Dynamic views such as V$SESSION, V$STMT, and V$PROPERTY |
| [Per-tag statistics view](/dbms/tag-table-usage/query-analysis/#tag-stat-axis-schema) | Axis-specific `V$<TABLE>_STAT` schema and queries |
| [Complete virtual table reference](./virtual-table-full/) | Full virtual table reference preserved from the 8.5 manual |
