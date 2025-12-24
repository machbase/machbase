---
type: docs
title: 'Tag Tables'
weight: 10
---

Complete reference for Tag tables - Machbase's specialized table type for sensor and device time-series data.

## Overview

Tag tables are optimized for storing sensor data with the pattern: (sensor_id, timestamp, value). They provide automatic rollup statistics, metadata management, and ultra-fast time-series queries.

## Key Features

- **Millions of inserts per second**
- **Automatic rollup statistics** (per-second, per-minute, per-hour)
- **3-level partitioned indexing**
- **Metadata layer** for sensor information
- **High compression** (10-100x ratios)

## Basic Syntax

```sql
CREATE TAGDATA TABLE table_name (
    tag_column VARCHAR(n) PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column data_type SUMMARIZED
);
```

## When to Use

- IoT sensor data
- Industrial equipment telemetry
- Smart meters
- GPS tracking
- Environmental monitoring
- Any (sensor_id, time, value) pattern

## Related Documentation

- [Tutorial: IoT Sensor Data](../../tutorials/iot-sensor-data/)
- [Core Concepts: Table Types](../../core-concepts/table-types-overview/)
- [Binary Columns](./binary-columns/)
- Original reference: [Tag Tables](../../../dbms/feature-table/tag/)
