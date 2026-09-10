---
type: docs
title: 'SQL リファレンス'
weight: 80
toc: true
---

Machbase の SQL 構文を説明します。SQL コマンド、データ型、関数、演算子を参照できます。

## SQL コマンドの分類 {#sql-command-categories}

### データ定義言語（DDL） {#data-definition-language-ddl}

- `CREATE TABLE`：Log テーブルの作成
- `CREATE TAG TABLE`：Tag テーブルの作成
- `CREATE VOLATILE TABLE`：Volatile テーブルの作成
- `CREATE LOOKUP TABLE`：Lookup テーブルの作成
- `CREATE VIEW`：ビューの作成
- `ALTER TABLE`：テーブル構造の変更
- `DROP TABLE`：テーブルの削除
- `DROP VIEW`：ビューの削除
- `CREATE INDEX`：インデックスの作成
- `DROP INDEX`：インデックスの削除

### データ操作言語（DML） {#data-manipulation-language-dml}

- `INSERT`：データの挿入
- `SELECT`：データの検索
- `UPDATE`：データの更新（Volatile/Lookup）
- `DELETE`：データの削除
- `DURATION`：時刻による検索条件

### データ制御言語（DCL） {#data-control-language-dcl}

- `CREATE USER`：ユーザーの作成
- `ALTER USER`：ユーザーの変更
- `DROP USER`：ユーザーの削除
- `GRANT`：権限の付与
- `REVOKE`：権限の取り消し

### システムコマンド {#system-commands}

- `SHOW TABLES`：テーブル一覧
- `SHOW TABLE`：テーブル構造
- `SHOW VIEWS`：ビュー一覧
- `SHOW USERS`：ユーザー一覧
- `SHOW INDEXES`：インデックス一覧
- `SHOW STORAGE`：ストレージ情報
- `SHOW LICENSE`：ライセンス情報

## データ型 {#data-types}

### 数値型 {#numeric-types}
- `SHORT`, `INTEGER`, `LONG`
- `FLOAT`, `DOUBLE`

### 文字列型 {#string-types}
- `CHAR(n)`, `VARCHAR(n)`

### 日時型 {#datetime-types}
- `DATE`, `DATETIME`

### バイナリー型 {#binary-types}
- `BINARY(n)`

### ネットワーク型 {#network-types}
- `IPV4`, `IPV6`

## 関数 {#functions}

### 時刻関数 {#time-functions}
- `NOW`, `SYSDATE`
- `TO_DATE()`, `TO_TIMESTAMP()`
- `TO_CHAR()`
- `INTERVAL`

### 集計関数 {#aggregate-functions}
- `COUNT()`, `SUM()`, `AVG()`
- `MIN()`, `MAX()`
- `STDDEV()`, `VARIANCE()`

### 文字列関数 {#string-functions}
- `UPPER()`, `LOWER()`
- `LENGTH()`, `SUBSTR()`
- `SEARCH` キーワード

### 数学関数 {#mathematical-functions}
- `ABS()`, `CEIL()`, `FLOOR()`
- `ROUND()`, `TRUNC()`
- `POWER()`, `SQRT()`
- [関数](./functions/)

## Machbase 固有の機能 {#machbase-specific-features}

### `DURATION` 句 {#duration-clause}

```sql
SELECT * FROM table DURATION n MINUTE|HOUR|DAY [BEFORE n MINUTE|HOUR|DAY];
```

### `SEARCH` キーワード {#search-keyword}

```sql
SELECT * FROM table WHERE column SEARCH 'keyword';
```

### ロールアップクエリー {#rollup-queries}

```sql
-- WITH ROLLUP で作成した TAG で実行
SELECT ROLLUP('hour', 1, time) AS rtime, AVG(value)
FROM tag_table
WHERE name = 'sensor-1'
GROUP BY rtime;
```

### 時刻に基づく削除 {#time-based-deletion}

```sql
DELETE FROM table OLDEST n ROWS;
DELETE FROM table EXCEPT n ROWS|DAY;
DELETE FROM table BEFORE datetime;
```

## 詳細なリファレンス {#complete-reference}

構文の詳細は、次を参照してください。
- [DDL](./ddl/)、[DML](./dml/)、[SELECT](./select/)、[関数](./functions/)

## クイックリファレンスの例 {#quick-reference-examples}

### テーブルの作成 {#create-tables}

```sql
-- 組み込みロールアップ付き Tag
CREATE TAG TABLE sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP;

-- Log テーブル
CREATE TABLE logs (
    level VARCHAR(10),
    message VARCHAR(2000)
);

-- Volatile テーブル
CREATE VOLATILE TABLE cache (
    key VARCHAR(100) PRIMARY KEY,
    value VARCHAR(500)
);

-- Lookup テーブル
CREATE LOOKUP TABLE devices (
    device_id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

-- VIEW
CREATE VIEW active_devices AS
SELECT device_id, name
FROM devices;
```

### データの検索 {#query-data}

```sql
-- 最近のデータ
SELECT * FROM sensors
WHERE time BETWEEN now - 1h AND now;

-- 条件付き
SELECT * FROM logs WHERE level = 'ERROR' DURATION 1 DAY;

-- 集計
SELECT sensor_id, AVG(value) FROM sensors
WHERE time BETWEEN now - 1d AND now
GROUP BY sensor_id;

-- ロールアップ検索
SELECT ROLLUP('hour', 1, time) AS rtime, AVG(value)
FROM sensors
WHERE sensor_id = 'sensor-1'
  AND time BETWEEN now - 7d AND now
GROUP BY rtime;
```

### ユーザーの管理 {#manage-users}

```sql
-- ユーザーを作成
CREATE USER analyst IDENTIFIED BY 'password';

-- 権限を付与
GRANT SELECT ON sensors TO analyst;

-- パスワードを変更
ALTER USER analyst IDENTIFIED BY 'newpassword';
```

## 学習の順序 {#learning-path}

1. **基礎**：基本の DDL/DML
2. **学習**：Machbase 固有の `DURATION`、`SEARCH`
3. **習得**：高度なクエリーと関数
4. **参照**：本セクションで構文を確認

## 関連ドキュメント {#related-documentation}

- [VIEW](./view)：ビューの作成、検索、メタデータ、性能、制限
- [基本概念](../core-concepts/)：Machbase の理解
- [SELECT](./select/)：クエリーの例
- [テーブルの種類](../table-types/)：実践
