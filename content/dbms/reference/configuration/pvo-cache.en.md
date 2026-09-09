---
type: docs
title: '16.2.3 PVO Cache Property Dictionary'
weight: 40
toc: true
---

PVO Statement Cache reduces repeated SQL processing costs by reusing parsing, validation,
optimization results, and execution plans. This manual does not expand the acronym without a public source.
It is available only in Standard Edition.

## Properties

| Property | Default | Range | Dynamic | Description |
|----------|--------|------|----------|------|
| `PVO_CACHE_ENABLE` | 1 | 0~1 | Yes | Enables PVO Cache. 0=disabled, 1=enabled |
| `PVO_CACHE_MAX_MEMORY_SIZE` | 268435456 | 32768~2^64-1 | Yes | Maximum total PVO Cache memory in bytes. Default: 256MB |
| `PVO_CACHE_SHARD_COUNT` | 16 | 1~256 | No | Number of cache shards. Requires a server restart |
| `PVO_CACHE_MAX_SQL_ENTRIES` | 0 | 0~2^64-1 | Yes | Maximum cached SQL entries. 0=unlimited |
| `PVO_CACHE_MAX_PLANS_PER_SQL` | 512 | 1~512 | Yes | Maximum plans (handles) per SQL statement |

## Property Details

### PVO_CACHE_ENABLE

Controls whether PVO Statement Cache is enabled.

```
PVO_CACHE_ENABLE = 1
```

### PVO_CACHE_MAX_MEMORY_SIZE

Maximum total memory, in bytes, available to PVO Cache. The value is distributed evenly across
`PVO_CACHE_SHARD_COUNT` shards.

```
PVO_CACHE_MAX_MEMORY_SIZE = 536870912   # 512MB
```

### PVO_CACHE_SHARD_COUNT

Number of internal cache shards. This setting applies at initialization and requires a server
restart. Increasing the shard count can reduce lock contention with many concurrent connections.

```
PVO_CACHE_SHARD_COUNT = 32
```

### PVO_CACHE_MAX_SQL_ENTRIES

Maximum number of SQL entries retained in PVO Cache. 0 means unlimited. A configured limit is
distributed across the shards.

```
PVO_CACHE_MAX_SQL_ENTRIES = 10000
```

### PVO_CACHE_MAX_PLANS_PER_SQL

Maximum number of plans retained for one SQL statement. Different bind parameter types can generate
different plans for the same SQL text.

```
PVO_CACHE_MAX_PLANS_PER_SQL = 256
```

## Dynamic Changes

Use `ALTER SYSTEM SET` to apply properties that can be changed without a server restart.

```sql
-- Enable PVO Cache
ALTER SYSTEM SET PVO_CACHE_ENABLE = 1;

-- Set maximum memory to 512MB
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 536870912;

-- Limit the number of SQL entries
ALTER SYSTEM SET PVO_CACHE_MAX_SQL_ENTRIES = 5000;
```

## Clearing the Cache

Use the following command to force a PVO Cache reset.

```sql
ALTER SYSTEM FLUSH PVO_CACHE;
```

## Checking Cache Settings

```sql
SELECT name, value
  FROM v$property
 WHERE name LIKE 'PVO_CACHE%'
 ORDER BY name;
```
