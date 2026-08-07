---
type: docs
title: '18.1.2 Data Type Dictionary'
weight: 20
toc: true
---

Machbase supports integer, floating-point, exact fixed-point, datetime, string,
network, binary, text, and JSON data types.

## Exact Fixed-Point

`DECIMAL` is the canonical exact fixed-point type. `NUMERIC`, `DEC`, `FIXED`,
and `NUMBER` are aliases.

```sql
CREATE RDB TABLE invoice (
    id     LONG PRIMARY KEY,
    amount DECIMAL(18,2),
    rate   NUMERIC(7,4)
);
```

`DECIMAL` means `DECIMAL(10,0)`, and `DECIMAL(M)` means `DECIMAL(M,0)`.
Precision ranges from 1 through 65; scale ranges from 0 through 30 and cannot
exceed precision. DECIMAL columns are supported by LOG, TAG, VOLATILE, LOOKUP,
and RDB tables.

See [DECIMAL and NUMERIC Fixed-Point Types](decimal-numeric-fixed-point/) for
rounding, overflow, indexing, expressions, and client mappings.

## Related Types

- [JSON Type Support by Table Type](table-types-type-support-scope-json/)
