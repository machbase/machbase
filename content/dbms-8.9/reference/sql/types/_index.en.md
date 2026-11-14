---
type: docs
title: '16.1.2 Data Type Dictionary'
weight: 20
toc: true
---

SQL data types supported by Machbase.

Choose a type for the required value range and precision. Values reserved for NULL, such as an
integer type's minimum or maximum, cannot be ordinary data. The table's NULL Value column shows
internal representations; use SQL NULL to insert and IS NULL to test.

## Data Type Summary

| Type | Size | Value Range | NULL Value |
|------|------|---------|---------|
| `SHORT` | 2 bytes | -32,767 ~ 32,767 | -32,768 |
| `USHORT` | 2 bytes | 0 ~ 65,534 | 65,535 |
| `INTEGER` | 4 bytes | -2,147,483,647 ~ 2,147,483,647 | -2,147,483,648 |
| `UINTEGER` | 4 bytes | 0 ~ 4,294,967,294 | 4,294,967,295 |
| `LONG` | 8 bytes | -9,223,372,036,854,775,807 ~ 9,223,372,036,854,775,807 | -9,223,372,036,854,775,808 |
| `ULONG` | 8 bytes | 0 ~ 18,446,744,073,709,551,614 | 18,446,744,073,709,551,615 |
| `FLOAT` | 4 bytes | 32-bit single-precision floating-point | Maximum positive value |
| `DOUBLE` | 8 bytes | 64-bit double-precision floating-point | Maximum positive value |
| `DECIMAL(M,D)` | Varies with precision | Exact fixed-point, M: 1–65, D: 0–30 | - |
| `ARRAY` | Varies with element type and cardinality | Fixed-length one-dimensional numeric array, cardinality 1–1024 | Whole-array and element NULLs are distinct |
| `DATETIME` | 8 bytes | 1970-01-01 – 2262-04-11 (nanosecond precision) | - |
| `VARCHAR(n)` | Variable | Up to n bytes (LOG declaration range: 1–32,767) | - |
| `IPV4` | 4 bytes | 0.0.0.0 ~ 255.255.255.255 | - |
| `IPV6` | 16 bytes | 0000:...:0000 ~ FFFF:...:FFFF | - |
| `TEXT` | Variable | 0–64MB (full-text indexing supported) | - |
| `BINARY` | Variable | LOG: 0–64MB / TAG: 1–32,767 bytes (fixed length) | - |
| `JSON` | Variable | JSON document: 1–32,768 bytes / path: 1–512 bytes | - |

---

## Integer Types

### SHORT

Signed 16-bit integer. Storage size matches C int16_t, but the minimum value (-32,768) is
reserved for NULL. INT16 is also accepted in SQL.

```sql
CREATE LOG TABLE t (c1 SHORT);
INSERT INTO t VALUES (-32767);  -- Valid minimum
INSERT INTO t VALUES (-32768);  -- Treated as NULL
```

### USHORT

Unsigned 16-bit integer (uint16_t). The maximum value (65,535) represents NULL.

### INTEGER

Signed 32-bit integer. Storage size matches C int32_t, but the minimum is reserved for NULL.
INT32 and INT are SQL aliases.

### UINTEGER

Unsigned 32-bit integer (uint32_t).

### LONG

Signed 64-bit integer. Storage size matches C int64_t, but the minimum is reserved for NULL.
INT64 is a SQL alias.

### ULONG

Unsigned 64-bit integer (uint64_t).

---

## Floating-point Types

### FLOAT

Equivalent to C's 32-bit float. The maximum positive value represents NULL.

### DOUBLE

Equivalent to C's 64-bit double. The maximum positive value represents NULL.

---

## Fixed-point Types

### DECIMAL / NUMERIC

Exact decimal storage within declared precision and scale. Input with more fractional digits
than the declared scale may be rounded. Determine required precision before storing amounts
or rates. NUMERIC, DEC, FIXED, and NUMBER are aliases
for DECIMAL.

```sql
CREATE TRANSACTION TABLE invoice (
    id     LONG PRIMARY KEY,
    amount DECIMAL(18,2),
    rate   NUMERIC(7,4)
);
```

DECIMAL means DECIMAL(10,0); DECIMAL(M) means DECIMAL(M,0). For declarations, rounding, indexes,
aggregation, and client mappings, see [DECIMAL and NUMERIC Fixed-point Types](decimal-numeric-fixed-point/).


---

## ARRAY Types

Machbase DBMS 8.7.0 supports fixed-length, one-dimensional numeric ARRAYs.
Specify cardinality after the element type.

```sql
CREATE LOG TABLE sensor_array (
    id INTEGER,
    location DOUBLE[2],
    acceleration FLOAT[3]
);
```

For element types, NULL distinctions, ingestion/query syntax, and SDK representations, see
[Numeric ARRAY Types](array/).

---

## Date/Time Types

### DATETIME

Internally stores nanoseconds elapsed since midnight on January 1, 1970. Range: 1970-01-01 00:00:00
000:000:000 through 2262-04-11 23:47:16.854:775:807.

- Supports nanosecond precision
- Internal representation: 8-byte integer (nanoseconds since epoch)
- String representation: `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`

```sql
-- Convert string to DATETIME
SELECT TO_DATE('2024-01-15 10:30:00 000:000:000');

-- Convert DATETIME to string
SELECT TO_CHAR(ts, 'YYYY-MM-DD HH24:MI:SS') FROM t;
```

---

## String Types

### VARCHAR(n)

Variable-length string. n is the storage limit in bytes, not characters. The LOG declaration
range is 1–32,767. UTF-8 characters vary in byte length, so account for encoded size when storing
Korean text, emoji, and other multibyte characters.

```sql
CREATE LOG TABLE t (name VARCHAR(100), description VARCHAR(1000));
```

### TEXT

Stores large text beyond VARCHAR capacity, up to 64MB. Distinguish text storage support
from KEYWORD index support; index availability depends on
table type.

- Supported in LOG and Standard Edition TRANSACTION tables
- LOG supports keyword search with KEYWORD indexes and SEARCH
- Not supported in TAG, LOOKUP, or VOLATILE

ORDER BY and GROUP BY cannot operate directly on LOG TEXT columns.
This is a query validation constraint, not merely a performance recommendation.
Store device IDs, error codes, severity, and other sort/group keys in separate VARCHAR or numeric columns.
Using MODIFY COLUMN to change TEXT to VARCHAR is also unsupported.

```sql
CREATE LOG TABLE log_table (ts DATETIME, message TEXT);
-- Create a keyword index
CREATE INDEX idx_msg ON log_table (message) INDEX_TYPE KEYWORD;
```

---

## Binary Types

### BINARY

Stores unstructured binary data such as images and documents.

- **LOG**: Variable length, up to 64MB
- **TRANSACTION**: Variable-length binary values (Standard Edition)
- **TAG**: Fixed-length BINARY(n) variant, 1–32,767 bytes
- Not supported in LOOKUP or VOLATILE

TAG BINARY(n):
- Supports X'...', B'...', and O'...' literals, including lowercase prefixes
- Supports '0x...' for compatibility
- Exceeding the declared length causes ERR-02233

---

## Network Address Types

### IPV4

Stores IPv4 addresses in 4 bytes, ranging from 0.0.0.0 through 255.255.255.255.

```sql
CREATE LOG TABLE access_log (ts DATETIME, src_ip IPV4, dst_ip IPV4);
INSERT INTO access_log VALUES (NOW, '192.168.0.1', '10.0.0.1');
SELECT * FROM access_log WHERE src_ip = TO_IPV4('192.168.0.1');
```

### IPV6

Stores IPv6 addresses in 16 bytes. Abbreviated notation is supported.

- `"::FFFF:1232"` — Omitted leading zeros
- `"::FFFF:192.168.0.3"` — IPv4-compatible notation
- `"::192.168.3.1"` — IPv4-compatible notation (deprecated)

```sql
CREATE LOG TABLE v6_log (ts DATETIME, src_ip IPV6);
INSERT INTO v6_log VALUES (NOW, '21DA:D3:0:2F3B:2AA:FF:FE28:9C5A');
```

---

## JSON Type

Stores JSON documents as text containing key-value pairs.

- Maximum data size: 32,768 bytes
- Maximum JSON path length: 512 bytes
- Supported in TAG, LOG, LOOKUP, and TRANSACTION
- VOLATILE cannot create JSON columns
- LOOKUP JSON columns cannot be primary keys

```sql
CREATE LOG TABLE sensor_data (
    ts   DATETIME,
    data JSON
);
INSERT INTO sensor_data VALUES (NOW, '{"temp":23.5,"hum":60}');
SELECT data -> 'temp' AS temperature FROM sensor_data;
```

For details by table type, see [JSON Support by Table Type](table-types-type-support-scope-json/).

---

## SQL Data Type Mappings

Mappings between Machbase types, SQL standard types, and C types.

| Machbase Type | Machbase CLI Type | SQL Type | C Type | Native C Type |
|--------------|------------------|----------|--------|------------|
| `short` | SQL_SMALLINT | SQL_SMALLINT | SQL_C_SSHORT | `int16_t` |
| `ushort` | SQL_USMALLINT | SQL_SMALLINT | SQL_C_USHORT | `uint16_t` |
| `integer` | SQL_INTEGER | SQL_INTEGER | SQL_C_SLONG | `int32_t` |
| `uinteger` | SQL_UINTEGER | SQL_INTEGER | SQL_C_ULONG | `uint32_t` |
| `long` | SQL_BIGINT | SQL_BIGINT | SQL_C_SBIGINT | `int64_t` |
| `ulong` | SQL_UBIGINT | SQL_BIGINT | SQL_C_UBIGINT | `uint64_t` |
| `float` | SQL_FLOAT | SQL_REAL | SQL_C_FLOAT | `float` |
| `double` | SQL_DOUBLE | SQL_FLOAT, SQL_DOUBLE | SQL_C_DOUBLE | `double` |
| `decimal` | SQL_DECIMAL | SQL_DECIMAL, SQL_NUMERIC | SQL_C_NUMERIC | decimal-preserving value |
| `datetime` | SQL_TIMESTAMP | SQL_TYPE_TIMESTAMP | SQL_C_TYPE_TIMESTAMP | `char *` (YYYY-MM-DD ...) |
| `varchar` | SQL_VARCHAR | SQL_VARCHAR | SQL_C_CHAR | `char *` |
| `ipv4` | SQL_IPV4 | SQL_VARCHAR | SQL_C_CHAR | `char *` (IP string) |
| `ipv6` | SQL_IPV6 | SQL_VARCHAR | SQL_C_CHAR | `char *` (IP string) |
| `text` | SQL_TEXT | SQL_LONGVARCHAR | SQL_C_CHAR | `char *` |
| `binary` | SQL_BINARY | SQL_BINARY | SQL_C_BINARY | `char *` |
| `json` | SQL_JSON | SQL_JSON | SQL_C_CHAR | `json_t` |

---

## Supported Data Types by Table Type

| Type | TAG | LOG | LOOKUP | VOLATILE | TRANSACTION |
|------|:---:|:---:|:------:|:--------:|:---:|
| SHORT | O | O | O | O | O |
| USHORT | O | O | O | O | O |
| INTEGER | O | O | O | O | O |
| UINTEGER | O | O | O | O | O |
| LONG | O | O | O | O | O |
| ULONG | O | O | O | O | O |
| FLOAT | O | O | O | O | O |
| DOUBLE | O | O | O | O | O |
| DECIMAL / NUMERIC | O | O | O | O | O |
| DATETIME | O | O | O | O | O |
| VARCHAR | O | O | O | O | O |
| IPV4 | O | O | O | O | O |
| IPV6 | O | O | O | O | O |
| TEXT | X | O | X | X | O |
| JSON | O | O | O | X | O |
| BINARY | O (fixed length) | O | X | X | O |

DECIMAL is supported in all public table types. TRANSACTION tables are available in Standard Edition.
Cluster Edition supports DECIMAL columns in LOG/TAG tables and DDL propagation.
