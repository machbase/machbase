---
type: docs
title: 'Troubleshooting'
weight: 110
---

Solutions to common problems, error codes, and performance optimization guide for Machbase.

## Common Issues

### Server Issues

#### Server Won't Start

**Symptoms**:
- `machadmin -u` fails
- "Address already in use" error
- No server process running

**Solutions**:
```bash
# Check if port is in use
netstat -an | grep 5656
lsof -i :5656

# Kill existing process
kill $(lsof -t -i:5656)

# Check database directory
ls -la $MACHBASE_HOME/dbs/

# Review logs
tail -50 $MACHBASE_HOME/trc/machbase.trc

# Try starting again
machadmin -u
```

#### Server Crashes

**Symptoms**:
- Server stops unexpectedly
- Core dump files
- "Segmentation fault" errors

**Solutions**:
```bash
# Check logs
tail -100 $MACHBASE_HOME/trc/machbase.trc

# Check system resources
free -h
df -h

# Reduce memory usage (in machbase.conf)
PROCESS_MAX_SIZE = 1073741824 # 1GB

# Check for disk space
du -sh $MACHBASE_HOME/dbs/
```

### Connection Issues

#### Cannot Connect

**Symptoms**:
- "Connection refused" error
- "Connection timeout"
- machsql fails to connect

**Solutions**:
```bash
# Verify server is running
machadmin -e

# Check network connectivity
ping server-address
telnet server-address 5656

# Check firewall
sudo iptables -L | grep 5656

# Verify credentials
machsql -s localhost -u SYS -p MANAGER
```

#### Too Many Connections

**Symptoms**:
- "Max connections exceeded" error
- New connections rejected

**Solutions**:
```sql
-- Check active connections
SHOW STATEMENTS;

-- Increase MAX_CONNECTION in machbase.conf
-- MAX_CONNECTION = 200

-- Kill idle connections (if necessary)
```

### Query Issues

#### Slow Queries

**Symptoms**:
- Queries take too long
- Timeout errors
- High CPU usage

**Solutions**:
```sql
-- Add time filter
SELECT * FROM table DURATION 1 HOUR;  -- Add this!

-- Use LIMIT
SELECT * FROM table LIMIT 1000;

-- Query rollup instead of raw data
SELECT ROLLUP('hour', 1, time) AS rtime, AVG(value)
FROM sensors
WHERE name = 'sensor-1'
GROUP BY rtime;

-- Create index
CREATE INDEX idx_column ON table(column);

-- Check query plan
EXPLAIN SELECT ...;
```

#### Out of Memory

**Symptoms**:
- "Out of memory" error
- Query fails midway
- Server becomes unresponsive

**Solutions**:
```sql
-- Reduce result set
SELECT * FROM table DURATION 1 HOUR LIMIT 1000;

-- Select fewer columns
SELECT col1, col2 FROM table;  -- Not SELECT *

-- Increase MAX_QPX_MEM in machbase.conf
-- MAX_QPX_MEM = 1G
```

### Data Issues

#### Import Fails

**Symptoms**:
- machloader error
- CSV import fails
- Data type mismatch

**Solutions**:
```bash
# Check CSV format
head -10 data.csv

# Verify table schema
machsql -f - <<EOF
SHOW TABLE tablename;
EOF

# Check error log
cat $MACHBASE_HOME/trc/machloader.trc

# Validate data types
# Ensure CSV columns match table schema

# Try small batch first
head -100 data.csv > test.csv
machloader -i -t table -d test.csv
```

#### Missing Data

**Symptoms**:
- Expected data not found
- Count mismatch
- Time gaps

**Solutions**:
```sql
-- Check time range
SELECT MIN(_arrival_time), MAX(_arrival_time) FROM table;

-- Check total count
SELECT COUNT(*) FROM table;

-- Check for NULLs
SELECT COUNT(*) FROM table WHERE column IS NULL;

-- Verify import completed
-- Check machloader logs
```

## Error Codes

### Common Error Messages

| Error Code | Message | Solution |
|-----------|---------|----------|
| -20000 | Connection failed | Check server status, network |
| -20001 | Authentication failed | Verify username/password |
| -20100 | Table not found | Check table name, use SHOW TABLES |
| -20101 | Column not found | Verify column name, use SHOW TABLE |
| -20200 | Duplicate key | Check PRIMARY KEY constraints |
| -20300 | Data type mismatch | Validate data types |
| -30000 | Out of memory | Reduce query size, increase memory |
| -30100 | Timeout | Add time filter, increase timeout |

For complete error code reference, see [Error Codes](./error-code/).

## Performance Optimization

### Query Optimization

1. **Always use time filters**
```sql
-- Bad
SELECT * FROM sensors WHERE sensor_id = 'sensor01';

-- Good
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
DURATION 1 HOUR;
```

2. **Use rollup for analytics**
```sql
-- Slow
SELECT AVG(value) FROM sensors DURATION 7 DAY;

-- Fast
-- sensors must be a TAG table created WITH ROLLUP.
SELECT ROLLUP('hour', 1, time) AS rtime, AVG(value)
FROM sensors
WHERE name = 'sensor-1'
  AND time BETWEEN now - 7d AND now
GROUP BY rtime;
```

3. **Create indexes**
```sql
CREATE INDEX idx_level ON logs(level);
```

4. **Limit results**
```sql
SELECT * FROM logs DURATION 1 DAY LIMIT 1000;
```

### Server Tuning

```properties
# Memory optimization
PROCESS_MAX_SIZE = 4294967296 # 4GB
MAX_QPX_MEM = 1073741824      # Per-query memory

# Performance tuning
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 900
DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC = 900
QUERY_PARALLEL_FACTOR = 8
```

### Data Management

1. **Implement retention**
```sql
DELETE FROM logs EXCEPT 30 DAYS;
```

2. **Batch writes**
```python
# Use APPEND API for bulk inserts
appender = conn.create_appender('table')
for row in data:
    appender.append(row)
appender.close()
```

3. **Monitor storage**
```sql
SHOW STORAGE;
```

## Diagnostic Commands

### Check Server Status

```bash
# Server running?
machadmin -e

# View active queries
machsql -f - <<EOF
SHOW STATEMENTS;
EOF

# Check storage
machsql -f - <<EOF
SHOW STORAGE;
EOF
```

### Check Logs

```bash
# Server log
tail -50 $MACHBASE_HOME/trc/machbase.trc

# Error log
grep -i error $MACHBASE_HOME/trc/machbase.trc

# Recent activity
tail -100 $MACHBASE_HOME/trc/machbase.trc
```

### System Information

```sql
-- Tables
SHOW TABLES;

-- Table details
SHOW TABLE tablename;

-- Users
SHOW USERS;

-- Indexes
SHOW INDEXES;

-- License
SHOW LICENSE;
```

## Getting Help

### Information to Gather

When reporting issues, collect:

1. **Error message** (exact text)
2. **Server logs** ($MACHBASE_HOME/trc/machbase.trc)
3. **Machbase version** (`machadmin -v`)
4. **Operating system** (`uname -a`)
5. **Steps to reproduce**

### Support Resources

- **Documentation**: Review this guide and [Common Issues](./common-issues/)
- **Error Codes**: Check [Error Code Reference](./error-code/)
- **Memory Issues**: See [Memory Error Guide](./memory-error/)

## Best Practices to Avoid Issues

1. **Always use time filters** in queries
2. **Implement data retention** policies
3. **Monitor server resources** regularly
4. **Regular backups** (daily)
5. **Test queries** on small datasets first
6. **Use appropriate table types** for data
7. **Keep Machbase updated** to latest version

## Quick Fixes

```bash
# Restart server
machadmin -s && sleep 5 && machadmin -u

# Check disk space
df -h

# Check memory
free -h

# View recent errors
grep -i error $MACHBASE_HOME/trc/machbase.trc | tail -20

# Test connection
machsql -s localhost -u SYS -p MANAGER -f - <<EOF
SELECT SYSDATE;
EOF
```

## Related Documentation

- [Configuration](../configuration/) - Server configuration
- [Tools Reference](../tools-reference/) - Command-line tools
- [Common Issues](./common-issues/) - Frequently asked questions
