---
title: Rollup
type: docs
weight: 70
---

# Machbase Rollup 

## Introduction: Addressing Performance Challenges in Long-Term Time-Series Aggregation

Analyzing statistical aggregates over extensive temporal ranges or encompassing entire datasets within large-scale time-series databases frequently encounters significant performance constraints. Operations such as calculating the average temperature trend over the preceding quarter, determining the peak pressure recorded over the past year, or identifying the minimum current value and its timestamp within a six-month interval impose substantial computational overhead. These challenges necessitate a mechanism to optimize the performance of aggregate queries, thereby reducing operational costs and query execution times. Machbase addresses this critical requirement through its integrated Rollup feature.

## The Machbase Rollup Mechanism

Machbase introduces Rollup tables as an optimized solution for managing and querying time-series aggregates, offering distinct advantages over traditional methods like manually maintained statistical tables in relational database management systems (RDBMS).

**Comparative Analysis: Rollup Tables vs. Conventional Statistical Tables**

| Feature                  | Machbase Rollup Table                                   | Conventional Statistical Table (RDBMS) |
| :----------------------- | :------------------------------------------------------ | :------------------------------------- |
| **Statistical Granularity Start Time** | Dynamically configurable                         | Immutable post-creation            |
| **Rollup Interval Types**| Predefined: Second, Minute, Hour; Custom intervals possible | Fixed, determined at creation        |
| **Interval Modification**| Dynamically alterable                             | Immutable post-creation            |
| **Creation & Management**| Integrated SQL DDL/DML (CREATE, ALTER, DROP, EXEC)   | External application logic required    |
| **Data Population**      | Automated internal process                              | Manual data insertion/computation    |
| **Supported Aggregates** | MIN, MAX, COUNT, SUM, AVG, SUMSQ; Optional: FIRST, LAST | Defined by user implementation        |
| **Data Source**          | Derived directly and automatically from Tag Table data  | Requires manual data sourcing        |

Machbase automatically generates Rollup tables by processing raw data ingested into Tag tables, streamlining the aggregation process and enhancing usability compared to the complexities of managing external statistical tables.

## Rollup Table Fundamentals

A **Rollup table** is a specialized internal table structure within Machbase designed to store pre-computed time-series aggregates derived from a source Tag table. It facilitates rapid retrieval of statistical summaries over specified time intervals.

*   **Core Aggregation Functions:** MIN, MAX, AVG (Average), SUM, COUNT, SUMSQ (Sum of Squares).
*   **Extended Aggregation Functions (Optional):** FIRST (earliest value within interval), LAST (latest value within interval).
*   **Aggregation Time Units:** Second, Minute, Hour (for Default Rollup); Custom intervals (e.g., 10 seconds, 15 minutes) possible via Custom Rollup.
*   **Rollup Types:**
    *   **Default Rollup:** Automatically generated at standard intervals (Second, Minute, Hour) during Tag table creation.
    *   **Custom Rollup:** User-defined Rollup tables with specific aggregation intervals and potentially cascading sources (Rollup derived from another Rollup).

**Conceptual Data Flow:**

```
+-----------+      +------------------------+      +-----------------+
| Tag Table | ---> | Rollup Building Thread | ---> | Rollup Table(s) |
| (Raw Data)|      | (Internal Aggregation) |      | (Aggregated Data)|
+-----------+      +------------------------+      +-----------------+
```

## Default Rollup

Default Rollup provides a convenient mechanism to automatically generate standard aggregate tables.

### Default Rollup Table Creation

Default Rollup tables for second, minute, and hour intervals can be automatically instantiated when creating a Tag table using the `WITH ROLLUP` clause. The system automatically assigns names to these Rollup tables based on the source Tag table name.

**Syntax:**

```sql
-- Creates Rollup tables for 1-second, 1-minute, and 1-hour intervals (equivalent to WITH ROLLUP(SEC))
CREATE TAG TABLE tag_table_name (
    name VARCHAR(...),
    time DATETIME,
    value DOUBLE
) WITH ROLLUP;

-- Explicitly creates Rollup tables for 1-second, 1-minute, and 1-hour intervals
CREATE TAG TABLE tag_table_name (
    name VARCHAR(...),
    time DATETIME,
    value DOUBLE
) WITH ROLLUP (SEC);

-- Creates Rollup tables for 1-minute and 1-hour intervals
CREATE TAG TABLE tag_table_name (
    name VARCHAR(...),
    time DATETIME,
    value DOUBLE
) WITH ROLLUP (MIN);

-- Creates only the 1-hour interval Rollup table
CREATE TAG TABLE tag_table_name (
    name VARCHAR(...),
    time DATETIME,
    value DOUBLE
) WITH ROLLUP (HOUR);
```

### Querying Default Rollup Data

Aggregated data stored in Rollup tables is accessed using the `ROLLUP()` pseudo-function within `SELECT` statements. This function directs the query planner to utilize the appropriate pre-computed aggregates instead of processing the raw Tag table data.

*   **Query Aggregation Units:** `sec`, `min`, `hour`. The query interval can be extended to multiples or standard calendar units like `day`, `month`, `year`.
*   **Supported Aggregate Functions in Query:** `min()`, `max()`, `avg()`, `sum()`, `count()`, `sumsq()`. If the `EXTENSION` option was used, `first()` and `last()` are also available.

**Example Query:** Retrieve hourly minimum and maximum values for a specific tag over a month.

```sql
SELECT
    ROLLUP('hour', 1, time) AS hourly_timestamp,
    MIN(value),
    MAX(value)
FROM
    tag_table_name
WHERE
    name = 'TAG_00001'
    AND time BETWEEN TO_DATE('2023-01-01 00:00:00') AND TO_DATE('2023-01-31 23:59:59')
GROUP BY
    hourly_timestamp
ORDER BY
    hourly_timestamp;
```

### Enabling Extended Aggregation Functions (FIRST, LAST)

The `FIRST()` and `LAST()` aggregate functions, which retrieve the value associated with the earliest and latest timestamps within an interval respectively, can be enabled by adding the `EXTENSION` keyword during Rollup creation.

**Syntax:**

```sql
CREATE TAG TABLE tag_table_name (
    name VARCHAR( ... ),
    time DATETIME,
    value DOUBLE
) WITH ROLLUP ( SEC | MIN | HOUR ) EXTENSION;
```

**Example Query with EXTENSION:** Retrieve the first and last value, sum, and count for 4-day intervals.

```sql
SELECT
    ROLLUP('day', 4, time, '2024-01-01') AS interval_start_time,
    FIRST(time, value),
    LAST(time, value),
    SUM(value),
    COUNT(value)
FROM
    tag_table_name
WHERE
    name = 'sensor00000'
    AND time >= TO_DATE('2024-01-01 00:00:00')
    AND time < TO_DATE('2024-03-01 00:00:00')
GROUP BY
    interval_start_time
ORDER BY
    interval_start_time;
```

## Custom Rollup

Custom Rollup allows for the creation of Rollup tables with user-defined aggregation intervals, potentially based on existing Tag tables or other Rollup tables.

### Custom Rollup Creation

Define a custom Rollup table using the `CREATE ROLLUP` statement, specifying the target column, interval, and time unit.

**Syntax:**

```sql
CREATE ROLLUP custom_rollup_name
ON source_table_or_rollup_name (column_to_aggregate)
INTERVAL interval_value time_unit [EXTENSION];
-- time_unit: SEC, MIN, HOUR
```

**Examples:**

```sql
-- Create a 10-second Rollup on the 'value' column of the 'tag' table
CREATE ROLLUP _tag_rollup_10sec ON tag(value) INTERVAL 10 SEC;

-- Create a 10-minute Rollup based on the previously created 10-second Rollup
CREATE ROLLUP _tag_rollup_10min ON _tag_rollup_10sec INTERVAL 10 MIN;

-- Create a 1-hour Rollup on the 'value' column of the 'example' table
CREATE ROLLUP _tag_rollup_hour ON example(value) INTERVAL 1 HOUR;
```

**Querying Constraint:** When querying data using a Custom Rollup, the interval specified in the `ROLLUP()` function must be an integer multiple of the base `INTERVAL` defined during the `CREATE ROLLUP` statement for that specific Rollup table.

**Query Examples (Based on `_tag_rollup_10sec`):**

```sql
-- Valid: Query interval (30 sec) is a multiple of base interval (10 sec)
SELECT ROLLUP('sec', 30, time) AS time, SUM(value), AVG(value) FROM tag GROUP BY time ORDER BY time;

-- Valid: Query interval (10 sec) is equal to the base interval (10 sec)
SELECT ROLLUP('sec', 10, time) AS time, SUM(value), AVG(value) FROM tag GROUP BY time ORDER BY time;

-- Invalid: Query interval (5 sec) is not a multiple of base interval (10 sec) - This query will result in an error.
SELECT ROLLUP('sec', 5, time) AS time, SUM(value), AVG(value) FROM tag GROUP BY time ORDER BY time;
```

### Custom Rollup Lifecycle Management

Control the operation and data collection process of Custom Rollup tables.

**Syntax:**

```sql
-- Activate the Rollup aggregation process for a specific Rollup table
EXEC ROLLUP_START('rollup_name');

-- Deactivate the Rollup aggregation process for a specific Rollup table
EXEC ROLLUP_STOP('rollup_name');

-- Force immediate execution of the aggregation process for the specified Rollup, overriding the standard interval wait time
EXEC ROLLUP_FORCE('rollup_name');
```

**Examples:**

```sql
EXEC ROLLUP_START('_tag_rollup_10sec');
EXEC ROLLUP_STOP('_tag_rollup_10min');
EXEC ROLLUP_FORCE('_tag_rollup_hour');
```

## Rollup Data Management: Deletion

Rollup data persists independently of the source Tag table data. Deleting data from a Tag table does not automatically remove the corresponding aggregated data from associated Rollup tables. Specific commands are required to manage Rollup data lifecycle.

**Syntax for Deleting Rollup Data:**

```sql
-- Delete all Rollup data associated with 'table_name' prior to a specific timestamp
DELETE FROM table_name ROLLUP BEFORE TO_DATE('YYYY-MM-DD HH24:MI:SS');

-- Delete all Rollup data associated with 'table_name'
DELETE FROM table_name ROLLUP;

-- Delete all Rollup data for a specific tag ('TAG01') associated with 'table_name'
DELETE FROM table_name ROLLUP WHERE name = 'TAG01';

-- Delete Rollup data for a specific tag ('TAG01') associated with 'table_name' up to a certain time
DELETE FROM table_name ROLLUP WHERE name = 'TAG01' AND time <= TO_DATE('YYYY-MM-DD HH24:MI:SS');
```

**Deleting Rollup Tables with Source Table:**

To remove all associated Rollup tables when dropping the source Tag table, use the `CASCADE` option.

```sql
DROP TABLE tag_table_name CASCADE;
```

## Monitoring Rollup Status: The Rollup Gap

The **Rollup Gap** represents the state where recently ingested data into the source Tag table has not yet been processed and incorporated into the corresponding Rollup table(s). This signifies a potential latency in the availability of the latest aggregated data.

*   **Monitoring:** Use the `SHOW ROLLUPGAP` command to inspect the current status of Rollup processing for all active Rollup configurations.
    *   The `GAP` column indicates the number of source data blocks (or partitions) pending aggregation. A value of `0` signifies that the Rollup is synchronized with the source data.
*   **Immediate Mitigation:** If a gap exists, `EXEC ROLLUP_FORCE('rollup_name')` can be executed to trigger an immediate aggregation cycle for the specified Rollup table.
*   **Addressing Persistent Gaps:** Continuous or growing gaps typically indicate that the system's resources are insufficient to keep pace with the data ingestion rate and the overhead of Rollup processing. Potential remediation strategies include:
    *   **Increase Parallelism:** Increment the `TAG_PARTITION_COUNT` property. This enhances parallel processing of Rollup tasks but consumes additional memory resources.
    *   **Hardware Enhancement:** Augment CPU core count, increase CPU clock speed, or improve Disk I/O subsystem performance.
    *   **Ingestion Rate Control:** Reduce the rate at which data is ingested into the source Tag table if system limits are consistently exceeded.

*Note: If the data ingestion volume perpetually surpasses the system's processing capacity, the Rollup Gap will inevitably expand.*

## Limitations of the Rollup Feature

While powerful, the Rollup feature has inherent limitations:

*   **Fixed Aggregate Function Set:** The feature supports a predefined set of aggregate functions (MIN, MAX, COUNT, SUM, AVG, SUMSQ, optionally FIRST, LAST). If custom or more complex statistical calculations are required, alternative processing methods (e.g., external applications, complex SQL queries on raw data) might be necessary.
*   **Sensitivity to Source Data Quality:** Erroneous or outlier data points ingested into the source Tag table will be incorporated into the Rollup aggregates. Data cleansing or validation prior to ingestion is crucial for maintaining the accuracy of Rollup data.
*   **Resource Contention and Latency:** Rollup processing consumes system resources (CPU, I/O, memory) as it reads from the Tag table, computes aggregates, and writes to the Rollup table. Under heavy data ingestion loads, resource contention can lead to delays (Rollup Gap) in reflecting the latest data within the Rollup tables. The latency can range from milliseconds to potentially increasing gaps if the system is overloaded.

## Conclusion

Machbase's Rollup feature provides a robust and efficient mechanism for managing and querying time-series data aggregates over extended periods. By automatically pre-computing statistics at various granularities (seconds, minutes, hours, or custom intervals), it significantly accelerates query performance for analytical workloads involving historical trends and summaries. Both Default and Custom Rollup options offer flexibility, while integrated management commands allow for operational control. Understanding the concepts of Rollup Gap and the inherent limitations is essential for effective deployment and monitoring in demanding high-volume time-series environments. The seamless integration with query mechanisms (`ROLLUP()` function) and visualization tools makes it a cornerstone for time-series data analysis within the Machbase ecosystem.
