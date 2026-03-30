---
title: 'Creating and Dropping Tag Tables'
type: docs
weight: 10
---

## What You'll Learn

Tag tables are the foundation for storing axis-based sensor data in Machbase. This guide covers how to create, configure, and drop both time-axis and distance-axis tag tables.

> **Version**: Distance-axis columns (`BASE DISTANCE`, `BASEDISTANCE`) are supported in Neo v8.0.75+.

## Axis Rules

Tag tables store rows for the same `tag_name` along a single axis column.

- Time axis: `DATETIME BASE TIME` or `DATETIME BASETIME`
- Distance axis: `DOUBLE`, `LONG`, or `ULONG` with `BASE DISTANCE` or `BASEDISTANCE`
- When you use `BASE`, it must be followed by either `TIME` or `DISTANCE`
- A tag table can have only one axis column
- Tag tables support `SELECT`, `INSERT`, and `DELETE`, but not `UPDATE`

## Creating a Time-Axis Tag Table

The most common time-axis tag table requires three essential elements:
- **Tag name** (PRIMARY KEY): Identifies the sensor or data source
- **Input time** (BASETIME): When the data was recorded
- **Sensor value**: The actual measurement

### Time-Axis Creation Example

```sql
-- This will fail - missing required keywords
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME, value DOUBLE);
[ERR-02253: Mandatory column definition (PRIMARY KEY / BASETIME) is missing.]

-- Correct way - with required BASETIME keyword
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
Executed successfully.

-- With SUMMARIZED for statistical information
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
Executed successfully.

Mach> desc tag;
[ COLUMN ]
----------------------------------------------------------------
NAME      TYPE        LENGTH
----------------------------------------------------------------
NAME      varchar         20
TIME      datetime       31
VALUE     double          17
```

> **Tip**: The SUMMARIZED keyword enables automatic statistical tracking (min, max, avg) for the value column, which is useful for analytics.

## Creating a Distance-Axis Tag Table

Distance-axis tag tables are used when the axis is cumulative distance, travel length, or line position instead of time.

```sql
Mach> CREATE TAG TABLE trip_sensor (
          name        VARCHAR(20) PRIMARY KEY,
          distance_m  DOUBLE BASE DISTANCE,
          value       DOUBLE,
          quality     INTEGER
      );
Executed successfully.

Mach> CREATE TAG TABLE trip_sensor_alias (
          name        VARCHAR(20) PRIMARY KEY,
          distance_m  LONG BASEDISTANCE,
          value       DOUBLE
      ) METADATA (route_id VARCHAR(20), axis_unit VARCHAR(8));
Executed successfully.
```

Distance-axis columns must use an 8-byte type.

- `DOUBLE`
- `LONG`
- `ULONG`

Use `DOUBLE` when you need fractional distances, and `LONG` or `ULONG` when integer distances are enough.

The following types are not allowed for a distance axis:

- `FLOAT`
- `INTEGER`
- `UINTEGER`
- `SHORT`
- `USHORT`

> **Limitation**: Distance-axis tag tables do not support `WITH ROLLUP`. See [Rollup Tables for Aggregation](../rollup-tables) for details.

## Adding Additional Sensor Columns

Real-world sensor data often requires more than just a name, axis, and value. You can add additional columns on both time-axis and distance-axis tables for fields such as group IDs or IP addresses.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double, grpid short, myip ipv4);
Executed successfully.

Mach> desc tag;
[ COLUMN ]
----------------------------------------------------------------
NAME             TYPE        LENGTH
----------------------------------------------------------------
NAME             varchar         20
TIME             datetime        31
VALUE            double          17
GRPID            short            6       <=== added column
MYIP             ipv4            15       <=== added column
```

> **Note**: In versions prior to 5.6, VARCHAR types were not allowed as additional columns. Version 5.6+ supports VARCHAR in additional columns.

## Adding Metadata Columns

Metadata columns store information that's specific to each tag name (like room number or description) without redundantly storing it with every sensor reading.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double)
   2  metadata (room_no integer, tag_description varchar(100));
Executed successfully.
```

### Example Metadata Usage

|name|room_no|tag_description|
|--|--|--|
|temp_001|1|It reads current temperature as Celsius|
|humid_001|1|It reads current humidity as percentage|

Query metadata alongside sensor data:

```sql
Mach> SELECT name, time, value, tag_description FROM tag LIMIT 1;
name                  time                            value
--------------------------------------------------------------------------------------
tag_description
------------------------------------------------------------------------------------
temp_001              2019-03-01 09:52:17 000:000:000 25.3
It reads current temperature as Celsius
```

## Configuring Table Properties

Control memory and CPU usage with these properties:

|Property|Description|Default|Range|
|--|--|--|--|
|TAG_PARTITION_COUNT|Number of partitions|4|1-1024|
|TAG_DATA_PART_SIZE|Data size per partition|16MB|1MB-1GB|
|TAG_STAT_ENABLE|Enable statistical tracking|1 (enabled)|0-1|

### Property Examples

```sql
-- Single partition for low-volume data
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE)
      TAG_PARTITION_COUNT=1;

-- Custom data part size
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE)
      TAG_DATA_PART_SIZE=1048576;

-- Multiple properties
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)
      TAG_PARTITION_COUNT=2, TAG_STAT_ENABLE=1;
```

## Dropping Tag Tables

When you need to recreate a tag table or free up disk space, use the DROP command:

```sql
Mach> DROP TABLE tag;
Dropped successfully.

Mach> DESC tag;
tag does not exist.
```

> **Warning**: Dropping a tag table deletes all associated data and metadata tables permanently. This action cannot be undone.

## Best Practices

1. **Use SUMMARIZED**: Add the SUMMARIZED keyword to value columns when you need statistical information
2. **Plan partitions**: Higher partition counts improve parallel processing but use more memory
3. **Choose appropriate names**: Tag table names can be any valid identifier (not required to be "TAG")
4. **Metadata vs Additional Columns**:
   - Use metadata for tag-specific information that changes rarely
   - Use additional columns for data that changes with each reading

## Next Steps

- Learn about [Managing Tag Metadata](../tag-metadata) to create and manage tag names
- Explore [Inserting Tag Data](../inserting-data) for various data input methods
- Understand [Querying Tag Data](../querying-data) for efficient data retrieval
