---
type: docs
title: '1.4 Choose the Next Document'
weight: 40
toc: true
---

The quick start stored and queried one row. When building a system, you also need to decide
how data changes, which timestamp matters, how it will be queried, and how long to retain it.

## Questions to Answer Before Designing

- Do you accumulate values over time for the same target, or overwrite its current state?
- Do queries use measurement or event time, or the time the server received the data?
- Which operations are most common: ranges for a specific tag, searches across columns, key
  lookups, or joins?
- How will you handle late arrivals, duplicates, and incorrect values?
- How long do you need raw data and aggregates, and which data must survive a restart?
- Which Edition supports the features you need?

## Next Paths

| What you need to do | Next document |
|---|---|
| Understand history, storage, and querying | [Core Concepts](../../core-concepts/) |
| Choose table types and update policies | [Table Type Selection and Schema Design](../../data-modeling-table-design/) |
| Store sensor and measurement histories | [TAG Tables](../../tag-table-usage/) |
| Collect and search events and logs | [LOG Tables](../../log-table-usage/) |
| Query tag statistics over long periods | [ROLLUP for TAG Tables](../../tag-rollup-usage/) |
| Manage reference and business data | [LOOKUP](../../lookup-table-usage/), [TRANSACTION](../../rdb-table-usage/) |
| Manage state that can be recreated | [VOLATILE Tables](../../volatile-table-usage/) |
| Insert and query data from applications | [Development and Application Integration](../../development-tools-integration/) |
| Check SQL syntax and data types | [SQL Reference](../../reference/sql/) |
| Configure operations, backups, and permissions | [Operations, Configuration, and Recovery](../../operations-configuration-recovery/), [Accounts and Permissions](../../security-access-control/) |

Start on a small scale with representative data and common queries. Measure ingestion speed,
query latency, and storage use before adjusting ingestion methods, indexes, aggregates, and
retention policies. [Scenario Guides](../../scenario-guides/) provides examples that combine
multiple table types and features.
