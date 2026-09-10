---
type: docs
title: 'WITH / CTE'
weight: 20
toc: true
---

共通テーブル式（Common Table Expression、CTE）は、1つのSQL文内で`SELECT`結果に名前を付けて
使用する機能です。複雑なインラインビューの段階分けや、集計結果と他のテーブルとの結合に使用します。

Machbase 8.7.0 Standard Editionは非再帰SELECT CTEをサポートします。CTEは現在のSQL文内だけで有効であり、
独立したデータベースオブジェクトとしては保存されません。

## サポート範囲

| 機能 | サポート | 説明 |
|---|:---:|---|
| 単一の非再帰CTE | O | CTE本文と主クエリは`SELECT`です。 |
| 複数のCTE | O | カンマで区切り、後のCTEから前のCTEを参照できます。 |
| 明示的な結果列名 | O | CTE名の後に結果列リストを指定します。 |
| 入れ子のCTE | O | 外側のCTEは下位の`SELECT`から参照できます。 |
| `INSERT SELECT` | O | `INSERT INTO ... WITH ... SELECT`の順で記述します。 |
| VIEW定義 | O | `CREATE VIEW ... AS WITH ... SELECT`を使用します。 |
| プリペアドステートメント | O | CTE本文と主`SELECT`で`?`または`:name`を使用できます。 |
| EXPLAIN | O | `EXPLAIN`、`EXPLAIN FULL`、`EXPLAIN TRACE`に対応します。 |
| `UNION ALL`、PIVOT | O | 既存の`SELECT`のサポート範囲と制約に従います。 |
| テーブルタイプ | O | LOG、TAG、LOOKUP、VOLATILE、TRANSACTIONを参照できます。 |
| 再帰CTE | X | `WITH RECURSIVE`、自己参照、相互再帰は非対応です。 |
| 実体化の制御 | X | `MATERIALIZED`、`NOT MATERIALIZED`は非対応です。 |
| データ変更CTE | X | CTE本文にDMLやDDLは使用できません。 |

CTE本文ではJOIN、集約関数、`GROUP BY`、`HAVING`、`ORDER BY`、`LIMIT`、`UNION ALL`、PIVOTを
既存の`SELECT`規則に従って使用できます。LOGテーブルの`DURATION`、`SERIES BY`、ウィンドウ関数、
TAGテーブルのROLLUPも既存の規則に従います。

名前付きパラメーターの命名規則とSDK別のバインド方法は、[Named Bind Parameter構文](../named-bind-parameter-syntax/)を参照してください。

## 基本構文

### SELECT

```sql
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

### INSERT SELECT

```sql
INSERT INTO target_table [(target_column [, ...])]
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

`INSERT SELECT`では、対象テーブルと対象列リストの後に`WITH`句を記述します。
他のDBMSの文頭に置く`WITH ... INSERT INTO ...`形式はサポートしません。

### VIEW

```sql
CREATE [OR REPLACE] VIEW view_name AS
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

### EXPLAIN

```sql
EXPLAIN [FULL | TRACE]
WITH cte_name [(column_name [, ...])] AS (
    select_statement
)
[, cte_name [(column_name [, ...])] AS (select_statement) ...]
select_statement;
```

## 基本的な使用方法

次の例は、現在のユーザーが以下のテーブルを所有することを前提とします。

| テーブル | タイプ | 使用列 |
|---|---|---|
| `sensor_data` | LOG | `name`, `device_id`, `time`, `value` |
| `device_info` | TRANSACTION | `device_id`, `device_name` |
| `device_summary` | LOG | `device_id`, `sample_count`, `avg_value` |

### クエリ結果に名前を付ける

```sql
WITH recent_data AS (
    SELECT name, time, value
    FROM sensor_data
    WHERE time >= NOW - 10m
)
SELECT name, time, value
FROM recent_data
ORDER BY time DESC;
```

最終出力の順序を保証するには、主`SELECT`に`ORDER BY`を指定します。CTE本文の`ORDER BY`だけでは
外側の結果順序は保証されません。

### 集計結果の結合

```sql
WITH top_devices AS (
    SELECT device_id,
           AVG(value) AS avg_value
    FROM sensor_data
    WHERE time >= NOW - 1h
    GROUP BY device_id
    ORDER BY avg_value DESC
    LIMIT 10
)
SELECT d.device_id,
       d.device_name,
       t.avg_value
FROM device_info d
JOIN top_devices t
  ON d.device_id = t.device_id
ORDER BY t.avg_value DESC;
```

大量の時系列データを先に集計し、結果件数を制限してから参照データと結合する場合に使用できます。

### 複数のCTEの連結

```sql
WITH recent_data AS (
    SELECT device_id, value
    FROM sensor_data
    WHERE time >= NOW - 30m
),
device_avg AS (
    SELECT device_id, AVG(value) AS avg_value
    FROM recent_data
    GROUP BY device_id
)
SELECT device_id, avg_value
FROM device_avg
WHERE avg_value >= 80;
```

`device_avg`は先に宣言した`recent_data`を参照できます。前のCTEから後のCTEを参照する前方参照は非対応です。

### 結果列名の指定

```sql
WITH device_stat (id, sample_count, average_value) AS (
    SELECT device_id, COUNT(*), AVG(value)
    FROM sensor_data
    GROUP BY device_id
)
SELECT id, sample_count, average_value
FROM device_stat;
```

明示した列数はCTE本文の結果列数と一致する必要があり、列名の重複は許可しません。
列リストを省略すると、`SELECT`の別名とインラインビューの列命名規則に従います。

## 使用できるSQLの文脈

### 下位SELECT

```sql
WITH active_devices AS (
    SELECT device_id
    FROM sensor_data
    WHERE time >= NOW - 1m
)
SELECT d.device_id, d.device_name
FROM device_info d
WHERE d.device_id IN (
    SELECT device_id
    FROM active_devices
);
```

外側の`SELECT`で宣言したCTEは、スカラーサブクエリ、`IN (subquery)`、インラインビューなどの
下位`SELECT`から参照できます。JOIN `ON`条件のスカラーサブクエリや`IN (subquery)`など、
既存の`SELECT`の制約はCTEを使用しても変わりません。

### INSERT SELECT

```sql
INSERT INTO device_summary
WITH hourly_summary AS (
    SELECT device_id,
           COUNT(*) AS sample_count,
           AVG(value) AS avg_value
    FROM sensor_data
    WHERE time >= NOW - 1h
    GROUP BY device_id
)
SELECT device_id, sample_count, avg_value
FROM hourly_summary;
```

CTEは結果行を生成し、実際の取り込み可否と重複キー処理は対象テーブルの既存の`INSERT SELECT`規則に従います。
CTEを使用しても、対象テーブルの制約や原子性の範囲は変わりません。

### VIEW定義

```sql
CREATE VIEW active_device_summary AS
WITH recent_data AS (
    SELECT device_id, value
    FROM sensor_data
    WHERE time >= NOW - 10m
)
SELECT device_id,
       COUNT(*) AS sample_count,
       AVG(value) AS avg_value
FROM recent_data
GROUP BY device_id;
```

VIEWにはCTEを含む`SELECT`定義が保存され、参照時にその定義を再解釈します。
`CREATE OR REPLACE VIEW`でも同じ構文を使用できます。

VIEW定義にバインドパラメーター（`?`）は使用できません。実行ごとに変わる条件は、VIEWを参照する`SELECT`に記述します。

### EXPLAIN

```sql
EXPLAIN FULL
WITH recent_data AS (
    SELECT name, time, value
    FROM sensor_data
    WHERE time >= NOW - 5m
)
SELECT *
FROM recent_data
WHERE name = 'sensor-01';
```

`EXPLAIN`、`EXPLAIN FULL`、`EXPLAIN TRACE`で、CTE展開後に実際のテーブルへ適用されるスキャン、
フィルター、JOIN計画を確認します。

### プリペアドステートメント

CTE本文と主`SELECT`でバインドパラメーター（`?`）を使用できます。

```sql
WITH selected_data AS (
    SELECT device_id, time, value
    FROM sensor_data
    WHERE device_id = ?
)
SELECT device_id, time, value
FROM selected_data
WHERE value >= ?;
```

参照しないCTEのバインドパラメーターも文のパラメーターとして登録されるため、値をバインドしてください。
同じCTEを複数回参照しても、元のCTE本文のパラメーター数が参照回数分に増えることはありません。

## 名前と有効範囲

### 宣言順序

後のCTEは前のCTEを参照できます。前方参照、自己参照、CTE間の相互参照はサポートしません。

### 実テーブルと名前が同じ場合

修飾のない名前がCTEと実際のTABLEまたはVIEWの両方に存在する場合、現在の有効範囲のCTEを優先します。

```sql
WITH device_info AS (
    SELECT device_id
    FROM sensor_data
)
SELECT *
FROM device_info;
```

実テーブルを選択するには、`user_name.device_info`のように所有者を明示します。
所有者で修飾した名前は、CTEではなく実際のTABLEまたはVIEWを検索します。

### 入れ子の範囲

外側のCTEは内側の`SELECT`から参照できます。内側の`SELECT`に宣言したCTEは外側から参照できません。
内側のCTEと外側のCTEが同名の場合は、内側を優先します。

## 実行特性と性能

MachbaseはCTE参照を既存のインラインビュー形式に展開して計画します。CTE結果の一時テーブルへの実体化や、
1回だけの評価は保証しません。

同じCTEへの複数の参照は、それぞれ個別に計画・実行される場合があります。

```sql
WITH recent_data AS (
    SELECT device_id, time, value
    FROM sensor_data
    WHERE time >= NOW - 1d
)
SELECT a.device_id, a.value, b.value
FROM recent_data a
JOIN recent_data b
  ON a.device_id = b.device_id
 AND a.time = b.time;
```

性能管理には次の基準を適用してください。

- 大量のテーブルを読み取るCTEの繰り返し参照を避けます。
- 時刻、TAG名、キー条件など選択性を高める条件を、CTE本文でできるだけ早く適用します。
- フィルターのプッシュダウンやCTE結果の自動再利用を前提に性能を予測しません。
- 繰り返し参照が必要な場合は、クエリの分割や実際に保存するオブジェクトの使用を検討します。
- `EXPLAIN`で各参照の実際の実行計画を確認します。

`MATERIALIZED`と`NOT MATERIALIZED`は非対応のため、ユーザーがCTEの評価方式を強制することはできません。

### CTEの展開上限

1つのSQL文のCTE展開で生成される`SELECT`単位は最大1,024個です。宣言できるCTE名の数ではなく、
複数参照と連鎖参照をすべて展開した`SELECT`単位の合計です。

上限を超えると次のエラーになります。

```text
CTE expansion limit exceeded
```

エラーが発生したら、繰り返し参照の連鎖を減らすか、中間結果を別のテーブルまたはVIEWに分離してください。

## 制約

次の機能はサポートしません。

- `WITH RECURSIVE`と再帰CTE
- `RECURSIVE`を省略した自己参照とCTE間の相互再帰
- 前方参照
- `MATERIALIZED`、`NOT MATERIALIZED`
- 再帰CTE構文の`SEARCH DEPTH FIRST`、`SEARCH BREADTH FIRST`、`CYCLE`
- 文頭の`WITH ... INSERT`、`WITH ... UPDATE`、`WITH ... DELETE`、`WITH ... MERGE`
- CTE本文のINSERT、UPDATE、DELETE、MERGE、DDL
- `UNION`、`INTERSECT`、`EXCEPT`
- `FROM`句のないリテラル`SELECT`同士の`UNION ALL`
- `EXISTS`式
- CTE本文の`FREQUENCY`
- ユーザー定義の`CREATE ROLLUP ... AS (...)`クエリのCTE

CTEはテーブルタイプ別のDML機能を拡張しません。LOG、TAG、LOOKUP、VOLATILE、TRANSACTIONの
参照と取り込みは、それぞれの既存規則に従います。

## エラーの確認

| 状況 | 確認内容 |
|---|---|
| CTE名の重複 | 同じ`WITH`句で各名前を1回だけ宣言しているか確認します。 |
| 列数の不一致 | 明示したCTE列数と`SELECT`結果列数をそろえます。 |
| 列名の重複 | 明示的な列リストから重複名を削除します。 |
| 前方参照 | 参照先のCTEを先に宣言します。 |
| 自己参照 | 再帰構造を削除するか、深さが固定されたSQLやアプリケーションの繰り返しへ変更します。 |
| テーブルが見つからない | 修飾名がCTEではなく実際のTABLE/VIEWを検索しているか確認します。 |
| 展開上限の超過 | 繰り返し参照の連鎖を減らすか、中間結果を別オブジェクトへ分離します。 |
| VIEWのバインドエラー | VIEW定義とCTEから`?`を削除し、参照時の条件へ移します。 |
| 構文エラー | 非対応の再帰、実体化、文頭の`WITH ... DML`構文を使用していないか確認します。 |

## 他のDBMSからの移行

| 移行元DBMSの機能 | Machbaseでの対応 |
|---|---|
| PostgreSQL/MySQLの`WITH RECURSIVE` | 深さが固定されたSQL、またはアプリケーションの繰り返しへ変更します。 |
| PostgreSQL/SQLiteの`MATERIALIZED` | キーワードを削除し、1回だけ評価されると仮定しないでください。 |
| PostgreSQL/SQLiteの`NOT MATERIALIZED` | キーワードを削除し、`EXPLAIN`で実際の計画を確認します。 |
| Oracleの再帰subquery factoring | 自己参照を除いた非再帰CTEのみ移行します。 |
| SQL Serverの`WITH ... UPDATE/DELETE/MERGE` | CTEとDMLを分離し、テーブル別のDML規則を適用します。 |
| 再帰CTEの`SEARCH`または`CYCLE` | 経路と循環検出はアプリケーションや保存列で処理します。 |

## 関連ドキュメント

- [SELECT構文](../select-syntax/)
- [DML構文](../dml-syntax/)
- [VIEW構文](../view-syntax/)
- [集合演算子](../set-operator-syntax/)
- [PIVOT構文](../pivot-syntax/)
- [ウィンドウ関数とOVER](../window-function-over-syntax/)
- [クエリ分析とEXPLAIN](/dbms/performance-tuning/performance-query-tuning/)
