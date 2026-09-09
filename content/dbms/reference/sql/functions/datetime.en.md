---
type: docs
title: 'Date/Time Functions'
weight: 50
toc: true
---

Machbase DATETIME internally stores nanoseconds elapsed since 1970-01-01 00:00:00 UTC. Date/time
functions convert these values to readable formats or perform arithmetic.

## Quick Reference

| Function | Syntax | Description |
|------|------|------|
| SYSDATE / NOW | `SYSDATE`, `NOW` | Return current system time |
| TO_DATE | `TO_DATE(str [, fmt])` | Convert a string to DATETIME |
| TO_DATE_SAFE | `TO_DATE_SAFE(str [, fmt])` | Return NULL on conversion failure |
| TO_CHAR | `TO_CHAR(col [, fmt])` | Convert DATETIME to a string |
| ADD_TIME | `ADD_TIME(col, diff)` | Add/subtract date/time components |
| DATE_TRUNC | `DATE_TRUNC(unit, col [, count])` | Truncate to the specified unit |
| DATE_BIN | `DATE_BIN(unit, count, col [, origin])` | Bucket time relative to a specified origin |
| DAYOFWEEK | `DAYOFWEEK(col)` | Return weekday number (0=Sunday) |
| YEAR / MONTH / DAY | `YEAR(col)`, `MONTH(col)`, `DAY(col)` | Extract year, month, and day |
| FROM_UNIXTIME | `FROM_UNIXTIME(unix_ts)` | Convert a 32-bit Unix timestamp to DATETIME |
| UNIX_TIMESTAMP | `UNIX_TIMESTAMP(col)` | Convert DATETIME to a 32-bit Unix timestamp |
| FROM_TIMESTAMP | `FROM_TIMESTAMP(ns)` | Convert nanosecond integer to DATETIME |
| TO_TIMESTAMP | `TO_TIMESTAMP(col)` | Convert DATETIME to nanosecond integer |

---

## SYSDATE / NOW

Pseudocolumns that return current system time. SYSDATE and NOW return the same value.

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

---

## TO_DATE

Converts a string to DATETIME using the specified format. The default format is
`YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`.

```sql
TO_DATE(date_string [, format_string])
```

```sql
Mach> SELECT TO_DATE('2014-12-30 11:22:33 444:555:666');
2014-12-30 11:22:33 444:555:666

Mach> SELECT TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS');
1999-12-31 13:12:32 000:000:000

Mach> SELECT TO_DATE('1999', 'YYYY');
1999-01-01 00:00:00 000:000:000
```

`TO_DATE_SAFE()` returns NULL instead of an error when conversion fails.

```sql
Mach> SELECT TO_DATE_SAFE('2016-12-32', 'YYYY-MM-DD');
NULL
```

---

## TO_CHAR (DATETIME)

Converts a DATETIME column value to a string. The default format is `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`.

```sql
TO_CHAR(datetime_col [, format_string])
```

### Format Strings

| Format | Description |
|------------|------|
| `YYYY` | Four-digit year |
| `YY` | Two-digit year |
| `MM` | Two-digit month (`01~12`) |
| `MON` | Three-letter English month abbreviation (JAN, FEB, ...) |
| `DD` | Two-digit day |
| `DAY` | Three-letter English weekday abbreviation (SUN, MON, ...) |
| `IW` | ISO 8601 week (`1~53`, Monday-based) |
| `WW` | Week of year (`1~53`, independent of weekday) |
| `W` | Week of month (`1~5`, independent of weekday) |
| `HH` | Two-digit hour |
| `HH12` | 12-hour clock (`1~12`) |
| `HH24` | 24-hour clock (`0~23`) |
| `HH2`, `HH3`, `HH6` | Truncate hours to the specified multiple |
| `MI` | Two-digit minute |
| `MI2`, `MI5`, `MI10`, `MI20`, `MI30` | Truncate minutes to the specified multiple |
| `SS` | Two-digit second |
| `SS2`, `SS5`, `SS10`, `SS20`, `SS30` | Truncate seconds to the specified multiple |
| `AM` | AM/PM |
| `mmm` | Three-digit milliseconds (`0~999`) |
| `uuu` | Three-digit microseconds (`0~999`) |
| `nnn` | Three-digit nanoseconds (`0~999`) |

```sql
Mach> SELECT TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS') FROM datetime_table;
2014-12-30 11:22:33
2013-11-11 01:02:03

Mach> SELECT TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.uuu.nnn') FROM datetime_table;
2014-12-30 11:22:33 444.555.666
```

---

## ADD_TIME

Adds or subtracts years, months, days, hours, minutes, and seconds from DATETIME. Milliseconds,
microseconds, and nanoseconds are not supported.

```sql
ADD_TIME(column, time_diff_format)
```

`time_diff_format`: `"Year/Month/Day Hour:Minute:Second"`; each component can be positive or negative.

```sql
-- One year later
Mach> SELECT ADD_TIME(dt, '1/0/0 0:0:0') FROM t;

-- One hour, one minute, and one second later
Mach> SELECT ADD_TIME(dt, '0/0/0 1:1:1') FROM t;

-- One year, one month, and one day earlier
Mach> SELECT ADD_TIME(dt, '-1/-1/-1 0:0:0') FROM t;
```

---

## DATE_TRUNC

Truncates a DATETIME value to the specified unit. With `count`, truncates to that multiple of the unit.

```sql
DATE_TRUNC(field, date_val [, count])
```

### Supported Units and Maximum Ranges

| Unit | Maximum Range |
|-----------|----------|
| `nanosecond` (`nsec`) | 1,000,000,000 (1 second) |
| `microsecond` (`usec`) | 60,000,000 (60 seconds) |
| `millisecond` (`msec`) | 60,000 (60 seconds) |
| `second` (`sec`) | 86,400 (1 day) |
| `minute` (`min`) | 1,440 (1 day) |
| `hour` | 24 (1 day) |
| `day` | 1 |
| `week` | 1 (starts on Sunday) |
| `month` | 1 |
| `year` | 1 |

```sql
-- Truncate to seconds
Mach> SELECT COUNT(*), DATE_TRUNC('second', i2) tm FROM t GROUP BY tm ORDER BY 2;

-- Truncate to 2-second intervals
Mach> SELECT COUNT(*), DATE_TRUNC('second', i2, 2) tm FROM t GROUP BY tm ORDER BY 2;

-- Truncate to 2-minute intervals (same as DATE_TRUNC('second', time, 120))
Mach> SELECT COUNT(*), DATE_TRUNC('minute', ts, 2) tm FROM t GROUP BY tm;
```

---

## DATE_BIN

Buckets DATETIME by the specified unit and count relative to `origin`. If omitted, origin is
`1970-01-01 00:00:00` in the local timezone.

```sql
DATE_BIN(field, count, source [, origin])
```

```sql
-- 2-hour buckets with a specific origin
SELECT DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00')) FROM log ORDER BY time;

-- 3-hour buckets aligned to the local timezone
SELECT DATE_BIN('hour', 3, ts) FROM t ORDER BY ts;
```

---

## DAYOFWEEK

Returns the weekday of a DATETIME value as an integer.

```sql
DAYOFWEEK(date_val)
```

| Return Value | Weekday |
|--------|------|
| 0 | Sunday |
| 1 | Monday |
| 2 | Tuesday |
| 3 | Wednesday |
| 4 | Thursday |
| 5 | Friday |
| 6 | Saturday |

```sql
SELECT DAYOFWEEK(dt) FROM log_table;
```

---

## YEAR / MONTH / DAY

Extracts year, month, and day from DATETIME as integers.

```sql
YEAR(datetime_col)
MONTH(datetime_col)
DAY(datetime_col)
```

```sql
Mach> SELECT YEAR(c1), MONTH(c1), DAY(c1) FROM extract_table;
year(c1)    month(c1)   day(c1)
---------------------------------
2001        1           1
```

---

## FROM_UNIXTIME / UNIX_TIMESTAMP

FROM_UNIXTIME converts a 32-bit Unix timestamp integer to DATETIME. UNIX_TIMESTAMP converts DATETIME
to a 32-bit Unix timestamp.

```sql
FROM_UNIXTIME(unix_timestamp_value)
UNIX_TIMESTAMP(datetime_value)
```

```sql
Mach> SELECT FROM_UNIXTIME(315540671);
1980-01-01 11:11:11 000:000:000

Mach> INSERT INTO unix_table VALUES (UNIX_TIMESTAMP('2001-01-01'));
Mach> SELECT * FROM unix_table;
C1
-----------
978274800
```

---

## FROM_TIMESTAMP / TO_TIMESTAMP

FROM_TIMESTAMP converts an integer count of nanoseconds since 1970-01-01 00:00:00 UTC to DATETIME.
TO_TIMESTAMP converts DATETIME to nanoseconds elapsed since the same epoch.

The epoch appears as 1970-01-01 09:00:00 in UTC+09:00.
Dates and times in the examples below use UTC+09:00.

```sql
FROM_TIMESTAMP(nanosecond_time_value)
TO_TIMESTAMP(datetime_value)
```

```sql
Mach> SELECT FROM_TIMESTAMP(1562302560007248869);
2019-07-05 13:56:00 007:248:869

Mach> SELECT TO_TIMESTAMP(c1) FROM datetime_tbl;
to_timestamp(c1)
-----------------------
1262308210000000000
```

Nanosecond arithmetic example:

```sql
-- 1ms (1,000,000 ns) before the current time
SELECT FROM_TIMESTAMP(SYSDATE - 1000000) FROM t;
```
