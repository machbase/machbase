---
type: docs
title: '2.1 Data Model Concepts'
weight: 10
toc: true
---

A data model defines what one record represents, how records are identified, and how they are
changed and queried. A time-series model also defines the meaning of the measurement target,
timestamp, and value. Establishing these rules before choosing column names helps keep ingestion
and analysis consistent.

<a id="time-series"></a>

## Understanding Time-Series Data

Time-series data records observations or events over time. Examples include temperature
measurements, trade histories, and service errors. Records may be collected at fixed intervals or
only when events occur. Storage order is not guaranteed to match event order.

### What One Row Represents and How It Is Identified

If one temperature-history row means “the value measured by one sensor at a particular time,”
you need a sensor identifier, measurement timestamp, and value. The identifier tells you where
the data came from, while the timestamp provides a basis for interpreting changes over time.

Multiple sensors can report at the same time, so a timestamp alone cannot uniquely identify a row.
Retransmission can also repeat a reading for the same sensor and timestamp. Decide whether to
allow duplicates, remove them, or introduce a separate event identifier. A TAG `PRIMARY KEY`
identifies a tag; it does not require every measurement row to have a unique name as a relational
row key would. See [TAG Table Operations](../../tag-table-usage/operations-lifecycle/) for
duplicate handling.

### Values, Units, and Quality

A number alone does not explain its unit or meaning. The same `23.5` could represent temperature,
pressure, or voltage. Manage units and measurement locations in tag definitions or reference
data, and keep the meaning of values consistent within a series.

Also distinguish `NULL` from `0`. Measuring zero is different from failing to obtain a value.
Record quality or status in another column when needed. A period with no collection may have no
rows at all, which is different from rows containing NULL.

Common aggregates such as `AVG` operate on non-NULL values. Filling all missing values with zero
or aggregating values with different units changes the result. For the exact NULL behavior of
supported aggregates, see the [Function Reference](../../reference/sql/functions/functions-full/).

### Time-Series Workload Characteristics

Many time-series systems continuously add rows and query time ranges for particular targets.
They may combine monitoring of current values with analysis over long periods. These patterns
motivate append-oriented ingestion, range queries, and ROLLUP.

Historical data is not necessarily immutable, however. Incorrect equipment clocks, sensor
calibration, or duplicate collection may require corrections. Some workloads read older data
more often than recent data. Design around measured ingestion, query, and correction patterns.

### Table-Type Roles

| Table type | Conceptual role |
|---|---|
| TAG | Measurement histories organized by name and a time or distance axis |
| LOG | Events and logs that continuously accumulate new records |
| TRANSACTION | Business data requiring transactions and row-level changes |
| LOOKUP | Persistent reference data loaded into memory |
| VOLATILE | Shared in-memory state that can be recreated after a restart |

Separating history from reference data reduces repetition of equipment names or locations in
every measurement row. However, joining historical records to current reference data also shows
current names or locations. If you need information as it was when an event occurred, store it
with the event or design a separate history of reference-data changes.

<a id="differences-rdbms"></a>

### Relational Business Models and Time-Series Models

Relational and time-series models are not mutually exclusive. A relational DBMS can store time
series and use indexes, partitions, and aggregates. Machbase also provides tables, SQL, joins, and
relational changes. Compare the main workload rather than the product names.

| Perspective | Relational business-data example | Time-series history example |
|---|---|---|
| Meaning of a row | The current state of an order | One sensor measurement or event |
| Change pattern | Update or delete a row found by key | Add records and correct or remove relevant ranges |
| Query pattern | Key lookups, condition searches, and joins of business tables | Target and time-range queries, trends, and interval statistics |
| Consistency requirements | Commit or cancel several changes together | Manage missing, duplicate, or delayed input and when it becomes queryable |
| Retention design | Business lifecycle and change history | Raw-data resolution, aggregation intervals, and retention periods |

Do not apply the storage and ingestion characteristics of LOG and TAG unchanged to TRANSACTION,
LOOKUP, or VOLATILE. For the final choice, see
[Table Type Selection](../../data-modeling-table-design/table-types-selection-type/) and
[Data Mutation Policy](../../data-modeling-table-design/alter-data-mutation-policy/).

<a id="write-oriented-append-only"></a>

## Write-Oriented Workloads and the Append-Only Model

Appending adds a new row instead of overwriting an existing value. For example, recording a new
event when equipment changes from `RUNNING` to `STOPPED` preserves both the previous state and
the transition time. You can also maintain separate tables for direct access to current state
and for its history of changes.

### Table Types and Change Models

LOG is an append-oriented history table and does not support general row `UPDATE`. TAG adds
measurement history and can correct DATA values within supported conditions and Edition limits.
This differs from a general row update that can arbitrarily change tag names or the time axis.

TRANSACTION provides relational DML and explicit transactions. LOOKUP and VOLATILE support
reference-data or state changes. Check
[Data Mutation Policy](../../data-modeling-table-design/alter-data-mutation-policy/) rather than
assuming that every table type supports the same operations.

Append-oriented design can help reduce contention between repeated input and arbitrary updates
to historical rows. It does not eliminate all internal synchronization or recovery work.
A storage structure alone does not guarantee lock-free execution or a particular throughput.

### SQL Input and SDK Append

SQL `INSERT` submits values through a SQL statement and reports its execution result.
SDK Append is an ingestion API for sending multiple rows during continuous collection.
Follow the SDK's contract for buffering, transmission, error checks, and closing resources.

Putting data into an application buffer, having the server process it, and reaching a point from
which it can be recovered after a failure are different events. Append operations on LOG and TAG
are not rolled back by `ROLLBACK` in an explicit TRANSACTION-table transaction. For Append into
TRANSACTION tables, check your SDK's transaction participation and error-handling contract.
See [Data Input and Export](../../development-tools-integration/data-input-load-export/) for
completion checks and retries.

### Corrections, Schema Changes, and Retention

One way to preserve a correction to an incorrect LOG event is to append a correction event.
Before deleting and reinserting data, check the time-based deletion ranges and input ordering
allowed for LOG. Do not assume that any individual row can be deleted independently.
For TAG values, follow
[TAG Data Correction Design](../../tag-table-usage/tag-data-update-correction/#design-correction-tag).

Adding or dropping columns and changing types are separate capabilities. Schema changes are not
universally prohibited for LOG or TAG; support depends on the table type and DATA or METADATA
area. Check [DDL Syntax](../../reference/sql/syntax/ddl-syntax/) before applying
changes.

Continuously appending raw records increases storage use. Define raw-data retention separately
from the purpose of ROLLUP statistics. Creating aggregates does not by itself delete raw data.

<a id="time-model-arrival-time"></a>

## Time Models and _arrival_time

### Event Time and Arrival Time

Event time is when a device made a measurement or an event occurred. Arrival time is when the
DBMS received the record. If a reading measured at 09:00 arrives at 09:05 after network recovery,
the difference is five minutes. Measurement trends require event time; collection-delay analysis
requires comparing the two timestamps.

Also distinguish precision, time zone, and clock accuracy. Being able to represent nanoseconds
does not mean a sensor clock is accurate to a nanosecond. For the time zone used when parsing or
displaying DATETIME strings, see
[Time Zone Configuration](../../reference/configuration/configuration-timezone/).

### The LOG Table's `_arrival_time`

LOG automatically includes a DATETIME column named `_arrival_time`. With ordinary input that
omits its value, the server records the arrival timestamp. Define a separate DATETIME column
if you also need event time.

```sql
CREATE LOG TABLE device_events (
    device_id VARCHAR(20),
    event_time DATETIME,
    status VARCHAR(20)
);
```

Some input paths explicitly supply `_arrival_time`, so it cannot always be treated as the
actual time of receipt. For ordering and restrictions on explicit values, see
[The LOG Time Model](../../log-table-usage/arrival-time-model/).

```sql
SELECT device_id, event_time, status
FROM device_events
WHERE _arrival_time >= TO_DATE('2026-07-03 09:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND _arrival_time <  TO_DATE('2026-07-03 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY _arrival_time;
```

A half-open interval `[start, end)` includes the start and excludes the end, helping avoid
counting shared boundaries twice when combining adjacent intervals. `BETWEEN` includes both
boundaries; choose the form that matches your purpose. LOG `DURATION` restricts a range using
`_arrival_time`.

### The TAG Table's BASETIME Column

In a time-axis TAG table, the application supplies timestamps in a DATETIME column declared
with `BASETIME`. TAG does not use LOG's automatic `_arrival_time` column.

```sql
CREATE TAG TABLE sensor_values (
    name VARCHAR(128) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

INSERT INTO sensor_values
VALUES ('temp_sensor_01',
        TO_DATE('2026-07-03 08:55:00', 'YYYY-MM-DD HH24:MI:SS'),
        23.1);
```

Here, `name` identifies the sensor, `time` is the measurement timestamp, and `value` is the
measured value. `SUMMARIZED` designates a representative numeric column for related statistics
features such as ROLLUP. Creating the table alone does not create aggregates for every interval
you might need.

TAG also has a BASE DISTANCE model with a numeric axis instead of time. Consider it for
measurements along a distance or position axis, but do not apply time-axis-only functions and
policies unchanged. [TAG Schema](../../tag-table-usage/table-structure-schema/) explains the rules
for each axis.

### Comparing the Two Time Models

| Item | LOG | Time-axis TAG |
|---|---|---|
| Special time column | Automatically created `_arrival_time` | Declared `BASETIME` column |
| Meaning of the input timestamp | Server time by default, or an explicitly supplied value | Time specified by the application |
| Separate event time | Can be stored in an ordinary DATETIME column | BASETIME can represent event time |
| Main design question | Which events and fields will be searched? | Which range of which tag will be analyzed? |

Needing event time does not by itself rule out LOG. Choose a table based on tag structure,
searches, aggregates, and update and deletion conditions, as well as the meaning of time.
DATETIME columns in LOOKUP, VOLATILE, and TRANSACTION are ordinary columns; they do not
automatically acquire the special time-axis behavior of LOG or TAG.

Distinguish storage order from display order, too. Specify `ORDER BY` when result ordering
matters, and add a tie-breaker when rows with identical timestamps must be ordered.
