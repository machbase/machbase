---
type: docs
title: 'LOAD DATA INFILE'
weight: 130
toc: true
---

`LOAD DATA INFILE`は、CSV形式のデータファイルをサーバーが直接読み取り、テーブルへ入力する構文です。

> 大量データの取り込みには`machloader`ユーティリティを推奨します。
> `machloader`は並列処理と多様なオプションを提供し、より高速に取り込めます。

## 構文

```sql
LOAD DATA INFILE 'file_path' INTO TABLE table_name
    [TABLESPACE tablespace_name]
    [AUTO { BULKLOAD | HEADUSE | HEADUSE_ESCAPE }]
    [{ FIELDS | COLUMNS } [TERMINATED BY 'char'] [ENCLOSED BY 'char']]
    [LINES TERMINATED BY 'char']
    [TRIM { ON | OFF }]
    [IGNORE number LINES]
    [MAX_LINE_LENGTH number]
    [ENCODED BY coding_name]
    [ON ERROR { STOP | IGNORE }]
```

## オプション

| オプション | 説明 |
|------|------|
| `AUTO BULKLOAD` | 行全体を1つの列に入力 |
| `AUTO HEADUSE` | 最初の行の列名でテーブルを自動作成して入力 |
| `AUTO HEADUSE_ESCAPE` | `HEADUSE`と同じ。ただし予約語・特殊文字を`_`に置換 |
| `TERMINATED BY 'char'` | フィールド区切り文字（デフォルト: `,`） |
| `ENCLOSED BY 'char'` | フィールド引用符（デフォルト: `"`） |
| `LINES TERMINATED BY 'char'` | レコード区切り文字 |
| `TRIM { ON \| OFF }` | 列の前後の空白を除去するか（デフォルト: ON） |
| `IGNORE number LINES` | 最初のN行を無視（ヘッダーのスキップなど） |
| `MAX_LINE_LENGTH number` | 1行の最大長（デフォルト: 512KB） |
| `ENCODED BY coding_name` | ファイルのエンコーディング（デフォルト: UTF8） |
| `ON ERROR STOP\|IGNORE` | エラー時に停止または無視（デフォルト: STOP） |

サポートするエンコーディング: `UTF8`、`MS949`、`KSC5601`、`EUCJP`、`SHIFTJIS`、`BIG5`、`GB231280`

## 例

```sql
-- 基本のCSVファイル入力（区切り: ,  引用符: "）
LOAD DATA INFILE '/tmp/sensor_data.csv' INTO TABLE sensor_log;

-- ヘッダー1行を無視し、;区切りのファイルを入力
LOAD DATA INFILE '/tmp/data.csv' INTO TABLE sample_data
    FIELDS TERMINATED BY ';' ENCLOSED BY '\''
    IGNORE 1 LINES
    ON ERROR IGNORE;

-- AUTO BULKLOAD: 各行を単一列に入力（テーブルを自動作成）
LOAD DATA INFILE '/tmp/raw.txt' INTO TABLE raw_table AUTO BULKLOAD;

-- AUTO HEADUSE: 最初の行を列名としてテーブルを自動作成し、入力
LOAD DATA INFILE '/tmp/data_with_header.csv' INTO TABLE auto_table AUTO HEADUSE;

-- エンコーディングの指定
LOAD DATA INFILE '/tmp/korean_data.csv' INTO TABLE Korean_table ENCODED BY MS949;
```

## 注意事項

- `AUTO`オプションを使用しない場合、対象テーブルのすべての列は`VARCHAR`または`TEXT`型である必要があります。
- ファイルパスは、Machbaseサーバープロセスがアクセスできるパスである必要があります。
- 取り込み中にエラーが発生しても、入力済みの行はロールバックされません。
- 大容量ファイルでは、`machloader`の使用が性能面で有利です。

## machloaderとの比較

| 項目 | LOAD DATA INFILE | machloader |
|------|-----------------|------------|
| 並列処理 | 未サポート | サポート |
| 使用方法 | SQL文 | CLIユーティリティ |
| 用途 | 少量データ、スクリプト内での使用 | 大量の一括取り込み |

## 関連文書

- [SAVE DATA INTO構文](../save-data-into-syntax/) — SELECT結果をファイルに保存
