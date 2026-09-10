---
title : インポート
type: docs
weight: 30
toc: true
---

machloader を使用すると、CSV やその他の区切り文字形式のテキストファイルを読み込めます。

詳細は [machloader](/ja/dbms-8.5/tools-reference/machloader/) を参照してください。

## 目次 {#index}

* [データのインポート](#importing-data)
* [挿入結果の確認](#confirm-data-insert)
* [実行例](#sample-example)


## テーブルの作成 {#create-table}

```sql
CREATE TABLE import_sample
(
    srcip     IPV4,
    srcport   INTEGER,
    dstip     IPV4,
    dstport   INTEGER,
    protocol  SHORT,
    eventlog  VARCHAR(1024),
    eventcode SHORT,
    eventsize LONG
);
```


## データのインポート {#importing-data}

machloader で CSV ファイルを読み込みます。

```bash
machloader  -i  -t  import_sample   -d  sample_data.csv
```


## 挿入結果の確認 {#confirm-data-insert}

挿入したデータを確認します。


``` sql
SELECT  COUNT(*)    FROM    import_sample;
```


## 実行例 {#sample-example}

machloader と machsql を使用する一連の操作を示します。

```sql
Mach> CREATE TABLE import_sample
     (
         srcip     IPV4,
         srcport   INTEGER,
         dstip     IPV4,
         dstport   INTEGER,
         protocol  SHORT,
         eventlog  VARCHAR(1024),
         eventcode SHORT,
         eventsize LONG
     );
Created successfully.
Mach> quit
```

```bash
[mach@localhost ~]$ cd $MACHBASE_HOME/sample/quickstart
[mach@localhost ~]$ tar -xzf sample_data.tar.gz
[mach@localhost ~]$ ls -l sample_data.csv
-rw-r--r-- 1 mach mach 110477124 Nov  9  2022 sample_data.csv
 
[mach@localhost ~]$ machloader -i -t import_sample -d sample_data.csv
-----------------------------------------------------------------
     Machbase Data Import/Export Utility.
     Release Version x.x.x.official
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved.
-----------------------------------------------------------------
NLS            : US7ASCII            EXECUTE MODE   : IMPORT
TARGET TABLE   : import_sample
DATA FILE      : sample_data.csv
IMPORT MODE    : APPEND              FIELD TERM     : ,
ROW TERM       : \n                  ENCLOSURE      : "
ESCAPE         : \                   ARRIVAL_TIME   : FALSE
ENCODING       : NONE                HEADER         : FALSE
CREATE TABLE   : FALSE
 Progress bar                       Imported records        Error records
                                             1000000                    0
Import time         :  0 hour  0 min  2.39 sec
Load success count  : 1000000
Load fail count     : 0
[mach@localhost ~]$
```

```sql
Mach> SELECT COUNT(*) FROM import_sample;
COUNT(*)
-----------------------
1000000
[1] row(s) selected.
Mach>
```
