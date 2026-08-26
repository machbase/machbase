---
type: docs
title: '4. Table Type Selection and Schema Design'
weight: 40
toc: true
---

Choose a table from data shape, mutation, persistence, transaction, and query requirements, then
design its schema and validate patterns. Read [Data model concepts](/dbms/core-concepts/concepts/)
first if the table roles are unfamiliar.

## Contents

| Section | Scope |
|---|---|
| [Choose a table type](table-types-selection-type/) | Decision flow and focused comparisons |
| [Schema objects](schema-objects-definition/) | Tables, columns, types, constraints, indexes, and views |
| [Data mutation policy](alter-data-mutation-policy/) | UPDATE, DELETE, and TRUNCATE boundaries |
| [Anti-patterns](table-types-patterns-type-anti/) | Incorrect table and schema choices |
| [Modeling patterns](patterns-modeling/) | Time-series, event, state, reference, and business models |

This chapter owns design decisions. Product behavior and storage principles remain in Chapter 2;
exact syntax and hard support matrices remain in Chapter 17.
