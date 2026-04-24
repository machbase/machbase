---
title : 'Functions'
type: docs
weight: 70
tocSort: true
---

## Error Handling

|Error Type|Code|When it occurs|
|---|---|---|
|Argument type error|`ERR-02036`, `ERR-02037`|A non-numeric value is passed, or an argument is passed to `PI`|
|Runtime error|`ERR-02317`|Negative input to `SQRT`, division by zero in `MOD`, invalid base/value in `LOG`, overflow in `EXP`/`POWER`, and similar cases|

If the input is `NULL`, the result is also `NULL`.

## ABS

This function works on a numeric column, converts it to a positive value, and returns the value as a real number.

```sql
ABS(column_expr)
```

```sql
Mach> CREATE TABLE abs_table (c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
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

This function performs a date and time operation on a given datetime column. Supports increment/decrement operations up to year, month, day, hour, minute, and second, and does not support operations on milli, micro, and nanoseconds. The Diff format is: "Year/Month/Day Hour:Minute:Second". Each item has a positive or negative value.

```sql
ADD_TIME(column,time_diff_format)
```

```sql
Mach> CREATE TABLE add_time_table (id INTEGER, dt DATETIME);
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

These aggregate functions estimate percentiles while keeping a bounded summary instead of sorting every raw value. They are useful when the input is very large and a small approximation error is acceptable.

```sql
APPROX_PERCENTILE(value, ratio)
APPROX_MEDIAN(value)
APPROX_P05(value)
APPROX_P10(value)
APPROX_P90(value)
APPROX_P95(value)
```

- `value` must be numeric.
- `ratio` must be a constant in the range `0.0` to `1.0`.
- Return type is `DOUBLE`.
- `NULL` values are ignored.

`APPROX_MEDIAN(value)` is an approximate 50th percentile. `APPROX_P05`, `APPROX_P10`, `APPROX_P90`, and `APPROX_P95` are convenience forms for fixed percentile points.

```sql
SELECT APPROX_PERCENTILE(latency_ms, 0.95) AS ap95,
       APPROX_MEDIAN(latency_ms) AS amedian,
       APPROX_P05(latency_ms) AS ap05
FROM api_log;
```


## AREA {#area}

`AREA(y, x)` is an exact aggregate function that calculates the area under a curve formed by `(x, y)` pairs.

```sql
AREA(y, x)
```

- Both arguments must be numeric.
- The function ignores rows where either argument is `NULL`.
- At least two valid points are required. Otherwise, the result is `NULL`.
- The result type is `DOUBLE`.

```sql
SELECT AREA(power_kw, sample_sec)
FROM power_log;
```


## AVG

This function is an aggregate function that operates on a numeric column and prints the average value of that column.

```sql
AVG(column_name)
```

```sql
Mach> CREATE TABLE avg_table (id1 INTEGER, id2 INTEGER);
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

This function converts two input values ​​to a 64-bit signed integer and returns the result of bitwise and/or. The input value must be an integer and the output value is a 64-bit signed integer.

For integer values ​​less than 0, it is recommended to use only uinteger and ushort types, because different results may be obtained depending on the platform.

```sql
BITAND (<expression1>, <expression2>)
BITOR (<expression1>, <expression2>)
```

```sql
Mach> CREATE TABLE bit_table (i1 INTEGER, i2 UINTEGER, i3 FLOAT, i4 DOUBLE, i5 SHORT, i6 VARCHAR(10));
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


## COUNT

This function is an aggregate function that obtains the number of records in a given column.

```sql
COUNT(column_name)
```

```sql
Mach> CREATE TABLE count_table (id1 INTEGER, id2 INTEGER);
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

`CUME_DIST(value, threshold)` returns the cumulative ratio of rows whose `value` is less than or equal to the given threshold.

```sql
CUME_DIST(value, threshold)
```

- This is an aggregate function, not a window function.
- Both arguments must be numeric.
- `threshold` must be a constant.
- The return value is a `DOUBLE` between `0.0` and `1.0`.

```sql
SELECT CUME_DIST(latency_ms, 100)
FROM api_log;
```


## DATE_TRUNC

This function returns a given datetime value as a new datetime value that is displayed only up to 'time unit' and 'time range'.

```sql
DATE_TRUNC (field, date_val [, count])
```

```sql
Mach> CREATE TABLE trunc_table (i1 INTEGER, i2 DATETIME);
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

The allowable time ranges for time units and time units are as follows.

* nanosecond, microsecond, and milisecond units and abbreviations can be used starting from 5.5.6.
* week is start from Sunday.

|Time Unit|Time Range|
|--|--|
|nanosecond (nsec)|1000000000 (1 second)|
|microsecond (usec)|60000000 (60 seconds)|
|milisecond (msec)|60000 (60 seconds)|
|second (sec)|86400 (1 day)|
|minute (min)|1440 (1 day)|
|hour|24 (1 day)|
|day|1|
|week|1|
|month|1|
|year|1|

For example, if you type in DATE_TRUNC('second', time, 120), the value returned will be displayed **every two minutes** and is the same as DATE_TRUNC('minute', time, 2).

## DATE_BIN
This function bins the given datetime value into a `time unit` and `time range`
based on the specified `origin`.

```sql
DATE_BIN(field, count, source [, origin])
```

- If `origin` is specified, the bin boundary is calculated from that timestamp.
- If `origin` is omitted, the bin boundary is calculated from `1970-01-01 00:00:00`
  in the server's local timezone.
- `count` must be an integer greater than or equal to 1.

Use the 3-argument form when you want local-time bucket boundaries consistent with
`DATE_TRUNC()` or `ROLLUP()`. Use the 4-argument form when you need a fixed origin
that does not depend on the server timezone.

For example, on a `UTC+09:00` server, users previously had to provide a timezone-adjusted
`origin` value instead of `DATE_BIN(..., 0)` to align with local-time boundaries. The
3-argument form now provides the same local-time alignment directly.

```sql
Mach> CREATE TABLE log (time DATETIME);
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

The following example shows local-time bucket alignment with the 3-argument form.

```sql
Mach> CREATE TABLE t3521 (ts DATETIME);
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

The allowable time ranges for time units and time units are as follows.

* nanosecond, microsecond, and milisecond units and abbreviations can be used starting from 5.5.6.
* week is equal to 7 days.

|Time Unit|
|----:|
|nanosecond (nsec)|
|microsecond (usec)|
|milisecond (msec)|
|second (sec)|
|minute (min)|
|hour|
|day|
|week|
|month|
|year|


## DAYOFWEEK

This function returns a natural number representing the day of the week for a given datetime value.

Returns a semantically equivalent value for [TO_CHAR (time, 'DAY')](#to_char), but returns an integer here.

```sql
DAYOFWEEK(date_val)
```

The returned natural number represents the next day of the week.

|Return Value|Day of Week|
|--|--|
|0|Sunday|
|1|Monday|
|2|Tuesday|
|3|Wednesday|
|4|Thursday|
|5|Friday|
|6|Saturday|


## DECODE

This function compares the given Column value with Search, and returns the next return value if it is the same. If there is no satisfactory Search value, it returns the default value. If Default is omitted, NULL is returned.

```sql
DECODE(column, [search, return],.. default)
```

```sql
Mach> CREATE TABLE decode_table (id1 VARCHAR(11));
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

Bit-extraction helpers for binary frames.
`EXTRACT_*` uses a big-endian model and `EXTRACT_LE_*` uses a little-endian model.
All functions accept `BINARY/VARBINARY` frames; NULL frames return NULL.

**Endian Model**

- `EXTRACT_*`: MSB-first (`bit 0` is the MSB of `byte[0]`)
- `EXTRACT_LE_*`: LSB-first (`bit 0` is the LSB of `byte[0]`)
- Bit indexes are zero-based across the full frame.

**Common Rules**

- Single bit: `0 <= bit_pos < frame_bits`
- Bit range: `start_bit >= 0`, `1 <= bit_count <= 64`,
  `start_bit + bit_count <= frame_bits`
- `EXTRACT_FLOAT*` reads 32 bits and `EXTRACT_DOUBLE*` reads 64 bits.
- Signed extraction uses two's-complement interpretation with sign-extension to
  64-bit.
- Range errors: `ERR_QP_INVALID_ARG_VALUE` (`ERR-02229` family)
- Argument type errors: `ERR_QP_FUNCTION_ARG_TYPE`

### EXTRACT_BIT

```
EXTRACT_BIT(frame, bit_pos) / EXTRACT_LE_BIT(frame, bit_pos) → TINYINT
```

Returns a single bit as 0 or 1.

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

Reads 1~64 bits as unsigned or two's-complement signed integers.

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

Reinterprets 32/64 bits as IEEE754 float/double; the selected bit window must
fit within the frame.

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

Reads 1~64 bits as unsigned (`signed=0`) or two's-complement signed (`signed=1`)
integer, then returns `raw * scale + offset`.

```sql
-- 20-bit sensor value, scale 0.01, offset -40.0
SELECT EXTRACT_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0)    AS be_value,
       EXTRACT_LE_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0) AS le_value
FROM t_bin;
```


## FIRST / LAST

This function is an aggregate function that returns the specific value of the highest (or last) record in the sequence in which the 'reference value' in each group is in order.

* FIRST: Returns a specific value from the most advanced record in the sequence
* LAST: Returns a specific value from the last record in the sequence

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


## FROM_UNIXTIME

This function converts a 32-bit UNIXTIME value entered as an integer to a datetime datatype value. (UNIX_TIMESTAMP converts datetime data to 32-bit UNIXTIME integer data.)

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


## FROM_TIMESTAMP

This function takes a nanosecond value that has passed since 1970-01-01 09:00 and converts it to a datetime data type.

(TO_TIMESTAMP () converts a datetime data type to nanosecond data that has passed since 1970-01-01 09:00.)

```sql
FROM_TIMESTAMP(nanosecond_time_value)
```

```sql
Mach> SELECT FROM_TIMESTAMP(1562302560007248869) FROM TEST;
FROM_TIMESTAMP(1562302560007248869)
--------------------------------------
2019-07-05 13:56:00 007:248:869
```

Both sysdate and now represent nanosecond values elapsed since 1970-01-01 09:00 at the current time, so you can use FROM_TIMESTAMP () immediately.

Of course, the results are the same without using them. This can be useful if you have sysdate and now operations in nanoseconds.

```sql
Mach> select sysdate, from_timestamp(sysdate) from test_tbl;
sysdate                         from_timestamp(sysdate)
-------------------------------------------------------------------
2019-07-05 14:00:59 722:822:443 2019-07-05 14:00:59 722:822:443
[1] row(s) selected.
 
Mach> select sysdate, from_timestamp(sysdate-1000000) from test_tbl;
sysdate                         from_timestamp(sysdate-1000000)
-------------------------------------------------------------------
2019-07-05 14:01:05 130:939:525 2019-07-05 14:01:05 129:939:525      -- 1 ms (1,000,000 ns) 차이가 발생함
[1] row(s) selected.
```


## GROUP_CONCAT

This function is an aggregate function that outputs the value of the corresponding column in the group in a string.

{{<callout type="warning">}}
This function cannot be used in Cluster Edition.
{{</callout>}}

```sql
GROUP_CONCAT(
     [DISTINCT] column
     [ORDER BY { unsigned_integer | column }
     [ASC | DESC] [, column ...]]
     [SEPARATOR str_val]
)
```

* DISTINCT: Duplicate values ​​are not appended if duplicate values ​​are attached.
* ORDER BY: Arranges the sequence of column values ​​to be attached according to the specified column values.
* SEPARATOR: A delimiter string used to append column values. The default value is a comma (,).

The syntax notes are as follows.

* You can specify only one column, and if you want to specify more than one column, you must use the TO_CHAR () function and the CONCAT operator (||) to make one expression.
* ORDER BY can specify other columns besides the columns to be joined, and can specify multiple columns.
* You must enter a string constant in SEPARATOR, and you can not enter a string column.

```sql
Mach> CREATE TABLE concat_table(id1 INTEGER, id2 DOUBLE, name VARCHAR(10));
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

This function returns the index of the number of characters in the string entered together. The index starts at 1.

* If no string pattern is found, 0 is returned.
* If the length of the string pattern to find is 0 or NULL, NULL is returned.

```sql
INSTR(target_string, pattern_string)
```

```sql
Mach> CREATE TABLE string_table(c1 VARCHAR(20));
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

Both functions return the smallest value (LEAST) or the largest value (GREATEST) if you specify multiple columns or values ​​as input parameters.

If the input value is 1 or absent, it is treated as an error. If the input value is NULL, NULL is returned. Therefore, if the input value is a column, it must be converted in advance using a function.
If a column (BLOB, TEXT) that can not be compared with the input value is included or type conversion is not possible for comparison, comparison is processed as an error.

```sql
LEAST(value_list, value_list,...)
GREATEST(value_list, value_list,...)
```

```sql
Mach> CREATE TABLE lgtest_table(c1 INTEGER, c2 LONG, c3 VARCHAR(10), c4 VARCHAR(5));
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

This function gets the length of a string column. The obtained value outputs the number of bytes in English.

```sql
LENGTH(column_name)
```

```sql
Mach> CREATE TABLE length_table (id1 INTEGER, id2 DOUBLE, name VARCHAR(15));
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

This function converts an English string to lowercase.

```sql
LOWER(column_name)
```

```sql
Mach> CREATE TABLE lower_table (name VARCHAR(20));
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

This function adds a character to the left (LPAD) or to the right (RPAD) until the input is of a given length.

The last parameter, char, can be omitted, or a space ' ' character if omitted. 
If the input column value is longer than the given length, the characters are not appended but only the length is taken from the beginning.

```sql
LPAD(str, len, padstr)
RPAD(str, len, padstr)
```

```sql
Mach> CREATE TABLE pad_table (c1 integer, c2 varchar(15));
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

This function removes the value corresponding to the pattern string from the first parameter. The LTRIM function checks to see if the characters are in pattern from left to right, the RTRIM function from right to left, and truncates until a character not in pattern is encountered. If all the strings are present in the pattern, NULL is returned.

If you do not specify a pattern expression, use the space character '' as a basis to remove the space character.

```sql
LTRIM(column_name, pattern)
RTRIM(column_name, pattern)
```

```sql
Mach> CREATE TABLE trim_table1(name VARCHAR(10));
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
 
Mach> CREATE TABLE trim_table2 (name VARCHAR(10));
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

This function is an aggregate function that obtains the maximum value of a given numeric column.

```sql
MAX(column_name)
```

```sql
Mach> CREATE TABLE max_table (c INTEGER);
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

`MEDIAN(value)` returns the exact median of a numeric expression. In the current implementation, it behaves like `PERCENTILE_CONT(value, 0.5)`.

```sql
MEDIAN(value)
```

- `value` must be numeric.
- `NULL` values are ignored.
- The result type is `DOUBLE`.

```sql
SELECT MEDIAN(temp_c)
FROM sensor_log;
```


## MIN

This function is an aggregate function that obtains the minimum value of a corresponding numeric column.

```sql
MIN(column_name)
```

```sql
Mach> CREATE TABLE min_table(c1 INTEGER);
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
 
This function returns value if the value of the column is NULL, or the value of the original column if it is not NULL.

```sql
NVL(string1, replace_with)
```

```sql
Mach> CREATE TABLE nvl_table (c1 varchar(10));
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


## ROUND

This function returns the result of rounding off the digits of the input value (input digit +1). If no digits are entered, the rounding is done at position 0. It is possible to enter a negative number in decimals place to round the decimal place.

```sql
ROUND(column_name, [decimals])
```

```sql
Mach> CREATE TABLE round_table (c1 DOUBLE);
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

This function assigns a number to the SELECT query result row.

It can be used inside Subquery or Inline View that is used inside SELECT query. If you use ROWNUM () function in Inline View in Target List, you need to give Alias ​​to refer to from outside.

```sql
ROWNUM()
```

**Available Clauses**

This function can be used in the target list, GROUP BY, or ORDER BY clause of a SELECT query. However, it can not be used in the WHERE and HAVING clauses of a SELECT query. ROWNUM () If you want to control WHERE or HAVING clause with result number, you can use SELECT query with ROWNUM () in Inline View and refer to it in WHERE or HAVING clause.

|Available Clauses|Unavailable Clauses|
|--|--|
|Target List / GROUP BY / ORDER BY|WHERE / HAVING|

```sql
Mach> CREATE TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
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

**Altering Results Due to Sorting**

If there is an ORDER BY clause in the SELECT query, the result number of ROWNUM () in the target list may not be sequentially assigned. This is because the ROWNUM () operation is performed before the operation of the ORDER BY clause. If you want to give it sequentially, you can use the query containing the ORDER BY clause in Inline View and then call ROWNUM () in the outer SELECT statement.

```sql
Mach> CREATE TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
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

Returns a number indicating how many of the records belong to the series grouped by SERIES BY. The return type is BIGINT type, and always returns 1 if the SERIES BY clause is not used.

```sql
SERIESNUM()
```

```sql
Mach> CREATE TABLE T1 (C1 INTEGER, C2 INTEGER);
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

This function is an aggregate function that returns the (standard) deviation and the population standard deviation of the (input) column. Equivalent to the square root of the VARIANCE and VAR_POP values, respectively.

```sql
STDDEV(column)
STDDEV_POP(column)
```

```sql
Mach> CREATE TABLE stddev_table(c1 INTEGER, C2 DOUBLE);
 
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

This function truncates the variable string column data from START to SIZE.

* START starts at 1 and returns NULL if it is zero.
* If SIZE is larger than the size of the corresponding string, only the maximum value of the string is returned.
SIZE is optional, and if omitted, it is internally specified by the size of the string.

```sql
SUBSTRING(column_name, start, [length])
```

```sql
Mach> CREATE TABLE substr_table (c1 VARCHAR(10));
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
 
Mach> CREATE TABLE substr_table (c1 VARCHAR(10));
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

Returns the duplicate string until the given delim is found by the count entered. If count is a negative value, it checks the delimiter from the end of the input string and returns it from the position where the delimiter was found to the end of the string.

If you enter count as 0 or there is no delimiter in the string, the function will return NULL.

```sql
SUBSTRING_INDEX(expression, delim, count)
```

```sql
Mach> CREATE TABLE substring_table (url VARCHAR(30));
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

This function is an aggregate function that represents the sum of the numeric columns.

```sql
SUM(column_name)
```

```sql
Mach> CREATE TABLE sum_table (c1 INTEGER, c2 INTEGER);
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

SUMSQ returns the sum of squares of the numeric values.

```sql
SUMSQ(value)
```

```sql
Mach> CREATE TABLE sumsq_table (c1 INTEGER, c2 INTEGER);
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

SYSDATE is a pseudocolumn, not a function, that returns the system's current time.

NOW is the same function as SYSDATE and is provided for user convenience.

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

This function converts a given data type to a string type. Depending on the type, format_string may be specified, but not for binary types.

```sql
TO_CHAR(column)
```

**TO_CHAR: Default Datatype**

The default data types are converted to data in the form of strings as shown below.

```sql
Mach> CREATE TABLE fixed_table (id1 SHORT, id2 INTEGER, id3 LONG, id4 FLOAT, id5 DOUBLE, id6 IPV4, id7 IPV6, id8 VARCHAR (128));
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

**TO_CHAR: Floating Point Number**

* Supported from 5.5.6 version

This function converts the values ​​of float and double into strings.
Format expression cannot be used repeatedly, and must be entered in the form of '[letter][number]'.

|Format Expression|Descibe|
|--|--|
|F / f|Specifies the number of decimal places for the column value. The maximum numeric value to input is 30.|
|N / n|Specify the number of decimal places for the column value, and enter a comma (,) for every three digits of the integer part. The maximum numeric value to input is 30.|

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

**TO_CHAR: DATETIME Type**

A function that converts the value of a datetime column to an arbitrary string. You can use this function to create and combine various types of strings.

If format_string is omitted, the default is "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn".

|Format Expression|Descibe|
|--|--|
|YYYY|Converts year to a four-digit number.|
|YY|Converts year to a two-digit number.|
|MM|Converts the month to a two-digit number.|
|MON|Converts the month to a three-digit abbreviated alphabet. (eg JAN, FEB, MAY, ...)|
|DD|Converts the day to a two-digit number.|
|DAY|Converts the day of the week to a three-digit abbreviation . (eg SUN, MON, ...)|
|IW|Converts the week number of a specific year from 1 to 53 (taking into account the day of the week) by the ISO 8601 rule.<br> - The start of one week is Monday.<br> - The first week can be considered as the last week of the previous year. Likewise, the last week can be considered the first week of the next year.<br>    See ISO 8601 more information.|
|WW|Converts week number of the particular year from 1 to 53 (Week Number) not taking into account the day of the week.<br>That is, from January 1 to January 7, it is converted to 1.|
|W|Converts week number of a given month from 1 to 5 (Number The Week) not taking in to account the day of the week.<br>That is, from March 1 to March 7 is converted to 1.|
|HH|Converts the time to a two-digit number.|
|HH12|Converts the time to a 2-digit number, from 1 to 12.|
|HH24|Converts the time to a 2-digit number, from 1 to 23.|
|HH2, HH3, HH6|Cuts the time to the number following HH.<br><br>That is, when HH6 is used, 0 is expressed from 0 to 5, and 6 is expressed from 6 to 11.<br>This expression is useful for calculating certain time-series statistics on time series.<br>This value is expressed on a 24-hour basis.|
|MI|The minute is represented by a two-digit number.|
|MI2, MI5, MI10, MI20, MI30|The corresponding minute is cut to the number following MI.<br><br>That is, when MI30 is used, 0 is expressed from 0 to 29 minutes, and 30 is represented from 30 to 59 minutes.<br>This expression is useful for calculating certain time-series statistics on time series.|
|SS|The second is represented by a two-digit number.|
|SS2, SS5, SS10, SS20, SS30|The corresponding seconds are truncated to successive digits.<br><br>That is, when SS30 is used, 0 is expressed from 0 to 29 seconds, and 30 is represented from 30 to 59 seconds.<br>This expression is useful for calculating certain time-series statistics on time series.|
|AM|The current time is expressed in AM or PM according to AM and PM, respectively.|
|mmm|The millisecond of the time is represented by a three-digit number.<br><br>The range of values ​​is 0 to 999.|
|uuu|The micro second of the time is represented as a three-digit number.<br><br>The range of values ​​is 0 to 999.|
|nnn|The nano second of the time is expressed as a three-digit number.<br><br>The range of values ​​is 0 to 999.|

```sql
Mach> CREATE TABLE datetime_table (id integer, dt datetime);
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

**TO_CHAR: Unsupported Type**

Currently, TO_CHAR is not supported for binary types.

This is because it is impossible to convert to plain text. If you want to output it to the screen, you can check it by outputting hexadecimal value through TO_HEX () function.


## TO_DATE

This function converts a string represented by a given format string to a datetime type.

If format_string is omitted, the default is "YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn".

```sql
-- default format is "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" if no format exists.
TO_DATE(date_string [, format_string])
```

```sql
Mach> CREATE TABLE to_date_table (id INTEGER, dt datetime);
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

Similar to TO_DATE (), but returns NULL without error if conversion fails.

```sql
TO_DATE_SAFE(date_string [, format_string])
```

```sql
Mach> CREATE TABLE date_table (ts DATETIME);
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

This function returns value if the value of the column is NULL, or the value of the original column if it is not NULL. To ensure consistency of output, convert to BIG ENDIAN type for short, int, and long types.

```sql
TO_HEX(column)
```

```sql
Mach> CREATE TABLE hex_table (id1 SHORT, id2 INTEGER, id3 VARCHAR(10), id4 FLOAT, id5 DOUBLE, id6 LONG, id7 IPV4, id8 IPV6, id9 TEXT, id10 BINARY,
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


## TO_IPV4 / TO_IPV4_SAFE

This function converts a given string to an IP version 4 type. If the string can not be converted to a numeric value, the TO_IPV4 () function returns an error and terminates the operation.

However, in the case of the TO_IPV4_SAFE () function, NULL is returned in case of error, and the operation can continue.

```sql
TO_IPV4(string_value)
TO_IPV4_SAFE(string_value)
```

```sql
Mach> CREATE TABLE ipv4_table (c1 varchar(100));
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

This function converts a given string to an IP version 6 type. If the string can not be converted to a numeric type, the TO_IPV6 () function returns an error and terminates the operation.

However, in the case of the TO_IPV6_SAFE () function, NULL is returned in case of error, and the operation can continue.

```sql
TO_IPV6(string_value)
TO_IPV6_SAFE(string_value)
```

```sql
Mach> CREATE TABLE ipv6_table (id varchar(100));
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

This function converts a given string to a numeric double. If the string can not be converted to a numeric value, the TO_NUMBER () function returns an error and terminates the operation.

However, in case of TO_NUMBER_SAFE () function, NULL is returned in case of error, and the operation can continue.

```sql
TO_NUMBER(string_value)
TO_NUMBER_SAFE(string_value)
```

```sql
Mach> CREATE TABLE number_table (id varchar(100));
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
 
Mach> CREATE TABLE safe_table (id varchar(100));
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

`TOP_K(value, k)` returns the most frequent `k` numeric values as a comma-separated `value:count` string.

```sql
TOP_K(value, k)
```

- `value` must be numeric.
- `k` must be a positive constant integer.
- `NULL` values are ignored.
- The result type is `VARCHAR`.
- Rows are ordered by frequency descending and, for ties, value ascending.

```sql
SELECT TOP_K(alarm_code, 3)
FROM event_log;
```

Example result:

```text
101:532,205:317,301:90
```


## TO_TIMESTAMP

This function converts a datetime data type to nanosecond data that has passed since 1970-01-01 09:00.

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

The TRUNC function returns the number truncated at the nth place after the decimal point. 

If n is omitted, treat it as 0 and delete all decimal places. If n is negative, it returns the value truncated from n before the decimal point.

```sql
TRUNC(number [, n])
```

```sql
Mach> CREATE TABLE trunc_table (i1 DOUBLE);
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

This function is an aggregate function that obtains the number of changes to a particular column value.

This function can not be used with 1) Join or 2) Inline view because it can be guaranteed that input data is input in chronological order.
The current version only supports types except varchar.

* **This function cannot be used in Cluster Edition.**

```sql
TS_CHANGE_COUNT(column)
```

```sql
Mach> CREATE TABLE ipcount_table (id INTEGER, ip IPV4);
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

UNIX_TIMESTAMP is a function that converts a date type value to a 32-bit integer value that is converted by unix's time () system call. (FROM_UNIXTIME is a function that converts integer data to a date type value on the contrary.)

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

This function converts the contents of a given English column to uppercase.

```sql
UPPER(string_value)
```

```sql
Mach> CREATE TABLE upper_table(id INTEGER,name VARCHAR(10));
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

This function is an aggregate function that returns the variance of a given numeric column value. The Variance function returns the variance for the sample, and the VAR_POP function returns the variance for the population.

```sql
VARIANCE(column_name)
VAR_POP(column_name)
```

```sql
Mach> CREATE TABLE var_table(c1 INTEGER, c2 DOUBLE);
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

These functions extract the corresponding year, month, and day from the input datetime column value and return it as an integer type value.

```sql
YEAR(datetime_col)
MONTH(datetime_col)
DAY(datetime_col)
```

```sql
Mach> CREATE TABLE extract_table(c1 DATETIME, c2 INTEGER);
Created successfully.
 
Mach> INSERT INTO extract_table VALUES (to_date('2001-01-01 12:30:00 000:000:000'), 1);
1 row(s) inserted.
 
Mach> SELECT YEAR(c1), MONTH(c1), DAY(c1) FROM extract_table;
year(c1)    month(c1)   day(c1)
----------------------------------------
2001        1           1
```


## ISNAN / ISINF

This function determines whether the numeric value received as an argument is a NaN or Inf value. Returns 1 for NaN or Inf values, and 0 otherwise.

```sql
ISNAN(number)
ISINF(number)
```

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

Stores a SQL scalar value at the given path as a JSON scalar.

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

- `path` must use full JSONPath syntax.
- `JSON_SET(..., path, NULL)` stores JSON `null`.
- If the JSON document argument is `NULL`, the result is SQL `NULL`.
- If `path` is `NULL` or an empty string, the function raises an error.
- Object paths are supported.
- Array element mutation such as `$.items[0]` is not supported.

## JSON_SET_JSON

Parses the third argument as JSON text and stores it as an object or array subtree.

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

- `path` must use full JSONPath syntax.
- If the third argument is SQL `NULL`, the result is SQL `NULL`.
- Invalid JSON text raises an error.
- Object paths are supported.
- Array element mutation is not supported.

## JSON_REMOVE

Removes a member or subtree from a JSON document.

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

- `path` must use full JSONPath syntax.
- A missing path is treated as a no-op.
- `JSON_REMOVE(..., '$')` is not allowed.
- If the JSON document argument is `NULL`, the result is SQL `NULL`.

## PI() {#pi}

Returns a `DOUBLE` constant π.

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

Returns the square root of one numeric argument.

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

Returns `base` raised to `exponent`.

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

Alias of `POWER()`.

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

`LOG(n)` is the same as natural log; `LOG(base, n)` calculates logarithm with a base.

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

Returns natural logarithm `ln(n)`.

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

Returns `e^n` of the argument.

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

Returns sine value of a radian input.

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

`SLOPE(y, x)` calculates the slope of the linear regression line for numeric `(x, y)` pairs.

```sql
SLOPE(y, x)
```

- Both arguments must be numeric.
- `NULL` values are ignored.
- If there are not enough valid rows or the `x` variance is zero, the result is `NULL`.
- The result type is `DOUBLE`.

```sql
SELECT SLOPE(temp_c, sample_sec)
FROM sensor_log;
```

## COS() {#cos}

Returns cosine value of a radian input.

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

Returns tangent value of a radian input.

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

Returns remainder using truncation toward zero of the quotient.

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

`MODE(value)` returns the most frequent numeric value in the input set.

```sql
MODE(value)
```

- `value` must be numeric.
- `NULL` values are ignored.
- If multiple values have the same highest frequency, the smallest value is returned.
- The result type is `DOUBLE` in the current implementation.

```sql
SELECT MODE(alarm_code)
FROM event_log;
```

## P05 / P10 / P90 / P95 {#p05-p10-p90-p95}

These are shorthand forms of exact percentile calculations for frequently used percentile points.

```sql
P05(value)
P10(value)
P90(value)
P95(value)
```

- `value` must be numeric.
- `NULL` values are ignored.
- The result type is `DOUBLE`.

`P05`, `P10`, `P90`, and `P95` are equivalent to `PERCENTILE_CONT(value, 0.05)`, `0.10`, `0.90`, and `0.95`.

```sql
SELECT P05(response_ms),
       P10(response_ms),
       P90(response_ms),
       P95(response_ms)
FROM web_log;
```

## PERCENTILE_CONT / PERCENTILE_DISC {#percentile_cont-percentile_disc}

These aggregate functions calculate exact percentiles on numeric input.

```sql
PERCENTILE_CONT(value, ratio)
PERCENTILE_DISC(value, ratio)
```

- `value` must be numeric.
- `ratio` must be a constant in the range `0.0` to `1.0`.
- `PERCENTILE_CONT` interpolates between adjacent sorted values when needed.
- `PERCENTILE_DISC` selects one of the observed values at the target rank.
- Both functions currently return `DOUBLE`.

```sql
SELECT PERCENTILE_CONT(latency_ms, 0.95) AS pcont95,
       PERCENTILE_DISC(latency_ms, 0.95) AS pdisc95
FROM api_log;
```

## QUANTILE {#quantile}

`QUANTILE(value, ratio)` calculates an exact continuous quantile on numeric input.

```sql
QUANTILE(value, ratio)
```

- `value` must be numeric.
- `ratio` must be a constant in the range `0.0` to `1.0`.
- The result type is `DOUBLE`.
- In the current implementation, it belongs to the same continuous percentile family as `PERCENTILE_CONT`.

```sql
SELECT QUANTILE(cpu_usage, 0.75)
FROM host_metric;
```

## RAND() {#rand}

Generates pseudo-random values.

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

`RAND(seed)` is deterministic for the same `seed`. `RAND()` without a seed uses session internal state and generates values in `[0,1)`.

## Support Type of Built-In Function 

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
|FROM_UNIXTIME|o|o|o|o|o|x|x|x|x|x|x|
|FROM_TIMESTAMP|o|o|o|o|o|x|x|x|x|x|x|
|GROUP_CONCAT|o|o|o|o|o|o|x|o|o|o|x|
|INSTR|x|x|x|x|x|o|o|x|x|x|x|
|LEAST / GREATEST|o|o|o|o|o|o|x|x|x|x|x|
|LENGTH|x|x|x|x|x|o|o|x|x|x|o|
|LOWER|x|x|x|x|x|o|x|x|x|x|x|
|LPAD / RPAD|x|x|x|x|x|o|x|x|x|x|x|
|LTRIM / RTRIM|x|x|x|x|x|o|x|x|x|x|x|
|MAX|o|o|o|o|o|o|x|o|o|o|x|
|MEDIAN|o|o|o|o|o|x|x|x|x|x|x|
|MIX|o|o|o|o|o|o|x|o|o|o|x|
|MODE|o|o|o|o|o|x|x|x|x|x|x|
|NVL|x|x|x|x|x|o|x|o|x|x|x|
|P05 / P10 / P90 / P95|o|o|o|o|o|x|x|x|x|x|x|
|PERCENTILE_CONT / PERCENTILE_DISC|o|o|o|o|o|x|x|x|x|x|x|
|QUANTILE|o|o|o|o|o|x|x|x|x|x|x|
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
|TO_IPV4 / TO_IPV4_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_IPV6 / TO_IPV6_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_NUMBER / TO_NUMBER_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_TIMESTAMP|x|x|x|x|x|x|x|x|x|o|x|
|TRUNC|o|o|o|o|o|x|x|x|x|x|x|
|TS_CHANGE_COUNT|o|o|o|o|o|x|x|o|o|o|x|
|UNIX_TIMESTAMP|o|o|o|o|o|x|x|x|x|x|x|
|UPPER|x|x|x|x|x|o|x|x|x|x|x|
|VARIANCE / VAR_POP|o|o|o|o|o|x|x|x|x|x|x|
|YEAR / MONTH / DAY|x|x|x|x|x|x|x|x|x|o|x|
|ISNAN / ISINF|o|o|o|o|o|x|x|x|x|x|x|


## JSON-related function 

These functions use json data type as an argument.

|Function name|Explanation|Note|
|--|--|--|
|JSON_EXTRACT(JSON column name, 'json path')|Return the value as string type.<br>(If the value does not exist, return ERROR.)| - JSON object or array : Convert every objects into string type and return it.<br> - String type : Return as is<br> - Numeric type : Convert into string type and return it<br> - boolean type : Return "True" or "False"|
|JSON_EXTRACT_DOUBLE(JSON column name, 'json path')	|Return the value as 64 bits double type.<br>(If the value does not exist, return NULL.)| - JSON object or array : Return NULL<br> - String type : Convert and return if possible. Else return NULL.<br> - Numeric type : Return 64bit real number.<br> - boolean type : Return "True" as 1.0 or "False" as 0.0|
|JSON_EXTRACT_INTEGER(JSON column name, 'json path')|Return the value as 64 bits integer type.<br>(If the value does not exist, return NULL.)| - JSON object or array : Return NULL<br> - String type : Convert and return if possible. Else return NULL.<br> - Numeric type : Return 64bit integer.<br> - boolean type : Return "True" as 1 or "False" as 0|
|JSON_EXTRACT_STRING(JSON column name, 'json path')|Return the value as string type.<br>(If the value does not exist, return NULL.)<br>Returns same results as operator(→)| - JSON object or array : Convert every objects into string type and return it.<br> - String type : Return as is <br> - Numeric type : Convert into string type and return it <br> - boolean type : Return "True" or "False"|
|JSON_SET(json_doc, path, scalar)|Returns a new JSON document with the SQL scalar value stored at the given path as a JSON scalar.| - `path` must use full JSONPath syntax.<br> - `NULL` is stored as JSON `null`.<br> - Only object paths are supported.|
|JSON_SET_JSON(json_doc, path, json_text)|Returns a new JSON document with the JSON text stored at the given path as an object or array subtree.| - `path` must use full JSONPath syntax.<br> - If the third argument is SQL `NULL`, the result is SQL `NULL`.<br> - Invalid JSON text raises an error.|
|JSON_REMOVE(json_doc, path)|Returns a new JSON document with the member or subtree at the given path removed.| - `path` must use full JSONPath syntax.<br> - Missing paths are treated as no-op.<br> - `JSON_REMOVE(..., '$')` is not allowed.|
|JSON_IS_VALID('json string')|Check if the json string is valid for the json format| - 0 : False<br> - 1 : True|
|JSON_TYPEOF(JSON column name, 'json path')|Returns the type of the value.| - None : Key does not exists.<br> - Object : Object type<br> - Integer : Integer Type<br> - Real : Real number type<br> - String : String type<br> - True/False : Boolean<br> - Array : Array Type<br> - Null : NULL|

```sql
Mach> CREATE TABLE jsontbl (name VARCHAR(20), jval JSON);
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


## JSON Operator

'->' operator is used for accessing an object of JSON data.

Returns the same results as JSON_EXTRACT_STRING function.

```sql
json_col -> 'json path'
```

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

## WINDOW FUNCTION

The WINDOW function is a function for comparison, operation, and definition between rows. It is also called an analysis function or ranking function.

It can only be used in the SELECT statement.

### WINDOW FUNCTION SYNTAX

Window functions necessarily include the OVER clause.

```
WINDOW_FUNCTION (ARGUMENTS) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

* WINDOW_FUNCTION: Window function name
* ARGUMENTS: Depending on the function, 0 to N arguments can be specified.
* PARTITION BY clause: The entire set can be divided into small groups based on criteria. (can be omitted)
* ORDER BY clause: Describes the order by clause on which items to sort. (Can be omitted)

### WINDOW FUNCTION LIST

#### LAG

Retrieve the value of the previous Nth row in a partition-specific window.

If there are no rows to retrieve, NULL is returned.

```
LAG(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE TABLE lag_table (name varchar(10), dt datetime, value INTEGER);
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

Retrieve the value of the Nth row from the partition-specific window.

If there are no rows to retrieve, NULL is returned.

```
LEAD(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE TABLE lead_table (name varchar(10), dt datetime, value INTEGER);
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

`NTILE(n)` divides ordered rows into `n` buckets as evenly as possible and returns the bucket number of each row.

```
NTILE(n) OVER ([PARTITION BY column_name] ORDER BY column_name)
```

- `n` must be a positive constant.
- `ORDER BY` inside `OVER (...)` is required.
- If rows cannot be divided evenly, earlier buckets receive one more row.

```
Mach> SELECT user_id,
             score,
             NTILE(4) OVER (ORDER BY score) AS score_band
      FROM exam_result;
```
