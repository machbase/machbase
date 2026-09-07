---
title: '5.2 Table Structure and Schema'
weight: 20
toc: true
aliases:
  - /dbms/tag-table-usage/time-distance-axis/
---

TAG names identify recurring subjects, while DATA rows record individual observations. Declare
the VARCHAR tag name first, the time/distance axis second, and an optional SUMMARIZED column third.
SUMMARIZED supports the numeric types and JSON accepted by TAG validation; ARRAY cannot be the
name, axis, or summarized column.

Each model below is an independent example. Use unused names and execute only the chosen
alternatives. Dependent INSERT/UPDATE steps are identified within their sections.

<a id="tag-table-design"></a>

## TAG Table Design

<a id="time-axis-design-tag"></a>

### Time and Distance Axes

Use DATETIME BASETIME for observation timestamps.

```sql
CREATE TAG TABLE time_sensor (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```


<a id="distance-axis-design-tag"></a>
<a id="distance-axis-query-range"></a>

Use DOUBLE, LONG, or ULONG BASEDISTANCE when position or distance is the main query axis.

```sql
CREATE TAG TABLE rail_sensor (
    name     VARCHAR(40) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```


A table cannot have both special axes. Use numeric comparisons for distance ranges.
Time-axis-only operations such as time ROLLUP must not be applied to distance values.
See [Queries](../query-analysis/) for examples.

<a id="tag-table-design-design-column"></a>

### Data Columns and NULL

Data columns exclude the name and axis and contain observations, status, and quality values.
Consider FLOAT/DOUBLE for approximate measurements, appropriate integer ranges for counters and
codes, DECIMAL for exact decimal values, JSON for structured attributes, and numeric ARRAY for
fixed-size numeric groups. Confirm table-specific restrictions in the
[Type Reference](../../reference/sql/type-data-types-dictionary/).

A multi-value row should describe one observation. Missing optional values can be NULL.

```sql
CREATE TAG TABLE weather_station (
    name        VARCHAR(64) PRIMARY KEY,
    time        DATETIME    BASETIME,
    temperature DOUBLE,     -- Required by this collection model
    humidity    DOUBLE,     -- Required by this collection model
    wind_speed  DOUBLE,     -- Optional
    rainfall    DOUBLE      -- Optional
);
```

```sql
-- Missing wind_speed and rainfall
INSERT INTO weather_station VALUES ('WS-01', NOW, 22.5, 65.0, NULL, NULL);
```


Define units and quality rules; missing input, numeric zero, and a row containing NULL are not
the same. Independent channel timestamps may call for separate series.

<a id="tag-table-design-design-column-binary"></a>

### Binary Data Design

BINARY(n) stores fixed-size frames of 1–32767 bytes. See the detailed binary section below.
Consider external storage plus a reference key when objects exceed the supported size.

<a id="tag-table-design-storage-varchar"></a>

### VARCHAR Design

Choose lengths from actual byte requirements, including the encoding of names and values.
Use consistent names for subjects, but do not assume that a hierarchy separator automatically
creates range-index semantics. Test real predicates and plans.

<a id="tag-table-design-strategy"></a>

### One Table or Several Tables

Group sensors with compatible schemas and operational requirements rather than making a table
for each sensor.

```sql
-- Group compatible temperature sensors in one table
CREATE TAG TABLE temperature_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

```sql
-- Temperature and humidity (DOUBLE values)
CREATE TAG TABLE thermo_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    temp  DOUBLE,
    humid DOUBLE
);

-- Vibration (DOUBLE plus a BINARY waveform)
CREATE TAG TABLE vibration_sensor (
    name     VARCHAR(64) PRIMARY KEY,
    time     DATETIME    BASETIME,
    rms      DOUBLE,
    waveform BINARY(4096)
);
```


Separate tables when schemas, retention, privileges, or operational lifecycles differ.
Measure tag metadata memory as the tag population grows. Do not depend on internal partition
names; select tag/axis ranges and use supported retention policies.

<a id="tag-table-design-duplication-removal"></a>

### Duplicate Removal

Configure, observe, and verify duplicate handling through
[Operations](../operations-lifecycle/#original-85-duplication-removal). A duplicate-check duration
is not a replacement for business identity or a guarantee of synchronous rejection.

<a id="tag-table-design-lsl-usl"></a>
<a id="original-85-lsl-usl-limits"></a>

## LSL and USL Input Limits

LOWER LIMIT and UPPER LIMIT metadata define per-tag input bounds. Out-of-range input is rejected;
this does not automatically correct bad values.

Do not describe all LSL/USL functionality as unavailable in Cluster. Declaring limits at table
creation, setting metadata values, and checking DATA INSERT/Append use common paths. The ALTER
exercises below are Standard Edition operations.

Limits must match the third SUMMARIZED column's type. The documented basic numeric types are
SHORT, USHORT, INTEGER, UINTEGER, LONG, ULONG, FLOAT, and DOUBLE. Keep reserved NULL boundary values
out of ordinary numeric data. LSL must not exceed USL; valid values include both boundaries.
A NULL lower or upper limit disables that side. Changing limits does not retroactively validate
previously stored rows.

### Declare Limits

The first table is used by the subsequent input and update exercise. The second is an alternative
with only a lower limit.

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl     INTEGER LOWER LIMIT,
    usl     INTEGER UPPER LIMIT
);
```

```sql
CREATE TAG TABLE example_lower_only (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl    INTEGER LOWER LIMIT
);
```


### Add Limits to Existing Metadata

The following alternatives use Standard Edition. Existing rows initially have NULL limits.

```sql
CREATE TAG TABLE example_alter_limits (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE example_alter_limits METADATA ADD COLUMN (lsl INTEGER LOWER LIMIT);
ALTER TABLE example_alter_limits METADATA ADD COLUMN (usl INTEGER UPPER LIMIT);
```

```sql
CREATE TAG TABLE example_alter_upper (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE example_alter_upper METADATA ADD COLUMN (usl INTEGER UPPER LIMIT);
```


### Set Bounds and Check Input

```sql
INSERT INTO example metadata VALUES ('TAG_01', 100, 200);
```


Run the invalid inputs separately from the successful ones. Values 95 and 205 fail; 100, 150,
and 200 are within the inclusive range.

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 95);  -- Failure
```

```text
[ERR-02342: SUMMARIZED value is less than LOWER LIMIT.]
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 100); -- Success (Inclusive)
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 150); -- Success
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 200); -- Success (Inclusive)
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 205); -- Failure
```

```text
[ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]
```

```sql
SELECT * FROM example;
```


The table contains three valid rows with values 100, 150, and 200. Their NOW timestamps depend
on execution time, not the historical timestamps in example terminal captures.

### Update or Disable Limits

```sql
UPDATE example metadata SET lsl = 10, usl = 100 WHERE tag_id = 'TAG_01';
```

```sql
SELECT tag_id, lsl, usl FROM example METADATA;
```


The metadata query returns lower 10 and upper 100. Existing observations are not revalidated.
Set both limits to NULL to disable checks for this tag rather than using DROP COLUMN as a
constraint-toggle operation.

```sql
UPDATE EXAMPLE METADATA SET lsl = NULL, usl = NULL WHERE tag_id = 'TAG_01';
```

```sql
SELECT tag_id, lsl, usl FROM example METADATA;
```


### Diagnose Rejected Input

Inspect LIMIT_DROP entries in the server trace and correlate them with the input error or SDK
failure count. The log identifies the bound, table, tag, and available column values.

```bash
  grep LIMIT_DROP $MACHBASE_HOME/trc/machbase.trc | tail -n 20
```


Long records can be truncated in trace output; retain application-side context for diagnosis.

<a id="original-85-binary-columns"></a>

## TAG Binary Columns

TAG BINARY(n) accepts lengths 1–32767. Omitting n from TAG BINARY selects 32767 bytes, so specify
the frame size when possible. Length-qualified BINARY(n) declarations are TAG-specific; other
table types have their own binary rules. BINARY cannot be indexed in this TAG use.

```sql
CREATE TAG TABLE t1(
  name VARCHAR(32) PRIMARY KEY,
  time DATETIME BASETIME,
  frame BINARY(4)
);
```


DESC and column metadata report the declared byte length, not hexadecimal width.
LENGTH and text display omit trailing zero padding from short inputs; typed driver buffers use
the declared fixed-size representation.

### Literal Forms

Prefixes are case-insensitive. These are expression templates, not standalone statements.

```sql
X'hex_digits'
x'hex_digits'
B'bit_digits'
b'bit_digits'
O'octal_digits'
o'octal_digits'
```


| Form | Unit and restriction |
|---|---|
| X'...' | Two hexadecimal digits per byte; even digit count |
| B'...' | Eight binary digits per byte; length divisible by eight |
| O'...' | Three octal digits per byte; each group 000–377 |

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


X'0A', B'00001010', and O'012' all represent byte 0x0A.

### Hexadecimal, Binary, and Octal Values

These are literal expressions that can be used in input SQL.

```sql
X'00'
X'0AFF'
x'abcdef'
```

```sql
B'00000000'  -- 0x00
B'00001010'  -- 0x0A
b'11111111'  -- 0xFF
```

```sql
O'000'  -- 0x00
O'012'  -- 0x0A
o'377'  -- 0xFF
```


### Empty Values

Empty literals represent zero-length input.

```sql
X''
B''
O''
```


### Length Checks

The final value cannot exceed the declared size. Run the bad_hex INSERT as an intentional error
after the three successful statements.

```sql
CREATE TAG TABLE t_limit (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(2)
);

INSERT INTO t_limit VALUES('ok_hex', '2024-01-01 00:00:00', X'0AFF');
INSERT INTO t_limit VALUES('ok_bit', '2024-01-01 00:00:01', B'0000101011111111');
INSERT INTO t_limit VALUES('ok_oct', '2024-01-01 00:00:02', O'012377');

INSERT INTO t_limit VALUES('bad_hex', '2024-01-01 00:00:03', X'000102'); -- Expected failure: three bytes
```


The same limit applies to INSERT SELECT and expressions, not only literals.

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
INSERT INTO t_dst SELECT name, time, value FROM t_src; -- Expected failure: eight bytes cannot fit BINARY(4)
```


The final INSERT fails because an eight-byte source does not fit BINARY(4). CASE and views do not
remove the destination's size constraint.

### Invalid Input

The following literals are intentionally invalid. They illustrate bad digits, invalid grouping,
out-of-byte-range octal values, and an unclosed quote.

```sql
X'0'        -- Odd number of hex digits
X'0G'       -- G is not a hexadecimal digit
B'0101'     -- Bit count is not divisible by eight
B'00000002' -- 2 is not a binary digit
O'12'       -- Octal digits are not grouped in threes
O'400'      -- Outside the one-byte range
X'0102      -- Missing closing quote
```

```text
[ERR-02233: Error occurred at column (n): (Invalid insert value.)]
```


### String Compatibility and Output

Legacy '0x...' strings can still be converted into BINARY; X/B/O literals express binary values
directly. Ordinary strings must fit by byte length. '0b...', '0o...', and unquoted 0x/0b/0o forms
are not SQL binary literals.

machsql displays uppercase hexadecimal without the 0x prefix and omits trailing zero padding.
machloader and SDKs must respect the declared size and their version-specific binary APIs.

## Cleanup

Remove only tables actually created for the selected exercises. Skip alternatives you did not run.

```sql
DROP TABLE time_sensor;
DROP TABLE rail_sensor;
DROP TABLE weather_station;
DROP TABLE temperature_sensor;
DROP TABLE thermo_sensor;
DROP TABLE vibration_sensor;
DROP TABLE example;
DROP TABLE example_lower_only;
DROP TABLE example_alter_limits;
DROP TABLE example_alter_upper;
DROP TABLE t1;
DROP TABLE t_bin;
DROP TABLE t_limit;
DROP TABLE t_dst;
DROP TABLE t_src;
```
