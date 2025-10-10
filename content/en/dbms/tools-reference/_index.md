---
title: 'Tools Reference'
weight: 90
---

Complete reference for Machbase command-line tools and utilities. This section covers all tools for database administration, data import/export, and system management.

## Command-Line Tools

### machadmin

Database server administration:
- Start/stop server
- Create/delete database
- Backup/restore
- Server status

```bash
machadmin -u          # Start server
machadmin -s          # Stop server
machadmin -c          # Create database
machadmin -b path     # Backup
machadmin -r path     # Restore
```

[Complete Reference](../../dbms/tools/machadmin/)

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

[Complete Reference](../../dbms/tools/machsql/)

### machloader

Bulk data import tool:
- CSV import
- Fast bulk loading
- Error handling

```bash
machloader -t table -d csv -i data.csv
```

[Complete Reference](../../dbms/tools/machloader/)

### machcoordinatoradmin

Cluster coordinator management (cluster edition):
- Coordinator administration
- Cluster configuration
- Node management

[Complete Reference](../../dbms/tools/machcoordinatoradmin/)

### machdeployeradmin

Cluster deployer management (cluster edition):
- Deployer administration
- Warehouse management
- Cluster deployment

[Complete Reference](../../dbms/tools/machdeployeradmin/)

## Tool Quick Reference

| Tool | Purpose | Common Use |
|------|---------|------------|
| machadmin | Server admin | Start/stop, backup |
| machsql | SQL client | Queries, scripts |
| machloader | Data import | CSV loading |
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
machloader -t sensors -d csv -i data.csv

# Export query results
machsql -f query.sql -o results.csv -r csv
```

### Backup and Restore

```bash
# Backup
machadmin -b /backup/machbase_backup

# Restore
machadmin -r /backup/machbase_backup
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
- `BUFFER_POOL_SIZE` - Memory buffer size
- `CHECKPOINT_INTERVAL_SEC` - Checkpoint interval

[Complete Configuration Reference](../configuration/)

## Log Files

```bash
# Server logs
$MACHBASE_HOME/trc/machbase.log

# SQL client logs
$MACHBASE_HOME/trc/machsql.log

# Loader logs
$MACHBASE_HOME/trc/machloader.log
```

## Troubleshooting

### Server Won't Start

```bash
# Check port availability
netstat -an | grep 5656

# Check logs
tail -50 $MACHBASE_HOME/trc/machbase.log

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
cat $MACHBASE_HOME/trc/machloader.log
```

## Best Practices

1. **Always use environment variables** - Set MACHBASE_HOME correctly
2. **Check server status** - Use `machadmin -e` before operations
3. **Review logs** - Check logs for errors and warnings
4. **Regular backups** - Use `machadmin -b` for backups
5. **Test scripts** - Validate SQL scripts before production use

## Related Documentation

- [Common Tasks](../common-tasks/) - Practical how-to guides
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
machloader -t mytable -d csv -i data.csv
```

For detailed tool documentation, see the [Tools Reference](../../dbms/tools/) in the original documentation.
