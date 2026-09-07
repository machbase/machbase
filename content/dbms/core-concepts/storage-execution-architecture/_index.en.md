---
type: docs
title: '2.2 Storage and Execution Architecture'
weight: 20
toc: true
---

Query time is not determined by the length of the SQL statement alone. It also depends on how
much data is read, how effectively conditions narrow that data, and the work required for sorting,
joins, and aggregation. This section explains which costs storage, indexes, and caches reduce.

<a id="architecture-machbase"></a>

## Machbase Architecture Overview

Users send write and query requests through `machsql` or an SDK. The server checks SQL syntax,
objects, and permissions, chooses an execution method, accesses stored data, and returns the
results. Storage and execution behavior depend on the table type and Edition.

### Standard Edition Architecture

Standard Edition handles SQL processing and storage in a single database server. Time-series
ingestion into LOG and TAG, relational changes in TRANSACTION, and reference data or state in
LOOKUP and VOLATILE each use a path suited to the table's characteristics.

```text
Client: machsql or SDK
          | Write and query requests
          v
Machbase DBMS server
  SQL analysis and execution plans
  Table-specific storage and index access
  Memory buffers and background processing
          |
          v
Stored data organized by table type
```

This is a conceptual diagram of the roles involved. It does not mean that every request uses
the same storage path or that an API call immediately writes a disk file.

### Cluster Edition Architecture

Cluster Edition divides work among several node roles. Ordinary application SQL connections
use a Broker, while Warehouses store time-series data and execute queries. Coordinators manage
cluster metadata and node state, Lookup nodes process reference data, and Deployers handle
deployment and node management.

Distributing data across groups shares processing and storage load. Replication within a group
prepares for failures. These are different goals: adding nodes does not make every query faster
by the same factor or automatically recover from every failure.

For feature differences, see [Edition Concepts](../concepts-edition/). Deployment and recovery
procedures are covered in [Cluster Installation](../../installation-deployment-upgrade/cluster-edition/)
and [Cluster Operations](../../operations-configuration-recovery/cluster/).

### Write and Query Flows

A write can be understood as checking the target table and columns, converting and validating
values, and transferring and storing data. SQL and Append APIs report processing results
differently, so applications must follow the error-handling and completion rules of their chosen
path.

A query involves SQL analysis and planning, data access, condition evaluation, aggregation, joins,
sorting, and result delivery. Not every query processes data in exactly that order; the actual
execution plan determines the access order.

<a id="storage-columnar-compression-column"></a>

## Columnar Storage and Compression

### Row-Oriented and Column-Oriented Storage

Row-oriented storage groups values belonging to one row. Column-oriented storage groups values
from the same column. The following illustration compares the ideas; it is not a literal diagram
of the on-disk files.

```text
Logical rows:
  (time1, sensorA, 23.1)
  (time2, sensorA, 23.5)
  (time3, sensorB, 18.0)

Row-oriented:     [time1, sensorA, 23.1] [time2, sensorA, 23.5] ...
Column-oriented:  [time1, time2, time3] [sensorA, sensorA, sensorB] [23.1, 23.5, 18.0]
```

Machbase's LOG and TAG time-series storage uses column-level access and compression. This can
reduce the amount of data read when an analysis needs only a few columns across many rows.
However, even a temperature average may also need sensor and timestamp data to evaluate its
conditions.

Row-oriented systems can also use indexes or partitions to read only relevant ranges. Compare
the number of rows and columns read and the access path, rather than assuming that row-oriented
storage always reads every row or that column-oriented storage is always faster. The relational
storage of TRANSACTION and the memory characteristics of LOOKUP and VOLATILE should not be
interpreted as identical to LOG and TAG storage.

### When Compression Helps

Values in a column share a type, and sensor values or timestamps may exhibit repeated or similar
patterns. These characteristics can help compression. Noisy values, irregular strings, and mixed
input ordering can produce different results.

Time-series timestamps are not necessarily monotonically increasing. Late measurements and input
from multiple sources may be interleaved. Measure compression and processing performance with the
actual types, value distributions, input order, and settings, rather than assuming a particular
algorithm or compression ratio.

### Partitions and Read Ranges

A partition divides data into manageable portions. Using query conditions and stored range
information to skip unrelated portions reduces reads. This is called partition pruning.

LOG and TAG storage units do not necessarily correspond to a user-defined day or month.
The actual access range depends on tag and axis conditions, data distribution, and each table's
storage structure. A time condition alone does not establish that only the necessary data is read;
check execution plans and measurements.

<a id="indexing-basics"></a>

## Indexing Principles

An index is an access path for finding data that matches a condition. It can help when the target
is a small fraction of the data, but another path may be better for an aggregate that reads most
rows. Indexes also require storage and maintenance during writes and updates.

| Table type | Basis for considering access paths |
|---|---|
| TAG | Tag name and ranges on the time or distance axis |
| LOG | `_arrival_time` conditions and supported search indexes |
| TRANSACTION | PRIMARY KEY, UNIQUE, and general indexes |
| LOOKUP and VOLATILE | Memory-resident keys and supported secondary indexes |

“The monthly average for all sensors” and “the last minute of values for sensor A” read different
proportions of the data. Even on the same table, their performance can differ substantially.
For joins, the input row counts and join conditions also matter.

See [Schema Object Definitions](../../data-modeling-table-design/schema-objects-definition/) for
supported indexes and restrictions, and [Index Tuning](../../performance-tuning/index-tuning/)
for measurement and adjustment.

<a id="execution-concepts-plan-cache"></a>

## Caches and Execution Plans

### SQL Execution

The server checks SQL syntax, types, and objects, identifies executable access paths using
conditions and indexes, and processes the actual data. An execution plan describes that method.
The cost of building a plan differs from the cost of reading data according to the plan.

### Plan Reuse and PVO Cache

The PVO Statement Cache reuses parsing, validation, optimization results, and execution plans
for reusable SQL, reducing repeated preparation work. It does not cache result rows: reusing a
plan still requires reading data and evaluating conditions.

Caches such as Min-Max Cache use stored range information to reduce the data that needs to be
read. Distinguish execution-plan caching from caches used for data access. Decide which cache
to enlarge after examining hit rates and memory use.

### Inspecting a Plan with EXPLAIN

The following example uses the `sensor_values` table created in
[Data Model Concepts](../concepts/#time-model-arrival-time).

```sql
EXPLAIN SELECT AVG(value)
FROM sensor_values
WHERE name = 'temp_sensor_01'
  AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD')
  AND time <  TO_DATE('2026-07-03', 'YYYY-MM-DD');
```

Use the plan to inspect data access and condition evaluation. A plan alone does not show the
actual response time or amount of disk I/O, so also measure execution with representative data.
Distinguishing a first run with empty caches from a run that reuses cached information makes the
results easier to interpret.

Check PVO cache hit and eviction statistics in `V$PVO_CACHE_STAT` and cached SQL in
`V$PVO_CACHE_LIST`. For configuration and diagnosis, see
[Cache and Memory Tuning](../../performance-tuning/cache-tuning-memory/#pvo-cache).
