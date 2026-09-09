---
type: docs
title: '4.5 Modeling Patterns'
weight: 50
toc: true
---
This page covers data modeling patterns commonly used in production.

Each section's SQL demonstrates a different model. Choose the relevant section and run it
in a separate practice environment after checking for existing tables with the same names.
Creating schemas does not automatically run collection, aggregation, or cache updates.
Also design the work performed by ingestion applications or schedulers and its failure handling.

- **[Time-Axis Modeling](/dbms/data-modeling-table-design/patterns-modeling/#time-axis-modeling)**
- **[Distance-Axis Modeling](/dbms/data-modeling-table-design/patterns-modeling/#distance-axis-modeling)**
- **[State and Cache Modeling](/dbms/data-modeling-table-design/patterns-modeling/#state-cache-status-modeling)**
- **[Event and Log Modeling](/dbms/data-modeling-table-design/patterns-modeling/#event-log-modeling-logs)**
- **[Reference and Master Data](/dbms/data-modeling-table-design/patterns-modeling/#reference-master-modeling)**
- **[Persistent and Temporary Data](/dbms/data-modeling-table-design/patterns-modeling/#persistent-temporary)**
- **[INSERT and UPDATE Patterns](/dbms/data-modeling-table-design/patterns-modeling/#insert-update)**
- **[JOIN and Metadata Design](/dbms/data-modeling-table-design/patterns-modeling/#join-metadata-design)**
- **[Combined Table Types](/dbms/data-modeling-table-design/patterns-modeling/#table-types-patterns-combined-type)**


<a id="time-axis-modeling"></a>

## Time-axis modeling

This pattern uses time as the primary axis and suits sensor measurements, energy monitoring,
and environmental data.

One row represents one observation from one meter. Define `time` as measurement time, not
arrival time, and document whether `kwh` is a cumulative reading or interval consumption.
The following schema assumes voltage and current belong to the same observation. If their
measurement intervals or timestamps differ, store separate series or define missing-value
rules instead of forcing them into one row.

### Basic pattern: TAG table

```sql
CREATE TAG TABLE power_meter (
    meter_id  VARCHAR(32) PRIMARY KEY,
    time      DATETIME    BASETIME,
    kwh       DOUBLE,
    voltage   DOUBLE,
    current   DOUBLE
) METADATA (
    location  VARCHAR(64),
    phase     SHORT,
    rating_kw DOUBLE
);
```

### Time-range aggregation

```sql
-- Hourly average and maximum meter readings (last 24 hours)
SELECT meter_id,
       DATE_TRUNC('hour', time, 1) AS hour,
       AVG(kwh) AS avg_kwh,
       MAX(kwh) AS peak_kwh
FROM power_meter
WHERE time >= NOW - 86400000000000
GROUP BY meter_id, hour
ORDER BY meter_id, hour;
```

If `kwh` is cumulative energy, this average is the mean meter reading, not hourly consumption.
Calculate interval consumption from the difference between start and end readings, accounting
for meter resets, replacement, and rollover. Also distinguish power (kW) from energy (kWh)
in column names and units.

### Multiple-resolution storage

Store high-resolution raw data and lower-resolution aggregates in separate tables.

```sql
-- Raw data (second-level resolution)
CREATE TAG TABLE power_raw (
    meter_id VARCHAR(32) PRIMARY KEY,
    time     DATETIME    BASETIME,
    kwh      DOUBLE
);

-- One-minute aggregates (cached in VOLATILE or a separate TAG table)
CREATE VOLATILE TABLE power_1min (
    key_id   VARCHAR(80) PRIMARY KEY,
    meter_id VARCHAR(32),
    ts       DATETIME,
    avg_kwh  DOUBLE,
    max_kwh  DOUBLE
);
```

This DDL creates storage only. The application must assign `key_id` values in `power_1min` that
uniquely identify each meter and interval, then populate aggregates. VOLATILE results disappear
on restart, so do not use it for long-term aggregate retention. Keep statistics needed after
raw-data deletion in persistent TAG tables or supported ROLLUPs, and check each retention policy.

### Time zone handling

DATETIME represents an instant; connection time zones affect string input and output. To
display Korean time, configure the client's time zone. Adding nine hours to a stored timestamp
changes the instant itself rather than displaying the same instant in another time zone.

```sql
-- Check the client time zone, then query the original timestamp
SELECT meter_id,
       time,
       kwh
FROM power_meter
WHERE meter_id = 'MTR-001'
  AND time >= '2024-01-01 00:00:00';
```

If input and connection time zones differ, align them before ingestion. For a JDBC `TIMEZONE`
example, see [JDBC Connections](/dbms/development-tools-integration/jdbc/).

<a id="distance-axis-modeling"></a>

## Distance-axis modeling

This pattern uses distance or position as the primary axis and suits pipeline inspection,
road sensors, and laser scans.

A distance axis is not another display format for time. Time-axis ROLLUP and retention rules
cannot be applied unchanged. For repeated inspections of a pipe, define an inspection-run
identifier or table separation rule so `pipe_id` does not mix runs. This example assumes
one inspection of one pipe, with distance in m and thickness in mm.

### Basic pattern

```sql
CREATE TAG TABLE pipeline_thickness (
    pipe_id   VARCHAR(32) PRIMARY KEY,
    distance  DOUBLE      BASEDISTANCE,    -- Unit: meters
    thickness DOUBLE,
    temp      DOUBLE
);
```

### Query a range

```sql
-- Query the 0–50 m range for a pipe
SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
  AND distance BETWEEN 0.0 AND 50.0
ORDER BY distance;

-- Query locations below the threshold
SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
  AND thickness < 8.0   -- Thickness below 8 mm
ORDER BY distance;
```

### Distance-based aggregation

```sql
-- Average thickness for each 10 m segment
SELECT pipe_id,
       FLOOR(distance / 10.0) * 10 AS segment_start,
       AVG(thickness) AS avg_thickness,
       MIN(thickness) AS min_thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
GROUP BY pipe_id, FLOOR(distance / 10.0) * 10
ORDER BY segment_start;
```

### Combine time and distance

To manage inspection time and position together, add a distance column to a time-axis TAG table.

```sql
-- Store a time axis with position information
CREATE TAG TABLE inspection_data (
    inspector  VARCHAR(64) PRIMARY KEY,
    time       DATETIME    BASETIME,
    distance   DOUBLE,      -- Position column, not an axis
    thickness  DOUBLE,
    defect     SHORT
);

-- Query a specific date and distance range
SELECT inspector, time, distance, thickness
FROM inspection_data
WHERE inspector = 'INSPECTOR-01'
  AND time BETWEEN '2024-01-01' AND '2024-01-02'
  AND distance BETWEEN 100.0 AND 200.0
ORDER BY time;
```

<a id="state-cache-status-modeling"></a>

## State and cache modeling

This cache pattern supports real-time queries of current device or sensor state.

### Latest-state cache

Cache each device's current state in a VOLATILE table.

```sql
-- State cache (VOLATILE)
CREATE VOLATILE TABLE device_status (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

-- State history (TAG or LOG)
CREATE TAG TABLE device_status_history (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    status VARCHAR(16)
);
```

### State update flow

The following SQL updates history and cache separately. The two writes are not one
transaction, and their separately evaluated `NOW` values need not match. In actual ingestion,
choose the measurement timestamp once and pass it to both paths. Define event ordering and
concurrent update handling in the application so late historical values do not overwrite
the latest cache.

```sql
-- On receiving a new measurement:
-- 1. Store history in TAG
INSERT INTO device_status_history VALUES ('DEV-01', NOW, 78.5, 'WARNING');

-- 2. Update the VOLATILE cache (ON DUPLICATE KEY UPDATE)
INSERT INTO device_status VALUES ('DEV-01', 'WARNING', 78.5, NOW)
ON DUPLICATE KEY UPDATE SET status = 'WARNING', value = 78.5, updated_at = NOW;
```

### Dashboard queries

```sql
-- All devices currently in an alarm state
SELECT device_id, status, value, updated_at
FROM device_status
WHERE status IN ('ALARM', 'WARNING')
ORDER BY updated_at DESC;

-- Latest state of a specific device
SELECT device_id, status, value, updated_at
FROM device_status
WHERE device_id = 'DEV-01';
```

### State definition reference

Manage the meaning of state codes in LOOKUP.

```sql
CREATE LOOKUP TABLE status_definition (
    code    VARCHAR(16) PRIMARY KEY,
    label   VARCHAR(64),
    color   VARCHAR(16),
    severity SHORT
);

INSERT INTO status_definition VALUES ('NORMAL', 'Normal', 'green', 0);
INSERT INTO status_definition VALUES ('WARNING', 'Warning', 'yellow', 1);
INSERT INTO status_definition VALUES ('ALARM', 'Alarm', 'red', 2);

-- Query with JOIN
SELECT d.device_id, s.label, s.color, d.value
FROM device_status d
JOIN status_definition s ON d.status = s.code
ORDER BY s.severity DESC;
```

<a id="event-log-modeling-logs"></a>

## Event and log modeling

Use LOG tables to model system events, alarms, and audit logs.

### Hierarchical event model

```sql
-- Alarm event LOG table
CREATE LOG TABLE alarm_event (
    severity    SHORT,          -- 1=INFO, 2=WARN, 3=ERROR, 4=CRITICAL
    category    VARCHAR(32),    -- Category
    source      VARCHAR(64),    -- Event source
    message     VARCHAR(512),
    src_ip      IPV4            -- Source IP, if available
);

-- System audit LOG table
CREATE LOG TABLE audit_log (
    user_id    VARCHAR(64),
    action     VARCHAR(32),    -- INSERT, UPDATE, DELETE, LOGIN, etc.
    target     VARCHAR(128),   -- Target table/resource
    detail     TEXT,           -- Details for full-text search
    result     VARCHAR(8)      -- SUCCESS, FAILURE
);

CREATE INDEX idx_audit_detail ON audit_log(detail) INDEX_TYPE KEYWORD;
```

### Alarm aggregation

```sql
-- Alarm counts by severity over the last hour
SELECT severity, COUNT(*) AS cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 3600000000000
GROUP BY severity
ORDER BY severity DESC;

-- Alarm summary by source over the last 24 hours
SELECT source, COUNT(*) AS total,
       SUM(CASE WHEN severity = 4 THEN 1 ELSE 0 END) AS critical_cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 86400000000000
GROUP BY source
ORDER BY total DESC;
```

### Log level filtering

```sql
-- ERROR or higher over the last 10 minutes
SELECT _arrival_time, source, message
FROM alarm_event
WHERE severity >= 3
  AND _arrival_time >= NOW - 600000000000
ORDER BY _arrival_time DESC
LIMIT 100;
```

### Full-text search

```sql
-- Audit logs containing a keyword
SELECT _arrival_time, user_id, action, target
FROM audit_log
WHERE detail SEARCH 'password'
  AND _arrival_time >= NOW - 86400000000000;
```

<a id="reference-master-modeling"></a>

## Reference and master data modeling

Use LOOKUP for reference data such as code tables, equipment master data, and user information.

Storing only identifiers in history avoids repeating names and locations. However, changing
a location in current master data also changes joined historical results. If the production
line at event time matters, model separate change history with validity periods or record
those attributes in the original row. The following hierarchy does not automatically enforce
references through foreign keys; applications must reject nonexistent factory and line codes.

### Hierarchical code system

```sql
-- Main category codes
CREATE LOOKUP TABLE category_main (
    code  VARCHAR(8)  PRIMARY KEY,
    label VARCHAR(64)
);

-- Subcategory codes (reference main category)
CREATE LOOKUP TABLE category_sub (
    code      VARCHAR(16) PRIMARY KEY,
    main_code VARCHAR(8),
    label     VARCHAR(64)
);

CREATE INDEX idx_sub_main ON category_sub(main_code);
```

### Equipment master hierarchy

```sql
-- Factory master
CREATE LOOKUP TABLE factory (
    factory_id VARCHAR(16) PRIMARY KEY,
    name       VARCHAR(64),
    location   VARCHAR(128)
);

-- Production line master (references factory)
CREATE LOOKUP TABLE production_line (
    line_id    VARCHAR(16) PRIMARY KEY,
    factory_id VARCHAR(16),
    name       VARCHAR(64)
);

-- Equipment master (references production line)
CREATE LOOKUP TABLE equipment (
    equip_id   VARCHAR(32) PRIMARY KEY,
    line_id    VARCHAR(16),
    equip_name VARCHAR(128),
    equip_type VARCHAR(32),
    install_dt DATETIME
);

CREATE INDEX idx_equip_line ON equipment(line_id);
CREATE INDEX idx_equip_type ON equipment(equip_type);
```

### Master data joins

Store equipment identifiers in the measurement table and attributes such as factory, line,
and equipment names once in LOOKUP tables. First restrict the measurement time range, then
join LOOKUP tables by equipment identifier. For join syntax and plan inspection, see
[JOIN and Subqueries](/dbms/tag-table-usage/query-analysis/).

<a id="persistent-temporary"></a>

## Combine persistent and temporary data

Keep authoritative data in persistent tables (TAG, LOG, TRANSACTION, LOOKUP) and query caches
in VOLATILE. Do not assume the two writes share one transaction. Design for cache lag and
reconstruction after failure.

### Raw data and aggregate cache

Store raw data in a persistent table and aggregate results in VOLATILE.

```sql
-- Raw data (persistent TAG)
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- Aggregate cache (temporary VOLATILE)
CREATE VOLATILE TABLE sensor_recent_avg (
    key_id    VARCHAR(64) PRIMARY KEY,
    sensor_id VARCHAR(64),
    base_ts   DATETIME,
    avg_val   DOUBLE,
    max_val   DOUBLE,
    cnt       LONG
);
```

### Cache refresh

One cache row holds a sensor's last two hours of statistics. `base_ts` is the latest included
measurement timestamp, not the aggregation window boundary. Use the same range definition
each time. For results at an identical instant, choose one reference timestamp per execution.
The example excludes future measurements. When comparing results, replace each SQL's `NOW`
with the same fixed reference timestamp to calculate both lower and upper bounds.

```sql
-- Periodic aggregate refresh (run hourly)
DELETE FROM sensor_recent_avg;

INSERT INTO sensor_recent_avg
SELECT name AS key_id,
       name,
       MAX(time) AS base_ts,
       AVG(value),
       MAX(value),
       COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000 * 2  -- Recalculate the last two hours
  AND time <= NOW
GROUP BY name;
```

Do not append `ON DUPLICATE KEY UPDATE` to `INSERT ... SELECT`. Rebuild the cache by
deleting its contents and loading it again.

Between deletion and reload, other queries may see an empty or partially populated cache.
Define application behavior during refresh, retries after failure, and fallback to raw-data
queries. If a consistently complete result is required, consider a separate switchover or
transaction model that provides it.

### Optimize dashboard queries

```sql
-- Query the stored cache (the application handles fallback to raw data)
SELECT sensor_id, base_ts, avg_val, max_val
FROM sensor_recent_avg
WHERE base_ts >= NOW - 3600000000000 * 2
  AND base_ts <= NOW
ORDER BY sensor_id, base_ts;
```

This predicate displays cache rows whose latest measurement is within the last two hours.
It does not recalculate stored averages relative to query time. Manage aggregate freshness
through the refresh interval.

### Failure recovery

If a server restart removes the VOLATILE table and cache, first recreate the table, then
recalculate the same last-two-hour statistics from TAG. Run the following CREATE only after
a restart in which the table disappeared. The source retention period must still include
the data needed for recalculation.

```sql
-- Rebuild the cache after server restart
CREATE VOLATILE TABLE sensor_recent_avg (
    key_id    VARCHAR(64) PRIMARY KEY,
    sensor_id VARCHAR(64),
    base_ts   DATETIME,
    avg_val   DOUBLE,
    max_val   DOUBLE,
    cnt       LONG
);

INSERT INTO sensor_recent_avg
SELECT name,
       name, MAX(time), AVG(value), MAX(value), COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000 * 2  -- Same last-two-hour range as normal refresh
  AND time <= NOW
GROUP BY name;
```

After recovery, compare per-sensor counts, averages, and latest timestamps with raw-data
aggregates at the same reference time. `cnt` includes rows with NULL measurements. Store
`COUNT(value)` separately if the sample count used for the average is needed.

<a id="insert-update"></a>

## INSERT and UPDATE patterns

The model must decide which data can change. This page does not redefine the DML support
matrix. Use [Data Mutation Policy](../alter-data-mutation-policy/) for table-specific conditions
and [Data Input and Export](/dbms/development-tools-integration/data-input-load-export/) to
choose INSERT, Append, or file ingestion.

<a id="join-metadata-design"></a>

## JOIN and metadata design

Apply these principles when combining table types.

First define join cardinality. Check whether each sensor code has exactly one master row or
is reused across factories. If one source row matches several reference rows, result counts
and aggregates such as SUM can be duplicated. Match identity scope and types, not just code names.

1. Review join order using filtered row counts and execution plans, not only raw row counts.
2. Match JOIN column types and check supported index usage.
3. Reduce joined rows with explicit time ranges and business predicates in WHERE.
4. For queries that include TAG attributes, consider METADATA instead of separate LOOKUP tables.

For reproducible join examples, see [TAG Queries and Analysis](/dbms/tag-table-usage/query-analysis/)
and [LOOKUP Queries and Analysis](/dbms/lookup-table-usage/query-analysis/).

<a id="table-types-patterns-combined-type"></a>

## Combined table types

These common designs combine multiple table types in production systems.

### Manufacturing equipment monitoring

```text
┌───────────────────────────────────────────────────────────────┐
│                 Equipment monitoring system                   │
├───────────────────┬───────────────────┬───────────────────────┤
│ TAG               │ LOG               │ LOOKUP                │
│ sensor_data       │ alarm_event       │ equipment_master      │
│ Measurement       │ Alarm events      │ Equipment reference   │
│ history           │                   │ data                  │
├───────────────────┴───────────────────┴───────────────────────┤
│ VOLATILE                                                      │
│ sensor_latest (latest-value cache)                             │
└───────────────────────────────────────────────────────────────┘
```

### Logistics and order management (Standard Edition)

```text
┌───────────────────────────────────────────────────────────────┐
│                   Logistics management system                 │
├───────────────────┬───────────────────┬───────────────────────┤
│ TRANSACTION       │ LOG               │ LOOKUP                │
│ orders            │ delivery_log      │ product_master        │
│ Order management  │ Delivery events   │ Product reference     │
│ UPDATE/DELETE     │                   │ data                  │
├───────────────────┴───────────────────┴───────────────────────┤
│ VOLATILE                                                      │
│ order_status_cache (current-state cache)                       │
└───────────────────────────────────────────────────────────────┘
```

### Pattern summary

| Role | Recommended type | Reason |
|------|---------|------|
| High-frequency measurement history | TAG | High-speed Append API buffers, time-series optimization |
| Event and alarm logs | LOG | Append-only, automatic arrival time |
| Relational business data (UPDATE/DELETE) | TRANSACTION | SELECT/INSERT/UPDATE/DELETE all supported |
| Reference and code data | LOOKUP | PK identity, general-predicate UPDATE/DELETE, persistence |
| Real-time state cache | VOLATILE | In-memory speed, UPSERT |

---

Read next:

- [SELECT GROUP BY and Aggregation](/dbms/reference/sql/syntax/select-syntax/)
- [Operations and Configuration](/dbms/operations-configuration-recovery/)
