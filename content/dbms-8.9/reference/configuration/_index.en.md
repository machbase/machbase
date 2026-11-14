---
type: docs
title: '16.2 Configuration Reference'
weight: 20
toc: true
---

Machbase server behavior is controlled by properties in `$MACHBASE_HOME/conf/machbase.conf`. This
section provides a quick reference to each property's allowed range and default value.

## Subsections

| Section | Description |
|------|------|
| [Configuration Property Dictionary](./configuration/) | Standard Edition properties for server operation, performance, security, and logging |
| [Cluster Configuration Property Dictionary](./configuration-2/) | Cluster Edition properties for Coordinator, Broker, and Warehouse nodes |
| [PVO Cache Property Dictionary](./pvo-cache/) | SQL execution plan cache (PVO Statement Cache) properties |
| [Timezone Configuration Dictionary](./configuration-timezone/) | Timezone properties and client timezone settings |

## Checking Property Values

Query the `v$property` system view to check current property values while the server is running.

```sql
-- Query all properties
SELECT name, value, type FROM v$property ORDER BY name;

-- Query a specific property
SELECT name, value, min, max
  FROM v$property
 WHERE name = 'PORT_NO';
```

## Dynamically Configurable Properties

Some properties can be changed with `ALTER SYSTEM SET` without restarting the server.

```sql
ALTER SYSTEM SET TRACE_LOG_LEVEL = 3;
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 536870912;
```

Query `v$property` after a change to verify that it took effect. Attempting to change a property
that requires a restart returns an error.
