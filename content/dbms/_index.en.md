---
type: docs
title: 'Machbase DBMS Manual'
weight: 30
toc: true
---

This manual is being reorganized around table-type usage. Korean content is authoritative during this restructuring pass; English pages keep the same chapter structure.

## Manual Structure

| Chapter | Title | Scope |
|----|------|------|
| 1 | [Getting Started](./getting-started/) | Overview, connection checks, quick start |
| 2 | [Core Concepts](./core-concepts/) | Table types, time model, ROLLUP, STREAM |
| 3 | [Installation, Deployment, and Upgrade](./installation-deployment-upgrade/) | Installation and edition-specific deployment |
| 4 | [Table Type Concepts and Selection](./data-modeling-table-design/) | Table type comparison and selection |
| 5 | [TAG Table Usage](./tag-table-usage/) | TAG structure, metadata, input, query, correction, operations |
| 6 | [ROLLUP for TAG Tables](./tag-rollup-usage/) | ROLLUP design, creation, query, rebuild, operations |
| 7 | [LOG Table Usage](./log-table-usage/) | LOG structure, input, text search, Collector, Fluentd, STREAM |
| 8 | [RDB Table Usage](./rdb-table-usage/) | RDB schema, DML, transactions, JOIN, backup constraints |
| 9 | [LOOKUP Table Usage](./lookup-table-usage/) | Reference data, primary keys, sequence, JSON, and joins |
| 10 | [VOLATILE Table Usage](./volatile-table-usage/) | Memory tables, UPSERT, state cache, restart behavior |
| 11 | [Application Integration](./application-integration/) | Drivers and REST API |
| 12 | [Performance Tuning](./performance-tuning/) | Query, ingestion, and cache tuning |
| 13 | [Operations, Configuration, and Recovery](./operations-configuration-recovery/) | Server operations, backup, Cluster operations |
| 14 | [Accounts, Privileges, and Access Control](./security-access-control/) | Users, privileges, and access control |
| 15 | [Scenario Guides](./scenario-guides/) | Task-oriented scenario guides |
| 16 | [Troubleshooting](./troubleshooting/) | Diagnostics and resolution guides |
| 17 | [Reference](./reference/) | SQL, functions, configuration, and API reference |
