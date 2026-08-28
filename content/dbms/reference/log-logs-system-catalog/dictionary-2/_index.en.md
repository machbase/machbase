---
type: docs
title: '17.3.2 Virtual Table Dictionary'
weight: 20
toc: true
---

Virtual tables are read-only runtime views. Global views use fixed names such as
`V$SESSION`, `V$STMT`, and `V$PROPERTY`.

TAG tables additionally create a table-specific `V$<TABLE>_STAT` view. Because its
schema depends on the TAG axis, see
[Per-tag statistics view](/dbms/tag-table-usage/query-analysis/#tag-stat-axis-schema) for
the BASE TIME and BASE DISTANCE column contracts.
