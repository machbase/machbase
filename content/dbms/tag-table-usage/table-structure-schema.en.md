---
type: docs
title: '5.2 Table Structure and Schema'
weight: 20
toc: true
aliases:
  - /dbms/tag-table-usage/time-distance-axis/
---


<a id="tag-table-design"></a>

## Design a TAG Table

TAG table design determines what constitutes one tag and where each value belongs,
not just how many columns to create.

See [Create, Alter, and Drop](../create-alter-drop/#original-85-creating-tag-tables)
for positional column roles, axis types, and prohibited types. This page covers
decisions within those rules.

The DDL on this page contains independent model examples. Sections explain required
creation order for exercises. Use different names if objects already exist.

Review the following when designing a schema:

- [Use Cases](#tag-schema-use-case-summary)
- [Tag Name Column](#tag-name-column-design)
- [Choose a Time or Distance Axis](#time-axis-design-tag)
- [Value Columns](#tag-table-design-design-column)
- [METADATA Columns](#metadata-column-design-summary)
- [JSON METADATA Columns](#json-metadata-column-design-summary)
- [Binary Columns](#tag-table-design-design-column-binary)
- [VARCHAR Storage Optimization](#tag-table-design-storage-varchar)
- [Storage Strategy](#tag-table-design-strategy)
- [LSL/USL](#tag-table-design-lsl-usl)
- [Correction and Duplicate Policies](#correction-duplication-policy-summary)
- [Constraints and Support](#tag-schema-limitations-summary)

<a id="tag-schema-use-case-summary"></a>

### Use Cases

TAG suits repeated observations with a shared structure across many subjects. Identify
the observed entity, such as a sensor, equipment item, vehicle, or inspection run,
then check whether its history can be queried along time or distance. Decide here
whether to model it as TAG or split it into other table types. See
[Use Cases](../patterns-scenarios/#use-cases-tag) for business models.

<a id="tag-name-column-design"></a>

### Tag Name Column

Decide whether a tag represents a sensor, equipment item, or inspection run. Finer
granularity increases tag counts and metadata/index overhead; coarser granularity
mixes histories of different entities within one tag. Naming conventions are also
covered in [VARCHAR Storage Optimization](#tag-table-design-storage-varchar).

<a id="time-axis-design-tag"></a>

### Choose a Time or Distance Axis

Choose the axis according to the query range: measurement timestamps require a time
axis; cumulative positions along a route require a distance axis. One TAG table
cannot have both. Changing the axis later requires recreating the table.

```sql
-- Time-axis TAG with ranges based on measurement timestamps.
CREATE TAG TABLE time_sensor (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

<a id="distance-axis-design-tag"></a>
<a id="distance-axis-query-range"></a>

```sql
-- Distance-axis TAG with ranges based on distance or position.
CREATE TAG TABLE rail_sensor (
    name     VARCHAR(40) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```

`DURATION`, ROLLUP, and time functions apply only to BASETIME. Use ordinary comparisons
and `BETWEEN` for distance ranges. See [Queries and Analysis](../query-analysis/) for examples.

<a id="tag-table-design-design-column"></a>

### Value Columns

Value columns are ordinary data columns other than the tag name and axis columns.
They store values that change per measurement row, such as readings, status, and quality codes.

#### Supported Types

Common types are listed below. See the [Data Type Reference](/dbms/reference/sql/types/)
for full support, including JSON, BINARY, DECIMAL, and numeric ARRAY.

| Type | Description | Storage size |
|------|------|---------|
| `DOUBLE` | 64-bit floating point | 8 bytes |
| `FLOAT` | 32-bit floating point | 4 bytes |
| `LONG` | 64-bit integer | 8 bytes |
| `INTEGER` (`INT`) | 32-bit integer | 4 bytes |
| `SHORT` | 16-bit integer | 2 bytes |
| `VARCHAR(n)` | Variable-length string | Up to n bytes |

#### Recommended Types

| Data | Recommended type |
|--------|---------|
| Analog values: temperature, humidity, pressure | `DOUBLE` |
| Counters, status codes | `INTEGER` |
| Flags, binary states | `SHORT` |
| Cumulative energy or flow | `DOUBLE` or `LONG` |
| Tag string values | `VARCHAR(n)` |

#### Multiple Value Columns

Storing multiple measurements in one table may introduce NULLs. This model suits
measurements collected at the same time.

```sql
CREATE TAG TABLE weather_station (
    name        VARCHAR(64) PRIMARY KEY,
    time        DATETIME    BASETIME,
    temperature DOUBLE,     -- Always collected
    humidity    DOUBLE,     -- Always collected
    wind_speed  DOUBLE,     -- Optional
    rainfall    DOUBLE      -- Optional
);
```

#### Allow NULL Values

TAG value columns allow NULL by default. If a tag collects only some measurements,
insert NULL into the remaining columns.

```sql
-- Without wind_speed and rainfall
INSERT INTO weather_station VALUES ('WS-01', NOW, 22.5, 65.0, NULL, NULL);
```

<a id="metadata-column-design-summary"></a>

### METADATA Columns

Use METADATA for current per-tag attributes, not values repeated in every DATA row.
Examples include installation location, units, equipment settings, and management
status. Separating DATA and METADATA preserves observation history while allowing
independent queries and changes to current tag attributes. Decide which attributes
belong in METADATA and which remain DATA: values that change per observation belong
in DATA; mostly fixed attributes over a tag lifetime belong in METADATA. See
[Use METADATA](../tag-metadata/#original-85-tag-metadata) for input, query, and update examples.

<a id="json-metadata-column-design-summary"></a>

### JSON METADATA Columns

Consider JSON METADATA for hierarchical or frequently changing attribute sets. For
example, store equipment location, manufacturer details, and installation options
in one JSON document and query selected paths. Choose separate columns for fixed
attributes used frequently in predicates, or JSON when attributes vary by tag.
Consider indexes for frequently filtered paths. See
[JSON METADATA](../tag-metadata/#metadata-design-json) for syntax and examples.

<a id="tag-table-design-design-column-binary"></a>

### Binary Columns

Use `BINARY(n)` in TAG tables for sensor frames of 1–32767 bytes. See
[Binary Columns](#original-85-binary-columns) for input literals, length limits, and
driver behavior. For large images or waveforms, also consider external storage
with only a reference key in the table.

<a id="tag-table-design-storage-varchar"></a>

### VARCHAR Storage Optimization

Declare `VARCHAR` according to the actual maximum length. See the
[DDL Reference](/dbms/reference/sql/syntax/ddl-syntax/) for storage-option syntax.
Combine site, equipment, and sensor identifiers with consistent separators in tag
names to support range queries.

<a id="tag-table-design-strategy"></a>

### Storage Strategy

Data is stored in column storage separated by tag. Choose a strategy based on volume and query patterns.

#### One Table or Multiple Tables

##### One TAG Table (Recommended)

Group sensors of the same kind in one TAG table.

```sql
-- Recommended: all temperature sensors in one table
CREATE TAG TABLE temperature_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

**Benefits**
- Fewer objects to manage
- Easier cross-tag aggregation
- Simpler operations

##### Multiple TAG Tables

Consider separate tables for different column layouts, retention periods, privileges,
or operational cycles. Do not create one table per sensor merely because sensor
counts increase.

```sql
-- Temperature/humidity sensors (DOUBLE values)
CREATE TAG TABLE thermo_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    temp  DOUBLE,
    humid DOUBLE
);

-- Vibration sensors (DOUBLE + BINARY waveform)
CREATE TAG TABLE vibration_sensor (
    name     VARCHAR(64) PRIMARY KEY,
    time     DATETIME    BASETIME,
    rms      DOUBLE,
    waveform BINARY(4096)
);
```

#### Manage Tag Counts

- Measure tag-index and metadata memory growth with production-scale data.
- Encode sensor hierarchies in tag names.
- Avoid designs where every record has a unique tag name (an antipattern).

#### Partition Strategy

Limit time-axis TAG queries by `BASETIME`. Do not depend on internal storage objects
or partition names. Manage retention through
[Data Retention Policies](/dbms/operations-configuration-recovery/policy-data-retention/).

<a id="tag-table-design-lsl-usl"></a>
<a id="original-85-lsl-usl-limits"></a>

### LSL and USL

LSL (Lower Specification Limit) and USL (Upper Specification Limit) define acceptable
value bounds. Setting per-tag bounds in METADATA can reject out-of-range DATA input,
allowing different ingestion quality rules for each tag.

This feature rejects input; it does not correct values. Log and reprocess rejected
input according to the ingestion error policy.

#### Constraints

The following constraints apply:

* LSL/USL is not entirely unsupported in Cluster. Limit definitions at table creation,
  metadata values, and DATA INSERT/Append limit checks use common paths. The exercise
  below that adds limit columns to existing METADATA with ALTER is for Standard Edition.
* The third TAG column, __Value__, must be __SUMMARIZED__ to configure LSL/USL.
* LSL must be less than or equal to USL. Input __Value__ must be within the inclusive
  bounds: __(LSL <= Value <= USL)__.
* Data inserted before limits are configured is not validated.
* NULL LSL/USL columns disable the corresponding input validation.
* Limits can be used independently; configure only USL for an upper bound.
* USL alone checks only upper-bound violations; LSL alone checks only lower-bound violations.

#### Supported Data Types

Limit columns must have the same type as the target __Value__ column. The following
covers bounds for basic numeric types. SUMMARIZED itself also supports JSON, so
SUMMARIZED eligibility and numeric limit configuration are separate requirements.

| Type | Description | Range | Significant digits |
|----|------|-----|----|
| short | Signed 16-bit integer | -32767 ~ 32767 | - |
| ushort | Unsigned 16-bit integer | 0 ~ 65534 | - |
| integer | Signed 32-bit integer | -2147483647 ~ 2147483647 | - |
| uinteger | Unsigned 32-bit integer | 0 ~ 4294967294 | - |
| long | Signed 64-bit integer | -9223372036854775807 ~ 9223372036854775807 | - |
| ulong | Unsigned 64-bit integer | 0~18446744073709551614 | - |
| float | 32-bit floating point | - | 6[^1] |
| double | 64-bit floating point | - | 15[^1] |

#### Configure and Use LSL/USL

The CREATE examples show independent alternatives. Only the base `example` table is
used in subsequent INSERT/UPDATE exercises; create alternatives separately.

Specify `LOWER LIMIT` (LSL) or `UPPER LIMIT` (USL) on tag metadata columns, either when
creating the TAG table or adding metadata columns.

##### CREATE

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

Use both limit columns or only one. LSL alone checks `Value >= LSL` without an upper
bound, equivalent to a NULL USL value.

```sql
CREATE TAG TABLE example_lower_only (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl    INTEGER LOWER LIMIT
);
```

##### ADD COLUMN

When added with `ADD COLUMN` after data already exists, the default is __NULL__.

```sql
CREATE TAG TABLE example_alter_limits (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE example_alter_limits METADATA ADD COLUMN (lsl INTEGER LOWER LIMIT);
ALTER TABLE example_alter_limits METADATA ADD COLUMN (usl INTEGER UPPER LIMIT);
```

As with [CREATE](#create), you can add only one limit attribute.

```sql
CREATE TAG TABLE example_alter_upper (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE example_alter_upper METADATA ADD COLUMN (usl INTEGER UPPER LIMIT);
```

##### INSERT

Set LSL/USL values for a specific TAG ID.

```sql
INSERT INTO example metadata VALUES ('TAG_01', 100, 200);
```

Subsequent tag data input behaves as follows:

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 95);  -- Failure
```

```text
[ERR-02342: SUMMARIZED value is less than LOWER LIMIT.]
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 100); -- Success (Inclusive)
```

```text
1 row(s) inserted.
Elapsed time: 0.000
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 150); -- Success
```

```text
1 row(s) inserted.
Elapsed time: 0.000
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 200); -- Success (Inclusive)
```

```text
1 row(s) inserted.
Elapsed time: 0.000
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 205); -- Failure
```

```text
[ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]
```

Querying the TAG table shows that only values within the specification range were inserted.

```sql
SELECT * FROM example;
```

```text
TAG_ID                                              TIME                            VALUE       LSL         USL
------------------------------------------------------------------------------------------------------------------------------
TAG_01                                              2023-09-12 09:31:27 923:289:631 100         100         200
TAG_01                                              2023-09-12 09:31:27 929:013:232 150         100         200
TAG_01                                              2023-09-12 09:31:27 939:209:248 200         100         200
[3] row(s) selected.
Elapsed time: 0.001
```

##### UPDATE

Update LSL/USL column values. These changes do not apply retroactively to existing data.

```sql
UPDATE example metadata SET lsl = 10, usl = 100 WHERE tag_id = 'TAG_01';
```

```text
1 row(s) updated.
Elapsed time: 0.001
```

```sql
SELECT tag_id, lsl, usl FROM example METADATA;
```

```text
TAG_ID                                              LSL         USL
----------------------------------------------------------------------------------------
TAG_01                                              10          100
[1] row(s) selected.
Elapsed time: 0.001
```

##### DELETE

Disable LSL/USL constraints by setting their values to NULL, not by using `DROP COLUMN`.

```sql
UPDATE EXAMPLE METADATA SET lsl = NULL, usl = NULL WHERE tag_id = 'TAG_01';
```

```text
1 row(s) updated.
Elapsed time: 0.001
```

```sql
SELECT tag_id, lsl, usl FROM example METADATA;
```

```text
TAG_ID                                              LSL         USL
----------------------------------------------------------------------------------------
TAG_01                                              NULL        NULL
[1] row(s) selected.
Elapsed time: 0.001
```

#### Check LSL/USL Violations in TRACE Logs
- Location: `$MACHBASE_HOME/trc/machbase.trc`
- Quick filter:
  ```bash
  grep LIMIT_DROP $MACHBASE_HOME/trc/machbase.trc | tail -n 20
  ```
- Log format: `LIMIT_DROP (TYPE=<UPPER|LOWER>) TABLE=<table-name> TAG=<tag name> <column=value ...>`
  - TYPE=LOWER/UPPER identifies the violated bound.
  - DATETIME uses `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`.
- Actual examples:
  ```
  [2025-11-29 13:50:34 P-151395 T-126343511537344][QP-INFO] LIMIT_DROP (TYPE=LOWER) TABLE=TAG3 TAG=tag-1  TIME=2020-01-01 00:00:00 000:000:000 VALUE=5.55
  [2025-11-29 13:50:34 P-151395 T-126343511537344][QP-INFO] LIMIT_DROP (TYPE=UPPER) TABLE=TAG3 TAG=tag-1  TIME=2020-01-01 00:00:04 000:000:000 VALUE=30.55
  [2025-11-29 13:50:35 P-151395 T-126344475694784][QP-INFO] LIMIT_DROP (TYPE=LOWER) TABLE=TAG3 TAG=tag-2  TIME=1998-12-24 09:00:00 000:000:000 VALUE=0
  [2025-11-29 13:50:35 P-151395 T-126344475694784][QP-INFO] LIMIT_DROP (TYPE=UPPER) TABLE=TAG3 TAG=tag-2  TIME=1998-12-24 09:00:00 000:000:008 VALUE=45
  ```
- Usage
  - Identify LOWER/UPPER violation times and values by tag.
  - Filter further by TAG/table name with grep to trace specific targets.
- Caution: Lines are limited to about 4KB and may truncate with many columns. Immediately after startup, before the metadata cache is ready, table names may appear as IDs.

[^1]: [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754)

<a id="correction-duplication-policy-summary"></a>
<a id="tag-table-design-duplication-removal"></a>

### Correction and Duplicate Policies

Value correction and deduplication require decisions beyond column definitions, but
should be planned during schema design. Decide which value columns can change,
whether to preserve originals in separate columns or tables, and how to rebuild
ROLLUP after correction. DATA UPDATE is Standard Edition only; in Cluster, design
reingestion and reaggregation procedures. See
[Data Correction](../tag-data-update-correction/#design-correction-tag).

If the same tag/axis value can be inserted repeatedly, decide whether to allow
duplicates, remove them during collection, or use Machbase automatic deduplication.
See [Automatic Deduplication](../operations-lifecycle/#original-85-duplication-removal)
for configuration and operational validation.

<a id="tag-schema-limitations-summary"></a>

### Constraints and Support

TAG tables are designed for repeated observations and do not support every SQL
feature of ordinary relational tables. Check axis, METADATA, correction, ROLLUP, and
Edition support before implementation. Verify that the design fits the supported
scope and revisit affected decisions if needed. See
[Constraints and Precautions](../constraints-errors-troubleshooting/#limitations-tag)
for unsupported features and common errors.

<a id="original-85-binary-columns"></a>

## Binary Columns


`BINARY(n)` stores fixed-length sensor-frame binary values in TAG tables. TAG
`BINARY` without a length uses 32767 bytes. Specify the required frame size to make
storage and transmission size clear. The length-qualified `BINARY(n)` form cannot
be declared in other table types. Valid lengths are 1–32K-1 (1–32767) bytes.
Binary columns cannot be indexed.

Insert `BINARY` values with explicit binary literals.

### DDL Rules

```sql
CREATE TAG TABLE t1(
  name VARCHAR(32) PRIMARY KEY,
  time DATETIME BASETIME,
  frame BINARY(4)
);
```

- Valid length: `1 <= n <= 32767` (32K-1).
- Out-of-range lengths, such as `BINARY(0)`, fail at creation.
- `DESC` and table metadata show declared byte length, not hexadecimal width.
  SQL `LENGTH(binary_col)` returns the displayed value length excluding trailing
  zero padding added to short input.

### Supported Input Formats

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
| `X'...'`, `x'...'` | Hexadecimal literal | 2 hexadecimal digits = 1 byte |
| `B'...'`, `b'...'` | Binary literal | 8 bits = 1 byte |
| `O'...'`, `o'...'` | Octal literal | 3 octal digits = 1 byte |

Prefixes are case-insensitive.

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

`X'0A'`, `B'00001010'`, and `O'012'` all represent the one-byte value `0x0A`.

### Binary Literal Rules

#### Hexadecimal Literals

`X'...'` and `x'...'` accept `0-9`, `A-F`, and `a-f`.

```sql
X'00'
X'0AFF'
x'abcdef'
```

Hexadecimal literals require an even number of digits; two digits represent one byte.

#### Binary Literals

`B'...'` and `b'...'` accept only `0` and `1`.

```sql
B'00000000'  -- 0x00
B'00001010'  -- 0x0A
b'11111111'  -- 0xFF
```

The bit count must be a multiple of 8; eight bits represent one byte.

#### Octal Literals

`O'...'` and `o'...'` accept only `0-7`.

```sql
O'000'  -- 0x00
O'012'  -- 0x0A
o'377'  -- 0xFF
```

Octal digits must occur in groups of three. Each group must be in the one-byte
range `000` through `377`.

#### Empty Values

Empty single quotes represent a zero-length binary value.

```sql
X''
B''
O''
```

### Length Limits

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

INSERT INTO t_limit VALUES('bad_hex', '2024-01-01 00:00:03', X'000102'); -- Fails: 3 bytes
```

Input fails whenever the final binary value exceeds the target `BINARY(n)` length,
regardless of source. This applies to binary literals, ordinary strings, legacy
`'0x...'` string input, and copying other `BINARY` columns through `INSERT ... SELECT`.

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
INSERT INTO t_dst SELECT name, time, value FROM t_src; -- Fails: 8-byte value into BINARY(4)
```

The same length check applies to values produced inside SQL expressions, including
`CASE`, `INSERT ... SELECT`, and views.

### Invalid Input

The following inputs are invalid:

```sql
X'0'        -- Odd number of hexadecimal digits
X'0G'       -- G is not a hexadecimal digit
B'0101'     -- Bit count is not a multiple of 8
B'00000002' -- 2 is not a binary digit
O'12'       -- Octal digits are not in groups of three
O'400'      -- Exceeds one-byte range
X'0102      -- Missing closing single quote
```

Invalid values or excessive lengths fail with this error:

```text
[ERR-02233: Error occurred at column (n): (Invalid insert value.)]
```

### Differences from Legacy String Input

String input in the form `'0x...'` remains available for compatibility. It converts
a string to `BINARY`; `X'...'`, `B'...'`, and `O'...'` explicitly identify binary
values as SQL binary literals.

Ordinary strings can also be inserted into `BINARY(n)`, but fail if their byte
length exceeds `n`. Prefer explicit binary literals in new SQL for clarity.

`'0b...'`, `'0o...'`, and unquoted `0x...`, `0b...`, `0o...` are not supported
as binary literals.

### Output and Tools

- machsql displays uppercase hexadecimal without `0x`. Trailing zero padding added
  to short input is omitted from text output.
- machloader: Declare `BINARY(n)` in the schema; invalid or oversized values fail.
- Machbase SQLCLI, ODBC, Java, C#, and Node.js drivers send/receive fixed-length
  buffers; metadata `LENGTH` is in bytes.

## Clean Up Examples

Drop only tables actually created on this page. If you did not execute an
alternative DDL statement, do not run its DROP statement.

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
