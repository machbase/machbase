---
type: docs
title: 'Core Concepts'
weight: 40
---

Deep dive into Machbase architecture, design principles, and key concepts. This section helps you understand how Machbase works under the hood and why it's optimized for time-series data.

## In This Section

### [Understanding Time-Series Data](./time-series-data/)

Learn what makes time-series data special and why traditional databases struggle with it:
- Characteristics of time-series workloads
- Write-heavy vs read-heavy patterns
- Why append-only architecture matters
- Time-based partitioning and compression

### [Table Types Overview](./table-types-overview/)

Complete guide to choosing the right table type:
- Detailed comparison of all 4 table types
- Decision flowchart and selection guide
- Performance characteristics
- Common use cases and anti-patterns
- When to use each type

### [Indexing and Performance](./indexing/)

How Machbase achieves high performance:
- Partitioned indexing for Tag tables
- LSM (Log-Structured Merge) indexing
- Automatic index management
- Query optimization strategies
- Understanding rollup statistics

## Who Should Read This

This section is for:
- **Developers** designing Machbase-based applications
- **Architects** planning system architecture
- **DBAs** optimizing performance
- **Data Engineers** implementing data pipelines

## Prerequisites

Before diving into Core Concepts:
- Complete [Getting Started](../getting-started/) section
- Finish at least 2 of the [Tutorials](../tutorials/)
- Have hands-on experience with Machbase

## Learning Path

We recommend reading in this order:

1. **Time-Series Data** - Understand the problem domain
2. **Table Types Overview** - Choose the right tools
3. **Indexing** - Optimize performance

## Quick Reference

### Table Type Decision Guide

```
Is it sensor data (ID, time, value)?
    YES → Tag Table

Is it log/event data?
    YES → Log Table

Need UPDATE/DELETE in memory?
    YES → Volatile Table

Is it reference/master data?
    YES → Lookup Table
```

### Performance Characteristics

| Table Type | Write Speed | Read Speed | UPDATE/DELETE | Storage |
|-----------|------------|-----------|---------------|---------|
| Tag       | Millions/sec | Very Fast | No* | Disk |
| Log       | Millions/sec | Fast | Time-based | Disk |
| Volatile  | 10,000s/sec | Very Fast | By Key | Memory |
| Lookup    | 100s/sec | Fast | By Key | Disk |

*Tag table metadata can be updated

## Key Concepts at a Glance

### Write-Once Architecture

Machbase is optimized for **append-only** data:
- No row-level locking
- Ultra-fast sequential writes
- Data integrity (logs can't be altered)

### Time-Based Partitioning

Data is automatically partitioned by time:
- Efficient time-range queries
- Easy data retention management
- Optimized compression

### Columnar Compression

Data is stored column-by-column:
- 10-100x compression ratios
- Faster analytical queries
- Reduced storage costs

### Automatic Rollup (Tag Tables)

Statistics are generated automatically:
- Per-second, per-minute, per-hour summaries
- MIN, MAX, AVG, SUM, COUNT, SUMSQ
- No manual aggregation needed

## Common Misconceptions

### "I need to create an index for every query"

**False**. Machbase automatically creates optimal indexes:
- Tag tables: 3-level partitioned index
- Log tables: Time-based partitioning (index optional)
- Volatile tables: Red-black tree for PRIMARY KEY
- Most queries work great without manual indexes

### "I should create one table per sensor"

**False**. Use a single Tag table for all sensors:
- Better performance
- Easier management
- Automatic optimization

### "Lookup tables are slow"

**Partially true**. Lookup tables have:
- Slower writes (hundreds/sec vs millions/sec)
- Fast reads (optimized for SELECT)
- Use for reference data, not high-volume inserts

### "Volatile tables are just like regular tables"

**False**. Volatile tables are special:
- 100% in memory
- Data lost on shutdown
- Use for temporary/cache data only

## Design Principles

### 1. Choose the Right Table Type

Don't force a table type for the wrong use case:
- Tag table for sensor data
- Log table for event streams
- Volatile table for real-time cache
- Lookup table for reference data

### 2. Leverage Time-Based Features

Use Machbase's time-aware features:
```sql
-- Good: Use DURATION
SELECT * FROM logs DURATION 1 HOUR;

-- Less optimal: Manual time filtering
SELECT * FROM logs
WHERE _arrival_time >= NOW - INTERVAL '1' HOUR;
```

### 3. Implement Data Retention

Don't let data grow forever:
```sql
-- Daily cleanup
DELETE FROM logs EXCEPT 30 DAYS;
```

### 4. Use Rollup for Analytics

Query pre-aggregated data:
```sql
-- Fast: Use rollup
SELECT * FROM sensors WHERE rollup = hour;

-- Slow: Aggregate raw data
SELECT sensor_id, AVG(value) FROM sensors GROUP BY sensor_id;
```

## Architecture Overview

### Storage Layers

```
┌─────────────────────────────────────┐
│         Query Engine                │
├─────────────────────────────────────┤
│         Memory Manager              │
│  ┌──────────────┐  ┌──────────────┐│
│  │ Volatile     │  │ Query Cache  ││
│  │ Tables       │  │              ││
│  └──────────────┘  └──────────────┘│
├─────────────────────────────────────┤
│         Storage Engine              │
│  ┌──────────────┐  ┌──────────────┐│
│  │ Tag/Log      │  │ Lookup       ││
│  │ Tables       │  │ Tables       ││
│  └──────────────┘  └──────────────┘│
└─────────────────────────────────────┘
```

### Data Flow

```
Sensors/Apps
     ↓
  APPEND API (bulk insert)
     ↓
  Write Buffer (memory)
     ↓
  Flush to Disk (compressed)
     ↓
  Automatic Indexing
     ↓
  Query Engine
```

## Next Steps

Ready to dive deeper?

1. **Start with**: [Understanding Time-Series Data](./time-series-data/)
2. **Then read**: [Table Types Overview](./table-types-overview/)
3. **Finally**: [Indexing and Performance](./indexing/)

Or jump to:
- [Common Tasks](../common-tasks/) - Practical how-to guides
- [Table Types](../table-types/) - Detailed reference for each type
- [SQL Reference](../sql-reference/) - Complete SQL syntax

## Further Reading

- [Advanced Features](../advanced-features/) - STREAM, Rollup configuration
- [Configuration](../configuration/) - Server tuning
- [Troubleshooting](../troubleshooting/) - Performance optimization

---

Understanding these core concepts will help you build efficient, scalable Machbase applications!
