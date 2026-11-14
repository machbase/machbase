---
type: docs
title: '6.5 条件付きROLLUP'
weight: 50
toc: true
---

<a id="original-85-rollup-conditional"></a>

## 元データをフィルタリングしてから集計

条件付きROLLUPは、元データの品質・状態の条件を適用した統計を保持します。
計算済みの平均から後で不良サンプルだけを除く処理とは異なります。
条件で使用したqualityカラム自体が集計結果に保持されるわけでもありません。

## 1. テーブルと2つのROLLUPの準備

```sql
CREATE TAG TABLE ch6_condition (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_condition_all
  ON ch6_condition(value) INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP ch6_condition_good
  ON ch6_condition(value) INTERVAL 1 MIN EXTENSION WHERE quality = 1;
INSERT INTO ch6_condition VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_condition VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_condition VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_condition VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
INSERT INTO ch6_condition VALUES
    ('TEMP_01', TO_DATE('2026-01-01 00:00:50', 'YYYY-MM-DD HH24:MI:SS'), 90.0, 0);
EXEC TABLE_FLUSH(ch6_condition);
ALTER ROLLUP ch6_condition_all FORCE;
ALTER ROLLUP ch6_condition_good FORCE;
```

## 2. 元データの条件とROLLUPの比較

```sql
SELECT DATE_TRUNC('minute', time) AS bucket, COUNT(value), AVG(value),
       MIN(value), MAX(value), FIRST(time, value), LAST(time, value)
  FROM ch6_condition
 WHERE name = 'TEMP_01' AND quality = 1
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_condition_good) */
       rollup('min', 1, time) AS bucket, COUNT(value), AVG(value),
       MIN(value), MAX(value), FIRST(time, value), LAST(time, value)
  FROM ch6_condition WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_condition_all) */
       rollup('min', 1, time) AS bucket, COUNT(value), AVG(value),
       MIN(value), MAX(value), FIRST(time, value), LAST(time, value)
  FROM ch6_condition WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

| バケット・集合 | COUNT | AVG | MIN | MAX | FIRST | LAST |
|---|---:|---:|---:|---:|---:|---:|
| 00:00 全件 | 3 | 40 | 10 | 90 | 10 | 90 |
| 00:00 quality=1 | 2 | 15 | 10 | 20 | 10 | 20 |
| 00:01 両集合共通 | 1 | 30 | 30 | 30 | 30 | 30 |

このサンプルでは、不良値が区間の最後にあるためLASTも異なります。
FIRST/LASTが返すのは、時刻と値の組ではなく、選択されたvalueです。

## 候補の明示的な選択

この例では、全件統計と正常値の統計の結果集合を固定するためにヒントを使用します。
自動選択は条件なしの候補を優先しますが、条件付き候補しかない場合はフィルタリング済み統計を選択し得ます。
「条件付きROLLUPは常に無視される」「EXTENSIONでは常にヒントが必須」という規則と解釈しないでください。

<a id="rollup-conditional-extension-tc"></a>
<a id="original-85-rollup-conditional-extension"></a>
<a id="condition-conditional-rollup"></a>

## 構文と制約

通常のROLLUPのフィルターは、INTERVAL・EXTENSIONの後のWHEREに記述します。
比較、BETWEEN、IN、LIKE、論理演算、サポートされるスカラー関数を使用できますが、
サブクエリ、集計関数、タグ名PRIMARY KEYの条件はサポートしていません。
CustomはSELECT内のWHEREを使用するため、構文を混同しないでください。

## 状態確認とクリーンアップ

```sql
SELECT DISTINCT ROLLUP_NAME, PREDICATE, ENABLED
  FROM V$ROLLUP WHERE ROOT_TABLE = 'CH6_CONDITION';
DROP ROLLUP ch6_condition_good;
DROP ROLLUP ch6_condition_all;
DROP TABLE ch6_condition;
```

業務の品質基準が変わったら、条件と再集計計画も更新してください。
既存の集計が新しい条件に自動的に切り替わることはありません。
[制御](../ingestion-control-rollup/)と[再構築範囲](../rollup-rebuild/)を確認してください。
