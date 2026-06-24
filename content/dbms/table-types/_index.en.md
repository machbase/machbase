---
type: docs
title: 'Table Types'
weight: 60
---

Detailed reference documentation for Machbase table types. Each section provides syntax, features, and usage patterns.

## Table Types

- [Tag Tables](./tag-tables/) - Sensor/device time-series data
- [Log Tables](./log-tables/) - Event streams and logs
- [Volatile Tables](./volatile-tables/) - In-memory real-time data
- [Lookup Tables](./lookup-tables/) - Reference and master data
- [RDB Tables](./rdb-tables/) - Persistent row tables for transactional state and reference data

## Quick Reference

| Type | Create Syntax | Best For |
|------|--------------|----------|
| Tag | `CREATE TAG TABLE` | Sensor data (ID, time, value) |
| Log | `CREATE TABLE` | Events, logs, flexible schema |
| Volatile | `CREATE VOLATILE TABLE` | Real-time cache, sessions |
| Lookup | `CREATE LOOKUP TABLE` | Device registry, config |
| RDB | `CREATE RDB TABLE` | Transactional state, dimensions, queues |

For a comprehensive comparison and decision guide, see [Table Types Overview](../core-concepts/table-types-overview/).
