---
type: docs
title: 'VIEW'
weight: 140
toc: true
---

VIEWは`SELECT`を名前付き論理オブジェクトとして保存し、再利用する機能です。データは別途保存せず、参照時に保存された定義SQLを内部で再展開して実行します。

## CREATE VIEW

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

Standard Editionでは、VIEW定義の`SELECT`の前に非再帰CTEを宣言できます。

```sql
CREATE VIEW view_name AS
WITH cte_name AS (
    SELECT ...
    FROM ...
)
SELECT ...
FROM cte_name;
```

- `CREATE OR REPLACE VIEW`は既存のVIEW定義を置き換えます。対象がVIEW以外のオブジェクトならエラーを返します。
- 列リストを明示すると、その名前がVIEWの正式な列名になります。省略すると別名または元の列名を使用します。
- `view_name`には`db.user.view_name`形式のスキーマ修飾名も使用できます。

### 基本例

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

### 列名を明示

```sql
CREATE VIEW v_customer_short (cust_id, cust_name) AS
SELECT id, name
FROM customer;
```

### 既存VIEW定義の置き換え

```sql
CREATE OR REPLACE VIEW v_customer_amount AS
SELECT id, amount * 10 AS amount
FROM customer
WHERE id <= 10;
```

### CTEを含むVIEW

```sql
CREATE VIEW v_customer_city_summary AS
WITH city_summary AS (
    SELECT city, COUNT(*) AS customer_count, SUM(amount) AS total_amount
    FROM customer
    GROUP BY city
)
SELECT city, customer_count, total_amount
FROM city_summary;
```

VIEW定義にバインドパラメーター（`?`）は使用できません。実行ごとに変わる条件はVIEWを参照する`SELECT`に記述します。

<a id="view-user-context"></a>

## VIEWのユーザーコンテキスト

Machbase 8.7.0以降では、VIEW内の`CURRENT_*`と`SESSION_*`関数で定義者と呼び出し元を区別できます。
次の例では`VIEW_OWNER`がVIEWを作成し、`VIEW_CALLER`が付与された権限で参照します。

```sql
CONNECT sys/manager;
CREATE USER view_owner IDENTIFIED BY 'VIEW_OWNER';
CREATE USER view_caller IDENTIFIED BY 'VIEW_CALLER';

CONNECT view_owner/VIEW_OWNER;
CREATE LOOKUP TABLE user_context_source (id INTEGER PRIMARY KEY);
INSERT INTO user_context_source VALUES (1);

CREATE VIEW v_user_context AS
SELECT CURRENT_USER() AS current_name,
       SESSION_USER() AS session_name,
       CURRENT_USER_ID() AS current_id,
       SESSION_USER_ID() AS session_id
  FROM user_context_source;

CONNECT sys/manager;
GRANT SELECT ON view_owner.v_user_context TO view_caller;

CONNECT view_caller/VIEW_CALLER;
SELECT current_name,
       session_name,
       CASE WHEN current_id <> session_id THEN 'DIFF' ELSE 'SAME' END AS id_context
  FROM view_owner.v_user_context;
```

```text
CURRENT_NAME  SESSION_NAME  ID_CONTEXT
VIEW_OWNER    VIEW_CALLER   DIFF
```

VIEW内の`CURRENT_*`はVIEW所有者を、`SESSION_*`は接続した呼び出し元を返します。通常のSQLでは
両方が同じユーザーを返します。関数の仕様は[ユーザーコンテキスト関数](../../functions/functions-full/#current-session-user)を参照してください。

```sql
CONNECT view_owner/VIEW_OWNER;
DROP VIEW v_user_context;
DROP TABLE user_context_source;

CONNECT sys/manager;
DROP USER view_caller;
DROP USER view_owner;
```

## DROP VIEW

```sql
DROP VIEW view_name;
DROP VIEW IF EXISTS view_name;
```

- `DROP VIEW IF EXISTS`は対象がなくてもエラーなしで成功します。
- 別のVIEWが対象VIEWを参照している場合は削除を拒否します。
- `DROP TABLE view_name`ではVIEWを削除できません。

## メタデータの確認

```sql
SHOW VIEWS;
DESC view_name;

SELECT USER_NAME, DB_NAME, VIEW_NAME, VIEW_SQL
FROM M$SYS_VIEWS
WHERE VIEW_NAME = 'V_CUSTOMER';
```

- `M$SYS_TABLES`ではVIEWは`TYPE = 7`で確認できます。

## 対応するVIEWの形式

| 形式 | サポート |
|------|-----------|
| 単純な射影と述語 | O |
| 式、関数、定数、CASE | O |
| JOIN | O |
| サブクエリを含む | O |
| 入れ子のVIEW | O |
| GROUP BY, HAVING | O |
| DISTINCT | O |
| UNION ALL | O |

## Tag / BINARY列の使用例

TAGテーブルの`BINARY`列を`extract_*()`関数で解析し、論理列として公開するパターンです。

```sql
CREATE TAG TABLE dam (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    frame BINARY(16)
);

CREATE VIEW damdata AS
SELECT name,
       time,
       extract_bit(frame, 0)                         AS bit0,
       extract_ulong(frame, 0, 16)                   AS u16,
       extract_float(frame, 0)                       AS f32,
       extract_scaled_double(frame, 0, 12, 0, 0.5, 0.5) AS sd12
FROM dam;

SELECT name, time, bit0, u16, f32, sd12
FROM damdata
WHERE name = 'main'
  AND time >= TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND time <  TO_DATE('2024-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time;
```

## 制約

- VIEW定義SQL（`SELECT`本文）は最大256KBをサポートします。
- VIEWはデータを別途保存しないため、性能は元のクエリとオプティマイザーの判断に依存します。
- `DISTINCT`や計算列に対する述語はフルスキャンになる場合があるため、`EXPLAIN`で確認してください。
- 再帰VIEW（自分自身を参照するVIEW）はサポートしません。

## 関連ドキュメント

- [SELECT syntax](../select-syntax/) — FROM句でVIEWを使用
- [WITH / CTE syntax](../cte-syntax/) — CTEを含むVIEW定義
