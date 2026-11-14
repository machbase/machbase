---
type: docs
title: '6.12 ROLLUPの活用シナリオ'
weight: 120
toc: true
---

<a id="storage-sensor-data-rollup"></a>

## センサー別の元データと区間統計

2つのセンサーが同時刻に測定しても、単位が異なる場合は平均を混在させません。
次は、現在の単位をメタデータで管理し、タグ別の集計を検索する独立した実習です。

### 1. 作成と入力

```sql
CREATE TAG TABLE ch6_scenario (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
) METADATA (unit VARCHAR(16));
INSERT INTO ch6_scenario METADATA VALUES ('TEMP_01', 'celsius');
INSERT INTO ch6_scenario METADATA VALUES ('PRESS_01', 'bar');
INSERT INTO ch6_scenario VALUES ('TEMP_01', TO_DATE('2026-01-01 10:00:00'), 20);
INSERT INTO ch6_scenario VALUES ('TEMP_01', TO_DATE('2026-01-01 10:00:30'), 22);
INSERT INTO ch6_scenario VALUES ('PRESS_01', TO_DATE('2026-01-01 10:00:00'), 1.02);
CREATE ROLLUP ch6_scenario_ru ON ch6_scenario(value) INTERVAL 1 MIN;
EXEC TABLE_FLUSH(ch6_scenario);
ALTER ROLLUP ch6_scenario_ru FORCE;
```

元データの入力後にROLLUPを作成しても、残っているデータを初期集計します。
作成の完了だけで、初期集計も完了したと判断しないでください。

### 2. 結果の確認

```sql
SELECT name, unit FROM ch6_scenario METADATA ORDER BY name;
SELECT name, DATE_TRUNC('minute', time) AS bucket, COUNT(value), AVG(value)
  FROM ch6_scenario GROUP BY name, bucket ORDER BY name, bucket;
SELECT name, rollup('min', 1, time) AS bucket, COUNT(value), AVG(value)
  FROM ch6_scenario GROUP BY name, bucket ORDER BY name, bucket;
SHOW ROLLUPGAP;
```

TEMP_01は2件・平均21°C、PRESS_01は1件・平均1.02barです。
メタデータ検索で得られるのは現在の単位であり、過去の単位変更履歴は自動的に保持されません。

### 3. 個別の観測値の確認

固定時刻のデータを入力したため、同じ固定範囲を検索します。
このデータに現在時刻を基準にした「直近5分」の条件を適用すると、実行日に応じて結果が空になります。

```sql
SELECT name, time, value FROM ch6_scenario
 WHERE name = 'TEMP_01'
   AND time >= TO_DATE('2026-01-01 10:00:00')
   AND time < TO_DATE('2026-01-01 10:01:00')
 ORDER BY time;
```

元の2つの値は20と22です。統計上の平均21から、個々の観測値や発生順序を復元することはできません。

### 4. クリーンアップ

```sql
DROP ROLLUP ch6_scenario_ru;
DROP TABLE ch6_scenario;
```

<a id="use-cases-rollup"></a>

## 業務別の適用

| 要求 | 確認する設計 |
|---|---|
| 正常品質の統計 | 条件フィルターと候補ヒントを固定して元データと比較 |
| OHLC | 拡張ROLLUPのFIRST/LAST、またはCustomの補助時刻による再集計 |
| 複数センサーの比較 | タグ別の単位と同じバケット・検索範囲を使用 |
| 累積メーターの消費量 | 境界の差、初期化・交換・欠損の規則。サンプル平均と区別 |
| 稼働率 | サンプル比率と時間比率の区別、欠測区間のポリシー |
| 最新の元データと長期集計の結合 | 集計完了を確認した基準点で区間が重複しないよう分割 |

元データとROLLUPの結果をUNION ALLで結合する場合は、境界の重複・欠落とサンプル数の違いを確認してください。
「直近2分は常に未集計」などの固定遅延を保証として使用しないでください。
部分結果を再結合して平均を求める場合は、合計と有効件数を渡します。

機能別の完結した実習は、[条件付き](../conditional-rollup/)、[拡張](../extension-rollup/)、
[JSON](../json-summarized-rollup/)、[Custom](../custom-rollup/)にあります。
問題が発生したら、[診断手順](../../troubleshooting/rollup/)に従って状態と意味を先に確認してください。
