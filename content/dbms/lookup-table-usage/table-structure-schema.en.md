---
type: docs
title: '9.2 Table Structure and Schema'
weight: 20
toc: true
---
This section covers LOOKUP table structure and schema design.


<a id="lookup-table-design"></a>

## LOOKUP Table Design

LOOKUP tables store code lists and reference data. A PRIMARY KEY identifies each row. They support
UPDATE/DELETE by primary key or general predicates and store data persistently on disk.

### Persistent Storage and In-Memory Queries

LOOKUP uses two layers to provide persistence and in-memory query performance.

1. Modified rows are written to persistent storage so they survive restarts.
2. At startup, the server reads all LOOKUP rows from persistent storage and reconstructs in-memory rows containing all column values.
3. Each in-memory row is registered in the mandatory PRIMARY KEY red-black index.
4. SQL queries use the reconstructed in-memory rows and indexes.

Conceptually, each row can be viewed as a key-value entry.

```
PRIMARY KEY                       Other column values
sensor_id = 'TEMP-01'  ───────►  { site, unit, status, ... }
          key                              value
```

This explains why LOOKUP is particularly suitable for PRIMARY KEY lookups while also providing a SQL
table interface, general predicate queries, JOIN, and secondary indexes. Persistent storage does not
mean that only requested rows are fetched from disk during queries. All rows and red-black secondary
indexes consume memory. Consider variable-length columns, JSON values, and secondary index sizes as
well as row counts when designing the schema.

- **[Use Cases](/dbms/lookup-table-usage/patterns-scenarios/#use-cases-lookup)**
- **[PRIMARY KEY Design](/dbms/lookup-table-usage/primary-key-policy/#design-primary-key)**
- **[Column and Sequence Design](/dbms/lookup-table-usage/sequence-column/#design-column-lookup-sequence)**
- **[JSON Columns and Queries](/dbms/lookup-table-usage/json-column-query/#condition-query-lookup-json)**
- **[Reference Design Patterns](/dbms/lookup-table-usage/patterns-scenarios/#patterns-reference-design)**
- **[Index Strategy](/dbms/lookup-table-usage/index-performance/#index-strategy-lookup)**
- **[PRIMARY KEY Policy](/dbms/lookup-table-usage/primary-key-policy/#policy-lookup-primary-key)**
- **[UPDATE/DELETE with General Predicates](/dbms/lookup-table-usage/predicate-update-delete/)**
- **[Backup and Recovery Support](/dbms/lookup-table-usage/operations-lifecycle/#recovery-support-scope-backup-lookup)**
- **[Limitations and Considerations](/dbms/lookup-table-usage/constraints-errors-troubleshooting/#limitations-lookup)**
