---
type: docs
title: 'Table Types'
weight: 60
---

Detailed reference documentation for Machbase table types. Each section provides syntax, features, and usage patterns.

## Table Types

- [Tag Tables](./tag-tables/) - Sensor/device time-series data
- [Log Tables](./log-tables/) - Event streams and logs
- [Volatile Tables](./volatile-tables/) - Non-persistent memory primary-key tables
- [Lookup Tables](./lookup-tables/) - Persistent reference tables with a memory primary-key index
- [RDB Tables](./rdb-tables/) - Generalized disk row tables

## Quick Reference

| Type | Create Syntax | Storage | Index Model | Persistence | DML Scope |
|------|--------------|---------|-------------|-------------|-----------|
| Tag | `CREATE TAG TABLE` | Disk time-series | Tag + axis index | Yes | `SELECT`, `INSERT`, time-based `DELETE` |
| Log | `CREATE TABLE` | Disk append log | Time partition + optional log indexes | Yes | `SELECT`, `INSERT`, time-based `DELETE` |
| Volatile | `CREATE VOLATILE TABLE` | Memory | Single primary-key memory index | No | Full DML by primary key |
| Lookup | `CREATE LOOKUP TABLE` | Persistent reference data | Single primary-key memory index | Yes | Full DML by primary key |
| RDB | `CREATE RDB TABLE` | Disk row table | Optional primary key, normal, unique, JSON path indexes | Yes | Full row DML and indexed predicates |

For a comprehensive comparison and decision guide, see [Table Types Overview](../core-concepts/table-types-overview/).
