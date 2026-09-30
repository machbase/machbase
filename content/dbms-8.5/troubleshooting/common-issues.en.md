---
title: 'Common Issues and Solutions'
type: docs
weight: 10
---

## Quick Troubleshooting Guide

This guide covers the most common issues encountered when working with Machbase and their solutions.

## Connection Issues

### Cannot Connect to Server

**Symptom**: Client tools fail to connect to Machbase server

**Common Causes**:

1. Server is not running
2. Wrong port number
3. Firewall blocking connection
4. Network configuration issues

**Solutions**:

```bash
# Check if server is running
ps -ef | grep machbase

# Check server status
machadmin -e

# Start server if not running
machadmin -u

# Verify port configuration in machbase.conf
grep PORT_NO $MACHBASE_HOME/conf/machbase.conf
```

### Connection Timeout

**Symptom**: Connection attempts time out

**Solution**:

- Check network connectivity
- Verify `PORT_NO` in `machbase.conf`
- Ensure no firewall is blocking the port
- Check if the max connections limit is reached

```sql
-- Check current connections
SELECT * FROM v$session;
```

## Performance Issues

### Slow INSERT Performance

**Symptom**: Data insertion is slower than expected

**Common Causes**:

1. Using INSERT instead of APPEND
2. Not using batch operations
3. Insufficient memory allocation
4. Too many indexes

**Solutions**:

For bulk loading, use the APPEND API or a CSV tool in APPEND mode. The SQL comment `INSERT /*+ APPEND */` does not switch an INSERT to the APPEND protocol.

```bash
# Bulk load into a tag table (default append mode)
csvimport -t TAG_TABLE -d data.csv
```

```properties
# machbase.conf: example that sets the TAG cache limit per pool to 2 GiB
TAG_CACHE_MAX_MEMORY_SIZE = 2147483648
```

The total cache capacity is this value multiplied by `TAG_CACHE_POOL_COUNT`. Adjust it to the physical memory and the memory used by other processes.

### Slow SELECT Performance

**Symptom**: Queries take too long

**Solutions**:

```sql
-- Use EXPLAIN to analyze query plan
EXPLAIN SELECT * FROM tag WHERE name = 'TAG_001';

-- For tag tables, ensure time range is specified
SELECT * FROM tag
WHERE name = 'TAG_001'
  AND time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD') AND TO_DATE('2024-01-31', 'YYYY-MM-DD');

-- Use rollup tables for aggregation queries
SELECT rollup('hour', 1, time), AVG(value)
FROM tag
GROUP BY rollup('hour', 1, time);

-- Create indexes on frequently queried columns
CREATE INDEX idx_column ON table_name (column_name);
```

## Table Creation Issues

### PRIMARY KEY / BASETIME Missing Error

**Symptom**: `ERR-02253: Mandatory column definition (PRIMARY KEY / BASETIME) is missing`

**Solution**:

```sql
-- Tag tables require both PRIMARY KEY and BASETIME
CREATE TAG TABLE tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

### Variable Length Columns Error

**Symptom**: `ERR-01851: Variable length columns are not allowed in tag table`

**Solution**: This error occurs in older versions (< 5.6). Upgrade to version 5.6+ or use fixed-length columns.

## Data Insertion Issues

### SUMMARIZED Value Out of Range

**Symptom**:

- `ERR-02341: SUMMARIZED value is greater than UPPER LIMIT`
- `ERR-02342: SUMMARIZED value is less than LOWER LIMIT`

**Solution**: The value exceeds LSL/USL limits. Either adjust the limits or fix the input data. The following example assumes that the metadata columns `lsl`/`usl` with the `LOWER LIMIT`/`UPPER LIMIT` attributes are defined for `table_name`. This feature is available in Standard Edition. For details, see [LSL/USL](../../table-types/tag-tables/lsl-usl-limits/).

```sql
-- Check current limits
SELECT * FROM _table_name_meta;

-- Update limits
UPDATE table_name METADATA SET lsl = 0, usl = 1000 WHERE name = 'TAG_001';

-- Or disable limits
UPDATE table_name METADATA SET lsl = NULL, usl = NULL WHERE name = 'TAG_001';
```

### Tag Metadata Not Found

**Symptom**: Cannot insert data, tag name not found

**Solution**: Register the tag name in the metadata first.

```sql
-- Insert tag metadata
INSERT INTO tag_table METADATA VALUES ('TAG_001');

-- Then insert data
INSERT INTO tag_table VALUES ('TAG_001', NOW, 100);
```

## Memory Issues

### Out of Memory Errors

**Symptom**: Server crashes or returns memory errors

**Solutions**:

1. **Check current memory usage**

```sql
SELECT * FROM V$SESMEM;
```

2. **Adjust memory settings in `machbase.conf`**

   For setting names and units, see [Property](../../configuration/property/). The total TAG cache capacity is the per-pool value multiplied by the pool count.

```conf
# Example that sets the TAG cache limit per pool to 4 GiB
TAG_CACHE_MAX_MEMORY_SIZE = 4294967296

# Example that sets the maximum memory used by one query to 64 MiB
MAX_QPX_MEM = 67108864
```

3. **Restart server after configuration changes**

```bash
machadmin -s  # Shut down server normally
machadmin -u  # Start server
```

For detailed memory error solutions, see [Memory Errors](../memory-error).

## Rollup Issues

### Dependent ROLLUP Table Exists

**Symptom**: `ERR-02651: Dependent ROLLUP table exists`

**Solution**: Drop rollup tables in reverse dependency order.

```sql
-- Check rollup dependencies
SELECT * FROM V$ROLLUP;

-- Drop in reverse order
DROP ROLLUP rollup_hour;
DROP ROLLUP rollup_min;
DROP ROLLUP rollup_sec;
DROP TABLE tag_table;
```

### Rollup Not Updating

**Symptom**: Rollup data is stale

**Solutions**:

```sql
-- Force rollup execution
ALTER ROLLUP rollup_name FORCE;

-- Check rollup status
SELECT * FROM v$rollup;

-- Restart rollup
ALTER ROLLUP rollup_name STOP;
ALTER ROLLUP rollup_name START;
```

## Index Issues

### Cannot Drop Index

**Symptom**: Index drop fails

**Solution**: Ensure no active sessions are using the table.

```sql
-- Check active sessions
SELECT * FROM v$session;

-- Kill sessions if necessary (carefully!): as SYS, check the target session_id
ALTER SYSTEM KILL SESSION session_id;

-- Then drop index
DROP INDEX index_name;
```

## License Issues

### License Expired

**Symptom**: Server won't start, license error

**Solution**:

```bash
# Check license status
machadmin -f

# Install new license
machadmin -t new_license_file.dat
```

## Backup and Recovery Issues

### Cannot Mount Database

**Symptom**: Mount operation fails

**Common Causes**:

1. Database files corrupted
2. Incompatible version
3. Files still in use

**Solutions**:

```sql
-- Check database status
SELECT * FROM V$STORAGE_MOUNT_DATABASES;

-- Unmount before remounting
UNMOUNT DATABASE database_name;

-- Mount database
MOUNT DATABASE 'path/to/database' TO database_name;
```

## Cluster-Specific Issues

### Node Communication Failure

**Symptom**: Nodes cannot communicate

**Solutions**:

1. Check network connectivity between nodes
2. Verify coordinator is running
3. Check firewall rules
4. Review cluster configuration

```bash
# Check cluster status
machcoordinatoradmin --cluster-status

# Restart coordinator if needed
machcoordinatoradmin -s
machcoordinatoradmin -u
```

## Best Practices for Avoiding Issues

1. **Regular Monitoring**:
   - Monitor server logs regularly
   - Check performance metrics via V$ tables
   - Set up alerting for critical errors

2. **Proper Configuration**:
   - Allocate sufficient memory
   - Configure appropriate partition counts
   - Set reasonable cache sizes

3. **Data Management**:
   - Use retention policies to manage data lifecycle
   - Regular backup of critical data
   - Monitor disk space usage

4. **Query Optimization**:
   - Always specify time ranges for tag queries
   - Use indexes appropriately
   - Leverage rollup tables for aggregations

5. **Capacity Planning**:
   - Estimate data growth
   - Plan for peak loads
   - Scale infrastructure proactively

## Getting More Help

- Review [Error Codes](../error-code) for specific error messages
- Check [Memory Errors](../memory-error) for memory-related issues
- Consult server logs in `$MACHBASE_HOME/trc/`
- Contact Machbase support with log files and error details

## Diagnostic Commands

Useful commands for troubleshooting:

```sql
-- Check server status
SELECT * FROM v$version;
SELECT * FROM V$SYSSTAT;

-- Monitor performance
SELECT * FROM V$SESMEM;
SELECT * FROM v$session;
SELECT * FROM V$STMT;

-- Check table information
SELECT * FROM m$sys_tables;
SELECT * FROM m$sys_users;
SELECT * FROM m$sys_table_property;
```

## Log Files Location

Important log file for troubleshooting:

```text
$MACHBASE_HOME/trc/machbase.trc
```

Check server errors, backup operations, and rollup operations in this trace log. You can adjust the log level with [TRACE_LOG_LEVEL](../trace-log/). Log file splitting and output to separate files depend on the operational settings, so fixed `backup.trc`, `rollup.trc`, and `error.trc` files are not always created.

For details on administrative operations, see [machadmin](../../tools-reference/machadmin/), [System/Session Management](../../sql-reference/sys-session-manage/), and [Database Mount](../../advanced-features/database-mount/).
