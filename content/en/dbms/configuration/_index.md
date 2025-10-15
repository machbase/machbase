---
type: docs
title: 'Configuration'
weight: 100
---

Server configuration and tuning guide for Machbase. Learn how to optimize server settings for your workload and hardware.

## Configuration File

### Location

```bash
$MACHBASE_HOME/conf/machbase.conf
```

### Editing Configuration

```bash
# Stop server before editing
machadmin -s

# Edit configuration
vi $MACHBASE_HOME/conf/machbase.conf

# Start server with new settings
machadmin -u
```

## Key Configuration Parameters

### Network Settings

```properties
# Server port
PORT_NO = 5656

# Bind IP address (0.0.0.0 for all interfaces)
BIND_IP_ADDRESS = 0.0.0.0

# Max connections
MAX_CONNECTION = 100
```

### Memory Settings

```properties
# Shared buffer pool (recommend: 50-70% of available RAM)
BUFFER_POOL_SIZE = 2G

# Volatile table memory
VOLATILE_TABLESPACE_SIZE = 1G

# Per-query memory limit
MAX_QPX_MEM = 512M

# Log buffer size
LOG_BUFFER_SIZE = 64M
```

### Performance Settings

```properties
# Checkpoint interval (seconds)
CHECKPOINT_INTERVAL_SEC = 600

# Query timeout (seconds)
QUERY_TIMEOUT = 60

# Max parallel queries
MAX_PARALLEL_QUERY = 4
```

### Storage Settings

```properties
# Database directory
DB_DIR = $MACHBASE_HOME/dbs

# Log directory
LOG_DIR = $MACHBASE_HOME/dbs

# Trace log directory
TRC_LOG_DIR = $MACHBASE_HOME/trc
```

### Backup Settings

```properties
# Backup compression
BACKUP_COMPRESSION = 1

# Backup threads
BACKUP_THREAD_COUNT = 4
```

## Tuning by Workload

### High Write Workload

```properties
# Increase buffers
BUFFER_POOL_SIZE = 4G
LOG_BUFFER_SIZE = 128M

# Reduce checkpoint frequency
CHECKPOINT_INTERVAL_SEC = 900

# Increase connections
MAX_CONNECTION = 200
```

### High Read Workload

```properties
# Increase buffer pool
BUFFER_POOL_SIZE = 8G

# Increase query memory
MAX_QPX_MEM = 1G

# Enable parallel queries
MAX_PARALLEL_QUERY = 8
```

### Mixed Workload

```properties
# Balanced settings
BUFFER_POOL_SIZE = 4G
LOG_BUFFER_SIZE = 64M
MAX_QPX_MEM = 512M
CHECKPOINT_INTERVAL_SEC = 600
MAX_PARALLEL_QUERY = 4
```

## Monitoring Configuration

### System Tables

```sql
-- View configuration
SELECT * FROM SYSTEM_.SYS_PROPERTIES_;

-- Check memory usage
SHOW STORAGE;
```

### Log Settings

```properties
# Enable trace logs
TRC_LOG_LEVEL = 1

# Log file size
TRC_LOG_FILE_SIZE = 10M

# Number of log files
TRC_LOG_FILE_COUNT = 10
```

## Security Configuration

### Access Control

```properties
# Restrict network access
BIND_IP_ADDRESS = 192.168.1.100

# Reduce max connections
MAX_CONNECTION = 50
```

### SSL/TLS

```properties
# Enable SSL
SSL_ENABLE = 1
SSL_CERT = /path/to/cert.pem
SSL_KEY = /path/to/key.pem
```

## Cluster Configuration

For cluster deployments, additional configuration is required:

```properties
# Cluster mode
CLUSTER_ENABLE = 1

# Cluster ID
CLUSTER_ID = cluster01

# Coordinator address
COORDINATOR_HOST = 192.168.1.10
COORDINATOR_PORT = 6656
```

See [Cluster Installation](../../dbms/install/cluster/) for complete cluster setup.

## Configuration Best Practices

1. **Backup config before changes** - Save original configuration
2. **Test in staging** - Validate changes before production
3. **Monitor after changes** - Watch logs and performance
4. **Document changes** - Keep change log
5. **Use appropriate values** - Match hardware and workload

## Common Configuration Issues

### Out of Memory

**Symptom**: Server crashes or slow performance

**Solution**:
```properties
# Reduce memory usage
BUFFER_POOL_SIZE = 1G  # Reduce buffer pool
MAX_QPX_MEM = 256M     # Reduce query memory
```

### Too Many Connections

**Symptom**: "Max connections exceeded" error

**Solution**:
```properties
# Increase connection limit
MAX_CONNECTION = 200
```

### Slow Queries

**Symptom**: Queries time out

**Solution**:
```properties
# Increase query timeout
QUERY_TIMEOUT = 120

# Increase query memory
MAX_QPX_MEM = 1G

# Enable parallel queries
MAX_PARALLEL_QUERY = 8
```

## Complete Configuration Reference

For detailed configuration documentation, see:
- [Configuration Properties](../../dbms/config-monitor/property/) - Complete parameter reference
- [System Tables](../../dbms/config-monitor/meta-table/) - System metadata
- [Virtual Tables](../../dbms/config-monitor/virtual-table/) - Monitoring tables

## Configuration Template

```properties
# machbase.conf - Production configuration template

# Network
PORT_NO = 5656
BIND_IP_ADDRESS = 0.0.0.0
MAX_CONNECTION = 100

# Memory (adjust based on available RAM)
BUFFER_POOL_SIZE = 4G
VOLATILE_TABLESPACE_SIZE = 1G
MAX_QPX_MEM = 512M
LOG_BUFFER_SIZE = 64M

# Performance
CHECKPOINT_INTERVAL_SEC = 600
QUERY_TIMEOUT = 60
MAX_PARALLEL_QUERY = 4

# Storage
DB_DIR = $MACHBASE_HOME/dbs
LOG_DIR = $MACHBASE_HOME/dbs
TRC_LOG_DIR = $MACHBASE_HOME/trc

# Logging
TRC_LOG_LEVEL = 1
TRC_LOG_FILE_SIZE = 10M
TRC_LOG_FILE_COUNT = 10
```

## Next Steps

- **Apply Configuration**: [Tools Reference](../tools-reference/) - machadmin usage
- **Monitor Performance**: [Troubleshooting](../troubleshooting/) - Performance tuning
- **Advanced Setup**: [Advanced Features](../advanced-features/) - Cluster configuration
