---
title : 'csvimport / csvexport'
type : docs
weight: 10
toc: true
---

csvimport と csvexport は、Machbase サーバーと CSV ファイル間でデータをインポート、エクスポートするツールです。

machloader のオプションを簡略化し、CSV ファイルを扱いやすくしています。

以下のオプションに加えて、machloader のすべてのオプションを使用できます。

日時の書式指定子は [TO_CHAR](../../sql-reference/functions/#to_char) を参照してください。

## 共通のラッパーオプション {#common-wrapper-options}

よく使用する machloader オプションを、CSV ラッパーでも利用できます。

| オプション | 対象 | 説明 |
|--|--|--|
| -P, --port=PORT | csvimport, csvexport | サーバーのポート番号（既定値：5656） |
| -l, --log=LOG_FILE | csvimport, csvexport | 実行ログファイル |
| -b, --bad=BAD_FILE | csvimport | インポートに失敗した行の出力ファイル |
| -m, --mode=MODE | csvimport | インポートモード（`append` または `replace`、既定値：`append`） |
| -a, --atime | csvimport, csvexport | `_ARRIVAL_TIME` 列を含める |
| -I, --silent | csvimport, csvexport | 出力量を減らす |
| -F, --dateformat=DATEFORMAT | csvimport, csvexport | 列の日時書式。例：`_arrival_time YYYY-MM-DD HH24:MI:SS` |

## csvimport {#csvimport}

csvimport で CSV ファイルをサーバーに読み込めます。

### 基本的な使用方法 {#basic-usage}

次のオプションでテーブル名とデータファイル名を指定します。

オプション：

```
-t：テーブル名を指定
-d：データファイル名を指定
* オプションを省略し、テーブル名とファイル名だけでも実行可能
```

例：

```
csvimport -t table_name -d table_name.csv
csvimport table_name file_path
csvimport file_path table_name
```

### CSV ヘッダーの除外 {#csv-header-exception}

読み込み時にヘッダーを除外するには、次のオプションを使用します。

オプション：

```
-H：先頭行をヘッダーとして扱い、入力から除外
```

例：

```
csvimport -t table_name -d table_name.csv -H
```

### テーブルの自動作成 {#automatic-table-creation}

読み込み先のテーブルが存在しない場合は、次のオプションで読み込み時に作成できます。

オプション：

```
-C：入力時にテーブルを自動作成。列名は c0、c1、...、型は VARCHAR(32767)
-H：CSV ヘッダーを列名として使用
```

例：

```
csvimport -t table_name -d table_name.csv -C
csvimport -t table_name -d table_name.csv -C -H
```


## csvexport {#csvexport}

csvexport でテーブルのデータを CSV ファイルに出力できます。

### 基本的な使用方法 {#basic-usage-1}

オプション：

```
-t：テーブル名を指定
-d：データファイル名を指定
* オプションを省略し、テーブル名とファイル名だけでも実行可能
```

例：

```
csvexport -t table_name -d table_name.csv
csvexport table_name file_path
csvexport file_path table_name
```

### CSV ヘッダーの出力 {#using-csv-header}

次のオプションで、列名のヘッダーを CSV ファイルに追加できます。

オプション：

```
-H：テーブルの列名を CSV ヘッダーとして出力
```

例：

```
csvexport -t table_name -d table_name.csv -H
```
