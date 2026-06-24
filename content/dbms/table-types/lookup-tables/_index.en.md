---
type: docs
title: 'Lookup Tables'
weight: 40
---

Complete reference for Lookup tables - Machbase's persistent primary-key table type for reference data.

## Overview

Lookup tables store persistent reference data and maintain a single primary-key
memory index. They support full CRUD operations, but queries and row changes should
be designed around the primary key.

## Key Features

- **Full CRUD support** (INSERT, UPDATE, DELETE, SELECT)
- **Persistent data**
- **Single primary-key memory index**
- **Fast primary-key reads**
- **JOIN with time-series tables**

## Basic Syntax

```sql
CREATE LOOKUP TABLE table_name (
    key_column data_type PRIMARY KEY,
    column2 data_type,
    ...
);
```

## When to Use

- Device registries
- Configuration tables
- Category/dimension tables
- Master data
- Reference data accessed by one primary key

## When NOT to Use

- High-frequency inserts (use Tag/Log instead)
- Time-series data
- Data requiring millions of writes/second
- Workloads that need multiple secondary indexes or general predicates (use RDB instead)

## Related Documentation

- [Inserting Lookup Data](./inserting-data/)
- [Core Concepts: Table Types](../../core-concepts/table-types-overview/)
