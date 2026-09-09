---
type: docs
title: '10. VOLATILE Table Usage'
weight: 100
toc: true
---

VOLATILE tables are in-memory tables shared across the server process. This chapter covers data loss
on restart, UPSERT, and cache patterns that can be rebuilt.

## Chapter Contents

| Section | Topics |
|----|------|
| [Overview and Use Criteria](./overview-use-criteria/) | Characteristics and selection criteria |
| [Table Structure and Schema](./table-structure-schema/) | PRIMARY KEY design, column types, and schema structure |
| [Create, Alter, and Drop](./create-alter-drop/) | CREATE VOLATILE TABLE, DROP, and persistence differences |
| [Data Ingestion and Modification](./data-input-mutation/) | INSERT, ON DUPLICATE KEY UPDATE, and DELETE |
| [Queries and Analysis](./query-analysis/) | SELECT, predicate queries, and LIKE |
| [Indexes and Performance](./index-performance/) | Red-black tree indexes and primary key indexes |
| [Operations and Data Lifecycle](./operations-lifecycle/) | Operational procedures and data management |
| [Constraints, Errors, and Troubleshooting](./constraints-errors-troubleshooting/) | Feature limitations and error handling |
