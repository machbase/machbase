---
title: '9.1 Overview and Use Criteria'
weight: 10
toc: true
---

LOOKUP tables store relatively small, frequently referenced data such as codes, equipment metadata,
thresholds, and configuration values. The data is persistent, but the complete row set used by SQL
queries resides in memory. Conceptually, the `PRIMARY KEY` is the key and the remaining row values are
the value, making LOOKUP especially suitable for key-based access.

## Characteristics

| Item | Description |
|------|-------------|
| Required constraint | One `PRIMARY KEY` |
| Persistence | Persisted and reloaded into memory at server startup |
| Runtime structure | In-memory rows addressed through a primary Red-Black index |
| Query pattern | Optimized for primary-key lookup; also supports predicates and joins |
| Memory usage | Complete rows and all secondary indexes consume server memory |

Use LOOKUP when the complete reference data set fits in server memory and is read repeatedly. Use an
RDB table when a large relational data set should not be fully memory-resident or requires relational
transactions and business processing.
