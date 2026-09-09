---
type: docs
title: '12.2 Data Modeling for Performance'
weight: 20
toc: true
---

Choose table types and schemas that fit the data lifecycle, query keys, and update patterns.
Do not try to compensate for an unsuitable table type through configuration or indexes alone.

<a id="table-types-selection-schema-type-tuning"></a>

<a id="table-type-선택"></a>

## Choose a table type

| Data | Consider first |
|--------|-----------|
| Time series centered on names, timestamps, and numeric values | TAG |
| Append-oriented events and logs | LOG |
| Relational changes and transactions | TRANSACTION |
| Small persistent reference datasets | LOOKUP |
| Rebuildable in-memory caches | VOLATILE |

<a id="schema-기준"></a>

## Schema design criteria

- Include only columns needed for queries and ingestion.
- Set string lengths based on observed maxima and possible growth.
- Use the appropriate SQL types for timestamps, numbers, and IP addresses instead of strings.
- Store relatively stable tag attributes in TAG metadata.
- Align nullability and defaults with business meaning.
- Compare the lifecycle and mutability of natural and surrogate relational keys.

Do not apply a uniform spare-capacity ratio to string lengths. Measure current distributions,
limits, and truncation impact, and prepare a schema change procedure.

<a id="index와-집계"></a>

## Indexes and aggregates

Choose index candidates from query predicates and join keys. When adding an index, measure
ingestion latency, storage, and memory as well as read improvements. Consider ROLLUP for repeated
TAG time aggregates, and avoid creating aggregation intervals that are rarely queried.

## Validation procedure

1. Prepare representative data and queries.
2. Measure a baseline with the chosen table type and a minimal schema.
3. Add one index or ROLLUP.
4. Remeasure reads, writes, memory, and storage.
5. Remove structures that are not worth maintaining.

For detailed design by table type, see
[Table Type Concepts and Selection](/dbms/data-modeling-table-design/).
