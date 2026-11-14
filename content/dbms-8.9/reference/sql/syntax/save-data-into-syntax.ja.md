---
type: docs
title: 'SAVE DATA INTO'
weight: 100
toc: true
---

`SAVE DATA INTO`は`SELECT`クエリの結果をCSVファイルに保存する構文です。

## 構文

```sql
SAVE DATA INTO 'file_path'
    [HEADER { ON | OFF }]
    [{ FIELDS | COLUMNS }
        [TERMINATED BY 'char']
        [ENCLOSED BY 'char']
    ]
    [ENCODED BY coding_name]
    AS select_query
```

## オプション

| オプション | デフォルト値 | 説明 |
|------|--------|------|
| `HEADER { ON \| OFF }` | OFF | 先頭行に列名を出力するかどうか |
| `TERMINATED BY 'char'` | `,` | フィールド区切り文字 |
| `ENCLOSED BY 'char'` | `"` | フィールドの引用文字 |
| `ENCODED BY coding_name` | UTF8 | 出力ファイルのエンコーディング |

対応するエンコーディング: `UTF8`, `MS949`, `KSC5601`, `EUCJP`, `SHIFTJIS`, `BIG5`, `GB231280`

## 例

```sql
-- 基本的なCSV保存
SAVE DATA INTO '/tmp/result.csv' AS SELECT * FROM sensor_log;

-- ヘッダーを含め、セミコロンで区切る
SAVE DATA INTO '/tmp/output.csv'
    HEADER ON
    FIELDS TERMINATED BY ';'
    AS SELECT name, time, value FROM sensor_log WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- 区切り文字と引用文字を指定
SAVE DATA INTO '/tmp/export.csv'
    HEADER ON
    FIELDS TERMINATED BY ';' ENCLOSED BY '\''
    ENCODED BY MS949
    AS SELECT * FROM t1 WHERE i1 > 100;

-- TAGテーブルのデータをエクスポート
SAVE DATA INTO '/tmp/tag_export.csv'
    HEADER ON
    AS SELECT name, time, value
         FROM sensor_tag
        WHERE name = 'TEMP-01'
          AND time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
                       AND TO_DATE('2024-01-02', 'YYYY-MM-DD')
        ORDER BY time;
```

## 注意事項

- ファイルパスはMachbaseサーバープロセスが書き込める場所を指定してください。
- 出力先にファイルが存在するとエラーになり、既存ファイルは変更しません。別のファイル名を指定するか、既存ファイルを移動してから再実行してください。
- SELECT結果がない場合、空のファイルやヘッダーのみのファイルが生成される場合があります。
- ファイルパスへのアクセス権がなければエラーを返します。

## 関連ドキュメント

- [LOAD DATA INFILE syntax](../load-data-infile-syntax/) — ファイルからテーブルへのデータ取り込み
