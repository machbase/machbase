---
type: docs
title: '9.1 Overview and Use Criteria'
weight: 10
toc: true
---

LOOKUP tables store relatively small, frequently referenced datasets such as code lists, device
master data, thresholds, and settings. Data is persistent, but all rows used by SQL queries reside
in memory. This makes them suitable for repeated key-based lookups and updates.

<a id="overview-lookup-characteristics"></a>

## LOOKUP Table Characteristics

Create a LOOKUP table with `CREATE LOOKUP TABLE`. A `PRIMARY KEY` is required.

```sql
CREATE LOOKUP TABLE ch9_overview (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    unit      VARCHAR(16),
    status    VARCHAR(16)
);
```

LOOKUP tables have the following characteristics.

| Item | Description |
|------|------|
| Main uses | Code tables, device master data, thresholds, and reference data |
| Requirement | `PRIMARY KEY` required |
| Storage | Persistent storage; all rows loaded into memory at server startup |
| Query patterns | Optimized for primary key lookups; supports general predicates and JOIN with other tables |
| Modification patterns | INSERT, UPDATE, DELETE |
| Additional features | SEQUENCE columns and Append duplicate-key policy |

<a id="overview-lookup-use-criteria"></a>

## Use Criteria

Use a LOOKUP table when:

- The dataset is relatively small and frequently referenced as a whole.
- All rows and required secondary indexes fit in server memory.
- You manage reference information such as codes, names, locations, units, or states.
- Descriptive information must be joined to source data in TAG or LOG tables.
- Reference values, such as thresholds or settings, can change during operation.
- A `PRIMARY KEY` clearly identifies each row.

For a JOIN that adds descriptions such as location and unit to TAG or LOG data, see
[Queries and Analysis](/dbms/lookup-table-usage/query-analysis/).

<a id="overview-lookup-not-use"></a>

## When to Consider Other Tables

Consider other table types for the following requirements.

| Requirement | Recommended table |
|----------|-------------|
| Large volumes of time-series measurements | TAG |
| Append-oriented source events | LOG |
| Large relational datasets that cannot all fit in memory | TRANSACTION |
| Transactions and relational business processing | TRANSACTION |
| Current-state cache kept only in server memory | VOLATILE |

LOOKUP is suitable for reference data. Persistence does not make it a disk-oriented large-volume
table. Store source data in LOG or TAG, and use LOOKUP for memory-resident reference data queried
repeatedly. Use TRANSACTION when relational data exceeds available memory or requires complex
business processing.

Clean up the example table as follows.

```sql
DROP TABLE ch9_overview;
```

<a id="overview-lookup-design-flow"></a>

## Design Sequence

Make the following decisions when designing a LOOKUP table.

1. Choose the `PRIMARY KEY` that identifies each row.
2. Choose a natural key or a surrogate key based on SEQUENCE or AUTO_INCREMENT.
3. Add indexes to columns frequently queried or joined.
4. Validate memory requirements for expected row sizes, row counts, and secondary indexes.
5. Distinguish columns updated during operation from immutable columns.
6. Prepare a query that checks the target scope before bulk changes.

For schema and key design, see
[Table Structure and Schema](/dbms/lookup-table-usage/table-structure-schema/) and
[PRIMARY KEY Policy](/dbms/lookup-table-usage/primary-key-policy/).
