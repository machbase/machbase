---
type: docs
title: 'Machbase DBMS Manual'
weight: 30
toc: true
---

This manual covers installation, table-type usage, application development, operations, security,
and reference information for Machbase 8.7.0.

If you are new to Machbase, work through the SQL exercises in Chapter 1, then learn data models
and storage and operational principles in Chapter 2. For system design, review table selection
in Chapter 4 before moving to the relevant table chapter. For exact syntax or feature support,
use Chapter 16.

## Manual Structure

| Chapter | Title | Scope |
|----|------|------|
| 1 | [Getting Started](./getting-started/) | Overview, connection checks, quick start, basic commands |
| 2 | [Core Concepts](./core-concepts/) | Table types, time model, ROLLUP, and retention policies |
| 3 | [Installation, Deployment, and Upgrade](./installation-deployment-upgrade/) | Preparation, Standard Edition, Cluster Edition, upgrade |
| 4 | [Table Type Selection and Schema Design](./data-modeling-table-design/) | Type decisions, schema, mutation policy, and patterns |
| 5 | [TAG Table Usage](./tag-table-usage/) | TAG structure, metadata, input, query, correction, operations |
| 6 | [ROLLUP for TAG Tables](./tag-rollup-usage/) | ROLLUP design, creation, query, rebuild, operations, performance tuning |
| 7 | [LOG Table Usage](./log-table-usage/) | LOG structure, input, and text search |
| 8 | [TRANSACTION Table Usage](./rdb-table-usage/) | TRANSACTION schema, DML, transactions, JOIN, backup and recovery |
| 9 | [LOOKUP Table Usage](./lookup-table-usage/) | Reference data, primary keys, JSON, predicate DML, and joins |
| 10 | [VOLATILE Table Usage](./volatile-table-usage/) | Memory tables, UPSERT, state cache, restart and data loss |
| 11 | [Development and Application Integration](./development-tools-integration/) | Integration methods, common concepts, and language-specific SDKs/APIs |
| 12 | [Performance Tuning](./performance-tuning/) | Query, ingestion, and cache tuning |
| 13 | [Operations, Configuration, and Recovery](./operations-configuration-recovery/) | Server operations, backup, and Cluster operations |
| 14 | [Accounts, Privileges, and Access Control](./security-access-control/) | Accounts, privileges, AUTH KEY, and access control |
| 15 | [Troubleshooting](./troubleshooting/) | Diagnostics and resolution guides |
| 16 | [Reference](./reference/) | SQL, functions, configuration, and system catalog reference |
