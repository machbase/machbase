---
type: docs
title: '集約関数'
weight: 10
toc: true
---

集約関数は複数行の値から1つの結果を計算します。`GROUP BY`句と併用するとグループ別の集計結果を取得できます。`NULL`値は集計で無視します（COUNT(*)を除く）。

## クイックリファレンス

| 関数 | 構文 | 説明 |
|------|------|------|
| COUNT | `COUNT(*) / COUNT(col)` | 全行数、またはNULLでない行数 |
| SUM | `SUM(col)` | 合計 |
| AVG | `AVG(col)` | 平均 |
| MIN | `MIN(col)` | 最小値 |
| MAX | `MAX(col)` | 最大値 |
| STDDEV | `STDDEV(col)` | 標本標準偏差 |
| STDDEV_POP | `STDDEV_POP(col)` | 母標準偏差 |
| VARIANCE | `VARIANCE(col)` | 標本分散 |
| VAR_POP | `VAR_POP(col)` | 母分散 |
| FIRST | `FIRST(sort_expr, return_expr)` | ソート基準で最初のレコードの値 |
| LAST | `LAST(sort_expr, return_expr)` | ソート基準で最後のレコードの値 |
| SUMSQ | `SUMSQ(col)` | 二乗和 |
| MEDIAN | `MEDIAN(col)` | 中央値 |
| MODE | `MODE(col)` | 最頻値 |
| AREA | `AREA(y, x)` | 曲線の下の面積（台形積分） |
| SLOPE | `SLOPE(y, x)` | 線形回帰の傾き |
| GROUP_CONCAT | `GROUP_CONCAT(col ...)` | グループ内の値を文字列として連結 |
| TS_CHANGE_COUNT | `TS_CHANGE_COUNT(col)` | 値の変更回数 |
| TOP_K | `TOP_K(col, k)` | 頻度上位k個の値 |
| PERCENTILE_CONT | `PERCENTILE_CONT(col, ratio)` | 連続分位点 |
| PERCENTILE_DISC | `PERCENTILE_DISC(col, ratio)` | 離散分位点 |
| APPROX_PERCENTILE | `APPROX_PERCENTILE(col, ratio)` | 近似分位点 |
| CUME_DIST | `CUME_DIST(value, threshold)` | 累積分布比率 |

---

## COUNT

指定列のレコード数を求めます。`COUNT(*)`はNULLを含む全行数を、`COUNT(col)`は列の値がNULLでない行数を返します。

```sql
COUNT(*)
COUNT(column_name)
```

```sql
Mach> CREATE LOG TABLE count_table (id1 INTEGER, id2 INTEGER);
Mach> INSERT INTO count_table VALUES(1, 1);
Mach> INSERT INTO count_table VALUES(2, 2);
Mach> INSERT INTO count_table VALUES(null, 4);

Mach> SELECT COUNT(*) FROM count_table;
COUNT(*)
---------
3

Mach> SELECT COUNT(id1) FROM count_table;
COUNT(id1)
-----------
2
```

---

## SUM

数値列の合計を返します。

```sql
SUM(column_name)
```

```sql
Mach> SELECT c1, SUM(c2) FROM sum_table GROUP BY c1;
c1          SUM(c2)
--------------------
1           6
2           6
3           4
```

---

## AVG

数値列の平均値を返します。

```sql
AVG(column_name)
```

```sql
Mach> SELECT id1, AVG(id2) FROM avg_table GROUP BY id1;
id1         AVG(id2)
---------------------
1           2
2           2
NULL        4
```

---

## MIN

指定した数値列の最小値を返します。

```sql
MIN(column_name)
```

```sql
Mach> SELECT MIN(c1) FROM min_table;
MIN(c1)
--------
1
```

---

## MAX

指定した数値列の最大値を返します。

```sql
MAX(column_name)
```

```sql
Mach> SELECT MAX(c) FROM max_table;
MAX(c)
-------
30
```

---

## STDDEV / STDDEV_POP

入力列の標本標準偏差（STDDEV）と母標準偏差（STDDEV_POP）を返します。

```sql
STDDEV(column)
STDDEV_POP(column)
```

```sql
Mach> SELECT c2, STDDEV(c1) FROM stddev_table GROUP BY c2;
c2          STDDEV(c1)
-----------------------
1           0.707107
2           0.707107

Mach> SELECT c2, STDDEV_POP(c1) FROM stddev_table GROUP BY c2;
c2          STDDEV_POP(c1)
---------------------------
1           0.5
2           0.5
```

---

## VARIANCE / VAR_POP

標本分散（VARIANCE）と母分散（VAR_POP）を返します。

```sql
VARIANCE(column_name)
VAR_POP(column_name)
```

```sql
Mach> SELECT VARIANCE(c1) FROM var_table;
VARIANCE(c1)
--------------
0.333333

Mach> SELECT VAR_POP(c1) FROM var_table;
VAR_POP(c1)
-------------
0.25
```

---

## FIRST / LAST

各グループを`sort_expr`でソートしたとき、最初（FIRST）または最後（LAST）のレコードの`return_expr`値を返します。時系列データの特定時点の値を取得する場合に便利です。

```sql
FIRST(sort_expr, return_expr)
LAST(sort_expr, return_expr)
```

```sql
Mach> SELECT group_no, FIRST(id, name) FROM firstlast_table GROUP BY group_no;
group_no    first(id, name)
----------------------------
0           John
1           Grey

Mach> SELECT group_no, LAST(id, name) FROM firstlast_table GROUP BY group_no;
group_no    last(id, name)
---------------------------
0           Ryan
1           Kyle
```

---

## SUMSQ

数値の二乗和を返します。

```sql
SUMSQ(value)
```

```sql
Mach> SELECT c1, SUMSQ(c2) FROM sumsq_table GROUP BY c1;
c1          SUMSQ(c2)
----------------------
1           14
2           41
```

---

## MEDIAN

数値式の正確な中央値を返します。

```sql
MEDIAN(value)
```

```sql
SELECT MEDIAN(temp_c) FROM sensor_log;
```

---

## MODE

入力集合で最も頻度の高い数値（最頻値）を返します。最頻値が複数ある場合は最小の値を返します。

```sql
MODE(value)
```

```sql
SELECT MODE(alarm_code) FROM event_log;
```

---

## AREA

数値の`(x, y)`点からなる曲線の下の面積を台形積分で計算します。有効な点が2つ未満の場合はNULLを返します。

```sql
AREA(y, x)
```

```sql
SELECT AREA(power_kw, sample_sec) FROM power_log;
```

---

## SLOPE

数値の`(x, y)`点に対する線形回帰直線の傾きを計算します。`x`の分散が0、または有効なデータが不足する場合はNULLを返します。

```sql
SLOPE(y, x)
```

```sql
SELECT SLOPE(temp_c, sample_sec) FROM sensor_log;
```

---

## GROUP_CONCAT

グループ内の列値を文字列として連結して返します。

{{< callout type="warning" >}}
Cluster Editionでは使用できません。
{{< /callout >}}

```sql
GROUP_CONCAT(
    [DISTINCT] column
    [ORDER BY column [ASC | DESC] [, ...]]
    [SEPARATOR str_val]
)
```

```sql
Mach> SELECT GROUP_CONCAT(name) FROM concat_table GROUP BY id2;
G_NAMES
---------
Jack,Jack,Ram
Jill,Zara,John

Mach> SELECT GROUP_CONCAT(DISTINCT name SEPARATOR '.') FROM concat_table GROUP BY id2;
G_NAMES
---------
Jack.Ram
Jill.Zara.John
```

---

## TS_CHANGE_COUNT

時刻順に取り込まれた列値の変更回数を返します。VARCHAR型は非対応です。

{{< callout type="warning" >}}
Cluster Editionでは使用できません。
{{< /callout >}}

```sql
TS_CHANGE_COUNT(column)
```

```sql
Mach> SELECT id, TS_CHANGE_COUNT(ip) FROM ipcount_table GROUP BY id;
id          TS_CHANGE_COUNT(ip)
--------------------------------
1           4
2           2
```

---

## TOP_K

頻度の高い`k`個の数値を`value:count`形式の文字列で返します。頻度の降順、頻度が同じ場合は値の昇順でソートします。

```sql
TOP_K(value, k)
```

```sql
SELECT TOP_K(alarm_code, 3) FROM event_log;
-- 結果例: 101:532,205:317,301:90
```

---

## PERCENTILE_CONT / PERCENTILE_DISC

正確な分位点を計算する集約関数です。`ratio`は0.0以上1.0以下の定数である必要があります。

- `PERCENTILE_CONT`: ソート済みの隣接値の間を補間します。
- `PERCENTILE_DISC`: 実際の観測値の1つを選択します。

```sql
PERCENTILE_CONT(value, ratio)
PERCENTILE_DISC(value, ratio)
```

短縮形として`P05`、`P10`、`P90`、`P95`関数も提供します。

```sql
SELECT PERCENTILE_CONT(latency_ms, 0.95) AS p95,
       PERCENTILE_DISC(latency_ms, 0.50) AS p50
FROM api_log;

-- 短縮形
SELECT P05(response_ms), P95(response_ms) FROM web_log;
```

---

## APPROX_PERCENTILE

近似分位点関数です。データ量が非常に多く、わずかな誤差を許容できる場合に便利です。`APPROX_MEDIAN`、`APPROX_P05`、`APPROX_P10`、`APPROX_P90`、`APPROX_P95`の短縮形もあります。

```sql
APPROX_PERCENTILE(value, ratio)
APPROX_MEDIAN(value)
APPROX_P95(value)
```

```sql
SELECT APPROX_PERCENTILE(latency_ms, 0.95) AS ap95,
       APPROX_MEDIAN(latency_ms)            AS amedian
FROM api_log;
```

---

## CUME_DIST

`value`が`threshold`以下の行の累積比率（0.0 ~ 1.0）を返します。ウィンドウ関数ではなく集約関数です。

```sql
CUME_DIST(value, threshold)
```

```sql
SELECT CUME_DIST(latency_ms, 100) FROM api_log;
```
