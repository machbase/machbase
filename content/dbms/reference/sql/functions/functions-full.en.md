---
type: docs
title: 'Complete Function Reference'
weight: 70
toc: true
tocSort: true
---

## Error Handling

| Error Type | Code | Condition |
|---|---|---|
| Argument type error | `ERR-02036`, `ERR-02037` | Nonnumeric input or arguments supplied to `PI` |
| Execution error | `ERR-02317` | Negative input to `SQRT`, division by zero in `MOD`, invalid base/value in `LOG`, overflow in `EXP`/`POWER`, and similar errors |

NULL input produces NULL output.

## ABS

Returns the absolute value of a numeric column as a floating-point number.

```sql
ABS(column_expr)
```

```sql
Mach> CREATE LOG TABLE abs_table (c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO abs_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO abs_table VALUES(2, 2.0, 'sqltest');
1 row(s) inserted.

Mach> INSERT INTO abs_table VALUES(3, 3.0, 'sqltest');
1 row(s) inserted.

Mach> SELECT ABS(c1), ABS(c2) FROM abs_table;
SELECT ABS(c1), ABS(c2) from abs_table;
ABS(c1)                     ABS(c2)
-----------------------------------------------------------
3                           3
2                           2
1                           1
[3] row(s) selected.
```


## ADD_TIME

Adds or subtracts years, months, days, hours, minutes, and seconds from DATETIME. Milliseconds,
microseconds, and nanoseconds are not supported. Diff format is
`"Year/Month/Day Hour:Minute:Second"`; each component can be positive or negative.

```sql
ADD_TIME(column,time_diff_format)
```

```sql
Mach> CREATE LOG TABLE add_time_table (id INTEGER, dt DATETIME);
Created successfully.

Mach> INSERT INTO  add_time_table VALUES(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(2, TO_DATE('2000-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(3, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(4, TO_DATE('2013-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(5, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(6, TO_DATE('2014-12-30 23:22:33 444:555:666'));
1 row(s) inserted.

Mach> SELECT ADD_TIME(dt, '1/0/0 0:0:0') FROM add_time_table;
ADD_TIME(dt, '1/0/0 0:0:0')
----------------------------------
2015-12-30 23:22:33 444:555:666
2015-12-30 11:22:33 444:555:666
2014-11-11 01:02:03 004:005:006
2013-11-11 01:02:03 004:005:006
2001-11-11 01:02:03 004:005:006
2000-11-11 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '0/0/0 1:1:1') FROM add_time_table;
ADD_TIME(dt, '0/0/0 1:1:1')
----------------------------------
2014-12-31 00:23:34 444:555:666
2014-12-30 12:23:34 444:555:666
2013-11-11 02:03:04 004:005:006
2012-11-11 02:03:04 004:005:006
2000-11-11 02:03:04 004:005:006
1999-11-11 02:03:04 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '1/1/1 0:0:0') FROM add_time_table;
ADD_TIME(dt, '1/1/1 0:0:0')
----------------------------------
2016-01-31 23:22:33 444:555:666
2016-01-31 11:22:33 444:555:666
2014-12-12 01:02:03 004:005:006
2013-12-12 01:02:03 004:005:006
2001-12-12 01:02:03 004:005:006
2000-12-12 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '-1/0/0 0:0:0') FROM add_time_table;
ADD_TIME(dt, '-1/0/0 0:0:0')
----------------------------------
2013-12-30 23:22:33 444:555:666
2013-12-30 11:22:33 444:555:666
2012-11-11 01:02:03 004:005:006
2011-11-11 01:02:03 004:005:006
1999-11-11 01:02:03 004:005:006
1998-11-11 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '0/0/0 -1:-1:-1') FROM add_time_table;
ADD_TIME(dt, '0/0/0 -1:-1:-1')
----------------------------------
2014-12-30 22:21:32 444:555:666
2014-12-30 10:21:32 444:555:666
2013-11-11 00:01:02 004:005:006
2012-11-11 00:01:02 004:005:006
2000-11-11 00:01:02 004:005:006
1999-11-11 00:01:02 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '-1/-1/-1 0:0:0') FROM add_time_table;
ADD_TIME(dt, '-1/-1/-1 0:0:0')
----------------------------------
2013-11-29 23:22:33 444:555:666
2013-11-29 11:22:33 444:555:666
2012-10-10 01:02:03 004:005:006
2011-10-10 01:02:03 004:005:006
1999-10-10 01:02:03 004:005:006
1998-10-10 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-1/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
[2] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-2/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
4           2013-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT ADD_TIME(TO_DATE('2000-12-01 00:00:00 000:000:001'), '-1/0/0 0:0:-1') FROM add_time_table;
ADD_TIME(TO_DATE('2000-12-01 00:00:00 000:000:001'), '-1/0/0 0:0:-1')
------------------------------------------
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
[6] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-2/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
4           2013-11-11 01:02:03 004:005:006
[3] row(s) selected.
```

## APPROX_PERCENTILE {#approx_percentile-family}

```
APPROX_PERCENTILE
APPROX_MEDIAN
APPROX_P05
APPROX_P10
APPROX_P90
APPROX_P95
```

These functions approximate percentiles using a bounded summary instead of sorting every raw value.
They are useful for very large datasets when a small error is acceptable.

```sql
APPROX_PERCENTILE(value, ratio)
APPROX_MEDIAN(value)
APPROX_P05(value)
APPROX_P10(value)
APPROX_P90(value)
APPROX_P95(value)
```

- `value` must be numeric.
- `ratio` must be a constant from `0.0` through `1.0`.
- The return type is `DOUBLE`.
- NULL values are ignored.

`APPROX_MEDIAN(value)` is the approximate median. `APPROX_P05`, `APPROX_P10`, `APPROX_P90`, and
`APPROX_P95` are shorthands for common percentiles.

```sql
SELECT APPROX_PERCENTILE(latency_ms, 0.95) AS ap95,
       APPROX_MEDIAN(latency_ms) AS amedian,
       APPROX_P05(latency_ms) AS ap05
FROM api_log;
```

## ARRAY_LENGTH

`ARRAY_LENGTH(array_value)` returns the declared cardinality of a non-NULL ARRAY.

```sql
SELECT ARRAY_LENGTH(ARRAY[10, NULL, 30]);
-- 3
```

It returns cardinality even if every element is NULL. A whole-array NULL returns NULL;
`ARRAY_LENGTH(NULL)` without type information is an error. For ARRAY syntax and constraints,
see [Numeric ARRAY Types](/dbms/reference/sql/types/array/).

## ARRAY_SPARSE

`ARRAY_SPARSE` specifies only populated positions in a fixed-length ARRAY. Positions start at 0;
omitted positions are element NULLs.

```sql
-- Infer type and cardinality from the target column.
INSERT INTO sensor_array (id, channels)
VALUES (1, ARRAY_SPARSE(0 => 10, 3 => 40));

-- Specify type and cardinality for an expression without a target.
SELECT ARRAY_SPARSE(INT32[4], 0 => 10, 3 => 40);

-- Bracket shorthand infers cardinality as the largest position + 1.
SELECT [1 => 12, 33 => 23];
```

With an ARRAY target, bracket shorthand uses the target's type and cardinality. A standalone
expression uses the same common numeric type rules as a dense ARRAY, and sets cardinality
to the largest position plus one. Targetless all-NULL sparse values, duplicate positions, and
out-of-range positions are errors. For ingestion methods and SDK sparse objects, see
[Sparse ARRAY and Selected-column Append APIs](/dbms/development-tools-integration/data-input-load-export/array-append/).



## AREA {#area}

`AREA(y, x)` is an aggregate function that calculates the exact area under a curve of numeric
`(x, y)` points.

```sql
AREA(y, x)
```

- Both arguments must be numeric.
- Rows with NULL in either argument are ignored.
- Fewer than two valid points produce NULL.
- The return type is `DOUBLE`.

```sql
SELECT AREA(power_kw, sample_sec)
FROM power_log;
```


## AVG

Aggregate function returning the average of a numeric column.

```sql
AVG(column_name)
```

```sql
Mach> CREATE LOG TABLE avg_table (id1 INTEGER, id2 INTEGER);
Created successfully.

Mach> INSERT INTO avg_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(null, 4);
1 row(s) inserted.

Mach> SELECT id1, AVG(id2) FROM avg_table GROUP BY id1;
id1         AVG(id2)
-------------------------------------------
2                2
NULL             4
1                2
```


## BITAND / BITOR

Converts two integers to signed 64-bit integers and returns their bitwise AND/OR. Inputs must be
integers; the output is also a signed 64-bit integer.

Negative integers can produce platform-dependent results. Using only uinteger and ushort types is
recommended.

```sql
BITAND (<expression1>, <expression2>)
BITOR (<expression1>, <expression2>)
```

```sql
Mach> CREATE LOG TABLE bit_table (i1 INTEGER, i2 UINTEGER, i3 FLOAT, i4 DOUBLE, i5 SHORT, i6 VARCHAR(10));
Created successfully.

Mach> INSERT INTO bit_table VALUES (-1, 1, 1, 1, 2, 'aaa');
1 row(s) inserted.

Mach> INSERT INTO bit_table VALUES (-2, 2, 2, 2, 3, 'bbb');
1 row(s) inserted.

Mach> SELECT BITAND(i1, i2) FROM bit_table;
BITAND(i1, i2)
-----------------------
2
1
[2] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i2, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
-1          1           1                           1                           2           aaa
[1] row(s) selected.

Mach> SELECT BITOR(i5, 1) FROM bit_table WHERE BITOR(i5, 1) = 3;
BITOR(i5, 1)
-----------------------
3
3
[2] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITOR(i2, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
-1          1           1                           1                           2           aaa
[1] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i3, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i4, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITAND(i5, 1) FROM bit_table WHERE BITAND(i5, 1) = 1;
BITAND(i5, 1)
-----------------------
1
[1] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITOR(i6, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITOR] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITOR(i1, i2) FROM bit_table;
BITOR(i1, i2)
-----------------------
-2
-1
[2] row(s) selected.

Mach> SELECT BITAND(i1, i3) FROM bit_table;
BITAND(i1, i3)
-----------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITOR(i1, i6) FROM bit_table;
BITOR(i1, i6)
-----------------------
[ERR-02037 : Function [BITOR] argument data type is mismatched.]
[0] row(s) selected.
```


## CAST

<span class="badge-since">Available since Machbase 8.7.0</span>

`CAST` explicitly converts a value, column, or expression to the specified data type. It is available
in SELECT, predicates, CASE, UNION ALL, VIEW definitions, and prepared statements.

### Syntax

```sql
CAST(expression AS data_type)
CAST(expression AS data_type(length))
CAST(expression AS DECIMAL(precision[, scale]))
CAST(array_expression AS numeric_type[cardinality])
CAST(array_expression AS DECIMAL(precision[, scale])[cardinality])
```

- `expression` is the value, column, or SQL expression to convert.
- `array_expression` is a numeric ARRAY or SQL NULL.
- `data_type` is a target type or alias listed below.
- Type names are case-insensitive.
- `length`, `precision`, and `scale` are allowed only for target types that support them.
- Input and target ARRAY cardinalities must match exactly.

### Supported Types and Aliases

| Category | Target Type | Accepted Names |
|------|-----------|---------------------|
| Signed integer | 16-bit | `INT16`, `SHORT` |
| | 32-bit | `INT32`, `INT`, `INTEGER` |
| | 64-bit | `INT64`, `LONG` |
| Unsigned integer | 16-bit | `UINT16`, `USHORT` |
| | 32-bit | `UINT32`, `UINTEGER` |
| | 64-bit | `UINT64`, `ULONG` |
| Floating-point | Single/double precision | `FLOAT`, `DOUBLE` |
| Fixed-point | DECIMAL | `DECIMAL`, `NUMERIC`, `DEC`, `FIXED`, `NUMBER` |
| Character | Fixed/variable length | `CHAR`, `VARCHAR` |
| Character LOB | Text | `TEXT`, `CLOB` |
| Date/time | Nanosecond precision | `DATETIME` |
| Network address | IP address | `IPV4`, `IPV6` |
| Binary | Binary/binary LOB | `BINARY`, `BLOB` |
| Document | JSON | `JSON` |

Names in the same row represent the same type. For example, INTEGER, INT, and INT32 all
represent signed 32-bit integers. Result column metadata may display the canonical
type name.

### Length and Precision

#### CHAR, VARCHAR, BINARY

| Type | Default Length | Allowed Length | Overflow Handling |
|------|-------------------:|-----------|----------------|
| `CHAR(n)` | 1 byte | 1–32,767 bytes | Retain the first n bytes |
| `VARCHAR(n)` | 32,767 bytes | 1–32,767 bytes | Retain the first n bytes |
| `BINARY(n)` | 1 byte | 1–67,108,864 bytes | Retain the first n bytes |

Length is measured in bytes, not characters. Specify enough space for UTF-8 strings because a
multibyte character can be truncated in the middle. CHAR does not pad unused space with blanks.
Result metadata for `CAST(... AS CHAR(n))` currently reports `VARCHAR(n)`.

```sql
SELECT '[' || CAST('abc' AS CHAR) || ']' AS char_default;
-- [a]

SELECT '[' || CAST('abc' AS CHAR(5)) || ']' AS char_value;
-- [abc] (no spaces added)

SELECT CAST('abcdef' AS VARCHAR(3)) AS varchar_value;
-- abc

SELECT CAST('414243' AS BINARY(2)) AS binary_value;
-- 4142
```

TEXT, CLOB, BLOB, and JSON do not accept a length. CAST results of these types currently
support up to 32,767 bytes. If exceeding the permitted limit would damage the result's meaning,
conversion returns an error rather than truncating it automatically.

#### DECIMAL

| Syntax | Interpretation |
|------|------|
| `DECIMAL` | `DECIMAL(10,0)` |
| `DECIMAL(p)` | `DECIMAL(p,0)` |
| `DECIMAL(p,s)` | precision `p`, scale `s` |

- Precision p ranges from 1 through 65.
- Scale s ranges from 0 through 30 and cannot exceed precision.
- Excess fractional digits are rounded half away from zero.
- Precision and scale are allowed only for DECIMAL-family types.

```sql
SELECT CAST('12.34' AS DECIMAL(5,2));
-- 12.34

SELECT CAST(123.456 AS NUMERIC(6,2));
-- 123.46
```

### NULL and Empty Strings

- NULL input returns NULL of the target type.
- Machbase treats the zero-length string literal `''` as SQL NULL.
- `''''` is a string containing one single quote, not an empty string.

```sql
SELECT CAST(NULL AS INTEGER) AS null_integer;
SELECT CAST('' AS VARCHAR(10)) AS empty_value;
SELECT CAST('''' AS VARCHAR(10)) AS quote_value;
```

### Numeric Conversion

Numeric types can be converted to one another, and numeric strings can be converted to numeric types.

```sql
SELECT CAST('123' AS INTEGER);
SELECT CAST('1.25' AS DOUBLE);
SELECT CAST(12.9 AS SHORT);       -- 12
SELECT CAST(-12.9 AS INTEGER);    -- -12
SELECT CAST('9223372036854775806e0' AS LONG);
```

- Floating-point-to-integer conversion truncates toward zero without rounding.
- Exponent notation in integer strings is parsed while preserving integer precision.
- Values outside the target type's range cause errors.
- Negative results are not allowed for unsigned integers. A value whose fractional truncation
  produces zero can be converted to zero.
- NaN and positive/negative infinity cannot be converted to integers.

CAST produces the integer ranges below. Values reserved for NULL in each type are excluded
from valid result ranges.

| Target Type | CAST Result Range |
|-----------|----------------|
| `INT16`, `SHORT` | -32,767~32,767 |
| `UINT16`, `USHORT` | 0~65,534 |
| `INT32`, `INT`, `INTEGER` | -2,147,483,647~2,147,483,647 |
| `UINT32`, `UINTEGER` | 0~4,294,967,294 |
| `INT64`, `LONG` | -9,223,372,036,854,775,807~9,223,372,036,854,775,807 |
| `UINT64`, `ULONG` | 0~18,446,744,073,709,551,614 |

### Converting an Entire Numeric ARRAY

Numeric ARRAYs with the same cardinality support conversion of all elements. Target types include
`INT16`, `UINT16`, `INT32`, `UINT32`, `INT64`, `UINT64`, `FLOAT`, `DOUBLE`, and `DECIMAL`, plus
the numeric aliases in the supported type table.

```sql
SELECT CAST([1.9, NULL, -3.9] AS INT32[3]);
SELECT CAST([1.235, NULL, -2.345] AS DECIMAL(6,2)[3]);
```

- A whole-array NULL remains a whole-array NULL after conversion.
- Each element NULL remains NULL at the same position.
- Each non-NULL element follows the corresponding scalar numeric CAST rules for truncation,
  rounding, and range checking.
- If any element cannot be converted, the CAST and its containing statement fail. No partially
  converted elements or rows remain as results.
- `DECIMAL[N]` means `DECIMAL(10,0)[N]`; `DECIMAL(p)[N]` means `DECIMAL(p,0)[N]`.


In a prepared statement, the CAST target also determines the parameter's element type, cardinality,
and DECIMAL precision/scale. The same statement can be rebound with dense ARRAYs, sparse ARRAYs,
and whole-array NULLs.

```sql
SELECT CAST(? AS INT32[3]);
SELECT CAST(? AS DECIMAL(12,4)[3]);
```

A scalar cannot be expanded to an ARRAY, and an ARRAY cannot be reduced to a scalar. Different
cardinalities are not padded or truncated. String, date, IP, BINARY, and JSON ARRAYs are not
supported as targets.

### String and LOB Conversion

Numbers, date/time values, IP addresses, binary values, and JSON can be converted to character types.

- Integers and DECIMAL return their decimal representation.
- FLOAT uses up to 9 significant digits; DOUBLE uses up to 17.
- DATETIME is formatted using the session date format and timezone.
- IPV4 and IPV6 use normalized address strings.
- BINARY and BLOB use uppercase hexadecimal without a prefix.
- JSON preserves its original JSON representation.

```sql
SELECT CAST(123456 AS VARCHAR(8));
-- 123456

SELECT CAST(CAST('2001:db8::1' AS IPV6) AS VARCHAR(64));

SELECT CAST(CAST('0x00ff10' AS BLOB) AS VARCHAR(8));
-- 00FF10
```

To convert a string to BINARY or BLOB, use an even-length hexadecimal string with no prefix,
or with a `0x`/`0X` prefix.

```sql
SELECT CAST('414243' AS BINARY(3));
SELECT CAST('0x00ff10' AS BLOB);
SELECT CAST(X'414243' AS VARCHAR(6));
```

BINARY(n) retains only the first n bytes. Nonhexadecimal characters and odd-length hexadecimal
strings cause errors.

### DATETIME Conversion

Strings and numbers can be converted to DATETIME.

- Strings are parsed using the session's default date format and timezone.
- Numbers are interpreted as nanoseconds since the Unix epoch.
- Numeric -1 is reserved for DATETIME NULL and cannot be converted.
- Converting DATETIME to a number returns nanoseconds since the Unix epoch.

```sql
SELECT CAST('2026-08-15 12:34:56' AS DATETIME);
SELECT CAST(1000000000 AS DATETIME);
SELECT CAST(CAST(1000000000 AS DATETIME) AS VARCHAR(40));
```

The same epoch value can display as different dates and times when session timezones
differ.

### IPV4 and IPV6 Conversion

Strings can be converted to IPV4 or IPV6. The entire address must be valid.

```sql
SELECT CAST('127.0.0.1' AS IPV4);
SELECT CAST('2001:db8::1' AS IPV6);
```

Invalid addresses and address formats incompatible with the target type cause errors.

### JSON Conversion

When converting a string to JSON, the entire input must be valid JSON. JSON strings, numbers,
true, false, and null are accepted, as well as objects and arrays.

```sql
SELECT CAST('{"ok":true}' AS JSON);
SELECT CAST('[1,2,3]' AS JSON);
SELECT CAST('"abc"' AS JSON);
SELECT CAST(CAST('"abc"' AS JSON) AS VARCHAR(16));
-- "abc"
```

Partially valid JSON or trailing non-JSON characters prevent conversion.

### Expressions and Result Metadata

CAST is an ordinary SQL expression and can be used in WHERE predicates, CASE, UNION ALL, and
VIEW definitions.

```sql
SELECT CASE
         WHEN reading >= 0 THEN CAST(reading AS VARCHAR(32))
         ELSE 'invalid'
       END AS reading_text
  FROM sensor_log;

CREATE VIEW sensor_cast_view AS
SELECT CAST(sensor_id AS VARCHAR(100)) AS sensor_id_text,
       CAST(value AS DECIMAL(12,3)) AS value_decimal
  FROM sensor_log;
```

CAST syntax is the same in prepared statements. Supply values through `?` or SDK named markers;
declare the target type and precision/scale in SQL.

```sql
SELECT CAST(? AS DECIMAL(12,2)) AS amount;
```

CAST result type, byte length, and DECIMAL precision/scale are reflected in result metadata and
VIEW column information. Result nullability follows input expression nullability.

To combine ARRAY results in CASE or UNION ALL, element type, cardinality, and DECIMAL
precision/scale must all match. If they differ, explicitly CAST each result to the same ARRAY
type before combining.

Each SDK exposes CAST results through existing result metadata APIs. No CAST-specific SDK API
is provided.

| SDK | CAST Result Metadata API |
|-----|------------------------|
| Machbase SQLCLI | `SQLDescribeCol()`, `SQLColAttribute()` |
| ODBC | `SQLDescribeCol()`, `SQLColAttribute()` |
| JDBC | `ResultSetMetaData` |
| Python | `cursor.description` |
| Node.js | `ColumnMeta` |
| .NET | `GetSchemaTable()` |
| Go (native) | native column metadata |
| Go (`database/sql`) | `ColumnTypeNullable()` and `ColumnType` APIs |

### Error Conditions

| Cause | Example |
|------|-----|
| Unsupported target type | `CAST('1' AS UNKNOWN_TYPE)` |
| Invalid length or precision/scale | `CAST('1' AS INTEGER(2))`, `CAST('1' AS DECIMAL(2,3))` |
| Numeric overflow or NULL reserved value | `CAST('65535' AS USHORT)` |
| Negative value converted to unsigned integer | `CAST('-1' AS UINTEGER)` |
| Nonnumeric string | `CAST('12x' AS INTEGER)` |
| Conversion between scalar and ARRAY | `CAST(1 AS INT32[1])`, `CAST([1] AS INT32)` |
| ARRAY cardinality mismatch | `CAST([1, 2] AS INT32[3])` |
| Unsupported ARRAY target type | `CAST([1] AS VARCHAR[1])` |
| Invalid IP address | `CAST('999.1.1.1' AS IPV4)` |
| Odd-length or nonhexadecimal binary string | `CAST('123' AS BINARY(4))`, `CAST('GG' AS BLOB)` |
| Invalid JSON | `CAST('{bad}' AS JSON)` |
| LOB or JSON result exceeding the allowed size | TEXT, CLOB, BLOB, or JSON results exceeding 32,767 bytes |

### Compatibility

CAST and whole numeric ARRAY CAST are supported in Machbase 8.7.0 in Standard and Cluster Editions.
In Cluster Edition, all cluster nodes must use the same version with CAST support.
Mixed execution with older nodes that do not support CAST is
not supported.

### Related Documentation

- [SQL Syntax Dictionary](../../syntax/)
- [Data Type Dictionary](../../types/)
- [Numeric ARRAY Types](../../types/array/)
- [DECIMAL and NUMERIC Fixed-point Types](../../types/decimal-numeric-fixed-point/)

## COUNT

Aggregate function that counts records in a column.

```sql
COUNT(column_name)
```

```sql
Mach> CREATE LOG TABLE count_table (id1 INTEGER, id2 INTEGER);
Created successfully.

Mach> INSERT INTO count_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(null, 4);
1 row(s) inserted.

Mach> SELECT COUNT(*) FROM count_table;
COUNT(*)
-----------------------
7
[1] row(s) selected.

Mach> SELECT COUNT(id1) FROM count_table;
COUNT(id1)
-----------------------
6
[1] row(s) selected.
```


## CUME_DIST {#cume_dist}

`CUME_DIST(value, threshold)` returns the cumulative fraction of rows whose value is at most threshold.

```sql
CUME_DIST(value, threshold)
```

- This is an aggregate function, not a window function.
- Both arguments must be numeric.
- threshold must be constant.
- The result is DOUBLE from 0.0 through 1.0.

```sql
SELECT CUME_DIST(latency_ms, 100)
FROM api_log;
```


<a id="current-session-user"></a>
<a id="current_user"></a>
<a id="session_user"></a>
<a id="current_user_id"></a>
<a id="session_user_id"></a>

## CURRENT_USER / SESSION_USER / CURRENT_USER_ID / SESSION_USER_ID

<span class="badge-since">Available since Machbase 8.7.0</span>

Returns the effective user for current SQL execution and the authenticated session user, by name or
internal ID.
Supported in both Standard and Cluster Editions.

| Function | Return Type | Description |
|---|---|---|
| `CURRENT_USER()` | `VARCHAR` | Effective username for current SQL execution |
| `SESSION_USER()` | `VARCHAR` | Authenticated username of the current session |
| `CURRENT_USER_ID()` | `INTEGER` | Effective user's internal ID |
| `SESSION_USER_ID()` | `INTEGER` | Authenticated session user's internal ID |

All four functions take no arguments and require parentheses. The parenthesis-free CURRENT_USER
keyword and USER, SYSTEM_USER, and CURRENT_SCHEMA aliases are not supported.

```sql
SELECT CURRENT_USER() AS current_name,
       SESSION_USER() AS session_name,
       CURRENT_USER_ID() AS current_id,
       SESSION_USER_ID() AS session_id;
```

In ordinary SQL, current user and session user are the same.

```text
CURRENT_NAME  SESSION_NAME  CURRENT_ID  SESSION_ID
SYS           SYS           1           1
```

### User Context in Views

When querying another user's definer VIEW, SQL inside the VIEW runs with the owner's privileges.

- CURRENT_USER() and CURRENT_USER_ID() return the VIEW owner.
- SESSION_USER() and SESSION_USER_ID() return the calling session user.

For a reproducible owner/caller example, see [VIEW Syntax](../../syntax/view-syntax/#view-user-context).


### Active Sessions After User Deletion

If another administrator session drops a connected user, existing connections do not terminate
immediately. The four functions continue to return the username and ID saved at login. The deleted
user cannot reconnect and no longer appears in M$SYS_USERS.

User IDs are internal Machbase metadata identifiers. Use them only to compare or join current
metadata, not as long-term business user keys.

```sql
SELECT COUNT(*)
  FROM M$SYS_USERS
 WHERE NAME = SESSION_USER()
   AND USER_ID = SESSION_USER_ID();
```

### Errors

Passing arguments returns ERR-02036. The other three functions follow the same rule.

```sql
SELECT CURRENT_USER(1);
-- ERR-02036: Function [CURRENT_USER] has an invalid argument.
```

For account lifecycle details, see [Account Management](../../../../security-access-control/account/).


## DATE_TRUNC

Truncates a DATETIME value to the specified time unit.

```sql
DATE_TRUNC (field, date_val [, count])
```

```sql
Mach> CREATE LOG TABLE trunc_table (i1 INTEGER, i2 DATETIME);
Created successfully.

Mach> INSERT INTO trunc_table VALUES (1, TO_DATE('1999-11-11 1:2:0 4:5:1'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (2, TO_DATE('1999-11-11 1:2:0 5:5:2'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (3, TO_DATE('1999-11-11 1:2:1 6:5:3'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (4, TO_DATE('1999-11-11 1:2:1 7:5:4'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (5, TO_DATE('1999-11-11 1:2:2 8:5:5'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (6, TO_DATE('1999-11-11 1:2:2 9:5:6'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (7, TO_DATE('1999-11-11 1:2:3 10:5:7'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (8, TO_DATE('1999-11-11 1:2:3 11:5:8'));
1 row(s) inserted.

Mach> SELECT COUNT(*), DATE_TRUNC('second', i2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('second', i2, 2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
4                    1999-11-11 01:02:00 000:000:000
4                    1999-11-11 01:02:02 000:000:000
[2] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('nanosecond', i2, 2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
1                    1999-11-11 01:02:00 004:005:000
1                    1999-11-11 01:02:00 005:005:002
1                    1999-11-11 01:02:01 006:005:002
1                    1999-11-11 01:02:01 007:005:004
1                    1999-11-11 01:02:02 008:005:004
1                    1999-11-11 01:02:02 009:005:006
1                    1999-11-11 01:02:03 010:005:006
1                    1999-11-11 01:02:03 011:005:008
[8] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('nsec', i2, 1000000000) tm FROM trunc_table group by tm ORDER BY 2; //Same as DATE_TRUNC('sec', i2, 1)
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.
```

Allowed ranges by time unit are as follows.

* Nanosecond, microsecond, and millisecond units and abbreviations are available from 5.5.6.
* Weeks start on Sunday.

| Time Unit | Range |
|--|--|
|nanosecond (nsec)|1000000000 (1 second)|
|microsecond (usec)|60000000 (60 seconds)|
|millisecond (msec)|60000 (60 seconds)|
|second (sec)|86400 (1 day)|
|minute (min)|1440 (1 day)|
|hour|24 (1 day)|
|day|1|
|week|1|
|month|1|
|year|1|

For example, DATE_TRUNC('second', time, 120) returns values at **2-minute** intervals, equivalent to
DATE_TRUNC('minute', time, 2).

## DATE_BIN
Bins DATETIME values by time unit and range relative to the specified origin.

```sql
DATE_BIN(field, count, source [, origin])
```

- With origin specified, buckets are calculated relative to that timestamp.
- Without origin, buckets are relative to 1970-01-01 00:00:00 in the server's local timezone.
- count must be an integer of at least 1.

To align buckets to local timezone boundaries like DATE_TRUNC() or ROLLUP(), use
the three-argument form without origin. To keep boundaries identical regardless of
server timezone, use the four-argument form with an explicit origin.

For example, with a UTC+09:00 server timezone, aligning to local boundaries previously
required a timezone-adjusted origin instead of DATE_BIN(..., 0).
`DATE_BIN(field, count, source)` now provides the same effect.

```sql
Mach> CREATE LOG TABLE log (time DATETIME);
Created successfully.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 00:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 01:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 02:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 03:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 04:00:00'));
1 row(s) inserted.

Mach> SELECT TIME, DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00')) FROM log ORDER BY time;
TIME                            DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00'))
---------------------------------------------------------------------------------------------
2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 01:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 02:00:00 000:000:000 2000-01-01 02:00:00 000:000:000
2000-01-01 03:00:00 000:000:000 2000-01-01 02:00:00 000:000:000
2000-01-01 04:00:00 000:000:000 2000-01-01 04:00:00 000:000:000
[5] row(s) selected.
```

Example of buckets aligned to local timezone boundaries:

```sql
Mach> CREATE LOG TABLE t3521 (ts DATETIME);
Created successfully.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 00:30:00'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 02:59:59'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 03:00:00'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 08:00:00'));
1 row(s) inserted.

Mach> SELECT ts,
             DATE_BIN('hour', 3, ts) AS date_bin_3arg,
             DATE_TRUNC('hour', ts, 3) AS date_trunc_3arg
        FROM t3521
    ORDER BY ts;
ts                              date_bin_3arg                   date_trunc_3arg
----------------------------------------------------------------------------------------------------
2000-01-01 00:30:00 000:000:000 2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 02:59:59 000:000:000 2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 03:00:00 000:000:000 2000-01-01 03:00:00 000:000:000 2000-01-01 03:00:00 000:000:000
2000-01-01 08:00:00 000:000:000 2000-01-01 06:00:00 000:000:000 2000-01-01 06:00:00 000:000:000
[4] row(s) selected.
```

Allowed ranges by time unit are listed below.

* Nanosecond, microsecond, and millisecond units and abbreviations are available from 5.5.6.
* A week equals 7 days.

| Time Unit |
|----:|
|nanosecond (nsec)|
|microsecond (usec)|
|millisecond (msec)|
|second (sec)|
|minute (min)|
|hour|
|day|
|week|
|month|
|year|


## DAYOFWEEK

Returns the weekday of a DATETIME value as an integer.

Semantically equivalent to [TO_CHAR(time, 'DAY')](#to_char), but returns an integer.

```sql
DAYOFWEEK(date_val)
```

Return values represent weekdays as follows.

| Return Value | Weekday |
|--|--|
| 0 | Sunday |
| 1 | Monday |
| 2 | Tuesday |
| 3 | Wednesday |
| 4 | Thursday |
| 5 | Friday |
| 6 | Saturday |


## DECODE

Compares a column value with search values and returns the corresponding return value for a match.
If none matches, returns default, or NULL if default is omitted.

```sql
DECODE(column, [search, return],.. default)
```

```sql
Mach> CREATE LOG TABLE decode_table (id1 VARCHAR(11));
Created successfully.

Mach> INSERT INTO decode_table VALUES('decodetest1');
1 row(s) inserted.

Mach> INSERT INTO decode_table VALUES('decodetest2');
1 row(s) inserted.

Mach> SELECT id1, DECODE(id1, 'decodetest1', 'result1', 'decodetest2', 'result2', 'DEFAULT') FROM decode_table;
id1          DECODE(id1, 'decodetest1', 'result1', 'decodetest2', 'result2', 'DEFAULT')
---------------------------------------------------------
decodetest2  result2
decodetest1  result1
[2] row(s) selected.

Mach> SELECT id1, DECODE(id1, 'codetest', 2, 99) FROM decode_table;
id1          DECODE(id1, 'codetest', 2, 99)
-----------------------------------------------
decodetest2  99
decodetest1  99
[2] row(s) selected.

Mach> SELECT DECODE(id1, 'decodetest1', 2) FROM decode_table;
DECODE(id1, 'decodetest1', 2)
--------------------------------
NULL
2
[2] row(s) selected.

Mach> SELECT DECODE(id1, 'codetest', 2) FROM decode_table;
DECODE(id1, 'codetest', 2)
-----------------------------
NULL
NULL
[2] row(s) selected.
```


## EXTRACT_*

Functions for extracting bits from binary frames.
EXTRACT_* uses big-endian order; EXTRACT_LE_* uses little-endian order.
All functions accept BINARY/VARBINARY and return NULL for a NULL frame.

**Endianness**

- EXTRACT_*: MSB first (bit 0 is the MSB of byte[0])
- EXTRACT_LE_*: LSB first (bit 0 is the LSB of byte[0])
- Bit indexes are 0-based across the entire frame.

**Common Rules**

- Single bit: `0 <= bit_pos < frame_bits`
- Range extraction: `start_bit >= 0`, `1 <= bit_count <= 64`,
  `start_bit + bit_count <= frame_bits`
- EXTRACT_FLOAT* reads 32 bits; EXTRACT_DOUBLE* reads 64 bits.
- Signed extraction interprets two's complement and sign-extends to 64 bits.
- Range error: ERR_QP_INVALID_ARG_VALUE (ERR-02229 family)
- Argument type error: ERR_QP_FUNCTION_ARG_TYPE

### EXTRACT_BIT

```
EXTRACT_BIT(frame, bit_pos) / EXTRACT_LE_BIT(frame, bit_pos) → TINYINT
```

Returns one bit as 0 or 1.

```sql
-- frame = 0x80 (1000 0000)
SELECT EXTRACT_BIT(frame, 0)    AS be_bit0,
       EXTRACT_LE_BIT(frame, 0) AS le_bit0
FROM t;
```

### EXTRACT_LONG, EXTRACT_ULONG

```
EXTRACT_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LE_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LONG(frame, start_bit, bit_count) → BIGINT
EXTRACT_LE_LONG(frame, start_bit, bit_count) → BIGINT
```

Reads 1–64 bits as an unsigned or two's-complement integer.

```sql
-- frame = 0x12 34
SELECT EXTRACT_ULONG(frame, 0, 16)    AS be_u16,  -- 0x1234
       EXTRACT_LE_ULONG(frame, 0, 16) AS le_u16   -- 0x3412
FROM t;
```

### EXTRACT_FLOAT,EXTRACT_DOUBLE

```
EXTRACT_FLOAT(frame, start_bit) → FLOAT
EXTRACT_LE_FLOAT(frame, start_bit) → FLOAT
EXTRACT_DOUBLE(frame, start_bit) → DOUBLE
EXTRACT_LE_DOUBLE(frame, start_bit) → DOUBLE
```

Reinterprets 32/64 bits as IEEE 754 float/double. The specified bit range must fit
within the frame.

```sql
SELECT EXTRACT_FLOAT(frame, 0)      AS be_f32,
       EXTRACT_LE_FLOAT(frame, 0)   AS le_f32,
       EXTRACT_DOUBLE(frame, 64)    AS be_f64,
       EXTRACT_LE_DOUBLE(frame, 64) AS le_f64
FROM sensor_bin;
```

### EXTRACT_SCALED_DOUBLE

```
EXTRACT_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
EXTRACT_LE_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
```

Reads 1–64 bits as unsigned when signed=0 or two's-complement signed when signed=1,
then returns `raw * scale + offset`.

```sql
-- 20-bit sensor value, scale 0.01, offset -40.0
SELECT EXTRACT_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0)    AS be_value,
       EXTRACT_LE_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0) AS le_value
FROM t_bin;
```


## FIRST / LAST

Aggregate functions returning a specified value from the first or last record in each group ordered
by a reference value.

* FIRST: Returns the value from the first record in sort order.
* LAST: Returns the value from the last record in sort order.

```sql
FIRST(sort_expr, return_expr)
LAST(sort_expr, return_expr)
```

```sql
Mach> create table firstlast_table (id integer, name varchar(20), group_no integer);
Created successfully.
Mach> insert into firstlast_table values (1, 'John', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (2, 'Grey', 1);
1 row(s) inserted.
Mach> insert into firstlast_table values (5, 'Ryan', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (4, 'Andrew', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (7, 'Kyle', 1);
1 row(s) inserted.
Mach> insert into firstlast_table values (6, 'Ross', 1);
1 row(s) inserted.

Mach> select group_no, first(id, name) from firstlast_table group by group_no;
group_no    first(id, name)
-------------------------------------
1           Grey
0           John
[2] row(s) selected.


Mach> select group_no, last(id, name) from firstlast_table group by group_no;
group_no    last(id, name)
-------------------------------------
1           Kyle
0           Ryan
```


## FROM_TIMESTAMP

Converts nanoseconds elapsed since 1970-01-01 00:00:00 UTC to datetime.

(TO_TIMESTAMP() converts datetime to nanoseconds elapsed since the same epoch.)

The epoch appears as 1970-01-01 09:00:00 in UTC+09:00.
Dates and times below use UTC+09:00.

```sql
FROM_TIMESTAMP(nanosecond_time_value)
```

```sql
Mach> SELECT FROM_TIMESTAMP(1562302560007248869);
FROM_TIMESTAMP(1562302560007248869)
--------------------------------------
2019-07-05 13:56:00 007:248:869
```

SYSDATE and NOW are DATETIME values representing the current time.
The example below converts the current time directly and after subtracting 1 millisecond (1,000,000
nanoseconds).

```sql
Mach> select sysdate, from_timestamp(sysdate) from test_tbl;
sysdate                         from_timestamp(sysdate)
-------------------------------------------------------------------
2019-07-05 14:00:59 722:822:443 2019-07-05 14:00:59 722:822:443
[1] row(s) selected.

Mach> select sysdate, from_timestamp(sysdate-1000000) from test_tbl;
sysdate                         from_timestamp(sysdate-1000000)
-------------------------------------------------------------------
2019-07-05 14:01:05 130:939:525 2019-07-05 14:01:05 129:939:525      -- Difference: 1 ms (1,000,000 ns)
[1] row(s) selected.
```


## FROM_UNIXTIME

Converts a 32-bit UNIXTIME integer to datetime. (UNIX_TIMESTAMP converts datetime to a 32-bit
UNIXTIME integer.)

Dates and times below use UTC+09:00.

```sql
FROM_UNIXTIME(unix_timestamp_value)
```

```sql
Mach> SELECT FROM_UNIXTIME(315540671) FROM TEST;
FROM_UNIXTIME(315540671)
----------------------------------
1980-01-01 11:11:11 000:000:000

Mach> SELECT FROM_UNIXTIME(UNIX_TIMESTAMP('2001-01-01')) FROM unix_table;
FROM_UNIXTIME(UNIX_TIMESTAMP('2001-01-01'))
------------------------------------------
2001-01-01 00:00:00 000:000:000
```


## GROUP_CONCAT

Aggregate function that concatenates column values within a group into a string.

{{< callout type="warning" >}}
Unavailable in Cluster Edition.
{{< /callout >}}

```sql
GROUP_CONCAT(
     [DISTINCT] column
     [ORDER BY { unsigned_integer | column }
     [ASC | DESC] [, column ...]]
     [SEPARATOR str_val]
)
```

* DISTINCT: Concatenate each distinct value once.
* ORDER BY: Order concatenated values by the specified columns.
* SEPARATOR: Delimiter between column values. Default: comma (,).

Syntax notes:

* Only one column can be specified. To combine columns, use TO_CHAR() and concatenation (||) to form one expression.
* ORDER BY can reference columns other than the concatenated column and can contain multiple columns.
* SEPARATOR must be a string constant, not a string column.

```sql
Mach> CREATE LOG TABLE concat_table(id1 INTEGER, id2 DOUBLE, name VARCHAR(10));
Created successfully.

Mach> INSERT INTO concat_table VALUES (1, 2, 'John');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (2, 1, 'Ram');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (3, 2, 'Zara');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (4, 2, 'Jill');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (5, 1, 'Jack');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (6, 1, 'Jack');
1 row(s) inserted.


Mach> SELECT GROUP_CONCAT(name) AS G_NAMES FROM concat_table GROUP BY id2;
G_NAMES
------------------------------------------------------------------------------------
Jack,Jack,Ram
Jill,Zara,John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(DISTINCT name) AS G_NAMES FROM concat_table GROUP BY Id2;
G_NAMES
------------------------------------------------------------------------------------
Jack,Ram
Jill,Zara,John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(name SEPARATOR '.') G_NAMES FROM concat_table GROUP BY Id2;
G_NAMES
------------------------------------------------------------------------------------
Jack.Jack.Ram
Jill.Zara.John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(name ORDER BY id1) G_NAMES, GROUP_CONCAT(id1 ORDER BY id1) G_SORTID FROM concat_table GROUP BY id2;
G_NAMES
------------------------------------------------------------------------------------
G_SORTID
------------------------------------------------------------------------------------
Ram,Jack,Jack
2,5,6
John,Zara,Jill
1,3,4
[2] row(s) selected.
```


## INSTR

Returns the 1-based starting position of a pattern string in the target string.

* Returns 0 if the pattern is absent.
* Returns NULL if the pattern has zero length or is NULL.

```sql
INSTR(target_string, pattern_string)
```

```sql
Mach> CREATE LOG TABLE string_table(c1 VARCHAR(20));
Created successfully.

Mach> INSERT INTO string_table VALUES ('abstract');
1 row(s) inserted.

Mach> INSERT INTO string_table VALUES ('override');
1 row(s) inserted.

Mach> SELECT c1, INSTR(c1, 'act') FROM string_table;
c1                    INSTR(c1, 'act')
------------------------------------------
override              0
abstract              6
[2] row(s) selected.
```


## LEAST / GREATEST

Given multiple columns or values, LEAST returns the minimum and GREATEST the maximum.

Zero or one input causes an error. A NULL input returns NULL; when inputs are columns, transform
NULLs with a function first.
Noncomparable columns such as BLOB or TEXT, or values that cannot be converted for comparison, cause errors.

```sql
LEAST(value_list, value_list,...)
GREATEST(value_list, value_list,...)
```

```sql
Mach> CREATE LOG TABLE lgtest_table(c1 INTEGER, c2 LONG, c3 VARCHAR(10), c4 VARCHAR(5));
Created successfully.

Mach> INSERT INTO lgtest_table VALUES (1, 2, 'abstract', 'ace');
1 row(s) inserted.

Mach> INSERT INTO lgtest_table VALUES (null, 100, null, 'bag');
1 row(s) inserted.

Mach> SELECT LEAST (c1, c2) FROM lgtest_table;
LEAST (c1, c2)
-----------------------
NULL
1
[2] row(s) selected.

Mach> SELECT LEAST (c1, c2, -1) FROM lgtest_table;
LEAST (c1, c2, -1)
-----------------------
NULL
-1
[2] row(s) selected.

Mach> SELECT GREATEST(c3, c4) FROM lgtest_table;
GREATEST(c3, c4)
--------------------
NULL
ace
[2] row(s) selected.

Mach> SELECT LEAST(c3, c4) FROM lgtest_table;
LEAST(c3, c4)
-----------------
NULL
abstract
[2] row(s) selected.

Mach> SELECT LEAST(NVL(c3, 'aa'), c4) FROM lgtest_table;
LEAST(NVL(c3, 'aa'), c4)
----------------------------
aa
abstract
[2] row(s) selected.
```


## LENGTH

Returns the length of a string column in bytes, based on English (ASCII) characters.

```sql
LENGTH(column_name)
```

```sql
Mach> CREATE LOG TABLE length_table (id1 INTEGER, id2 DOUBLE, name VARCHAR(15));
Created successfully.

Mach> INSERT INTO length_table VALUES(1, 10, 'Around the Horn');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(NULL, 20, 'Alfreds Futterkiste');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(3, NULL, 'Antonio Moreno');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(4, 40, NULL);
1 row(s) inserted.

Mach> select * FROM length_table;
ID1         ID2                         NAME
-------------------------------------------------------------
4           40                          NULL
3           NULL                        Antonio Moreno
NULL        20                          Alfreds Futterk
1           10                          Around the Horn
[4] row(s) selected.

Mach> select id1 * 10 FROM length_table;
id1 * 10
-----------------------
40
30
NULL
10
[4] row(s) selected.

Mach> select * FROM length_table Where id1 > 1 and id2 < 50;
ID1         ID2                         NAME
-------------------------------------------------------------
4           40                          NULL
[1] row(s) selected.

Mach> select name || ' with null concat' FROM length_table;
name || ' with null concat'
------------------------------------
NULL
Antonio Moreno with null concat
Alfreds Futterk with null concat
Around the Horn with null concat
[4] row(s) selected.

Mach> select LENGTH(name) FROM length_table;
LENGTH(name)
---------------
NULL
14
15
15
[4] row(s) selected.
```


## LOWER

Converts English letters to lowercase.

```sql
LOWER(column_name)
```

```sql
Mach> CREATE LOG TABLE lower_table (name VARCHAR(20));
Created successfully.

Mach> INSERT INTO lower_table VALUES('');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('James Backley');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('Alfreds Futterkiste');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('Antonio MORENO');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES (NULL);
1 row(s) inserted.

Mach> SELECT LOWER(name) FROM lower_table;
LOWER(name)
------------------------
NULL
antonio moreno
alfreds futterkiste
james backley
NULL
[5] row(s) selected.
```


## LPAD / RPAD

Pads the left (LPAD) or right (RPAD) of an input string to the specified length.

The final char parameter is optional; the default padding character is a space (' ').
If the input is longer than the specified length, returns only that many characters from the
beginning without padding.

```sql
LPAD(str, len, padstr)
RPAD(str, len, padstr)
```

```sql
Mach> CREATE LOG TABLE pad_table (c1 integer, c2 varchar(15));
Created successfully.

Mach> INSERT INTO pad_table VALUES (1, 'Antonio');
1 row(s) inserted.

Mach> INSERT INTO pad_table VALUES (25, 'Johnathan');
1 row(s) inserted.

Mach> INSERT INTO pad_table VALUES (30, 'M');
1 row(s) inserted.

Mach> SELECT LPAD(to_char(c1), 5, '0') FROM pad_table;
LPAD(to_char(c1), 5, '0')
-----------------------------
00030
00025
00001
[3] row(s) selected.

Mach> SELECT RPAD(to_char(c1), 5, '0') FROM pad_table;
RPAD(to_char(c1), 5, '0')
-----------------------------
30000
25000
10000
[3] row(s) selected.

Mach> SELECT LPAD(c2, 5) FROM pad_table;
LPAD(c2, 5)
---------------
    M
Johna
Anton
[3] row(s) selected.

Mach> SELECT RPAD(c2, 5) FROM pad_table;
RPAD(c2, 5)
---------------
M
Johna
Anton
[3] row(s) selected.

Mach> SELECT RPAD(c2, 10, '***') FROM pad_table;
RPAD(c2, 10, '***')
-----------------------
M*********
Johnathan*
Antonio***
[3] row(s) selected.
```


## LTRIM / RTRIM

Removes characters present in the pattern string from the first argument. LTRIM scans from the left
and RTRIM from the right, stopping at the first character absent from the pattern. Returns NULL if
every character is removed.

If pattern is omitted, trims spaces (' ').

```sql
LTRIM(column_name, pattern)
RTRIM(column_name, pattern)
```

```sql
Mach> CREATE LOG TABLE trim_table1(name VARCHAR(10));
Created successfully.

Mach> INSERT INTO trim_table1 VALUES ('   smith   ');
1 row(s) inserted.

Mach> SELECT ltrim(name) FROM trim_table1;
ltrim(name)
---------------
smith
[1] row(s) selected.

Mach> SELECT rtrim(name) FROM trim_table1;
rtrim(name)
---------------
   smith
[1] row(s) selected.

Mach> SELECT ltrim(name, ' s') FROM trim_table1;
ltrim(name, ' s')
---------------------
mith
[1] row(s) selected.

Mach> SELECT rtrim(name, 'h ') FROM trim_table1;
rtrim(name, 'h ')
---------------------
   smit
[1] row(s) selected.

Mach> CREATE LOG TABLE trim_table2 (name VARCHAR(10));
Created successfully.

Mach> INSERT INTO trim_table2 VALUES ('ddckaaadkk');
1 row(s) inserted.

Mach> SELECT ltrim(name, 'dc') FROM trim_table2;
ltrim(name, 'dc')
---------------------
kaaadkk
[1] row(s) selected.

Mach> SELECT rtrim(name, 'dk') FROM trim_table2;
rtrim(name, 'dk')
---------------------
ddckaaa
[1] row(s) selected.

Mach> SELECT ltrim(name, 'dckak') FROM trim_table2;
ltrim(name, 'dckak')
------------------------
NULL
[1] row(s) selected.

Mach> SELECT rtrim(name, 'dckak') FROM trim_table2;
rtrim(name, 'dckak')
------------------------
NULL
[1] row(s) selected.
```


## MAX

Aggregate function returning the maximum of the specified numeric column.

```sql
MAX(column_name)
```

```sql
Mach> CREATE LOG TABLE max_table (c INTEGER);
Created successfully.

Mach> INSERT INTO max_table VALUES(10);
1 row(s) inserted.

Mach> INSERT INTO max_table VALUES(20);
1 row(s) inserted.

Mach> INSERT INTO max_table VALUES(30);
1 row(s) inserted.

Mach> SELECT MAX(c) FROM max_table;
MAX(c)
--------------
30
[1] row(s) selected.
```


## MEDIAN {#median}

MEDIAN(value) returns the exact median of a numeric expression, using the same behavior as
PERCENTILE_CONT(value, 0.5).

```sql
MEDIAN(value)
```

- value must be numeric.
- NULL values are ignored.
- The return type is DOUBLE.

```sql
SELECT MEDIAN(temp_c)
FROM sensor_log;
```


## MIN

Aggregate function returning the minimum of the specified numeric column.

```sql
MIN(column_name)
```

```sql
Mach> CREATE LOG TABLE min_table(c1 INTEGER);
Created successfully.

Mach> INSERT INTO min_table VALUES(1);
1 row(s) inserted.

Mach> INSERT INTO min_table VALUES(22);
1 row(s) inserted.

Mach> INSERT INTO min_table VALUES(33);
1 row(s) inserted.

Mach> SELECT MIN(c1) FROM min_table;
MIN(c1)
--------------
1
[1] row(s) selected.
```


## NVL

Replaces a NULL column value with the specified value; otherwise returns the original value.

```sql
NVL(string1, replace_with)
```

```sql
Mach> CREATE LOG TABLE nvl_table (c1 varchar(10));
Created successfully.

Mach> INSERT INTO nvl_table VALUES ('Johnathan');
1 row(s) inserted.

Mach> INSERT INTO nvl_table VALUES (NULL);
1 row(s) inserted.

Mach> SELECT NVL(c1, 'Thomas') FROM nvl_table;
NVL(c1, 'Thomas')
---------------------
Thomas
Johnathan
```

## NEXTVAL

NEXTVAL(sequence_column) returns the next value of a Lookup table sequence column.

```sql
NEXTVAL(sequence_column)
```

- NEXTVAL is available only in INSERT.
- The argument must be a column configured with PROPERTY(SEQUENCE=...).
- For sequence column creation and examples, see [Sequence Column](/dbms/lookup-table-usage/sequence-column/).

```sql
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-a');
```


## ROUND

Returns the input rounded at the specified decimal position (using the next digit). If omitted,
rounds to zero decimal places. A negative position rounds within the integer part.

```sql
ROUND(column_name, [decimals])
```

```sql
Mach> CREATE LOG TABLE round_table (c1 DOUBLE);
Created successfully.

Mach> INSERT INTO round_table VALUES (1.994);
1 row(s) inserted.

Mach> INSERT INTO round_table VALUES (1.995);
1 row(s) inserted.

Mach> SELECT c1, ROUND(c1, 2) FROM round_table;
c1                          ROUND(c1, 2)
-----------------------------------------------------------
1.995                       2
1.994                       1.99
```


## ROWNUM

Numbers SELECT result rows.

Can be used inside SELECT subqueries and inline views. Assign an alias to ROWNUM() in an inline
view's select list to reference it externally.

```sql
ROWNUM()
```

**Allowed Clauses**

Allowed in SELECT lists, GROUP BY, and ORDER BY; not allowed in WHERE or HAVING. To filter by row
number, calculate ROWNUM() in an inline view and reference it in the outer query.

| Allowed Clauses | Disallowed Clauses |
|--|--|
|Target List / GROUP BY / ORDER BY|WHERE / HAVING|

```sql
Mach> CREATE LOG TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO rownum_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(2, 2.0, 'Second Row');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(3, 3.3, 'Third Row');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(4, 4.3, 'Fourth Row');
1 row(s) inserted.

Mach> SELECT INNER_RANK, c3 AS NAME
    2 FROM   (SELECT ROWNUM() AS INNER_RANK, * FROM rownum_table)
    3 WHERE  INNER_RANK < 3;
INNER_RANK           NAME
------------------------------------
1                    Fourth Row
2                    Third Row
[2] row(s) selected.
```

**Effect of Sorting on Row Numbers**

With ORDER BY, ROWNUM() values in the select list may appear out of sequence because ROWNUM() is
evaluated before sorting. For sequential numbering, place the ordered query in an inline view and
call ROWNUM() in the outer SELECT.

```sql
Mach> CREATE LOG TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO rownum_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(2, 2.0, 'John');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(3, 3.3, 'Sarah');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(4, 4.3, 'Micheal');
1 row(s) inserted.

Mach> SELECT ROWNUM(), c2 AS SORT, c3 AS NAME
    2 FROM   ( SELECT * FROM rownum_table ORDER BY c3 );
ROWNUM()             SORT                        NAME
-----------------------------------------------------------------
1                    1                           NULL
2                    2                           John
3                    4.3                         Micheal
4                    3.3                         Sarah
[4] row(s) selected.
```


## SERIESNUM

Returns the number of the contiguous SERIES BY interval containing each row. Rows in the same
interval share a number; this is not the row's position within the interval. Return type: BIGINT.
Without SERIES BY, always returns 1.

```sql
SERIESNUM()
```

```sql
Mach> CREATE LOG TABLE T1 (C1 INTEGER, C2 INTEGER);
Created successfully.

Mach> INSERT INTO T1 VALUES (0, 1);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (2, 3);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (3, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (4, 1);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (5, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (6, 3);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (7, 1);
1 row(s) inserted.


Mach> SELECT SERIESNUM(), C1, C2 FROM T1 ORDER BY C1 SERIES BY C2 > 1;
SERIESNUM() C1 C2
-------------------------------------------------
1 1 2
1 2 3
1 3 2
2 5 2
2 6 3
[5] row(s) selected.
```


## STDDEV / STDDEV_POP

Aggregate functions returning sample standard deviation (STDDEV) and population standard deviation
(STDDEV_POP), respectively the square roots of VARIANCE and VAR_POP.

```sql
STDDEV(column)
STDDEV_POP(column)
```

```sql
Mach> CREATE LOG TABLE stddev_table(c1 INTEGER, C2 DOUBLE);

Mach> INSERT INTO stddev_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (2, 1);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (3, 2);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (4, 2);
1 row(s) inserted.

Mach> SELECT c2, STDDEV(c1) FROM stddev_table GROUP BY c2;
c2                          STDDEV(c1)
-----------------------------------------------------------
1                           0.707107
2                           0.707107
[2] row(s) selected.

Mach> SELECT c2, STDDEV_POP(c1) FROM stddev_table GROUP BY c2;
c2                          STDDEV_POP(c1)
-----------------------------------------------------------
1                           0.5
2                           0.5
[2] row(s) selected.
```


## SUBSTR

Returns SIZE characters from a string column starting at START.

* START is 1-based; 0 returns NULL.
* If SIZE exceeds the remaining length, returns from START to the end of the string.
SIZE is optional and defaults to the string length.

```sql
SUBSTRING(column_name, start, [length])
```

```sql
Mach> CREATE LOG TABLE substr_table (c1 VARCHAR(10));
Created successfully.

Mach> INSERT INTO substr_table values('ABCDEFG');
1 row(s) inserted.

Mach> INSERT INTO substr_table values('abstract');
1 row(s) inserted.

Mach> SELECT SUBSTR(c1, 1, 1) FROM substr_table;
SUBSTR(c1, 1, 1)
--------------------
a
A
[2] row(s) selected.

Mach> SELECT SUBSTR(c1, 3, 3) FROM substr_table;
SUBSTR(c1, 3, 3)
--------------------
str
CDE
[2] row(s) selected.

Mach> SELECT SUBSTR(c1, 2) FROM substr_table;
SUBSTR(c1, 2)
-----------------
bstract
BCDEFG
[2] row(s) selected.

Mach> drop table substr_table;
Dropped successfully.

Mach> CREATE LOG TABLE substr_table (c1 VARCHAR(10));
Created successfully.

Mach> INSERT INTO substr_table values('ABCDEFG');
1 row(s) inserted.

Mach> SELECT SUBSTR(c1, 1, 1) FROM substr_table;
SUBSTR(c1, 1, 1)
--------------------
A
[1] row(s) selected.

Mach> SELECT SUBSTR(c1, 3, 3) FROM substr_table;
SUBSTR(c1, 3, 3)
--------------------
CDE
[1] row(s) selected.

Mach> SELECT SUBSTR(c1, 2) FROM substr_table;
SUBSTR(c1, 2)
-----------------
BCDEFG
[1] row(s) selected.
```


## SUBSTRING_INDEX

Returns the substring before count occurrences of delim. For negative count, searches from the end
and returns the substring from the delimiter position to the end.

count=0 returns NULL. If count is nonzero and the delimiter is absent, returns the entire input string.

```sql
SUBSTRING_INDEX(expression, delim, count)
```

```sql
Mach> CREATE LOG TABLE substring_table (url VARCHAR(30));
Created successfully.

Mach> INSERT INTO substring_table VALUES('www.machbase.com');
1 row(s) inserted.

Mach> SELECT SUBSTRING_INDEX(url, '.', 1) FROM substring_table;
SUBSTRING_INDEX(url, '.', 1)
----------------------------------
www
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', 2) FROM substring_table;
SUBSTRING_INDEX(url, '.', 2)
----------------------------------
www.machbase
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', -1) FROM substring_table;
SUBSTRING_INDEX(url, '.', -1)
----------------------------------
com
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(url, '.', 2), '.', -1) FROM substring_table;
SUBSTRING_INDEX(SUBSTRING_INDEX(url, '.', 2), '.', -1)
-------------------------------------------
machbase
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', 0) FROM substring_table;
SUBSTRING_INDEX(url, '.', 0)
----------------------------------
NULL
[1] row(s) selected.
```


## SUM

Aggregate function returning the sum of a numeric column.

```sql
SUM(column_name)
```

```sql
Mach> CREATE LOG TABLE sum_table (c1 INTEGER, c2 INTEGER);
Created successfully.

Mach> INSERT INTO sum_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(3, 4);
1 row(s) inserted.

Mach> SELECT c1, SUM(c1) from sum_table group by c1;
c1          SUM(c1)
------------------------------------
2           6
3           3
1           3
[3] row(s) selected.

Mach> SELECT c1, SUM(c2) from sum_table group by c1;
c1          SUM(c2)
------------------------------------
2           6
3           4
1           6
[3] row(s) selected.
```


## SUMSQ

SUMSQ returns the sum of squared numeric values.

```sql
SUMSQ(value)
```

```sql
Mach> CREATE LOG TABLE sumsq_table (c1 INTEGER, c2 INTEGER);
Created successfully.

Mach> INSERT INTO sumsq_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (1, 3);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (2, 4);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (2, 5);
1 row(s) inserted.

Mach> SELECT c1, SUMSQ(c2) FROM sumsq_table GROUP BY c1;
c1          SUMSQ(c2)
------------------------------------
2           41
1           14
[2] row(s) selected.
```


## SYSDATE / NOW

SYSDATE is a pseudocolumn, not a function, and returns current system time.

NOW provides the same behavior as SYSDATE for convenience.

```sql
SYSDATE
NOW
```

```sql
Mach> SELECT SYSDATE, NOW FROM t1;

SYSDATE                         NOW
-------------------------------------------------------------------
2017-01-16 14:14:53 310:973:000 2017-01-16 14:14:53 310:973:000
```


## TO_CHAR

Converts the input data type to a string. format_string is available depending on type, but cannot
be used for binary types.

```sql
TO_CHAR(column)
```

**TO_CHAR: Basic Data Types**

Basic data types convert to strings as shown below.

```sql
Mach> CREATE LOG TABLE fixed_table (id1 SHORT, id2 INTEGER, id3 LONG, id4 FLOAT, id5 DOUBLE, id6 IPV4, id7 IPV6, id8 VARCHAR (128));
Created successfully.

Mach> INSERT INTO fixed_table values(200, 19234, 1234123412, 3.14, 7.8338, '192.168.0.1', '::127.0.0.1', 'log varchar');
1 row(s) inserted.

Mach> SELECT '[ ' || TO_CHAR(id1) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id1) || ' ]'
------------------------------------------------------------------------------------
[ 200 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id2) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id2) || ' ]'
------------------------------------------------------------------------------------
[ 19234 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id3) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id3) || ' ]'
------------------------------------------------------------------------------------
[ 1234123412 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id4) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id4) || ' ]'
------------------------------------------------------------------------------------
[ 3.140000 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id5) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id5) || ' ]'
------------------------------------------------------------------------------------
[ 7.833800 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id6) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id6) || ' ]'
------------------------------------------------------------------------------------
[ 192.168.0.1 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id7) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id7) || ' ]'
------------------------------------------------------------------------------------
[ 0000:0000:0000:0000:0000:0000:7F00:0001 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id8) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id8) || ' ]'
------------------------------------------------------------------------------------
[ log varchar ]
[1] row(s) selected.
```

**TO_CHAR: Floating-point Numbers**

* Supported from 5.5.6

Converts float and double values to strings.
The format expression cannot be repeated and must have the form '[letter][number]'.

| Format | Description |
|--|--|
| F / f | Decimal places. Maximum: 30. |
| N / n | Decimal places with a comma every three integer digits. Maximum: 30. |

```sql
Mach> create table float_table (i1 float, i2 double);
Created successfully.

Mach> insert into float_table values (1.23456789, 1234.5678901234567890);
1 row(s) inserted.

Mach> select TO_CHAR(i1, 'f8'), TO_CHAR(i2, 'N9') from float_table;
TO_CHAR(i1, 'f8')       TO_CHAR(i2, 'N9')
--------------------------------------------------------------
1.23456788              1,234.567890123
[1] row(s) selected.
```

**TO_CHAR: DATETIME**

Converts datetime column values to formatted strings that can be generated and combined as needed.

If format_string is omitted, the default is "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn".

| Format | Description |
|--|--|
| YYYY | Four-digit year |
| YY | Two-digit year |
| MM | Two-digit month |
| MON | Three-letter English month abbreviation, such as JAN, FEB, MAY |
| DD | Two-digit day |
| DAY | Three-letter English weekday abbreviation, such as SUN, MON |
| IW | ISO 8601 week of year, 1–53, accounting for weekdays.<br>Weeks start on Monday.<br>The first week may belong to the previous year; the last week may belong to the next year.<br>See ISO 8601 for details. |
| WW | Week of year, 1–53, independent of weekday.<br>For example, January 1–7 returns 1. |
| W | Week of month, 1–5, independent of weekday.<br>For example, March 1–7 returns 1. |
| HH | Two-digit hour |
| HH12 | Two-digit hour in the range 1–12 |
| HH24 | Two-digit hour in the range 00–23 |
| HH2, HH3, HH6 | Truncate hours to the multiple after HH.<br>For HH6, hours 0–5 return 0 and 6–11 return 6.<br>Useful for time-series statistics.<br>Values use the 24-hour clock. |
| MI | Two-digit minute |
| MI2, MI5, MI10, MI20, MI30 | Truncate minutes to the multiple after MI.<br>For MI30, minutes 0–29 return 0 and 30–59 return 30.<br>Useful for time-series statistics. |
| SS | Two-digit second |
| SS2, SS5, SS10, SS20, SS30 | Truncate seconds to the multiple after SS.<br>For SS30, seconds 0–29 return 0 and 30–59 return 30.<br>Useful for time-series statistics. |
| AM | Display AM/PM |
| mmm | Three-digit milliseconds, 0–999 |
| uuu | Three-digit microseconds, 0–999 |
| nnn | Three-digit nanoseconds, 0–999 |

```sql
Mach> CREATE LOG TABLE datetime_table (id integer, dt datetime);
Created successfully.

Mach> INSERT INTO  datetime_table values(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(2, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(3, TO_DATE('2013-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(4, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> SELECT id, dt FROM datetime_table WHERE dt > TO_DATE('2000-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 11:22:33 444:555:666
3           2013-11-11 01:02:03 004:005:006
2           2012-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT id, dt FROM datetime_table WHERE dt > TO_DATE('2013-11-11 1:2:3') and dt < TO_DATE('2014-11-11 1:2:3');
id          dt
-----------------------------------------------
3           2013-11-11 01:02:03 004:005:006
[1] row(s) selected.

Mach> SELECT id, TO_CHAR(dt) FROM datetime_table;
id          TO_CHAR(dt)
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33 444:555:666
3           2013-11-11 01:02:03 004:005:006
2           2012-11-11 01:02:03 004:005:006
1           1999-11-11 01:02:03 004:005:006
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY')
-------------------------------------------------------------------------------------------------
4           2014
3           2013
2           2012
1           1999
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM')
-------------------------------------------------------------------------------------------------
4           2014-12
3           2013-11
2           2012-11
1           1999-11
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD')
-------------------------------------------------------------------------------------------------
4           2014-12-30
3           2013-11-11
2           2012-11-11
1           1999-11-11
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD TO_CHAR') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD TO_CHAR')
-------------------------------------------------------------------------------------------------
4           2014-12-30 TO_CHAR
3           2013-11-11 TO_CHAR
2           2012-11-11 TO_CHAR
1           1999-11-11 TO_CHAR
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS')
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33
3           2013-11-11 01:02:03
2           2012-11-11 01:02:03
1           1999-11-11 01:02:03
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.uuu.nnn') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33 444.555.666
3           2013-11-11 01:02:03 004.005.006
2           2012-11-11 01:02:03 004.005.006
1           1999-11-11 01:02:03 004.005.006
[4] row(s) selected.
```

**TO_CHAR: Unsupported Types**

TO_CHAR currently does not support binary types.

They cannot be converted to ordinary strings. Use TO_HEX() to inspect hexadecimal output.


## TO_DATE

Converts a string to datetime using the specified format.

If format_string is omitted, the default is "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn".

```sql
-- default format is "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" if no format exists.
TO_DATE(date_string [, format_string])
```

```sql
Mach> CREATE LOG TABLE to_date_table (id INTEGER, dt datetime);
Created successfully.

Mach> INSERT INTO  to_date_table VALUES(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(2, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(3, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(4, TO_DATE('2014-12-30 23:22:34 777:888:999', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn'));
1 row(s) inserted.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('1999-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 23:22:34 777:888:999
3           2014-12-30 11:22:33 444:555:666
2           2012-11-11 01:02:03 004:005:006
1           1999-11-11 01:02:03 004:005:006
[4] row(s) selected.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('2000-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 23:22:34 777:888:999
3           2014-12-30 11:22:33 444:555:666
2           2012-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('2012-11-11 1:2:3','YYYY-MM-DD HH24:MI:SS') and dt < TO_DATE('2014-11-11 1:2:3','YYYY-MM-DD HH24:MI:SS');
id          dt
-----------------------------------------------
2           2012-11-11 01:02:03 004:005:006
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999', 'YYYY') FROM to_date_table LIMIT 1;
id          TO_DATE('1999', 'YYYY')
-----------------------------------------------
4           1999-01-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12', 'YYYY-MM') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12', 'YYYY-MM')
-----------------------------------------------
4           1999.12.01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999', 'YYYY') FROM to_date_table LIMIT 1;
id          TO_DATE('1999', 'YYYY')
-----------------------------------------------
4           1999-01-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12', 'YYYY-MM') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12', 'YYYY-MM')
-----------------------------------------------
4           1999-12-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12', 'YYYY-MM-DD HH24:MI') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12', 'YYYY-MM-DD HH24:MI')
-------------------------------------------------------
4           1999-12-31 13:12:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS')
-------------------------------------------------------
4           1999-12-31 13:12:32 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123', 'YYYY-MM-DD HH24:MI:SS mmm') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32 123', 'YYYY-MM-DD HH24:MI:SS mmm')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123:456', 'YYYY-MM-DD HH24:MI:SS mmm:uuu') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32 123:456', 'YYYY-MM-DD HH24:MI:SS mmm:uuu')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:456:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123:456:789', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn') FROM to_date_table LIMIT 1;
id           TO_DATE('1999-12-31 13:12:32 123:456:789', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:456:789
[1] row(s) selected.
```


## TO_DATE_SAFE

Similar to TO_DATE(), but returns NULL without an error when conversion fails.

```sql
TO_DATE_SAFE(date_string [, format_string])
```

```sql
Mach> CREATE LOG TABLE date_table (ts DATETIME);
Created successfully.

Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-01-01', 'YYYY-MM-DD'));
1 row(s) inserted.
Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-01-02', 'YYYY'));
1 row(s) inserted.
Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-12-32', 'YYYY-MM-DD'));
1 row(s) inserted.

Mach> SELECT ts FROM date_table;
ts
----------------------------------
NULL
NULL
2016-01-01 00:00:00 000:000:000
[3] row(s) selected.
```


## TO_HEX

Returns NULL for NULL input; otherwise returns a hexadecimal string. short, int, and long are
converted to big-endian order for consistent output.

```sql
TO_HEX(column)
```

```sql
Mach> CREATE LOG TABLE hex_table (id1 SHORT, id2 INTEGER, id3 VARCHAR(10), id4 FLOAT, id5 DOUBLE, id6 LONG, id7 IPV4, id8 IPV6, id9 TEXT, id10 BINARY,
id11 DATETIME);
Created successfully.

Mach> INSERT INTO hex_table VALUES(256, 65535, '0123456789', 3.141592, 1024 * 1024 * 1024 * 3.14, 13513135446, '192.168.0.1', '::192.168.0.1', 'textext',
'binary', TO_DATE('1999', 'YYYY'));
1 row(s) inserted.

Mach> SELECT TO_HEX(id1), TO_HEX(id2), TO_HEX(id3), TO_HEX(id4), TO_HEX(id5), TO_HEX(id6), TO_HEX(id7), TO_HEX(id8), TO_HEX(id9), TO_HEX(id10), TO_HEX(id11)
FROM hex_table;
TO_HEX(id1)  TO_HEX(id2)  TO_HEX(id3)            TO_HEX(id4)  TO_HEX(id5)        TO_HEX(id6)        TO_HEX(id7)
-------------------------------------------------------------------------------------------------------------------------
TO_HEX(id8)                          TO_HEX(id9)
--------------------------------------------------------------------------------------------------------------------------
TO_HEX(id10)                                                                      TO_HEX(id11)
--------------------------------------------------------------------------------------------------------
0100   0000FFFF   30313233343536373839   D80F4940   1F85EB51B81EE941   0000000325721556   04C0A80001
06000000000000000000000000C0A80001   74657874657874
62696E617279                                                                      0CB325846E226000
[1] row(s) selected.
```


## TO_INET_STR

TO_INET_STR(ipv4_value) converts IPV4 to a dotted-decimal string.

```sql
TO_INET_STR(ipv4_value)
```

```sql
SELECT TO_INET_STR(TO_IPV4('192.168.0.1'));
```


## TO_IPV4 / TO_IPV4_SAFE

Converts a string to IPv4. If the string cannot be converted to a numeric address, TO_IPV4() returns
an error and stops the operation.

TO_IPV4_SAFE() instead returns NULL on error, allowing the operation to continue.

```sql
TO_IPV4(string_value)
TO_IPV4_SAFE(string_value)
```

```sql
Mach> CREATE LOG TABLE ipv4_table (c1 varchar(100));
Created successfully.

Mach> INSERT INTO ipv4_table VALUES('192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipv4_table VALUES('     192.168.0.2    ');
1 row(s) inserted.

Mach> INSERT INTO ipv4_table VALUES(NULL);
1 row(s) inserted.

Mach> SELECT c1 FROM ipv4_table;
c1
------------------------------------------------------------------------------------
NULL
     192.168.0.2
192.168.0.1
[3] row(s) selected.

Mach> SELECT TO_IPV4(c1) FROM ipv4_table;
TO_IPV4(c1)
------------------
NULL
192.168.0.2
192.168.0.1
[3] row(s) selected.

Mach> INSERT INTO ipv4_table VALUES('192.168.0.1.1');
1 row(s) inserted.

Mach> SELECT TO_IPV4(c1) FROM ipv4_table limit 1;
TO_IPV4(c1)
------------------
[ERR-02068 : Invalid IPv4 address format (192.168.0.1.1).]
[0] row(s) selected.

Mach> SELECT TO_IPV4_SAFE(c1) FROM ipv4_table;
TO_IPV4_SAFE(c1)
-------------------
NULL
NULL
192.168.0.2
192.168.0.1
[4] row(s) selected.
```


## TO_IPV6 / TO_IPV6_SAFE

Converts a string to IPv6. If conversion fails, TO_IPV6() returns an error and stops the operation.

TO_IPV6_SAFE() instead returns NULL on error, allowing the operation to continue.

```sql
TO_IPV6(string_value)
TO_IPV6_SAFE(string_value)
```

```sql
Mach> CREATE LOG TABLE ipv6_table (id varchar(100));
Created successfully.

Mach> INSERT INTO ipv6_table VALUES('::0.0.0.0');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0' || '.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('   ::127.0.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0.0.4  ');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('   ::FFFF:255.255.255.255   ');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('21DA:D3:0:2F3B:2AA:FF:FE28:9C5A');
1 row(s) inserted.

Mach> SELECT TO_IPV6(id) FROM ipv6_table;
TO_IPV6(id)
---------------------------------------------------------------
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.2
::127.0.0.1
::
[7] row(s) selected.

Mach> INSERT INTO ipv6_table VALUES('127.0.0.10.10');
1 row(s) inserted.

Mach> SELECT TO_IPV6(id) FROM ipv6_table limit 1;
TO_IPV6(id)
---------------------------------------------------------------
[ERR-02148 : Invalid IPv6 address format.(127.0.0.10.10)]
[0] row(s) selected.

Mach> SELECT TO_IPV6_SAFE(id) FROM ipv6_table;
TO_IPV6_SAFE(id)
---------------------------------------------------------------
NULL
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.2
::127.0.0.1
::
[8] row(s) selected.
```


## TO_NUMBER / TO_NUMBER_SAFE

Converts a string to a number (double). If conversion fails, TO_NUMBER() returns an error and stops
the operation.

TO_NUMBER_SAFE() instead returns NULL on error, allowing the operation to continue.

```sql
TO_NUMBER(string_value)
TO_NUMBER_SAFE(string_value)
```

```sql
Mach> CREATE LOG TABLE number_table (id varchar(100));
Created successfully.

Mach> INSERT INTO number_table VALUES('10');
1 row(s) inserted.

Mach> INSERT INTO number_table VALUES('20');
1 row(s) inserted.

Mach> INSERT INTO number_table VALUES('30');
1 row(s) inserted.

Mach> SELECT TO_NUMBER(id) from number_table;
TO_NUMBER(id)
------------------------------
30
20
10
[3] row(s) selected.

Mach> CREATE LOG TABLE safe_table (id varchar(100));
Created successfully.

Mach> INSERT INTO safe_table VALUES('invalidnumber');
1 row(s) inserted.

Mach> SELECT TO_NUMBER(id) from safe_table;
TO_NUMBER(id)
------------------------------
[ERR-02145 : The string cannot be converted to number value.(invalidnumber)]
[0] row(s) selected.

Mach> SELECT TO_NUMBER_SAFE(id) from safe_table;
TO_NUMBER_SAFE(id)
------------------------------
NULL
[1] row(s) selected.
```


## TOP_K {#top_k}

TOP_K(value, k) returns the k most frequent numeric values as a value:count string.

```sql
TOP_K(value, k)
```

- value must be numeric.
- k must be a positive integer constant.
- NULL values are ignored.
- The return type is VARCHAR.
- Results are ordered by descending frequency, then ascending value for ties.

```sql
SELECT TOP_K(alarm_code, 3)
FROM event_log;
```

Example result:

```text
101:532,205:317,301:90
```


## TO_TIMESTAMP

Converts datetime to nanoseconds elapsed since 1970-01-01 00:00:00 UTC.

Dates and times below use UTC+09:00.

```sql
TO_TIMESTAMP(datetime_value)
```

```sql
Mach> create table datetime_tbl (c1 datetime);
Created successfully.

Mach> insert into datetime_tbl values ('2010-01-01 10:10:10');
1 row(s) inserted.

Mach> select to_timestamp(c1) from datetime_tbl;
to_timestamp(c1)
-----------------------
1262308210000000000
[1] row(s) selected.
```


## TRUNC

TRUNC truncates a value to n decimal places.

If n is omitted, it defaults to 0 and removes all decimal places. Negative n truncates at the
corresponding position before the decimal point.

```sql
TRUNC(number [, n])
```

```sql
Mach> CREATE LOG TABLE trunc_table (i1 DOUBLE);
Created successfully.

Mach> INSERT INTO trunc_table VALUES (158.799);
1 row(s) inserted.

Mach> SELECT TRUNC(i1, 1), TRUNC(i1, -1) FROM trunc_table;
TRUNC(i1, 1)                TRUNC(i1, -1)
-----------------------------------------------------------
158.7                       150
[1] row(s) selected.

Mach> SELECT TRUNC(i1, 2), TRUNC(i1, -2) FROM trunc_table;
TRUNC(i1, 2)                TRUNC(i1, -2)
-----------------------------------------------------------
158.79                      100
[1] row(s) selected.
```


## TS_CHANGE_COUNT

Aggregate function counting changes in a column's value.

Cannot be used with JOIN or an inline view because chronological input order cannot be guaranteed.
VARCHAR is not supported.

* **Unavailable in Cluster Edition.**

```sql
TS_CHANGE_COUNT(column)
```

```sql
Mach> CREATE LOG TABLE ipcount_table (id INTEGER, ip IPV4);
Created successfully.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.4');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.4');
1 row(s) inserted.

Mach> SELECT id, TS_CHANGE_COUNT(ip) from ipcount_table GROUP BY id;
id          TS_CHANGE_COUNT(ip)
------------------------------------
2           2
1           4
[2] row(s) selected.
```


## UNIX_TIMESTAMP

UNIX_TIMESTAMP converts a date value to a 32-bit integer based on Unix time(). FROM_UNIXTIME
performs the reverse conversion.

```sql
UNIX_TIMESTAMP(datetime_value)
```

```sql
Mach> CREATE table unix_table (c1 int);
Created successfully.

Mach> INSERT INTO unix_table VALUES (UNIX_TIMESTAMP('2001-01-01'));
1 row(s) inserted.

Mach> SELECT * FROM unix_table;
C1
--------------
978274800
[1] row(s) selected.
```


## UPPER

Converts English letters to uppercase.

```sql
UPPER(string_value)
```

```sql
Mach> CREATE LOG TABLE upper_table(id INTEGER,name VARCHAR(10));
Created successfully.

Mach> INSERT INTO upper_table VALUES(1, '');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(2, 'James');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(3, 'sarah');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(4, 'THOMAS');
1 row(s) inserted.

Mach> SELECT id, UPPER(name) FROM upper_table;
id          UPPER(name)
----------------------------
4           THOMAS
3           SARAH
2           JAMES
1           NULL
[4] row(s) selected.
```


## VARIANCE / VAR_POP

Aggregate functions returning variance of a numeric column. VARIANCE returns sample variance;
VAR_POP returns population variance.

```sql
VARIANCE(column_name)
VAR_POP(column_name)
```

```sql
Mach> CREATE LOG TABLE var_table(c1 INTEGER, c2 DOUBLE);
Created successfully.

Mach> INSERT INTO var_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (2, 1);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (2, 2);
1 row(s) inserted.

Mach> SELECT VARIANCE(c1) FROM var_table;
VARIANCE(c1)
------------------------------
0.333333
[1] row(s) selected.

Mach> SELECT VAR_POP(c1) FROM var_table;
VAR_POP(c1)
------------------------------
0.25
[1] row(s) selected.
```


## YEAR / MONTH / DAY

Extracts year, month, and day from a datetime column as integers.

```sql
YEAR(datetime_col)
MONTH(datetime_col)
DAY(datetime_col)
```

```sql
Mach> CREATE LOG TABLE extract_table(c1 DATETIME, c2 INTEGER);
Created successfully.

Mach> INSERT INTO extract_table VALUES (to_date('2001-01-01 12:30:00 000:000:000'), 1);
1 row(s) inserted.

Mach> SELECT YEAR(c1), MONTH(c1), DAY(c1) FROM extract_table;
year(c1)    month(c1)   day(c1)
----------------------------------------
2001        1           1
```


## ISNAN / ISINF

Tests whether a numeric argument is NaN or Inf, returning 1 if so and 0 otherwise.

```sql
ISNAN(number)
ISINF(number)
```

The example assumes the table already contains NaN and Inf values.
SQL INSERT cannot use nan or inf tokens directly as values.

```sql
Mach> SELECT * FROM test;
I1                          I2                          I3
------------------------------------------------------------------------
1                           1                           1
nan                         inf                         0
NULL                        NULL                        NULL
[3] row(s) selected.


Mach> SELECT ISNAN(i1), ISNAN(i2), ISNAN(i3), i3 FROM test ;
ISNAN(i1)   ISNAN(i2)   ISNAN(i3)   i3
-----------------------------------------------------
0           0           0           1
1           0           0           0
NULL        NULL        NULL        NULL
[3] row(s) selected.

Mach> SELECT * FROM test WHERE ISNAN(i1) = 1;
I1                          I2                          I3
------------------------------------------------------------------------
nan                         inf                         0
[1] row(s) selected.
```

## JSON_SET

Stores a SQL scalar as a JSON scalar at the specified document path.

```sql
JSON_SET(json_doc, path, scalar)
```

```sql
Mach> SELECT JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE') FROM dual;
JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE')
--------------------------------------------------------------------------------
{"ship":{"status":"DONE"}}
[1] row(s) selected.
```

Notes:

- path must be a full JSONPath.
- JSON_SET(..., path, NULL) stores JSON null.
- A NULL document argument produces SQL NULL.
- A NULL or empty path causes an error.
- Support focuses on object paths.
- Array element updates such as $.items[0] are not supported.

## JSON_SET_JSON

Parses the third argument as JSON text and stores an object or array subtree.

```sql
JSON_SET_JSON(json_doc, path, json_text)
```

```sql
Mach> SELECT JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}') FROM dual;
JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}')
----------------------------------------------------------------------------
{"ship":{"owner":{"name":"machbase"}}}
[1] row(s) selected.
```

Notes:

- path must be a full JSONPath.
- If the third argument is SQL NULL, the result is SQL NULL.
- Invalid JSON text causes an error.
- Support focuses on object paths.
- Array element updates are not supported.

## JSON_REMOVE

Removes a member or subpath from a JSON document.

```sql
JSON_REMOVE(json_doc, path)
```

```sql
Mach> SELECT JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team') FROM dual;
JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team')
--------------------------------------------------------------------------
{"owner":{"name":"machbase"}}
[1] row(s) selected.
```

Notes:

- path must be a full JSONPath.
- A missing path is a no-op.
- JSON_REMOVE(..., '$') is not allowed.
- A NULL document argument produces SQL NULL.

## PI() {#pi}

Returns π as DOUBLE.

```sql
SELECT PI();
```

```sql
Mach> SELECT PI();
PI()
------------------------------
3.141592653589793
[1] row(s) selected.
```

## SQRT() {#sqrt}

Returns the square root.

```sql
SELECT SQRT(9), SQRT(2.25), SQRT(16.0);
```

```sql
Mach> SELECT SQRT(9), SQRT(2.25), SQRT(16.0);
SQRT(9)   SQRT(2.25)         SQRT(16.0)
-----------------------------------------------
3         1.5000000000000000  4
[1] row(s) selected.
```

## POWER() {#power}

Returns base raised to exponent.

```sql
SELECT POWER(2, 3), POWER(9, 0.5), POWER(4, -1);
```

```sql
Mach> SELECT POWER(2, 3), POWER(9, 0.5), POWER(4, -1);
POWER(2, 3)   POWER(9, 0.5)   POWER(4, -1)
------------------------------------------------
8             3.0000000000000000 0.2500000000000000
[1] row(s) selected.
```

## POW() {#pow}

Alias for POWER().

```sql
SELECT POW(2, 3), POW(2, -1), POW(10, 0);
```

```sql
Mach> SELECT POW(2, 3), POW(2, -1), POW(10, 0);
POW(2, 3)   POW(2, -1)   POW(10, 0)
-----------------------------------------
8           0.5           1
[1] row(s) selected.
```

## LOG() {#log}

LOG(n) calculates the natural logarithm; LOG(base, n) calculates the logarithm to the specified base.

```sql
SELECT LOG(2, 8), LOG(100), LOG(10, 1000);
```

```sql
Mach> SELECT LOG(2, 8), LOG(100), LOG(10, 1000);
LOG(2, 8)   LOG(100)             LOG(10, 1000)
------------------------------------------------
3           4.605170185988092     3
[1] row(s) selected.
```

## LN() {#ln}

Returns the natural logarithm ln(n).

```sql
SELECT LN(1), LN(10), LN(1000);
```

```sql
Mach> SELECT LN(1), LN(10), LN(1000);
LN(1)      LN(10)         LN(1000)
-----------------------------------
0          2.302585092994046 6.907755278982137
[1] row(s) selected.
```

## EXP() {#exp}

Returns e^n.

```sql
SELECT EXP(0), EXP(1), EXP(-1);
```

```sql
Mach> SELECT EXP(0), EXP(1), EXP(-1);
EXP(0)      EXP(1)         EXP(-1)
-----------------------------------
1           2.718281828459045 0.36787944117144233
[1] row(s) selected.
```

## FLOOR() {#floor}

Rounds down toward negative infinity.

```sql
SELECT FLOOR(-1.2), FLOOR(3.9), FLOOR(-3.0);
```

```sql
Mach> SELECT FLOOR(-1.2), FLOOR(3.9), FLOOR(-3.0);
FLOOR(-1.2)  FLOOR(3.9)  FLOOR(-3.0)
-----------------------------------------
-2            3           -3
[1] row(s) selected.
```

## CEIL() {#ceil}

Rounds up toward positive infinity.

```sql
SELECT CEIL(-1.2), CEIL(3.2), CEIL(-3.0);
```

```sql
Mach> SELECT CEIL(-1.2), CEIL(3.2), CEIL(-3.0);
CEIL(-1.2)  CEIL(3.2)  CEIL(-3.0)
-------------------------------------
-1           4          -3
[1] row(s) selected.
```

## SIN() {#sin}

Returns sine for an input in radians.

```sql
SELECT SIN(0), SIN(PI()/2), SIN(PI());
```

```sql
Mach> SELECT SIN(0), SIN(PI()/2), SIN(PI());
SIN(0)      SIN(PI()/2)   SIN(PI())
------------------------------------
0           1             0
[1] row(s) selected.
```

## SLOPE {#slope}

SLOPE(y, x) calculates the linear regression slope for numeric (x, y) points.

```sql
SLOPE(y, x)
```

- Both arguments must be numeric.
- NULL values are ignored.
- Insufficient valid data or zero x variance produces NULL.
- The return type is DOUBLE.

```sql
SELECT SLOPE(temp_c, sample_sec)
FROM sensor_log;
```

## COS() {#cos}

Returns cosine for an input in radians.

```sql
SELECT COS(0), COS(PI()), COS(PI()/2);
```

```sql
Mach> SELECT COS(0), COS(PI()), COS(PI()/2);
COS(0)      COS(PI())   COS(PI()/2)
-------------------------------------
1           -1          0
[1] row(s) selected.
```

## TAN() {#tan}

Returns tangent for an input in radians.

```sql
SELECT TAN(0), TAN(PI()/4), TAN(PI());
```

```sql
Mach> SELECT TAN(0), TAN(PI()/4), TAN(PI());
TAN(0)      TAN(PI()/4)  TAN(PI())
-----------------------------------
0           1            0
[1] row(s) selected.
```

## MOD() {#mod}

Calculates the remainder with the quotient truncated toward zero.

```sql
SELECT MOD(10, 3), MOD(11, 4), MOD(-10, 3), MOD(3.5, 0.5);
```

```sql
Mach> SELECT MOD(10, 3), MOD(11, 4), MOD(-10, 3), MOD(3.5, 0.5);
MOD(10, 3)  MOD(11, 4)  MOD(-10, 3)  MOD(3.5, 0.5)
-------------------------------------------------------
1           3           -1           0
[1] row(s) selected.
```

## MODE {#mode}

MODE(value) returns the most frequent numeric value in the input set.

```sql
MODE(value)
```

- value must be numeric.
- NULL values are ignored.
- Ties return the smaller value.
- The return type is DOUBLE.

```sql
SELECT MODE(alarm_code)
FROM event_log;
```

## P05 / P10 / P90 / P95 {#p05-p10-p90-p95}

Exact percentile shorthand functions for frequently used percentiles.

```sql
P05(value)
P10(value)
P90(value)
P95(value)
```

- value must be numeric.
- NULL values are ignored.
- The return type is DOUBLE.

P05, P10, P90, and P95 correspond to PERCENTILE_CONT(value, 0.05), 0.10, 0.90, and 0.95 respectively.

```sql
SELECT P05(response_ms),
       P10(response_ms),
       P90(response_ms),
       P95(response_ms)
FROM web_log;
```

## PERCENTILE_CONT / PERCENTILE_DISC {#percentile_cont-percentile_disc}

Aggregate functions calculating exact percentiles for numeric input.

```sql
PERCENTILE_CONT(value, ratio)
PERCENTILE_DISC(value, ratio)
```

- value must be numeric.
- ratio must be a constant from 0.0 through 1.0.
- PERCENTILE_CONT interpolates between adjacent sorted values when needed.
- PERCENTILE_DISC selects an observed value at the target rank.
- Both return DOUBLE.

```sql
SELECT PERCENTILE_CONT(latency_ms, 0.95) AS pcont95,
       PERCENTILE_DISC(latency_ms, 0.95) AS pdisc95
FROM api_log;
```

## QUANTILE {#quantile}

QUANTILE(value, ratio) calculates an exact continuous percentile for numeric input.

```sql
QUANTILE(value, ratio)
```

- value must be numeric.
- ratio must be a constant from 0.0 through 1.0.
- The return type is DOUBLE.
- Uses the same continuous-percentile semantics as PERCENTILE_CONT.

```sql
SELECT QUANTILE(cpu_usage, 0.75)
FROM host_metric;
```

## RAND() {#rand}

Generates a random value.

```sql
SELECT RAND(5) = RAND(5) AS same_seed, RAND(7) = RAND(8) AS diff_seed, RAND() = RAND() AS diff_default;
```

```sql
Mach> SELECT RAND(5) = RAND(5) AS same_seed, RAND(7) = RAND(8) AS diff_seed, RAND() = RAND() AS diff_default FROM m$sys_users WHERE name = 'SYS';
same_seed   diff_seed   diff_default
------------------------------------
1           0           0
[1] row(s) selected.
```

RAND(seed) returns the same value for the same seed. RAND() generates a value in
[0,1) from internal session state.

## REGEXP_LIKE

REGEXP_LIKE tests whether a string matches a regular expression and returns a Boolean.
It is commonly used in WHERE.

```sql
REGEXP_LIKE(source, pattern)
REGEXP_LIKE(source, pattern, match_param)
```

- source must be VARCHAR.
- pattern must be a constant VARCHAR regular expression.
- Optional match_param must be a constant VARCHAR. c enables case-sensitive matching;
  i enables case-insensitive matching. Default: c.

```sql
SELECT *
FROM sensor_text
WHERE REGEXP_LIKE(message, 'error|warn', 'i');
```

## REGEXP_INSTR

REGEXP_INSTR returns the 1-based position of a regular expression match, or 0 if
none exists.

```sql
REGEXP_INSTR(source, pattern[, position[, occurrence[, return_pos[, match_param]]]])
```

- source must be VARCHAR.
- pattern must be a constant VARCHAR regular expression.
- position and occurrence must be constant integers of at least 1.
- return_pos must be a constant integer: 0 returns the start position; 1 returns
  the position after the match.
- match_param accepts c or i; default: c.

```sql
SELECT REGEXP_INSTR('TechOnTheNet', 'The', 1, 1, 1, 'i');
```

## REGEXP_SUBSTR

REGEXP_SUBSTR returns the substring matching a regular expression.

```sql
REGEXP_SUBSTR(source, pattern[, position[, occurrence[, match_param]]])
```

- source must be VARCHAR.
- pattern must be a constant VARCHAR regular expression.
- position and occurrence must be constant integers of at least 1.
- match_param accepts c or i; default: c.

```sql
SELECT REGEXP_SUBSTR('TechOnTheNet', 'a|e|i|o|u', 1, 2, 'i');
```

## REGEXP_REPLACE

REGEXP_REPLACE replaces text matching a regular expression.

```sql
REGEXP_REPLACE(source, pattern[, replacement[, position[, occurrence[, match_param]]]])
```

- source must be VARCHAR.
- pattern and replacement must be constant VARCHAR values.
- Omitting replacement removes matching text.
- position must be a constant integer of at least 1.
- occurrence must be a constant integer: 0 replaces every match; a positive value replaces
  only that occurrence.
- match_param accepts c or i; default: c.

```sql
SELECT REGEXP_REPLACE('TechOnTheNet', 'a|e|i|o|u', 'Z', 1, 2, 'i');
```

<a id="support-type-of-built-in-function"></a>
## Supported Types for Built-in Functions

| |Short|Integer|Long|Float|Double|Varchar|Text|Ipv4|Ipv6|Datetime|Binary|
|--|--|--|--|--|--|--|--|--|--|--|--|
|ABS|o|o|o|o|o|x|x|x|x|x|x|
|ADD_TIME|x|x|x|x|x|x|x|x|x|o|x|
|APPROX_PERCENTILE / APPROX_MEDIAN / APPROX_P05 / APPROX_P10 / APPROX_P90 / APPROX_P95|o|o|o|o|o|x|x|x|x|x|x|
|AREA|o|o|o|o|o|x|x|x|x|x|x|
|AVG|o|o|o|o|o|x|x|x|x|x|x|
|BITAND / BITOR|o|o|o|x|x|x|x|x|x|x|x|
|COUNT|o|o|o|o|o|o|x|o|o|o|x|
|CUME_DIST|o|o|o|o|o|x|x|x|x|x|x|
|DATE_TRUNC|x|x|x|x|x|x|x|x|x|o|x|
|DECODE|o|o|o|o|o|o|x|o|x|o|x|
|FIRST / LAST|o|o|o|o|o|o|x|o|o|o|x|
|FROM_TIMESTAMP|o|o|o|o|o|x|x|x|x|x|x|
|FROM_UNIXTIME|o|o|o|o|o|x|x|x|x|x|x|
|GROUP_CONCAT|o|o|o|o|o|o|x|o|o|o|x|
|INSTR|x|x|x|x|x|o|o|x|x|x|x|
|LEAST / GREATEST|o|o|o|o|o|o|x|x|x|x|x|
|LENGTH|x|x|x|x|x|o|o|x|x|x|o|
|LOWER|x|x|x|x|x|o|x|x|x|x|x|
|LPAD / RPAD|x|x|x|x|x|o|x|x|x|x|x|
|LTRIM / RTRIM|x|x|x|x|x|o|x|x|x|x|x|
|MAX|o|o|o|o|o|o|x|o|o|o|x|
|MEDIAN|o|o|o|o|o|x|x|x|x|x|x|
|MIN|o|o|o|o|o|o|x|o|o|o|x|
|MODE|o|o|o|o|o|x|x|x|x|x|x|
|NVL|x|x|x|x|x|o|x|o|x|x|x|
|P05 / P10 / P90 / P95|o|o|o|o|o|x|x|x|x|x|x|
|PERCENTILE_CONT / PERCENTILE_DISC|o|o|o|o|o|x|x|x|x|x|x|
|QUANTILE|o|o|o|o|o|x|x|x|x|x|x|
|REGEXP_LIKE|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_INSTR|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_SUBSTR|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_REPLACE|x|x|x|x|x|o|x|x|x|x|x|
|SLOPE|o|o|o|o|o|x|x|x|x|x|x|
|TOP_K|o|o|o|o|o|x|x|x|x|x|x|
|ROUND|o|o|o|o|o|x|x|x|x|x|x|
|ROWNUM|o|o|o|o|o|o|o|o|o|o|o|
|SERIESNUM|o|o|o|o|o|o|o|o|o|o|o|
|STDDEV / STDDEV_POP|o|o|o|o|o|x|x|x|x|x|x|
|SUBSTR|x|x|x|x|x|o|x|x|x|x|x|
|SUBSTRING_INDEX|x|x|x|x|x|o|o|x|x|x|x|
|SUM|o|o|o|o|o|x|x|x|x|x|x|
|SYSDATE / NOW|x|x|x|x|x|x|x|x|x|x|x|
|TO_CHAR|o|o|o|o|o|o|x|o|o|o|x|
|TO_DATE / TO_DATE_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_HEX|o|o|o|o|o|o|o|o|o|o|o|
|TO_INET_STR|x|x|x|x|x|x|x|o|x|x|x|
|TO_IPV4 / TO_IPV4_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_IPV6 / TO_IPV6_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_NUMBER / TO_NUMBER_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_TIMESTAMP|x|x|x|x|x|x|x|x|x|o|x|
|TRUNC|o|o|o|o|o|x|x|x|x|x|x|
|TS_CHANGE_COUNT|o|o|o|o|o|x|x|o|o|o|x|
|UNIX_TIMESTAMP|x|x|x|x|x|x|x|x|x|o|x|
|UPPER|x|x|x|x|x|o|x|x|x|x|x|
|VARIANCE / VAR_POP|o|o|o|o|o|x|x|x|x|x|x|
|YEAR / MONTH / DAY|x|x|x|x|x|x|x|x|x|o|x|
|ISNAN / ISINF|o|o|o|o|o|x|x|x|x|x|x|


<a id="json-related-function"></a>
## JSON Functions

These functions take JSON data as arguments.

| Function | Description | Notes |
|--|--|--|
| JSON_EXTRACT(JSON column name, 'json path') | Returns a string.<br>Returns ERROR if the value is missing. | JSON object/array: serialize to a string.<br>String: return unchanged.<br>Numeric: convert to a string.<br>Boolean: return "True" or "False". |
| JSON_EXTRACT_DOUBLE(JSON column name, 'json path') | Returns a 64-bit double.<br>Returns NULL if the value is missing. | JSON object/array: NULL.<br>String: convert if possible; otherwise NULL.<br>Numeric: 64-bit floating-point value.<br>Boolean: "True" becomes 1.0; "False" becomes 0.0. |
| JSON_EXTRACT_INTEGER(JSON column name, 'json path') | Returns a 64-bit integer.<br>Returns NULL if the value is missing. | JSON object/array: NULL.<br>String: convert if possible; otherwise NULL.<br>Numeric: 64-bit integer.<br>Boolean: "True" becomes 1; "False" becomes 0. |
| JSON_EXTRACT_STRING(JSON column name, 'json path') | Returns a string.<br>Returns NULL if the value is missing.<br>Same result as the arrow (→) operator. | JSON object/array: serialize to a string.<br>String: return unchanged.<br>Numeric: convert to a string.<br>Boolean: return "True" or "False". |
| JSON_SET(json_doc, path, scalar) | Returns a new JSON document with a SQL scalar stored as a JSON scalar at the path. | Full JSONPath required.<br>NULL values become JSON null.<br>Only object paths supported. |
| JSON_SET_JSON(json_doc, path, json_text) | Returns a new JSON document with JSON text stored as an object or array subtree at the path. | Full JSONPath required.<br>SQL NULL third argument produces SQL NULL.<br>Invalid JSON text causes an error. |
| JSON_REMOVE(json_doc, path) | Returns a new JSON document with the member or subtree at the path removed. | Full JSONPath required.<br>Missing path is a no-op.<br>JSON_REMOVE(..., '$') is not allowed. |
| JSON_IS_VALID('json string') | Checks whether JSON text is valid. | 0: False<br>1: True |
| JSON_TYPEOF(JSON column name, 'json path') | Returns the value type. | None: key absent<br>Object: object<br>Integer: integer<br>Real: floating-point<br>String: string<br>True/False: Boolean<br>Array: array<br>Null: NULL |

```sql
Mach> CREATE LOG TABLE jsontbl (name VARCHAR(20), jval JSON);
Created successfully.

Mach> INSERT INTO jsontbl VALUES("name1", '{"name":"test1"}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name2", '{"name":"test2", "value":123}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name3", '{"name":{"class1": "test3"}}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name4", '{"myarray": [1, 2, 3, 4]}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name5", '{"name":"error"');
[ERR-02233: Error occurred at column (2): (Error in json load.)]

Mach> SELECT name, JSON_EXTRACT_STRING(jval, '$.name') FROM jsontbl;
name                  JSON_EXTRACT_STRING(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 {"class1": "test3"}
name2                 test2
name1                 test1
[4] row(s) selected.

Mach> SELECT name, JSON_EXTRACT_INTEGER(jval, '$.myarray[1]') FROM jsontbl;
name                  JSON_EXTRACT_INTEGER(jval, '$.myarray[1]')
--------------------------------------------------------------------
name4                 2
name3                 NULL
name2                 NULL
name1                 NULL
[4] row(s) selected.

Mach> SELECT name, JSON_TYPEOF(jval, '$.name') FROM jsontbl;
name                  JSON_TYPEOF(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 None
name3                 Object
name2                 String
name1                 String
[4] row(s) selected.
```


<a id="json-operator"></a>
## JSON Operators

The -> operator accesses objects in JSON data.

Returns the same result as JSON_EXTRACT_STRING.

```sql
json_col -> 'json path'
```

Access JSON column members with the JSONPath -> operator or dot shorthand.

```sql
-- JSONPath arrow syntax
jval->'$.sensor.temperature'

-- JSON dot shorthand
jval.sensor.temperature
```

Both expressions retrieve the same JSON value. The existing -> operator remains available; dot
notation is additional syntax for a shorter expression.

```sql
Mach> SELECT name, jval->'$.name' FROM jsontbl;
name                  JSON_EXTRACT_STRING(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 {"class1": "test3"}
name2                 test2
name1                 test1
[4] row(s) selected.

Mach> SELECT name, jval->'$.myarray[1]' FROM jsontbl;
name                  JSON_EXTRACT_INTEGER(jval, '$.myarray[1]')
--------------------------------------------------------------------
name4                 2
name3                 NULL
name2                 NULL
name1                 NULL
[4] row(s) selected.

Mach> SELECT name, jval->'$.name.class1' FROM jsontbl;
name                  jval->'$.name.class1'
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 test3
name2                 NULL
name1                 NULL
[4] row(s) selected
```

### JSONPath Arrow Syntax

Arrow syntax uses a JSONPath string.

```sql
jval->'$.name'
jval->'$.sensor.temperature'
jval->'$.items[0].name'
```

Brackets can also specify JSON keys directly. Use brackets when a key contains a dot (.).

```sql
-- Key named a.b
jval->'$["a.b"]'
jval->'$[a.b]'

-- Multiple key levels with brackets
jval->'$[Plant1][Line1][Temperature]'

-- One key name containing dots
jval->'$[Plant1.Line1.Temperature]'
```

`$[Plant1.Line1.Temperature]` looks up one key named Plant1.Line1.Temperature. To traverse Plant1,
Line1, and Temperature separately, use `$[Plant1][Line1][Temperature]` or
`$.Plant1.Line1.Temperature`.

For keys containing special characters or dots, quoted bracket syntax is recommended:

```sql
jval->'$["a.b"]["c.d"]["e.f"]'
```

The following syntax is not supported.

```sql
jval->'$."a.b"'
```

### JSON Dot Shorthand

Append member names to a JSON column to query JSON values.

```sql
-- Single member
jval.name

-- Nested member
jval.sensor.temperature

-- Array index
jval.items[0].name

-- Key containing special characters
jval.items[0]."product-id"
```

Double-quoted keys in dot syntax preserve case and special characters.

```sql
SELECT name, jval."Camel-Key", jval.items[0]."product-id"
  FROM jsontbl
 ORDER BY name;
```

### Type Comparison in WHERE

JSON member access results display as strings. When compared with SQL numeric values in WHERE,
however, JSON values are parsed as numbers and compared numerically.

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.value' > 100
 ORDER BY name;

SELECT name
  FROM jsontbl
 WHERE jval.value BETWEEN 10 AND 30
 ORDER BY name;

SELECT name
  FROM jsontbl
 WHERE jval.value IN (10, 20, 30)
 ORDER BY name;
```

Supported comparisons:

- JSON integer with SQL integer
- JSON real/double with SQL numeric
- JSON numeric string with SQL numeric
- JSON Boolean with strings 'true' and 'false'
- `=`, `<>`, `<`, `<=`, `>`, `>=`, `BETWEEN`, literal `IN (...)`

When compared with SQL integers, JSON integers use integer comparison. Values beyond double
precision, such as 9007199254740992 and 9007199254740993, remain distinguishable.

Comparisons with character values continue to use string comparison.

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.name' = 'test1'
 ORDER BY name;
```

In numeric comparisons, JSON values that cannot be parsed as numbers do not match; they do not cause
errors. Ordinary VARCHAR-versus-number comparison rules are unchanged. Automatic numeric comparison
applies only to JSON member access expressions.

### Name Resolution

Ordinary SQL column name resolution takes precedence over JSON dot resolution.

```sql
SELECT t.jval.name
  FROM jsontbl t;
```

The expression above is first resolved as an ordinary column name. If that fails and jval is a JSON
column, jval.name is treated as JSON member access.

JSON dot access must be rooted in a JSON column.

```sql
-- Not supported
(jval->'$.sensor').temperature
name.member
```

### Constraints

The following syntax is not supported.

- wildcard: `jval.items[*].name`
- recursive descent: `jval..name`
- filter expression: `jval.items[?(@.price > 10)]`
- negative array index: `jval.items[-1]`
- single quoted key: `jval.'product-id'`
- Mixing dot and arrow syntax: `jval.items->'$.name'`
- Dot access on a non-JSON column: `name.member`
- Dot access after an arbitrary expression: `(jval->'$.sensor').temperature`
- quoted member arrow path: `jval->'$."a.b"'`

Automatic numeric comparison of JSON members is not supported in subquery IN, `IN (SELECT ...)`. Use
literal IN (...).

<a id="window-function"></a>
## Window Functions

Window functions compare and calculate across rows and are also called analytic or ranking functions.

Available only in SELECT.

### Window Function Syntax

Window functions must include OVER.

```
WINDOW_FUNCTION (ARGUMENTS) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

* WINDOW_FUNCTION: Function name
* ARGUMENTS: Zero or more arguments, depending on the function
* PARTITION BY clause: Divide the full set into smaller groups (optional)
* ORDER BY clause: Specify sort order (optional)

### Window Function List

#### LAG

Returns the value from N rows before the current row within each partition's window.

Returns NULL if no such row exists.

```
LAG(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE LOG TABLE lag_table (name varchar(10), dt datetime, value INTEGER);
Created successfully.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-01'), 1);
1 row(s) inserted.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-02'), 2);
1 row(s) inserted.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-03'), 3);
1 row(s) inserted.

-- Divide the set by name, sort by dt, and retrieve the first previous value.
Mach> SELECT name, dt, value, LAG(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lag_table;
name        dt                              value       LAG(value, 1)
---------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           NULL
name1       2024-01-02 00:00:00 000:000:000 2           1
name1       2024-01-03 00:00:00 000:000:000 3           2
[3] row(s) selected.
```


#### LEAD

Returns the value from N rows after the current row within each partition's window.

Returns NULL if no such row exists.

```
LEAD(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE LOG TABLE lead_table (name varchar(10), dt datetime, value INTEGER);
Created successfully.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-01'), 1);
1 row(s) inserted.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-02'), 2);
1 row(s) inserted.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-03'), 3);
1 row(s) inserted.

-- Divide the set by name, sort by dt, and retrieve the first and subsequent values.
Mach> SELECT name, dt, value, LEAD(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lead_table;
name        dt                              value       LEAD(value, 1)
----------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           2
name1       2024-01-02 00:00:00 000:000:000 2           3
name1       2024-01-03 00:00:00 000:000:000 3           NULL
[3] row(s) selected.
```


#### NTILE

NTILE(n) divides ordered rows into n buckets as evenly as possible and returns each row's bucket number.

```
NTILE(n) OVER ([PARTITION BY column_name] ORDER BY column_name)
```

- n must be a positive constant.
- ORDER BY inside OVER (...) is required.
- When rows do not divide evenly, earlier buckets each receive one extra row.

```
Mach> SELECT user_id,
             score,
             NTILE(4) OVER (ORDER BY score) AS score_band
      FROM exam_result;
```
