---
title: 'Binary Columns'
type: docs
weight: 95
toc: true
---

## Overview

`BINARY(n)` in Tag tables stores fixed-length binary values for sensor frames.
It is rejected in other table types or protocols. Length must be 1~32K-1
(1~32767) bytes. Indexes cannot be created on binary columns.

Machbase SQL supports explicit binary literals when inserting `BINARY` values.

## DDL Rules

```sql
CREATE TAG TABLE t1(
  name VARCHAR(32) PRIMARY KEY,
  time DATETIME BASETIME,
  frame BINARY(4)
);
```

- Valid length: `1 <= n <= 32767` (32K-1).
- Out-of-range sizes cause create-time errors (for example `BINARY(0)`).
- `DESC` and table metadata show the declared byte length (not hex width).
  SQL `LENGTH(binary_col)` returns the displayed value length, excluding trailing
  zero padding added for shorter inputs.

## Supported Input Formats

```sql
X'hex_digits'
x'hex_digits'
B'bit_digits'
b'bit_digits'
O'octal_digits'
o'octal_digits'
```

| Format | Meaning | Unit |
| --- | --- | --- |
| `X'...'`, `x'...'` | Hexadecimal literal | 2 hex digits = 1 byte |
| `B'...'`, `b'...'` | Binary bit literal | 8 bits = 1 byte |
| `O'...'`, `o'...'` | Octal literal | 3 octal digits = 1 byte |

The prefix can be uppercase or lowercase.

```sql
CREATE TAG TABLE t_bin (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_bin VALUES('hex1', '2024-01-01 00:00:00', X'0A');
INSERT INTO t_bin VALUES('hex2', '2024-01-01 00:00:01', x'00010203');
INSERT INTO t_bin VALUES('bit1', '2024-01-01 00:00:02', B'00001010');
INSERT INTO t_bin VALUES('oct1', '2024-01-01 00:00:03', O'012');
```

`X'0A'`, `B'00001010'`, and `O'012'` all represent the same 1-byte value,
`0x0A`.

## Binary Literal Rules

### Hexadecimal Literal

`X'...'` and `x'...'` can contain `0-9`, `A-F`, and `a-f`.

```sql
X'00'
X'0AFF'
x'abcdef'
```

The number of hexadecimal digits must be even. Two hexadecimal digits represent
one byte.

### Bit Literal

`B'...'` and `b'...'` can contain only `0` and `1`.

```sql
B'00000000'  -- 0x00
B'00001010'  -- 0x0A
b'11111111'  -- 0xFF
```

The number of bits must be a multiple of 8. Eight bits represent one byte.

### Octal Literal

`O'...'` and `o'...'` can contain only `0-7`.

```sql
O'000'  -- 0x00
O'012'  -- 0x0A
o'377'  -- 0xFF
```

Octal digits must be grouped in units of three digits. Each 3-digit value must
be in the 1-byte range from `000` to `377`.

### Empty Value

Use empty quotes to represent a zero-length binary value.

```sql
X''
B''
O''
```

## Length Limit

A `BINARY(n)` column accepts at most `n` bytes.

```sql
CREATE TAG TABLE t_limit (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(2)
);

INSERT INTO t_limit VALUES('ok_hex', '2024-01-01 00:00:00', X'0AFF');
INSERT INTO t_limit VALUES('ok_bit', '2024-01-01 00:00:01', B'0000101011111111');
INSERT INTO t_limit VALUES('ok_oct', '2024-01-01 00:00:02', O'012377');

INSERT INTO t_limit VALUES('bad_hex', '2024-01-01 00:00:03', X'000102'); -- fails: 3 bytes
```

If the final binary value exceeds the target `BINARY(n)` length, insertion
fails regardless of the source kind. This applies to binary literals, ordinary
strings, legacy `'0x...'` string input, and `INSERT ... SELECT` from another
`BINARY` column.

```sql
CREATE TAG TABLE t_src (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(8)
);

CREATE TAG TABLE t_dst (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_src VALUES('k1', '2024-01-01 00:00:00', X'0102030405060708');
INSERT INTO t_dst SELECT name, time, value FROM t_src; -- fails: 8 bytes into BINARY(4)
```

The same length rule applies when the binary value is produced inside a SQL
expression such as `CASE`, `INSERT ... SELECT`, or a view.

## Invalid Input

The following inputs are invalid.

```sql
X'0'        -- odd number of hexadecimal digits
X'0G'       -- G is not a hexadecimal digit
B'0101'     -- bit count is not a multiple of 8
B'00000002' -- 2 is not a bit digit
O'12'       -- octal digits are not grouped by 3
O'400'      -- exceeds the 1-byte range
X'0102      -- missing closing quote
```

Invalid values and over-length values fail with the following error.

```text
[ERR-02233: Error occurred at column (n): (Invalid insert value.)]
```

## Difference from Legacy String Input

For compatibility, string input in the form `'0x...'` is still supported.
However, `'0x...'` is a string literal converted into a `BINARY` column, while
`X'...'`, `B'...'`, and `O'...'` explicitly mark the value as a binary literal in
SQL.

Ordinary strings can also be inserted into `BINARY(n)` columns, but insertion
fails if the string byte length exceeds `n`. For new SQL, prefer explicit binary
literals because their meaning is clear.

`'0b...'`, `'0o...'`, unquoted `0x...`, unquoted `0b...`, and unquoted `0o...`
are not supported as binary literal formats.

## Output and Tooling Notes

- machsql displays uppercase hex without the `0x` prefix. Trailing zero padding
  is not shown in the text output for shorter inputs.
- machloader: declare `BINARY(n)` in the schema; invalid values or over-length
  values fail.
- REST append: JSON string is decoded as hex; falls back to the legacy base64
  path only if hex parsing fails.
- CLI/ODBC/Java/C#/Node drivers send/receive fixed-length buffers; metadata
  `LENGTH` is the byte length.
