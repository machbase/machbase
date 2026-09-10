---
title: 'Tag データの検索'
type: docs
weight: 40
toc: true
---

## 概要 {#overview}

Machbase は、タグの軸に沿った範囲検索を高速に実行します。時間軸と距離軸の主な検索パターンを説明します。

## クイックスタート {#quick-start}

特定タグの時刻範囲と距離範囲を、高速に検索できます。

## サンプルスキーマ（時間軸） {#sample-schema-time-axis}

TAG テーブルと 2 つのタグを作成する例です。

TAG_0001 には 2018 年 1 月 1 日～10 日、TAG_0002 には 2 月 1 日～10 日のデータを入力します。

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

同じセッションで直後に検証する場合は、先にテーブルをフラッシュします。

## 全 TAG データの取得 {#extract-all-tag-data}

```bash
Mach> select * from tag;
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

条件がなければ、タグごとに時刻順に並んだデータを取得できます。


## 特定タグ名のデータ取得 {#extract-data-for-a-specific-tag-name}

TAG_0002 のデータを取得する例です。

```sql
Mach> select * from tag where name='TAG_0002';
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


## 時刻範囲の検索 {#query-for-time-range}

TAG_0002 の指定期間のデータを取得します。

> BETWEEN は両端を含みます。`<` や `>` は境界を含みません。以下では境界と同じ時刻の行がないため、結果は同じです。

```bash
Mach> select * from tag where name = 'TAG_0002' and time between to_date('2018-02-01') and to_date('2018-02-05');
NAME                  TIME                            VALUE                      
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11                         
TAG_0002              2018-02-02 02:00:00 000:000:000 12                         
TAG_0002              2018-02-03 03:00:00 000:000:000 13                         
TAG_0002              2018-02-04 04:00:00 000:000:000 14                         
[4] row(s) selected.
 
Mach> select * from tag where name = 'TAG_0002' and time > to_date('2018-02-01') and time < to_date('2018-02-05');
NAME                  TIME                            VALUE                      
--------------------------------------------------------------------------------------
TAG_0002              2018-02-01 01:00:00 000:000:000 11                         
TAG_0002              2018-02-02 02:00:00 000:000:000 12                         
TAG_0002              2018-02-03 03:00:00 000:000:000 13                         
TAG_0002              2018-02-04 04:00:00 000:000:000 14                         
[4] row(s) selected.
```

## サンプルスキーマ（距離軸） {#distance-axis-sample-schema}

次の例は `BASE DISTANCE` の Tag テーブルを使用します。

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

## 距離範囲の検索 {#query-a-distance-range}

```sql
SELECT name, distance_m, value, quality
  FROM trip_tag
 WHERE name = 'ODO_A'
   AND distance_m BETWEEN 0 AND 1000
 ORDER BY distance_m;
```

時間軸と同様、軸の範囲を絞るのが基本です。

## DOUBLE 距離軸の小数境界 {#fractional-boundaries-on-a-double-distance-axis}

```sql
SELECT name, distance_m, value, quality
  FROM trip_tag
 WHERE name = 'ODO_B'
   AND distance_m BETWEEN 1000.1 AND 2000
 ORDER BY distance_m;
```

数値を直接比較するため、`1000` は除外され、`1500` と `2000` は含まれます。

## 距離検索の実行計画 {#check-the-execution-plan-for-distance-queries}

大きなテーブルでは `EXPLAIN` を使用し、距離条件がキー範囲に適用されることを確認します。

```sql
EXPLAIN
SELECT name, distance_m, value
  FROM trip_tag
 WHERE name = 'ODO_B'
   AND distance_m BETWEEN 1000.1 AND 2000
 ORDER BY distance_m;
```

次の点を確認します。

- `KEYVALUE INDEX SCAN` などのインデックススキャン
- `distance_m between ...` を含む `KEY RANGE`

## 距離バケットの集計 {#distance-bucket-aggregation}

`TRUNC(..., 0)` を使用すると、距離軸のバケットを確実に作成できます。

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

例えば距離 `1750` は、`1500` のバケットに集計されます。

## 複数タグの時刻範囲検索 {#time-range-search-for-multiple-tags}

2 つ以上のタグから、同じ時刻範囲を取得する例です。

多数のタグを同時に高速取得する場合は、次の形式を推奨します。

```bash
Mach> select * from tag where name in ('TAG_0002', 'TAG_0001') and time between to_date('2018-01-05') and to_date('2018-02-05');
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

## 値による絞り込み {#search-data-over-a-certain-value}

タグの値にも条件を指定できます。

TAG_0002 のうち、12 より大きく 15 より小さい値を取得します。

```bash
Mach> select * from tag where name = 'TAG_0002' and value > 12 and value < 15 and time between to_date('2018-02-01') and to_date('2018-02-05');
NAME                  TIME                            VALUE                      
--------------------------------------------------------------------------------------
TAG_0002              2018-02-03 03:00:00 000:000:000 13                         
TAG_0002              2018-02-04 04:00:00 000:000:000 14                         
[2] row(s) selected.
```

## タグ ID ごとの統計情報 {#display-statistical-information-by-specific-tag-id}

Tag テーブルを作成すると、タグ ID ごとの簡単な統計を集計する仮想テーブルが作成されます。

名前は `v${テーブル名}_stat` です。

このテーブルから統計を高速に取得できます。

統計対象は、自動的に第 3 列になります。


```bash
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
Executed successfully.
 
Mach> DESC v$tag_stat;
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

第 3 列に SUMMARIZED がなければ、MIN_VALUE、MAX_VALUE、MIN_VALUE_TIME、MAX_VALUE_TIME は保存されません。

収集する情報を示します。

| 列名 | 情報 |
|--|--|
|NAME|タグ ID の名前|
|ROW_COUNT|行数|
|MIN_TIME|対象タグの BASETIME の最小値|
|MAX_TIME|対象タグの BASETIME の最大値|
|MIN_VALUE|対象タグの SUMMARIZED 列の最小値|
|MIN_VALUE_TIME|MIN_VALUE に対応する BASETIME|
|MAX_VALUE|対象タグの SUMMARIZED 列の最大値|
|MAX_VALUE_TIME|MAX_VALUE に対応する BASETIME|
|RECENT_ROW_TIME|最後に入力したレコードの BASETIME|

以下の統計例は、先のサンプルとは独立して、同名テーブルが存在しない状態で実行します。

1. SUMMARIZED 列がある場合

```bash
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
Executed successfully.
  
Mach> INSERT INTO tag VALUES('tag-0', TO_DATE('2021-08-12'), 10);
Mach> INSERT INTO tag VALUES('tag-0', TO_DATE('2021-08-13'), 10);
Mach> INSERT INTO tag VALUES('tag-0', TO_DATE('2021-08-14'), 20);
Mach> INSERT INTO tag VALUES('tag-0', TO_DATE('2021-08-11'), 5);
Mach> INSERT INTO tag VALUES('tag-1', TO_DATE('2022-08-12'), 100);
Mach> INSERT INTO tag VALUES('tag-1', TO_DATE('2022-08-11'), 200);
Mach> INSERT INTO tag VALUES('tag-1', TO_DATE('2022-08-10'), 50);
  
Mach> EXEC TABLE_FLUSH(tag);
Executed successfully.

Mach> SELECT * FROM v$tag_stat;
NAME                                                                              ROW_COUNT            MIN_TIME                        MAX_TIME                        MIN_VALUE                 
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
MIN_VALUE_TIME                  MAX_VALUE                   MAX_VALUE_TIME                  RECENT_ROW_TIME               
---------------------------------------------------------------------------------------------------------------------------------
tag-0                                                                             4                    2021-08-11 00:00:00 000:000:000 2021-08-14 00:00:00 000:000:000 5                         
2021-08-11 00:00:00 000:000:000 20                          2021-08-14 00:00:00 000:000:000 2021-08-11 00:00:00 000:000:000
tag-1                                                                             3                    2022-08-10 00:00:00 000:000:000 2022-08-12 00:00:00 000:000:000 50                        
2022-08-10 00:00:00 000:000:000 200                         2022-08-11 00:00:00 000:000:000 2022-08-10 00:00:00 000:000:000
[2] row(s) selected.
  
2. SUMMARIZED 列がない場合
Mach> CREATE TAG TABLE other_tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
Executed successfully.
  
Mach> INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-12'), 10);
Mach> INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-13'), 10);
Mach> INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-14'), 20);
Mach> INSERT INTO other_tag VALUES('tag-0', TO_DATE('2021-08-11'), 5);
Mach> INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-12'), 100);
Mach> INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-11'), 200);
Mach> INSERT INTO other_tag VALUES('tag-1', TO_DATE('2022-08-10'), 50);
  
Mach> EXEC TABLE_FLUSH(other_tag);
Executed successfully.

Mach> SELECT * FROM v$other_tag_stat;
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


## RESTful API による取得 {#extraction-by-using-restful-api}

### RESTful API の準備 {#prepare-for-restful-api}

次のプロパティを設定してサーバーを起動します。

machbase.conf

```
HTTP_ENABLE = 1
HTTP_PORT_NO = 5657
```

`V$HTTP_STATUS` で、稼働中の HTTP ポートを確認できます。

```sql
SELECT HTTP_PORT FROM V$HTTP_STATUS;
```

RESTful API の呼び出し形式：

**SELECT 形式**

```bash
http://{host}:{http_port}/machiot-rest-api/datapoints/raw/{Table}/{TagName}/{Start}/{End}/{Direction}/{Count}/{Offset}/
 
Table      : Tag テーブル名
TagName    : タグ名。複数のタグはカンマで区切る。
Start, End : 範囲。YYYY-MM-DD、YYYY-MM-DDTHH24:MI:SS、YYYY-MM-DDTHH24:MI:SS,mmm を使用する。
Direction  : 0 は時刻の昇順。
Count      : LIMIT。0 は全行。
Offset     : オフセット。不要なら 0。
```

### curl で単一タグを取得 {#sample-for-fetching-single-tag-data-by-using-curl-}

**単一タグ**

```bash
$ curl "http://127.0.0.1:5657/machiot-rest-api/datapoints/raw/TAG/TAG_0001/2018-01-01T00:00:00/2018-01-06T00:00:00/0/0/0"
```

### curl で複数タグを取得 {#fetching-multi-tag-data-by-using-curl}

2 つのタグの値を取得する例です。

```bash
$ curl "http://127.0.0.1:5657/machiot-rest-api/datapoints/raw/TAG/TAG_0001,TAG_0002/2018-01-05T00:00:00/2018-02-05T00:00:00/0/0/0"
```


## ヒントによる検索方向の指定 {#specifying-the-serach-direction-using-hints}

通常、Tag テーブルは軸の値が古いレコードから検索します。逆順で取得するには、ヒントで方向を制御できます。以下は `t_name`、`t_time`、`t_value` 列を持つ別のサンプルテーブルとデータを使用した出力例です。

### 順方向 {#forward-search}

既定の方向です。`/*+ SCAN_FORWARD(table_name) */` でも指定できます。

```bash
Mach> SELECT * FROM tag WHERE t_name='TAG_99' LIMIT 10;
T_NAME                T_TIME                          T_VALUE                    
--------------------------------------------------------------------------------------
TAG_99                2017-01-01 00:00:49 500:000:000 0                          
TAG_99                2017-01-01 00:01:39 500:000:000 1                          
TAG_99                2017-01-01 00:02:29 500:000:000 2                          
TAG_99                2017-01-01 00:03:19 500:000:000 3                          
TAG_99                2017-01-01 00:04:09 500:000:000 4                          
TAG_99                2017-01-01 00:04:59 500:000:000 5                          
TAG_99                2017-01-01 00:05:49 500:000:000 6                          
TAG_99                2017-01-01 00:06:39 500:000:000 7                          
TAG_99                2017-01-01 00:07:29 500:000:000 8                          
TAG_99                2017-01-01 00:08:19 500:000:000 9                          
[10] row(s) selected.
Elapsed time: 0.001
 
Mach> SELECT /*+ SCAN_FORWARD(tag) */  * FROM tag WHERE t_name='TAG_99' LIMIT 10;
T_NAME                T_TIME                          T_VALUE                    
--------------------------------------------------------------------------------------
TAG_99                2017-01-01 00:00:49 500:000:000 0                          
TAG_99                2017-01-01 00:01:39 500:000:000 1                          
TAG_99                2017-01-01 00:02:29 500:000:000 2                          
TAG_99                2017-01-01 00:03:19 500:000:000 3                          
TAG_99                2017-01-01 00:04:09 500:000:000 4                          
TAG_99                2017-01-01 00:04:59 500:000:000 5                          
TAG_99                2017-01-01 00:05:49 500:000:000 6                          
TAG_99                2017-01-01 00:06:39 500:000:000 7                          
TAG_99                2017-01-01 00:07:29 500:000:000 8                          
TAG_99                2017-01-01 00:08:19 500:000:000 9                          
[10] row(s) selected.
Elapsed time: 0.001
Mach>
```

### 逆方向 {#backward-search}

`/*+ SCAN_BACKWARD(table_name) */` を使用します。

```bash
Mach> SELECT /*+ SCAN_BACKWARD(tag) */ * FROM tag WHERE t_name='TAG_99' LIMIT 10;
T_NAME                T_TIME                          T_VALUE                    
--------------------------------------------------------------------------------------
TAG_99                2017-02-27 20:53:19 500:000:000 9                          
TAG_99                2017-02-27 20:52:29 500:000:000 8                          
TAG_99                2017-02-27 20:51:39 500:000:000 7                          
TAG_99                2017-02-27 20:50:49 500:000:000 6                          
TAG_99                2017-02-27 20:49:59 500:000:000 5                          
TAG_99                2017-02-27 20:49:09 500:000:000 4                          
TAG_99                2017-02-27 20:48:19 500:000:000 3                          
TAG_99                2017-02-27 20:47:29 500:000:000 2                          
TAG_99                2017-02-27 20:46:39 500:000:000 1                          
TAG_99                2017-02-27 20:45:49 500:000:000 0                          
[10] row(s) selected.
Elapsed time: 0.001
Mach>
```

### 既定のスキャン方向 {#setting-basic-scan-direction-property}

[TABLE_SCAN_DIRECTION](../../../configuration/property/#table_scan_direction) で、SELECT にヒントがない場合の方向を指定できます。
