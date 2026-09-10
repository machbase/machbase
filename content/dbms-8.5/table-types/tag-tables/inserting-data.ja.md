---
title: 'Tag データの挿入'
type: docs
weight: 30
toc: true
---

## 概要 {#overview}

時間軸と距離軸の Tag データを入力する複数の方法があります。データ量とアプリケーションの要件に合わせて選択してください。

## 方法 1：`INSERT` 文 {#method-1-insert-statement}

少量のデータやテストに適した、最も簡単な方法です。

### 基本的な `INSERT` の例 {#basic-insert-example}

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
Executed successfully.

Mach> insert into tag metadata values ('TAG_0001');
1 row(s) inserted.

-- 個別の値を入力
Mach> insert into tag values('TAG_0001', now, 0);
1 row(s) inserted.

Mach> insert into tag values('TAG_0001', now, 1);
1 row(s) inserted.

Mach> insert into tag values('TAG_0001', now, 2);
1 row(s) inserted.

Mach> EXEC TABLE_FLUSH(tag);
Executed successfully.

Mach> select * from tag where name = 'TAG_0001';
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
TAG_0001              2018-12-19 17:41:37 806:901:728 0
TAG_0001              2018-12-19 17:41:42 327:839:368 1
TAG_0001              2018-12-19 17:41:43 812:782:202 2
[3] row(s) selected.
```

対話的な例では `EXEC TABLE_FLUSH(tag)` を実行すると、挿入したばかりの行を
直後のクエリーと統計ビューで確認できます。

> **用途**：テスト、少量の入力、対話的な入力

### TAG メタデータと `_LAST_UPDATE_TIME` {#tag-metadata-and-_last_update_time}

メタデータ列がない場合は、`name`、`time`、`value` の 3 値だけを入力できます。

```sql
CREATE TAG TABLE sensor (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);

INSERT INTO sensor VALUES('tag1', now, 1);
```

ユーザー定義メタデータ列があり、列リストを省略して新しいタグを入力する場合は、データ値とメタデータ値を一緒に指定します。`_LAST_UPDATE_TIME` はシステムが管理するメタデータ変更時刻なので、指定しないでください。

```sql
CREATE TAG TABLE sensor_meta (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    site   VARCHAR(32),
    status INTEGER
);

INSERT INTO sensor_meta
VALUES('tag1', now, 1, 'seoul', 1);
```

列リストを使用する場合は、必要なユーザー定義列だけを指定します。`_LAST_UPDATE_TIME` は指定しません。

```sql
INSERT INTO sensor_meta(name, time, value, site, status)
VALUES('tag2', now, 1, 'busan', 1);
```

タグのメタデータがすでに存在する場合、データだけの入力ではメタデータも `_LAST_UPDATE_TIME` も変更されません。

### 距離軸の `INSERT` の例 {#distance-axis-insert-example}

距離軸でも `INSERT` 構文は同じですが、軸列には数値の距離を保存します。

```sql
Mach> CREATE TAG TABLE trip_sensor (
          name        VARCHAR(20) PRIMARY KEY,
          distance_m  DOUBLE BASE DISTANCE,
          value       DOUBLE,
          quality     INTEGER
      );
Executed successfully.

Mach> INSERT INTO trip_sensor VALUES('ODO_A', 0, 10.1, 100);
1 row(s) inserted.

Mach> INSERT INTO trip_sensor VALUES('ODO_A', 500, 11.2, 101);
1 row(s) inserted.

Mach> INSERT INTO trip_sensor VALUES('ODO_B', 1000.1, 21.5, 100);
1 row(s) inserted.

Mach> EXEC TABLE_FLUSH(trip_sensor);
Executed successfully.
```

`DOUBLE` は小数の距離、`LONG` と `ULONG` は整数の距離を保存します。

## 方法 2：CSV のインポート {#method-2-csv-file-import}

`csvimport` で、CSV から大量データを高速に読み込めます。

### CSV 形式 {#csv-file-format}

タグ名、時刻、値を持つ `data.csv` を作成します。

```csv
TAG_0001, 2009-01-28 07:03:34 0:000:000, -41.98
TAG_0001, 2009-01-28 07:03:34 1:000:000, -46.50
TAG_0001, 2009-01-28 07:03:34 2:000:000, -36.16
```

### `csvimport` の使用 {#using-csvimport}

```bash
csvimport -t TAG -d data.csv -F "time YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" -l error.log
```

**オプション：**
- `-t TAG`：対象テーブル
- `-d data.csv`：データファイル
- `-F`：日時形式
- `-l error.log`：エラーログ

> **用途**：一括読み込み、データ移行、バッチインポート

> **注意**：未登録のタグ名は、インポート時に自動登録されます。単位、場所、状態などのメタデータが入力前に必要なら、先に登録してください。

## 方法 3：RESTful API {#method-3-restful-api}

HTTP で入力します。IoT デバイスや Web アプリケーションに適しています。

### API 構文 {#api-syntax}

```json
{
  "values": [
    [TAG_NAME, TAG_TIME, VALUE],
    [TAG_NAME, TAG_TIME, VALUE],
    ...
  ],
  "date_format": "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"
}
```

`date_format` を省略すると、`YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn` を使用します。

時間軸には日時文字列、距離軸には列型に一致する数値を指定します。

### API の例 {#api-example}

```bash
curl -X POST http://localhost:5657/machiot/datapoints/raw/TAG \
  -H "Content-Type: application/json" \
  -d '{
    "date_format": "YYYY-MM-DD HH24:MI:SS",
    "values": [
      ["TAG_0001", "2024-01-01 10:00:00", 25.5],
      ["TAG_0001", "2024-01-01 10:01:00", 26.0],
      ["TAG_0002", "2024-01-01 10:00:00", 30.2]
    ]
  }'
```

> **用途**：IoT、リアルタイムストリーミング、Web アプリケーション

## 方法 4：SDK 連携 {#method-4-sdk-integration}

SDK を使用すると、アプリケーションからプログラムで入力できます。

### 対応言語 {#supported-languages}

- **[C/C++](../../../sdk-integration/cli-odbc/)**：高速なネイティブ連携
- **[Java](../../../sdk-integration/jdbc/)**：Java アプリケーション
- **[Python](../../../sdk-integration/python/)**：データサイエンスと自動化
- **[C#](../../../sdk-integration/dotnet/)**：.NET アプリケーション

### Python の例 {#python-example}

```python
import machbaseAPI as mach

# Machbase に接続
conn = mach.connect(host='localhost', port=5656)

# データを挿入
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO tag VALUES (?, ?, ?)
""", ('TAG_0001', '2024-01-01 10:00:00', 25.5))

conn.close()
```

各文は自動コミットされます。`commit()` はサポートされないため呼び出しません。

> **用途**：アプリケーション連携、自動収集、独自ツール

## 入力方法の選択 {#choosing-the-right-method}

| 方法 | 主な用途 | 利点 | 制約 |
|--------|----------|------|------|
| `INSERT` | テスト、少量データ | 簡単で対話的 | 大量データには遅い |
| CSV インポート | 一括読み込み、移行 | 高速で効率的 | ファイルの準備が必要 |
| RESTful API | IoT、Web | 柔軟でプラットフォーム非依存 | 通信のオーバーヘッド |
| SDK | アプリケーション | 詳細な制御、型安全性 | 開発が必要 |

## 追加列の入力 {#working-with-additional-columns}

追加列がある場合は、入力に含めます。

軸の値は、定義と列順に合わせてください。時間軸は `DATETIME`、距離軸は `DOUBLE`、`LONG`、`ULONG` です。

```sql
-- 追加列のある Tag
CREATE TAG TABLE sensors (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    location VARCHAR(50),
    status SHORT
);

-- 追加列を含めて入力
INSERT INTO sensors VALUES (
    'TEMP_001',
    '2024-01-01 10:00:00',
    25.5,
    'Building A',
    1
);
```

## 推奨事項 {#best-practices}

1. **必要なメタデータを事前登録**：タグ名は自動登録されますが、明示的な値が必要なメタデータは先に登録します。`_LAST_UPDATE_TIME` はサーバー管理なので入力しません。
2. **バッチ操作を使用**：大量データには CSV またはバッチ API を使用します。
3. **エラーを処理**：戻り値を確認し、エラーを記録します。
4. **時刻精度を統一**：データ全体でタイムスタンプ精度をそろえます。
5. **データを検証**：タグ名と日時が規約に合うことを確認します。

## 性能向上のヒント {#performance-tips}

- **CSV インポート**：数百万行の一括入力に適します。
- **バッチ入力**：複数の入力をまとめます。Machbase は各文を自動コミットするため、SQL トランザクションでまとめることはできません。
- **並列読み込み**：複数の `csvimport` プロセスを使用します。
- **プリペアードステートメント**：SDK ではパラメーター化したクエリーを使用します。

## 次のステップ {#next-steps}

- [Tag データの検索](../querying-data)
- [Tag インデックス](../tag-indexes)による最適化
- [ロールアップテーブル](../rollup-tables)による時系列集計
