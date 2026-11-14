---
type: docs
title: '9. LOOKUP Table Usage'
weight: 90
toc: true
---

LOOKUP tables load persistently stored reference and master data into memory at server startup,
providing fast access by PRIMARY KEY. This chapter covers the memory-resident architecture, JSON and
SEQUENCE, JOIN, and DML with general predicates.

## Chapter Contents

| Section | Topics |
|----|------|
| [Overview and Use Criteria](./overview-use-criteria/) | Purpose and selection criteria |
| [Table Structure and Schema](./table-structure-schema/) | Columns, primary keys, and schema design |
| [Create, Alter, and Drop](./create-alter-drop/) | CREATE, ALTER, and DROP DDL |
| [Data Ingestion and Modification](./data-input-mutation/) | INSERT, Append, reload, and deletion |
| [Queries and Analysis](./query-analysis/) | SELECT, JOIN, and predicate queries |
| [Indexes and Performance](./index-performance/) | Red-black indexes, secondary indexes, and tuning |
| [Operations and Data Lifecycle](./operations-lifecycle/) | Backup, recovery, and persistence |
| [Constraints, Errors, and Troubleshooting](./constraints-errors-troubleshooting/) | Limitations, error causes, and remedies |
| [Usage Patterns and Scenarios](./patterns-scenarios/) | Code tables, reference data, and thresholds |
| [PRIMARY KEY Policy](./primary-key-policy/) | Natural versus surrogate keys and key immutability |
| [SEQUENCE Columns](./sequence-column/) | Automatic numbering and NEXTVAL |
| [JSON Columns and Queries](./json-column-query/) | Supported JSON features, path predicates, and primary key restrictions |
| [UPDATE/DELETE with General Predicates](./predicate-update-delete/) | Modifications using non-PK, range, string, date, and JSON path predicates |
