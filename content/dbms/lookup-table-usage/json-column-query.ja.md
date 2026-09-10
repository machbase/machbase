---
type: docs
title: '9.12 JSON列とJSONクエリ'
weight: 120
toc: true
---

LOOKUPテーブルのJSON列のサポート範囲と、JSON条件によるクエリを説明します。

<a id="condition-query-lookup-json"></a>

## LOOKUPのJSON条件検索

LOOKUPテーブルは、`JSON`列を一般列としてサポートします。
JSON列は、可変的な属性値を参照データと一緒に保存する場合に使用できます。

```sql
CREATE LOOKUP TABLE ch9_json (
    sensor_id VARCHAR(80) PRIMARY KEY,
    location  VARCHAR(200),
    config    JSON
);

INSERT INTO ch9_json VALUES (
    'TEMP-01',
    'factory1',
    '{"unit":"celsius","level":3,"threshold":{"high":90.0}}'
);

SELECT sensor_id, config
FROM ch9_json
WHERE config->'$.unit' = 'celsius';
```

<a id="design-column-lookup-json"></a>

## 型別のJSON条件

数値を数値として比較する場合は、型別のJSON抽出関数を使用します。

```sql
SELECT sensor_id
FROM ch9_json
WHERE JSON_EXTRACT_INTEGER(config, '$.level') >= 3
  AND JSON_EXTRACT_DOUBLE(config, '$.threshold.high') > 80.0;
```

JSON構造自体も確認できます。

```sql
SELECT sensor_id
FROM ch9_json
WHERE JSON_IS_VALID(config) = 1
  AND JSON_TYPEOF(config, '$.threshold') = 'Object';
```

<a id="lookup-json-serialized-string"></a>

## PRIMARY KEYの制約

LOOKUPテーブルはJSON列を保存できますが、JSON列を`PRIMARY KEY`には使用できません。
行識別子には、`INTEGER`、`LONG`、`VARCHAR`などの安定した一般型を使用します。

```sql
-- 失敗: JSON列はPRIMARY KEYに使用できません。
CREATE LOOKUP TABLE ch9_json_bad (
    config JSON PRIMARY KEY,
    note   VARCHAR(80)
);
```

```sql
-- 推奨: 別の識別子をPRIMARY KEYに使用します。
CREATE LOOKUP TABLE ch9_json_ok (
    sensor_id VARCHAR(80) PRIMARY KEY,
    config    JSON,
    note      VARCHAR(80)
);
```

<a id="lookup-json-design-criteria"></a>

## 設計基準

| 状況 | 推奨方法 |
|------|----------|
| 結合・検索で頻繁に使用する値 | 別の列 |
| 機器ごとに異なる可変属性 | JSON列 |
| 数値条件検索 | 一般の数値列に分離 |
| PRIMARY KEY | 安定した識別子列を使用 |
| 高頻度のパス検索 | 別の列に抽出 |

JSONパスごとの専用インデックスはサポートしていません。
高頻度の検索条件は別の列に分離し、その列にインデックスを適用する設計を先に検討してください。

```sql
CREATE LOOKUP TABLE ch9_json_fast (
    sensor_id VARCHAR(80) PRIMARY KEY,
    unit      VARCHAR(16),
    level     INTEGER,
    config    JSON
);

CREATE INDEX ch9_json_unit_idx ON ch9_json_fast(unit);
```

<a id="lookup-json-update-delete"></a>

## UPDATE・DELETEの条件

```sql
UPDATE ch9_json
SET location = 'factory2'
WHERE config->'$.unit' = 'celsius';

DELETE FROM ch9_json
WHERE JSON_EXTRACT_INTEGER(config, '$.level') < 2;
```

対象範囲が広くなる場合があるため、UPDATE/DELETE前に同じ条件で件数を確認します。

<a id="lookup-json-limitations"></a>

このページの実習オブジェクトは、次のように削除します。
`ch9_json_bad`は作成に失敗する例なので、削除対象ではありません。

```sql
DROP TABLE ch9_json_fast;
DROP TABLE ch9_json_ok;
DROP TABLE ch9_json;
```

## 注意事項

- LOOKUPテーブルは、JSON列を一般列としてサポートします。
- JSON列はPRIMARY KEYには使用できません。
- JSONパスごとの専用インデックスはサポートしていません。
- 頻繁に検索する値は、LOOKUPの一般列に分離します。
- JSONパスインデックスが必要なら、TRANSACTIONまたはTAGテーブルを検討します。
