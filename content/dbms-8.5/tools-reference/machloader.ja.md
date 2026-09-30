---
title : machloader
type : docs
weight: 30
toc: true
---

machloader は、テキストファイルと Machbase 間でデータをインポート、エクスポートします。既定は CSV ですが、他の形式もサポートします。

主な機能と注意事項を示します。

* スキーマファイルで日時形式を指定できます。サーバーがサポートする形式を使用してください。全フィールドに共通の形式、または列ごとに異なる形式を指定できます。
* 既存データを削除してから入力する場合は、`-m replace` を使用します。
* スキーマとデータファイルの整合性は検証しません。スキーマ、テーブル、ファイルの整合性は利用者が確認してください。
* 既定では APPEND モードを使用します。
* 既定では `_ARRIVAL_TIME` を使用しません。この列を入出力するには `-a` を指定します。

日時の書式指定子は [TO_CHAR](../../sql-reference/functions/#to_char) を参照してください。

次のコマンドでオプションを確認できます。

```bash
[mach@localhost]$ machloader -h
```

| オプション | 説明 |
|--|--|
|-s, --server=SERVER|サーバー IP（既定値：127.0.0.1）|
|-u, --user=USER|接続ユーザー（既定値：SYS）|
|-p, --password=PASSWORD|パスワード（既定値：MANAGER）|
|-P, --port=PORT|サーバーポート（既定値：5656）|
|-i, --import|インポート|
|-o, --export|エクスポート|
|-c, --schema|テーブル情報からスキーマファイルを作成|
|-t, --table=TABLE_NAME|スキーマ作成対象のテーブル名|
|-f, --form=SCHEMA_FORM_FILE|スキーマファイル名|
|-d, --data=DATA_FILE|データファイル名|
|-l, --log=LOG_FILE|実行ログファイル|
|-b, --bad=BAD_FILE|-i 実行時の入力エラーデータと、その説明を記録するファイル|
|-m, --mode=MODE|-i の入力方式。append は既存データに追加、replace は既存データを削除してから入力|
|-D, --delimiter=DELIMITER|フィールド区切り文字（既定値：,）|
|-n, --newline=NEWLINE|レコード区切り文字（既定値：\n）|
|-e, --enclosure=ENCLOSURE|各フィールドの囲み文字|
|-r, --format=FORMAT|入出力形式（既定値：csv）|
|--first=FIRST_ROW|処理を開始する行番号|
|-a, --atime|組み込み列 `_ARRIVAL_TIME` を使用するか。既定では使用しない|
|-z, --timezone|タイムゾーン。例：+0900、-1230|
|-I, --silent|著作権表示と入出力状況を非表示にする|
|-h, --help	|オプション一覧を表示|
|-F, --dateformat=DATEFORMAT|列の日時形式。例：`_arrival_time YYYY-MM-DD HH24:MI:SS`。<br>unixtimestamp を指定すると Unix タイムスタンプとして扱う（`time_column unixtimestamp`）。<br>nanotimestamp ではナノ秒時刻として扱う（`time_column nanotimestamp`）|
|-E, --encoding=CHARACTER_SET|入出力ファイルの文字コード。UTF8（既定）、ASCII、MS949、KSC5601、EUCJP、SHIFTJIS、BIG5、GB231280、UTF16 に対応|
|-C, --create|インポート先のテーブルがなければ作成|
|-H, --header|入出力時のヘッダーの有無。既定は未指定|
|--summary|選択した設定を表示して終了。データの入出力は行わない|
|-S, --slash|バックスラッシュ区切りを指定|

詳しい使用方法を示します。

## CSV ファイルのインポート {#csv-file-import}

CSV ファイルを Machbase サーバーへ読み込みます。

オプション：

- `-i`：インポートを指定します。
- `-d`：データファイル名を指定します。
- `-t`：テーブル名を指定します。

例：

```
machloader -i -d data.csv -t table_name
```

## CSV ファイルのエクスポート {#csv-file-export}

データを CSV ファイルに書き出します。

オプション：

- `-o`：エクスポートを指定します。
- `-d`：データファイル名を指定します。
- `-t`：テーブル名を指定します。

例：

```
machloader -o -d data.csv -t table_name
```

## CSV ヘッダーの使用 {#use-csv-file-header}

CSV ファイルのヘッダーに関する設定です。

オプション：

- `-i -H`：インポート時に CSV の先頭行をヘッダーとして扱い、入力から除外します。
- `-o -H`：エクスポート時にテーブルの列名を CSV ヘッダーとして出力します。

例：

```
machloader -i -d data.csv -t table_name -H
machloader -o -d data.csv -t table_name -H
```

## テーブルの自動作成 {#automatic-table-creation}

テーブルの自動作成に関するオプションです。

オプション：

- `-C`：インポート時にテーブルを自動作成します。列名は c0、c1、... の順に生成され、型は `varchar(32767)` です。
- `-H`：インポート時に CSV ヘッダーを列名として使用します。

例：

```
machloader -i -d data.csv -t table_name -C
machloader -i -d data.csv -t table_name -C -H
```

## CSV 以外の形式 {#files-not-csv-format}

CSV 以外の形式のファイルに使用する区切り文字を設定します。

オプション：

- `-D`：フィールドの区切り文字を指定します。
- `-n`：レコードの区切り文字を指定します。
- `-e`：フィールドの囲み文字を指定します。

例：

```
machloader -i -d data.txt -t table_name -D '^' -n '\n' -e '"'
machloader -o -d data.txt -t table_name -D '^' -n '\n' -e '"'
```

## 入力モードの指定 {#specify-input-mode}

インポート（`-i`）には `replace` と `append` の 2 つのモードがあり、既定は `append` です。`replace` は既存データを削除するため、注意して使用してください。

オプション：

- `-m`：インポートモードを指定します。

例：

```
machloader -i -d data.csv -t table_name -m replace
```

## 接続情報の指定 {#specify-connection-information}

サーバー IP、ポート、ユーザー、パスワードを個別に指定します。

オプション：

- `-s`：サーバー IP アドレスを指定します（既定値：127.0.0.1）。
- `-P`：サーバーのポート番号を指定します（既定値：5656）。
- `-u`：接続ユーザー名を指定します（既定値：SYS）。
- `-p`：接続ユーザーのパスワードを指定します（既定値：MANAGER）。

例：

```
machloader -i -s 192.168.0.10 -P 5656 -u mach -p machbase -d data.csv -t table_name
```

## ログファイルの作成 {#create-log-file}

machloader の実行ログファイルと bad-data ファイルを作成します。

オプション：

- `-b`：インポートに失敗した行を記録する bad-data ファイル名を指定します。
- `-l`：インポートに失敗した行とエラーメッセージを記録する実行ログファイル名を指定します。

例：

```
machloader -i -d data.csv -t table_name -b table_name.bad -l table_name.log
```

## スキーマファイルの作成 {#create-schema-file}

machloader のスキーマファイルを作成できます。スキーマファイルを使用すると、データ型の形式を変更する場合や、テーブルの列数とデータファイルのフィールド数が異なる場合もインポート、エクスポートできます。

オプション：

- `-c`：スキーマファイルを作成します。
- `-t`：テーブル名を指定します。
- `-f`：作成するスキーマファイル名を指定します。

例：

```
machloader -c -t table_name -f table_name.fmt
machloader -c -t table_name -f table_name.fmt -a
```

## スキーマファイルの日時形式 {#set-datetime-format-in-schema-file}

`DATEFORMAT` オプションで日時形式を指定できます。

すべての日時列に設定する構文：

```
DATEFORMAT <dateformat>
```

日時列ごとに設定する構文：

```
DATEFORMAT <column_name> <format>
```

例：

```
-- Set dateformat for each field in datetest.csv file in the schema file (datetest.fmt).
datetest.fmt
table datetest
{
INS_DT datetime;
UPT_DT datetime;
}
DATEFORMAT ins_dt "YYYY/MM/DD HH12:MI:SS"
DATEFORMAT upt_dt "YYYY DD MM HH12:MI:SS"
 
datetest.csv
2017/02/20 11:05:23,2017 20 02 11:05:23
2017/02/20 11:06:34,2017 20 02 11:06:34
 
-- Import datetest.csv file and check input data.
machloader -i -f datetest.fmt -d datetest.csv
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 8.5.4.develop
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
Import time : 0 hour 0 min 0.39 sec
Load success count : 2
Load fail count : 0
 
mach> SELECT * FROM datetest;
INS_DT UPT_DT
-------------------------------------------------------------------
2017-02-20 11:06:34 000:000:000 2017-02-20 11:06:34 000:000:000
2017-02-20 11:05:23 000:000:000 2017-02-20 11:05:23 000:000:000
[2] row(s) selected.
Elapsed time: 0.000
```

## IGNORE {#ignore}

CSV ファイルの特定のフィールドを入力しない場合は、fmt ファイルで `IGNORE` オプションを指定します。
`ignoretest.csv` には 3 つのフィールドがあります。最後のフィールドが不要なら、fmt ファイルでその列に `IGNORE` を指定します。

例：

```
-- Set ignore option for last field in ignoretest.fmt file.
ignoretest.fmt
table ignoretest
{
ID integer;
MSG varchar(40);
SUB_ID integer IGNORE;
}
 
ignoretest.csv
1, "msg1", 3
2, "msg2", 4
 
 
-- Import ignoretest.csv file and check input data.
machloader -i -f ignoretest.fmt -d ignoretest.csv
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 8.5.4.develop
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
NLS : US7ASCII EXECUTE MODE : IMPORT
SCHEMA FILE : ignoretest.fmt DATA FILE : ignoretest.csv
IMPORT_MODE : APPEND FIELD TERM : ,
ROW TERM : \n ENCLOSURE : "
ARRIVAL_TIME : FALSE ENCODING : NONE
HEADER : FALSE CREATE TABLE : FALSE
 
Progress bar Imported records Error records
2 0
 
Import time : 0 hour 0 min 0.39 sec
Load success count : 2
Load fail count : 0
 
 
mach> SELECT * FROM ignoretest;
ID MSG
---------------------------------------------------------
2 msg2
1 msg1
[2] row(s) selected.
Elapsed time: 0.000
```

## テーブルの列数がファイルのフィールド数より多い場合 {#if-number-of-columns-is-more-than-number-of-fields}

テーブルの列数がデータファイルのフィールド数より多い場合、スキーマファイルで指定した列にだけデータを入力し、残りの列には `NULL` を格納します。

## テーブルの列数がファイルのフィールド数より少ない場合 {#if-number-of-columns-is-less-than-number-of-fields}

テーブルの列数がデータファイルのフィールド数より少ない場合、テーブルにないフィールドは `IGNORE` オプションで除外する必要があります。

例：

```
-- Exclude the input data by setting the IGNORE option on the last field.
loader_test.fmt
table loader_test
{
ID integer;
MSG varchar (40);
SUB_ID integer IGNORE;
}
```
