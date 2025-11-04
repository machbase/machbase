---
type: docs
title: 'Log Tables'
weight: 20
---

Complete reference for Log tables - Machbase's flexible table type for event streams, application logs, and time-stamped data.

## Overview

Log tables are optimized for append-only event data with flexible schemas. They automatically add nanosecond-precision timestamps and support full-text search.

## Key Features

- **Millions of inserts per second**
- **Automatic _arrival_time** column (nanosecond precision)
- **Flexible schema** (any columns)
- **Full-text search** with SEARCH keyword
- **Newest data first** (automatic ordering)
- **Optional LSM indexing**

## Basic Syntax

```sql
CREATE TABLE table_name (
    column1 data_type,
    column2 data_type,
    ...
);
-- _arrival_time automatically added
```

## When to Use

- Application logs
- HTTP access logs
- Event streams
- Transaction logs
- Any time-stamped event data

## Related Documentation

- [Tutorial: Application Logs](../../tutorials/application-logs/)
- [Core Concepts: Table Types](../../core-concepts/table-types-overview/)
- Original reference: [Log Tables](../../../dbms/feature-table/log/)
