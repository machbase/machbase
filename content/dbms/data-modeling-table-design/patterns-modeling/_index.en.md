---
type: docs
title: '4.5 Modeling Patterns'
weight: 50
toc: true
---

These patterns combine row meaning, identifiers, queries, and lifecycle decisions. They are separate
examples, not one installation script. Use an isolated exercise environment and check for existing
table names. Creating tables does not schedule ingestion, aggregation, or cache updates; define the
application or scheduler responsible for each operation and its failures.


<a id="time-axis-modeling"></a>

## Time-axis modeling

One row represents one meter observation. Define `time` as measurement time and specify whether
`kwh` is a cumulative reading or interval consumption. The schema assumes voltage and current
belong to the same observation; independently sampled values may need separate series or explicit
missing-value rules.

```sql
CREATE TAG TABLE power_meter (
    meter_id VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    kwh DOUBLE,
    voltage DOUBLE,
    current DOUBLE
) METADATA (
    location VARCHAR(64),
    phase SHORT,
    rating_kw DOUBLE
);

SELECT meter_id,
       DATE_TRUNC('hour', time, 1) AS hour,
       AVG(kwh) AS avg_kwh, MAX(kwh) AS peak_kwh
FROM power_meter
WHERE time >= NOW - 86400000000000
GROUP BY meter_id, hour
ORDER BY meter_id, hour;
```

For a cumulative meter, this is the average of readings, not hourly consumption. Consumption needs
reading differences plus reset, replacement, and rollover rules. Distinguish power (kW) from energy
(kWh). Use client time-zone settings for display: adding nine hours changes the instant rather than
displaying the same instant in another zone.

Separate raw and aggregate row grains. A VOLATILE minute cache needs an application-assigned key
for each meter/bucket and a job that fills its values. It disappears on restart. Aggregates required
after raw data expires need persistent TAG tables or supported ROLLUP and explicit retention.

<a id="distance-axis-modeling"></a>

## Distance-axis modeling

Distance is a different axis, not another display format for time. Time-axis ROLLUP and Retention
cannot be applied unchanged. Repeated inspections need a run identifier or another separation rule
so the same pipe's runs are not mixed. This example assumes one run, metres for distance, and
millimetres for thickness.

```sql
CREATE TAG TABLE pipeline_thickness (
    pipe_id VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    thickness DOUBLE,
    temp DOUBLE
);

SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A' AND distance BETWEEN 0.0 AND 50.0
ORDER BY distance;

SELECT pipe_id, FLOOR(distance / 10.0) * 10 AS segment_start,
       AVG(thickness) AS avg_thickness, MIN(thickness) AS min_thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
GROUP BY pipe_id, FLOOR(distance / 10.0) * 10
ORDER BY segment_start;
```

If inspection time is the primary access axis, use a time-axis TAG table and retain distance as an
ordinary column. An additional column does not acquire a second TAG axis automatically.

<a id="state-cache-status-modeling"></a>

## Current-state caching

Retain history in TAG or LOG and optionally maintain one current row per device in VOLATILE.

```sql
CREATE VOLATILE TABLE device_status (
    device_id VARCHAR(64) PRIMARY KEY,
    status VARCHAR(16),
    value DOUBLE,
    updated_at DATETIME
);
CREATE TAG TABLE device_status_history (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    status VARCHAR(16)
);

INSERT INTO device_status_history VALUES ('DEV-01', NOW, 78.5, 'WARNING');
INSERT INTO device_status VALUES ('DEV-01', 'WARNING', 78.5, NOW)
ON DUPLICATE KEY UPDATE SET status = 'WARNING', value = 78.5, updated_at = NOW;
```

These writes are not one transaction, and separate NOW expressions need not match. In production,
pass one chosen observation time to both paths. Define ordering and concurrent-writer handling so
a late historical value does not overwrite newer state. The application must recover when the
history write succeeds but the cache write fails. A LOOKUP code table can hold status labels and
severity for display joins.

<a id="event-log-modeling-logs"></a>

## Event and log modeling

Use LOG for structured event fields plus searchable text. Add an ordinary event-time column when
the occurrence time differs from the default server `_arrival_time`.

```sql
CREATE LOG TABLE alarm_event (
    severity SHORT,
    category VARCHAR(32),
    source VARCHAR(64),
    message VARCHAR(512),
    src_ip IPV4
);
CREATE LOG TABLE audit_log (
    user_id VARCHAR(64),
    action VARCHAR(32),
    target VARCHAR(128),
    detail TEXT,
    result VARCHAR(8)
);
CREATE INDEX idx_audit_detail ON audit_log(detail) INDEX_TYPE KEYWORD;

SELECT severity, COUNT(*) AS cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 3600000000000
GROUP BY severity
ORDER BY severity DESC;

SELECT _arrival_time, user_id, action, target
FROM audit_log
WHERE detail SEARCH 'password'
  AND _arrival_time >= NOW - 86400000000000;
```

Keep field meanings consistent: for example, define severity codes before using numeric ranges to
select alarms. Word search is not equivalent to arbitrary substring matching.

<a id="reference-master-modeling"></a>

## Reference and master data

Store repeated descriptions once and join by stable identifiers. A factory/line/equipment hierarchy
can use separate LOOKUP tables:

```sql
CREATE LOOKUP TABLE factory (
    factory_id VARCHAR(16) PRIMARY KEY,
    name VARCHAR(64), location VARCHAR(128)
);
CREATE LOOKUP TABLE production_line (
    line_id VARCHAR(16) PRIMARY KEY,
    factory_id VARCHAR(16), name VARCHAR(64)
);
CREATE LOOKUP TABLE equipment (
    equip_id VARCHAR(32) PRIMARY KEY,
    line_id VARCHAR(16), equip_name VARCHAR(128),
    equip_type VARCHAR(32), install_dt DATETIME
);
CREATE INDEX idx_equip_line ON equipment(line_id);
CREATE INDEX idx_equip_type ON equipment(equip_type);
```

These references are not automatically validated by foreign keys. The application must reject
unknown parent codes and coordinate changes. Joining old observations to current master data
shows current attributes. If the location at event time matters, retain versioned reference history
or record the relevant attributes in the original observation.

<a id="persistent-temporary"></a>

## Persistent history and temporary aggregates

Keep raw history in a persistent table and rebuildable aggregates in VOLATILE. The example below
uses one cache row per sensor for the last two hours. `base_ts` is the latest measurement included,
not the start or end of the aggregation window.

The example excludes future-dated measurements. When comparing results from separate queries,
pass one fixed reference time instead of evaluating NOW independently and calculate both bounds
from that value.

```sql
CREATE TAG TABLE sensor_data (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
);
CREATE VOLATILE TABLE sensor_recent_avg (
    key_id VARCHAR(64) PRIMARY KEY,
    sensor_id VARCHAR(64),
    base_ts DATETIME,
    avg_val DOUBLE,
    max_val DOUBLE,
    cnt LONG
);

DELETE FROM sensor_recent_avg;
INSERT INTO sensor_recent_avg
SELECT name, name, MAX(time), AVG(value), MAX(value), COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000 * 2
  AND time <= NOW
GROUP BY name;
```

```sql
SELECT sensor_id, base_ts, avg_val, max_val
FROM sensor_recent_avg
WHERE base_ts >= NOW - 3600000000000 * 2
  AND base_ts <= NOW
ORDER BY sensor_id, base_ts;
```

This displays cache rows whose latest measurement is within the last two hours. It does not
recalculate an existing average at query time; the refresh schedule controls aggregate freshness.

DELETE and INSERT SELECT are separate operations; readers may observe an empty or partially filled
cache. Define what the application displays during refresh and how it retries or queries history.
Do not append ON DUPLICATE KEY UPDATE to INSERT SELECT. If a consistent complete snapshot is
required, choose a model that explicitly provides that transition or transaction boundary.

After restart, recreate the VOLATILE table using its definition above before running INSERT SELECT;
both the table and its old rows are gone. Rebuild the same two-hour statistic rather than changing
its meaning to a 24-hour average. Raw retention must leave enough data for reconstruction.

Compare the cache's sensor counts, averages, and latest times against raw aggregation at a common
reference time. COUNT(*) includes rows with NULL measurements; retain COUNT(value) separately if
the number of samples used by AVG is needed. A cache SELECT alone does not implement fallback to
raw data; that is an application decision.

<a id="insert-update"></a>

## INSERT-oriented and UPDATE-oriented data

Use [Data mutation policy](../alter-data-mutation-policy/) for table-specific DML constraints and
[Data input and export](/dbms/development-tools-integration/data-input-load-export/) for INSERT,
Append, and file-path selection. This modeling page does not duplicate the support matrix.

<a id="join-metadata-design"></a>

## Joins and metadata

Define the relationship before writing a join. A sensor identifier should match the intended number
of master rows. If an identifier repeats across factories or several master versions match, a join
can multiply history rows and inflate SUM. Align key types and identifier scope.

Use filtered row counts and execution plans to evaluate join order. Specify time predicates and
project only needed columns. TAG metadata may be simpler than another LOOKUP for stable per-tag
attributes, but it does not automatically preserve attribute history.

See [TAG queries](../../tag-table-usage/query-analysis/) and
[LOOKUP queries](../../lookup-table-usage/query-analysis/) for detailed join examples.

<a id="table-types-patterns-combined-type"></a>

## Combining table types

| System role | Candidate | Check |
|---|---|---|
| Repeated measurements | TAG | Tag/axis design, ingestion and ROLLUP |
| Alarm and delivery events | LOG | Event fields, time meaning and retention |
| Orders, stock, maintenance jobs | TRANSACTION | Standard Edition and changes that must commit together |
| Equipment or product definitions | LOOKUP | Complete memory size and reference integrity |
| Current dashboard state | VOLATILE | Rebuild source, concurrency and restart behavior |

A manufacturing system can combine measurement history, alarm events, equipment definitions, and
an optional latest-state cache. In Standard Edition, an order system can combine transactional
orders with delivery events and reference products. These combinations still need an explicit
cross-table failure policy; shared SQL access does not make every table part of one transaction.

Continue with [SELECT and aggregation](../../reference/sql/syntax-dictionary-sql/select-syntax/) and
[operations](../../operations-configuration-recovery/).
