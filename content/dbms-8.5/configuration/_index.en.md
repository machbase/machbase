---
type: docs
title: 'Configuration'
weight: 100
toc: true
---

Machbase server properties are key-value pairs read from `machbase.conf` when the server
starts. This page shows commonly changed properties and points to the full property
reference for exact limits.

## Configuration File

### Location

```bash
$MACHBASE_HOME/conf/machbase.conf
```

### Editing Configuration

```bash
# Stop the server before editing.
machadmin -s

# Edit the configuration file.
vi $MACHBASE_HOME/conf/machbase.conf

# Start the server with the new settings.
machadmin -u
```

Most properties are startup properties. Change them while the server is stopped unless
the property reference explicitly says that runtime alteration is supported.

## Key Configuration Parameters

### Network And Sessions

```properties
# Server port.
PORT_NO = 5656

# Bind IP address. Use 0.0.0.0 to listen on all interfaces.
BIND_IP_ADDRESS = 0.0.0.0

# Maximum concurrent sessions.
MAX_SESSION_COUNT = 4096

# Idle and query timeout in seconds. 0 disables the timeout.
SESSION_IDLE_TIMEOUT_SEC = 0
SESSION_QUERY_TIMEOUT_SEC = 0
```

### Memory

```properties
# Maximum memory size of the machbased process.
PROCESS_MAX_SIZE = 8589934592 # 8GB

# Disk columnar tablespace memory limit.
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE = 8589934592 # 8GB

# Volatile tablespace memory limit.
VOLATILE_TABLESPACE_MEMORY_MAX_SIZE = 2147483648 # 2GB

# Query processor memory limit per query.
MAX_QPX_MEM = 1073741824 # 1GB
```

### Storage And Checkpoint

```properties
# Database directory. ? is expanded to $MACHBASE_HOME.
DBS_PATH = ?/dbs

# Table and index checkpoint intervals in seconds.
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 120
DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC = 120
```

### Query Processing

```properties
# Parallel query factor. Standard builds default to 0; cluster builds default to 4.
QUERY_PARALLEL_FACTOR = 0

# Tag table scan direction: -1 backward, 0 engine-decided, 1 forward.
TABLE_SCAN_DIRECTION = 0
```

### Trace Logging

```properties
# Trace log directory. ? is expanded to $MACHBASE_HOME.
TRACE_LOGFILE_PATH = ?/trc

# Trace log file size and retained file count.
TRACE_LOGFILE_SIZE = 10485760 # 10MB
TRACE_LOGFILE_COUNT = 1000

# Trace log level.
TRACE_LOG_LEVEL = 277
```

## Tuning Examples

### Larger Memory Budget

```properties
PROCESS_MAX_SIZE = 17179869184 # 16GB
DISK_COLUMNAR_TABLESPACE_MEMORY_MAX_SIZE = 12884901888 # 12GB
MAX_QPX_MEM = 2147483648 # 2GB
```

### More Concurrent Clients

```properties
MAX_SESSION_COUNT = 8192
MAX_STMT_COUNT_PER_SESSION = 2048
```

### Longer Running Queries

```properties
# Disable query timeout.
SESSION_QUERY_TIMEOUT_SEC = 0

# Or set a 2 minute timeout.
SESSION_QUERY_TIMEOUT_SEC = 120
```

## Monitoring Configuration

```sql
-- View current property values.
SELECT * FROM V$PROPERTY;

-- Check storage usage.
SELECT * FROM V$STORAGE;
```

## Security Configuration

```properties
# Listen only on a specific interface.
BIND_IP_ADDRESS = 192.168.1.100

# Block native DB remote access. Set BIND_IP_ADDRESS=127.0.0.1 to
# limit HTTP to loopback as well.
GRANT_REMOTE_ACCESS = 0
```

## Cluster Configuration

Cluster edition has additional properties. Common examples include:

```properties
# Cluster link endpoint.
CLUSTER_LINK_HOST = localhost
CLUSTER_LINK_PORT_NO = 3868

# Coordinator storage path.
COORDINATOR_DBS_PATH = ?/dbs

# Coordinator HTTP admin port.
HTTP_ADMIN_PORT = 5779
```

See [Cluster Installation](../installation/cluster/) for complete cluster setup.

## Configuration Best Practices

1. Back up `machbase.conf` before changes.
2. Change one tuning area at a time.
3. Verify values against the property reference before production use.
4. Restart the server after startup property changes.
5. Monitor `V$PROPERTY`, trace logs, and workload behavior after changes.

## Complete Configuration Reference

- [Configuration Properties](./property/) - standard server property reference
- [Cluster Configuration Properties](./property-cl/) - cluster edition property reference
- [Meta Tables](./meta-table/) - system metadata tables
- [Virtual Tables](./virtual-table/) - runtime monitoring tables
