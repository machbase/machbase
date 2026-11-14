---
type: docs
title: '10.2 Table Structure and Schema'
weight: 20
toc: true
---

This section covers primary key design and schema structure for VOLATILE tables.


<a id="primary-key-design-primary-key"></a>

## PRIMARY KEY Design

You can create a VOLATILE table without a PRIMARY KEY. However, a PRIMARY KEY is required for
primary key lookups and `ON DUPLICATE KEY UPDATE`.

### Single PRIMARY KEY

```sql
CREATE VOLATILE TABLE ch10_schema_state (
    device_id  VARCHAR(32) PRIMARY KEY,
    state      VARCHAR(16),
    updated_at DATETIME
);
```

### When a Composite Key Is Needed

If a combination of columns uniquely identifies a row, encode that combination in a separate PRIMARY
KEY column.

```sql
CREATE VOLATILE TABLE ch10_schema_hourly (
    key_id     VARCHAR(96) PRIMARY KEY,
    sensor_id  VARCHAR(64),
    hour_ts    DATETIME,
    avg_value  DOUBLE,
    sample_cnt INTEGER
);

-- Insert composite key values
INSERT INTO ch10_schema_hourly
VALUES ('TEMP-01:2026010110', 'TEMP-01', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 23.5, 60);
INSERT INTO ch10_schema_hourly
VALUES ('TEMP-01:2026010111', 'TEMP-01', TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 24.1, 60);
INSERT INTO ch10_schema_hourly
VALUES ('TEMP-02:2026010110', 'TEMP-02', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 21.0, 60);

-- Query by composite key
SELECT sensor_id, avg_value FROM ch10_schema_hourly
 WHERE key_id = 'TEMP-01:2026010110';
```

### Using ON DUPLICATE KEY UPDATE

```sql
-- Update when the PRIMARY KEY already exists
INSERT INTO ch10_schema_state VALUES ('DEV-01', 'ONLINE', NOW)
ON DUPLICATE KEY UPDATE SET state = 'ONLINE', updated_at = NOW;
```

### Considerations

- A table can be created without a PRIMARY KEY, but primary key operations such as UPSERT and primary key lookups are unavailable.
- Multiple rows cannot have the same PRIMARY KEY. `ON DUPLICATE KEY UPDATE` updates the existing row instead of adding a duplicate.
- Only one column can be designated as the PRIMARY KEY.

<a id="volatile-table-design"></a>

## VOLATILE Table Design

VOLATILE tables keep data only in memory and lose it on server restart. The table definition
remains. Decide which data can be lost and how to reload it. Use these tables for state or caches
shared by multiple sessions that do not need to survive a restart.

Review the following topics when defining the schema.

- [Use Cases](../overview-use-criteria/#use-cases-volatile)
- [Persistence Differences and DDL](../create-alter-drop/#differences-persistence-ddl)
- [Memory Lifecycle](../operations-lifecycle/#lifecycle-memory)
- [Red-Black Tree Indexes](../index-performance/#index-strategy-red-black)
- [ON DUPLICATE KEY UPDATE](../data-input-mutation/#on-duplicate-key-update)
- [Restart and Data Rebuilding](../operations-lifecycle/#data-loss)

Clean up the example tables as follows.

```sql
DROP TABLE ch10_schema_hourly;
DROP TABLE ch10_schema_state;
```
