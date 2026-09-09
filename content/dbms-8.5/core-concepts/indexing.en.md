---
type: docs
title: 'Indexing and Performance'
weight: 30
---

Learn how Machbase indexes work and how to optimize query performance. This guide covers indexing strategies, automatic index management, and performance tuning.

## Indexing Overview

Machbase uses different indexing strategies for each table type, all designed for time-series workloads:

| Table Type | Index Type | Management | Purpose |
|-----------|-----------|------------|---------|
| Tag | 3-level Partitioned | Automatic | Fast sensor_id + time queries |
| Log | LSM (optional) | Manual | Fast column lookups |
| Volatile | Red-Black Tree | Automatic | Fast PRIMARY KEY access |
| Lookup | LSM (optional) | Manual | Fast column lookups |

**Key insight**: Most users never need to manually create indexes!

## Tag Table Indexing

### Automatic 3-Level Partitioned Index

Tag tables automatically create a sophisticated indexing system:

**Level 1: Tag Name Index**
- Quickly find specific sensor
- O(log n) lookup by sensor_id

**Level 2: Time Partitioning**
- Data partitioned by time ranges
- Skips irrelevant time periods

**Level 3: Value Index (for SUMMARIZED columns)**
- Per-partition value indexes
- Fast range queries

### How It Works

```sql
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
) WITH ROLLUP;

-- Behind the scenes, Machbase creates:
-- 1. Index on sensor_id (tag name)
-- 2. Time-based partitions
-- 3. Rollup/index structures for the summarized column
```

### Query Optimization

**Optimal Queries** (use all 3 index levels):
```sql
-- Fast: Uses sensor_id index + time partition + value index
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN '2025-10-10 00:00:00' AND '2025-10-10 23:59:59'
  AND temperature > 25.0;
```

**Good Queries** (use 2 index levels):
```sql
-- Uses sensor_id + time partition
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

**Slow Queries** (full scan):
```sql
-- Scans all sensors (no sensor_id filter)
SELECT * FROM sensors
WHERE temperature > 30.0;
```

### Rollup Table Indexes

Rollup tables are indexed when they exist:

```sql
-- Query rollup (very fast, pre-aggregated data)
SELECT rollup('hour', 1, time) AS hour_time, AVG(temperature), COUNT(temperature)
FROM sensors
WHERE sensor_id = 'sensor01'
GROUP BY hour_time;

-- Common rollup levels: sec, min, hour
```

### Best Practices

**DO**:
- Always include sensor_id in WHERE clause
- Use time filters (`DURATION` for Log tables, BASETIME ranges for Tag tables)
- Query rollup tables for statistics
- Let Machbase manage indexes automatically

**DON'T**:
- Try to create manual indexes (not supported)
- Query without sensor_id filter (slow full scan)
- Query raw data when rollup is sufficient

## Log Table Indexing

### LSM Index (Optional)

Log tables can optionally create LSM (Log-Structured Merge) indexes:

```sql
-- Create log table
CREATE TABLE app_logs (
    level VARCHAR(10),
    component VARCHAR(50),
    message VARCHAR(2000)
);

-- Create LSM index on frequently queried column
CREATE INDEX idx_level ON app_logs(level);
CREATE INDEX idx_component ON app_logs(component);
```

### When to Create Indexes

**Create index if**:
- Column frequently in WHERE clause
- Query performance is slow
- Column has moderate cardinality (not too many unique values)

**Skip index if**:
- Only querying by time
- Column has very high cardinality
- Write performance is critical

### LSM Index Characteristics

**Advantages**:
- Optimized for write-heavy workloads
- No blocking on writes
- Automatically maintained

**How LSM Works**:
1. New writes go to memory buffer
2. Periodically flushed to disk segments
3. Background merge process combines segments
4. Reads search across segments

### Index Building

```sql
-- Check index status
SHOW INDEXES;

-- View index building progress
SHOW INDEXGAP;

-- Index builds in background (non-blocking)
```

### Query Optimization

**With Index**:
```sql
-- Fast: Uses idx_level
SELECT * FROM app_logs
WHERE level = 'ERROR'
DURATION 1 HOUR;
```

**Keyword Index Required**:
```sql
-- SEARCH requires a KEYWORD index
CREATE INDEX idx_message ON app_logs(message) INDEX_TYPE KEYWORD;

SELECT * FROM app_logs
WHERE message SEARCH 'timeout'
DURATION 1 HOUR;
```

## Volatile Table Indexing

### Automatic Red-Black Tree

Volatile tables automatically create in-memory indexes on PRIMARY KEY:

```sql
CREATE VOLATILE TABLE device_status (
    device_id INTEGER PRIMARY KEY,  -- Automatically indexed
    status VARCHAR(20),
    last_updated DATETIME
);
```

### Performance Characteristics

- **Lookup**: O(log n) by PRIMARY KEY
- **Insert**: O(log n)
- **Update**: O(log n)
- **Delete**: O(log n)

All operations are in-memory (very fast!).

### Query Optimization

**Fast**:
```sql
-- Uses PRIMARY KEY index
SELECT * FROM device_status WHERE device_id = 101;
UPDATE device_status SET status = 'RUNNING' WHERE device_id = 101;
DELETE FROM device_status WHERE device_id = 101;
```

**Slower**:
```sql
-- Full scan (no index on status)
SELECT * FROM device_status WHERE status = 'ERROR';
```

## Lookup Table Indexing

### LSM Index (Same as Log Table)

```sql
CREATE LOOKUP TABLE devices (
    device_id INTEGER PRIMARY KEY,
    device_name VARCHAR(100),
    location VARCHAR(200)
);

-- Create indexes on frequently queried columns
CREATE INDEX idx_location ON devices(location);
```

Same principles as Log table indexing.

## Time-Based Partitioning

### Automatic Partitioning

Tag and Log tables use time-aware storage for efficient range queries. Lookup tables are
persistent reference tables and are optimized through primary keys and optional indexes.

```
Partition Structure:
┌──────────────────────────────────────┐
│ Partition 1: Week 1 (Oct 1-7)       │
│   - Data for this week               │
│   - Separate index                   │
│   - Optimized compression            │
├──────────────────────────────────────┤
│ Partition 2: Week 2 (Oct 8-14)      │
│   - Data for this week               │
│   - Separate index                   │
│   - Optimized compression            │
├──────────────────────────────────────┤
│ Partition 3: Week 3 (Oct 15-21)     │
│   - Active partition                 │
│   - Less compressed (for writes)     │
└──────────────────────────────────────┘
```

### Benefits

**Query Performance**:
- Only scan relevant partitions
- Skip old/future partitions
- Parallel partition scanning

**Data Management**:
- Easy retention (drop old partitions)
- Per-partition compression
- Efficient backup/restore

### Query Optimization

**Good** (scans 1 partition):
```sql
SELECT * FROM logs DURATION 1 DAY;
```

**Slower** (scans multiple partitions):
```sql
SELECT * FROM logs DURATION 30 DAY;
```

**Very Slow** (scans all partitions):
```sql
SELECT * FROM logs;  -- No time filter!
```

## Query Optimization Strategies

### 1. Always Use Time Filters

**Bad**:
```sql
SELECT * FROM sensors WHERE sensor_id = 'sensor01';
```

**Good**:
```sql
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 2. Use DURATION Keyword

**Good** (optimized syntax):
```sql
SELECT * FROM logs DURATION 1 HOUR;
```

**Less Optimal** (manual time filter):
```sql
SELECT * FROM logs
WHERE _arrival_time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
                        AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 3. Query Rollup, Not Raw Data

**Good** (instant results when matching rollups exist):
```sql
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN TO_DATE('2025-10-01', 'YYYY-MM-DD')
               AND TO_DATE('2025-10-08', 'YYYY-MM-DD');

SELECT rollup('hour', 1, time) AS hour_time, AVG(temperature)
FROM sensors
WHERE sensor_id = 'sensor01'
GROUP BY hour_time;
```

**Slow** (millions of rows):
```sql
SELECT sensor_id, AVG(temperature)
FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN TO_DATE('2025-10-01', 'YYYY-MM-DD')
               AND TO_DATE('2025-10-08', 'YYYY-MM-DD')
GROUP BY sensor_id;
```

### 4. Limit Result Sets

**Good**:
```sql
SELECT * FROM logs DURATION 1 HOUR LIMIT 1000;
```

**Bad**:
```sql
SELECT * FROM logs;  -- Returns millions of rows!
```

### 5. Use Indexes on High-Selectivity Columns

**Good Index** (moderate cardinality):
```sql
-- level: ERROR, WARN, INFO (low cardinality - good!)
CREATE INDEX idx_level ON logs(level);
```

**Bad Index** (very high cardinality):
```sql
-- message: millions of unique values (don't index!)
CREATE INDEX idx_message ON logs(message);  -- Don't do this!
```

## Compression

### Automatic Compression

Machbase automatically compresses data:

**Logical Compression** (columnar):
- Each column compressed separately
- Pattern-based compression
- 10-100x compression ratios

**Physical Compression** (block):
- Disk block compression
- Transparent to users
- Additional 2-5x compression

### Compression Characteristics

| Table Type | Compression Method | Typical Ratio |
|-----------|-------------------|---------------|
| Tag | Columnar + block | 50-100x |
| Log | Columnar + block | 10-50x |
| Volatile | None (in-memory) | 1x |
| Lookup | Block-level | 2-5x |

### Impact on Performance

**Reads**:
- Compressed data read faster (less I/O)
- Decompression overhead minimal
- Net benefit for large scans

**Writes**:
- Buffer in memory first
- Compress during flush
- No write-time penalty

## Performance Monitoring

### Check Table Statistics

```sql
-- View table info
SHOW TABLE sensors;

-- View storage usage
SHOW STORAGE;

-- View tablespace info
SHOW TABLESPACES;
```

### Monitor Queries

```sql
-- View active queries
SHOW STATEMENTS;

-- Check slow queries
-- (long-running queries appear here)
```

### Index Health

```sql
-- Check indexes
SHOW INDEXES;

-- View index building progress
SHOW INDEXGAP;
```

## Performance Tuning

### Server Configuration

Key parameters (in machbase.conf):

```properties
# Memory settings
PROCESS_MAX_SIZE = 8G                         # Process memory limit
VOLATILE_TABLESPACE_MEMORY_MAX_SIZE = 1G      # Volatile table memory
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE = 2G # Disk table memory

# Write performance
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 600
DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC = 600

# Query performance
MAX_QPX_MEM = 512M             # Per-query memory limit
SESSION_QUERY_TIMEOUT_SEC = 60 # Query timeout, 0 disables timeout
```

### Application Optimization

**Batch Writes**:
```c
// Use APPEND protocol for bulk inserts
SQLAppendOpen(stmt, "sensors");
for (int i = 0; i < 10000; i++) {
    SQLAppendDataV(stmt, sensor_id, time, value);
}
SQLAppendClose(stmt);  // Commit batch
```

**Connection Pooling**:
- Reuse connections
- Avoid connection overhead
- 10-20 connections typical

**Query Result Limits**:
```sql
-- Always limit results for UI queries
SELECT * FROM logs DURATION 1 HOUR LIMIT 100;
```

## Common Performance Issues

### Issue 1: Slow Queries Without Time Filter

**Problem**:
```sql
SELECT * FROM sensors WHERE sensor_id = 'sensor01';
-- Slow: scans all partitions
```

**Solution**:
```sql
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
  AND time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### Issue 2: Querying Raw Data for Analytics

**Problem**:
```sql
SELECT AVG(temperature)
FROM sensors
WHERE time BETWEEN TO_DATE('2025-10-01', 'YYYY-MM-DD')
               AND TO_DATE('2025-10-08', 'YYYY-MM-DD');
-- Slow: aggregates millions of rows
```

**Solution**:
```sql
SELECT rollup('hour', 1, time) AS hour_time, AVG(temperature)
FROM sensors
WHERE time BETWEEN TO_DATE('2025-10-01', 'YYYY-MM-DD')
               AND TO_DATE('2025-10-08', 'YYYY-MM-DD')
GROUP BY hour_time;  -- Fast when matching rollups exist
```

### Issue 3: Missing Indexes on Log Tables

**Problem**:
```sql
-- Slow without index
SELECT * FROM logs WHERE level = 'ERROR' DURATION 1 DAY;
```

**Solution**:
```sql
CREATE INDEX idx_level ON logs(level);
-- Now fast!
```

### Issue 4: Large Result Sets

**Problem**:
```sql
SELECT * FROM logs DURATION 30 DAY;
-- Returns millions of rows!
```

**Solution**:
```sql
-- Aggregate instead
SELECT level, COUNT(*) FROM logs
DURATION 30 DAY
GROUP BY level;

-- Or limit results
SELECT * FROM logs DURATION 30 DAY LIMIT 1000;
```

## Best Practices Summary

1. **Always use time filters** (DURATION or time range)
2. **Query rollup for analytics** (Tag tables)
3. **Create indexes on frequently queried columns** (Log/Lookup tables)
4. **Limit result sets** (use LIMIT clause)
5. **Use batch writes** (APPEND protocol)
6. **Let Machbase manage indexes** (Tag/Volatile tables)
7. **Monitor query performance** (SHOW STATEMENTS)
8. **Implement data retention** (DELETE old data)

## Next Steps

- **Apply Knowledge**: [SELECT Reference](../../sql-reference/select/) - Query optimization
- **Learn More**: [Table Types](../../table-types/) - Detailed table documentation
- **Troubleshoot**: [Troubleshooting](../../troubleshooting/) - Performance issues

## Key Takeaways

1. **Tag tables** use automatic 3-level partitioned indexes
2. **Log/Lookup tables** can use optional LSM indexes
3. **Volatile tables** use automatic in-memory indexes
4. **Time-based partitioning** is automatic and essential
5. **Always filter by time** for optimal performance
6. **Query rollup, not raw data** for analytics
7. **Most users never create manual indexes** - it's automatic!

---

Master indexing and unlock Machbase's full performance potential!
