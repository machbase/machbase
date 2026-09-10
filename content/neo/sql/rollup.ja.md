---
title: ロールアップ
type: docs
weight: 11
toc: true
---

## はじめに {#introduction}

大規模な時系列データの統計値を取得する場合、対象範囲が広がるほど計算コストが増加します。Machbase の **Rollup** は、TAG テーブルのデータを時間区間ごとに事前集計し、高速に検索する機能です。定義したダウンサンプリング周期で自動集計するため、よく使用する統計値をすぐに取得できます。

## 基本概念 {#core-concepts}

**Rollup テーブル**は、元の TAG テーブルまたは別の Rollup テーブルを基に、Machbase が内部で事前計算した集計結果を格納します。クエリ実行時に、負荷の高い集計処理を繰り返す必要がなくなります。

### 標準の集計関数 {#supported-aggregations}

- `MIN()`: 区間内の最小値。
- `MAX()`: 区間内の最大値。
- `SUM()`: 区間内の合計。
- `COUNT()`: 区間内のデータ件数。
- `AVG()`: 区間内の平均値。
- `SUMSQ()`: 値の二乗和。

### 拡張集計関数（オプション） {#extended-aggregations-optional}

Rollup 作成時に `EXTENSION` を指定すると、次の関数も使用できます。

- `FIRST()`: 区間内の最初の値。
- `LAST()`: 区間内の最後の値。

### 時間単位 {#time-granularity}

Rollup は固定の時間間隔で動作し、基本単位は秒（SEC）、分（MIN）、時（HOUR）です。日、週、月、年などの大きい単位も、内部で HOUR などの適切な基本単位に対応付けて処理します。

## Rollup テーブルの種類 {#rollup-table-types}

### デフォルト Rollup {#default-rollup}

- TAG テーブル作成時の `WITH ROLLUP` 句で自動作成します。
- 最小単位に応じて秒・分・時のテーブルを作成します。たとえば `WITH ROLLUP (MIN)` では分・時の Rollup を作成します。
- テーブル名は `_<元のテーブル名>_ROLLUP_SEC` の形式で自動生成します。
- 1 つの TAG テーブルに作成できるデフォルト Rollup は 1 セットだけです。

### カスタム Rollup {#custom-rollup}

- `CREATE ROLLUP` 文で明示的に作成します。
- 10 秒、5 分など、必要な間隔を指定できます。
- TAG テーブルだけでなく、別の Rollup テーブルをソースに指定して、多段の集計構造を作成できます。

## Rollup テーブルの作成 {#creating-rollup-tables}

### デフォルト Rollup の作成 {#default-rollup-creation}

```sql
CREATE TAG TABLE table_name (
    name_column datatype PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column numeric_datatype [SUMMARIZED],
    ...
)
WITH ROLLUP [ ( SEC | MIN | HOUR ) ] [ EXTENSION ];
```

- 括弧内には最も細かい単位を指定します。省略時は秒（SEC）です。
- `EXTENSION` を付けると、`FIRST()` と `LAST()` を使用できます。

例:

```sql
-- 秒・分・時の Rollup を作成
CREATE TAG TABLE sensor_data (...) WITH ROLLUP;

-- 分・時の Rollup を作成
CREATE TAG TABLE hourly_stats (...) WITH ROLLUP (MIN);

-- 時の Rollup だけを作成
CREATE TAG TABLE daily_summary (...) WITH ROLLUP (HOUR);

-- 拡張関数を有効化
CREATE TAG TABLE detailed_sensor_data (...) WITH ROLLUP EXTENSION;
```

### カスタム Rollup の作成 {#custom-rollup-creation}

```sql
CREATE ROLLUP rollup_name
ON source_table_or_rollup ( value_column )
INTERVAL interval_value ( SEC | MIN | HOUR )
[ EXTENSION ];
```

- `rollup_name`: 作成する Rollup の名前。
- `SEC | MIN | HOUR`: 集計間隔の単位。
- `source_table_or_rollup`: 元の TAG テーブルまたは既存の Rollup テーブル。
- `value_column`: ソースが TAG テーブルの場合に集計対象の数値列を指定します。Rollup の場合は省略します。
- `interval_value`: 集計間隔の数値。
- `EXTENSION`: 拡張関数（FIRST/LAST）を有効にします。

**注意事項**

- ソースが Rollup テーブルの場合、新しい間隔はソースの間隔の倍数で、より大きい単位にする必要があります。

例:

```sql
-- 30 秒間隔の Rollup を作成
CREATE ROLLUP _tag_data_rollup_30sec ON tag_data(value) INTERVAL 30 SEC;

-- 上位の Rollup（10 分）
CREATE ROLLUP _tag_data_rollup_10min ON _tag_data_rollup_30sec INTERVAL 10 MIN;

-- 15 分間隔、拡張関数あり
CREATE ROLLUP _tag_data_rollup_15min_ext ON tag_data(value) INTERVAL 15 MIN EXTENSION;
```

## Rollup データの検索 {#querying-rollup-data}

Rollup テーブルを使用するには `ROLLUP()` 関数を指定します。Machbase が適切な Rollup テーブルを自動選択します。旧 `ROLLUP` キーワード構文もありますが非推奨です。

推奨する一般構文は次のとおりです。

```sql
SELECT
    ROLLUP( time_unit, period, basetime_column [, origin ] ) AS rollup_time,
    AGGREGATE_FUNCTION( value_column ) AS aggregate_result
    [, other_aggregates... ]
FROM
    source_tag_table
WHERE
    [ time_range_predicate ]
    [ AND name_predicate ]
    [ AND other_predicates... ]
GROUP BY
    rollup_time -- ROLLUP(...) 式を直接指定することも可能
ORDER BY
    rollup_time;
```

時間単位の MIN/MAX の記述例です。

```sql
SELECT
    ROLLUP('hour', 1, time) AS rollup_time,
    MIN(value),
    MAX(value)
FROM tag_table
WHERE ...
GROUP BY rollup_time
ORDER BY rollup_time;
```

- 第 1 引数: 単位（'sec'、'min'、'hour'、'day'、'week'、'month'、'year' など）。
- 第 2 引数: 単位の倍数。使用する Rollup テーブルの間隔の有効な倍数である必要があります。
- 第 3 引数: `BASETIME` 列。
- 第 4 引数: 省略可能な起点時刻（origin）。デフォルトは `1970-01-01 00:00:00` です。時間区間の境界をそろえる DATETIME リテラルで、週・月・年の区切りを指定する際に使用します。

`ROLLUP()` を含む列は必ず `GROUP BY` に指定し、`MIN`、`MAX`、`AVG`、`SUM`、`COUNT`、`SUMSQ`、`FIRST`、`LAST` などの集計関数と組み合わせて使用します。

検索例:


```sql
-- 指定月の TAG_00001 の時間単位の MIN と MAX
SELECT
    ROLLUP('hour', 1, time) as mtime,
    MIN(value),
    MAX(value)
FROM TAG
WHERE name = 'TAG_00001'
  AND time BETWEEN TO_DATE('2023-01-01 00:00:00') AND TO_DATE('2023-01-31 23:59:59')
GROUP BY mtime
ORDER BY mtime;

-- MIN または SEC の Rollup を使用した 15 分平均
SELECT
    ROLLUP('min', 15, time) AS rollup_interval,
    AVG(value)
FROM TAG
WHERE name = 'SENSOR_A'
GROUP BY rollup_interval
ORDER BY rollup_interval;

-- 拡張 Rollup の日別 FIRST と LAST。起点は 2024 年 1 月 1 日
SELECT
    ROLLUP('day', 1, time, '2024-01-01') as day_interval,
    FIRST(time, value),
    LAST(time, value)
FROM TAG_WITH_EXTENSION
WHERE name = 'SENSOR_B'
GROUP BY day_interval
ORDER BY day_interval;

-- 月曜日（2024-01-01）を起点とする週平均
SELECT
    ROLLUP('week', 1, time, '2024-01-01') AS week_start,
    AVG(value)
FROM TAG
WHERE name = 'SENSOR_C'
GROUP BY week_start
ORDER BY week_start;
```

## Rollup の管理 {#managing-rollup-tables}

### 実行制御 {#lifecycle-control}

```sql
-- 指定した Rollup の集計スレッドを開始
EXEC ROLLUP_START('rollup_name');
-- 指定した Rollup の集計スレッドを停止
EXEC ROLLUP_STOP('rollup_name');
-- 通常の待機時間を省き、未処理データを直ちに集計
EXEC ROLLUP_FORCE('rollup_name');
```

- `ROLLUP_FORCE` は待機時間を無視して、直ちに集計を実行します。

実行例:

```sql
EXEC ROLLUP_START('_tag_data_rollup_30sec');
EXEC ROLLUP_STOP('_tag_data_rollup_10min');
EXEC ROLLUP_FORCE('_tag_rollup_hour'); -- 時間単位の未処理データを集計
```

### Rollup データの削除 {#rollup-data-deletion}

```sql
DELETE FROM table_name ROLLUP; -- すべて削除
DELETE FROM table_name ROLLUP BEFORE TO_DATE('YYYY-MM-DD HH24:MI:SS');
DELETE FROM table_name ROLLUP WHERE name = 'TAG01';
DELETE FROM table_name ROLLUP WHERE name = 'TAG01' AND time <= TO_DATE(...);
```

元の TAG テーブルからデータを削除しても Rollup データは自動削除されないため、別途削除する必要があります。

削除例:

```sql
-- 2024 年 1 月 15 日より前の Rollup データを削除
DELETE FROM TAG ROLLUP BEFORE TO_DATE('2024-01-15 00:00:00');
-- TAG01 の Rollup データをすべて削除
DELETE FROM TAG ROLLUP WHERE name = 'TAG01';
```

### Rollup テーブルの削除 {#rollup-table-deletion}

```sql
DROP ROLLUP rollup_name;          -- カスタム Rollup を削除
DROP TABLE tag_table CASCADE;     -- TAG テーブルと関連 Rollup をまとめて削除
```

他の Rollup から参照される Rollup を削除する場合は、依存する Rollup を先に削除してください。

削除順序の例:

```sql
-- _rollup_min が _rollup_sec に依存する場合
DROP ROLLUP _rollup_min;
DROP ROLLUP _rollup_sec;
-- sensor_data と関連するすべての Rollup を削除
DROP TABLE sensor_data CASCADE;
```

## Rollup Gap {#rollup-gap}

Rollup Gap は、TAG テーブルに最新データが入った時点と、Rollup テーブルに反映された時点の差を表します。周期的な集計のため小さな遅延は発生します。大きなギャップや増加するギャップは、処理のボトルネックを示す場合があります。

```sql
SHOW ROLLUPGAP;
```

`SHOW ROLLUPGAP` は、各 Rollup の処理待ちデータ件数を表示します。

- `GAP` が 0 なら、最新の状態です。
- ギャップが増加し続ける場合は、次の対策を検討してください。
  1. `EXEC ROLLUP_FORCE` で直ちに集計する。
  2. `TAG_PARTITION_COUNT` を増やす（メモリ使用量の増加に注意）。
  3. CPU・ディスク I/O の処理能力を増強する。
  4. 入力速度を調整するか、ハードウェアを拡張する。

## 制約事項 {#limitations}

- 対応する集計関数は固定されており、ユーザー定義の集計は提供しません。
- Rollup は元のデータに依存するため、外れ値の除去などの品質管理は取り込み前に行ってください。
- 高速な取り込み環境では CPU と I/O の使用量が増加し、リソースが不足すると Rollup Gap が拡大する場合があります。
- 高い即時性が必要な場合は、元の TAG データを直接検索するほうが適切な場合があります。

## 例 {#rollup-examples}


Machbase Rollup テーブルの作成、管理、検索の実例を示します。

### 例 1: デフォルト Rollup の作成と検索 {#example-1-default-rollup-creation-and-query}

デフォルト Rollup（SEC、MIN、HOUR）を持つ TAG テーブルを作成し、時間単位で集計します。

```sql
-- 1. デフォルト Rollup を有効にした TAG テーブルを作成
CREATE TAG TABLE iot_sensors (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED -- この列の Rollup 集計を SUMMARIZED で指定
)
WITH ROLLUP; -- _iot_sensors_ROLLUP_SEC、_iot_sensors_ROLLUP_MIN、_iot_sensors_ROLLUP_HOUR を作成

-- 2. サンプルデータを挿入
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:05:15', 20.1);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:15:30', 20.5);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:55:00', 21.0);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 11:05:00', 21.5);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 11:35:45', 21.8);
INSERT INTO iot_sensors VALUES ('TEMP_B', '2024-03-10 10:10:00', 15.0);
INSERT INTO iot_sensors VALUES ('TEMP_B', '2024-03-10 11:10:00', 16.0);

-- Rollup 処理を待つか、強制実行する（任意）
-- EXEC ROLLUP_FORCE('_iot_sensors_ROLLUP_SEC');
-- EXEC ROLLUP_FORCE('_iot_sensors_ROLLUP_MIN');
-- EXEC ROLLUP_FORCE('_iot_sensors_ROLLUP_HOUR');

-- 3. TEMP_A の時間単位の平均温度を検索
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    AVG(temperature) AS avg_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time BETWEEN TO_DATE('2024-03-10 10:00:00') AND TO_DATE('2024-03-10 12:00:00')
GROUP BY
    hour_interval
ORDER BY
    hour_interval;

/* 予想される出力（概算）:
hour_interval                   avg_temp
---------------------------------------------------------------
2024-03-10 10:00:00 000:000:000 20.533...  -- 20.1、20.5、21.0 の平均
2024-03-10 11:00:00 000:000:000 21.65      -- 21.5、21.8 の平均
*/
```

### 例 2: カスタム Rollup の作成と検索 {#example-2-custom-rollup-creation-and-query}

15 分ごとに集計するカスタム Rollup テーブルを作成します。

```sql
-- 前提: 例 1 の iot_sensors テーブルが存在すること

-- 1. temperature 列を基に 15 分間隔のカスタム Rollup テーブルを作成
CREATE ROLLUP _iot_sensors_rollup_15min
ON iot_sensors (temperature)
INTERVAL 15 MIN;

-- Rollup 処理を待つか、強制実行する（任意）
-- EXEC ROLLUP_FORCE('_iot_sensors_rollup_15min');

-- 2. TEMP_A の温度の MIN と MAX を 15 分単位で検索
SELECT
    ROLLUP('min', 15, event_time) AS interval_15min,
    MIN(temperature) AS min_temp,
    MAX(temperature) AS max_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time BETWEEN TO_DATE('2024-03-10 10:00:00') AND TO_DATE('2024-03-10 12:00:00')
GROUP BY
    interval_15min
ORDER BY
    interval_15min;

/* 予想される出力（概算）:
interval_15min                  min_temp    max_temp
---------------------------------------------------------------
2024-03-10 10:00:00 000:000:000 20.1        20.1        -- 10:00〜10:14:59
2024-03-10 10:15:00 000:000:000 20.5        20.5        -- 10:15〜10:29:59
2024-03-10 10:45:00 000:000:000 21.0        21.0        -- 10:45〜10:59:59（10:55 のデータ）
2024-03-10 11:00:00 000:000:000 21.5        21.5        -- 11:00〜11:14:59
2024-03-10 11:30:00 000:000:000 21.8        21.8        -- 11:30〜11:44:59
*/
```

### 例 3: 拡張 Rollup の検索（FIRST/LAST） {#example-3-extended-rollup-query-firstlast}

拡張 Rollup を使用して、区間内の最初と最後の値を検索します。

```sql
-- 1. デフォルト Rollup と EXTENSION を指定して TAG テーブルを作成
DROP TABLE IF EXISTS iot_sensors_ext CASCADE; -- 存在する場合は削除
CREATE TAG TABLE iot_sensors_ext (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    pressure DOUBLE SUMMARIZED
)
WITH ROLLUP EXTENSION; -- FIRST() と LAST() を有効化

-- 2. サンプルデータを挿入
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:01:00', 1000.1);
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:05:00', 1000.5); -- 09:00 区間内の値（最初の値は 09:01 の 1000.1）
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:55:00', 1001.0); -- 09:00 区間の最後の値
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:02:00', 1001.2); -- 10:00 区間の最初の値
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:08:00', 1001.5);
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:40:00', 1001.8); -- 10:00 区間の最後の値

-- Rollup 処理を待つか、強制実行する（任意）
-- EXEC ROLLUP_FORCE('_iot_sensors_ext_ROLLUP_SEC'); ... など

-- 3. PRES_1 の時間ごとの最初と最後の圧力を検索
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    FIRST(event_time, pressure) AS first_pressure,
    LAST(event_time, pressure) AS last_pressure
FROM
    iot_sensors_ext
WHERE
    sensor_id = 'PRES_1'
GROUP BY
    hour_interval
ORDER BY
    hour_interval;

/* 予想される出力（概算）:
hour_interval                   first_pressure last_pressure
----------------------------------------------------------------------
2024-03-10 09:00:00 000:000:000 1000.1         1001.0
2024-03-10 10:00:00 000:000:000 1001.2         1001.8
*/
```

### 例 4: 日・週単位の検索 {#example-4-querying-different-granularities-dailyweekly}

複数の日・週にまたがるデータが `iot_sensors` に格納されているものとして、日平均と週平均を求めます。

```sql
-- iot_sensors に 2024-03-01〜2024-03-15 の TEMP_A のデータがあるものとする

-- 1. TEMP_A の日平均温度を検索
SELECT
    ROLLUP('day', 1, event_time) AS day_interval,
    AVG(temperature) AS avg_daily_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-01') AND event_time < TO_DATE('2024-03-16')
GROUP BY
    day_interval
ORDER BY
    day_interval;

-- 2. 月曜日（2024-03-04）を週の開始として TEMP_A の週平均温度を検索
SELECT
    ROLLUP('week', 1, event_time, '2024-03-04') AS week_start_monday, -- 週の境界をそろえる起点を指定
    AVG(temperature) AS avg_weekly_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-01') AND event_time < TO_DATE('2024-03-16')
GROUP BY
    week_start_monday
ORDER BY
    week_start_monday;
```


### 例 5: 月単位の Rollup クエリ {#example-5-monthly-rollup-queries}

Rollup を使用して月単位で集計します。通常は HOUR レベルの Rollup テーブルを使用して効率的に計算します。

```sql
-- 例 1 の iot_sensors に複数月のデータがあるものとする。
-- たとえば TEMP_A の 2024 年 1 月〜4 月のデータ。
-- 月別集計を確認するには複数月のデータが必要。
-- サンプルデータ（必要に応じて追加）:
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-01-15 12:00:00', 18.0);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-01-25 14:00:00', 18.5);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-02-10 08:00:00', 19.0);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-02-20 09:00:00', 19.2);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-05 10:00:00', 19.5); -- 前の例のデータも使用
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-20 11:00:00', 20.0);

-- 1. TEMP_A の月平均温度を検索
-- 起点のデフォルトは 1970-01-01 で、通常の暦月に対応する。
SELECT
    ROLLUP('month', 1, event_time) AS month_interval, -- 暦月ごとに集計
    AVG(temperature) AS avg_monthly_temp,
    COUNT(temperature) AS data_points_per_month
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    month_interval
ORDER BY
    month_interval;

/* 予想される出力（概算。値は投入データによって変わる）:
month_interval                  avg_monthly_temp data_points_per_month
--------------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 18.25            2
2024-02-01 00:00:00 000:000:000 19.1             2
2024-03-01 00:00:00 000:000:000 20.628571...     7 -- （例 1 のデータを含む）
*/

-- 2. TEMP_A の四半期（3 か月）の SUM と COUNT を検索
-- month 単位で period=3 を指定
SELECT
    ROLLUP('month', 3, event_time) AS quarter_interval, -- 3 か月単位で集計
    SUM(temperature) AS sum_quarterly_temp,
    COUNT(temperature) AS data_points_per_quarter
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    quarter_interval
ORDER BY
    quarter_interval;

/* 予想される出力（概算）:
quarter_interval                sum_quarterly_temp data_points_per_quarter
----------------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 219.1              11 -- 1 月・2 月・3 月の合計と件数
*/

-- 3. 起点の明示指定（任意。標準以外の月の区切りが必要な場合に使用）
-- 注意: month の起点には、いずれかの月の 1 日を指定すること。
SELECT
    ROLLUP('month', 1, event_time, '2024-01-01') AS month_interval, -- 起点を明示指定
    MIN(temperature) AS min_monthly_temp,
    MAX(temperature) AS max_monthly_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    month_interval
ORDER BY
    month_interval;

/* 予想される出力（概算）:
month_interval                  min_monthly_temp max_monthly_temp
--------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 18.0             18.5
2024-02-01 00:00:00 000:000:000 19.0             19.2
2024-03-01 00:00:00 000:000:000 19.5             21.8 -- （例 1 のデータを含む）
*/
```

### 例 6: Rollup の管理コマンド {#example-6-rollup-management-commands}

状態の確認、集計の強制実行、古い Rollup データの削除、Rollup を持つテーブルの削除を行います。

```sql
-- 1. 全 Rollup の現在のギャップを確認
SHOW ROLLUPGAP;

-- 2. 指定したカスタム Rollup の集計を直ちに実行
-- EXEC ROLLUP_FORCE('_iot_sensors_rollup_15min');

-- 3. iot_sensors の Rollup から 2024 年 3 月 1 日より前のデータを削除
DELETE FROM iot_sensors ROLLUP BEFORE TO_DATE('2024-03-01 00:00:00');

-- 4. iot_sensors_ext と関連するすべての Rollup テーブルを削除
DROP TABLE iot_sensors_ext CASCADE;
```
