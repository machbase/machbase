---
type: docs
title: '5.5 検索と分析'
weight: 50
toc: true
---

TAGテーブルから時系列データを検索する主なパターンを説明します。時間軸・距離軸の範囲検索、
複数タグの検索、統計ビューの活用を含みます。

<a id="original-85-querying-data"></a>

## Tagデータの検索


### サンプルスキーマ（時間軸）

次の例はTAGテーブルに2つのタグを登録し、タグごとに10行を入力します。
`TAG_0001`は2018年1月1日から10日、`TAG_0002`は2月1日から10日のデータを使用します。

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);

insert into tag metadata values ('TAG_0001');
insert into tag metadata values ('TAG_0002');

insert into tag values('TAG_0001', '2018-01-01 01:00:00 000:000:000', 1);
insert into tag values('TAG_0001', '2018-01-02 02:00:00 000:000:000', 2);
insert into tag values('TAG_0001', '2018-01-03 03:00:00 000:000:000', 3);
insert into tag values('TAG_0001', '2018-01-04 04:00:00 000:000:000', 4);
insert into tag values('TAG_0001', '2018-01-05 05:00:00 000:000:000', 5);
insert into tag values('TAG_0001', '2018-01-06 06:00:00 000:000:000', 6);
insert into tag values('TAG_0001', '2018-01-07 07:00:00 000:000:000', 7);
insert into tag values('TAG_0001', '2018-01-08 08:00:00 000:000:000', 8);
insert into tag values('TAG_0001', '2018-01-09 09:00:00 000:000:000', 9);
insert into tag values('TAG_0001', '2018-01-10 10:00:00 000:000:000', 10);

insert into tag values('TAG_0002', '2018-02-01 01:00:00 000:000:000', 11);
insert into tag values('TAG_0002', '2018-02-02 02:00:00 000:000:000', 12);
insert into tag values('TAG_0002', '2018-02-03 03:00:00 000:000:000', 13);
insert into tag values('TAG_0002', '2018-02-04 04:00:00 000:000:000', 14);
insert into tag values('TAG_0002', '2018-02-05 05:00:00 000:000:000', 15);
insert into tag values('TAG_0002', '2018-02-06 06:00:00 000:000:000', 16);
insert into tag values('TAG_0002', '2018-02-07 07:00:00 000:000:000', 17);
insert into tag values('TAG_0002', '2018-02-08 08:00:00 000:000:000', 18);
insert into tag values('TAG_0002', '2018-02-09 09:00:00 000:000:000', 19);
insert into tag values('TAG_0002', '2018-02-10 10:00:00 000:000:000', 20);

exec table_flush(tag);
```

例の最後の`TABLE_FLUSH`はストレージバッファを明示的に処理する手順です。
トランザクションのコミットや検索時の可視性を保証するコマンドとは解釈しません。詳細は
[TABLE_FLUSH](/dbms/reference/sql/syntax/execute-procedure-syntax/#table-flush)を参照してください。

### 全TAGデータの抽出

```sql
select * from tag ORDER BY name, time;
```

```text
NAME TIME VALUE
--------------------------------------------------------------------------------------
TAG_0001 2018-01-01 01:00:00 000:000:000 1
TAG_0001 2018-01-02 02:00:00 000:000:000 2
TAG_0001 2018-01-03 03:00:00 000:000:000 3
TAG_0001 2018-01-04 04:00:00 000:000:000 4
TAG_0001 2018-01-05 05:00:00 000:000:000 5
TAG_0001 2018-01-06 06:00:00 000:000:000 6
TAG_0001 2018-01-07 07:00:00 000:000:000 7
TAG_0001 2018-01-08 08:00:00 000:000:000 8
TAG_0001 2018-01-09 09:00:00 000:000:000 9
TAG_0001 2018-01-10 10:00:00 000:000:000 10
TAG_0002 2018-02-01 01:00:00 000:000:000 11
TAG_0002 2018-02-02 02:00:00 000:000:000 12
TAG_0002 2018-02-03 03:00:00 000:000:000 13
TAG_0002 2018-02-04 04:00:00 000:000:000 14
TAG_0002 2018-02-05 05:00:00 000:000:000 15
TAG_0002 2018-02-06 06:00:00 000:000:000 16
TAG_0002 2018-02-07 07:00:00 000:000:000 17
TAG_0002 2018-02-08 08:00:00 000:000:000 18
TAG_0002 2018-02-09 09:00:00 000:000:000 19
TAG_0002 2018-02-10 10:00:00 000:000:000 20
[20] row(s) selected.
```

上記は例の実行結果です。結果の順序を保証する必要がある場合は`ORDER BY name, time`を明示します。
条件のない検索の出力順序は、実行計画とスキャン方向に依存する場合があります。


### 特定のタグ名によるデータの抽出

TAG名がTAG_0002のデータを検索する例です。

```sql
select * from tag where name='TAG_0002' ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
TAG_0002              2018-02-05 05:00:00 000:000:000 15
TAG_0002              2018-02-06 06:00:00 000:000:000 16
TAG_0002              2018-02-07 07:00:00 000:000:000 17
TAG_0002              2018-02-08 08:00:00 000:000:000 18
TAG_0002              2018-02-09 09:00:00 000:000:000 19
TAG_0002              2018-02-10 10:00:00 000:000:000 20
[10] row(s) selected.
```


### 時間範囲の検索

TAG_0002に時間範囲を指定してデータを検索する例です。

> `BETWEEN`は両方の境界を含み、`>=`と`<=`を組み合わせた条件と同じです。
> 以下の例は境界時刻にデータがないため、`>`・`<`の条件でも同じ結果を返します。
> 連続する検索区間で境界行を重複して読み取らないようにするには、
> `time >= 開始 AND time < 終了`を使用します。

```sql
select * from tag where name = 'TAG_0002' and time between to_date('2018-02-01') and to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[4] row(s) selected.
```

```sql
select * from tag where name = 'TAG_0002' and time > to_date('2018-02-01') and time < to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[4] row(s) selected.
```

### 距離軸のサンプルスキーマ

距離軸（`BASE DISTANCE`）のTagテーブルを使用する例です。

```sql
CREATE TAG TABLE trip_tag (
    name        VARCHAR(20) PRIMARY KEY,
    distance_m  DOUBLE BASE DISTANCE,
    value       DOUBLE,
    quality     INTEGER
);

INSERT INTO trip_tag VALUES('ODO_A', 0, 10.1, 100);
INSERT INTO trip_tag VALUES('ODO_A', 500, 11.2, 101);
INSERT INTO trip_tag VALUES('ODO_A', 1000, 12.3, 102);

INSERT INTO trip_tag VALUES('ODO_B', 1000.1, 21.5, 100);
INSERT INTO trip_tag VALUES('ODO_B', 1500, 22.1, 101);
INSERT INTO trip_tag VALUES('ODO_B', 2000, 22.9, 102);

EXEC TABLE_FLUSH(trip_tag);
```

### 距離区間の検索

```sql
SELECT name, distance_m, value, quality
  FROM trip_tag
 WHERE name = 'ODO_A'
   AND distance_m BETWEEN 0 AND 1000
 ORDER BY distance_m;
```

時間軸と同様、距離軸も軸範囲を絞り込むことが基本的な検索パターンです。

### DOUBLE距離軸の小数境界による検索

```sql
SELECT name, distance_m, value, quality
  FROM trip_tag
 WHERE name = 'ODO_B'
   AND distance_m BETWEEN 1000.1 AND 2000
 ORDER BY distance_m;
```

数値をそのまま比較するため、`1000`は除外され、`1500`と`2000`は含まれます。

### 距離軸の実行計画の確認

大規模な距離軸検索では、`EXPLAIN`で距離条件がキー範囲に含まれることを確認します。

```sql
EXPLAIN
SELECT name, distance_m, value
  FROM trip_tag
 WHERE name = 'ODO_B'
   AND distance_m BETWEEN 1000.1 AND 2000
 ORDER BY distance_m;
```

確認するポイント:

- `KEYVALUE INDEX SCAN`または同様のインデックススキャンが表示されるか
- `KEY RANGE`の下に`distance_m between ...`条件が表示されるか

### 距離バケットの集計

次の例は0以上の距離を500単位の区間に分割します。TRUNCは0方向に切り捨てるため、
負の座標の区間が必要な場合は、FLOORなど必要な境界規則を別途選択します。

```sql
SELECT TRUNC(distance_m / 500, 0) * 500 AS dist_bucket,
       COUNT(*)                         AS sample_count,
       MIN(value)                       AS min_v,
       MAX(value)                       AS max_v,
       AVG(value)                       AS avg_v
  FROM trip_tag
 WHERE name = 'ODO_B'
 GROUP BY TRUNC(distance_m / 500, 0) * 500
 ORDER BY dist_bucket;
```

たとえば`1750`は`1500`のバケットに集計されます。

### 複数タグの時間範囲検索

2つ以上のタグに同じ時間範囲を適用する例です。対象名の一覧が決まっている場合は`IN`で表します。
対象タグが多い場合の性能は、リストのサイズと時間範囲を合わせて測定します。

```sql
select * from tag where name in ('TAG_0002', 'TAG_0001') and time between to_date('2018-01-05') and to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2018-01-05 05:00:00 000:000:000 5
TAG_0001              2018-01-06 06:00:00 000:000:000 6
TAG_0001              2018-01-07 07:00:00 000:000:000 7
TAG_0001              2018-01-08 08:00:00 000:000:000 8
TAG_0001              2018-01-09 09:00:00 000:000:000 9
TAG_0001              2018-01-10 10:00:00 000:000:000 10
TAG_0002              2018-02-01 01:00:00 000:000:000 11
TAG_0002              2018-02-02 02:00:00 000:000:000 12
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[10] row(s) selected.
```

### 指定値を超えるデータの検索

タグ値の条件も指定できます。TAG_0002の値から、12より大きく15より小さい値を絞り込んだ結果です。

```sql
select * from tag where name = 'TAG_0002' and value > 12 and value < 15 and time between to_date('2018-02-01') and to_date('2018-02-05') ORDER BY name, time;
```

```text
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0002              2018-02-03 03:00:00 000:000:000 13
TAG_0002              2018-02-04 04:00:00 000:000:000 14
[2] row(s) selected.
```

<a id="tag-stat-axis-schema"></a>

### タグ別統計ビュー`V$<TABLE>_STAT`

Tagテーブルを作成すると、Tag IDごとの統計情報を集計する仮想テーブルが自動作成されます。
この仮想テーブルの名前はv${tagテーブル名}_statです。

タグ名・軸に関する統計と、3番目のSUMMARIZED列の値の統計を区別します。
STATはバックグラウンドのインデックス・統計処理状態を反映するため、直前の入力の検証は
元データのSELECTと合わせて行います。すぐに統計を確認する実習では、TABLE_FLUSHの後に
INDEX_FLUSHで処理を待ちます。

<span class="badge-since">BASE DISTANCEの軸別STATスキーマはMachbase 8.7.0からサポート</span>

軸に関する列名と型はTAGテーブルの軸によって異なります。

| TAGの軸 | 最小/最大の軸値 | 最小/最大値が発生した軸値 | 最新入力行の軸値 | 軸統計の型 |
|--------|--------------|----------------------|------------------|--------------|
| `DATETIME BASE TIME` | `MIN_TIME`, `MAX_TIME` | `MIN_VALUE_TIME`, `MAX_VALUE_TIME` | `RECENT_ROW_TIME` | `DATETIME` |
| `DOUBLE/LONG/ULONG BASE DISTANCE` | `MIN_DISTANCE`, `MAX_DISTANCE` | `MIN_VALUE_DISTANCE`, `MAX_VALUE_DISTANCE` | `RECENT_ROW_DISTANCE` | 元のBASE DISTANCEの型 |

両Editionの共通列は`NAME`、`ROW_COUNT`、`MIN_VALUE`、`MAX_VALUE`です。
Cluster Editionではスキーマの先頭に`HOSTNAME VARCHAR(64)`が追加されます。

#### BASE TIME STATスキーマ


```sql
DESC v$tag_stat;
```

```text
[ COLUMN ]
----------------------------------------------------------------------------------------------------
NAME                                                        NULL?    TYPE                LENGTH
----------------------------------------------------------------------------------------------------
NAME                                                                 varchar             100
ROW_COUNT                                                            ulong               20
MIN_TIME                                                             datetime            31
MAX_TIME                                                             datetime            31
MIN_VALUE                                                            double              17
MIN_VALUE_TIME                                                       datetime            31
MAX_VALUE                                                            double              17
MAX_VALUE_TIME                                                       datetime            31
RECENT_ROW_TIME                                                      datetime            31
```

3番目の列にSUMMARIZEDキーワードがない場合、VALUE関連情報
（MIN_VALUE、MAX_VALUE、MIN_VALUE_TIME、MAX_VALUE_TIME）は保存されません。

収集される統計情報は次のとおりです。

|列名|情報|
|--|--|
|NAME|Tag IDの名前|
|ROW_COUNT|行数|
|MIN_TIME|該当Tag IDの行で最小のbasetime列値|
|MAX_TIME|該当Tag IDの行で最大のbasetime列値|
|MIN_VALUE|該当Tag IDの行で最小のsummarized列値|
|MIN_VALUE_TIME|MIN_VALUEとともに挿入されたbasetime列値|
|MAX_VALUE|該当Tag IDの行で最大のsummarized列値|
|MAX_VALUE_TIME|MAX_VALUEとともに挿入されたbasetime列値|
|RECENT_ROW_TIME|最も最近に挿入されたbasetime列値|

次の統計実習は、前の20行の検索例とは別のテーブルを使用します。そのため、以下の2つのタグだけが
検索され、前のTAG_0001・TAG_0002が統計の期待結果に混在しません。

1. SUMMARIZED列がある場合

```sql
CREATE TAG TABLE ch5_stat_time (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
```

```sql
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-12'), 10);
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-13'), 10);
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-14'), 20);
INSERT INTO ch5_stat_time VALUES('tag-0', TO_DATE('2021-08-11'), 5);
INSERT INTO ch5_stat_time VALUES('tag-1', TO_DATE('2022-08-12'), 100);
INSERT INTO ch5_stat_time VALUES('tag-1', TO_DATE('2022-08-11'), 200);
INSERT INTO ch5_stat_time VALUES('tag-1', TO_DATE('2022-08-10'), 50);
```

```sql
EXEC TABLE_FLUSH(ch5_stat_time);
EXEC INDEX_FLUSH(ch5_stat_time);
SELECT * FROM v$ch5_stat_time_stat ORDER BY name;
```

```text
NAME                                                                              ROW_COUNT            MIN_TIME                        MAX_TIME                        MIN_VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
MIN_VALUE_TIME                  MAX_VALUE                   MAX_VALUE_TIME                  RECENT_ROW_TIME
---------------------------------------------------------------------------------------------------------------------------------
tag-0                                                                             4                    2021-08-11 00:00:00 000:000:000 2021-08-14 00:00:00 000:000:000 5
2021-08-11 00:00:00 000:000:000 20                          2021-08-14 00:00:00 000:000:000 2021-08-11 00:00:00 000:000:000
tag-1                                                                             3                    2022-08-10 00:00:00 000:000:000 2022-08-12 00:00:00 000:000:000 50
2022-08-10 00:00:00 000:000:000 200                         2022-08-11 00:00:00 000:000:000 2022-08-10 00:00:00 000:000:000
[2] row(s) selected.
```

2. SUMMARIZED列がない場合

```sql
CREATE TAG TABLE other_tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
```

```text
Executed successfully.
```

```sql
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-12'), 10);
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-13'), 10);
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-14'), 20);
INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-11'), 5);
INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-12'), 100);
INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-11'), 200);
INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-10'), 50);
```

```sql
EXEC TABLE_FLUSH(other_tag);
EXEC INDEX_FLUSH(other_tag);
SELECT * FROM v$other_tag_stat ORDER BY name;
```

```text
NAME                                                                              ROW_COUNT            MIN_TIME                        MAX_TIME                        MIN_VALUE
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
MIN_VALUE_TIME                  MAX_VALUE                   MAX_VALUE_TIME                  RECENT_ROW_TIME
---------------------------------------------------------------------------------------------------------------------------------
tag-0                                                                             4                    2021-08-11 00:00:00 000:000:000 2021-08-14 00:00:00 000:000:000 NULL
NULL                            NULL                        NULL                            2021-08-11 00:00:00 000:000:000
tag-1                                                                             3                    2022-08-10 00:00:00 000:000:000 2022-08-12 00:00:00 000:000:000 NULL
NULL                            NULL                        NULL                            2022-08-10 00:00:00 000:000:000
[2] row(s) selected.
```

#### BASE DISTANCE STATスキーマ

距離軸TAGテーブルの統計ビューは、距離値を数値型で提供します。

```sql
CREATE TAG TABLE distance_sensor (
    name       VARCHAR(32) PRIMARY KEY,
    odometer_m DOUBLE BASE DISTANCE,
    value      DOUBLE SUMMARIZED
);

INSERT INTO distance_sensor VALUES('sensor', 20.5, 8);
INSERT INTO distance_sensor VALUES('sensor', 10.25, 3);
INSERT INTO distance_sensor VALUES('sensor', 30.75, 5);

EXEC TABLE_FLUSH(distance_sensor);
EXEC INDEX_FLUSH(distance_sensor);
```

Standard Editionの`DOUBLE BASE DISTANCE`テーブルのスキーマは次のとおりです。

```sql
DESC V$DISTANCE_SENSOR_STAT;
```

```text
[ COLUMN ]
----------------------------------------------------------------------------------------------------
NAME                                                        NULL?    TYPE                LENGTH
----------------------------------------------------------------------------------------------------
NAME                                                                 varchar             100
ROW_COUNT                                                            ulong               20
MIN_DISTANCE                                                         double              17
MAX_DISTANCE                                                         double              17
MIN_VALUE                                                            double              17
MIN_VALUE_DISTANCE                                                   double              17
MAX_VALUE                                                            double              17
MAX_VALUE_DISTANCE                                                   double              17
RECENT_ROW_DISTANCE                                                  double              17
```

5つの距離軸統計列の型は、元のBASE DISTANCE列の型に従います。

| BASE DISTANCEの型 | STAT列の型 | `DESC`の長さ |
|--------------------|----------------|-------------|
| `DOUBLE` | `double` | 17 |
| `LONG` | `long` | 20 |
| `ULONG` | `ulong` | 20 |

```sql
SELECT name,
       row_count,
       min_distance,
       max_distance,
       min_value,
       min_value_distance,
       max_value,
       max_value_distance,
       recent_row_distance
  FROM V$DISTANCE_SENSOR_STAT
 WHERE name = 'sensor';
```

- `MIN_DISTANCE`と`MAX_DISTANCE`は、該当統計行の最小・最大距離です。
- `MIN_VALUE_DISTANCE`と`MAX_VALUE_DISTANCE`は、それぞれ最小・最大のsummarized値が発生した距離です。
- `RECENT_ROW_DISTANCE`は最大距離ではなく、最も最近に入力された行の距離です。
- `SUMMARIZED`列がない場合、`MIN_VALUE_DISTANCE`と`MAX_VALUE_DISTANCE`は`NULL`です。

##### Cluster Editionでの検索

Cluster Editionの統計ビューには`HOSTNAME`が追加され、Warehouseごとの統計行が返る場合が
あります。まずWarehouseごとの値を確認します。

```sql
SELECT hostname, name, row_count,
       min_distance, max_distance,
       min_value, min_value_distance,
       max_value, max_value_distance,
       recent_row_distance
  FROM V$DISTANCE_SENSOR_STAT
 ORDER BY hostname, name;
```

行数と距離の境界値は、タグ名ごとに安全に集計できます。

```sql
SELECT name,
       SUM(row_count)     AS row_count,
       MIN(min_distance)  AS min_distance,
       MAX(max_distance)  AS max_distance
  FROM V$DISTANCE_SENSOR_STAT
 GROUP BY name;
```

{{< callout type="warning" >}}
`MIN_VALUE`と`MIN_VALUE_DISTANCE`、`MAX_VALUE`と`MAX_VALUE_DISTANCE`は、同じWarehouse行の
組み合わせを維持する必要があります。2つの列を独立して`MIN`または`MAX`で集計すると、
異なるWarehouseの値が組み合わされる可能性があります。`RECENT_ROW_DISTANCE`もWarehouseごとの
最新入力距離のため、`MAX(RECENT_ROW_DISTANCE)`をクラスター全体の最新入力行と解釈しないでください。
{{< /callout >}}

##### 8.7.0との互換性

BASE DISTANCE統計ビューの従来の名前はエイリアスとして提供されません。既存テーブルも、
8.7.0サーバーが再起動すると新しいスキーマで構成されます。

| 8.7.0より前の名前 | 8.7.0の名前 |
|-----------------|------------|
| `MIN_TIME` | `MIN_DISTANCE` |
| `MAX_TIME` | `MAX_DISTANCE` |
| `MIN_VALUE_TIME` | `MIN_VALUE_DISTANCE` |
| `MAX_VALUE_TIME` | `MAX_VALUE_DISTANCE` |
| `RECENT_ROW_TIME` | `RECENT_ROW_DISTANCE` |

BASE TIME TAGテーブルは従来の`*_TIME DATETIME`スキーマを維持します。


### スキャン方向のヒント

軸方向の走査と結果のソートを区別します。軸を逆方向に検索したときの最新値は最大の軸値であり、
最後に入力した行を示すSTATのRECENT_ROW値とは異なる場合があります。
同じ軸値を持つ複数行の順序も区別する必要がある場合は、アプリケーションに追加の基準が必要です。

```sql
SELECT *
  FROM tag
 WHERE name = 'TAG_0001'
 ORDER BY time
 LIMIT 10;

SELECT /*+ SCAN_FORWARD(tag) */ name, time, value
  FROM tag
 WHERE name = 'TAG_0001'
 LIMIT 10;

SELECT /*+ SCAN_BACKWARD(tag) */ name, time, value
  FROM tag
 WHERE name = 'TAG_0001'
 LIMIT 10;
```

ヒントがない場合のデフォルト方向は
[TABLE_SCAN_DIRECTION](/dbms/reference/configuration/configuration/)を参照してください。

## 後片付け

```sql
DROP TABLE ch5_stat_time;
DROP TABLE distance_sensor;
DROP TABLE trip_tag;
DROP TABLE other_tag;
DROP TABLE tag;
```
