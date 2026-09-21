---
title: ロールアップ
type: docs
weight: 11
toc: true
---

## はじめに {#introduction}

大規模な時系列データの統計値を取得する場合、対象範囲が広がるほど計算コストが増加します。長い時間範囲やデータ全体を集計すると、計算量が多く、時間もかかります。Machbase の **Rollup** は、TAG テーブルのデータを時間区間ごとに事前集計し、高速に検索する機能です。定義したダウンサンプリング周期で自動集計するため、よく使用する統計値をすぐに取得できます。

## 基本概念 {#core-concepts}

**Rollup テーブル**は、元の TAG テーブルまたは別の Rollup テーブルを基に、Machbase が内部で事前計算した集計結果を格納します。クエリ実行時に、負荷の高い集計処理を繰り返す必要がなくなります。

### 標準の集計関数 {#supported-aggregations}

Rollup テーブルは、次の標準の集計関数に対応しています。

- `MIN()`: 区間内の最小値。
- `MAX()`: 区間内の最大値。
- `SUM()`: 区間内の合計。
- `COUNT()`: 区間内のデータ件数。
- `AVG()`: 区間内の平均値。
- `SUMSQ()`: 区間内の値の二乗和。

### 拡張集計関数（オプション） {#extended-aggregations-optional}

Rollup 作成時に `EXTENSION` を指定すると、次の関数も使用できます。

- `FIRST()`: 区間内の最初の値。
- `LAST()`: 区間内の最後の値。

### 時間単位 {#time-granularity}

Rollup は、次の固定の時間間隔で集計します。

- 秒（`SEC`）
- 分（`MIN`）
- 時（`HOUR`）

Rollup を使用するクエリでは、これらの基本単位またはその倍数で集計を指定できます。日、週、月、年などの大きい単位も、内部で適切な基本の Rollup テーブルに対応付けて処理します。1 日以上の間隔には、通常 HOUR ベースの Rollup テーブルを使用します。

## Rollup テーブルの種類 {#rollup-table-types}

Machbase では、Rollup テーブルを作成・管理する方法として次の 2 つを提供しています。

### デフォルト Rollup {#default-rollup}

- TAG テーブル作成時に `WITH ROLLUP` 句を指定すると、自動的に作成されます。
- 指定した最小単位に応じて、秒・分・時の Rollup テーブルを作成します。たとえば `WITH ROLLUP (MIN)` では分・時の Rollup を、`WITH ROLLUP` または `WITH ROLLUP (SEC)` では秒・分・時の Rollup を作成します。
- テーブル名は元の TAG テーブル名を基に、`_<元のテーブル名>_ROLLUP_SEC` の形式で自動生成されます（例: `_mytag_ROLLUP_SEC`）。
- 1 つの TAG テーブルに作成できるデフォルト Rollup は 1 セットだけです。

### カスタム Rollup {#custom-rollup}

- `CREATE ROLLUP` 文で明示的に作成します。
- 10 秒、5 分など、必要な間隔を指定できます。
- TAG テーブルだけでなく、別の Rollup テーブルをソースに指定して、多段の集計構造を作成できます。
- デフォルト Rollup の単位にとらわれず、必要な集計間隔を柔軟に定義できます。

## Rollup テーブルの作成 {#creating-rollup-tables}

### デフォルト Rollup の作成 {#default-rollup-creation}

デフォルト Rollup テーブルは、TAG テーブルの定義時に作成されます。

**構文:**

```sql
CREATE TAG TABLE table_name (
    name_column datatype PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column numeric_datatype [SUMMARIZED]
    [, additional_columns...]
)
WITH ROLLUP [ ( SEC | MIN | HOUR ) ] [ EXTENSION ];
```

- `SEC | MIN | HOUR`: 最も細かい単位を指定します。省略時は秒（`SEC`）です。指定した単位より大きい単位の Rollup も自動的に含まれます（例: `MIN` を指定すると `HOUR` も含まれます）。
- `EXTENSION`: 省略可能なキーワードです。指定すると `FIRST()` と `LAST()` を使用できます。

**例:**

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

カスタム Rollup テーブルは、専用の DDL 文で明示的に作成します。

**構文:**

```sql
CREATE ROLLUP rollup_name
ON source_table_or_rollup_name ( source_value_column )
INTERVAL interval_value ( SEC | MIN | HOUR )
[ EXTENSION ];
```

- `rollup_name`: 作成する Rollup テーブルの名前。
- `source_table_or_rollup_name`: 元の TAG テーブルまたは既存の Rollup テーブルの名前。
- `source_value_column`: ソーステーブルで集計対象とする数値列。ソースが Rollup テーブルの場合は省略します。
- `interval_value`: 集計間隔の数値（例: 10、30）。
- `SEC | MIN | HOUR`: 集計間隔の単位。
- `EXTENSION`: 省略可能なキーワードです。指定すると `FIRST()` と `LAST()` を使用できます。

**注意事項:**

- ソースは TAG テーブルまたは別の Rollup テーブルである必要があります。
- ソースが Rollup テーブルの場合、新しい `INTERVAL` はソースの Rollup の間隔の倍数で、より大きい単位にする必要があります。

**例:**

```sql
-- 30 秒間隔の Rollup を作成
CREATE ROLLUP _tag_data_rollup_30sec ON tag_data(value) INTERVAL 30 SEC;

-- 上位の Rollup（10 分）
CREATE ROLLUP _tag_data_rollup_10min ON _tag_data_rollup_30sec INTERVAL 10 MIN;

-- 15 分間隔、拡張関数あり
CREATE ROLLUP _tag_data_rollup_15min_ext ON tag_data(value) INTERVAL 15 MIN EXTENSION;
```

## Rollup データの検索 {#querying-rollup-data}

事前集計による性能上の利点を活かすには、クエリで `ROLLUP()` 関数を使用します。旧 `ROLLUP` キーワード構文もありますが非推奨です。Machbase は、要求された間隔と単位に合わせて適切な Rollup テーブルを自動選択します。

**構文（推奨）:**

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

時間単位で `MIN` と `MAX` を検索する例です。

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

- `time_unit`（第 1 引数）: 集計間隔の単位（'sec'、'min'、'hour'、'day'、'week'、'month'、'year' など）。
- `period`（第 2 引数）: `time_unit` を基準とした集計間隔の倍数。使用する Rollup テーブルの間隔の有効な倍数である必要があります。
- `basetime_column`（第 3 引数）: TAG テーブルで `BASETIME` 属性を指定した DATETIME 列。
- `origin`（第 4 引数、省略可能）: 時間区間の境界をそろえる起点時刻を指定する DATETIME リテラル。デフォルトは `1970-01-01 00:00:00` です。週・月・年の区切りをそろえる際に重要です。
- `AGGREGATE_FUNCTION`: 対応する集計関数のいずれか（`MIN`、`MAX`、`AVG`、`SUM`、`COUNT`、`SUMSQ`、`EXTENSION` 指定時は `FIRST`/`LAST`）。

**注意事項:**

- `ROLLUP()` を含む式（またはその別名）を、必ず `GROUP BY` に指定します。
- `ROLLUP()` を使用する場合、値の列には上記の集計関数だけを適用できます。

**検索例:**

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

Rollup スレッドによる集計処理は、手動で制御できます。

**コマンド:**

```sql
-- 指定した Rollup の集計スレッドを開始
EXEC ROLLUP_START('rollup_name');
-- 指定した Rollup の集計スレッドを停止
EXEC ROLLUP_STOP('rollup_name');
-- 通常の待機時間を省き、未処理データを直ちに集計
EXEC ROLLUP_FORCE('rollup_name');
```

- `ROLLUP_FORCE` は待機時間を無視して、直ちに集計を実行します。

**実行例:**

```sql
EXEC ROLLUP_START('_tag_data_rollup_30sec');
EXEC ROLLUP_STOP('_tag_data_rollup_10min');
EXEC ROLLUP_FORCE('_tag_rollup_hour'); -- 時間単位の未処理データを集計
```

### Rollup データの削除 {#rollup-data-deletion}

元の TAG テーブルからデータを削除しても、Rollup テーブルの集計データは自動的には削除**されません**。Rollup データは別途削除する必要があります。

**構文:**

```sql
-- Delete all Rollup data for the specified table
DELETE FROM table_name ROLLUP;

-- Delete Rollup data before a specific timestamp for the specified table
DELETE FROM table_name ROLLUP BEFORE TO_DATE('YYYY-MM-DD HH24:MI:SS');

-- Delete all Rollup data for a specific tag within the table
DELETE FROM table_name ROLLUP WHERE name = 'specific_tag_id';

-- Delete Rollup data for a specific tag before a specific timestamp
DELETE FROM table_name ROLLUP WHERE name = 'specific_tag_id' AND time <= TO_DATE('YYYY-MM-DD HH24:MI:SS');
```

**削除例:**

```sql
-- 2024 年 1 月 15 日より前の Rollup データを削除
DELETE FROM TAG ROLLUP BEFORE TO_DATE('2024-01-15 00:00:00');

-- TAG01 の Rollup データをすべて削除
DELETE FROM TAG ROLLUP WHERE name = 'TAG01';
```

### Rollup テーブルの削除 {#rollup-table-deletion}

カスタム Rollup テーブルは個別に削除できます。デフォルト Rollup テーブルは、通常、元の TAG テーブルを削除するときに一緒に削除されます。

**構文:**

```sql
-- Drop a specific Custom Rollup table
DROP ROLLUP rollup_name;

-- Drop a TAG table and all its dependent Rollup tables (Default and Custom)
DROP TABLE tag_table_name CASCADE;
```

**注意事項:** 他の Rollup から参照されている Rollup テーブルは削除できません。依存する Rollup を先に（作成と逆の順序で）削除してください。

**削除順序の例:**

```sql
-- _rollup_min が _rollup_sec に依存する場合
DROP ROLLUP _rollup_min;
DROP ROLLUP _rollup_sec;

-- sensor_data と関連するすべての Rollup を削除
DROP TABLE sensor_data CASCADE;
```

## Rollup Gap {#rollup-gap}

**Rollup Gap** は、TAG テーブルに最新データが入った時点と、Rollup テーブルに反映された時点の差を表します。周期的な集計のため小さな遅延は発生します。大きなギャップや増加するギャップは、処理のボトルネックを示す場合があります。

### Rollup Gap の確認 {#checking-rollup-gap}

ギャップの有無を含め、Rollup の現在の処理状況を確認できます。

**コマンド:**

```sql
SHOW ROLLUPGAP;
```

このコマンドは、動作中の各 Rollup の情報と、ギャップの原因となっている処理待ちデータの件数を表示します。`GAP` が 0 なら、最新の状態です。

### Rollup Gap の解消 {#mitigating-rollup-gap}

ギャップが大きくなった場合は、次の対策を検討してください。

1. **集計の強制実行:** `EXEC ROLLUP_FORCE('rollup_name');` で、指定した Rollup の処理待ちデータを直ちに集計します。
2. **並列度の向上:** 元の TAG テーブルの `TAG_PARTITION_COUNT` プロパティを増やします。並列に動作できる Rollup スレッドが増えますが、メモリ使用量も増加するため注意してください。
3. **ハードウェアリソース:** CPU の速度・コア数とディスク I/O の処理能力を増強します。
4. **入力速度の管理:** データの入力速度が常にシステムの処理能力を上回る場合は、入力速度を調整するか、ハードウェアをさらに拡張します。

ギャップが解消されない場合は、データの取り込みと Rollup 集計を合わせた負荷に対して、システムリソースが不足していることが多いです。

## 制約事項 {#limitations}

Rollup は強力な機能ですが、次の制約があります。

- **固定の集計関数:** 対応する集計関数（`MIN`、`MAX`、`AVG`、`SUM`、`COUNT`、`SUMSQ`、オプションで `FIRST`/`LAST`）は固定されており、ユーザー定義の集計は提供しません。独自の集計ロジックが必要な場合は、別の方法を使用してください。
- **元データの品質:** Rollup は元のデータに依存するため、元の TAG テーブルに取り込まれた誤ったデータや外れ値も、そのまま集計結果に反映されます。外れ値の除去などの品質管理は、取り込み前または取り込み時に行ってください。
- **リソース消費:** Rollup 処理では、ソースの読み取りと Rollup テーブルへの書き込みに CPU と I/O を使用します。高速な取り込み環境ではリソースの競合が起きやすく、リソースが不足すると Rollup Gap が拡大する場合があります。
- **遅延:** TAG テーブルにデータが届いてから Rollup テーブルに反映されるまでには、集計間隔と処理時間に応じた遅延（Rollup Gap）があります。高い即時性が求められる場合や、集計値にマイクロ秒単位の精度が必要な場合は、元の TAG データを直接検索するほうが適切なことがあります。

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

上記の例のように Rollup 機能を活用すると、膨大な時系列データをさまざまな分析単位ですばやく検索できます。要件に合わせて、デフォルト Rollup とカスタム Rollup を適切に組み合わせて使用してください。
