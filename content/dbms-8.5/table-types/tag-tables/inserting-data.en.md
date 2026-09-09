---
title: 'Inserting Tag Data'
type: docs
weight: 30
---

## Overview

Machbase provides multiple methods to insert both time-axis and distance-axis tag data. Choose the method that best fits your data volume and application requirements.

## Method 1: INSERT Statement

The simplest way to insert data - ideal for small datasets and testing.

### Basic INSERT Example

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
Executed successfully.

Mach> insert into tag metadata values ('TAG_0001');
1 row(s) inserted.

-- Insert single values
Mach> insert into tag values('TAG_0001', now, 0);
1 row(s) inserted.

Mach> insert into tag values('TAG_0001', now, 1);
1 row(s) inserted.

Mach> insert into tag values('TAG_0001', now, 2);
1 row(s) inserted.

Mach> EXEC TABLE_FLUSH(tag);
Executed successfully.

Mach> select * from tag where name = 'TAG_0001';
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2018-12-19 17:41:37 806:901:728 0
TAG_0001              2018-12-19 17:41:42 327:839:368 1
TAG_0001              2018-12-19 17:41:43 812:782:202 2
[3] row(s) selected.
```

`EXEC TABLE_FLUSH(tag)` makes recently inserted TAG rows visible to immediate
queries and statistic views in interactive examples.

> **When to use**: Testing, low-volume inserts, interactive data entry

### TAG Metadata and `_LAST_UPDATE_TIME`

For a TAG table without metadata columns, you can continue to insert only the three values `name`, `time`, and `value`.

```sql
CREATE TAG TABLE sensor (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);

INSERT INTO sensor VALUES('tag1', now, 1);
```

For a TAG table with user-defined metadata columns, when you insert a new tag without a column list, provide the data values and the user-defined metadata values together. Do not include `_LAST_UPDATE_TIME`; it is the system-managed metadata changed time.

```sql
CREATE TAG TABLE sensor_meta (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    site   VARCHAR(32),
    status INTEGER
);

INSERT INTO sensor_meta
VALUES('tag1', now, 1, 'seoul', 1);
```

When you use a column list, specify only the required user-defined columns. Do not specify `_LAST_UPDATE_TIME`.

```sql
INSERT INTO sensor_meta(name, time, value, site, status)
VALUES('tag2', now, 1, 'busan', 1);
```

If the metadata row for the tag already exists, a data-only insert does not change metadata values. Therefore, `_LAST_UPDATE_TIME` is not changed.

### Distance-Axis INSERT Example

Distance-axis tag tables use the same `INSERT` syntax, but the axis column stores numeric distance values.

```sql
Mach> CREATE TAG TABLE trip_sensor (
          name        VARCHAR(20) PRIMARY KEY,
          distance_m  DOUBLE BASE DISTANCE,
          value       DOUBLE,
          quality     INTEGER
      );
Executed successfully.

Mach> INSERT INTO trip_sensor VALUES('ODO_A', 0, 10.1, 100);
1 row(s) inserted.

Mach> INSERT INTO trip_sensor VALUES('ODO_A', 500, 11.2, 101);
1 row(s) inserted.

Mach> INSERT INTO trip_sensor VALUES('ODO_B', 1000.1, 21.5, 100);
1 row(s) inserted.

Mach> EXEC TABLE_FLUSH(trip_sensor);
Executed successfully.
```

A `DOUBLE` distance axis stores fractional distances directly, while `LONG` and `ULONG` are for integer distances only.

## Method 2: CSV File Import

Load large amounts of data quickly from CSV files using the `csvimport` tool.

### CSV File Format

Create a CSV file (`data.csv`) with tag name, timestamp, and value:

```csv
TAG_0001, 2009-01-28 07:03:34 0:000:000, -41.98
TAG_0001, 2009-01-28 07:03:34 1:000:000, -46.50
TAG_0001, 2009-01-28 07:03:34 2:000:000, -36.16
```

### Using csvimport

```bash
csvimport -t TAG -d data.csv -F "time YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" -l error.log
```

**Options explained**:
- `-t TAG`: Target table name
- `-d data.csv`: Data file path
- `-F`: Time format specification
- `-l error.log`: Error log file

> **When to use**: Bulk loading, data migration, batch imports

> **Important**: Machbase auto-registers missing tag names during import. Pre-register tag metadata when you need explicit metadata values such as unit, location, or status before data is loaded.

## Method 3: RESTful API

Insert data via HTTP requests - perfect for IoT devices and web applications.

### API Syntax

```json
{
  "values": [
    [TAG_NAME, TAG_TIME, VALUE],
    [TAG_NAME, TAG_TIME, VALUE],
    ...
  ],
  "date_format": "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"
}
```

If `date_format` is omitted, the default format `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn` is used.

Time-axis tag tables use timestamp strings as the axis value, while distance-axis tag tables use numeric values that match the axis column type.

### API Example

```bash
curl -X POST http://localhost:5657/machiot/datapoints/raw/TAG \
  -H "Content-Type: application/json" \
  -d '{
    "date_format": "YYYY-MM-DD HH24:MI:SS",
    "values": [
      ["TAG_0001", "2024-01-01 10:00:00", 25.5],
      ["TAG_0001", "2024-01-01 10:01:00", 26.0],
      ["TAG_0002", "2024-01-01 10:00:00", 30.2]
    ]
  }'
```

> **When to use**: IoT devices, real-time data streaming, web applications

## Method 4: SDK Integration

Use Machbase SDKs for programmatic data insertion from your applications.

### Supported Languages

- **[C/C++ library](../../../sdk-integration/cli-odbc/)** - High-performance native integration
- **[Java library](../../../sdk-integration/jdbc/)** - Java applications
- **[Python library](../../../sdk-integration/python/)** - Data science and automation
- **[C# library](../../../sdk-integration/dotnet/)** - .NET applications

### Python Example

```python
import machbaseAPI as mach

# Connect to Machbase
conn = mach.connect(host='localhost', port=5656)

# Insert data
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO tag VALUES (?, ?, ?)
""", ('TAG_0001', '2024-01-01 10:00:00', 25.5))

conn.commit()
conn.close()
```

> **When to use**: Application integration, automated data collection, custom tools

## Choosing the Right Method

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **INSERT** | Testing, small datasets | Simple, interactive | Slow for large data |
| **CSV Import** | Bulk loading, migration | Very fast, efficient | Requires file preparation |
| **RESTful API** | IoT, web apps | Flexible, platform-independent | Network overhead |
| **SDK** | Applications | Full control, type-safe | Requires development |

## Working with Additional Columns

If your tag table has additional columns, include them in your insert:

The axis value must always match the table definition and column order. Time-axis tables expect a `DATETIME` value, while distance-axis tables expect `DOUBLE`, `LONG`, or `ULONG`.

```sql
-- Tag table with additional columns
CREATE TAG TABLE sensors (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    location VARCHAR(50),
    status SHORT
);

-- Insert with additional columns
INSERT INTO sensors VALUES (
    'TEMP_001',
    '2024-01-01 10:00:00',
    25.5,
    'Building A',
    1
);
```

## Best Practices

1. **Register Tag Metadata When Needed**: Missing tag names are auto-registered; insert metadata first when you need explicit metadata values. `_LAST_UPDATE_TIME` is managed automatically by the server, so do not enter it directly
2. **Use Batch Operations**: For large datasets, use CSV import or batch API calls
3. **Handle Errors**: Always check return values and log errors
4. **Time Precision**: Be consistent with timestamp precision across your data
5. **Validate Data**: Ensure tag names and timestamps follow your naming and time conventions

## Performance Tips

- **CSV Import**: Fastest for bulk data (millions of rows)
- **Batch Inserts**: Group multiple INSERT statements in transactions
- **Parallel Loading**: Use multiple csvimport processes for parallel ingestion
- **Prepared Statements**: Use parameterized queries in SDKs for better performance

## Next Steps

- Learn about [Querying Tag Data](../querying-data) for data retrieval
- Explore [Tag Indexes](../tag-indexes) for query optimization
- Understand [Rollup Tables](../rollup-tables) for time-series aggregation
