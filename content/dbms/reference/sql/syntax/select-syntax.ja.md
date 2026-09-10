---
type: docs
title: 'SELECT'
weight: 10
toc: true
---

`SELECT`はMachbaseの各種テーブルからデータを参照・絞り込み・集計する構文です。

## SELECTの完全な構文

```sql
query_stmt ::=
    [ with_clause ]
    select_stmt

select_stmt ::=
    'SELECT' [ hint_clause ] target_list
    [ 'FROM' table_reference_list ]
    [ 'WHERE' condition_expr ]
    [ 'DURATION' duration_expr ]
    [ 'GROUP BY' expr_list [ 'HAVING' condition_expr ] ]
    [ 'ORDER BY' expr_list [ 'ASC' | 'DESC' ] ]
    [ 'SERIES BY' condition_expr ]
    [ 'LIMIT' [ offset ',' ] row_count ]

-- 集合演算子
select_stmt 'UNION ALL' select_stmt
```

`DURATION`は`WHERE`の後、`GROUP BY`・`HAVING`・`ORDER BY`・`SERIES BY`・`LIMIT`の前に記述します。
上記はSQL句の記述順序であり、内部の実行順序ではありません。

`with_clause`はStandard Editionで非再帰CTEを宣言します。構文と制約の詳細は
[WITH / CTE構文](../cte-syntax/)を参照してください。

### 選択リスト（target_list）

```sql
target_list ::=
    '*'
  | target_expr ( ',' target_expr )*

target_expr ::=
    column_name [ 'AS' alias ]
  | expr [ 'AS' alias ]
  | '(' subquery ')' [ 'AS' alias ]
```

### FROM句

```sql
table_reference_list ::=
    table_reference ( ',' table_reference )*

table_reference ::=
    table_name [ alias ]
  | '(' subquery ')' [ alias ]
  | table_name [ alias ] join_clause
  | view_name [ alias ]

join_clause ::=
    [ 'INNER' | 'LEFT OUTER' | 'RIGHT OUTER' ] 'JOIN' table_reference 'ON' condition_expr
  | 'CROSS JOIN' table_reference
```

---

## FROM句のないSELECT

テーブルを参照せず、定数、算術式、単純な関数の結果を1行で返します。

```sql
SELECT 1;
SELECT 'alive';
SELECT 1 + 2;
SELECT ABS(-7);
SELECT SYSDATE;
```

---

## WHERE句

```sql
condition_expr ::=
    expr comparison_op expr
  | expr [ 'NOT' ] 'BETWEEN' expr 'AND' expr
  | column_name [ 'NOT' ] 'IN' '(' value_list | subquery ')'
  | column_name 'RANGE' duration_spec
  | column_name [ 'NOT' ] 'SEARCH' string_literal
  | column_name 'ESEARCH' pattern_literal
  | column_name [ 'NOT' ] 'REGEXP' pattern_literal
  | expr 'IS' [ 'NOT' ] 'NULL'
  | condition_expr ( 'AND' | 'OR' ) condition_expr
  | 'NOT' condition_expr
  | '(' condition_expr ')'
  | '(' subquery ')'
```

### 主なWHERE演算子

| 演算子 | 説明 |
|--------|------|
| `=`, `<>`, `<`, `<=`, `>`, `>=` | 比較演算子 |
| `BETWEEN value1 AND value2` | 範囲条件 |
| `IN (value_list)` | 値リスト条件 |
| `IN (subquery)` | サブクエリIN |
| `RANGE n unit` | 現在時刻を基準とする時間範囲条件 |
| `SEARCH 'keyword'` | キーワードインデックスを使用するテキスト検索 |
| `ESEARCH 'pattern%'` | 拡張テキスト検索（%ワイルドカード） |
| `REGEXP 'pattern'` | 正規表現検索（インデックスを使用しない） |
| `IS NULL` / `IS NOT NULL` | NULL条件 |

```sql
-- BETWEEN
SELECT * FROM sensor_log WHERE value BETWEEN 10.0 AND 20.0;

-- IN
SELECT * FROM sensor_log WHERE status IN ('OK', 'WARN');

-- RANGE (現在時刻を基準とする直近1時間)
SELECT * FROM sensor_log WHERE _arrival_time RANGE 1 HOUR;

-- SEARCH (キーワードインデックスを使用)
SELECT * FROM log_table WHERE message SEARCH 'error';

-- ESEARCH (ワイルドカードパターン)
SELECT * FROM log_table WHERE message ESEARCH 'timeout%';

-- REGEXP (正規表現)
SELECT * FROM log_table WHERE message REGEXP 'error[0-9]+';
```

---

## GROUP BY / HAVING

```sql
'GROUP BY' expr_list [ 'HAVING' condition_expr ]
```

```sql
SELECT name, AVG(value), MAX(value), COUNT(*)
  FROM sensor_log
 GROUP BY name
HAVING AVG(value) > 50.0;
```

---

## ORDER BY

```sql
'ORDER BY' expr_list [ 'ASC' | 'DESC' ]
```

```sql
SELECT name, value FROM sensor_log ORDER BY value DESC;
SELECT name, value FROM sensor_log ORDER BY name ASC, value DESC;
```

---

## LIMIT

```sql
'LIMIT' [ offset ',' ] row_count
```

```sql
-- 先頭10件のみ参照
SELECT * FROM sensor_log LIMIT 10;

-- 11件目から10件を参照
SELECT * FROM sensor_log LIMIT 10, 10;
```

---

## DURATION

`_arrival_time`列を基準に参照する時間範囲を指定します。

```sql
duration_expr ::=
    number time_unit [ ( 'BEFORE' | 'AFTER' ) number time_unit ]
  | 'FROM' datetime_expr 'TO' datetime_expr

time_unit ::= 'YEAR' | 'MONTH' | 'WEEK' | 'DAY' | 'HOUR' | 'MINUTE' | 'SECOND'
```

```sql
-- 直近1時間のデータ
SELECT * FROM sensor_log DURATION 1 HOUR;

-- 1日前を基準とする1時間の範囲
SELECT * FROM sensor_log DURATION 1 HOUR BEFORE 1 DAY;

-- 明示的な範囲
SELECT * FROM sensor_log
DURATION FROM TO_DATE('2024-01-01','YYYY-MM-DD')
         TO TO_DATE('2024-01-31','YYYY-MM-DD');
```

---

## JOIN

### INNER JOIN (カンマ形式)

```sql
SELECT t1.id, t2.name
  FROM sensor_log t1, devices t2
 WHERE t1.id = t2.device_id AND t1.value > 50;
```

### ANSI JOIN

```sql
-- INNER JOIN
SELECT t1.id, t2.name
  FROM sensor_log t1
  INNER JOIN devices t2 ON (t1.id = t2.device_id)
 WHERE t1.value > 50;

-- LEFT OUTER JOIN
SELECT t1.id, t2.location
  FROM sensor_log t1
  LEFT OUTER JOIN devices t2 ON (t1.name = t2.name);

-- RIGHT OUTER JOIN
SELECT t1.value, t2.name
  FROM sensor_log t1
  RIGHT OUTER JOIN devices t2 ON (t1.name = t2.name);
```

> FULL OUTER JOINはサポートしません。

---

## SERIES BY

ソート済みの結果から、条件を連続して満たすレコードのグループを抽出します。

```sql
'ORDER BY' expr 'SERIES BY' condition_expr
```

```sql
-- C2 > 1を連続して満たすレコード群を参照
SELECT c1, c2, SERIESNUM() AS grp
  FROM t1
 ORDER BY c1
 SERIES BY c2 > 1;
```

---

## SUBQUERY

```sql
-- FROM句のサブクエリ（インラインビュー）
SELECT a.name, a.avg_val
  FROM (SELECT name, AVG(value) AS avg_val FROM sensor_log GROUP BY name) a
 WHERE a.avg_val > 50;

-- WHERE句のサブクエリ
SELECT * FROM sensor_log
 WHERE value > (SELECT AVG(value) FROM sensor_log);

-- IN句のサブクエリ
SELECT * FROM sensor_log
 WHERE name IN (SELECT name FROM devices WHERE status = 'ACTIVE');
```

> 相関サブクエリ（外側のクエリの列を参照するサブクエリ）はサポートしません。

---

## CASE式

```sql
-- simple CASE
CASE expr
    WHEN value1 THEN result1
    [ WHEN value2 THEN result2 ... ]
    [ ELSE default_result ]
END

-- searched CASE
CASE
    WHEN condition1 THEN result1
    [ WHEN condition2 THEN result2 ... ]
    [ ELSE default_result ]
END
```

```sql
SELECT name,
       value,
       CASE
           WHEN value >= 80 THEN 'HIGH'
           WHEN value >= 40 THEN 'MID'
           ELSE 'LOW'
       END AS level
  FROM sensor_log;
```

---

## PIVOT

インラインビューの集計結果を行から列へ変換します。

```sql
'PIVOT' '(' aggregate_func '(' column ')' 'FOR' pivot_column 'IN' '(' value_list ')' ')'
```

```sql
SELECT *
  FROM (SELECT regtime, tagid, dvalue FROM result_d)
 PIVOT (SUM(dvalue) FOR tagid IN ('AXIS_X', 'AXIS_Y', 'AXIS_Z'));
```

---

## UNION ALL

```sql
select_stmt 'UNION ALL' select_stmt
```

2つのSELECT結果を結合します。列数と型に互換性が必要です。重複を除去する`UNION`、`INTERSECT`、`EXCEPT`はサポートしません。

```sql
SELECT id, name FROM table_a
UNION ALL
SELECT id, name FROM table_b;
```

---

## SAVE DATA INTO

SELECT結果をCSVファイルに保存します。

```sql
'SAVE DATA INTO' 'file_path'
    [ 'HEADER' ( 'ON' | 'OFF' ) ]
    [ ( 'FIELDS' | 'COLUMNS' )
        [ 'TERMINATED BY' char ]
        [ 'ENCLOSED BY' char ] ]
    [ 'ENCODED BY' encoding ]
    'AS' select_stmt
```

```sql
SAVE DATA INTO '/tmp/sensor_data.csv' HEADER ON AS SELECT * FROM sensor_log;
```

---

## 関連ドキュメント

- [WITH / CTE syntax](../cte-syntax/) - 非再帰の共通テーブル式
- [ヒント辞典](../select-hint-syntax/) - SELECTクエリの性能最適化ヒント
- [SERIES BY](../series-syntax/) - 連続条件によるグループ化の詳細
- [PIVOT](../pivot-syntax/) - 行から列への変換の詳細例
- [SEARCH/ESEARCH/REGEXP](../search-esearch-regexp-syntax/) - テキスト検索の詳細
- [DURATION相対時間式](../../relative-time/) - 時間範囲式の全一覧
