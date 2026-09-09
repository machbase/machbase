---
type: docs
title: '10.1 Overview and Use Criteria'
weight: 10
toc: true
aliases:
  - /dbms/volatile-table-usage/patterns-scenarios/
  - /dbms/volatile-table-usage/state-cache-temporary-aggregation/
---

VOLATILE tables store temporary data in memory. Data is lost when the server restarts, so use them
for current state that can be rebuilt, temporary aggregates, and caches shared across sessions.

<a id="overview-volatile-characteristics"></a>

## VOLATILE Table Characteristics

Create a VOLATILE table with `CREATE VOLATILE TABLE`.

```sql
CREATE VOLATILE TABLE ch10_overview (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
```

VOLATILE tables have the following characteristics.

| Item | Description |
|------|------|
| Main uses | Current-state caches, temporary aggregates, and intermediate results |
| Storage | Memory |
| Data after restart | Lost |
| Sharing scope | Server-wide |
| Key | Optional PRIMARY KEY |
| Main features | UPDATE, DELETE, `ON DUPLICATE KEY UPDATE`, and red-black tree indexes |
| Backup | Not supported |

<a id="overview-volatile-use-criteria"></a>
<a id="use-cases-volatile"></a>

## Use Criteria

Use a VOLATILE table when:

- Data may be lost after a server restart.
- Data can be recalculated or rebuilt from its source at any time.
- Current state, recent aggregates, or temporary results require fast queries.
- Multiple sessions need to share the same temporary state.
- In-memory response time is more important than disk persistence.

The following example maintains the latest sensor state.

```sql
INSERT INTO ch10_overview VALUES ('TEMP-01', 23.5, NOW)
ON DUPLICATE KEY UPDATE SET value = 23.5, updated_at = NOW;

SELECT *
FROM ch10_overview
WHERE sensor_id = 'TEMP-01';

-- Clean up because the next section reuses this name.
DROP TABLE ch10_overview;
```

### Usage Patterns

| Pattern | Key | Source for rebuilding | Recommended expiration method |
|------|-----|-------------|----------------|
| Latest device state | Device ID | TAG or LOG | Update the same key |
| Short-interval aggregates | Target and time bucket | TAG or LOG | Replace or rebuild the bucket |
| Job progress | Job ID | Job system | Delete the key after completion |
| Temporary query cache | Request or object ID | Persistent table | Rebuild the entire cache |

For current-state updates, see [Data Ingestion and Modification](../data-input-mutation/). For
temporary aggregates, see [Queries and Analysis](../query-analysis/).

<a id="overview-volatile-not-use"></a>

## When to Consider Other Tables

Use another table type for the following requirements.

| Requirement | Recommended table |
|----------|-------------|
| Source data that must survive a restart | TAG or LOG |
| Persistent reference data, such as code lists or device master data | LOOKUP |
| Business data requiring transactions and relational updates | TRANSACTION |
| Time-series data for long-term analysis | TAG |

Data stored only in a VOLATILE table cannot be recovered after server shutdown. Store important data
in a suitable persistent table: TAG, LOG, LOOKUP, or TRANSACTION. Use VOLATILE tables for caches or
intermediate results.

<a id="overview-volatile-design-flow"></a>

## Design Sequence

Make the following decisions when designing a VOLATILE table.

1. Confirm that the data can be rebuilt.
2. Decide whether a PRIMARY KEY is required.
3. Estimate the row count and memory usage.
4. Prepare an initial load procedure for use after restart.
5. Save results that must be retained to persistent tables through explicit application writes.
   There is no dedicated flush command that persists a VOLATILE table.

For schema and primary key design, see
[Table Structure and Schema](/dbms/volatile-table-usage/table-structure-schema/). For restart
handling, see [Restart and Data Loss](/dbms/volatile-table-usage/operations-lifecycle/).
