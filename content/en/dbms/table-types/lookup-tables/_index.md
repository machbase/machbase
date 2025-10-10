---
type: docs
title: 'Lookup Tables'
weight: 40
---

Complete reference for Lookup tables - Machbase's table type for reference data, master data, and dimension tables.

## Overview

Lookup tables are disk-based tables optimized for reference data that changes rarely but is frequently read. They support full CRUD operations and are ideal for device registries and configuration.

## Key Features

- **Full CRUD support** (INSERT, UPDATE, DELETE, SELECT)
- **Persistent disk storage**
- **Fast reads**
- **JOIN with time-series tables**
- **Optional LSM indexing**

## Basic Syntax

```sql
CREATE LOOKUP TABLE table_name (
    column1 data_type,
    column2 data_type,
    ...
);
```

## When to Use

- Device registries
- Configuration tables
- Category/dimension tables
- Master data
- Reference data that changes rarely

## When NOT to Use

- High-frequency inserts (use Tag/Log instead)
- Time-series data
- Data requiring millions of writes/second

## Related Documentation

- [Tutorial: Reference Data](../../tutorials/reference-data/)
- [Core Concepts: Table Types](../../core-concepts/table-types-overview/)
- Original reference: [Lookup Tables](../../../dbms/feature-table/lookup/)
