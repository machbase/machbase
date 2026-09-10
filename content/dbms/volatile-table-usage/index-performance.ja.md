---
type: docs
title: '10.6 インデックスとパフォーマンス'
weight: 60
toc: true
aliases:
  - /dbms/volatile-table-usage/red-black-index/
---

VOLATILEテーブルのインデックス作成と選択基準を説明します。

<a id="original-85-volatile-indexes"></a>
<a id="index-strategy-red-black"></a>

## サポートするインデックス

`PRIMARY KEY`を宣言すると、キー検索用のインデックスが作成されます。
一般列には`REDBLACK`インデックスを追加できます。
`BITMAP`と`KEYWORD`インデックスは、VOLATILEテーブルではサポートしていません。

次の例は、作成からクリーンアップまで順に実行できます。

```sql
CREATE VOLATILE TABLE ch10_index (
    id       INTEGER PRIMARY KEY,
    name     VARCHAR(20),
    status   VARCHAR(16)
);

CREATE INDEX ch10_index_name_idx
ON ch10_index(name) INDEX_TYPE REDBLACK;

INSERT INTO ch10_index VALUES (1, 'west device', 'ACTIVE');
INSERT INTO ch10_index VALUES (2, 'east device', 'INACTIVE');

SELECT id, name
FROM ch10_index
WHERE name = 'west device';

DROP INDEX ch10_index_name_idx;
DROP TABLE ch10_index;
```

## 設計基準

- キーによる単一行の検索と更新には`PRIMARY KEY`を使用します。
- 一般列の等価・範囲条件を繰り返し使用する場合だけ、セカンダリインデックスを追加します。
- データだけでなくインデックスもメモリを使用するため、不要なインデックスは削除します。
- 実際のクエリ条件と行数を基準に、作成前後の応答時間とメモリを比較します。

構文の詳細は[インデックス構文](/dbms/reference/sql/syntax/index-syntax/)を参照してください。
