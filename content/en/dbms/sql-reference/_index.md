---
type: docs
title: 'SQL Reference'
weight: 80
---

Complete SQL syntax reference for Machbase. This section provides detailed documentation for all SQL commands, data types, functions, and operators.

## SQL Command Categories

### Data Definition Language (DDL)

- `CREATE TABLE` - Create log tables
- `CREATE TAGDATA TABLE` - Create tag tables
- `CREATE VOLATILE TABLE` - Create volatile tables
- `CREATE LOOKUP TABLE` - Create lookup tables
- `ALTER TABLE` - Modify table structure
- `DROP TABLE` - Delete tables
- `CREATE INDEX` - Create indexes
- `DROP INDEX` - Delete indexes

### Data Manipulation Language (DML)

- `INSERT` - Insert data
- `SELECT` - Query data
- `UPDATE` - Update data (Volatile/Lookup tables)
- `DELETE` - Delete data
- `DURATION` - Time-based query clause

### Data Control Language (DCL)

- `CREATE USER` - Create database users
- `ALTER USER` - Modify users
- `DROP USER` - Delete users
- `GRANT` - Grant permissions
- `REVOKE` - Revoke permissions

### System Commands

- `SHOW TABLES` - List tables
- `SHOW TABLE` - View table structure
- `SHOW USERS` - List users
- `SHOW INDEXES` - List indexes
- `SHOW STORAGE` - View storage info
- `SHOW LICENSE` - View license info

## Data Types

### Numeric Types
- `SHORT`, `INTEGER`, `LONG`
- `FLOAT`, `DOUBLE`

### String Types
- `CHAR(n)`, `VARCHAR(n)`

### Date/Time Types
- `DATE`, `DATETIME`

### Binary Types
- `BINARY(n)`

### Network Types
- `IPV4`, `IPV6`

## Functions

### Time Functions
- `NOW`, `SYSDATE`
- `TO_DATE()`, `TO_TIMESTAMP()`
- `TO_CHAR()`
- `INTERVAL`

### Aggregate Functions
- `COUNT()`, `SUM()`, `AVG()`
- `MIN()`, `MAX()`
- `STDDEV()`, `VARIANCE()`

### String Functions
- `UPPER()`, `LOWER()`
- `LENGTH()`, `SUBSTR()`
- `SEARCH` keyword

### Mathematical Functions
- `ABS()`, `CEIL()`, `FLOOR()`
- `ROUND()`, `TRUNC()`
- `POWER()`, `SQRT()`

## Machbase-Specific Features

### DURATION Clause

```sql
SELECT * FROM table DURATION n MINUTE|HOUR|DAY [BEFORE n MINUTE|HOUR|DAY];
```

### SEARCH Keyword

```sql
SELECT * FROM table WHERE column SEARCH 'keyword';
```

### Rollup Queries

```sql
SELECT * FROM tag_table WHERE rollup = sec|min|hour;
```

### Time-Based Deletion

```sql
DELETE FROM table OLDEST n ROWS;
DELETE FROM table EXCEPT n ROWS|DAYS;
DELETE FROM table BEFORE datetime;
```

## Complete Reference

For complete SQL syntax documentation, see:
- [SQL Reference](../../dbms/sql-ref/) - Detailed SQL command reference

## Quick Reference Examples

### Create Tables

```sql
-- Tag table
CREATE TAGDATA TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- Log table
CREATE TABLE logs (
    level VARCHAR(10),
    message VARCHAR(2000)
);

-- Volatile table
CREATE VOLATILE TABLE cache (
    key VARCHAR(100) PRIMARY KEY,
    value VARCHAR(500)
);

-- Lookup table
CREATE LOOKUP TABLE devices (
    device_id INTEGER,
    name VARCHAR(100)
);
```

### Query Data

```sql
-- Recent data
SELECT * FROM sensors DURATION 1 HOUR;

-- With conditions
SELECT * FROM logs WHERE level = 'ERROR' DURATION 1 DAY;

-- Aggregations
SELECT sensor_id, AVG(value) FROM sensors
DURATION 1 DAY GROUP BY sensor_id;

-- Rollup query
SELECT * FROM sensors WHERE rollup = hour DURATION 7 DAY;
```

### Manage Users

```sql
-- Create user
CREATE USER analyst IDENTIFIED BY 'password';

-- Grant permissions
GRANT SELECT ON sensors TO analyst;

-- Change password
ALTER USER analyst IDENTIFIED BY 'newpassword';
```

## Learning Path

1. **Start with**: Basic DDL/DML commands
2. **Learn**: Machbase-specific features (DURATION, SEARCH)
3. **Master**: Advanced queries and functions
4. **Reference**: This section for syntax details

## Related Documentation

- [Core Concepts](../core-concepts/) - Understanding Machbase
- [Common Tasks](../common-tasks/querying/) - Query examples
- [Tutorials](../tutorials/) - Hands-on practice
