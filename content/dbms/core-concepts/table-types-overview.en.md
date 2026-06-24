---
type: docs
title: 'Table Types: Complete Guide'
weight: 20
---

Choose the right table type for your data. This guide compares Machbase table types with decision frameworks, performance characteristics, and real-world examples.

## The Five Table Types

Machbase provides specialized table types, each optimized for different workloads:

1. **Tag Table** - Sensor/device axis-based data (time or distance)
2. **Log Table** - Event streams and logs
3. **Volatile Table** - Non-persistent memory table with a single primary-key index
4. **Lookup Table** - Persistent reference table with a single primary-key memory index
5. **RDB Table** - Generalized disk row table with optional primary key and secondary indexes

## Quick Decision Guide

### Start Here

Answer these questions to find your table type:

```
┌─────────────────────────────────────────────────┐
│ What kind of data do you have?                  │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
    Persistent?                 Temporary?
        │                           │
        ▼                           ▼
    ┌───────┐                 ┌──────────┐
    │ YES   │                 │ Volatile │
    └───┬───┘                 │  Table   │
        │                     └──────────┘
        ▼
    Sensor/telemetry data
    (ID, axis, value)?
        │
    ┌───┴────┐
    │        │
   YES      NO
    │        │
    ▼        ▼
  Tag     Log/Event
  Table    data?
            │
        ┌───┴────┐
        │        │
       YES      NO
        │        │
        ▼        ▼
      Log     Need single
      Table    primary-key
               reference?
                  │
              ┌───┴────┐
              │        │
             YES      NO
              │        │
              ▼        ▼
           Lookup    RDB
            Table    Table
```

If the data is persistent reference data and every access path is centered on one
primary key, choose a Lookup table. If it needs a generalized disk row schema,
optional primary key, secondary indexes, JSON path indexes, or general indexed
predicates, choose an RDB table.

### Decision Table

| Your Data | Recommended Table | Why |
|-----------|------------------|-----|
| Temperature sensors from 1000 devices | **Tag Table** | Multiple sensors, time-series values |
| Application error logs | **Log Table** | Event stream, flexible schema |
| Live user sessions | **Volatile Table** | Needs UPDATE, temporary |
| Device metadata/registry | **Lookup Table** | Persistent reference data by primary key |
| Stock market ticks | **Tag Table** | Symbol as tag, price as value |
| Conveyor vibration by position | **Tag Table** | Distance-axis measurements |
| HTTP access logs | **Log Table** | Event-based, many columns |
| Shopping cart contents | **Volatile Table** | Frequent updates, session-based |
| Product catalog keyed by product ID | **Lookup Table** | Persistent reference data by one primary key |
| Current alarm state | **RDB Table** | Generalized disk rows with UPDATE/DELETE |
| Work queue | **RDB Table** | Row changes and indexed predicates |

## Tag Table Deep Dive

### When to Use

Perfect for:
- IoT sensor data (temp, humidity, pressure)
- Industrial equipment telemetry
- Smart meters
- GPS tracking
- Distance-based telemetry (odometer, conveyor length, rail position)
- Any data with `(sensor_id, time|distance, value)` pattern

### Structure

```sql
-- Time axis
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,    -- Tag name (sensor identifier)
    time DATETIME BASETIME,               -- Timestamp
    value DOUBLE SUMMARIZED,              -- Rollup target value
    other_value DOUBLE                    -- Additional measured value
) WITH ROLLUP;

-- Distance axis
CREATE TAG TABLE conveyor_profile (
    line_id VARCHAR(20) PRIMARY KEY,
    distance_m DOUBLE BASE DISTANCE,
    vibration DOUBLE,
    temperature DOUBLE
);
```

### Key Features

**Rollup Statistics (Time Axis Only)**:
```sql
-- Raw data
INSERT INTO sensors VALUES ('sensor01', NOW, 25.3);

-- Hourly statistics through the rollup expression
SELECT rollup('hour', 1, time) AS hour_time, AVG(value), COUNT(value)
FROM sensors
GROUP BY hour_time;
```

Create the table with `WITH ROLLUP` or define rollups with `CREATE ROLLUP` before using
the rollup expression. Distance-axis tag tables use range queries and bucket aggregations
instead of rollups.

**Metadata Layer**:
```sql
-- Separate table for sensor metadata
SELECT * FROM sensors._META;

-- Add custom metadata columns
ALTER TABLE sensors._META ADD COLUMN location VARCHAR(100);
UPDATE sensors._META SET location = 'Building A' WHERE name = 'sensor01';
```

**Performance**:
- Millions of inserts per second
- Ultra-fast queries by tag + axis range
- Automatic 3-level partitioned indexing

### Best Practices

**DO**:
- Use for multi-sensor data (1000s of sensors in one table)
- Mark the rollup target column as SUMMARIZED
- Query rollup tables for statistics on time-axis tables
- Use metadata table for sensor info

**DON'T**:
- Create separate tables for each sensor
- Try to UPDATE data values (use metadata for updates)
- Use for non-sensor data

### Example Use Cases

```sql
-- Manufacturing: Equipment sensors
CREATE TAG TABLE equipment_telemetry (
    equipment_id VARCHAR(50) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED,
    vibration DOUBLE,
    rpm DOUBLE,
    power_consumption DOUBLE
);

-- Smart City: Environmental monitoring
CREATE TAG TABLE air_quality (
    station_id VARCHAR(30) PRIMARY KEY,
    time DATETIME BASETIME,
    pm25 DOUBLE SUMMARIZED,
    pm10 DOUBLE,
    co2 DOUBLE,
    temperature DOUBLE
);

-- Distance axis: Conveyor or route profile
CREATE TAG TABLE route_profile (
    route_id VARCHAR(30) PRIMARY KEY,
    distance_m DOUBLE BASE DISTANCE,
    vibration DOUBLE,
    temperature DOUBLE
);
```

## Log Table Deep Dive

### When to Use

Perfect for:
- Application logs
- Event streams
- Access logs
- Transaction logs
- Any time-stamped events with variable schema

### Structure

```sql
CREATE TABLE app_logs (
    level VARCHAR(10),
    component VARCHAR(50),
    message VARCHAR(2000),
    user_id INTEGER,
    ip_addr IPV4
    -- _arrival_time automatically added!
);
```

### Key Features

**Automatic Timestamps**:
```sql
-- You insert
INSERT INTO app_logs VALUES ('ERROR', 'DB', 'Connection timeout', 123, '192.168.1.1');

-- Machbase stores with nanosecond timestamp
-- _arrival_time: 2025-10-10 14:23:45.123456789
```

**Full-Text Search**:
```sql
-- Create a keyword index before using SEARCH
CREATE INDEX idx_app_logs_message ON app_logs(message) INDEX_TYPE KEYWORD;

-- Fast text search
SELECT * FROM app_logs
WHERE message SEARCH 'timeout'
  AND level = 'ERROR';
```

**Flexible Schema**:
- Any number of columns
- Any data types
- No fixed pattern required

**Performance**:
- Millions of inserts per second
- Newest data returned first (automatic ordering)
- Optional LSM indexing for fast lookups

### Best Practices

**DO**:
- Use for variable event data
- Leverage SEARCH for text queries
- Use DURATION for time-based queries
- Implement retention policies

**DON'T**:
- Use for sensor data (use Tag table instead)
- Store reference data (use Lookup table)
- Expect UPDATE/DELETE by key

### Example Use Cases

```sql
-- Application monitoring
CREATE TABLE application_events (
    app_name VARCHAR(50),
    event_type VARCHAR(50),
    severity VARCHAR(20),
    message VARCHAR(2000),
    user_id INTEGER,
    session_id VARCHAR(100),
    stack_trace VARCHAR(4000)
);

-- Web server access logs
CREATE TABLE http_access (
    method VARCHAR(10),
    uri VARCHAR(1000),
    status_code INTEGER,
    response_time INTEGER,
    client_ip IPV4,
    user_agent VARCHAR(500),
    referer VARCHAR(500)
);

-- Financial transactions
CREATE TABLE transactions (
    transaction_id VARCHAR(50),
    account_id INTEGER,
    transaction_type VARCHAR(30),
    amount DOUBLE,
    currency VARCHAR(3),
    status VARCHAR(20),
    description VARCHAR(500)
);
```

## Volatile Table Deep Dive

### When to Use

Perfect for:
- Real-time dashboards
- Session management
- Live status boards
- Caching layer
- Temporary data requiring UPDATE/DELETE by primary key

### Structure

```sql
CREATE VOLATILE TABLE live_status (
    device_id INTEGER PRIMARY KEY,    -- PRIMARY KEY required for updates
    status VARCHAR(20),
    last_value DOUBLE,
    last_updated DATETIME
);
```

### Key Features

**UPDATE and DELETE by Key**:
```sql
-- Update existing record
UPDATE live_status
SET status = 'RUNNING', last_value = 25.3, last_updated = NOW
WHERE device_id = 101;

-- Delete specific record
DELETE FROM live_status WHERE device_id = 101;
```

**Non-Persistent Memory Primary-Key Table**:
- All data in RAM
- A single primary-key memory index
- Extremely fast reads/writes
- 10,000s of operations per second

**WARNING: Non-Persistent**:
- Data lost on server restart
- Archive important data before shutdown

### Best Practices

**DO**:
- Use PRIMARY KEY for fast lookups
- Keep data volume small (limited by RAM)
- Archive to Log/Tag tables periodically
- Use for current state only

**DON'T**:
- Store data that must persist
- Use for high-volume streaming data
- Expect data to survive restarts

### Example Use Cases

```sql
-- Real-time equipment status
CREATE VOLATILE TABLE equipment_status (
    equipment_id INTEGER PRIMARY KEY,
    online CHAR(1),
    current_temp DOUBLE,
    current_pressure DOUBLE,
    last_heartbeat DATETIME
);

-- Active user sessions
CREATE VOLATILE TABLE user_sessions (
    session_token VARCHAR(100) PRIMARY KEY,
    user_id INTEGER,
    ip_address IPV4,
    login_time DATETIME,
    last_activity DATETIME,
    expires_at DATETIME
);

-- Live monitoring cache
CREATE VOLATILE TABLE monitoring_cache (
    metric_key VARCHAR(100) PRIMARY KEY,
    metric_value VARCHAR(500),
    updated_at DATETIME
);
```

## Lookup Table Deep Dive

### When to Use

Perfect for:
- Device registries
- Configuration tables
- Category/dimension tables
- Master data
- Persistent reference data accessed by one primary key

### Structure

```sql
CREATE LOOKUP TABLE devices (
    device_id VARCHAR(20) PRIMARY KEY,
    device_name VARCHAR(100),
    location VARCHAR(200),
    device_type VARCHAR(50),
    owner VARCHAR(100)
);
```

### Key Features

**Full CRUD Support by Primary Key**:
```sql
-- Insert
INSERT INTO devices VALUES ('sensor01', 'Sensor A', 'Building 1', 'Temperature', 'Facilities');

-- Update
UPDATE devices SET location = 'Building 2' WHERE device_id = 'sensor01';

-- Delete
DELETE FROM devices WHERE device_id = 'sensor01';

-- Select
SELECT * FROM devices WHERE device_id = 'sensor01';
```

**JOIN with Time-Series**:
```sql
-- Enrich sensor data with device info
SELECT s.*, d.device_name, d.location
FROM sensors s
JOIN devices d ON s.sensor_id = d.device_id
WHERE s.time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
                 AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

**Persistent Data with a Memory Primary-Key Index**:
- Data persists across restart
- A single primary-key memory index supports fast key access
- Full DML is designed around primary-key predicates

### Best Practices

**DO**:
- Use for reference/master data
- JOIN with Tag/Log tables
- Design access around the primary key
- Keep data volume reasonable (<1M rows ideal)

**DON'T**:
- Use for high-frequency inserts
- Store time-series data
- Expect millions of writes per second

### Example Use Cases

```sql
-- Device registry
CREATE LOOKUP TABLE device_registry (
    device_id VARCHAR(50) PRIMARY KEY,
    device_name VARCHAR(100),
    device_type VARCHAR(50),
    location VARCHAR(200),
    installation_date DATETIME,
    status VARCHAR(20)
);

-- Configuration management
CREATE LOOKUP TABLE system_config (
    config_key VARCHAR(100) PRIMARY KEY,
    config_value VARCHAR(500),
    config_category VARCHAR(50),
    description VARCHAR(500)
);

-- User management
CREATE LOOKUP TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(200),
    role VARCHAR(50),
    created_at DATETIME
);
```

## RDB Table Deep Dive

### When to Use

Perfect for:
- Equipment master data
- Alarm rules and current alarm state
- Work queues
- Dimension tables joined with Tag or Log data
- Generalized disk row data that must persist and support indexed predicates

### Structure

```sql
CREATE RDB TABLE device_master (
    id         INTEGER PRIMARY KEY,
    name       VARCHAR(64) NOT NULL,
    site       VARCHAR(32) DEFAULT 'SEOUL',
    state      VARCHAR(16),
    info       JSON,
    updated_at DATETIME
);
```

### Key Features

**Full DML support on disk rows**:
```sql
INSERT INTO device_master(id, name, state) VALUES (1, 'pump-01', 'READY');

UPDATE device_master
   SET state = 'RUNNING'
 WHERE id = 1;

DELETE FROM device_master
 WHERE id = 1;
```

**Indexes and constraints**:
```sql
CREATE INDEX idx_device_site ON device_master(site);
CREATE UNIQUE INDEX uidx_device_name ON device_master(name);
CREATE PRIMARY KEY INDEX pk_device_id ON device_master(id);
CREATE INDEX idx_device_owner ON device_master(info->'$.owner');
```

**Backup and mount integration**:
RDB table data is included in database and table backup images. Mounted databases can read RDB tables and views, but mounted RDB objects are read-only.

### Best Practices

**DO**:
- Use for persistent operational state that changes by row
- Add indexes for frequent lookup predicates
- Use RDB tables as dimensions in joins with Tag and Log data
- Use when Lookup's single primary-key model is too narrow

**DON'T**:
- Use for high-volume sensor ingestion (use Tag or Log instead)
- Use in cluster edition
- Expect backend-native SQL passthrough

## Performance Comparison

### Write Performance

| Table Type | Inserts/sec | UPDATE Support | DELETE Support |
|-----------|-------------|----------------|----------------|
| Tag | Millions | Metadata only | Time-based |
| Log | Millions | No | Time-based |
| Volatile | 10,000s | By PRIMARY KEY | By PRIMARY KEY |
| Lookup | 100s | Yes | Yes |
| RDB | Workload-dependent | Yes | Yes |

### Read Performance

| Table Type | Read Speed | Best For | Index Type |
|-----------|-----------|----------|------------|
| Tag | Very Fast | sensor_id + time | 3-level partitioned |
| Log | Fast | Time range | Optional log indexes |
| Volatile | Very Fast | PRIMARY KEY | Red-black tree |
| Lookup | Fast | PRIMARY KEY | Memory primary-key index |
| RDB | Fast | Indexed predicates | RDB indexes |

### Storage

| Table Type | Storage | Compression | Persistence |
|-----------|---------|-------------|-------------|
| Tag | Disk | 10-100x | Yes |
| Log | Disk | 10-100x | Yes |
| Volatile | Memory | None | No |
| Lookup | Persistent + memory index | Moderate | Yes |
| RDB | Disk | Backend-dependent | Yes |

## Combining Table Types

### Pattern: IoT Platform

```sql
-- Tag: Sensor readings
CREATE TAG TABLE sensor_data (...);

-- Lookup: Device registry
CREATE LOOKUP TABLE devices (...);

-- RDB: Current device state and work queue
CREATE RDB TABLE device_state (...);

-- Volatile: Live status
CREATE VOLATILE TABLE device_status (...);

-- Log: Events and alerts
CREATE TABLE device_events (...);
```

### Pattern: Web Application

```sql
-- Log: Access logs
CREATE TABLE http_access (...);

-- Log: Application logs
CREATE TABLE app_logs (...);

-- Volatile: Active sessions
CREATE VOLATILE TABLE sessions (...);

-- Lookup: User accounts
CREATE LOOKUP TABLE users (...);

-- RDB: Orders and workflow state
CREATE RDB TABLE orders (...);
```

### Pattern: Manufacturing

```sql
-- Tag: Equipment sensors
CREATE TAG TABLE equipment_telemetry (...);

-- Log: Production events
CREATE TABLE production_log (...);

-- Volatile: Line status
CREATE VOLATILE TABLE line_status (...);

-- Lookup: Equipment catalog
CREATE LOOKUP TABLE equipment_catalog (...);

-- RDB: Alarm rules and active alarm state
CREATE RDB TABLE alarm_state (...);
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Wrong Table for Use Case

**Bad**: Using Log table for sensor data
```sql
-- Don't do this!
CREATE TABLE sensors (sensor_id VARCHAR(20), value DOUBLE);
```

**Good**: Use Tag table
```sql
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

### Anti-Pattern 2: One Table Per Sensor

**Bad**: Creating 1000 tables for 1000 sensors
```sql
CREATE TAG TABLE sensor001 (...);
CREATE TAG TABLE sensor002 (...);
-- ... 998 more tables
```

**Good**: One table for all sensors
```sql
CREATE TAG TABLE all_sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    ...
);
```

### Anti-Pattern 3: Storing History in Volatile

**Bad**: Using Volatile for persistent data
```sql
-- Data will be lost on restart!
CREATE VOLATILE TABLE important_transactions (...);
```

**Good**: Use Log or Tag table
```sql
CREATE TABLE important_transactions (...);
```

### Anti-Pattern 4: High-Frequency Writes to Lookup

**Bad**: Millions of inserts to Lookup table
```sql
-- Too slow!
CREATE LOOKUP TABLE sensor_readings (...);
```

**Good**: Use Tag or Log table
```sql
CREATE TAG TABLE sensor_readings (...);
```

## Migration Guide

### From Other Databases

**From PostgreSQL/MySQL**:
- Event tables → Log tables
- Operational row tables → RDB tables
- Time-series tables → Tag tables
- Temp tables → Volatile tables
- Dimension tables → Lookup tables

**From InfluxDB**:
- Measurements → Tag tables
- Tags → Tag primary key + metadata
- Fields → a SUMMARIZED value column plus regular value columns

**From MongoDB**:
- Time-series collections → Tag/Log tables
- Reference collections → Lookup tables
- Capped collections → Log tables with retention

## Summary Matrix

| Feature | Tag | Log | Volatile | Lookup | RDB |
|---------|-----|-----|----------|--------|-----|
| **Primary Use** | Sensors | Events | Cache | Reference | Row state |
| **Schema** | Fixed pattern | Flexible | Flexible | Flexible | Flexible |
| **Writes/sec** | Millions | Millions | 10,000s | 100s | Workload-dependent |
| **UPDATE** | Metadata | No | Yes | Yes | Yes |
| **DELETE** | Time-based | Time-based | By key | By key | Yes |
| **Storage** | Disk | Disk | Memory | Disk | Disk |
| **Persistence** | Yes | Yes | No | Yes | Yes |
| **Rollup** | When configured | No | No | No | No |
| **Best Query** | ID + time | Time | Key | Primary key | Indexed predicates |
| **Compression** | Very high | High | None | Moderate | Backend-dependent |

## Next Steps

- **Deep Dive**: [Indexing and Performance](../indexing/) - Optimize queries
- **Detailed Reference**: [Table Types](../../table-types/) - Complete documentation
- **Hands-On**: [Table Types](../../table-types/) - Practice with real examples

## Key Takeaways

1. **Tag tables** for sensor/device data with rollup support
2. **Log tables** for flexible event streams and logs
3. **Volatile tables** for in-memory, update-able data
4. **Lookup tables** for persistent primary-key reference data
5. **RDB tables** for generalized disk row data
6. **Combine types** for complete solutions
7. **Choose wisely** - table type determines performance

---

Master table selection and build efficient Machbase applications!
