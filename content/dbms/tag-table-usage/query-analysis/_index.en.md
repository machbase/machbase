---
title: '5.5 Query and Analysis'
weight: 50
toc: true
---

<a id="original-85-querying-data"></a>

## TAG Data Query

Detailed query examples are being aligned with the Korean manual. The TAG statistics
contract below is authoritative for both time- and distance-axis tables.

<a id="tag-stat-axis-schema"></a>

## Per-tag statistics view `V$<TABLE>_STAT`

Creating a TAG table automatically creates a read-only `V$<TABLE>_STAT` view. Its axis
column names and types depend on the TAG axis.

<span class="badge-since">Axis-specific BASE DISTANCE schema is supported since Machbase 8.7.0</span>

| TAG axis | Minimum/maximum axis | Axis of minimum/maximum value | Most recently inserted row axis | Axis-stat type |
|----------|----------------------|--------------------------------|---------------------------------|----------------|
| `DATETIME BASE TIME` | `MIN_TIME`, `MAX_TIME` | `MIN_VALUE_TIME`, `MAX_VALUE_TIME` | `RECENT_ROW_TIME` | `DATETIME` |
| `DOUBLE/LONG/ULONG BASE DISTANCE` | `MIN_DISTANCE`, `MAX_DISTANCE` | `MIN_VALUE_DISTANCE`, `MAX_VALUE_DISTANCE` | `RECENT_ROW_DISTANCE` | Original BASE DISTANCE type |

Both editions expose `NAME`, `ROW_COUNT`, `MIN_VALUE`, and `MAX_VALUE`. Cluster Edition
prepends `HOSTNAME VARCHAR(64)` to the schema.

### BASE DISTANCE schema

```sql
CREATE TAG TABLE distance_sensor (
    name       VARCHAR(32) PRIMARY KEY,
    odometer_m DOUBLE BASE DISTANCE,
    value      DOUBLE SUMMARIZED
);

INSERT INTO distance_sensor VALUES('sensor', 20.5, 8);
INSERT INTO distance_sensor VALUES('sensor', 10.25, 3);
INSERT INTO distance_sensor VALUES('sensor', 30.75, 5);

EXEC TABLE_FLUSH(distance_sensor);
```

The Standard Edition schema for this `DOUBLE BASE DISTANCE` table is:

```text
Mach> DESC V$DISTANCE_SENSOR_STAT;
[ COLUMN ]
----------------------------------------------------------------------------------------------------
NAME                                                        NULL?    TYPE                LENGTH
----------------------------------------------------------------------------------------------------
NAME                                                                 varchar             100
ROW_COUNT                                                            ulong               20
MIN_DISTANCE                                                         double              17
MAX_DISTANCE                                                         double              17
MIN_VALUE                                                            double              17
MIN_VALUE_DISTANCE                                                   double              17
MAX_VALUE                                                            double              17
MAX_VALUE_DISTANCE                                                   double              17
RECENT_ROW_DISTANCE                                                  double              17
```

All five distance-axis statistics use the original BASE DISTANCE type.

| BASE DISTANCE type | STAT column type | `DESC` length |
|--------------------|------------------|---------------|
| `DOUBLE` | `double` | 17 |
| `LONG` | `long` | 20 |
| `ULONG` | `ulong` | 20 |

```sql
SELECT name,
       row_count,
       min_distance,
       max_distance,
       min_value,
       min_value_distance,
       max_value,
       max_value_distance,
       recent_row_distance
  FROM V$DISTANCE_SENSOR_STAT
 WHERE name = 'sensor';
```

- `MIN_VALUE_DISTANCE` and `MAX_VALUE_DISTANCE` identify where the minimum and maximum
  summarized values occurred.
- `RECENT_ROW_DISTANCE` is the distance of the most recently inserted row, not the
  greatest distance.
- Without a `SUMMARIZED` column, `MIN_VALUE_DISTANCE` and `MAX_VALUE_DISTANCE` are NULL.

### Cluster Edition

Cluster Edition can return one STAT row per warehouse. Inspect those rows before
aggregating them.

```sql
SELECT hostname, name, row_count,
       min_distance, max_distance,
       min_value, min_value_distance,
       max_value, max_value_distance,
       recent_row_distance
  FROM V$DISTANCE_SENSOR_STAT
 ORDER BY hostname, name;
```

Row counts and distance bounds can be aggregated safely by tag name.

```sql
SELECT name,
       SUM(row_count)     AS row_count,
       MIN(min_distance)  AS min_distance,
       MAX(max_distance)  AS max_distance
  FROM V$DISTANCE_SENSOR_STAT
 GROUP BY name;
```

{{< callout type="warning" >}}
Keep `MIN_VALUE` paired with `MIN_VALUE_DISTANCE` and `MAX_VALUE` paired with
`MAX_VALUE_DISTANCE` from the same warehouse row. Aggregating each column independently
can combine values from different warehouses. `RECENT_ROW_DISTANCE` is also
warehouse-local; `MAX(RECENT_ROW_DISTANCE)` is not the globally most recent inserted row.
{{< /callout >}}

### Compatibility

Machbase 8.7.0 does not provide the former BASE DISTANCE `*_TIME` names as aliases.
Existing distance-axis tables use the new schema after the upgraded server restarts.

| Before 8.7.0 | 8.7.0 |
|--------------|-------|
| `MIN_TIME` | `MIN_DISTANCE` |
| `MAX_TIME` | `MAX_DISTANCE` |
| `MIN_VALUE_TIME` | `MIN_VALUE_DISTANCE` |
| `MAX_VALUE_TIME` | `MAX_VALUE_DISTANCE` |
| `RECENT_ROW_TIME` | `RECENT_ROW_DISTANCE` |

BASE TIME TAG tables retain their existing `*_TIME DATETIME` schema.
