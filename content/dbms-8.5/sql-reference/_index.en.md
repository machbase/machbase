---
type: docs
title: 'SQL Reference'
weight: 80
toc: true
---

Complete SQL syntax reference for Machbase. This section provides detailed documentation for all SQL commands, data types, functions, and operators.

## SQL Command Categories

### Data Definition Language (DDL)

- `CREATE TABLE` - Create log tables
- `CREATE TAG TABLE` - Create tag tables
- `CREATE VOLATILE TABLE` - Create volatile tables
- `CREATE LOOKUP TABLE` - Create lookup tables
- `CREATE VIEW` - Create stored VIEWs
- `ALTER TABLE` - Modify table structure
- `DROP TABLE` - Delete tables
- `DROP VIEW` - Delete stored VIEWs
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
- `SHOW VIEWS` - List VIEWs
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
- [Functions](./functions/)

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
-- On a TAG table created WITH ROLLUP.
SELECT ROLLUP('hour', 1, time) AS rtime, AVG(value)
FROM tag_table
WHERE name = 'sensor-1'
GROUP BY rtime;
```

### Time-Based Deletion

```sql
DELETE FROM table OLDEST n ROWS;
DELETE FROM table EXCEPT n ROWS|DAY;
DELETE FROM table BEFORE datetime;
```

## Complete Reference

For complete SQL syntax documentation, see:
- [DDL](./ddl/), [DML](./dml/), [SELECT](./select/), and [Functions](./functions/)

## Quick Reference Examples

### Create Tables

```sql
-- Tag table with built-in rollup
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP;

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
    device_id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

-- VIEW
CREATE VIEW active_devices AS
SELECT device_id, name
FROM devices;
```

### Query Data

```sql
-- Recent data
SELECT * FROM sensors
WHERE time BETWEEN now - 1h AND now;

-- With conditions
SELECT * FROM logs WHERE level = 'ERROR' DURATION 1 DAY;

-- Aggregations
SELECT sensor_id, AVG(value) FROM sensors
WHERE time BETWEEN now - 1d AND now
GROUP BY sensor_id;

-- Rollup query
SELECT ROLLUP('hour', 1, time) AS rtime, AVG(value)
FROM sensors
WHERE sensor_id = 'sensor-1'
  AND time BETWEEN now - 7d AND now
GROUP BY rtime;
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

- [VIEW](./view) - Stored VIEW creation, querying, metadata, performance, and limits
- [Core Concepts](../core-concepts/) - Understanding Machbase
- [SELECT](./select/) - Query examples
- [Table Types](../table-types/) - Hands-on practice
