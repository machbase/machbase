---
type: docs
title: 'Tag Tables'
weight: 10
---

Complete reference for Tag tables - Machbase's specialized table type for sensor, device, and distance-based series data.

## Overview

Tag tables are optimized for storing data with the pattern `(tag_name, axis, value)`. The axis can be either time or distance, and Tag tables provide metadata management and ultra-fast range queries on that axis.

## Key Features

- **Millions of inserts per second**
- **Automatic rollup statistics for time-axis tables** (per-second, per-minute, per-hour)
- **3-level partitioned indexing**
- **Metadata layer** for sensor information
- **High compression** (10-100x ratios)

## Basic Syntax

```sql
-- Time axis
CREATE TAG TABLE sensor_data (
    tag_name VARCHAR(32) PRIMARY KEY,
    event_time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- Distance axis
CREATE TAG TABLE trip_data (
    tag_name VARCHAR(32) PRIMARY KEY,
    distance_m DOUBLE BASE DISTANCE,
    value DOUBLE
);
```

## When to Use

- IoT sensor data
- Industrial equipment telemetry
- Smart meters
- GPS tracking
- Conveyor or odometer-based telemetry
- Environmental monitoring
- Any `(tag_name, time|distance, value)` pattern

## Related Documentation

- [Tutorial: IoT Sensor Data](../../tutorials/iot-sensor-data/)
- [Core Concepts: Table Types](../../core-concepts/table-types-overview/)
- [Creating and Dropping Tag Tables](./creating-tag-tables/)
- [Conditional Rollup for Filtering Noise](./rollup-conditional/)
- [Custom Rollup: User-Defined Aggregation](./rollup-custom/)
- [Rollup Rebuild Guide](./rollup-rebuild/)
- [Binary Columns](./binary-columns/)
- Original reference: [Tag Tables](../../../dbms/feature-table/tag/)
