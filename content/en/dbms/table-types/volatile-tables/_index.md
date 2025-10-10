---
title: 'Volatile Tables'
weight: 30
---

Complete reference for Volatile tables - Machbase's in-memory table type for real-time, frequently-updated data.

## Overview

Volatile tables store all data in memory for maximum speed. They support UPDATE and DELETE operations by primary key, making them ideal for real-time dashboards and session management.

## Key Features

- **100% in-memory** storage
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

## When NOT to Use

- Data that must persist
- High-volume streaming data (use Tag/Log instead)
- Large datasets (limited by RAM)

## Related Documentation

- [Tutorial: Real-time Analytics](../../tutorials/realtime-analytics/)
- [Core Concepts: Table Types](../../core-concepts/table-types-overview/)
- Original reference: [Volatile Tables](../../../dbms/feature-table/volatile/)
