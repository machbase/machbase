---
title: '5.9 Patterns and Scenarios'
weight: 90
toc: true
---

Each schema is an independent example. Define subject identity, observation granularity, units,
and missing-data handling before choosing a table shape.

<a id="use-cases-tag"></a>

## IoT Equipment Observations

Group several values in one row when they belong to the same equipment observation.

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


Here the name identifies a device, not one channel such as /TEMP. For per-channel names such as
/TEMP and /VIBRATION, consider a name/time/value schema. If channels have different observation
times, define missing values and quality rather than pretending they were simultaneous.

## Energy Monitoring

```sql
CREATE TAG TABLE energy_meter (
    meter_id  VARCHAR(64) PRIMARY KEY,
    time      DATETIME    BASETIME,
    kwh       DOUBLE,
    voltage   DOUBLE,
    current   DOUBLE
);
```


If kwh is a cumulative register, AVG(kwh) averages register readings; it is not interval consumption.
Consumption requires boundary differences plus reset, replacement, and missing-data rules.
Distinguish power in kW from energy in kWh and record units in the collection contract or metadata.

## Vehicle Tracking

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


Define coordinate system and speed units. Missing coordinates are not numeric zero. This schema
does not automatically add spatial indexes or map matching. Restrict by vehicle and time before
applying the required analysis.

## When Another Model Fits Better

A distinct tag per event grows metadata without a recurring subject. General row changes without
tag/time constraints need another mutation model; event-centric histories can use LOG.

## Verify and Clean Up

The IoT SELECT returns the three measurements in one row. Remove only tables created for this
exercise; skip DROP statements for unused alternatives.

```sql
SELECT name, time, temperature, vibration, current FROM factory_sensor;
DROP TABLE factory_sensor;
DROP TABLE energy_meter;
DROP TABLE vehicle_track;
```
