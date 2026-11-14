---
type: docs
title: '6. ROLLUP for TAG Tables'
weight: 60
toc: true
---

ROLLUP preaggregates data from time-axis TAG tables and combines the stored statistics at query time
to reduce repeated analysis cost. This chapter distinguishes basic, conditional, extension, JSON,
and Custom ROLLUP in Machbase DBMS 8.7.0, covering creation, result validation, and rebuilding.

## Distinguish Three Intervals

| Concept | Meaning | Example |
|---|---|---|
| Creation INTERVAL | Width of stored aggregation buckets | 1 MIN |
| WAKEUP INTERVAL | How often the aggregation job wakes up | 10 SEC |
| Query bucket | Result interval requested by a report | `rollup('min', 5, time)` |

Multiple partial aggregates can be stored for the same bucket. Basic ROLLUP public query syntax
merges the required statistics; for Custom target TAG tables, users write the final reaggregation
query. Define source retention separately from ROLLUP retention and rebuild policies.

## Chapter Contents

| Section | Topics |
|---|---|
| [Overview and Use Criteria](./overview-use-criteria/) | Basic exercise and source/aggregate comparison |
| [Target TAG Design](./target-tag-table-design/) | ON/FROM, hierarchy constraints, and capacity estimates |
| [Creation and Deletion](./create-delete-rollup/) | CREATE, WITH ROLLUP, IF NOT EXISTS, and dependencies |
| [Query Syntax](./query-syntax-rollup/) | Candidate selection, time units, and origin |
| [Conditional ROLLUP](./conditional-rollup/) | Source filters and explicit candidate selection |
| [Custom ROLLUP](./custom-rollup/) | Reaggregating incremental results and OHLCV hierarchies |
| [Extension ROLLUP](./extension-rollup/) | FIRST/LAST and OHLC validation |
| [JSON ROLLUP](./json-summarized-rollup/) | Path/full-document aggregation and NULL |
| [Control and Status](./ingestion-control-rollup/) | STOP/START/WAKEUP/FORCE, V$ROLLUP, and gaps |
| [REBUILD](./rollup-rebuild/) | Supported targets, bucket boundaries, and corrections |
| [Performance Tuning](./performance-tuning-rollup/) | Comparing costs for equivalent results |
| [Usage Scenarios](./patterns-scenarios/) | Multiple tags and source/aggregate responsibilities |

Each page is a standalone exercise with object names beginning with `ch6_`. Check for conflicts with
existing business objects and keep intentional-error examples separate from success scripts. Query
fixed-time data using the stated fixed ranges. Clean up only the exercise tables and ROLLUPs.

Custom and REBUILD are Standard Edition only. Creating a ROLLUP or successfully ingesting data does
not mean aggregation has finished. Exercises use a named FORCE call to catch up processing and then
check results.

Continue with [Support Scope](../reference/support-scope-constraints/rollup/) and
[Troubleshooting](../troubleshooting/rollup/) for limitations and diagnosis.
