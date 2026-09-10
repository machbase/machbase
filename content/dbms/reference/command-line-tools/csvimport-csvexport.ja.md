---
type: docs
title: '16.4.4 csvimport / csvexport'
weight: 40
toc: true
---

`csvimport`と`csvexport`は、CSVファイル専用の簡易インポート/エクスポートラッパーです。`machloader`のCSV関連オプションを簡略化して提供します。以下にないオプションも`machloader`と同様に使用できます。

## csvimport

CSVファイルをMachbaseテーブルにインポートします。

### オプション一覧

| オプション | 説明 |
|------|------|
| `-t`, `--table=TABLE_NAME` | 対象テーブル名 |
| `-d`, `--data=DATA_FILE` | インポートするCSVファイル名 |
| `-s`, `--server=SERVER` | サーバーIPアドレス (デフォルト値: 127.0.0.1) |
| `-P`, `--port=PORT` | サーバーポート番号 (デフォルト値: 5656) |
| `-u`, `--user=USER` | ユーザー名 (デフォルト値: SYS) |
| `-p`, `--password=PASSWORD` | ユーザーパスワード (デフォルト値: MANAGER) |
| `-H` | CSVの先頭行をヘッダーとして扱い、取り込みから除外 |
| `-C` | テーブルがなければ自動作成（`-H`を併用するとヘッダーを列名として使用） |
| `-m`, `--mode=MODE` | インポートモード。`append`（デフォルト）または`replace` |
| `-a`, `--atime` | `_ARRIVAL_TIME`列を含める |
| `-F`, `--dateformat=DATEFORMAT` | datetime列の日付形式 |
| `-l`, `--log=LOG_FILE` | 実行ログファイル |
| `-b`, `--bad=BAD_FILE` | 取り込みに失敗した行を記録するbadファイル |
| `-I`, `--silent` | バナーと状態を表示せずに実行 |

### 基本的な使用方法

テーブル名とファイル名を指定します。

```bash
csvimport -t table_name -d data.csv
```

オプションなしで引数だけでも実行できます（順序は任意）。

```bash
csvimport table_name data.csv
csvimport data.csv table_name
```

### ヘッダー行の処理

CSVの先頭行をヘッダーとして扱い、データから除外します。

```bash
csvimport -t table_name -d data.csv -H
```

### テーブルの自動作成

テーブルがなければ自動作成します。

```bash
# 列名をc0、c1、...として自動生成
csvimport -t table_name -d data.csv -C

# CSV ヘッダーを列名として使用
csvimport -t table_name -d data.csv -C -H
```

自動作成した列の型はすべて`varchar(32767)`です。

### replaceモード

既存データを削除し、CSVファイルから再び取り込みます。

```bash
csvimport -t table_name -d data.csv -m replace
```

### サーバー接続情報の指定

```bash
csvimport -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -t sensor_data -d data.csv
```

## csvexport

MachbaseテーブルのデータをCSVファイルへエクスポートします。

### オプション一覧

| オプション | 説明 |
|------|------|
| `-t`, `--table=TABLE_NAME` | エクスポートするテーブル名 |
| `-d`, `--data=DATA_FILE` | 保存するCSVファイル名 |
| `-s`, `--server=SERVER` | サーバーIPアドレス (デフォルト値: 127.0.0.1) |
| `-P`, `--port=PORT` | サーバーポート番号 (デフォルト値: 5656) |
| `-u`, `--user=USER` | ユーザー名 (デフォルト値: SYS) |
| `-p`, `--password=PASSWORD` | ユーザーパスワード (デフォルト値: MANAGER) |
| `-H` | 列名をCSVヘッダーとして生成 |
| `-a`, `--atime` | `_ARRIVAL_TIME`列を含める |
| `-F`, `--dateformat=DATEFORMAT` | datetime列の日付形式 |
| `-l`, `--log=LOG_FILE` | 実行ログファイル |
| `-I`, `--silent` | バナーと状態を表示せずに実行 |

### 基本的な使用方法

```bash
csvexport -t table_name -d output.csv
```

オプションなしで引数だけでも実行できます。

```bash
csvexport table_name output.csv
csvexport output.csv table_name
```

### ヘッダーを含むエクスポート

列名をCSVファイルの先頭行（ヘッダー）として出力します。

```bash
csvexport -t table_name -d output.csv -H
```

### `_ARRIVAL_TIME`を含むエクスポート

```bash
csvexport -t table_name -d output.csv -a
```

## 使用例

```bash
# 基本的なインポート
csvimport -t sensor_data -d sensor_20240101.csv

# ヘッダー付きCSVのインポート
csvimport -t sensor_data -d sensor_20240101.csv -H

# 全データのエクスポート（ヘッダーを含む）
csvexport -t sensor_data -d export_20240101.csv -H

# ログファイルを指定してインポート
csvimport -t sensor_data -d data.csv -H \
    -l import.log -b import.bad

# リモートサーバーからエクスポート
csvexport -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -t sensor_data -d remote_export.csv -H -a
```
