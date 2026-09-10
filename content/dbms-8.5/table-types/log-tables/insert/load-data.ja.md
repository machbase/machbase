---
title : SQL による読み込み
type: docs
weight: 40
toc: true
---

LOAD DATA 文で、CSV ファイルのデータを Machbase に読み込みます。

CSV ファイルの先頭行を列名として、データを保存するテーブルを作成します。

* 自動作成される列のデータ型は VARCHAR(32767) です。
* データファイルには $MACHBASE_HOME を基準とする相対パス、または絶対パスを指定できます。

テーブルのデータを CSV ファイルに保存するには、SAVE DATA 文を使用します。

テーブルを事前に作成する場合は、CSV の各フィールドに対応する列を VARCHAR または TEXT 型にしてください。

LOAD DATA 文に load_sample.csv を指定すると、load_sample テーブルが自動作成されます。


## データの読み込み {#loading-data}

```sql
LOAD DATA INFILE 'sample/quickstart/load_sample.csv' INTO TABLE load_sample AUTO HEADUSE;
```

## 読み込み結果の確認 {#confirm-data-loading}

```sql
SELECT * FROM load_sample;
```


## 実行例 {#sample-example}

サンプルファイルを使用して、次のように実行できます。

```bash
[mach@localhost ~]$ cd $MACHBASE_HOME/sample/quickstart
[mach@localhost ~]$ ls -l load_sample.csv
-rw-r--r-- 1 mach mach 2373 Jun 13 15:07 load_sample.csv
 
[mach@localhost ~]$ machsql
=================================================================
     Machbase Client Query Utility
     Release Version x.x.x.official
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved
=================================================================
Machbase server address (Default:127.0.0.1) :
Machbase user ID  (Default:SYS)
Machbase User Password :
MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
 
Mach> LOAD DATA INFILE 'sample/quickstart/load_sample.csv' INTO TABLE load_sample AUTO HEADUSE;
50 row(s) loaded.
Mach> DESC load_sample;
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
SENSOR_ID                     varchar             32767
EPOCH_TIME                    varchar             32767
E_YEAR                        varchar             32767
E_MONTH                       varchar             32767
E_DAY                         varchar             32767
E_HOUR                        varchar             32767
E_MINUTE                      varchar             32767
E_SECOND                      varchar             32767
VALUE                         varchar             32767
Mach> SELECT COUNT(*) FROM load_sample;
COUNT(*)
-----------------------
50
[1] row(s) selected.
Mach>
```
