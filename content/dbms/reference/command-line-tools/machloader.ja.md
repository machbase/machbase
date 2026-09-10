---
type: docs
title: '16.4.3 machloader'
weight: 30
toc: true
---

`machloader`は、CSVなどのテキストファイルとMachbaseサーバー間でデータをインポート/エクスポートする汎用ロードツールです。デフォルトでAPPENDモードを使用し、スキーマファイルによる複雑な変換にも対応します。

## オプション一覧

```bash
machloader -h
```

| オプション | 説明 |
|------|------|
| `-s`, `--server=SERVER` | サーバーIPアドレス (デフォルト値: 127.0.0.1) |
| `-P`, `--port=PORT` | サーバーポート番号 (デフォルト値: 5656) |
| `-u`, `--user=USER` | ユーザー名 (デフォルト値: SYS) |
| `-p`, `--password=PASSWORD` | ユーザーパスワード (デフォルト値: MANAGER) |
| `-i`, `--import` | インポートモード |
| `-o`, `--export` | エクスポートモード |
| `-c`, `--schema` | スキーマファイル生成モード |
| `-t`, `--table=TABLE_NAME` | 対象テーブル名 |
| `-f`, `--form=SCHEMA_FILE` | スキーマファイル名 |
| `-d`, `--data=DATA_FILE` | データファイル名 |
| `-m`, `--mode=MODE` | インポートモード。`append`（デフォルト）または`replace` |
| `-H`, `--header` | ヘッダー行の有無。インポート時は先頭行をヘッダーとして扱い、エクスポート時は列名をヘッダーとして生成 |
| `-D`, `--delimiter=DELIMITER` | フィールド区切り文字 (デフォルト値: `,`) |
| `-n`, `--newline=NEWLINE` | レコード区切り文字 (デフォルト値: `\n`) |
| `-e`, `--enclosure=ENCLOSURE` | フィールドの囲み文字 |
| `-r`, `--format=FORMAT` | ファイル形式 (デフォルト値: csv) |
| `-E`, `--encoding=CHARSET` | ファイルエンコーディング。UTF8（デフォルト）、ASCII、MS949、KSC5601、EUCJP、SHIFTJIS、BIG5、GB231280、UTF16 |
| `-F`, `--dateformat=DATEFORMAT` | datetime列の日付形式。`unixtimestamp`または`nanotimestamp`を指定可能 |
| `-z`, `--timezone` | タイムゾーン設定。例: `+0900`、`-1230` |
| `-a`, `--atime` | `_ARRIVAL_TIME`列を含めるかどうか（デフォルト: 含めない） |
| `-C`, `--create` | インポート時にテーブルがなければ自動作成 |
| `-l`, `--log=LOG_FILE` | 実行ログファイル |
| `-b`, `--bad=BAD_FILE` | 取り込みに失敗した行を記録するbadファイル |
| `--first=FIRST_ROW` | 処理を開始する先頭行番号 |
| `-I`, `--silent` | バナーと進行状況を表示せずに実行 |
| `-S`, `--slash` | バックスラッシュ区切り文字の指定 |
| `--summary` | 選択したオプション値を表示して終了（実際の処理はしない） |
| `-h`, `--help` | オプション一覧を表示 |

## CSVファイルのインポート

基本的なインポート:

```bash
machloader -i -d data.csv -t sensor_data
```

サーバー接続情報の指定:

```bash
machloader -i -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -d data.csv -t sensor_data
```

ヘッダー行のあるCSVのインポート:

```bash
machloader -i -d data.csv -t sensor_data -H
```

既存データを削除してからインポート（replaceモード）:

```bash
machloader -i -d data.csv -t sensor_data -m replace
```

特定の行から開始:

```bash
machloader -i -d data.csv -t sensor_data --first=10
```

## CSVファイルのエクスポート

```bash
machloader -o -d output.csv -t sensor_data
machloader -o -d output.csv -t sensor_data -H
```

`_ARRIVAL_TIME`列を含むエクスポート:

```bash
machloader -o -d output.csv -t sensor_data -a
```

### ARRAY列

Machbase DBMS 8.7.0のARRAY列は`[value,null,value]`形式でインポート/エクスポートします。
ARRAY内部にカンマを含むため、CSVフィールドを囲み文字で囲みます。

```csv
1,"[1.5,null,3.5,4.5]"
```

NULLフィールドはARRAY全体のNULLを表し、`"[null,null]"`は全要素がNULLの非NULL ARRAYを表します。
`-C`によるテーブル自動作成ではARRAY型を推論しないため、ARRAY列が必要なテーブルは事前に
明示的に作成してください。型とNULL規則の詳細は[数値ARRAY型](/dbms/reference/sql/types/array/)を参照してください。

## エンコーディングと区切り文字の設定

EUC-KRエンコーディング、タブ区切り:

```bash
machloader -i -d data.txt -t table_name -E MS949 -D '\t'
```

パイプ（`|`）区切り文字:

```bash
machloader -i -d data.txt -t table_name -D '|'
machloader -o -d data.txt -t table_name -D '|'
```

## タイムゾーンの指定

```bash
machloader -i -d data.csv -t sensor_data -z +0900
machloader -i -d data.csv -t sensor_data -z -1230
```

## datetime形式の指定

コマンドラインで直接指定:

```bash
machloader -i -d data.csv -t sensor_data \
    -F "_arrival_time YYYY-MM-DD HH24:MI:SS"
```

Unixタイムスタンプで取り込み:

```bash
machloader -i -d data.csv -t sensor_data \
    -F "time_column unixtimestamp"
```

ナノ秒タイムスタンプで取り込み:

```bash
machloader -i -d data.csv -t sensor_data \
    -F "time_column nanotimestamp"
```

## スキーマファイルの使用

スキーマファイルを作成します:

```bash
machloader -c -t sensor_data -f sensor_data.fmt
```

スキーマファイルを使ったインポート/エクスポート:

```bash
machloader -i -f sensor_data.fmt -d data.csv
machloader -o -f sensor_data.fmt -d output.csv
```

スキーマファイル形式の例 (`sensor_data.fmt`):

```
table sensor_data
{
    name   varchar(64);
    time   datetime;
    value  double;
}
DATEFORMAT time "YYYY-MM-DD HH24:MI:SS"
```

特定列を無視:

```
table sensor_data
{
    id     integer;
    name   varchar(64);
    extra  varchar(32) IGNORE;
}
```

## ログとbadファイル

```bash
machloader -i -d data.csv -t sensor_data \
    -l import.log -b import.bad
```

- `-l`: インポートの実行ログ（成功/失敗統計）
- `-b`: 失敗した行データを元の形式で記録

## テーブルの自動作成

テーブルがなければ自動作成します。列名は`c0`、`c1`、...の順で、型は`varchar(32767)`です。

```bash
machloader -i -d data.csv -t new_table -C
machloader -i -d data.csv -t new_table -C -H   # ヘッダーを列名として使用
```

## 使用例

```bash
# 実際のインポート前に設定を確認（--summary）
machloader -i -d data.csv -t sensor_data --summary

# 大容量ファイルのインポート（ログとbadファイルを指定）
machloader -i -d bigdata.csv -t sensor_data \
    -H -z +0900 \
    -l import_20240101.log -b import_20240101.bad

# テーブル全体のエクスポート
machloader -o -d export_20240101.csv -t sensor_data -H -a
```
