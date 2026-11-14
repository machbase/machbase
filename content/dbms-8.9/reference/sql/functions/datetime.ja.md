---
type: docs
title: '日付/時刻関数'
weight: 50
toc: true
---

Machbaseの`DATETIME`型は、1970-01-01 00:00:00 UTCからの経過時間をナノ秒値で内部保存します。日付/時刻関数は、この値を読みやすい形式へ変換したり、算術演算を行ったりします。

## クイックリファレンス

| 関数 | 構文 | 説明 |
|------|------|------|
| SYSDATE / NOW | `SYSDATE`, `NOW` | 現在のシステム時刻を返す |
| TO_DATE | `TO_DATE(str [, fmt])` | 文字列をDATETIMEへ変換 |
| TO_DATE_SAFE | `TO_DATE_SAFE(str [, fmt])` | 変換失敗時にNULLを返す |
| TO_CHAR | `TO_CHAR(col [, fmt])` | DATETIMEを文字列へ変換 |
| ADD_TIME | `ADD_TIME(col, diff)` | 日付/時刻の加減算 |
| DATE_TRUNC | `DATE_TRUNC(unit, col [, count])` | 指定単位で時刻を切り捨て |
| DATE_BIN | `DATE_BIN(unit, count, col [, origin])` | 指定した基準で時刻をバケット化 |
| DAYOFWEEK | `DAYOFWEEK(col)` | 曜日番号を返す（0=日曜日） |
| YEAR / MONTH / DAY | `YEAR(col)`, `MONTH(col)`, `DAY(col)` | 年、月、日を抽出 |
| FROM_UNIXTIME | `FROM_UNIXTIME(unix_ts)` | Unixタイムスタンプ（32ビット）をDATETIMEへ変換 |
| UNIX_TIMESTAMP | `UNIX_TIMESTAMP(col)` | DATETIMEをUnixタイムスタンプ（32ビット）へ変換 |
| FROM_TIMESTAMP | `FROM_TIMESTAMP(ns)` | ナノ秒整数をDATETIMEへ変換 |
| TO_TIMESTAMP | `TO_TIMESTAMP(col)` | DATETIMEをナノ秒整数へ変換 |

---

## SYSDATE / NOW

現在のシステム時刻を返す疑似列です。`SYSDATE`と`NOW`は同じ値を返します。

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

指定した書式文字列に従って文字列を`DATETIME`型へ変換します。書式を省略すると、デフォルトの`YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`を使用します。

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

変換失敗時にエラーではなくNULLを返す`TO_DATE_SAFE()`も提供します。

```sql
Mach> SELECT TO_DATE_SAFE('2016-12-32', 'YYYY-MM-DD');
NULL
```

---

## TO_CHAR (DATETIME)

`DATETIME`列の値を指定形式の文字列へ変換します。書式を省略すると、デフォルトの`YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`を使用します。

```sql
TO_CHAR(datetime_col [, format_string])
```

### 書式文字列

| 書式指定子 | 説明 |
|------------|------|
| `YYYY` | 4桁の年 |
| `YY` | 2桁の年 |
| `MM` | 2桁の月（`01~12`） |
| `MON` | 月の英語3文字略称（JAN, FEB, ...） |
| `DD` | 2桁の日 |
| `DAY` | 曜日の英語3文字略称（SUN, MON, ...） |
| `IW` | ISO 8601の週番号（`1~53`、月曜日基準） |
| `WW` | 年内の週番号（`1~53`、曜日に依存しない） |
| `W` | 月内の週番号（`1~5`、曜日に依存しない） |
| `HH` | 2桁の時 |
| `HH12` | 12時間制の時（`1~12`） |
| `HH24` | 24時間制の時（`0~23`） |
| `HH2`, `HH3`, `HH6` | 指定単位で時刻を切り捨て |
| `MI` | 2桁の分 |
| `MI2`, `MI5`, `MI10`, `MI20`, `MI30` | 指定単位で分を切り捨て |
| `SS` | 2桁の秒 |
| `SS2`, `SS5`, `SS10`, `SS20`, `SS30` | 指定単位で秒を切り捨て |
| `AM` | AM/PM |
| `mmm` | 3桁のミリ秒（`0~999`） |
| `uuu` | 3桁のマイクロ秒（`0~999`） |
| `nnn` | 3桁のナノ秒（`0~999`） |

```sql
Mach> SELECT TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS') FROM datetime_table;
2014-12-30 11:22:33
2013-11-11 01:02:03

Mach> SELECT TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.uuu.nnn') FROM datetime_table;
2014-12-30 11:22:33 444.555.666
```

---

## ADD_TIME

`DATETIME`列に年/月/日/時/分/秒単位の加減算を行います。ミリ秒・マイクロ秒・ナノ秒単位はサポートしません。

```sql
ADD_TIME(column, time_diff_format)
```

`time_diff_format`形式: `"Year/Month/Day Hour:Minute:Second"`（各項目は正数または負数）

```sql
-- 1年後
Mach> SELECT ADD_TIME(dt, '1/0/0 0:0:0') FROM t;

-- 1時間1分1秒後
Mach> SELECT ADD_TIME(dt, '0/0/0 1:1:1') FROM t;

-- 1年1か月1日前
Mach> SELECT ADD_TIME(dt, '-1/-1/-1 0:0:0') FROM t;
```

---

## DATE_TRUNC

`DATETIME`値を指定時間単位に切り捨てて返します。`count`を指定すると、その倍数単位で切り捨てます。

```sql
DATE_TRUNC(field, date_val [, count])
```

### 対応する時間単位と最大範囲

| 時間単位 | 最大範囲 |
|-----------|----------|
| `nanosecond` (`nsec`) | 1,000,000,000 (1秒) |
| `microsecond` (`usec`) | 60,000,000 (60秒) |
| `millisecond` (`msec`) | 60,000 (60秒) |
| `second` (`sec`) | 86,400 (1日) |
| `minute` (`min`) | 1,440 (1日) |
| `hour` | 24 (1日) |
| `day` | 1 |
| `week` | 1 (日曜日開始) |
| `month` | 1 |
| `year` | 1 |

```sql
-- 秒単位で切り捨て
Mach> SELECT COUNT(*), DATE_TRUNC('second', i2) tm FROM t GROUP BY tm ORDER BY 2;

-- 2秒単位で切り捨て
Mach> SELECT COUNT(*), DATE_TRUNC('second', i2, 2) tm FROM t GROUP BY tm ORDER BY 2;

-- 2分単位で切り捨て（DATE_TRUNC('second', time, 120)と同じ）
Mach> SELECT COUNT(*), DATE_TRUNC('minute', ts, 2) tm FROM t GROUP BY tm;
```

---

## DATE_BIN

基準時刻`origin`を基点に、`DATETIME`値を指定した時間単位と幅のバケットへ割り当てます。`origin`を省略すると、ローカルタイムゾーンの`1970-01-01 00:00:00`を使用します。

```sql
DATE_BIN(field, count, source [, origin])
```

```sql
-- 2時間バケット（指定したorigin基準）
SELECT DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00')) FROM log ORDER BY time;

-- 3時間バケット（ローカルタイムゾーンの境界基準）
SELECT DATE_BIN('hour', 3, ts) FROM t ORDER BY ts;
```

---

## DAYOFWEEK

`DATETIME`値の曜日を整数で返します。

```sql
DAYOFWEEK(date_val)
```

| 戻り値 | 曜日 |
|--------|------|
| 0 | 日曜日 |
| 1 | 月曜日 |
| 2 | 火曜日 |
| 3 | 水曜日 |
| 4 | 木曜日 |
| 5 | 金曜日 |
| 6 | 土曜日 |

```sql
SELECT DAYOFWEEK(dt) FROM log_table;
```

---

## YEAR / MONTH / DAY

入力`DATETIME`値から年、月、日を抽出して整数で返します。

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

`FROM_UNIXTIME`は32ビットのUnixタイムスタンプ整数を`DATETIME`へ変換します。`UNIX_TIMESTAMP`は逆に`DATETIME`を32ビットのUnixタイムスタンプへ変換します。

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

`FROM_TIMESTAMP`は1970-01-01 00:00:00 UTCからの経過ナノ秒数を表す整数を`DATETIME`へ変換します。
`TO_TIMESTAMP`は逆に`DATETIME`を同じ基準時点からの経過ナノ秒数の整数へ変換します。

基準時点はUTC+09:00では1970-01-01 09:00:00と表示されます。
次の例の日付と時刻はUTC+09:00基準です。

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

ナノ秒単位の算術演算例:

```sql
-- 現在時刻の1ms（1,000,000 ns）前
SELECT FROM_TIMESTAMP(SYSDATE - 1000000) FROM t;
```
