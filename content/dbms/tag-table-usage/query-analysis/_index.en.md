---
title: '5.5 Query and Analysis'
weight: 50
toc: true
---

Use independent fixtures for ordinary range queries and statistics. The first table contains
20 rows; later STAT examples use their own tables so those rows do not change expected counts.
Use unused exercise names and remove only the objects you create.

<a id="original-85-querying-data"></a>

## Time-Axis Queries

### Prepare the Data

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);

insert into tag metadata values ('TAG_0001');
insert into tag metadata values ('TAG_0002');

insert into tag values('TAG_0001', '2018-01-01 01:00:00 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-02 02:00:00 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-03 03:00:00 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-04 04:00:00 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-05 05:00:00 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-06 06:00:00 000:000:000', 6);
insert into tag values('TAG_0001', '2018-01-07 07:00:00 000:000:000', 7);
insert into tag values('TAG_0001', '2018-01-08 08:00:00 000:000:000', 8);
insert into tag values('TAG_0001', '2018-01-09 09:00:00 000:000:000', 9);
insert into tag values('TAG_0001', '2018-01-10 10:00:00 000:000:000', 10);

insert into tag values('TAG_0002', '2018-02-01 01:00:00 000:000:000', 11);
insert into tag values('TAG_0002', '2018-02-02 02:00:00 000:000:000', 12);
insert into tag values('TAG_0002', '2018-02-03 03:00:00 000:000:000', 13);
insert into tag values('TAG_0002', '2018-02-04 04:00:00 000:000:000', 14);
insert into tag values('TAG_0002', '2018-02-05 05:00:00 000:000:000', 15);
insert into tag values('TAG_0002', '2018-02-06 06:00:00 000:000:000', 16);
insert into tag values('TAG_0002', '2018-02-07 07:00:00 000:000:000', 17);
insert into tag values('TAG_0002', '2018-02-08 08:00:00 000:000:000', 18);
insert into tag values('TAG_0002', '2018-02-09 09:00:00 000:000:000', 19);
insert into tag values('TAG_0002', '2018-02-10 10:00:00 000:000:000', 20);

exec table_flush(tag);
```


TAG_0001 has ten January 1–10 observations and TAG_0002 has ten February 1–10 observations.
TABLE_FLUSH handles storage buffers; it is not a transaction commit or a general visibility
guarantee. Use explicit ORDER BY when result order matters.

### All Rows and One Tag

```sql
select * from tag ORDER BY name, time;
```

```sql
select * from tag where name='TAG_0002' ORDER BY name, time;
```


Expect 20 rows for the first query and 10 for TAG_0002.

### Time Boundaries

```sql
select * from tag where name = 'TAG_0002' and time between to_date('2018-02-01') and to_date('2018-02-05') ORDER BY name, time;
```

```sql
select * from tag where name = 'TAG_0002' and time > to_date('2018-02-01') and time < to_date('2018-02-05') ORDER BY name, time;
```


Both queries return the February 1–4 values 11, 12, 13, and 14 because this fixture has no rows
exactly on either midnight boundary. In general, BETWEEN includes both endpoints and is equivalent
to >= and <=, not > and <. Use >= start AND < end for adjacent nonoverlapping intervals.

### Multiple Tags and Value Filters

```sql
select * from tag where name in ('TAG_0002', 'TAG_0001') and time between to_date('2018-01-05') and to_date('2018-02-05') ORDER BY name, time;
```

```sql
select * from tag where name = 'TAG_0002' and value > 12 and value < 15 and time between to_date('2018-02-01') and to_date('2018-02-05') ORDER BY name, time;
```


The multi-tag query returns ten rows. The value-filtered query returns TAG_0002 values 13 and 14.
IN expresses a known name list; its performance depends on the list and time range.

## Distance-Axis Queries

```sql
CREATE TAG TABLE trip_tag (
    name        VARCHAR(20) PRIMARY KEY,
    distance_m  DOUBLE BASE DISTANCE,
    value       DOUBLE,
    quality     INTEGER
);

INSERT INTO trip_tag VALUES('ODO_A', 0, 10.1, 100);
INSERT INTO trip_tag VALUES('ODO_A', 500, 11.2, 101);
INSERT INTO trip_tag VALUES('ODO_A', 1000, 12.3, 102);

INSERT INTO trip_tag VALUES('ODO_B', 1000.1, 21.5, 100);
INSERT INTO trip_tag VALUES('ODO_B', 1500, 22.1, 101);
INSERT INTO trip_tag VALUES('ODO_B', 2000, 22.9, 102);

EXEC TABLE_FLUSH(trip_tag);
```

```sql
SELECT name, distance_m, value, quality
  FROM trip_tag
 WHERE name = 'ODO_A'
   AND distance_m BETWEEN 0 AND 1000
 ORDER BY distance_m;
```

```sql
SELECT name, distance_m, value, quality
  FROM trip_tag
 WHERE name = 'ODO_B'
   AND distance_m BETWEEN 1000.1 AND 2000
 ORDER BY distance_m;
```


ODO_A returns distances 0, 500, and 1000. ODO_B returns 1000.1, 1500, and 2000. BETWEEN is
inclusive for these numeric bounds; use the axis's actual numeric type.

### Inspect the Plan and Aggregate Buckets

```sql
EXPLAIN
SELECT name, distance_m, value
  FROM trip_tag
 WHERE name = 'ODO_B'
   AND distance_m BETWEEN 1000.1 AND 2000
 ORDER BY distance_m;
```

```sql
SELECT TRUNC(distance_m / 500, 0) * 500 AS dist_bucket,
       COUNT(*)                         AS sample_count,
       MIN(value)                       AS min_v,
       MAX(value)                       AS max_v,
       AVG(value)                       AS avg_v
  FROM trip_tag
 WHERE name = 'ODO_B'
 GROUP BY TRUNC(distance_m / 500, 0) * 500
 ORDER BY dist_bucket;
```


Inspect how the axis predicate is applied. This example buckets nonnegative distances in units of
500; 1750 belongs to bucket 1500. TRUNC rounds toward zero, so choose a different boundary rule,
such as FLOOR, if negative coordinates must be bucketed mathematically.

<a id="tag-stat-axis-schema"></a>

## Per-Tag Statistics View

A TAG table supplies V$<TABLE>_STAT. Its axis fields and their types depend on the declared axis.
Separate name/axis statistics from value statistics for the third SUMMARIZED column.
STAT reflects background index/statistics processing. For a controlled exercise, TABLE_FLUSH
followed by INDEX_FLUSH waits for the relevant processing; verify raw data as well.

| Axis | Minimum/maximum | Axis of min/max value | Last inserted row axis | Type |
|---|---|---|---|---|
| DATETIME BASETIME | MIN_TIME, MAX_TIME | MIN_VALUE_TIME, MAX_VALUE_TIME | RECENT_ROW_TIME | DATETIME |
| DOUBLE/LONG/ULONG BASEDISTANCE | MIN_DISTANCE, MAX_DISTANCE | MIN_VALUE_DISTANCE, MAX_VALUE_DISTANCE | RECENT_ROW_DISTANCE | Original distance type |

Both Editions expose NAME, ROW_COUNT, MIN_VALUE, and MAX_VALUE. Cluster prepends
HOSTNAME VARCHAR(64). Without SUMMARIZED, the value-related statistics are NULL.

### Time Statistics: Separate Fixture

```sql
CREATE TAG TABLE ch5_stat_time (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
```

```sql
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-12'), 10);
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-13'), 10);
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-14'), 20);
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-11'), 5);
INSERT INTO ch5_stat_time VALUES('tag-1', TO_DATE('2022-08-12'), 100);
INSERT INTO ch5_stat_time VALUES('tag-1', TO_DATE('2022-08-11'), 200);
INSERT INTO ch5_stat_time VALUES('tag-1', TO_DATE('2022-08-10'), 50);
```

```sql
EXEC TABLE_FLUSH(ch5_stat_time);
EXEC INDEX_FLUSH(ch5_stat_time);
SELECT * FROM v$ch5_stat_time_stat ORDER BY name;
```


| Tag | ROW_COUNT | MIN_TIME | MAX_TIME | MIN_VALUE | MAX_VALUE | RECENT_ROW_TIME |
|---|---:|---|---|---:|---:|---|
| tag-0 | 4 | 2021-08-11 | 2021-08-14 | 5 | 20 | 2021-08-11 |
| tag-1 | 3 | 2022-08-10 | 2022-08-12 | 50 | 200 | 2022-08-10 |

RECENT_ROW_TIME is the timestamp of the last inserted row, not the greatest measurement timestamp.
MIN_VALUE_TIME and MAX_VALUE_TIME identify the observations producing the extrema.

### Without SUMMARIZED

```sql
CREATE TAG TABLE other_tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
```

```sql
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-12'), 10);
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-13'), 10);
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-14'), 20);
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-11'), 5);
INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-12'), 100);
INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-11'), 200);
INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-10'), 50);
```

```sql
EXEC TABLE_FLUSH(other_tag);
EXEC INDEX_FLUSH(other_tag);
SELECT * FROM v$other_tag_stat ORDER BY name;
```


Counts and axis statistics remain available; MIN_VALUE, MAX_VALUE, and their associated time
fields are NULL.

### Distance Statistics

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
EXEC INDEX_FLUSH(distance_sensor);
```

```sql
DESC V$DISTANCE_SENSOR_STAT;
```

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


Expect row count 3, minimum distance 10.25, maximum distance 30.75, minimum value 3 at distance
10.25, and maximum value 8 at distance 20.5. The last inserted row's distance is 30.75.
All five distance fields follow the original DOUBLE/LONG/ULONG type; they are not DATETIME.

### Cluster Results

```sql
SELECT hostname, name, row_count,
       min_distance, max_distance,
       min_value, min_value_distance,
       max_value, max_value_distance,
       recent_row_distance
  FROM V$DISTANCE_SENSOR_STAT
 ORDER BY hostname, name;
```

```sql
SELECT name,
       SUM(row_count)     AS row_count,
       MIN(min_distance)  AS min_distance,
       MAX(max_distance)  AS max_distance
  FROM V$DISTANCE_SENSOR_STAT
 GROUP BY name;
```


Inspect warehouse-local rows before aggregation. Counts and axis bounds can be grouped by tag.
Keep MIN_VALUE paired with MIN_VALUE_DISTANCE, and MAX_VALUE paired with MAX_VALUE_DISTANCE,
from the same warehouse row. Taking each column's independent minimum/maximum can mix rows.
MAX(RECENT_ROW_DISTANCE) is not the cluster's most recently inserted observation.

### 8.7.0 Compatibility

| Former distance-view field | 8.7.0 field |
|---|---|
| MIN_TIME | MIN_DISTANCE |
| MAX_TIME | MAX_DISTANCE |
| MIN_VALUE_TIME | MIN_VALUE_DISTANCE |
| MAX_VALUE_TIME | MAX_VALUE_DISTANCE |
| RECENT_ROW_TIME | RECENT_ROW_DISTANCE |

The old distance names are not aliases. Existing distance-axis tables expose the new schema after
restart on 8.7.0. Time-axis tables keep their *_TIME DATETIME fields. Read fields by name or account
for Cluster's leading HOSTNAME when using positional mappings.

## Scan Direction and Result Order

```sql
SELECT *
  FROM tag
 WHERE name = 'TAG_0001'
 ORDER BY time
 LIMIT 10;

SELECT /*+ SCAN_FORWARD(tag) */ name, time, value
  FROM tag
 WHERE name = 'TAG_0001'
 LIMIT 10;

SELECT /*+ SCAN_BACKWARD(tag) */ name, time, value
  FROM tag
 WHERE name = 'TAG_0001'
 LIMIT 10;
```


Backward axis traversal concerns the greatest axis values, which can differ from the last inserted
row's STAT value. Use explicit sorting when output order is part of the requirement; equal axis
values need an additional application-defined tie rule. See
[TABLE_SCAN_DIRECTION](../../reference/configuration/dictionary-configuration/) for defaults.

## Cleanup

```sql
DROP TABLE ch5_stat_time;
DROP TABLE distance_sensor;
DROP TABLE trip_tag;
DROP TABLE other_tag;
DROP TABLE tag;
```
