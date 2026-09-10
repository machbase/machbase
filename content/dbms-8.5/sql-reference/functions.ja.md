---
title : '関数'
type: docs
weight: 70
tocSort: true
toc: true
---

## エラー処理 {#error-handling}

| 種類 | コード | 発生条件 |
|---|---|---|
| 引数の型 | `ERR-02036`、`ERR-02037` | 非数値を指定、または `PI` に引数を指定 |
| 実行時 | `ERR-02317` | `SQRT` の負数、`MOD` のゼロ除算、`LOG` の不正な底や値、`EXP`/`POWER` のオーバーフローなど |

入力が `NULL` の場合、結果も `NULL` です。

## ABS {#abs}

数値を正の値に変換し、実数として返します。

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


## ADD_TIME {#add_time}

DATETIME の加減算を行います。年、月、日、時、分、秒に対応し、ミリ秒、マイクロ秒、ナノ秒は未対応です。差分は「年/月/日 時:分:秒」で、各項目に正負の値を指定します。

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

すべての元データをソートせず、サイズを制限した要約を保持してパーセンタイルを推定します。大量データで、小さな近似誤差を許容できる場合に適しています。

```sql
APPROX_PERCENTILE(value, ratio)
APPROX_MEDIAN(value)
APPROX_P05(value)
APPROX_P10(value)
APPROX_P90(value)
APPROX_P95(value)
```

- `value` は数値。
- `ratio` は `0.0` ～ `1.0` の定数。
- 戻り値は `DOUBLE`。
- `NULL` は除外。

`APPROX_MEDIAN(value)` は近似中央値です。`APPROX_P05`、`APPROX_P10`、`APPROX_P90`、`APPROX_P95` は、各固定パーセンタイルの短縮形です。

```sql
SELECT APPROX_PERCENTILE(latency_ms, 0.95) AS ap95,
       APPROX_MEDIAN(latency_ms) AS amedian,
       APPROX_P05(latency_ms) AS ap05
FROM api_log;
```


## AREA {#area}

`AREA(y, x)` は、`(x, y)` の点列で構成する曲線の下の面積を正確に計算する集計関数です。

```sql
AREA(y, x)
```

- 両引数は数値。
- どちらかが `NULL` の行は除外。
- 有効な点が 2 つ未満なら `NULL`。
- 結果は `DOUBLE`。

```sql
SELECT AREA(power_kw, sample_sec)
FROM power_log;
```


## AVG {#avg}

数値列の平均を返す集計関数です。

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


## BITAND / BITOR {#bitand--bitor}

2 つの整数入力を 64 ビット符号付き整数に変換し、ビット AND/OR の結果を同じ型で返します。

負数の整数はプラットフォームによって結果が異なる場合があるため、uinteger と ushort の使用を推奨します。

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


## COUNT {#count}

指定列のレコード数を求める集計関数です。

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

`CUME_DIST(value, threshold)` は、`value` がしきい値以下の行の累積比率を返します。

```sql
CUME_DIST(value, threshold)
```

- ウィンドウ関数ではなく集計関数。
- 両引数は数値。
- `threshold` は定数。
- 結果は `0.0` ～ `1.0` の `DOUBLE`。

```sql
SELECT CUME_DIST(latency_ms, 100)
FROM api_log;
```


## DATE_TRUNC {#date_trunc}

日時を指定の単位と間隔に切りそろえ、新しい DATETIME として返します。

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

対応する単位と間隔の上限：

* ナノ秒、マイクロ秒、ミリ秒と略記は 5.5.6 以降で対応。
* 週は日曜日から開始。

| 単位 | 間隔の上限 |
|--|--|
| ナノ秒（nanosecond / nsec） | 1000000000（`1` 秒） |
| マイクロ秒（microsecond / usec） | 60000000（60 秒） |
| ミリ秒（milisecond / msec） | 60000（60 秒） |
| 秒（second / sec） | 86400（`1` 日） |
| 分（minute / min） | 1440（`1` 日） |
| 時間（hour） | 24（`1` 日） |
| 日（day） | `1` |
| 週（week） | `1` |
| 月（month） | `1` |
| 年（year） | `1` |

DATE_TRUNC('second', time, 120) は 2 分単位になり、DATE_TRUNC('minute', time, 2) と同じです。

## DATE_BIN {#date_bin}
指定した `origin` を基準に、DATETIME を
時間単位と間隔のバケットへ割り当てます。

```sql
DATE_BIN(field, count, source [, origin])
```

- `origin` があれば、その時刻から境界を計算。
- 省略時は、サーバーのローカルタイムゾーンの `1970-01-01 00:00:00` を
  基準に計算。
- `count` は `1` 以上の整数。

`DATE_TRUNC()`/`ROLLUP()` と同じローカル時刻の境界には 3 引数形式を使用します。
サーバーのタイムゾーンに依存しない固定の基準が必要なら、
4 引数形式を使用します。

例えば `UTC+09:00` では、以前は `DATE_BIN(..., 0)` の代わりに
タイムゾーンを調整した `origin` が必要でした。3 引数形式では、
同じローカル時刻への整列を直接指定できます。

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

3 引数形式の例です。

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

対応する時間単位：

* ナノ秒、マイクロ秒、ミリ秒と略記は 5.5.6 以降で対応。
* 週は 7 日。

| 時間単位 |
|----:|
| ナノ秒（nanosecond / nsec） |
| マイクロ秒（microsecond / usec） |
| ミリ秒（milisecond / msec） |
| 秒（second / sec） |
| 分（minute / min） |
| 時間（hour） |
| 日（day） |
| 週（week） |
| 月（month） |
| 年（year） |


## DAYOFWEEK {#dayofweek}

日時の曜日を表す整数を返します。

[TO_CHAR(time, 'DAY')](#to_char) と同じ曜日を、文字列ではなく整数で返します。

```sql
DAYOFWEEK(date_val)
```

対応する値：

| 値 | 曜日 |
|--|--|
|`0`|日曜日|
|`1`|月曜日|
|2|火曜日|
|3|水曜日|
|4|木曜日|
|5|金曜日|
|6|土曜日|


## DECODE {#decode}

列値と Search を比較し、一致すると直後の値を返します。一致がなければ Default、Default を省略した場合は `NULL` を返します。

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


## `EXTRACT_*` {#extract_}

バイナリーフレームからビットを取り出す補助関数です。
`EXTRACT_*` はビッグエンディアン、`EXTRACT_LE_*` はリトルエンディアンです。
`BINARY/VARBINARY` を入力し、`NULL` フレームには `NULL` を返します。

**エンディアンモデル**

- `EXTRACT_*`：MSB 優先。`bit 0` は `byte[0]` の最上位ビット。
- `EXTRACT_LE_*`：LSB 優先。`bit 0` は `byte[0]` の最下位ビット。
- ビット位置は、フレーム全体で `0` から数えます。

**共通規則**

- 単一ビット：`0 <= bit_pos < frame_bits`
- 範囲：`start_bit >= 0`、`1 <= bit_count <= 64`、
  `start_bit + bit_count <= frame_bits`
- `EXTRACT_FLOAT*` は 32 ビット、`EXTRACT_DOUBLE*` は 64 ビット。
- 符号付きは 2 の補数として解釈し、64 ビットへ
  符号拡張します。
- 範囲エラー：`ERR_QP_INVALID_ARG_VALUE`（`ERR-02229` 系）
- 引数型エラー：`ERR_QP_FUNCTION_ARG_TYPE`

### EXTRACT_BIT {#extract_bit}

```
EXTRACT_BIT(frame, bit_pos) / EXTRACT_LE_BIT(frame, bit_pos) → TINYINT
```

`1` ビットを `0` または `1` として返します。

```sql
-- frame = 0x80 (1000 0000)
SELECT EXTRACT_BIT(frame, 0)    AS be_bit0,
       EXTRACT_LE_BIT(frame, 0) AS le_bit0
FROM t;
```

### EXTRACT_LONG, EXTRACT_ULONG {#extract_long-extract_ulong}

```
EXTRACT_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LE_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LONG(frame, start_bit, bit_count) → BIGINT
EXTRACT_LE_LONG(frame, start_bit, bit_count) → BIGINT
```

`1`～64 ビットを符号なし、または 2 の補数の符号付き整数として取得します。

```sql
-- frame = 0x12 34
SELECT EXTRACT_ULONG(frame, 0, 16)    AS be_u16,  -- 0x1234
       EXTRACT_LE_ULONG(frame, 0, 16) AS le_u16   -- 0x3412
FROM t;
```

### EXTRACT_FLOAT,EXTRACT_DOUBLE {#extract_floatextract_double}

```
EXTRACT_FLOAT(frame, start_bit) → FLOAT
EXTRACT_LE_FLOAT(frame, start_bit) → FLOAT
EXTRACT_DOUBLE(frame, start_bit) → DOUBLE
EXTRACT_LE_DOUBLE(frame, start_bit) → DOUBLE
```

32/64 ビットを IEEE 754 の float/double として再解釈します。
指定範囲はフレーム内に収まる必要があります。

```sql
SELECT EXTRACT_FLOAT(frame, 0)      AS be_f32,
       EXTRACT_LE_FLOAT(frame, 0)   AS le_f32,
       EXTRACT_DOUBLE(frame, 64)    AS be_f64,
       EXTRACT_LE_DOUBLE(frame, 64) AS le_f64
FROM sensor_bin;
```

### EXTRACT_SCALED_DOUBLE {#extract_scaled_double}

```
EXTRACT_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
EXTRACT_LE_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
```

`1`～64 ビットを符号なし（`signed=0`）または符号付き（`signed=1`）の整数として読み、
`raw * scale + offset` を返します。

```sql
-- 20 ビットのセンサー値。倍率 0.01、オフセット -40.0
SELECT EXTRACT_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0)    AS be_value,
       EXTRACT_LE_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0) AS le_value
FROM t_bin;
```


## FIRST / LAST {#first--last}

グループ内の基準値で並べたとき、先頭または末尾レコードの指定値を返す集計関数です。

* FIRST：先頭のレコードの値。
* LAST：末尾のレコードの値。

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


## FROM_UNIXTIME {#from_unixtime}

整数の 32 ビット UNIXTIME を DATETIME に変換します。UNIX_TIMESTAMP は逆の変換です。

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


## FROM_TIMESTAMP {#from_timestamp}

1970-01-01 00:00:00 UTC（UTC+09:00 では 1970-01-01 09:00）からのナノ秒値を DATETIME に変換します。

TO_TIMESTAMP() は逆の変換です。

```sql
FROM_TIMESTAMP(nanosecond_time_value)
```

```sql
Mach> SELECT FROM_TIMESTAMP(1562302560007248869) FROM TEST;
FROM_TIMESTAMP(1562302560007248869)
--------------------------------------
2019-07-05 13:56:00 007:248:869
```

SYSDATE と NOW も同じ起点からの現在のナノ秒値なので、そのまま FROM_TIMESTAMP() に渡せます。

単に日時を表示する場合は不要ですが、ナノ秒値として演算した結果を日時に戻す際に役立ちます。

```sql
Mach> select sysdate, from_timestamp(sysdate) from test_tbl;
sysdate                         from_timestamp(sysdate)
-------------------------------------------------------------------
2019-07-05 14:00:59 722:822:443 2019-07-05 14:00:59 722:822:443
[1] row(s) selected.
 
Mach> select sysdate, from_timestamp(sysdate-1000000) from test_tbl;
sysdate                         from_timestamp(sysdate-1000000)
-------------------------------------------------------------------
2019-07-05 14:01:05 130:939:525 2019-07-05 14:01:05 129:939:525      -- 1 ms（1,000,000 ns）の差が生じる
[1] row(s) selected.
```


## GROUP_CONCAT {#group_concat}

グループ内の列値を連結した文字列を返す集計関数です。

{{< callout type="warning" >}}
Cluster Edition では使用できません。
{{< /callout >}}

```sql
GROUP_CONCAT(
     [DISTINCT] column
     [ORDER BY { unsigned_integer | column }
     [ASC | DESC] [, column ...]]
     [SEPARATOR str_val]
)
```

* DISTINCT：重複値を連結しない。
* `ORDER BY`：指定列で連結順を決定。
* SEPARATOR：区切り文字列。既定値はカンマ。

構文上の注意：

* 対象は `1` 式です。複数列は TO_CHAR() と連結演算子 || で `1` つにします。
* `ORDER BY` は対象以外の列や複数列も指定できます。
* SEPARATOR は文字列定数で、列は指定できません。

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


## INSTR {#instr}

文字列内のパターンの位置を、`1` 始まりの文字位置で返します。

* 見つからなければ `0`。
* 検索パターンが空または `NULL` なら `NULL`。

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


## LEAST / GREATEST {#least--greatest}

複数の列や値から、最小値（LEAST）または最大値（GREATEST）を返します。

引数が `1` つ以下ならエラーです。`NULL` があれば `NULL` を返すため、必要なら入力列を事前に変換してください。
BLOB/TEXT など比較できない型や、型変換できない組み合わせはエラーになります。

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


## LENGTH {#length}

文字列列の長さをバイト数で返します。

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


## LOWER {#lower}

英字を小文字に変換します。

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


## LPAD / RPAD {#lpad--rpad}

指定長になるまで、左（LPAD）または右（RPAD）に文字を追加します。

最後の char を省略すると空白を使用します。
元の値が指定長より長い場合は、先頭から指定長だけを返します。

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


## LTRIM / RTRIM {#ltrim--rtrim}

LTRIM は左、RTRIM は右から `pattern` に含まれる文字を取り除きます。含まれない文字で停止します。すべて除去した場合は `NULL` を返します。

`pattern` を省略すると空白を除去します。

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


## MAX {#max}

数値列の最大値を返す集計関数です。

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

正確な中央値を返します。現在の実装では `PERCENTILE_CONT(value, 0.5)` と同じです。

```sql
MEDIAN(value)
```

- `value` は数値。
- `NULL` は除外。
- 結果は `DOUBLE`。

```sql
SELECT MEDIAN(temp_c)
FROM sensor_log;
```


## MIN {#min}

数値列の最小値を返す集計関数です。

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


## NVL {#nvl}
 
列が `NULL` なら指定した代替値、そうでなければ元の値を返します。

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

## `NEXTVAL` {#nextval}

Lookup のシーケンス列の次の値を返します。

```sql
NEXTVAL(sequence_column)
```

- `INSERT` でのみ使用可能。
- 引数は `PROPERTY(SEQUENCE=...)` を設定した列。
- 定義と例は[シーケンス列](../ddl/#sequence-column)を参照。

```sql
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-a');
```


## ROUND {#round}

指定桁の次の桁で四捨五入します。桁を省略すると `0` です。負の桁を指定すると、小数点より左側を丸めます。

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


## ROWNUM {#rownum}

SELECT の結果行に番号を付けます。

サブクエリーやインラインビュー内でも使用できます。選択リストに付けた値を外側から参照するには、別名を指定します。

```sql
ROWNUM()
```

**使用できる句**

選択リスト、GROUP BY、`ORDER BY` に使用でき、`WHERE`/HAVING には直接使用できません。条件で番号を使う場合は、インラインビューで番号を生成し、外側から参照します。

| 使用可能 | 使用不可 |
|--|--|
| 選択リスト / GROUP BY / `ORDER BY` | `WHERE` / HAVING |

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

**ソートによる番号順の変化**

ROWNUM() は `ORDER BY` より前に評価されるため、ソート後の番号は連続しない場合があります。順番どおりに付けるには、インラインビューでソートし、外側で ROWNUM() を呼びます。

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


## SERIESNUM {#seriesnum}

SERIES BY でまとめた系列の番号を BIGINT で返します。SERIES BY がなければ常に `1` です。

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


## STDDEV / STDDEV_POP {#stddev--stddev_pop}

標本標準偏差と母標準偏差を返します。VARIANCE と VAR_POP の平方根にそれぞれ相当します。

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


## SUBSTR {#substr}

文字列の START 位置から SIZE 分を切り出します。

* START は `1` 始まり。`0` は `NULL`。
* SIZE が文字列長を超える場合、末尾まで返します。
SIZE を省略すると、文字列の長さを使用します。

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


## SUBSTRING_INDEX {#substring_index}

delim が `count` 回現れる位置までの部分文字列を返します。`count` が負なら末尾から数え、区切り位置から末尾までを返します。

`count` が `0`、または区切りがない場合は `NULL` を返します。

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


## SUM {#sum}

数値列の合計を返します。

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


## SUMSQ {#sumsq}

数値の二乗和を返します。

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


## SYSDATE / NOW {#sysdate--now}

SYSDATE は関数ではなく、システムの現在時刻を返す疑似列です。

NOW も同じ動作を提供します。

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


## TO_CHAR {#to_char}

値を文字列に変換します。型に応じて format_string を指定できます。BINARY は未対応です。

```sql
TO_CHAR(column)
```

**TO_CHAR：基本型**

基本型を次のように文字列へ変換します。

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

**TO_CHAR：浮動小数点**

* 5.5.6 以降で対応。

float と double を文字列へ変換します。
書式は「文字＋数値」で指定し、繰り返せません。

| 書式 | 説明 |
|--|--|
|F / f|小数点以下の桁数。最大 30。|
|N / `n`|小数点以下の桁数と、整数部の 3 桁ごとのカンマ。最大 30。|

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

**TO_CHAR：DATETIME**

DATETIME を任意の書式に変換します。各書式を組み合わせられます。

省略時は YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn です。

| 書式 | 説明 |
|--|--|
|YYYY|年を 4 桁で表示。|
|YY|年を 2 桁で表示。|
|MM|月を 2 桁で表示。|
|MON|月の 3 文字略記。例：JAN、FEB、MAY。|
|DD|日を 2 桁で表示。|
|DAY|曜日の 3 文字略記。例：SUN、MON。|
|IW|ISO 8601 に従う週番号（`1`～53）。週は月曜開始。年初は前年の最終週、年末は翌年の第 `1` 週になる場合がある。詳細は ISO 8601 を参照。|
|WW|曜日を考慮しない年の週番号（`1`～53）。`1` 月 `1`～7 日は `1`。|
|W|曜日を考慮しない月の週番号（`1`～5）。3 月 `1`～7 日は `1`。|
|HH|時を 2 桁で表示。|
|HH12|時を `1`～12 の 2 桁で表示。|
|HH24|時を 00～23 の 2 桁で表示。|
|HH2, HH3, HH6|HH の後の値の単位で切り下げ。HH6 なら `0`～5 時は `0`、6～11 時は 6。時間単位の統計に使用。24 時間基準。|
|MI|分を 2 桁で表示。|
|MI2, MI5, MI10, MI20, MI30|指定分単位で切り下げ。MI30 なら `0`～29 分は `0`、30～59 分は 30。期間集計に使用。|
|SS|秒を 2 桁で表示。|
|SS2, SS5, SS10, SS20, SS30|指定秒単位で切り下げ。SS30 なら `0`～29 秒は `0`、30～59 秒は 30。期間集計に使用。|
|AM|午前は AM、午後は PM。|
|mmm|ミリ秒を 3 桁で表示（`0`～999）。|
|uuu|マイクロ秒を 3 桁で表示（`0`～999）。|
|nnn|ナノ秒を 3 桁で表示（`0`～999）。|

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

**TO_CHAR：未対応の型**

BINARY は未対応です。

通常のテキストに変換できないため、画面で確認するには TO_HEX() で 16 進数にします。


## TO_DATE {#to_date}

指定書式の文字列を DATETIME に変換します。

省略時は YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn です。

```sql
-- 書式を省略した場合は YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn
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


## TO_DATE_SAFE {#to_date_safe}

TO_DATE() と同様ですが、変換失敗時にエラーではなく `NULL` を返します。

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


## TO_HEX {#to_hex}

値を 16 進文字列に変換します。入力が `NULL` なら `NULL` を返します。出力を統一するため、short、int、long はビッグエンディアンに変換します。

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


## TO_INET_STR {#to_inet_str}

`IPV4` をドット区切りの 10 進文字列へ変換します。

```sql
TO_INET_STR(ipv4_value)
```

```sql
SELECT TO_INET_STR(TO_IPV4('192.168.0.1'));
```


## TO_IPV4 / TO_IPV4_SAFE {#to_ipv4--to_ipv4_safe}

文字列を IPv4 に変換します。変換できない場合、TO_IPV4() はエラーで停止します。

TO_IPV4_SAFE() は失敗時に `NULL` を返し、処理を継続できます。

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


## TO_IPV6 / TO_IPV6_SAFE {#to_ipv6--to_ipv6_safe}

文字列を IPv6 に変換します。変換できない場合、TO_IPV6() はエラーで停止します。

TO_IPV6_SAFE() は失敗時に `NULL` を返し、処理を継続できます。

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


## TO_NUMBER / TO_NUMBER_SAFE {#to_number--to_number_safe}

文字列を `DOUBLE` に変換します。変換できない場合、TO_NUMBER() はエラーで停止します。

TO_NUMBER_SAFE() は失敗時に `NULL` を返し、処理を継続できます。

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

出現頻度の高い `k` 個の数値を、`value:count` のカンマ区切り文字列で返します。

```sql
TOP_K(value, k)
```

- `value` は数値。
- `k` は正の整数定数。
- `NULL` は除外。
- 結果は `VARCHAR`。
- 頻度の降順。同頻度なら値の昇順。

```sql
SELECT TOP_K(alarm_code, 3)
FROM event_log;
```

結果の例：

```text
101:532,205:317,301:90
```


## TO_TIMESTAMP {#to_timestamp}

DATETIME を、1970-01-01 00:00:00 UTC（UTC+09:00 では 1970-01-01 09:00）からのナノ秒値に変換します。

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


## TRUNC {#trunc}

小数点以下の `n` 桁で切り捨てます。

`n` の省略時は `0` で、小数部をすべて除きます。負の場合は、小数点より左の指定桁で切り捨てます。

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


## TS_CHANGE_COUNT {#ts_change_count}

特定の列値が変化した回数を求める集計関数です。

入力の時刻順を保証する必要があるため、JOIN やインラインビューとは併用できません。
現在は `VARCHAR` 以外の型をサポートします。

* **Cluster Edition では使用できません。**

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


## UNIX_TIMESTAMP {#unix_timestamp}

日時を UNIX の time() と同じ 32 ビット整数へ変換します。FROM_UNIXTIME は逆の変換です。

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


## UPPER {#upper}

英字を大文字に変換します。

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


## VARIANCE / VAR_POP {#variance--var_pop}

数値列の分散を返します。VARIANCE は標本分散、VAR_POP は母分散です。

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


## YEAR / MONTH / DAY {#year--month--day}

DATETIME から年、月、日を取り出し、整数で返します。

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


## ISNAN / ISINF {#isnan--isinf}

数値が `NaN` または `Inf` かを調べ、該当すれば `1`、それ以外は `0` を返します。

```sql
ISNAN(number)
ISINF(number)
```

次の例は、テーブルに `NaN` と `Inf` がすでにあることを前提にしています。
引用符なしの `nan`、`inf` は `INSERT` の有効な値ではありません。

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

## JSON_SET {#json_set}

指定パスに SQL スカラー値を JSON スカラーとして保存します。

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

注意事項：

- `path` は完全な JSONPath。
- `JSON_SET(..., path, NULL)` は JSON の `null` を保存。
- JSON 文書が `NULL` なら SQL の `NULL`。
- `path` が `NULL` または空ならエラー。
- オブジェクトのパスに対応。
- `$.items[0]` などの配列要素変更は未対応。

## JSON_SET_JSON {#json_set_json}

第 3 引数を JSON として解析し、オブジェクトまたは配列のサブツリーとして保存します。

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

注意事項：

- `path` は完全な JSONPath。
- 第 3 引数が SQL の `NULL` なら、結果も SQL の `NULL`。
- 不正な JSON はエラー。
- オブジェクトのパスに対応。
- 配列要素の変更は未対応。

## JSON_REMOVE {#json_remove}

JSON のメンバーまたはサブツリーを削除します。

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

注意事項：

- `path` は完全な JSONPath。
- 存在しないパスは何もしない。
- `JSON_REMOVE(..., '$')` は不可。
- JSON 文書が `NULL` なら SQL の `NULL`。

## `PI`() {#pi}

定数 π を `DOUBLE` で返します。

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

## `SQRT`() {#sqrt}

数値の平方根を返します。

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

## `POWER()` {#power}

`base` の `exponent` 乗を返します。

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

`POWER()` の別名です。

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

## `LOG`() {#log}

`LOG(n)` は自然対数、`LOG(base, n)` は底を指定した対数です。

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

自然対数 `ln(n)` を返します。

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

## `EXP`() {#exp}

e の `n` 乗を返します。

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

負の無限大方向へ切り下げます。

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

正の無限大方向へ切り上げます。

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

ラジアン入力の正弦を返します。

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

`SLOPE(y, x)` は、数値ペア `(x, y)` の線形回帰直線の傾きを返します。

```sql
SLOPE(y, x)
```

- 両引数は数値。
- `NULL` は除外。
- 有効な行が不足、または `x` の分散が `0` なら `NULL`。
- 結果は `DOUBLE`。

```sql
SELECT SLOPE(temp_c, sample_sec)
FROM sensor_log;
```

## COS() {#cos}

ラジアン入力の余弦を返します。

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

ラジアン入力の正接を返します。

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

## `MOD`() {#mod}

商を `0` 方向へ切り捨てた剰余を返します。

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

入力中で最も頻度の高い数値を返します。

```sql
MODE(value)
```

- `value` は数値。
- `NULL` は除外。
- 最高頻度が同じなら最小の値。
- 現在の結果型は `DOUBLE`。

```sql
SELECT MODE(alarm_code)
FROM event_log;
```

## `P05` / `P10` / `P90` / `P95` {#p05-p10-p90-p95}

よく使う正確なパーセンタイルの短縮形です。

```sql
P05(value)
P10(value)
P90(value)
P95(value)
```

- `value` は数値。
- `NULL` は除外。
- 結果は `DOUBLE`。

`P05`、`P10`、`P90`、`P95` は、`PERCENTILE_CONT`(`value`, `ratio`) の `ratio` が `0.05`、`0.10`、`0.90`、`0.95` の場合に相当します。

```sql
SELECT P05(response_ms),
       P10(response_ms),
       P90(response_ms),
       P95(response_ms)
FROM web_log;
```

## `PERCENTILE_CONT` / `PERCENTILE_DISC` {#percentile_cont-percentile_disc}

数値入力の正確なパーセンタイルを計算します。

```sql
PERCENTILE_CONT(value, ratio)
PERCENTILE_DISC(value, ratio)
```

- `value` は数値。
- `ratio` は `0.0`～`1.0` の定数。
- `PERCENTILE_CONT` は必要に応じて隣接値を補間。
- `PERCENTILE_DISC` は指定順位に対応する観測値を選択。
- 現在は両方とも `DOUBLE` を返す。

```sql
SELECT PERCENTILE_CONT(latency_ms, 0.95) AS pcont95,
       PERCENTILE_DISC(latency_ms, 0.95) AS pdisc95
FROM api_log;
```

## QUANTILE {#quantile}

正確な連続分位点を計算します。

```sql
QUANTILE(value, ratio)
```

- `value` は数値。
- `ratio` は `0.0`～`1.0` の定数。
- 結果は `DOUBLE`。
- 現在は `PERCENTILE_CONT` と同じ連続パーセンタイルの系統。

```sql
SELECT QUANTILE(cpu_usage, 0.75)
FROM host_metric;
```

## `RAND()` {#rand}

疑似乱数を生成します。

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

`RAND(seed)` は同じ `seed` なら決定的な結果になります。引数なしの `RAND()` はセッションの内部状態を使い、`[0,1)` の値を生成します。

## `REGEXP_LIKE` {#regexp_like}

文字列が正規表現に一致するかを真偽値で返します。
主に `WHERE` で使用します。

```sql
REGEXP_LIKE(source, pattern)
REGEXP_LIKE(source, pattern, match_param)
```

- `source` は `VARCHAR`。
- `pattern` は定数の `VARCHAR` 正規表現。
- `match_param` は任意の定数 `VARCHAR`。`c` は大文字小文字を区別、
  `i` は区別しません。既定は `c`。

```sql
SELECT *
FROM sensor_text
WHERE REGEXP_LIKE(message, 'error|warn', 'i');
```

## `REGEXP_INSTR` {#regexp_instr}

一致位置を `1` 始まりで返します。見つからない場合は
`0` を返します。

```sql
REGEXP_INSTR(source, pattern[, position[, occurrence[, return_pos[, match_param]]]])
```

- `source` は `VARCHAR`。
- `pattern` は定数の `VARCHAR` 正規表現。
- `position` と `occurrence` は `1` 以上の整数定数。
- `return_pos` は整数定数。`0` は開始位置、`1` は一致部分の
  直後の位置を返す。
- `match_param` は `c` または `i`。既定は `c`。

```sql
SELECT REGEXP_INSTR('TechOnTheNet', 'The', 1, 1, 1, 'i');
```

## `REGEXP_SUBSTR` {#regexp_substr}

正規表現に一致する部分文字列を返します。

```sql
REGEXP_SUBSTR(source, pattern[, position[, occurrence[, match_param]]])
```

- `source` は `VARCHAR`。
- `pattern` は定数の `VARCHAR` 正規表現。
- `position` と `occurrence` は `1` 以上の整数定数。
- `match_param` は `c` または `i`。既定は `c`。

```sql
SELECT REGEXP_SUBSTR('TechOnTheNet', 'a|e|i|o|u', 1, 2, 'i');
```

## `REGEXP_REPLACE` {#regexp_replace}

正規表現に一致するテキストを置換します。

```sql
REGEXP_REPLACE(source, pattern[, replacement[, position[, occurrence[, match_param]]]])
```

- `source` は `VARCHAR`。
- `pattern` と `replacement` は定数の `VARCHAR`。
- `replacement` を省略すると一致部分を削除。
- `position` は `1` 以上の整数定数。
- `occurrence` は整数定数。`0` は全一致を置換、正の値は
  指定した出現だけを置換。
- `match_param` は `c` または `i`。既定は `c`。

```sql
SELECT REGEXP_REPLACE('TechOnTheNet', 'a|e|i|o|u', 'Z', 1, 2, 'i');
```

## 組み込み関数の対応型 {#support-type-of-built-in-function}

| |Short|Integer|Long|Float|Double|Varchar|Text|Ipv4|Ipv6|Datetime|Binary|
|--|--|--|--|--|--|--|--|--|--|--|--|
|ABS|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|ADD_TIME|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|o|`x`|
|APPROX_PERCENTILE / APPROX_MEDIAN / `APPROX_P05` / `APPROX_P10` / `APPROX_P90` / `APPROX_P95`|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|AREA|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|AVG|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|BITAND / BITOR|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|
|COUNT|o|o|o|o|o|o|`x`|o|o|o|`x`|
|CUME_DIST|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|DATE_TRUNC|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|o|`x`|
|DECODE|o|o|o|o|o|o|`x`|o|`x`|o|`x`|
|FIRST / LAST|o|o|o|o|o|o|`x`|o|o|o|`x`|
|FROM_UNIXTIME|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|FROM_TIMESTAMP|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|GROUP_CONCAT|o|o|o|o|o|o|`x`|o|o|o|`x`|
|INSTR|`x`|`x`|`x`|`x`|`x`|o|o|`x`|`x`|`x`|`x`|
|LEAST / GREATEST|o|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|
|LENGTH|`x`|`x`|`x`|`x`|`x`|o|o|`x`|`x`|`x`|o|
|LOWER|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|LPAD / RPAD|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|LTRIM / RTRIM|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|MAX|o|o|o|o|o|o|`x`|o|o|o|`x`|
|MEDIAN|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|MIN|o|o|o|o|o|o|`x`|o|o|o|`x`|
|MODE|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|NVL|`x`|`x`|`x`|`x`|`x`|o|`x`|o|`x`|`x`|`x`|
|`P05` / `P10` / `P90` / `P95`|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|`PERCENTILE_CONT` / `PERCENTILE_DISC`|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|QUANTILE|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|`REGEXP_LIKE`|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|`REGEXP_INSTR`|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|`REGEXP_SUBSTR`|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|`REGEXP_REPLACE`|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|SLOPE|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|TOP_K|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|ROUND|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|ROWNUM|o|o|o|o|o|o|o|o|o|o|o|
|SERIESNUM|o|o|o|o|o|o|o|o|o|o|o|
|STDDEV / STDDEV_POP|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|SUBSTR|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|SUBSTRING_INDEX|`x`|`x`|`x`|`x`|`x`|o|o|`x`|`x`|`x`|`x`|
|SUM|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|SYSDATE / NOW|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|
|TO_CHAR|o|o|o|o|o|o|`x`|o|o|o|`x`|
|TO_DATE / TO_DATE_SAFE|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|TO_HEX|o|o|o|o|o|o|o|o|o|o|o|
|TO_INET_STR|`x`|`x`|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|
|TO_IPV4 / TO_IPV4_SAFE|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|TO_IPV6 / TO_IPV6_SAFE|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|TO_NUMBER / TO_NUMBER_SAFE|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|TO_TIMESTAMP|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|o|`x`|
|TRUNC|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|TS_CHANGE_COUNT|o|o|o|o|o|`x`|`x`|o|o|o|`x`|
|UNIX_TIMESTAMP|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|UPPER|`x`|`x`|`x`|`x`|`x`|o|`x`|`x`|`x`|`x`|`x`|
|VARIANCE / VAR_POP|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|
|YEAR / MONTH / DAY|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|`x`|o|`x`|
|ISNAN / ISINF|o|o|o|o|o|`x`|`x`|`x`|`x`|`x`|`x`|


## JSON 関数 {#json-related-function}

JSON を引数とする関数です。

| 関数 | 説明 | 備考 |
|--|--|--|
|JSON_EXTRACT(JSON column name, 'json path')|文字列を返す。存在しない場合はエラー。|オブジェクト/配列は文字列化、文字列はそのまま、数値は文字列化、真偽値は True/False。|
|JSON_EXTRACT_DOUBLE(JSON column name, 'json path')|64 ビット実数を返す。存在しない場合は `NULL`。|オブジェクト/配列は `NULL`。文字列は変換可能なら数値、不可能なら `NULL`。数値は実数、真偽値は `1.0`/`0.0`。|
|JSON_EXTRACT_INTEGER(JSON column name, 'json path')|64 ビット整数を返す。存在しない場合は `NULL`。|オブジェクト/配列は `NULL`。文字列は変換可能なら数値、不可能なら `NULL`。数値は整数、真偽値は `1`/`0`。|
|JSON_EXTRACT_STRING(JSON column name, 'json path')|文字列を返す。存在しない場合は `NULL`。`->` と同じ。|オブジェクト/配列と数値は文字列化、文字列はそのまま、真偽値は True/False。|
|JSON_SET(json_doc, `path`, scalar)|指定パスに SQL スカラーを JSON スカラーとして保存した新しい文書。|完全な JSONPath。`NULL` は JSON `null`。オブジェクトパスのみ。|
|JSON_SET_JSON(json_doc, `path`, json_text)|指定パスに JSON のオブジェクト/配列を保存した新しい文書。|完全な JSONPath。第 3 引数が SQL `NULL` なら SQL `NULL`。不正な JSON はエラー。|
|JSON_REMOVE(json_doc, `path`)|メンバーやサブツリーを削除した新しい文書。|完全な JSONPath。存在しないパスは何もしない。'$' の削除は不可。|
|JSON_IS_VALID('json string')|有効な JSON かを確認。|`0`：偽、`1`：真。|
|JSON_TYPEOF(JSON column name, 'json path')|値の型を返す。|None：キーなし、Object：オブジェクト、Integer：整数、Real：実数、String：文字列、True/False：真偽値、Array：配列、Null：`NULL`。|

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


## JSON 演算子 {#json-operator}

`->` で JSON のオブジェクトにアクセスします。

JSON_EXTRACT_STRING と同じ結果を返します。

```sql
json_col -> 'json path'
```

JSONPath の `->` またはドット省略記法を使用できます。

```sql
-- JSONPath の矢印構文
jval->'$.sensor.temperature'

-- JSON のドット省略記法
jval.sensor.temperature
```

どちらも同じ値を参照します。従来の `->` は引き続き利用でき、ドット記法は同じパスを短く記述する追加構文です。

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

### JSONPath の矢印構文 {#jsonpath-arrow-syntax}

JSONPath 文字列を指定します。

```sql
jval->'$.name'
jval->'$.sensor.temperature'
jval->'$.items[0].name'
```

角括弧でキーを直接指定することもできます。キーに `.` を含む場合に使用します。

```sql
-- キー名は a.b
jval->'$["a.b"]'
jval->'$[a.b]'

-- 角括弧による複数階層
jval->'$[Plant1][Line1][Temperature]'

-- ドットを含む単一キー
jval->'$[Plant1.Line1.Temperature]'
```

`$[Plant1.Line1.Temperature]` は、`Plant1.Line1.Temperature` という単一キーを参照します。入れ子なら `$[Plant1][Line1][Temperature]` または `$.Plant1.Line1.Temperature` を使用します。

特殊文字やドットを含むキーには、引用符付きの角括弧表記を推奨します。

```sql
jval->'$["a.b"]["c.d"]["e.f"]'
```

次の構文は未対応です。

```sql
jval->'$."a.b"'
```

### JSON のドット省略記法 {#json-dot-shorthand}

JSON 列の後ろにメンバー名を連結します。

```sql
-- 単一メンバー
jval.name

-- 入れ子のメンバー
jval.sensor.temperature

-- 配列添字
jval.items[0].name

-- 特殊文字を含むキー
jval.items[0]."product-id"
```

二重引用符で囲むと、大文字小文字と特殊文字を維持します。

```sql
SELECT name, jval."Camel-Key", jval.items[0]."product-id"
  FROM jsontbl
 ORDER BY name;
```

### `WHERE` の型比較 {#type-comparison-in-where}

メンバー取得の結果は文字列のように表示されますが、`WHERE` で SQL の数値と比較する場合は、JSON 値を解析して数値比較します。

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

対応する比較：

- JSON 整数と SQL 整数
- JSON 実数と SQL 数値
- JSON の数値文字列と SQL 数値
- JSON 真偽値と文字列 `'true'` / `'false'`
- `=`、`<>`、`<`、`<=`、`>`、`>=`、`BETWEEN`、リテラル `IN (...)` 

JSON 整数と SQL 整数は整数として比較するため、`9007199254740992` と `9007199254740993` のように `DOUBLE` 精度を超える値も区別できます。

文字列との比較は、従来の文字列比較を使用します。

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.name' = 'test1'
 ORDER BY name;
```

数値比較時に解析できない JSON 値は、不一致となりエラーにはなりません。通常の `VARCHAR` の比較規則は変わらず、自動数値比較は JSON メンバーアクセスだけに適用します。

### 名前解決 {#name-resolution}

通常の SQL 列名の解決を優先します。

```sql
SELECT t.jval.name
  FROM jsontbl t;
```

通常の列参照として解決できず、`jval` が JSON 列の場合、`jval.name` をメンバーアクセスとして扱います。

ドットアクセスの基点は JSON 列に限ります。

```sql
-- 未サポート
(jval->'$.sensor').temperature
name.member
```

### 制限 {#limitations}

次は未対応です。

- ワイルドカード：`jval.items[*].name`
- 再帰探索：`jval..name`
- フィルター式：`jval.items[?(@.price > 10)]`
- 負の配列添字：`jval.items[-1]`
- 単一引用符のキー：`jval.'product-id'`
- ドットと矢印の混在：`jval.items->'$.name'`
- JSON 以外の列：`name.member`
- 任意の式の後のドット：`(jval->'$.sensor').temperature`
- 矢印パスの引用メンバー：`jval->'$."a.b"'`

`IN (SELECT ...)` のサブクエリーでは JSON の自動数値比較は未対応です。リテラル `IN (...)` を使用してください。

## ウィンドウ関数 {#window-function}

行間の比較や計算を行う関数で、分析関数やランキング関数とも呼びます。

SELECT でのみ使用できます。

### 構文 {#window-function-syntax}

OVER 句は必須です。

```
WINDOW_FUNCTION (ARGUMENTS) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

* WINDOW_FUNCTION：関数名。
* ARGUMENTS：関数に応じて `0`～N 個の引数。
* PARTITION BY：条件ごとに小グループへ分割（省略可）。
* `ORDER BY`：グループ内の並び順（関数により省略可）。

### 関数一覧 {#window-function-list}

#### LAG {#lag}

パーティション内の N 行前の値を取得します。

対象行がなければ `NULL` です。

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

-- name で分割し dt 順に並べ、1 行前の値を取得
Mach> SELECT name, dt, value, LAG(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lag_table;
name        dt                              value       LAG(value, 1) 
---------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           NULL          
name1       2024-01-02 00:00:00 000:000:000 2           1             
name1       2024-01-03 00:00:00 000:000:000 3           2             
[3] row(s) selected.
```


#### LEAD {#lead}

パーティション内の N 行後の値を取得します。

対象行がなければ `NULL` です。

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

-- name で分割し dt 順に並べ、1 行後の値を取得
Mach> SELECT name, dt, value, LEAD(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lead_table;
name        dt                              value       LEAD(value, 1) 
----------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           2              
name1       2024-01-02 00:00:00 000:000:000 2           3              
name1       2024-01-03 00:00:00 000:000:000 3           NULL           
[3] row(s) selected.
```


#### NTILE {#ntile}

並べた行をできるだけ均等な `n` バケットに分け、各行のバケット番号を返します。

```
NTILE(n) OVER ([PARTITION BY column_name] ORDER BY column_name)
```

- `n` は正の定数。
- OVER 内の `ORDER BY` が必須。
- 割り切れない場合、先のバケットに `1` 行多く割り当てる。

```
Mach> SELECT user_id,
             score,
             NTILE(4) OVER (ORDER BY score) AS score_band
      FROM exam_result;
```
