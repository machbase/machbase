---
type: docs
title: '5.5 Queries and Analysis'
weight: 50
toc: true
---

This page covers common TAG time-series query patterns: time and distance ranges,
multiple tags, and statistics views.

<a id="original-85-querying-data"></a>

## Query Tag Data


### Sample Schema (Time Axis)

This example registers two tags and inserts 10 rows per tag. `TAG_0001` has data
from January 1–10, 2018; `TAG_0002` has data from February 1–10.

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

The final `TABLE_FLUSH` explicitly processes storage buffers. Do not interpret it
as a transaction commit or a guarantee of query visibility. See
[TABLE_FLUSH](/dbms/reference/sql/syntax/execute-procedure-syntax/#table-flush) for details.

### Retrieve All TAG Data

```sql
select * from tag ORDER BY name, time;
```

```text
NAME TIME VALUE
--------------------------------------------------------------------------------------
TAG_0001 2018-01-01 01:00:00 000:000:000 1
TAG_0001 2018-01-02 02:00:00 000:000:000 2
TAG_0001 2018-01-03 03:00:00 000:000:000 3
TAG_0001 2018-01-04 04:00:00 000:000:000 4
TAG_0001 2018-01-05 05:00:00 000:000:000 5
TAG_0001 2018-01-06 06:00:00 000:000:000 6
TAG_0001 2018-01-07 07:00:00 000:000:000 7
TAG_0001 2018-01-08 08:00:00 000:000:000 8
TAG_0001 2018-01-09 09:00:00 000:000:000 9
TAG_0001 2018-01-10 10:00:00 000:000:000 10
TAG_0002 2018-02-01 01:00:00 000:000:000 11
TAG_0002 2018-02-02 02:00:00 000:000:000 12
TAG_0002 2018-02-03 03:00:00 000:000:000 13
TAG_0002 2018-02-04 04:00:00 000:000:000 14
TAG_0002 2018-02-05 05:00:00 000:000:000 15
TAG_0002 2018-02-06 06:00:00 000:000:000 16
TAG_0002 2018-02-07 07:00:00 000:000:000 17
TAG_0002 2018-02-08 08:00:00 000:000:000 18
TAG_0002 2018-02-09 09:00:00 000:000:000 19
TAG_0002 2018-02-10 10:00:00 000:000:000 20
[20] row(s) selected.
```

The output is one execution result. Specify `ORDER BY name, time` when ordering
must be guaranteed. Unfiltered output order may depend on the execution plan and
scan direction.


### Retrieve Data by Tag Name

This example retrieves data for TAG_0002.

```sql
select * from tag where name='TAG_0002' ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
TAG_0002              2018-02-05 05:00:00 000:000:000 15
TAG_0002              2018-02-06 06:00:00 000:000:000 16
TAG_0002              2018-02-07 07:00:00 000:000:000 17
TAG_0002              2018-02-08 08:00:00 000:000:000 18
TAG_0002              2018-02-09 09:00:00 000:000:000 19
TAG_0002              2018-02-10 10:00:00 000:000:000 20
[10] row(s) selected.
```


### Query a Time Range

This example applies a time range to TAG_0002.

> `BETWEEN` includes both boundaries, equivalent to `>=` together with `<=`.
> The examples return the same results with `>` and `<` because there are no rows
> at the boundary timestamps. To avoid reading boundary rows twice in adjacent
> intervals, use `time >= start AND time < end`.

```sql
select * from tag where name = 'TAG_0002' and time between to_date('2018-02-01') and to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[4] row(s) selected.
```

```sql
select * from tag where name = 'TAG_0002' and time > to_date('2018-02-01') and time < to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[4] row(s) selected.
```

### Distance-Axis Sample Schema

This example uses a distance-axis (`BASE DISTANCE`) TAG table.

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

### Query a Distance Range

```sql
SELECT name, distance_m, value, quality
  FROM trip_tag
 WHERE name = 'ODO_A'
   AND distance_m BETWEEN 0 AND 1000
 ORDER BY distance_m;
```

As with a time axis, narrowing the axis range is the basic query pattern.

### Fractional Boundaries on a DOUBLE Distance Axis

```sql
SELECT name, distance_m, value, quality
  FROM trip_tag
 WHERE name = 'ODO_B'
   AND distance_m BETWEEN 1000.1 AND 2000
 ORDER BY distance_m;
```

Numeric comparison excludes `1000` and includes `1500` and `2000`.

### Check Distance-Axis Execution Plans

For large distance-range queries, use `EXPLAIN` to check whether distance predicates
become key ranges.

```sql
EXPLAIN
SELECT name, distance_m, value
  FROM trip_tag
 WHERE name = 'ODO_B'
   AND distance_m BETWEEN 1000.1 AND 2000
 ORDER BY distance_m;
```

Check for:

- `KEYVALUE INDEX SCAN` or a similar index scan
- A `distance_m between ...` condition under `KEY RANGE`

### Aggregate into Distance Buckets

This example groups nonnegative distances into intervals of 500. TRUNC truncates
toward zero. For negative coordinates, choose the desired boundary rule separately,
such as FLOOR.

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

For example, `1750` belongs to bucket `1500`.

### Query a Time Range Across Multiple Tags

Apply the same time range to two or more tags. Use `IN` when the target name list
is known. For many tags, measure performance with both list size and time-range width.

```sql
select * from tag where name in ('TAG_0002', 'TAG_0001') and time between to_date('2018-01-05') and to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2018-01-05 05:00:00 000:000:000 5
TAG_0001              2018-01-06 06:00:00 000:000:000 6
TAG_0001              2018-01-07 07:00:00 000:000:000 7
TAG_0001              2018-01-08 08:00:00 000:000:000 8
TAG_0001              2018-01-09 09:00:00 000:000:000 9
TAG_0001              2018-01-10 10:00:00 000:000:000 10
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[10] row(s) selected.
```

### Filter by Values

You can also filter tag values. This example selects TAG_0002 values greater than
12 and less than 15.

```sql
select * from tag where name = 'TAG_0002' and value > 12 and value < 15 and time between to_date('2018-02-01') and to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[2] row(s) selected.
```

<a id="tag-stat-axis-schema"></a>

### Per-Tag Statistics View `V$<TABLE>_STAT`

Creating a TAG table automatically creates a virtual table aggregating statistics
per tag ID, named v${tag table name}_stat.

Distinguish tag-name/axis statistics from value statistics for the third SUMMARIZED
column. STAT reflects background index/statistics processing, so verify recent
input with source SELECT queries as well. Exercises needing immediate statistics
use TABLE_FLUSH followed by INDEX_FLUSH to wait for processing.

<span class="badge-since">Axis-specific BASE DISTANCE STAT schemas are supported since Machbase 8.7.0</span>

Axis-related column names and types depend on the TAG axis.

| TAG axis | Minimum/maximum axis | Axis of minimum/maximum value | Latest inserted row axis | Axis statistic type |
|--------|--------------|----------------------|------------------|--------------|
| `DATETIME BASE TIME` | `MIN_TIME`, `MAX_TIME` | `MIN_VALUE_TIME`, `MAX_VALUE_TIME` | `RECENT_ROW_TIME` | `DATETIME` |
| `DOUBLE/LONG/ULONG BASE DISTANCE` | `MIN_DISTANCE`, `MAX_DISTANCE` | `MIN_VALUE_DISTANCE`, `MAX_VALUE_DISTANCE` | `RECENT_ROW_DISTANCE` | Original BASE DISTANCE type |

Both Editions share `NAME`, `ROW_COUNT`, `MIN_VALUE`, and `MAX_VALUE`. Cluster
Edition adds `HOSTNAME VARCHAR(64)` at the beginning of the schema.

#### BASE TIME STAT Schema


```sql
DESC v$tag_stat;
```

```text
[ COLUMN ]
----------------------------------------------------------------------------------------------------
NAME                                                        NULL?    TYPE                LENGTH
----------------------------------------------------------------------------------------------------
NAME                                                                 varchar             100
ROW_COUNT                                                            ulong               20
MIN_TIME                                                             datetime            31
MAX_TIME                                                             datetime            31
MIN_VALUE                                                            double              17
MIN_VALUE_TIME                                                       datetime            31
MAX_VALUE                                                            double              17
MAX_VALUE_TIME                                                       datetime            31
RECENT_ROW_TIME                                                      datetime            31
```

Without SUMMARIZED on the third column, VALUE statistics (MIN_VALUE, MAX_VALUE,
MIN_VALUE_TIME, MAX_VALUE_TIME) are not stored.

Collected statistics:

| Column | Information |
|--|--|
| NAME | Tag ID name |
| ROW_COUNT | Row count |
| MIN_TIME | Minimum basetime for this tag ID |
| MAX_TIME | Maximum basetime for this tag ID |
| MIN_VALUE | Minimum summarized value for this tag ID |
| MIN_VALUE_TIME | Basetime inserted with MIN_VALUE |
| MAX_VALUE | Maximum summarized value for this tag ID |
| MAX_VALUE_TIME | Basetime inserted with MAX_VALUE |
| RECENT_ROW_TIME | Basetime of the most recently inserted row |

The statistics exercise uses a separate table from the preceding 20-row query
example. Only its two tags appear; TAG_0001 and TAG_0002 do not affect expected statistics.

1. With a SUMMARIZED column

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

```text
NAME                                                                              ROW_COUNT            MIN_TIME                        MAX_TIME                        MIN_VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
MIN_VALUE_TIME                  MAX_VALUE                   MAX_VALUE_TIME                  RECENT_ROW_TIME
---------------------------------------------------------------------------------------------------------------------------------
tag-0                                                                             4                    2021-08-11 00:00:00 000:000:000 2021-08-14 00:00:00 000:000:000 5
2021-08-11 00:00:00 000:000:000 20                          2021-08-14 00:00:00 000:000:000 2021-08-11 00:00:00 000:000:000
tag-1                                                                             3                    2022-08-10 00:00:00 000:000:000 2022-08-12 00:00:00 000:000:000 50
2022-08-10 00:00:00 000:000:000 200                         2022-08-11 00:00:00 000:000:000 2022-08-10 00:00:00 000:000:000
[2] row(s) selected.
```

2. Without a SUMMARIZED column

```sql
CREATE TAG TABLE other_tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
```

```text
Executed successfully.
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

```text
NAME                                                                              ROW_COUNT            MIN_TIME                        MAX_TIME                        MIN_VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
MIN_VALUE_TIME                  MAX_VALUE                   MAX_VALUE_TIME                  RECENT_ROW_TIME
---------------------------------------------------------------------------------------------------------------------------------
tag-0                                                                             4                    2021-08-11 00:00:00 000:000:000 2021-08-14 00:00:00 000:000:000 NULL
NULL                            NULL                        NULL                            2021-08-11 00:00:00 000:000:000
tag-1                                                                             3                    2022-08-10 00:00:00 000:000:000 2022-08-12 00:00:00 000:000:000 NULL
NULL                            NULL                        NULL                            2022-08-10 00:00:00 000:000:000
[2] row(s) selected.
```

#### BASE DISTANCE STAT Schema

Distance-axis TAG statistics views expose distance values as numeric types.

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

In Standard Edition, a `DOUBLE BASE DISTANCE` table has this schema:

```sql
DESC V$DISTANCE_SENSOR_STAT;
```

```text
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

The five distance statistic columns use the original BASE DISTANCE type.

| BASE DISTANCE type | STAT column type | `DESC` length |
|--------------------|----------------|-------------|
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

- `MIN_DISTANCE` and `MAX_DISTANCE` are the minimum and maximum distances for the statistics row.
- `MIN_VALUE_DISTANCE` and `MAX_VALUE_DISTANCE` are the distances where the minimum
  and maximum summarized values occurred.
- `RECENT_ROW_DISTANCE` is the most recently inserted row's distance, not the largest distance.
- Without `SUMMARIZED`, `MIN_VALUE_DISTANCE` and `MAX_VALUE_DISTANCE` are `NULL`.

##### Query in Cluster Edition

Cluster statistics views add `HOSTNAME` and may return rows per Warehouse. Inspect
Warehouse-specific values first.

```sql
SELECT hostname, name, row_count,
       min_distance, max_distance,
       min_value, min_value_distance,
       max_value, max_value_distance,
       recent_row_distance
  FROM V$DISTANCE_SENSOR_STAT
 ORDER BY hostname, name;
```

Row counts and distance boundaries can be safely aggregated by tag name.

```sql
SELECT name,
       SUM(row_count)     AS row_count,
       MIN(min_distance)  AS min_distance,
       MAX(max_distance)  AS max_distance
  FROM V$DISTANCE_SENSOR_STAT
 GROUP BY name;
```

{{< callout type="warning" >}}
Keep `MIN_VALUE` paired with `MIN_VALUE_DISTANCE` and `MAX_VALUE` with
`MAX_VALUE_DISTANCE` from the same Warehouse row. Independent `MIN` or `MAX`
aggregations can combine values from different Warehouses. `RECENT_ROW_DISTANCE`
is also per-Warehouse; do not interpret `MAX(RECENT_ROW_DISTANCE)` as the latest
inserted row across the cluster.
{{< /callout >}}

##### 8.7.0 Compatibility

Old BASE DISTANCE statistics column names are not provided as aliases. Existing
tables also use the new schema after the 8.7.0 server restarts.

| Before 8.7.0 | 8.7.0 |
|-----------------|------------|
| `MIN_TIME` | `MIN_DISTANCE` |
| `MAX_TIME` | `MAX_DISTANCE` |
| `MIN_VALUE_TIME` | `MIN_VALUE_DISTANCE` |
| `MAX_VALUE_TIME` | `MAX_VALUE_DISTANCE` |
| `RECENT_ROW_TIME` | `RECENT_ROW_DISTANCE` |

BASE TIME TAG tables retain the `*_TIME DATETIME` schema.


### Scan Direction Hints

Distinguish axis traversal from result sorting. The latest value in a reverse-axis
scan is the largest axis value; it may differ from STAT RECENT_ROW, which describes
the last inserted row. Ordering multiple rows with the same axis value requires
an additional application-defined criterion.

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

See [TABLE_SCAN_DIRECTION](/dbms/reference/configuration/configuration/) for the
default direction without a hint.

## Cleanup

```sql
DROP TABLE ch5_stat_time;
DROP TABLE distance_sensor;
DROP TABLE trip_tag;
DROP TABLE other_tag;
DROP TABLE tag;
```
