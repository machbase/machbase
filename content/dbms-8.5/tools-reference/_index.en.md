---
type: docs
title: 'Tools Reference'
weight: 90
---

Complete reference for Machbase command-line tools and utilities. This section covers all tools for database administration, data import/export, and system management.

## Command-Line Tools

### machadmin

Database server administration:
- Start/stop server
- Create/delete database
- Restore/extract backup images
- Server status

```bash
machadmin -u          # Start server
machadmin -s          # Stop server
machadmin -c          # Create database
machadmin -r path     # Restore
machadmin -w path     # View backup image information
```

[Complete Reference](./machadmin/)

### machsql

Interactive SQL client:
- Execute queries
- Run SQL scripts
- Export results
- Database administration

```bash
machsql                           # Interactive mode
machsql -f script.sql            # Run script
machsql -o output.csv -r csv     # Export to CSV
```

[Complete Reference](./machsql/)

### machloader

Bulk data import tool:
- CSV import
- Fast bulk loading
- Error handling

```bash
machloader -i -t table -d data.csv
```

[Complete Reference](./machloader/)

### machcoordinatoradmin

Cluster coordinator management (cluster edition):
- Coordinator administration
- Cluster configuration
- Node management

[Complete Reference](./machcoordinatoradmin/)

### machdeployeradmin

Cluster deployer management (cluster edition):
- Deployer administration
- Warehouse management
- Cluster deployment

[Complete Reference](./machdeployeradmin/)

## Tool Quick Reference

| Tool | Purpose | Common Use |
|------|---------|------------|
| machadmin | Server admin | Start/stop, restore |
| machsql | SQL client | Queries, scripts |
| machloader | Data import | CSV loading |
| csvimport/csvexport | CSV wrapper | Simple import/export |
| machcoordinatoradmin | Cluster coordinator | Cluster management |
| machdeployeradmin | Cluster deployer | Cluster deployment |

## Common Operations

### Server Management

```bash
# Start server
machadmin -u

# Stop server
machadmin -s

# Check status
machadmin -e

# Create database
machadmin -c

# Delete database
machadmin -d
```

### Data Operations

```bash
# Interactive SQL
machsql

# Run script
machsql -f setup.sql

# Import CSV
machloader -i -t sensors -d data.csv

# Export query results
machsql -f query.sql -o results.csv -r csv
```

### Backup Image Operations

```bash
# Restore
machadmin -r /backup/machbase_backup

# Extract a backup file to a backup directory
machadmin -x /backup/machbase_backup

# View backup image information
machadmin -w /backup/machbase_backup
```

## Environment Variables

```bash
# Required environment variables
export MACHBASE_HOME=/path/to/machbase
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

## Configuration Files

### machbase.conf

Main server configuration file location:
```
$MACHBASE_HOME/conf/machbase.conf
```

Key parameters:
- `PORT_NO` - Server port (default: 5656)
- `PROCESS_MAX_SIZE` - Maximum memory size of the server process
- `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC` - Table checkpoint interval
- `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC` - Index checkpoint interval

[Complete Configuration Reference](../configuration/)

## Log Files

```bash
# Server logs
$MACHBASE_HOME/trc/machbase.trc

# SQL client logs
$MACHBASE_HOME/trc/machsql.trc

# Loader logs
$MACHBASE_HOME/trc/machloader.trc
```

## Troubleshooting

### Server Won't Start

```bash
# Check port availability
netstat -an | grep 5656

# Check logs
tail -50 $MACHBASE_HOME/trc/machbase.trc

# Verify database created
ls -la $MACHBASE_HOME/dbs/
```

### Connection Issues

```bash
# Verify server running
machadmin -e

# Test connection
machsql -s localhost -u SYS -p MANAGER
```

### Import Errors

```bash
# Check CSV format
head -10 data.csv

# View loader logs
cat $MACHBASE_HOME/trc/machloader.trc
```

## Best Practices

1. **Always use environment variables** - Set MACHBASE_HOME correctly
2. **Check server status** - Use `machadmin -e` before operations
3. **Review logs** - Check logs for errors and warnings
4. **Validate maintenance inputs** - Check backup image paths before restore/extract operations
5. **Test scripts** - Validate SQL scripts before production use

## Related Documentation

- [First Steps](../getting-started/first-steps/) - Practical how-to guides
- [Configuration](../configuration/) - Server configuration
- [Troubleshooting](../troubleshooting/) - Problem solving

## Quick Start

```bash
# 1. Set environment
export MACHBASE_HOME=/opt/machbase
export PATH=$MACHBASE_HOME/bin:$PATH

# 2. Create database
machadmin -c

# 3. Start server
machadmin -u

# 4. Connect
machsql

# 5. Import data
machloader -i -t mytable -d data.csv
```

For detailed tool documentation, see each tool page in this section.
