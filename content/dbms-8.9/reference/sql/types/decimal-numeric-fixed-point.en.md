---
type: docs
title: 'DECIMAL and NUMERIC Fixed-point Types'
weight: 20
toc: true
---

DECIMAL stores decimal values exactly. NUMERIC, DEC, FIXED, and NUMBER are aliases;
DESC, SHOW, and result metadata display the canonical name DECIMAL.
NUMBER is a Machbase compatibility extension, not a MySQL alias.

## Declaration Syntax

```sql
DECIMAL
DECIMAL(precision)
DECIMAL(precision, scale)

NUMERIC
NUMERIC(precision)
NUMERIC(precision, scale)
```

| Declaration | Interpretation |
|------|------|
| `DECIMAL` | `DECIMAL(10,0)` |
| `DECIMAL(M)` | `DECIMAL(M,0)` |
| `DECIMAL(M,D)` | precision `M`, scale `D` |

- Precision is the total number of significant digits, from 1 through 65.
- Scale is the number of fractional digits, from 0 through 30.
- Scale cannot exceed precision.
- UNSIGNED and ZEROFILL are not supported.

```sql
CREATE TRANSACTION TABLE invoice (
    invoice_id LONG PRIMARY KEY,
    amount     DECIMAL(18,2),
    tax_rate   NUMERIC(7,4)
);
```

## Rounding and Overflow

Input with more fractional digits than scale is rounded half away
from zero.

```sql
CREATE TRANSACTION TABLE decimal_rounding (
    id     INTEGER PRIMARY KEY,
    amount DECIMAL(5,2)
);

INSERT INTO decimal_rounding VALUES (1, 1.235);   -- 1.24
INSERT INTO decimal_rounding VALUES (2, -1.235);  -- -1.24
```

Values exceeding precision cause errors rather than truncation or floating-point conversion.
DECIMAL NULL is managed separately from the value, without a numeric sentinel.

## Support by Table Type

| Table Type | DECIMAL Columns | Main Uses |
|------------|:------------:|----------------|
| LOG | O | Monetary/settlement events and exact aggregation |
| TAG | O | Exact measurements and aggregate data columns |
| VOLATILE | O | State/cache values and primary keys |
| LOOKUP | O | Reference amounts/rates, primary keys, and secondary indexes |
| TRANSACTION | O | Relational business data and PK/UNIQUE/ordinary indexes |

```sql
CREATE LOG TABLE payment_log (
    occurred_at DATETIME,
    amount      DECIMAL(18,2)
);

CREATE TAG TABLE meter_value (
    name   VARCHAR(80) PRIMARY KEY,
    time   DATETIME BASETIME,
    value  DECIMAL(24,6)
);

CREATE VOLATILE TABLE exchange_cache (
    rate_key DECIMAL(12,6) PRIMARY KEY,
    label    VARCHAR(32)
);

CREATE LOOKUP TABLE price_rule (
    rule_id LONG PRIMARY KEY,
    amount  DECIMAL(18,2)
);
```

Cluster Edition supports DECIMAL columns in LOG/TAG tables and DDL propagation. TRANSACTION
tables remain exclusive to Standard Edition regardless of DECIMAL support.

## Comparison and Indexes

All table engines use the same DECIMAL comparison rules. Numerically equal values compare equal
regardless of their represented scale.

```sql
-- 1, 1.0, and 1.00 are equal in equality, PK, and UNIQUE comparisons.
SELECT * FROM price_rule WHERE amount = 1.00;
```

DECIMAL is supported in VOLATILE/LOOKUP primary key memory indexes and TRANSACTION ordinary,
UNIQUE, and PRIMARY KEY indexes. TRANSACTION indexes use the same numeric ordering for
equality, ranges, and sorting.

Derived VIEW columns preserve DECIMAL precision and scale. Check them separately through DESC,
SHOW, M$SYS_COLUMNS, and client result metadata.

## Expressions and Aggregates

DECIMAL values support +, -, *, /, ROUND, TRUNC, [CAST](../../functions/functions-full/#cast), and the
following aggregate and ordering operations.

- `SUM`, `AVG`, `MIN`, `MAX`
- `GROUP BY`, `ORDER BY`, `DISTINCT`

Advanced statistics, percentile functions, TOP_K, and other operations without an exact DECIMAL
path convert to DOUBLE, so results may be approximate.

## Input/Output and Client Mappings

machloader .fmt files, CSV import/export, and Append preserve sign, NULL, precision, and scale.
Pass values as strings or language-native decimal types,
without converting through floating-point types.

| Interface | Recommended Mapping |
|-----------|-----------|
| ODBC | `SQL_DECIMAL` / `SQL_NUMERIC`, `SQL_C_NUMERIC` |
| JDBC | `java.math.BigDecimal` |
| Python | `decimal.Decimal` |
| Node.js | Decimal-compatible string or connector decimal representation |
| .NET | `decimal`, `DbType.Decimal` |

For Go NUMERIC values, also use the connector's decimal-preserving value or string representation
instead of converting to float64.

## Choosing a Type

- Use DECIMAL for exact decimal currency, tax rates, and settlement amounts.
- Use FLOAT or DOUBLE when approximation and a wide exponent range matter, such as sensor values.
- Converting DECIMAL to DOUBLE during storage, comparison, or calculation loses exact fixed-point semantics.
