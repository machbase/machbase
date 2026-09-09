---
type: docs
title: '8.2 Table Structure and Schema'
weight: 20
toc: true
---

Automatic numbering does not eliminate all duplicates: the same external device can still be
inserted twice with different numbers. Schema design starts by distinguishing row identifiers from
keys that prevent business duplicates.

<a id="rdb-table-design"></a>
<a id="rdb-table-design-design-schema-type-rdb"></a>

<a id="내부-식별자와-업무-키를-나눕니다"></a>

## Internal Identifiers and Business Keys

This example manages an internal number separately from an external device code.

```sql
CREATE TRANSACTION TABLE ch8_schema (
    id            LONG PRIMARY KEY AUTO_INCREMENT,
    external_code VARCHAR(64) NOT NULL,
    device_name   VARCHAR(128) NOT NULL,
    price         DECIMAL(18,2),
    state         JSON,
    updated_at    DATETIME
);
CREATE UNIQUE INDEX ch8_schema_code ON ch8_schema(external_code);

INSERT INTO ch8_schema(external_code, device_name, price, state, updated_at)
VALUES ('ERP-01', 'Pump A', 19900.25, '{"status":"NORMAL"}',
        TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));

SELECT external_code, device_name, price, state->'$.status' AS status
  FROM ch8_schema;
```

One ERP-01 row is returned with price 19900.25 and state NORMAL. The server assigns id. Do not make
consecutive or gap-free numbering a business requirement. For retrieving assigned IDs, check your
SDK and [AUTO_INCREMENT](/dbms/reference/sql/syntax/auto-increment-syntax/).

<a id="primary-key와-unique는-역할이-다릅니다"></a>

## PRIMARY KEY and UNIQUE

A TRANSACTION table permits one single-column PRIMARY KEY. Specify PRIMARY KEY after the column
definition, or add it to an existing table with CREATE PRIMARY KEY INDEX. It cannot be created on
data containing NULL or duplicate values.

Use a composite UNIQUE INDEX to enforce uniqueness across multiple columns. Do not copy UNIQUE,
FOREIGN KEY, or table-level PRIMARY KEY syntax inside CREATE TABLE from another DBMS. Define
uniqueness with CREATE UNIQUE INDEX after table creation.

UNIQUE INDEX keys containing NULL are not considered duplicates of other NULL-containing keys. If a
code must exist and be unique, also declare NOT NULL as in the example. Empty strings are another
potential pitfall. Check Machbase empty-string/NULL behavior through the actual input path and
validate required codes during collection.

The following optional exercise checks a UNIQUE violation. Run it separately from successful inserts.

```sql
-- Expected failure: duplicate external_code
INSERT INTO ch8_schema(external_code, device_name)
VALUES ('ERP-01', 'Duplicate Pump');
```

After failure, ERP-01 should still have one row. To update on duplicates, use the separate
[UPSERT](../insert-on-duplicate-key-update/) rules.

<a id="타입은-표현-범위와-연산-목적에-맞춥니다"></a>

## Choosing Data Types

| Value | Type choice | What to check |
|---|---|---|
| Identifiers and quantities | SHORT, INTEGER, LONG, and supported unsigned types | Range and reserved NULL values |
| Measurements and approximate values | FLOAT, DOUBLE | Floating-point rounding |
| Money and exact decimals | DECIMAL(M,D), NUMERIC, and other aliases | Precision, scale, and input conversion |
| Codes and names | VARCHAR(n) | Byte length, not character count |
| Long text and binary data | TEXT/CLOB, BINARY/BLOB | Storage support versus sorting, function, and index support |
| Event/change timestamps | DATETIME | Source time zone and conversion format |
| Network addresses | IPV4, IPV6 | Address format and comparison semantics |
| Additional attributes | JSON | Frequently searched paths and their types |
| Fixed-length numeric collections | Numeric ARRAY | Element type/length, whole-array NULL, and NULL elements |

Check complete ranges in the [Data Type Dictionary](/dbms/reference/sql/types/) and monetary values
in [DECIMAL](/dbms/reference/sql/types/decimal-numeric-fixed-point/). Do not use DOUBLE for every
monetary column simply because an example does.

<a id="필요한-제약만-명시하고-입력도-검증합니다"></a>

## Constraints and Input Validation

TRANSACTION requires at least one user column. LOG automatic arrival timestamps and TAG
METADATA/BASETIME/BASEDISTANCE are unavailable. Do not assume foreign keys automatically enforce
referential integrity; include required relationship validation in the application and data checks.

The example UNIQUE INDEX does not validate business rules for device names or prices. Define
required values, allowed states, and quantity ranges separately.

```sql
SELECT COUNT(*) AS device_count FROM ch8_schema;
DROP TABLE ch8_schema;
```

The count before cleanup is 1. Continue with [Create, Alter, and Drop](../create-alter-drop/) for
schema changes and [Index Design](../index-performance/) for query access paths.
