---
type: docs
title: 'Volatile Tables'
weight: 30
---

Complete reference for Volatile tables - Machbase's non-persistent memory primary-key table type.

## Overview

Volatile tables store all data in memory and do not persist rows across server restart.
Each Volatile table has a single primary-key memory index, and `UPDATE`, `DELETE`,
and point lookup operations are designed around that primary key.

## Key Features

- **100% in-memory** storage
- **Non-persistent** rows
- **Single primary-key memory index**
- **UPDATE and DELETE** by PRIMARY KEY
- **10,000s of operations** per second
- **Fast key-based lookups** (O(log n))
- **WARNING: Data lost on shutdown**

## Basic Syntax

```sql
CREATE VOLATILE TABLE table_name (
    key_column data_type PRIMARY KEY,
    column1 data_type,
    column2 data_type,
    ...
);
```

## When to Use

- Real-time dashboards
- User sessions
- Live status boards
- Caching layer
- Temporary calculations
- Non-persistent key-value style state

## When NOT to Use

- Data that must persist
- High-volume streaming data (use Tag/Log instead)
- Large datasets (limited by RAM)

## Related Documentation

- [Insert and Update Data](./insert-update/)
- [Core Concepts: Table Types](../../core-concepts/table-types-overview/)
