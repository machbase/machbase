---
type: docs
title: '4. Table Type Selection and Schema Design'
weight: 40
toc: true
---

This chapter translates the meaning of your data and its mutation/query requirements into
Machbase DBMS tables and columns. Once the database is running, decide what one row represents.
Choosing a familiar table type first and forcing all data into it can create conflicting
requirements for history, updates, and retention.

If table roles are new to you, first read [Data Model Concepts](/dbms/core-concepts/concepts/).
This chapter connects those concepts to concrete schemas and designs you can validate.

## Start with the Data

Before choosing a table name, describe one row in a sentence. “One measurement from one sensor,”
“one equipment state-change event,” and “the current installation information for one device”
describe different units of data. Records from the same equipment can still have different
storage roles.

| Design question | Decision to make |
|---|---|
| What does one row represent? | A measurement, event, current state, or reference record |
| How is its subject identified? | Tag names, business keys, and duplicate-ingestion identifiers |
| What does the time or axis mean? | Measurement time, receipt time, or distance/position |
| How are values interpreted? | Units, type ranges, precision, NULL, and missing observations |
| Which mutations are needed? | Appends, historical corrections, key changes, and deletion boundaries |
| Which queries recur? | Tag/time ranges, predicate searches, key lookups, aggregates, and joins |
| What must be retained? | Raw data, aggregates, reference history, and state recoverable after restart |
| What can be undone after failure? | Table/API transaction scope, retries, and reconstruction |

Data size or input frequency alone does not determine the table type. Check that values grouped
in a row describe the same observation or event, and design common identifiers for records that
must be joined. Having a join key does not mean the DBMS automatically enforces every business
relationship. Check the constraints supported by the selected table type.

## Contents

| Section | Design outcome |
|---|---|
| 4.1 [Choose a Table Type](./table-types-selection-type/) | A type matching mutation, query, persistence, and Edition requirements |
| 4.2 [Schema Objects](./schema-objects-definition/) | Columns and types, identifiers, defaults/constraints, indexes, and views |
| 4.3 [Data Mutation Policy](./alter-data-mutation-policy/) | Correction/deletion boundaries and failure handling |
| 4.4 [Anti-Patterns](./table-types-patterns-type-anti/) | Reasons to revise choices that do not match requirements |
| 4.5 [Modeling Patterns](./patterns-modeling/) | Concrete combinations of history, state, and reference data |

Choose a type in 4.1 and define structure and mutation rules in 4.2–4.3. Check the anti-patterns in
4.4, then adapt the patterns in 4.5 to your data. Comparison tables are starting points; follow
the linked table guides and references for exact SQL and supported conditions.

## An Equipment-Monitoring Example

Temperature, alarms, equipment definitions, and display state need not use the same storage model.

| Data | Meaning of one row | Storage role to consider |
|---|---|---|
| Temperature history | One sensor reading at a particular time | TAG for tag/time-range queries and aggregation |
| Alarm history | One alarm event at a particular time | LOG for append-oriented events |
| Equipment reference data | One device's name, location, and thresholds | LOOKUP, or TRANSACTION when multiple changes must share a transaction |
| Current display state | Recent state that can be recalculated | VOLATILE when authoritative data and a rebuild path exist |

This is an example, not a fixed prescription. A record containing several measurements, or different
mutation and retention requirements, may call for another design. Check Standard Edition support
when considering TRANSACTION.

Joining temperature history to current equipment definitions interprets that history using today's
names and locations. If you need the location or threshold at measurement time, retain it with
the history or model changes to the reference data. When maintaining a current-state cache, do not
assume the history insert and cache update form one transaction. Prepare a way to rebuild the cache
after failure.

## Validate with a Small Data Set

Before scaling up, use representative records and common queries to check the design.

1. Insert normal values together with NULLs, missing observations, boundary values, and duplicate
   or late-arriving records.
2. Check that raw queries and aggregates use the same time basis, units, and NULL policy.
3. Compare results after corrections, deletion, and reingestion, including effects on related
   rows and aggregates.
4. Distinguish data that must survive restart from state that must be recreated, and verify the
   recovery sequence.
5. Increase ingestion rate, query range, and concurrency while measuring throughput, latency,
   and storage.

Design for input failures, applications using old schemas, and restart recovery alongside the
normal workflow. Before evolving a schema, inspect existing data and dependencies in views,
ROLLUPs, and clients. When needed, migrate to a new table, validate it, and then switch over.

Continue with the [Table Usage Chapters](/dbms/) and
[Development and Application Integration](/dbms/development-tools-integration/) for implementation,
and [Performance Tuning](/dbms/performance-tuning/) for measurement.
