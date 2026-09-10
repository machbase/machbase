---
title : ストリームの使用例
type: docs
weight: 30
toc: true
---

## サンプルデータのダウンロード {#download-sample-data}

次の手順でサンプルデータをダウンロードします。

```bash
#1．MACHBASE の Git リポジトリからサンプルを取得
$ git clone https://github.com/MACHBASE/TagTutorial.git MyTutorial
 
#2．必要なデータを展開
$ cd MyTutorial/
$ gunzip edu_3_plc_stream/*.gz
 
#3．サンプルデータのディレクトリへ移動
$ cd edu_3_plc_stream/
```

## TAG テーブルと LOG テーブルの作成 {#create-tag-log-table}

STREAM を使用するため、次のコマンドを環境に合わせて変更し、TAG テーブルと LOG テーブルを作成します。

```bash
$ pwd
~/MyTutorial/edu_3_plc_stream
 
#1-1．TAG を作成
$ machsql --server=127.0.0.1 --port=${MACHBASE_PORT_NO} --user=SYS --password=MANAGER --script=1_create_tag.sql
#1-2．TAG メタデータを入力
$ sh 2_load_meta.sh
 
#2．LOG を作成
$ machsql --server=127.0.0.1 --port=${MACHBASE_PORT_NO} --user=SYS --password=MANAGER --script=3_create_plc_tag_table.sql
```

## STREAM の作成と実行 {#create-and-run-stream}

作成した TAG テーブルと LOG テーブル用のサンプルファイルを実行し、STREAM を開始します。

```bash
$ machsql --server=127.0.0.1 --port=${MACHBASE_PORT_NO} --user=SYS --password=MANAGER --script=4_plc_stream_tag.sql
```

サンプルには、STREAM を作成するクエリーと開始するクエリーの 2 種類が含まれます。

```sql
#STREAM クエリーの作成例
EXEC STREAM_CREATE(event_v0, 'insert into tag select ''MTAG_V00'', tm, v0 from plc_tag_table;');

#STREAM クエリーの開始例
EXEC STREAM_START(event_v0);
```

正常に開始されると、plc_tag_table への入力に応じて各 STREAM が動作し、TAG テーブルへデータを挿入します。

## STREAM の状態確認 {#check-stream-status}

仮想テーブル v$streams で、実行中のストリーム数、クエリー、状態、エラーメッセージを確認できます。

```sql
Mach> desc v$streams;
[ COLUMN ]
----------------------------------------------------------------------------------------------------
NAME                                                        NULL?    TYPE                LENGTH
----------------------------------------------------------------------------------------------------
NAME                                                                 varchar             100
LAST_EX_TIME                                                         datetime            31
TABLE_NAME                                                           varchar             100
END_RID                                                              long                20
STATE                                                                varchar             10
QUERY_TXT                                                            varchar             2048
ERROR_MSG                                                            varchar             2048
FREQUENCY                                                            ulong               20
```

次のように、すべての STREAM の状態を確認できます。

```sql
Mach> select state, name, table_name, query_txt from v$streams;
STATE   NAME     TABLE_NAME    QUERY_TXT
------------------------------------------------------------------------------------------------
RUNNING EVENT_V0 PLC_TAG_TABLE insert into tag select 'MTAG_V00', tm, v0 from plc_tag_table;
RUNNING EVENT_V1 PLC_TAG_TABLE insert into tag select 'MTAG_V00', tm, v1 from plc_tag_table;
RUNNING EVENT_C0 PLC_TAG_TABLE insert into tag select 'MTAG_C00', tm, c0 from plc_tag_table;
RUNNING EVENT_C1 PLC_TAG_TABLE insert into tag select 'MTAG_C01', tm, c1 from plc_tag_table;
RUNNING EVENT_C2 PLC_TAG_TABLE insert into tag select 'MTAG_C02', tm, c2 from plc_tag_table;
RUNNING EVENT_C3 PLC_TAG_TABLE insert into tag select 'MTAG_C03', tm, c3 from plc_tag_table;
RUNNING EVENT_C4 PLC_TAG_TABLE insert into tag select 'MTAG_C04', tm, c4 from plc_tag_table;
RUNNING EVENT_C5 PLC_TAG_TABLE insert into tag select 'MTAG_C05', tm, c5 from plc_tag_table;
RUNNING EVENT_C6 PLC_TAG_TABLE insert into tag select 'MTAG_C06', tm, c6 from plc_tag_table;
RUNNING EVENT_C7 PLC_TAG_TABLE insert into tag select 'MTAG_C07', tm, c7 from plc_tag_table;
RUNNING EVENT_C8 PLC_TAG_TABLE insert into tag select 'MTAG_C08', tm, c8 from plc_tag_table;
RUNNING EVENT_C9 PLC_TAG_TABLE insert into tag select 'MTAG_C09', tm, c9 from plc_tag_table;
RUNNING EVENT_C10 PLC_TAG_TABLE insert into tag select 'MTAG_C10', tm, c10 from plc_tag_table;
RUNNING EVENT_C11 PLC_TAG_TABLE insert into tag select 'MTAG_C11', tm, c11 from plc_tag_table;
RUNNING EVENT_C12 PLC_TAG_TABLE insert into tag select 'MTAG_C12', tm, c12 from plc_tag_table;
RUNNING EVENT_C13 PLC_TAG_TABLE insert into tag select 'MTAG_C13', tm, c13 from plc_tag_table;
RUNNING EVENT_C14 PLC_TAG_TABLE insert into tag select 'MTAG_C14', tm, c14 from plc_tag_table;
RUNNING EVENT_C15 PLC_TAG_TABLE insert into tag select 'MTAG_C15', tm, c15 from plc_tag_table;
```

## データの読み込み {#load-data}

すべての STREAM が実行中であることを確認し、machloader でデータを入力して動作を確認します。
STREAM は入力方法に依存しません。CLI、JDBC、Collector など、どの方法で入力しても TAG テーブルへ自動的に挿入します。

```bash
$ cat 5_plc_tag_load.sh
machloader -i -t plc_tag_table -d 5_plc_tag.csv -F "tm YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"
 
$ sh 5_plc_tag_load.sh
-----------------------------------------------------------------
     Machbase Data Import/Export Utility.
     Release Version 8.5.4.develop
     Copyright 2014 MACHBASE Corporation or its subsidiaries.
     All Rights Reserved.
-----------------------------------------------------------------
NLS            : US7ASCII            EXECUTE MODE   : IMPORT
TARGET TABLE   : plc_tag_table       DATA FILE      : 5_plc_tag.csv
IMPORT MODE    : APPEND              FIELD TERM     : ,
ROW TERM       : \n                  ENCLOSURE      : "
ESCAPE         : \                   ARRIVAL_TIME   : FALSE
ENCODING       : NONE                HEADER         : FALSE
CREATE TABLE   : FALSE              CREATE TABLESPACE: FALSE
 
 Progress bar                       Imported records        Error records
                                               80000                    0
```

読み込み中に TAG テーブルを検索すると、リアルタイムで挿入されていることを確認できます。

```sql
Mach> select count(*) from TAG;
count(*)
-----------------------
16775979
[1] row(s) selected.
Mach> select count(*) from TAG;
count(*)
-----------------------
17609187
[1] row(s) selected.
Mach> select count(*) from TAG;
count(*)
-----------------------
18238357
[1] row(s) selected.
Elapsed time: 0.000
```

## STREAM の実行結果 {#result-of-stream}

次のように、元テーブル plc_tag_table のどこまで読み取ったか確認できます。

```sql
Mach> select name, state, end_rid from v$streams;
name      state   end_rid
---------------------------------------------------------
EVENT_V0  RUNNING 909912
EVENT_V1  RUNNING 1584671
EVENT_C0  RUNNING 1312416
EVENT_C1  RUNNING 1268520
EVENT_C2  RUNNING 1636800
EVENT_C3  RUNNING 1197840
EVENT_C4  RUNNING 622728
EVENT_C5  RUNNING 972780
EVENT_C6  RUNNING 1021512
EVENT_C7  RUNNING 1287474
EVENT_C8  RUNNING 826956
EVENT_C9  RUNNING 1639032
EVENT_C10 RUNNING 725954
EVENT_C11 RUNNING 1511436
EVENT_C12 RUNNING 531079
EVENT_C13 RUNNING 1004400
EVENT_C14 RUNNING 741768
EVENT_C15 RUNNING 746604
[18] row(s) selected.
```

end_rid が元テーブルのレコード数と一致すれば、未処理のデータはありません。

```sql
Mach> select name, state, end_rid from v$streams;
name      state   end_rid
---------------------------------------------------------
EVENT_V0  RUNNING 2000000
EVENT_V1  RUNNING 2000000
EVENT_C0  RUNNING 2000000
EVENT_C1  RUNNING 2000000
EVENT_C2  RUNNING 2000000
EVENT_C3  RUNNING 2000000
EVENT_C4  RUNNING 2000000
EVENT_C5  RUNNING 2000000
EVENT_C6  RUNNING 2000000
EVENT_C7  RUNNING 2000000
EVENT_C8  RUNNING 2000000
EVENT_C9  RUNNING 2000000
EVENT_C10 RUNNING 2000000
EVENT_C11 RUNNING 2000000
EVENT_C12 RUNNING 2000000
EVENT_C13 RUNNING 2000000
EVENT_C14 RUNNING 2000000
EVENT_C15 RUNNING 2000000
[18] row(s) selected.
```

TAG テーブルの件数が「元テーブルのレコード数 × STREAM 数」と一致すれば、すべてのデータが正常に処理されたことを確認できます。

```sql
Mach> select count(*) from TAG;
count(*)
-----------------------
36000000
[1] row(s) selected.
```

入力データの時刻範囲も、次のように確認できます。

```sql
Mach> select min(time), max(time) from TAG;
min(time)                       max(time)
-------------------------------------------------------------------
2009-01-28 07:03:34 000:000:000 2009-01-28 12:36:58 020:000:000
[1] row(s) selected.
```

## データの追加 {#add-data}

INSERT 文でデータを追加し、入力のたびに STREAM が反応するか確認できます。

```sql
Mach> insert into plc_tag_table values(TO_DATE('2009-01-28 12:37:00 000:000:000'), 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000);
1 row(s) inserted.
```

PLC_TAG_TABLE に 1 レコードを追加すると、次のように各ストリームの end_rid が 2000001 に増加します。

```sql
Mach> select name, state, end_rid from v$streams;
name      state   end_rid
---------------------------------------------------------------
EVENT_V0  RUNNING 2000001
EVENT_V1  RUNNING 2000001
EVENT_C0  RUNNING 2000001
EVENT_C1  RUNNING 2000001
EVENT_C2  RUNNING 2000001
EVENT_C3  RUNNING 2000001
EVENT_C4  RUNNING 2000001
EVENT_C5  RUNNING 2000001
EVENT_C6  RUNNING 2000001
EVENT_C7  RUNNING 2000001
EVENT_C8  RUNNING 2000001
EVENT_C9  RUNNING 2000001
EVENT_C10 RUNNING 2000001
EVENT_C11 RUNNING 2000001
EVENT_C12 RUNNING 2000001
EVENT_C13 RUNNING 2000001
EVENT_C14 RUNNING 2000001
EVENT_C15 RUNNING 2000001
[18] row(s) selected.
```
