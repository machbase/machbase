---
type: docs
title: '4.4 Modeling Anti-patterns'
weight: 40
toc: true
---

An anti-pattern is a mismatch between a design and its requirements, not simply the choice of a
particular table. The same schema can be suitable for current state and unsuitable for accumulating
history. Check the assumptions of each example before adopting the alternative.


<a id="high-frequency-lookup"></a>

## Accumulating unbounded history in LOOKUP

The issue is growing history, not frequent lookup itself. LOOKUP retains complete rows and indexes
in memory, so it is suitable for repeated key access to reference data that fits the memory budget.

```sql
CREATE LOOKUP TABLE sensor_data_wrong (
    sensor_id VARCHAR(64) PRIMARY KEY,
    value DOUBLE,
    ts DATETIME
);
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.3, NOW);
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.5, NOW); -- duplicate-key error
```

This schema gives each sensor one current row. LOOKUP could use a different key for every
observation, but that would still retain all history in memory. If tag/time history and aggregation
are the main requirement, consider TAG:

```sql
CREATE TAG TABLE sensor_data (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
);
```

Add a VOLATILE latest-value cache only when performance warrants it and rebuilding is possible.
If TAG latest-value queries already meet the requirement, a separate cache adds unnecessary work.

<a id="per-sensor-create"></a>

## One table per sensor

Creating a new table for every sensor multiplies DDL, permissions, catalog objects, and query
targets. Sensors sharing schema, units, access policy, and retention can normally share a TAG table.

```sql
CREATE TAG TABLE temperature_sensor (
    name VARCHAR(128) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
);
INSERT INTO temperature_sensor VALUES ('TEMP-01', NOW, 23.5);
INSERT INTO temperature_sensor VALUES ('TEMP-02', NOW, 24.1);
```

A new tag need not mean new DDL. Separate tables can still be appropriate for independent schema,
permissions, units, or retention. Sensor count alone should not decide the split.

<a id="table-types-selection-type-wrong"></a>

## Choosing from a data label alone

| Design | Actual problem | Alternative to evaluate |
|---|---|---|
| Every event message becomes a TAG name | Unbounded tag metadata with no recurring measured entity | LOG with source, severity, and message columns |
| Sensor value stored in LOG without measurement time | Receipt time cannot reconstruct delayed observations | Add an event-time column, or use TAG when tag/time analysis dominates |
| Growing order history in LOOKUP | Memory-resident history and no multi-statement business transaction | TRANSACTION in Standard Edition |
| Measurement history in TRANSACTION | TAG-specific axis access and ROLLUP are unavailable | TAG if those features matter more than relational transaction scope |

LOG can legitimately contain sensor values when event fields and search dominate. TRANSACTION can
legitimately contain measurements when registration must commit with other business changes.
Choose from mutation, query, memory, and consistency requirements, not the industry label.

<a id="storage-persistent-volatile"></a>

## Keeping the only permanent copy in VOLATILE

VOLATILE tables and their data disappear when the server stops or restarts. Do not make them the
only copy of settings, audit events, or business results that must survive.

```sql
CREATE LOOKUP TABLE app_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value VARCHAR(256)
);
INSERT INTO app_config VALUES ('max_connections', '1000');
```

LOOKUP or TRANSACTION can retain persistent settings. VOLATILE is appropriate for rebuildable
caches or work state with an explicitly disposable lifetime. An application must preserve any
required results in a persistent table; a cache is not a backup.

<a id="time-series-storage-misuse-rdb"></a>

## TRANSACTION used without considering time-series requirements

TRANSACTION supports relational DML and supported SDK Append paths, but not TAG-specific BASETIME
storage or ROLLUP. If repeated tag/time aggregation is required and relational updates are not,
compare a TAG model using representative ingestion and queries.

```sql
CREATE TAG TABLE sensor_history (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    unit VARCHAR(16)
);
SELECT name, DATE_TRUNC('hour', time, 1) AS hour, AVG(value), MAX(value)
FROM sensor_history
WHERE time >= NOW - 86400000000000
GROUP BY name, hour;
```

Conversely, an observation that must participate in a business transaction can justify
TRANSACTION. Support constraints and measured workload behavior should settle the choice.

## Aggregating values with different meanings

Identical column types do not make values comparable. The average of cumulative energy in kWh is
not power in kW. Averaging bucket averages without their sample counts can change the overall
average. Replacing NULL with zero turns a missing measurement into a measured value.

Record units, sample-count semantics, and quality rules with the schema. Retain sums and valid
counts when re-aggregation requires them, and verify future analysis needs before deleting raw data.
