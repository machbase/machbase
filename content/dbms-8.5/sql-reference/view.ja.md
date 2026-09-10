---
title : 'VIEW'
type: docs
weight: 25
toc: true
---

## 目次 {#index}

* [保存されたビューとは](#what-is-a-stored-view)
* [Machbase でビューを使う理由](#why-use-view-in-machbase)
* [基本構文](#basic-syntax)
* [基本例](#basic-examples)
* [列名の決定方法](#how-column-names-are-determined)
* [対応する構成](#supported-view-shapes)
* [Machbase 固有の例](#machbase-specific-examples)
* [メタデータと運用確認](#metadata-and-operational-checks)
* [性能と制限](#performance-and-limits)
* [よくある失敗](#common-failure-cases)

## 保存されたビューとは {#what-is-a-stored-view}

本ページは、`CREATE VIEW` で定義する保存されたビューを説明します。
`FROM (SELECT ...)` と書くインラインビューとは区別します。

`SELECT` の定義を名前付きの論理オブジェクトとして保存し、再利用します。

* データ自体は別に保存しません。
* 検索時に定義 SQL を内部で展開して実行します。
* テーブルと同様に `SELECT` の対象にできますが、物理的な保存機能ではありません。
* 本ページの対象は `CREATE VIEW`、`DROP VIEW`、`SELECT`、
  `DESC`、`SHOW VIEWS`、`M$SYS_VIEWS`、`EXPLAIN` です。

ビューは、データのコピーではなく、
再利用できる名前付きクエリーとして理解してください。

## Machbase でビューを使う理由 {#why-use-view-in-machbase}

次の場合に特に役立ちます。

* 同じクエリーを簡単な名前で再利用する
* 複雑な `JOIN`、`GROUP BY`、`CASE`、`UNION ALL` を共有する
* Tag テーブルの `BINARY` を `extract_*()` でデコードし、論理列として公開する
* `SHOW VIEWS`、`DESC`、`M$SYS_VIEWS`、`EXPLAIN` で、
  メタデータと実行計画を確認する

ビューでも、基底テーブルの特性は重要です。

* Lookup/Volatile では、主キーに基づく効率的な条件が重要です。
* Tag では `name`、`time`、`EXPLAIN` を引き続き確認してください。
* 元のクエリーとオプティマイザー経路を使用するため、性能も元クエリーに従います。

## 基本構文 {#basic-syntax}

### ビューの作成 {#create-a-view}

```sql
CREATE VIEW view_name AS
SELECT ...
FROM ...;
```

```sql
CREATE VIEW view_name (col1, col2, ...) AS
SELECT ...
FROM ...;
```

```sql
CREATE OR REPLACE VIEW view_name AS
SELECT ...
FROM ...;
```

* `view_name` は `db.user.view_name` のように修飾できます。
* `CREATE OR REPLACE VIEW` は既存の定義を置換します。
* 同名のオブジェクトがビューでなければ、置換は失敗します。
* 検証対象の実装では、置換後もオブジェクト `ID` を維持します。
* 新しい定義の検証が失敗した場合、元の定義を維持します。

### ビューの削除 {#drop-a-view}

```sql
DROP VIEW view_name;
DROP VIEW IF EXISTS view_name;
```

* `DROP VIEW IF EXISTS` は、対象がなくても成功します。
* 他のビューから依存されている場合、`DROP VIEW` は拒否されます。
* `DROP TABLE view_name` では削除できません。

### メタデータの検索 {#metadata-queries}

```sql
SHOW VIEWS;
DESC view_name;

SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS;
```

## 基本例 {#basic-examples}

Lookup を基にした単純なビューの例です。

```sql
CREATE LOOKUP TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(20),
    city VARCHAR(20),
    amount INTEGER
);

CREATE VIEW v_customer AS
SELECT id, name, city, amount
FROM customer;

SELECT name, city
FROM v_customer
WHERE id = 100;
```

公開する列名を明示することもできます。

```sql
CREATE VIEW v_customer_short (cust_id, cust_name) AS
SELECT id, name
FROM customer;

SELECT cust_id, cust_name
FROM v_customer_short
WHERE cust_id = 100;
```

既存の定義を変更するには `CREATE OR REPLACE VIEW` を使用します。

```sql
CREATE VIEW v_customer_amount AS
SELECT id, amount
FROM customer;

CREATE OR REPLACE VIEW v_customer_amount AS
SELECT id, amount * 10 AS amount
FROM customer
WHERE id <= 10;
```

## 列名の決定方法 {#how-column-names-are-determined}

### 列リストを明示した場合 {#when-an-explicit-column-list-is-given}

```sql
CREATE VIEW v_sales (sales_id, sales_name) AS
SELECT id, name
FROM t_sales;
```

この例では `sales_id` と `sales_name` が正式な列名になります。

### 列リストを省略した場合 {#when-no-explicit-column-list-is-given}

次の優先順位で決まります。

1. `SELECT` の別名
2. 単純な列参照の場合は元の列名
3. `EXPR1`、`EXPR2` などの自動生成名

```sql
CREATE VIEW v_expr AS
SELECT id,
       name AS user_name,
       val + 10
FROM t1;
```

この結果は `ID`、`USER_NAME`、`EXPR3` になります。

### `UNION ALL` ビューの列名 {#column-names-in-union-all-views}

最も左の `SELECT` の名前を使用します。

```sql
CREATE VIEW v_union AS
SELECT id FROM t1
UNION ALL
SELECT id FROM t2;
```

`DESC v_union` では `ID` と表示され、`SELECT id FROM v_union` を実行できます。

## 対応するビューの構成 {#supported-view-shapes}

検証対象の構成には、次があります。

* 単純な射影と条件
* 式、関数、定数、`CASE`
* `JOIN`
* サブクエリーを含むビュー
* 入れ子のビュー
* `GROUP BY`, `HAVING`
* `DISTINCT`
* `UNION ALL`

例：

```sql
CREATE VIEW v_expr_case AS
SELECT id,
       CASE WHEN amount >= 100 THEN 'VIP' ELSE 'NORMAL' END AS grade,
       UPPER(city) AS city_upper
FROM customer;
```

```sql
CREATE VIEW v_city_sum AS
SELECT city, SUM(amount) AS total_amount
FROM customer
GROUP BY city
HAVING SUM(amount) >= 100;
```

```sql
CREATE VIEW v_union AS
SELECT id FROM customer WHERE city = 'SEOUL'
UNION ALL
SELECT id FROM customer WHERE city = 'BUSAN';
```

```sql
CREATE VIEW v_nested AS
SELECT id, total_amount
FROM v_city_sum
JOIN (
    SELECT city AS city_name, COUNT(*) AS city_cnt
    FROM customer
    GROUP BY city
) x
ON v_city_sum.city = x.city_name;
```

## Machbase 固有の例 {#machbase-specific-examples}

### Tag/`BINARY` データのデコード {#decoding-tag--binary-data}

実用的なパターンとして、Tag テーブルの `BINARY` 列からデコードした値を
論理列として公開できます。

```sql
CREATE TAG TABLE dam (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    frame BINARY(16)
);

CREATE VIEW damdata AS
SELECT name,
       time,
       extract_bit(frame, 0) AS bit0,
       extract_ulong(frame, 0, 16) AS u16,
       extract_long(frame, 0, 16) AS s16,
       extract_float(frame, 0) AS f32,
       extract_scaled_double(frame, 0, 12, 0, 0.5, 0.5) AS sd12
FROM dam;
```

```sql
SELECT name, time, bit0, u16, s16, f32, sd12
FROM damdata
WHERE name = 'main'
  AND time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND time <  TO_DATE('2024-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time;
```

この場合も、基底の Tag テーブルと同様に `name`、`time`、`EXPLAIN` を
確認してください。

### 修飾名と引用識別子 {#schema-qualified-and-quoted-names}

スキーマ修飾名や引用符付き識別子を使用できます。

```sql
CREATE VIEW machbasedb.sys.v_local AS
SELECT id, val
FROM other_user.v_src
WHERE id >= 2;

CREATE VIEW "V_QUOTED" AS
SELECT id, val
FROM t1;

CREATE VIEW v_dep AS
SELECT id
FROM "V_QUOTED"
WHERE val >= 20;
```

* 異なるスキーマの同名ビューは、修飾名で区別します。
* 引用名のビューに依存がある場合も、`DROP VIEW` は拒否されます。

## メタデータと運用確認 {#metadata-and-operational-checks}

### `SHOW VIEWS` {#show-views}

`SHOW VIEWS` は、参照可能なビューと定義 SQL を一覧表示します。

出力列：

* `USER_NAME`
* `DB_NAME`
* `VIEW_NAME`
* `VIEW_SQL`

```sql
SHOW VIEWS;
```

### `M$SYS_VIEWS` {#msys_views}

`M$SYS_VIEWS` は、定義 SQL を確認する公開メタデータインターフェースです。

```sql
SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS
WHERE VIEW_NAME = 'V_CUSTOMER';
```

主な用途：

* ビューの一覧
* 特定のビューの定義確認
* `CREATE OR REPLACE VIEW` 後の定義確認

### `DESC`, `M$SYS_TABLES`, `M$SYS_COLUMNS` {#desc-msys_tables-msys_columns}

```sql
DESC v_customer;

SELECT ID, NAME, TYPE
FROM M$SYS_TABLES
WHERE TYPE = 7;

SELECT TABLE_ID, ID, NAME, TYPE, LENGTH
FROM M$SYS_COLUMNS
WHERE TABLE_ID = (
    SELECT ID
    FROM M$SYS_TABLES
    WHERE TYPE = 7
      AND NAME = 'V_CUSTOMER'
);
```

* `DESC` は公開する列名と型を表示します。
* `M$SYS_TABLES` はビューを `TYPE = 7` として表示します。
* `M$SYS_COLUMNS` は公開する列を表示します。
* 置換後も `M$SYS_TABLES.ID` は維持され、
  `M$SYS_VIEWS.VIEW_SQL` が更新されます。

### `EXPLAIN` {#explain}

ビューは物理データを持たないため、性能は元のクエリーと最適化経路に依存します。
本番では、まず `EXPLAIN` を確認してください。

```sql
EXPLAIN
SELECT *
FROM v_customer
WHERE id = 3;
```

## 性能と制限 {#performance-and-limits}

### インデックス利用と条件のプッシュダウン {#index-usage-and-predicate-pushdown}

次の構成では、基底テーブルのインデックスを利用しやすくなります。

* 基底列を直接公開する単純な射影
* 列名だけを変更するビュー
* 外側の条件を基底列へ直接対応付けられる単純なフィルター

次は全表スキャンになる場合があるため、`EXPLAIN` が重要です。

* `DISTINCT` ビューへの外側の条件
* `id + 1 AS id2` のような式で生成した列への条件

### 単純な保存ビューの最適化 {#simple-stored-view-optimizations}

検証対象の実装では、次の最適化を利用できる場合があります。

* 使用しない射影対象の除外
* 外側の条件を押し下げられる場合の `COUNT(*)` の高速経路

一方、`SELECT *`、`DISTINCT`、`GROUP BY`、`HAVING`、集合演算、ウィンドウ、
複雑な結合では、すべての射影を処理する経路を使用する場合があります。

### 定義 SQL の長さ制限 {#view-definition-sql-length-limit}

`AS` の後の定義 SQL は、現在の実装で最大 `256KB` です。

超過すると、次の種類のエラーになります。

```text
ERR-02010: Syntax error: near token (VIEW_SQL_TOO_LONG).
```

### 削除と依存関係 {#drop-and-dependency-rules}

* 依存するビューがあると `DROP VIEW` は拒否されます。
* 実際に参照するオブジェクトを基に依存を解決します。
* 文字列リテラルや別名に現れるだけの名前は依存と見なしません。

## よくある失敗 {#common-failure-cases}

### 列数の不一致 {#column-count-mismatch}

```sql
CREATE VIEW v_bad (c1, c2, c3) AS
SELECT id, val
FROM t1;
```

### 自己再帰ビュー {#direct-recursive-view}

```sql
CREATE VIEW v_recursive AS
SELECT id
FROM v_recursive;
```

### 列名の重複と `_RID` {#duplicate-column-names-and-_rid}

```sql
CREATE VIEW v_dup AS
SELECT id AS c1, val AS c1
FROM t1;

CREATE VIEW v_rid (_RID) AS
SELECT id
FROM t1;
```

### `CREATE OR REPLACE VIEW` でビュー以外を置換 {#replacing-a-non-view-object-with-create-or-replace-view}

```sql
CREATE OR REPLACE VIEW t1 AS
SELECT id
FROM src_t1;
```

### 予約名と無効なパス {#reserved-names-or-invalid-paths}

```sql
CREATE VIEW v$bad AS
SELECT id
FROM t1;

CREATE VIEW _tag_bad AS
SELECT id
FROM t1;

CREATE VIEW no_such_db.sys.v_bad AS
SELECT id
FROM t1;
```

### `DROP TABLE` でビューを削除 {#dropping-a-view-with-drop-table}

```sql
DROP TABLE v_customer;
```

この場合、ビューは削除されず、エラーを返します。

## 関連ドキュメント {#related-documents}

* [DDL](../ddl)
* [SELECT](../select)
