---
type: docs
title: '18.1.2.2 DECIMAL and NUMERIC Fixed-Point Types'
weight: 20
toc: true
---

`DECIMAL` is an exact base-10 fixed-point type. `NUMERIC`, `DEC`, `FIXED`, and
`NUMBER` are aliases. `NUMBER` is a Machbase compatibility extension rather than
a MySQL alias. `DESC`, `SHOW`, and result metadata use the canonical name
`DECIMAL`.

## Declaration

```sql
DECIMAL
DECIMAL(precision)
DECIMAL(precision, scale)
NUMERIC
NUMERIC(precision)
NUMERIC(precision, scale)
```

| Declaration | Meaning |
|-------------|---------|
| `DECIMAL` | `DECIMAL(10,0)` |
| `DECIMAL(M)` | `DECIMAL(M,0)` |
| `DECIMAL(M,D)` | precision `M`, scale `D` |

- Precision ranges from 1 through 65.
- Scale ranges from 0 through 30 and cannot exceed precision.
- `UNSIGNED` and `ZEROFILL` are not supported.
- Excess fractional digits use round-half-away-from-zero.
- Precision overflow is rejected instead of truncated or converted to floating point.

## Table Support

| Table type | DECIMAL column | Typical use |
|------------|:--------------:|-------------|
| LOG | O | Financial events and exact aggregation |
| TAG | O | Exact measurement columns |
| VOLATILE | O | State/cache values and primary keys |
| LOOKUP | O | Reference values, primary keys, and indexes |
| RDB | O | Relational data and normal/UNIQUE/PRIMARY indexes |

LOG and TAG DECIMAL columns are supported in Cluster Edition. RDB tables remain
limited to Standard Edition independently of the column type.

## Comparison and Operations

All table engines use the same canonical comparison. `1`, `1.0`, and `1.00`
compare as the same value for equality, primary-key, and unique checks.

VIEW-derived columns preserve DECIMAL precision and scale. `DESC`, `SHOW`,
`M$SYS_COLUMNS`, and client result metadata expose both attributes.

DECIMAL supports `+`, `-`, `*`, `/`, `ROUND`, `TRUNC`, `CAST`, `SUM`, `AVG`,
`MIN`, `MAX`, `GROUP BY`, `ORDER BY`, and `DISTINCT`. Advanced statistical,
percentile, and `TOP_K` functions may convert DECIMAL input to DOUBLE and return
an approximate result.

## Client Mapping

| Interface | Recommended mapping |
|-----------|---------------------|
| ODBC | `SQL_DECIMAL` / `SQL_NUMERIC`, `SQL_C_NUMERIC` |
| JDBC | `java.math.BigDecimal` |
| Python | `decimal.Decimal` |
| Node.js | Decimal-compatible string or connector decimal representation |
| .NET | `decimal`, `DbType.Decimal` |

machloader formats, CSV import/export, and append paths preserve sign, NULL,
precision, and scale. Avoid converting DECIMAL values through FLOAT or DOUBLE.
