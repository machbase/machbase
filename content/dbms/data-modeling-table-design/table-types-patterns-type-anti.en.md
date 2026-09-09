---
type: docs
title: '4.4 Anti-Patterns'
weight: 40
toc: true
---
An anti-pattern is a use that conflicts with data semantics and requirements, not simply the
choice of a particular table type. Check whether each example's assumptions apply to your
workload before choosing an alternative. The same schema may suit current state but not history.

- **[Unbounded History in LOOKUP](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#high-frequency-lookup)**
- **[One Table per Sensor](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#per-sensor-create)**
- **[Incorrect Table Type](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#table-types-selection-type-wrong)**
- **[VOLATILE as Persistent Storage](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#storage-persistent-volatile)**
- **[Misusing TRANSACTION for Time Series](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#time-series-storage-misuse-rdb)**


<a id="high-frequency-lookup"></a>

<a id="고빈도-lookup-조회"></a>

## Unbounded history in LOOKUP

### Problem

The issue is not query frequency itself, but storing continuously growing measurement history
in LOOKUP. LOOKUP keeps all rows and indexes in memory, so long-term history increases memory
pressure. It suits repeated key lookups on small reference datasets.

### Anti-pattern example

```sql
-- Incorrect design: sensor measurements in LOOKUP
CREATE LOOKUP TABLE sensor_data_wrong (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    ts         DATETIME
);

-- sensor_id is the PK, so this schema holds only one current row per sensor
-- Appending history with the same PK causes a conflict
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.3, NOW);
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.5, NOW);  -- Duplicate PK error
```

### Correct pattern

Consider TAG when collection and querying focus on per-tag measurement history. LOOKUP can
assign a distinct key to each measurement, but all history still resides in memory. Add a
VOLATILE latest-value cache only when performance requires it and it is rebuildable from raw
data. If TAG latest-value queries meet the requirement, no separate cache is needed.

```sql
-- Correct design: history in TAG
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- Latest-value cache in VOLATILE
CREATE VOLATILE TABLE sensor_latest (
    sensor_id VARCHAR(64) PRIMARY KEY,
    value     DOUBLE,
    updated_at DATETIME
);
```

### Result

| | Anti-pattern (LOOKUP) | Correct design (TAG) |
|-|-----------------|-----------------|
| History under the same sensor key | No (the sample sensor key identifies a row) | Yes (multiple measurements under a tag name) |
| Continuous ingestion path | Row-identifier based | Time-series Append API available |
| Time-range queries | General predicates | Tag/time-axis queries |

<a id="per-sensor-create"></a>

## One table per sensor

### Problem

Creating a separate table for each sensor or tag increases DDL, privileges, and query targets
as sensor counts grow, raising operational costs.

### Anti-pattern example

```sql
-- Incorrect design: one table per sensor
CREATE TAG TABLE sensor_temp_01 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE sensor_temp_02 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE sensor_temp_03 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
-- ... 10,000 sensors require 10,000 tables
```

### Consequences

| Problem | Description |
|------|------|
| Management complexity | DDL management for every table |
| Query complexity | Combining tables for cross-sensor aggregates |
| Metadata growth | Increased system catalog load |
| Adding a sensor | DDL required each time |

### Correct pattern

Store all sensor data in one TAG table with sensor names as the PRIMARY KEY.

This applies to sensors sharing column structure, privileges, and retention policies.
Separate tables may be appropriate when units, schemas, access privileges, or retention
periods require independent management. Sensor count alone should not determine table separation.

```sql
-- Correct design: all temperature sensors in one table
CREATE TAG TABLE temperature_sensor (
    name   VARCHAR(128) PRIMARY KEY,
    time   DATETIME     BASETIME,
    value  DOUBLE
);

-- Insert all sensor data into one table
INSERT INTO temperature_sensor VALUES ('TEMP-01', NOW, 23.5);
INSERT INTO temperature_sensor VALUES ('TEMP-02', NOW, 24.1);
INSERT INTO temperature_sensor VALUES ('TEMP-10000', NOW, 22.9);
```

### Benefits

- No DDL for new sensors; INSERT with a new tag name is sufficient.
- Simpler cross-sensor aggregation.
- Fewer objects to operate and manage.

<a id="table-types-selection-type-wrong"></a>

## Incorrect table type

The following common anti-patterns select table types that do not match data characteristics.

### Anti-pattern 1: Event logs in TAG

```sql
-- Incorrect: event logs in TAG
CREATE TAG TABLE error_log_wrong (
    name   VARCHAR(256) PRIMARY KEY,  -- Event content becomes the tag name
    time   DATETIME     BASETIME,
    level  SHORT
);
-- Problem: a unique name per event causes unbounded tag growth
```

**Correct design:** Use a LOG table.

```sql
CREATE LOG TABLE error_log (
    level   SHORT,
    msg     VARCHAR(512),
    src     VARCHAR(128)
);
```

### Anti-pattern 2: Sensor values in LOG

Storing sensor values in LOG is not inherently wrong. The problem below is omitting actual
measurement time when queries require per-tag measurement-time aggregates, leaving only
arrival time. LOG can suit searches on multi-field equipment events.

```sql
-- Insufficient schema when measurement time is required
CREATE LOG TABLE sensor_wrong (
    sensor_id VARCHAR(64),
    value     DOUBLE
    -- No measurement time; only server arrival time is recorded automatically
);
```

**Correct design:** Use a TAG table.

```sql
CREATE TAG TABLE sensor_measurements (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

### Anti-pattern 3: Large histories in LOOKUP

```sql
-- Incorrect: order history requiring relational transactions in LOOKUP
CREATE LOOKUP TABLE order_history_wrong (
    order_id LONG PRIMARY KEY,
    customer VARCHAR(64)
    -- Check memory for all rows/indexes and explicit transaction requirements
);
```

**Correct design:** Use a TRANSACTION table.

```sql
CREATE TRANSACTION TABLE order_history (
    order_id  LONG,
    customer  VARCHAR(64),
    item_id   INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16)
);
-- UPDATE/DELETE/SELECT are all supported
UPDATE order_history SET status = 'SHIPPED' WHERE order_id = 1001;
```

### Anti-pattern 4: Time-series data in TRANSACTION

TRANSACTION supports time columns and an Append API, but not TAG-specific time-axis storage
or ROLLUP. Consider TAG when measurement collection and aggregation matter more than relational
changes. See
[Misusing TRANSACTION for Time Series](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#time-series-storage-misuse-rdb).

<a id="storage-persistent-volatile"></a>

## VOLATILE as persistent storage

### Problem

This pattern stores data requiring permanent retention in VOLATILE.

### Anti-pattern example

```sql
-- Incorrect: critical configuration in VOLATILE
CREATE VOLATILE TABLE critical_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value    VARCHAR(256)
);

INSERT INTO critical_config VALUES ('license_key', 'XXXX-XXXX-XXXX');
INSERT INTO critical_config VALUES ('max_connections', '1000');
-- All settings disappear on server restart!
```

### Consequences

- The table and data disappear when the server stops or restarts.
- A failure that terminates the server process also prevents recovery of in-memory data.
  Keeping the only source in VOLATILE therefore risks data loss.

### Correct pattern

Store data requiring permanent retention in LOOKUP or TRANSACTION.

```sql
-- Correct: configuration in LOOKUP
CREATE LOOKUP TABLE app_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value    VARCHAR(256)
);

INSERT INTO app_config VALUES ('max_connections', '1000');
-- Data remains after server restart
```

### Appropriate VOLATILE uses

Use VOLATILE for data that can be recreated or discarded after restart. This includes task
state with a defined lifetime as well as query caches. Do not keep required business results
only in memory.

| Suitable | Unsuitable |
|------|--------|
| Latest sensor value cache | Source transaction data |
| Real-time aggregate results | Critical configuration |
| Temporary session state | Audit logs |
| Dashboard cache | User information |

<a id="time-series-storage-misuse-rdb"></a>

## Misusing TRANSACTION for time series

### Problem

This pattern stores continuous time-series data, such as sensor or IoT measurements, in
TRANSACTION. If relational updates are unnecessary, the lack of TAG/time-axis access and
ROLLUP may conflict with query and operational requirements. Conversely, TRANSACTION is
justified when measurement registration must share a transaction with other business changes.

### Anti-pattern example

```sql
-- Incorrect: sensor time series in TRANSACTION
CREATE TRANSACTION TABLE sensor_timeseries (
    sensor_id VARCHAR(64),
    ts        DATETIME,
    value     DOUBLE,
    unit      VARCHAR(16)
);
```

### Consequences

| Problem | Description |
|------|------|
| Ingestion semantics mismatch | Relational writes for values that do not require relational transactions |
| No TAG time axis | Cannot use TAG's BASETIME-based query structure |
| Different aggregation features | Cannot use TAG-specific ROLLUP |

### Correct pattern

Store sensor measurements in a TAG table.

```sql
-- Correct: use TAG
CREATE TAG TABLE sensor_history (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    unit   VARCHAR(16)
);

-- Bulk ingestion through high-speed Append API buffers
-- Time-based aggregation and TAG-specific optimizations available
SELECT name, DATE_TRUNC('hour', time, 1) AS hour, AVG(value), MAX(value)
FROM sensor_history
WHERE time >= NOW - 86400000000000
GROUP BY name, hour;
```

### When TRANSACTION is appropriate

Use TRANSACTION for relational business data such as orders, inventory, and equipment
history. Even with time columns, business history requiring UPDATE/DELETE suits TRANSACTION;
high-frequency measurements that accumulate without updates suit TAG.

## Aggregating values with different meanings

Identical schemas do not make values with different units or row semantics directly
aggregatable. Average cumulative energy (kWh) is not power consumption (kW), and an unweighted
average of interval averages may differ from the overall sample average. Replacing NULL
with zero turns measurement failures into valid zeros.

Record units, sample counts, and quality rules alongside type selection. When reaggregating
interval statistics, retain required components such as sums and valid counts. Before
deleting raw data, check the resolution needed for future analysis.
