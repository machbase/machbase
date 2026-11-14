---
type: docs
title: '16.4.5 tagmetaimport'
weight: 50
toc: true
---

`tagmetaimport`はCSVファイルからTAGテーブルのメタデータを一括インポートするツールです。大量の
TAG名とメタデータの登録に使用します。既存タグの自動更新やファイル全体の単一トランザクションでの反映は行いません。

## オプション一覧

```bash
tagmetaimport -h
```

| オプション | 説明 |
|------|------|
| `-s`, `--server=SERVER` | サーバーIPアドレス (デフォルト値: 127.0.0.1) |
| `-P`, `--port=PORT` | サーバーポート番号 (デフォルト値: 5656) |
| `-u`, `--user=USER` | ユーザー名 (デフォルト値: SYS) |
| `-p`, `--password=PASSWORD` | ユーザーパスワード (デフォルト値: MANAGER) |
| `-t`, `--table=TABLE_NAME` | 対象のメタデータ保存テーブル名。論理sensor_tagには_SENSOR_TAG_METAを指定 |
| `-d`, `--data=DATA_FILE` | メタデータCSVファイルのパス |
| `-l`, `--log=LOG_FILE` | ログファイルのパス |
| `-b`, `--bad=BAD_FILE` | 取り込みに失敗したレコードの保存先ファイル |
| `-H`, `--header` | CSVの先頭行をヘッダーとして扱う |
| `-D`, `--delimiter=DELIMITER` | フィールド区切り文字 (デフォルト値: `,`) |
| `-E`, `--encoding=CHARSET` | ファイルエンコーディング (デフォルト値: UTF8) |
| `-I`, `--silent` | 進行状況の出力を削減。完了サマリーで成功・失敗件数を確認 |
| `-h`, `--help` | オプション一覧を表示 |

## 入力ファイル形式

メタデータCSVファイルは、TAGテーブルのメタデータ列の順序に合わせて作成します。

TAGテーブルの定義例:

```sql
CREATE TAG TABLE sensor_tag (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE      SUMMARIZED
) METADATA (
    unit   VARCHAR(32),
    location VARCHAR(128)
);
```

このテーブルのメタデータCSVファイル（`tag_meta.csv`）:

```
name,unit,location
sensor_001,celsius,Building-A Floor-1
sensor_002,celsius,Building-A Floor-2
sensor_003,bar,Boiler-Room
sensor_004,rpm,Motor-Section
```

ヘッダーなしでデータだけの場合:

```
sensor_001,celsius,Building-A Floor-1
sensor_002,celsius,Building-A Floor-2
```

## 使用例

### 基本的なインポート

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta.csv -H
```

### ヘッダー付きCSVファイルのインポート

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta.csv -H
```

### リモートサーバーへのインポート

```bash
tagmetaimport -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta.csv -H
```

### タブ区切りファイル

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta.tsv -D '\t' -H
```

### EUC-KRエンコーディングのファイル

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
    -t _SENSOR_TAG_META -d tag_meta_kr.csv -E MS949 -H
```

## 動作

- `-t`は論理TAGをMETADATA対象へ自動変換しません。論理テーブルsensor_tagの対象は`_SENSOR_TAG_META`です。この名前はツールの取り込み先の指定にのみ使用します。
- 既存のタグ名は通常のMETADATA INSERTでエラーになります。失敗件数とbad/logファイルで確認します。
- データの取り込み後にメタデータを追加する場合、このツールが効率的です。
- 少量のメタデータはSQL INSERTまたは`machsql`で直接取り込むこともできます。

```sql
-- machsqlでメタデータを直接挿入
INSERT INTO sensor_tag METADATA (name, unit, location)
VALUES ('sensor_005', 'volt', 'Panel-Room');
```

## 注意事項

- 事前にTAGテーブルを作成してください。
- CSVファイルの列順序はTAGテーブルのメタデータ列の順序に合わせてください。
- `BASETIME`列（`time`）と`SUMMARIZED`列（`value`）はメタデータファイルに含めません。

既存値の変更には`UPDATE sensor_tag METADATA ...`または明示的なSQL UPSERTを使用します。
再現可能な新規取り込みと重複取り込み失敗の例は、[メタデータの一括登録](../../../tag-table-usage/tagmetaimport/)を
参照してください。`_LAST_UPDATE_TIME`は、新規メタデータの取り込み時と値の実際の変更時にサーバーが管理します。
