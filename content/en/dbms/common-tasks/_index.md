---
title: 'Common Tasks'
weight: 50
---

Practical how-to guides for everyday Machbase operations. Each guide provides step-by-step instructions with real examples.

## Quick Links

| Task | What You'll Learn | Time |
|------|------------------|------|
| [Connecting](./connecting/) | Connect via machsql, ODBC, JDBC, REST API | 10 min |
| [Importing Data](./importing-data/) | CSV import, bulk loading, APPEND protocol | 15 min |
| [Querying Data](./querying/) | Common query patterns and optimization | 20 min |
| [User Management](./user-management/) | Create users, grant permissions, security | 15 min |
| [Backup & Recovery](./backup-recovery/) | Backup strategies, restore procedures | 15 min |

## In This Section

### [Connecting to Machbase](./connecting/)

Learn all the ways to connect to Machbase:
- machsql command-line client
- ODBC/CLI connections
- JDBC for Java applications
- REST API for HTTP access
- Python, .NET, and other SDKs
- Connection pooling and best practices

### [Importing Data](./importing-data/)

Master data import techniques:
- CSV file import with machloader
- Bulk loading with APPEND protocol
- Real-time data ingestion
- Handling large datasets
- Error handling and validation
- Performance optimization

### [Querying Data](./querying/)

Common query patterns:
- Time-based queries with DURATION
- Aggregations and GROUP BY
- Text search with SEARCH keyword
- JOIN operations
- Subqueries and CTEs
- Query optimization tips

### [User Management](./user-management/)

Manage database users and security:
- Creating and deleting users
- Granting and revoking permissions
- Role-based access control
- Password management
- Auditing user activities
- Security best practices

### [Backup and Recovery](./backup-recovery/)

Protect your data:
- Full database backups
- Incremental backups
- Online vs offline backups
- Restore procedures
- Disaster recovery planning
- Backup automation

## Who Should Read This

These guides are for:
- **Database administrators** managing Machbase installations
- **Developers** building applications with Machbase
- **Data engineers** setting up data pipelines
- **DevOps** automating database operations

## Prerequisites

Before following these guides:
- Have Machbase installed and running
- Complete the [Getting Started](../getting-started/) section
- Basic SQL knowledge
- Command-line familiarity

## Quick Reference

### Daily Operations

```sql
-- Connect
machsql -s localhost -u SYS -p MANAGER

-- Import CSV
machloader -t sensor_data -d csv -i data.csv

-- Query recent data
SELECT * FROM logs DURATION 1 HOUR;

-- Create user
CREATE USER analyst IDENTIFIED BY 'password';

-- Backup
machadmin -b /backup/machbase_backup
```

### Common Commands

| Task | Command |
|------|---------|
| Start server | `machadmin -u` |
| Stop server | `machadmin -s` |
| Check status | `machadmin -e` |
| Connect | `machsql` |
| Import CSV | `machloader -t TABLE -d csv -i file.csv` |
| Backup | `machadmin -b /path/to/backup` |
| Restore | `machadmin -r /path/to/backup` |

### Key SQL Operations

```sql
-- USER MANAGEMENT
CREATE USER username IDENTIFIED BY 'password';
GRANT SELECT ON table TO username;
ALTER USER username IDENTIFIED BY 'newpass';
DROP USER username;

-- DATA IMPORT
-- (Use machloader or APPEND API)

-- QUERYING
SELECT * FROM table DURATION 1 HOUR;
SELECT * FROM table WHERE column = 'value';
SELECT AVG(value) FROM table GROUP BY sensor_id;

-- BACKUP
-- (Use machadmin command-line tool)
```

## Best Practices

### Connection Management

1. **Use connection pooling** for applications
2. **Close connections** when done
3. **Handle connection errors** gracefully
4. **Limit concurrent connections** (10-20 typical)

### Data Import

1. **Use APPEND protocol** for high-volume data
2. **Batch inserts** (1000-10000 rows per batch)
3. **Validate data** before import
4. **Monitor import progress** and errors
5. **Use CSV for one-time imports**, API for continuous

### Querying

1. **Always use time filters** (DURATION)
2. **Limit result sets** (use LIMIT clause)
3. **Query rollup for analytics** (Tag tables)
4. **Create indexes** on frequently queried columns
5. **Avoid SELECT *** on large tables

### User Management

1. **Use strong passwords** (minimum 8 characters)
2. **Grant minimal permissions** (principle of least privilege)
3. **Regular password rotation** (quarterly)
4. **Audit user activities** (check logs)
5. **Remove inactive users** promptly

### Backup and Recovery

1. **Daily automated backups** (cron jobs)
2. **Test restores regularly** (monthly)
3. **Keep multiple backup copies** (3-2-1 rule)
4. **Store offsite** (disaster recovery)
5. **Document procedures** (runbooks)

## Troubleshooting Quick Fixes

### Connection Issues

```bash
# Check if server is running
machadmin -e

# Check port availability
netstat -an | grep 5656

# Verify credentials
machsql -s localhost -u SYS -p MANAGER
```

### Import Issues

```bash
# Check CSV format
head -10 data.csv

# Validate data types
SHOW TABLE tablename;

# Check error logs
cat $MACHBASE_HOME/trc/machloader.log
```

### Query Performance

```sql
-- Add time filter
SELECT * FROM table DURATION 1 HOUR;

-- Use LIMIT
SELECT * FROM table LIMIT 1000;

-- Check active queries
SHOW STATEMENTS;
```

### User Permission Issues

```sql
-- Check user permissions
SHOW USERS;

-- Grant required permissions
GRANT SELECT ON tablename TO username;
```

### Backup Issues

```bash
# Check disk space
df -h

# Verify backup directory permissions
ls -la /backup/

# Check backup logs
cat $MACHBASE_HOME/trc/machadmin.log
```

## Additional Resources

### Related Documentation

- [Getting Started](../getting-started/) - Basic Machbase usage
- [Core Concepts](../core-concepts/) - Understanding Machbase architecture
- [Tutorials](../tutorials/) - Hands-on learning
- [SQL Reference](../sql-reference/) - Complete SQL syntax
- [Tools Reference](../tools-reference/) - Command-line tools
- [Troubleshooting](../troubleshooting/) - Detailed problem solving

### External Resources

- [ODBC Documentation](../../sdk/cli-odbc/) - ODBC driver details
- [JDBC Documentation](../../sdk/jdbc/) - JDBC driver details
- [REST API](../../sdk/restful_api/) - HTTP API reference
- [Python SDK](../../sdk/python/) - Python integration

## Next Steps

Choose a task based on your needs:

1. **New to Machbase?** Start with [Connecting](./connecting/)
2. **Need to load data?** Go to [Importing Data](./importing-data/)
3. **Writing queries?** Check [Querying Data](./querying/)
4. **Managing access?** See [User Management](./user-management/)
5. **Protecting data?** Read [Backup & Recovery](./backup-recovery/)

---

These guides provide practical solutions to everyday Machbase tasks. Pick the task you need and follow the step-by-step instructions!
