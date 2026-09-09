---
type: docs
title: '9.6 Indexes and Performance'
weight: 60
toc: true
---
This section covers LOOKUP index structure and performance tuning.


<a id="index-tuning-lookup-volatile"></a>
<a id="original-85-lookup-indexes"></a>
<a id="index-strategy-lookup"></a>

## Tuning LOOKUP Indexes

A red-black tree index is created automatically for the LOOKUP PRIMARY KEY. All rows and indexes
reside in memory during SQL queries. You can add red-black secondary indexes to non-PK columns when
needed.

### LOOKUP Table Indexes

#### Automatic Primary Key Red-Black Tree Index

Creating a LOOKUP table automatically creates a red-black tree index on its PRIMARY KEY. Each index
entry points to the in-memory row containing all column values for that key. Although the table is
persistent, the query execution path is memory-based and optimized for repeated key lookups on small
reference datasets.

```sql
CREATE LOOKUP TABLE ch9_index_device (
    device_id   VARCHAR(64) PRIMARY KEY,  -- Red-black tree created automatically
    device_name VARCHAR(128),
    location    VARCHAR(256),
    category    VARCHAR(32)
);

INSERT INTO ch9_index_device VALUES ('DEV-01', 'Boiler', 'Seoul', 'temperature');
INSERT INTO ch9_index_device VALUES ('DEV-02', 'Pump',   'Busan', 'pressure');
```

```sql
-- Primary key lookup using the red-black tree index
SELECT device_id, device_name, location FROM ch9_index_device
 WHERE device_id = 'DEV-01';
```

The query returns one row. The LOOKUP side also uses the primary key when joined to event logs.

```sql
CREATE LOG TABLE ch9_index_event (device_id VARCHAR(64), level SHORT);
INSERT INTO ch9_index_event VALUES ('DEV-01', 3);
INSERT INTO ch9_index_event VALUES ('DEV-02', 1);
EXEC TABLE_FLUSH(ch9_index_event);

SELECT e.device_id, e.level, d.location
  FROM ch9_index_event e, ch9_index_device d
 WHERE e.device_id = d.device_id
 ORDER BY e.device_id;
```

The query returns two rows. Adding a time range on the LOG side further reduces source rows read.

#### Secondary Indexes on Non-PK Columns

Red-black secondary indexes can also be created on non-PK columns. Filtering on a column without a
secondary index sequentially scans the entire table.

```sql
-- Add a secondary index to a frequently filtered non-PK column
CREATE INDEX ch9_index_device_location ON ch9_index_device(location);

SELECT device_id FROM ch9_index_device WHERE location = 'Seoul';

-- An unindexed column may require a full scan
SELECT device_id FROM ch9_index_device WHERE category = 'temperature';
```

Both queries return DEV-01. The results match but access paths differ, so compare them with
execution plans on production-scale data.

Secondary indexes speed up queries but increase update cost and memory usage. Create them only on
frequently used predicate columns.

#### LOOKUP Usage Guidelines

Lookup cost for primary key and red-black secondary indexes grows with tree size. Unindexed
predicates scan all memory-resident rows. Do not define capacity limits from row count alone.
Measure actual row sizes, variable-length values, index counts, and query/update ratios under the
same workload. Also check startup time, because startup reads all persistent data to build memory
rows and indexes.

| Usage pattern | Suitability |
|----------|-------|
| Retrieve device information by primary key | Suitable |
| Search lists by non-PK columns | Suitable with secondary indexes |
| Small reference-code tables | Suitable |
| Large reference datasets that do not all fit in server memory | Consider TRANSACTION |
| Reference data requiring relational transactions | Consider TRANSACTION |

### Distinction from VOLATILE

VOLATILE is a separate table type whose data is lost on restart. For its index design, see
[VOLATILE Indexes and Performance](/dbms/volatile-table-usage/index-performance/).

### Large Reference Datasets

Consider alternatives in the following scenario because of LOOKUP table size and secondary-index
update costs.

**Scenario**: Device reference data must be filtered by multiple columns while retaining change history.

```sql
-- Alternative: a LOG table with LSM/BITMAP indexes
CREATE LOG TABLE ch9_index_device_hist (
    device_id   VARCHAR(64),
    device_name VARCHAR(128),
    location    VARCHAR(256),
    category    VARCHAR(32),
    updated_at  DATETIME
);

-- Indexes can be created on non-PK columns
CREATE INDEX ch9_index_hist_location ON ch9_index_device_hist (location);
CREATE INDEX ch9_index_hist_category ON ch9_index_device_hist (category) INDEX_TYPE BITMAP;
```

LOG tables are append-only, so adapt the design to the reference-data update pattern.

Clean up the example objects as follows.

```sql
DROP TABLE ch9_index_device_hist;
DROP INDEX ch9_index_device_location;
DROP TABLE ch9_index_event;
DROP TABLE ch9_index_device;
```

### Key Points

- The PRIMARY KEY index is created automatically.
- Create secondary indexes only for repeated non-PK predicates.
- Measure memory for rows, variable-length values, and indexes, together with startup time and update load.
