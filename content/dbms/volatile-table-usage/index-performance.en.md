---
type: docs
title: '10.6 Indexes and Performance'
weight: 60
toc: true
aliases:
  - /dbms/volatile-table-usage/red-black-index/
---

This section explains how to create and choose indexes for VOLATILE tables.

<a id="original-85-volatile-indexes"></a>
<a id="index-strategy-red-black"></a>

## Supported Indexes

Declaring a `PRIMARY KEY` creates an index for key lookups. You can add `REDBLACK` indexes to
ordinary columns. VOLATILE tables do not support `BITMAP` or `KEYWORD` indexes.

Run the following example in order from table creation through cleanup.

```sql
CREATE VOLATILE TABLE ch10_index (
    id       INTEGER PRIMARY KEY,
    name     VARCHAR(20),
    status   VARCHAR(16)
);

CREATE INDEX ch10_index_name_idx
ON ch10_index(name) INDEX_TYPE REDBLACK;

INSERT INTO ch10_index VALUES (1, 'west device', 'ACTIVE');
INSERT INTO ch10_index VALUES (2, 'east device', 'INACTIVE');

SELECT id, name
FROM ch10_index
WHERE name = 'west device';

DROP INDEX ch10_index_name_idx;
DROP TABLE ch10_index;
```

## Design Criteria

- Use a `PRIMARY KEY` for single-row key lookups and updates.
- Add secondary indexes only for repeated equality or range predicates on ordinary columns.
- Indexes consume memory as well as data. Remove unnecessary indexes.
- Compare response time and memory usage before and after creating indexes, using actual query predicates and row counts.

For syntax details, see [Index Syntax](/dbms/reference/sql/syntax/index-syntax/).
