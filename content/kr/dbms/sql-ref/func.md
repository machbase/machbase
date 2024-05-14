---
layout : post
title : '지원 함수'
type: docs
weight: 70
---

# 목차

* [ABS](#abs)
* [ADD_TIME](#add_time)
* [AVG](#avg)
* [BITAND / BITOR](#bitand--bitor)
* [COUNT](#count)
* [DATE_TRUNC](#date_trunc)
* [DATE_BIN](#date_bin)
* [DAYOFWEEK](#dayofweek)
* [DECODE](#decode)
* [FIRST / LAST](#first--last)
* [FROM_UNIXTIME](#from_unixtime)
* [FROM_TIMESTAMP](#from_timestamp)
* [GROUP_CONCAT](#group_concat)
* [INSTR](#instr)
* [LEAST / GREATEST](#least--greatest)
* [LENGTH](#length)
* [LOWER](#lower)
* [LPAD / RPAD](#lpad--rpad)
* [LTRIM / RTRIM](#ltrim--rtrim)
* [MAX](#max)
* [MIN](#min)
* [NVL](#nvl)
* [ROUND](#round)
* [ROWNUM](#rownum)
* [SERIESNUM](#seriesnum)
* [STDDEV / STDDEV_POP](#stddev--stddev_pop)
* [SUBSTR](#substr)
* [SUBSTRING_INDEX](#substring_index)
* [SUM](#sum)
* [SUMSQ](#sumsq)
* [SYSDATE / NOW](#sysdate--now)
* [TO_CHAR](#to_char)
* [TO_DATE](#to_date)
* [TO_DATE_SAFE](#to_date_safe)
* [TO_HEX](#to_hex)
* [TO_IPV4 / TO_IPV4_SAFE](#to_ipv4--to_ipv4_safe)
* [TO_IPV6 / TO_IPV6_SAFE](#to_ipv6--to_ipv6_safe)
* [TO_NUMBER / TO_NUMBER_SAFE](#to_number--to_number_safe)
* [TO_TIMESTAMP](#to_timestamp)
* [TRUNC](#trunc)
* [TS_CHANGE_COUNT](#ts_change_count)
* [UNIX_TIMESTAMP](#unix_timestamp)
* [UPPER](#upper)
* [VARIANCE / VAR_POP](#variance--var_pop)
* [YEAR / MONTH / DAY](#year--month--day)
* [ISNAN / ISINF](#isnan--isinf)
* [내장 함수 지원 타입](#내장-함수-지원-타입)
* [JSON 관련 함수](#json-관련-함수)
* [JSON Operator](#json-operator)
* [WINDOW 함수](#window-함수)

## ABS

이 함수는 숫자형 컬럼에 대해 동작하고, 양의 값으로 변환해서 실수형으로 값을 리턴한다.

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

이 함수는 주어진 datetime 컬럼에 대해 날짜 가감연산을 수행한다.

연, 월, 일, 시간, 분, 초 까지의 가감 연산을 지원하며, 밀리, 마이크로, 나노초에 대한 연산은 지원하지 않는다. Diff format은 다음과 같다.

"Year/Month/Day Hour:Minute:Second" 각 항목은 양수 혹은 음수 값을 가진다.

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

## AVG

이 함수는 집계 함수로써, 숫자형 컬럼에 대해 동작하고 해당 컬럼의 평균 값을 출력한다.

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

이 함수는 두 입력 값을 64-bit 의 부호 있는 정수로 변환한 뒤, 비트별 and/or 을 수행한 결과를 반환한다. 입력 값은 반드시 정수형이어야 하며, 출력 값은 64비트 부호 있는 정수가 된다.

0보다 작은 정수값에 대해서는 플랫폼에 따라 다른 결과를 얻을 수 있으므로 uinteger, ushort 타입만 사용하기를 권장한다.

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

이 함수는 집계 함수로써, 해당 컬럼의 레코드 개수를 구하는 함수이다.

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

## DATE_TRUNC

이 함수는 주어진 datetime 값을 '시간 단위'와 '시간 범위'까지만 표시된 새로운 datetime 값으로 반환한다.

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
 
Mach> SELECT COUNT(*), DATE_TRUNC('nsec', i2, 1000000000) tm FROM trunc_table group by tm ORDER BY 2; //DATE_TRUNC('sec', i2, 1) 과같음
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.
```

시간 단위와, 시간 단위별 허용되는 시간 범위는 다음과 같다.

* nanosecond, microsecond, milisecond 단위와 축약어는, 5.5.6 부터 사용 가능하다.
* week의 기준은 일요일이다.

|시간 단위 (축약어)|시간 범위|
|----:|:----|
|nanosecond (nsec)|	1000000000 (1초)|
|microsecond (usec)|	60000000 (60초)|
|milisecond (msec)|	60000 (60초)|
|second (sec)|	86400 (1일)|
|minute (min)|	1440 (1일)|
|hour|	24 (1일)|
|day|	1|
|week|	1|
|month|	1|
|year|	1|

예를 들어, DATE_TRUNC('second', time, 120) 으로 입력하면, 반환되는 값은 2분 간격으로 표시될 것이며 이는 DATE_TRUNC('minute', time, 2) 와 동일하다.

## DATE_BIN
이 함수는 주어진 datetime 값을 `지정된 원점` 기준으로 `시간 단위`와 `시간 범위`으로 `Binning` 한다.

```sql
DATE_BIN (field, count, source, origin)
```

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

Mach> SELECT TIME, DATE_BIN('hour', 3, time, TO_DATE('2020-01-01 01:00:00')) FROM log ORDER BY time;
TIME                            DATE_BIN('hour', 3, time, TO_DATE('2020-01-01 01:00:00')) 
---------------------------------------------------------------------------------------------
2000-01-01 00:00:00 000:000:000 1999-12-31 22:00:00 000:000:000                           
2000-01-01 01:00:00 000:000:000 2000-01-01 01:00:00 000:000:000                           
2000-01-01 02:00:00 000:000:000 2000-01-01 01:00:00 000:000:000                           
2000-01-01 03:00:00 000:000:000 2000-01-01 01:00:00 000:000:000                           
2000-01-01 04:00:00 000:000:000 2000-01-01 04:00:00 000:000:000                           
[5] row(s) selected.
```

시간 단위는 다음과 같다.

* nanosecond, microsecond, milisecond 단위와 축약어는, 5.5.6 부터 사용 가능하다.
* week는 7 day랑 같다.

|시간 단위 (축약어)|
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

이 함수는 주어진 datetime 값의 요일을 나타내는 자연수를 반환한다.

[TO_CHAR(time, 'DAY')](#to_char) 와 의미상 비슷한 값을 반환하지만, 여기서는 정수를 반환한다.

```sql
DAYOFWEEK(date_val)
```

반환되는 자연수는 다음의 요일을 나타낸다.

|반환값|요일|
|--|---|
|0|	일요일|
|1|	월요일|
|2|	화요일|
|3|	수요일|
|4|	목요일|
|5|	금요일|
|6|	토요일|

## DECODE

이 함수는 주어진 Column 값을 Search와 같은지 비교하고, 같으면 바로 다음의 Return 값을 되돌린다. 만일 만족하는 Search 값이 없을 경우에는 Default 값을 리턴한다. Default가 생략되었을 경우에는 NULL이 리턴된다.

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

## FIRST / LAST

이 함수는 집계 함수로써, 각 Group 에서 '기준 값'이 순서상 가장 앞선 (또는 가장 나중의) 레코드의 특정 값을 반환한다.
* FIRST : 순서상 가장 앞선 레코드에서 특정 값을 반환
* LAST : 순서상 가장 나중의 레코드에서 특정 값을 반환

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

이 함수는 정수형으로 입력된 32비트 UNIXTIME 값을 datetime 자료형의 값으로 변환한다. (UNIX_TIMESTAMP 는 datetime 자료형을 32비트 UNIXTIME 정수형 데이터로 변환한다.)

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

이 함수는 1970-01-01 09:00 부터 경과된 nanosecond 값을 입력받아 datetime 자료형의 값으로 변환한다. (TO_TIMESTAMP() 는 datetime 자료형을 1970-01-01 09:00 부터 경과된 nanosecond 데이터로 변환한다.)

```sql
FROM_TIMESTAMP(nanosecond_time_value)
```
```sql
Mach> SELECT FROM_TIMESTAMP(1562302560007248869) FROM TEST;
FROM_TIMESTAMP(1562302560007248869)
--------------------------------------
2019-07-05 13:56:00 007:248:869
```

sysdate, now 는 모두 현재 시각의 1970-01-01 09:00 부터 경과된 nanosecond 값을 나타내므로, 곧바로 FROM_TIMESTAMP() 를 사용해도 된다.

물론, 사용하지 않아도 결과는 같다. sysdate 와 now 에 nanosecond 단위로 연산을 한 경우에 유용하게 사용할 수 있다.

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

이 함수는 집계 함수로써, 그룹 안에 존재하는 해당 컬럼의 값을 문자열로 이어 붙여서 출력한다.

{{<callout type="warning">}}
Cluster Edition 에서는 사용할 수 없는 함수이다.
{{</callout>}}

```sql
GROUP_CONCAT(
     [DISTINCT] column
     [ORDER BY { unsigned_integer | column }
     [ASC | DESC] [, column ...]]
     [SEPARATOR str_val]
)
```

* DISTINCT: 이어 붙일 컬럼의 값이 중복되는 경우, 중복된 값은 이어 붙이지 않는다.
* ORDER BY: 지정된 컬럼 값들에 따라, 이어 붙이는 컬럼 값의 순서를 정렬한다.
* SEPARATOR: 컬럼 값을 이어 붙일 때 사용하는 구분자 문자열로, 기본 값은 콤마(,)이다.

문법에 대한 주의사항은 아래와 같다.

* 이어 붙일 컬럼은 1개만 지정할 수 있으며, 2개 이상 지정하고자 하는 경우에는 TO_CHAR() 함수와 CONCAT 연산자 (||)를 활용해서 1개의 표현식으로 만들어서 입력해야 한다.
* ORDER BY 에는 이어 붙이는 컬럼 외에 다른 컬럼을 지정할 수 있으며, 여러 컬럼을 지정할 수 있다.
* SEPARATOR 에는 반드시 문자열 상수를 입력해야 하며, 문자열 컬럼은 입력할 수 없다.

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

이 함수는 입력된 문자열 패턴이, 함께 입력된 문자열에서 몇 번째 문자에 있는지 그 인덱스를 반환한다. 인덱스 시작은 1 이다.

* 문자열 패턴을 찾을 수 없는 경우, 0 이 반환된다.
* 찾고자 하는 문자열 패턴의 길이가 0이거나 NULL 인 경우, NULL 이 반환된다.

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

두 함수는 입력 매개변수로 여러 개의 컬럼 또는 값들을 지정하면 그중 가장 작은 값(LEAST) 또는 가장 큰 값(GREATEST)을 반환한다.

만약 입력값이 1개 또는 없는 경우에는 오류로 처리되며 입력값들 중에 NULL이 있는 경우에는 NULL을 반환하므로 입력값이 컬럼인 경우 함수등을 이용하여 미리 변환하여야 한다.

입력값의 비교가 불가능한 컬럼(BLOB, TEXT) 등이 포함되어 있거나 대소비교를 위한 형 변환이 불가능한 경우 오류로 처리된다.

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

이 함수는 문자열 컬럼의 길이를 구한다. 구해진 값은 영문 기준으로 바이트 수를 출력한다.

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

이 함수는 영문 문자열을 소문자로 변환한다.

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

이 함수는 입력 값을 주어진 길이(length)가 될때까지 문자(char)를 왼쪽(LPAD) 또는 오른쪽(RPAD)에 덧붙이는 함수이다.

마지막 매개변수인 char는 생략이 가능하며 생략된 경우에는 공백 문자 ' ' 를 이용한다.
입력된 컬럼값이 length로 주어진 길이보다 긴 경우에는 문자를 덧붙이지 않고 앞에서부터 length 만큼만 가져온다.

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

이 함수는 첫 번째 매개변수에서 pattern 문자열에 해당하는 값을 제거하는 역할을 수행한다. LTRIM 함수는 컬럼 값의 왼쪽에서 오른쪽으로, RTRIM 함수는 오른쪽에서 왼쪽으로 문자들이 pattern에 있는지 확인하고 pattern에 없는 문자를 만날 때까지 잘라낸다. 만약 모든 문자열이 pattern에 존재한다면 NULL을 리턴한다.

Pattern 표현식을 명시하지 않은 경우 공백 문자 ' '를 기본으로 사용하여 공백 문자를 제거한다.

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

이 함수는 집계 함수로써, 해당 숫자 컬럼의 최대 값을 구하는 함수이다.

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

## MIN

이 함수는 집계 함수로써, 해당 숫자 컬럼의 최소값을 구하는 함수이다.

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

이 함수는 컬럼의 값이 NULL이면 value를 리턴하고, NULL이 아니면 원래 컬럼의 값을 출력한다.

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

이 함수는 정수형 입력 값에서 (입력된 자릿수+1) 의 자릿수에서 반올림한 결과를 반환한다. 자릿수가 입력되지 않은 경우, 반올림은 0의 자리에서 이뤄진다. 소수점 자리를 반올림하기 위해서 decimals 자리에 음수를 입력하는 것이 가능하다.

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

이 함수는 SELECT 쿼리 결과 Row에 번호를 부여하는 함수이다.

SELECT 쿼리 내부에 사용되는 Subquery 또는 Inline View 내부에서도 사용이 가능하며, Inline View 에서 ROWNUM() 함수를 Target List에 사용하는 경우엔 Alias를 부여해야 외부에서 참조가 가능하다.

```sql
ROWNUM()
```

### 사용 가능한 절

해당 함수는 SELECT 쿼리의 Target List, GROUP BY, 또는 ORDER BY 절에서 사용이 가능하다. 하지만 SELECT 쿼리의 WHERE와 HAVING 절에서는 사용할 수 없다. ROWNUM() 결과 번호로 WHERE나 HAVING 절을 통해 제어하고자 한다면, ROWNUM() 을 포함한 SELECT 쿼리를 Inline View로 사용한 다음 외부에 있는 WHERE나 HAVING 절에서 참조하면 된다.

|사용할 수 있는 절|사용할 수 없는 절|
|---|---|
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

### 정렬로 인한 결과 변화

SELECT 쿼리에 ORDER BY 절이 존재하는 경우, Target List에 있는 ROWNUM()의 결과 번호가 순차적으로 부여되지 않는 경우가 발생할 수 있다. 이는 ROWNUM() 연산이 ORDER BY 절의 연산 이전에 이루어지기 때문이다. 순차적으로 부여하고자 할 경우, ORDER BY 절을 포함한 쿼리를 Inline View로 사용한 다음 ROWNUM()을 외부 SELECT 문에서 호출하면 된다.

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

각 레코드가, SERIES BY 로 그룹지어진 시리즈의 몇 번째에 속해있는지를 나타낸 번호를 반환한다. 반환형은 BIGINT 형이며, SERIES BY 절이 사용되지 않았을 경우엔 항상 1을 반환한다.

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

이 함수는 집계 함수로써, 입력된 컬럼의 (샘플) 표준 편차와 모집단 표준 편차를 반환한다. 각각 VARIANCE 와 VAR_POP 값의 제곱근과 같다.

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

이 함수는 가변 문자열 컬럼의 데이터를 START 부터 SIZE 만큼 잘라낸다.

* START 는 1부터 시작하며, 0일 경우에는 NULL을 리턴한다.
* SIZE가 만일 해당 문자열의 크기보다 클 경우에는 그 문자열의 최대값까지만 되돌린다.

SIZE는 생략 가능하며, 생략할 경우에는 해당 문자열 크기만큼 내부적으로 지정된다.

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

주어진 구분자(delim)가 입력한 count만큼 발견될 때까지 복제한 문자열을 반환한다. 만약 count를 음수값으로 입력하면 입력한 문자열의 끝에서부터 구분자를 검사해서 구분자가 발견된 위치에서 문자열의 끝까지 반환한다.

만약 count를 0으로 입력하거나 문자열에 구분자가 존재하지 않는다면 함수는 NULL을 리턴할 것이다.

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

이 함수는 집계 함수로써, 숫자형 컬럼의 총합을 나타낸다.

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

SUMSQ 함수는 숫자형 컬럼값에 대한 제곱 합을 반환한다.

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

SYSDATE 는 함수가 아니라 의사컬럼 (pseudocolumn) 으로, 시스템의 현재 시각을 반환한다.

NOW 는 SYSDATE 와 동일한 함수이며, 사용자 편의를 위해 같이 제공한다.

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

이 함수는 주어진 데이터 타입을 문자열 타입으로 변환하는 함수이다. 타입에 따라 format_string을 지정할 수도 있으며, Binary 타입에 대해서는 지원하지 않는다.

```sql
TO_CHAR(column)
```
### TO_CHAR : 기본 자료형

아래와 같이 기본 자료형에서는 그대로 문자열 형식의 데이터로 변환된다.

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

### TO_CHAR : 부동소수형

* 5.5.6 부터 지원됩니다.

float, double 컬럼의 값을 임의의 문자열로 변환하는 함수이다.

포맷 표현은 중복해서 사용할 수 없고, '[문자][숫자]' 의 형태로 입력해야 한다.

|포맷 표현식|설명|
|--|--|
|F / f	|컬럼 값의 소수점 자릿수를 지정한다. 입력 최대 숫자값은 30이다.|
|N / n	|컬럼 값의 소수점 자릿수를 지정하고, 정수 부분은 세자리마다 쉼표 (,) 를 입력한다. 입력 최대 숫자값은 30이다.|

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

### TO_CHAR : DATETIME 형

datetime 컬럼의 값을 임의의 문자열로 변환하는 함수이다. 이 함수를 이용하여 다양한 형태의 문자열을 만들고 조합할 수 있다.

format_string이 생략된 경우에는 기본값으로 "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" 을 사용해서 변환한다.

| 포맷 표현식                     | 설명                                                                                                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| YYYY                       | 연도를 4자리 숫자로 변환한다.                                                                                                                                                                          |
| YY                         | 연도를 2자리 숫자로 변환한다.                                                                                                                                                                          |
| MM                         | 해당 월을 2자리 숫자로 변환한다.                                                                                                                                                                        |
| MON                        | 해당 월을 3자리 축약 알파벳으로 변환한다. (e.g. JAN, FEB, MAY, ...)                                                                                                                                         |
| DD                         | 해당 일을 2자리 숫자로 변환한다.                                                                                                                                                                        |
| DAY                        | 해당 요일을 3자리 축약 알파벳으로 변환한다. (e.g. SUN, MON, ...)                                                                                                                                             |
| IW                         | ISO 8601 규칙에 의해 (요일을 고려한), 1부터 53까지의 특정 연도의 주 수 (Week Number) 를 변환한다.<br>한 주의 시작은 월요일이다.<br>첫 주는 이전 연도의 마지막 주로 간주할 수 있다. 마찬가지로, 마지막 주는 다음 연도의 첫 주로 간주할 수 있다.<br>자세한 내용은 ISO 8601 규칙을 참고한다. |
| WW                         | 요일을 고려하지 않은, 1부터 53까지의 특정 연도의 주 수 (Week Number) 를 변환한다.<br>즉, 1월 1일부터 1월 7일까지는 1로 변환된다.                                                                                                    |
| W                          | 요일을 고려하지 않은, 1부터 5까지의 특정 달의 주 수 (Week Number) 를 변환한다.<br>즉, 3월 1일부터 3월 7일까지는 1로 변환된다.                                                                                                      |
| HH                         | 해당 시간을 2자리 숫자로 변환한다.                                                                                                                                                                       |
| HH12                       | 해당 시간을 2자리 숫자로 변환하되, 1~12까지 표현한다.                                                                                                                                                          |
| HH24                       | 해당 시간을 2자리 숫자로 변환하되, 1~23까지 표현한다.                                                                                                                                                          |
| HH2, HH3, HH6              | 해당 시간을 HH 다음에 오는 숫자로 절삭한다.<br>즉, HH6을 사용한 경우 0시부터 5시까지는 0으로 6~11시까지는 6으로 표현한다.<br>이 표현은 시계열 상의 특정 시간 단위 통계를 계산할 때 유용하다.<br>이 값은 24시 기준으로 표현된다.                                             |
| MI                         | 해당 분을 두자리 숫자로 표현한다.                                                                                                                                                                        |
| MI2, MI5, MI10, MI20, MI30 | 해당 분을 MI 다음에 오는 숫자로 절삭한다.<br>즉, MI30을 사용한 경우에는 0분에서 29분까지는 0으로 표현되고, 30~59분까지는 30으로 표현된다.<br>이 표현은 시계열 상의 특정 시간 단위 통계를 계산할 때 유용하다.                                                         |
| SS                         | 해당 초를 두자리 숫자로 표현한다.                                                                                                                                                                        |
| SS2, SS5, SS10, SS20, SS30 | 해당 초를 이어지는 숫자로 절삭한다.<br>즉, SS30을 사용한 경우에는 0초에서 29초까지는 0으로 표현되고, 30~59초까지는 30으로 표현된다.<br><br><br>이 표현은 시계열 상의 특정 시간 단위 통계를 계산할 때 유용하다.                                                      |
| AM                         | 현재 시간이 오전, 오후에 따라 각각 AM 혹은 PM으로 표현한다.                                                                                                                                                      |
| mmm                        | 해당 시간의 mili second를 3자리 숫자로 표현한다.<br>값의 범위는 0~999이다.                                                                                                                                       |
| uuu                        | 해당 시간의 micro second를 3자리 숫자로 표현한다.<br>값의 범위는 0~999이다.                                                                                                                                      |
| nnn                        | 해당 시간의 nano second를 3자리 숫자로 표현한다.<br>값의 범위는 0~999이다.                                                                                                                                       |

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

### TO_CHAR : 지원하지 않는 타입

현재 Binary 타입에 대해서는 TO_CHAR를 지원하지 않는다.

왜냐하면, 일반 텍스트로 변환이 불가능하기 때문이다. 만일 이를 화면에 출력하고자 할 경우에는 TO_HEX() 함수를 통해 16진수 값을 출력해서 확인할 수 있다.

## TO_DATE

이 함수는 주어진 포맷 문자열로 표현된 문자열을 datetime 타입으로 변환한다.

format_string이 생략된 경우에는 기본값으로 "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" 을 사용해서 변환한다.

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

TO_DATE() 와 비슷하지만, 변환에 실패할 경우 에러를 내지 않고 NULL 을 반환한다.

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

이 함수는 컬럼의 값이 NULL이면 value를 리턴하고, NULL이 아니면 원래 컬럼의 값을 출력한다. 출력의 일관성을 보장하기 위해 short, int, long 타입의 경우에는 BIG ENDIAN 형태로 변환해서 출력해 준다.

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

이 함수는 주어진 문자열을 IP 버전4 타입으로 변환한다. 만일 해당 문자열이 숫자형으로 변환이 불가능할 경우에는 TO_IPV4() 함수는 에러를 리턴하고, 동작을 종료한다.

그러나, TO_IPV4_SAFE() 함수의 경우에는 에러 상황일 경우 NULL을 리턴하고, 동작을 계속할 수 있게 되어 있다.

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

이 함수는 주어진 문자열을 IP 버전6 타입으로 변환한다. 만일 해당 문자열이 숫자형으로 변환이 불가능할 경우에는 TO_IPV6() 함수는 에러를 리턴하고, 동작을 종료한다.

그러나, TO_IPV6_SAFE() 함수의 경우에는 에러 상황일 경우 NULL을 리턴하고, 동작을 계속할 수 있게 되어 있다.

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

이 함수는 주어진 문자열을 숫자형 double 타입으로 변환한다. 만일 해당 문자열이 숫자형으로 변환이 불가능할 경우에는 TO_NUMBER() 함수는 에러를 리턴하고, 동작을 종료한다.

그러나, TO_NUMBER_SAFE() 함수의 경우에는 에러 상황일 경우 NULL을 리턴하고, 동작을 계속할 수 있게 되어 있다.

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

## TO_TIMESTAMP

이 함수는 datetime 자료형을 1970-01-01 09:00 부터 경과된 nanosecond 데이터로 변환한다.

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

TRUNC 함수는 소수점 아래 n번째 자리에서 버림한 number를 반환한다. 

n이 생략될 경우 이를 0으로 취급하여 소수점 아래 자리는 모두 삭제한다. n이 음수일 경우 소수점 앞 n자리에서 버림한 값을 반환한다.

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

* Cluster Edition 에서는 사용할 수 없는 함수이다.

이 함수는 집계 함수로써, 특정 컬럼 값의 변경 횟수를 얻는다.

입력되는 데이터의 순서가 시간 순으로 입력된다는 것을 보장할 수 있어야 원하는 결과를 얻을 수가 있기 때문에 이 함수는 1) Join을 사용하거나 2) Inline view 를 사용한 경우에는 사용할 수가 없다.

현재 버전에서는 varchar를 제외한 타입만 지원한다.

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

UNIX_TIMESTAMP는 date타입의 값을 unix의 time() 시스템 호출이 변환하는 32비트 정수 값으로 변환하는 함수이다. (FROM_UNIXTIME은 반대로 정수형 데이터를 date 타입 값으로 변환하는 함수이다.)

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

이 함수는 주어진 영문 컬럼의 내용을 대문자로 변환한다.

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

이 함수는 집계 함수로써, 주어진 숫자형 컬럼 값들의 분산값을 리턴한다. Variance함수는 샘플에 대한 분산을, VAR_POP함수는 모집단에 대한 분산값을 리턴한다.

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

이 함수들은 입력된 datetime 컬럼값에서 해당하는 연, 월, 일을 추출하여 정수형 값으로 반환하는 함수이다.

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

이 함수는 인자로 받은 숫자형 값이 NaN / Inf 값인지를 판단한다. NaN / Inf 값인 경우 1 그렇지 않은 경우 0 을 반환한다.

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

## 내장 함수 지원 타입

|                            | Short | Integer | Long | Float | Double | Varchar | Text | Ipv4 | Ipv6 | Datetime | Binary |
| --------------------------: | :-----: | :-------: | :----: | :-----: | :------: | :-------: | :----: | :----: | :----: | :--------: | :------: |
| ABS                        | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |
| ADD_TIME                   | x     | x       | x    | x     | x      | x       | x    | x    | x    | o        | x      |
| AVG                        | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |
| BITAND / BITOR             | o     | o       | o    | x     | x      | x       | x    | x    | x    | x        | x      |
| COUNT                      | o     | o       | o    | o     | o      | o       | x    | o    | o    | o        | x      |
| DATE_TRUNC                 | x     | x       | x    | x     | x      | x       | x    | x    | x    | o        | x      |
| DECODE                     | o     | o       | o    | o     | o      | o       | x    | o    | x    | o        | x      |
| FIRST / LAST               | o     | o       | o    | o     | o      | o       | x    | o    | o    | o        | x      |
| FROM_UNIXTIME              | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |
| FROM_TIMESTAMP             | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |
| GROUP_CONCAT               | o     | o       | o    | o     | o      | o       | x    | o    | o    | o        | x      |
| INSTR                      | x     | x       | x    | x     | x      | o       | o    | x    | x    | x        | x      |
| LEAST / GREATEST           | o     | o       | o    | o     | o      | o       | x    | x    | x    | x        | x      |
| LENGTH                     | x     | x       | x    | x     | x      | o       | o    | x    | x    | x        | o      |
| LOWER                      | x     | x       | x    | x     | x      | o       | x    | x    | x    | x        | x      |
| LPAD / RPAD                | x     | x       | x    | x     | x      | o       | x    | x    | x    | x        | x      |
| LTRIM / RTRIM              | x     | x       | x    | x     | x      | o       | x    | x    | x    | x        | x      |
| MAX                        | o     | o       | o    | o     | o      | o       | x    | o    | o    | o        | x      |
| MIX                        | o     | o       | o    | o     | o      | o       | x    | o    | o    | o        | x      |
| NVL                        | x     | x       | x    | x     | x      | o       | x    | o    | x    | x        | x      |
| ROUND                      | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |
| ROWNUM                     | o     | o       | o    | o     | o      | o       | o    | o    | o    | o        | o      |
| SERIESNUM                  | o     | o       | o    | o     | o      | o       | o    | o    | o    | o        | o      |
| STDDEV / STDDEV_POP        | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |
| SUBSTR                     | x     | x       | x    | x     | x      | o       | x    | x    | x    | x        | x      |
| SUBSTRING_INDEX            | x     | x       | x    | x     | x      | o       | o    | x    | x    | x        | x      |
| SUM                        | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |
| SYSDATE / NOW              | x     | x       | x    | x     | x      | x       | x    | x    | x    | x        | x      |
| TO_CHAR                    | o     | o       | o    | o     | o      | o       | x    | o    | o    | o        | x      |
| TO_DATE / TO_DATE_SAFE     | x     | x       | x    | x     | x      | o       | x    | x    | x    | x        | x      |
| TO_HEX                     | o     | o       | o    | o     | o      | o       | o    | o    | o    | o        | o      |
| TO_IPV4 / TO_IPV4_SAFE     | x     | x       | x    | x     | x      | o       | x    | x    | x    | x        | x      |
| TO_IPV6 / TO_IPV6_SAFE     | x     | x       | x    | x     | x      | o       | x    | x    | x    | x        | x      |
| TO_NUMBER / TO_NUMBER_SAFE | x     | x       | x    | x     | x      | o       | x    | x    | x    | x        | x      |
| TO_TIMESTAMP               | x     | x       | x    | x     | x      | x       | x    | x    | x    | o        | x      |
| TRUNC                      | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |
| TS_CHANGE_COUNT            | o     | o       | o    | o     | o      | x       | x    | o    | o    | o        | x      |
| UNIX_TIMESTAMP             | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |
| UPPER                      | x     | x       | x    | x     | x      | o       | x    | x    | x    | x        | x      |
| VARIANCE / VAR_POP         | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |
| YEAR / MONTH / DAY         | x     | x       | x    | x     | x      | x       | x    | x    | x    | o        | x      |
| ISNAN / ISINF              | o     | o       | o    | o     | o      | x       | x    | x    | x    | x        | x      |

## JSON 관련 함수

이 함수들은 입력된 JSON 데이터 타입을 인자로 받아 사용한다.

| 함수명                                         | 설명                                                                                    | 비고                                                                                                                                       |
| ------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| JSON_EXTRACT(JSON 칼럼명, 'json path')         | 해당 값을 string type으로 출력한다.<br>(해당 객체가 없을 경우 ERROR를 출력한다.)                              | - JSON 객체 혹은 배열형 : 포함된 모든 객체를 문자열로 변환해서 리턴<br> - 문자열 : 그대로 리턴<br>- 숫자형 :문자열로 변환하여 리턴<br>- boolean 형 : "True" or "False" 리턴                        |
| JSON_EXTRACT_DOUBLE(JSON 칼럼명, 'json path')  | 해당 값을 부동소수점 64비트 double type으로 출력한다.<br>(해당 객체가 없을 경우 NULL을 출력한다.)                    | - JSON 객체 혹은 배열형 : NULL 리턴<br>- 문자열 : 변환하여 리턴하고, 변환 실패시 NULL 리턴<br>- 숫자형 : 64비트 실수 리턴<br>- boolean 형 : "True"는 1.0, "False"는 0.0 리턴              |
| JSON_EXTRACT_INTEGER(JSON 칼럼명, 'json path') | 해당 값을 64비트 integer type으로 출력한다.<br>(해당 객체가 없을 경우 NULL을 출력한다.)                         | - JSON 객체 혹은 배열형 : NULL 리턴<br>- 문자열 : 변환하여 리턴하고, 변환 실패시 NULL 리턴<br>- 숫자형 : 64비트 정수 리턴<br>- boolean 형 : "True"는 1 , "False"는 0 리턴                 |
| JSON_EXTRACT_STRING(JSON 칼럼명, 'json path')  | 해당 값을 string type으로 출력한다.<br>(해당 객체가 없을 경우 NULL을 출력한다.)<br>operator(->)와 같은 결과를 출력한다. | - JSON 객체 혹은 배열형 : 포함된 모든 객체를 문자열로 변환해서 리턴<br>- 문자열 : 그대로 리턴<br>- 숫자형 :문자열로 변환하여 리턴<br>- Boolean 형 : "True", "Fase" 리턴                           |
| JSON_IS_VALID('json string')                | json string이 json format에 유효한지 확인한다.                                                  | - 0 : False<br>- 1 : True                                                                                                                    |
| JSON_TYPEOF(JSON 칼럼명, 'json path')          | 해당 값의 타입을 반환한다.                                                                       | - None : 해당 키가 존재하지 않음<br>- Object : 객체형<br>- Integer : 정수형<br>- Real : 실수형<br>- String : 문자형<br>- True/False : Boolean<br>- Array :배열형<br>- Null : NULL |

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

JSON 데이터의 object에 접근할 때 '->' operator를 사용할 수 있다.

JSON_EXTRACT_STRING과 같은 결과를 반환한다.

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

## WINDOW 함수

WINDOW 함수란 행과 행 간 비교, 연산, 정의하기 위한 함수며, 분석함수 또는 순위함수라고 하기도 한다.

WINDOW 함수는 SELECT 구문에만 사용할 수 있다.

### WINDOW 함수 문법

윈도우 함수는 OVER 절을 필수로 포함한다.

```
WINDOW_FUNCTION (ARGUMENTS) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

* WINDOW_FUNCTION : 윈도우 함수 명
* ARGUMENTS : 함수에 따라 0 ~ N개 인수가 지정될 수 있다. 
* PARTITION BY 절 : 전체 집합을 기준에 의해 소그룹으로 나눌 수 있다.(생략 가능)
* ORDER BY 절 : 어떤 항목에 대해 정렬할 지 order by 절을 기술한다.(생략 가능)

### WINDOW 함수 종류

#### LAG

파티션별 윈도우에서 이전 N 번째 행의 값을 가져올 수 있다.

가져올 행이 존재하지 않으면 NULL을 리턴한다.

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

-- name 별로 집합을 나누고, dt 기준으로 정렬하여 1번째 이전 값을 가져온다.
Mach> SELECT name, dt, value, LAG(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lag_table;
name        dt                              value       LAG(value, 1) 
---------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           NULL          
name1       2024-01-02 00:00:00 000:000:000 2           1             
name1       2024-01-03 00:00:00 000:000:000 3           2             
[3] row(s) selected.
```


#### LEAD

파티션별 윈도우에서 이후 N 번째 행의 값을 가져올 수 있다. 

가져올 행이 존재하지 않으면 NULL을 리턴한다.

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

-- name 별로 집합을 나누고, dt 기준으로 정렬하여 1번째 이후 값을 가져온다.
Mach> SELECT name, dt, value, LEAD(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lead_table;
name        dt                              value       LEAD(value, 1) 
----------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           2              
name1       2024-01-02 00:00:00 000:000:000 2           3              
name1       2024-01-03 00:00:00 000:000:000 3           NULL           
[3] row(s) selected.
```
