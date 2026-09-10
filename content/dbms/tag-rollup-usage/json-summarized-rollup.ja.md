---
type: docs
title: '6.8 JSON SUMMARIZED ROLLUP'
weight: 80
toc: true
---

<a id="json-summarized-rollup"></a>

## JSONパスとドキュメント全体の集計

JSONパスROLLUPは指定パスの数値を集計します。
ドキュメント全体のROLLUPは、JSON SUMMARIZEDカラム内の数値パスごとの統計を保持します。
パスが存在しない値、JSON null、SQL NULL、配列を同じサンプルとして解釈しないでください。

## 準備

```sql
CREATE TAG TABLE ch6_json (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value JSON SUMMARIZED
);
CREATE ROLLUP ch6_json_metric ON ch6_json(value.metric) INTERVAL 1 MIN;
CREATE ROLLUP ch6_json_whole ON ch6_json(value) INTERVAL 1 MIN;
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:00'),
    '{"metric":10,"nested":{"x":2},"status":"OK","items":[1,2]}');
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:10'),
    '{"metric":20,"nested":{"x":4},"status":"WARN","items":[3,4]}');
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:20'),
    '{"metric":null,"status":false}');
INSERT INTO ch6_json VALUES ('S1', TO_DATE('2026-01-01 00:00:30'), NULL);
EXEC TABLE_FLUSH(ch6_json);
ALTER ROLLUP ch6_json_metric FORCE;
ALTER ROLLUP ch6_json_whole FORCE;
```

## パス集計の比較

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       COUNT(JSON_EXTRACT_DOUBLE(value, '$.metric')),
       AVG(JSON_EXTRACT_DOUBLE(value, '$.metric'))
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_json_metric) */
       rollup('min', 1, time) AS bucket,
       COUNT(value.metric), AVG(value.metric)
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_json_metric) */
       rollup('min', 1, time) AS bucket, AVG(value->'$.metric')
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
```

metricの有効な数値サンプルは2個で、平均は15です。dotとarrowは同じパスを表します。
特定の配列要素をパスで指定することと、ドキュメント全体の集計が配列を自動展開することは異なります。
パス宣言の例として`value.items[0]."metric-id"`を使用できますが、対象のJSON構造と数値サンプルが実際に存在することを先に確認してください。

## ドキュメント全体の集計とCOUNT

```sql
SELECT COUNT(*) AS raw_rows, COUNT(value) AS raw_documents FROM ch6_json;

SELECT /*+ ROLLUP_TABLE(ch6_json_whole) */
       rollup('min', 1, time) AS bucket,
       COUNT(value), AVG(value), MIN(value), MAX(value), SUM(value)
  FROM ch6_json WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
```

元データのCOUNT(*)は4、COUNT(value)は3です。
ドキュメント全体のROLLUPのCOUNT(value)は、保存済みのドキュメント集計件数を合算します。
現在、この集計の件数は元データのCOUNT(*)で作成されるため、上記のように数値パスを持つドキュメントとSQL NULLが混在するバケットでは4です。
通常の元データのCOUNT(value)のNULL除外規則を、そのまま適用しないでください。

AVGの結果はmetricが15、nested.xが3で、各パスの有効な数値サンプルから計算します。
文字列・ブール値・JSON null・配列は数値集計から除外され、数値でないパスはnullまたは省略として現れる場合があります。
JSONシリアライズ時のキー順序を、固定の文字列結果として比較しないでください。
数値パスがないドキュメントやSQL NULLだけの区間は、別のサンプルを作成して確認してください。

JSONパス集計とドキュメント全体の集計は候補モードが異なります。
異なるモードのROLLUPをヒントで強制しても同じ結果になるとは考えないでください。
無効なJSONは入力エラーになります。

## クリーンアップ

```sql
DROP ROLLUP ch6_json_whole;
DROP ROLLUP ch6_json_metric;
DROP TABLE ch6_json;
```
