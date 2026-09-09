---
type: docs
title: '5.9 Usage Patterns and Scenarios'
weight: 90
toc: true
---

Each example is independent. Check for conflicting objects before creating
tables. Define tag names, the meaning of one observation, value units, and
missing-data policy before applying DDL.

<a id="use-cases-tag"></a>

## Use Cases

### IoT Sensor Data

Manage sensor data from factories, buildings, and infrastructure in one TAG table.

```sql
CREATE TAG TABLE factory_sensor (
    name        VARCHAR(128) PRIMARY KEY,
    time        DATETIME     BASETIME,
    temperature DOUBLE,
    vibration   DOUBLE,
    current     DOUBLE
);

-- One row groups measurements from the same equipment observation.
INSERT INTO factory_sensor VALUES (
    'F01/LINE-A/MOTOR-01',
    NOW,
    75.3, 0.15, 2.4
);
```

This model stores simultaneous measurements from one device in multiple
columns. For per-measurement tags such as `.../TEMP` and `.../VIBRATION`,
consider a single-value `name, time, value` model. Represent differences in
measurement times with NULL and quality status.

### Energy Monitoring

Collect electricity, gas, and water meter data over time.

```sql
CREATE TAG TABLE energy_meter (
    meter_id  VARCHAR(64) PRIMARY KEY,
    time      DATETIME    BASETIME,
    kwh       DOUBLE,
    voltage   DOUBLE,
    current   DOUBLE
);
```

If `kwh` is cumulative, AVG(kwh) is the average meter reading, not interval
consumption. Calculate consumption from boundary differences with rules
for resets, replacements, and missing values. Distinguish power kW from
energy kWh and record units in metadata or the ingestion contract.

### Vehicle and Asset Tracking

Record GPS coordinates and speed as time series.

```sql
CREATE TAG TABLE vehicle_track (
    vehicle_id VARCHAR(32) PRIMARY KEY,
    time       DATETIME    BASETIME,
    lat        DOUBLE,
    lon        DOUBLE,
    speed      DOUBLE,
    heading    DOUBLE
);
```

Specify coordinate reference systems and latitude, longitude, and speed
units in the ingestion contract. Replacing missing positions with 0 makes
them indistinguishable from real coordinates. Creating this table does
not automatically provide spatial indexes or route matching. Query by
vehicle/time range first, then perform the required analysis.

### Unsuitable Cases

- A different tag name for every record (exploding tag counts)
- Frequent full-data UPDATE without tag/time limits
- Simple event logs (prefer LOG tables)


## Verify Results and Clean Up

For the IoT example, verify that the following query returns the three
measurements in one row.

```sql
SELECT name, time, temperature, vibration, current FROM factory_sensor;
DROP TABLE factory_sensor;
DROP TABLE energy_meter;
DROP TABLE vehicle_track;
```

Apply cleanup only to tables actually created on this page.
