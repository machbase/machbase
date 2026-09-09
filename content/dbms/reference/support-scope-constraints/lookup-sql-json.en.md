---
type: docs
title: '16.6.5 LOOKUP SQL/JSON Support'
weight: 50
toc: true
---

This page lists LOOKUP table SQL features and JSON constraints.

## Feature Support

| Feature | Support | Notes |
|------|:---:|------|
| **Basic CRUD** | | |
| INSERT | O | Ordinary INSERT |
| SELECT | O | Primary key and general predicates are supported |
| UPDATE (PK predicate) | O | Uses the primary key fast path |
| DELETE (PK predicate) | O | Uses the primary key fast path |
| UPDATE (general predicate) | O | Collects matching primary keys, then updates rows |
| DELETE (general predicate) | O | Collects matching primary keys, then deletes rows |
| **JSON Features** | | |
| JSON columns | O | Create, store, query, and update ordinary columns |
| JSON path query (`$.key`) | O | Supports `->`, `JSON_EXTRACT_*`, `JSON_TYPEOF`, and `JSON_IS_VALID` |
| JSON PK | X | JSON columns cannot be primary keys |
| JSON path index | X | Separate JSON path indexes are not supported |
| **Other Features** | | |
| Explicit transactions (`BEGIN`/`COMMIT`/`ROLLBACK`) | X | DML is applied per statement; multiple statements cannot be rolled back together |
| Prepared Statement | O | Parameter binding for primary key and general predicates |
| Append API | △ | Ordinary SQL INSERT is the default; Append follows a separate LOOKUP append policy |


## Canonical References

For LOOKUP JSON schemas and examples, see
[JSON Columns and Queries](../../../lookup-table-usage/json-column-query/). For UPDATE/DELETE
syntax, see [DML Syntax](../../sql/syntax/dml-syntax/).
