---
type: docs
title: '5.6 インデックスと性能'
weight: 60
toc: true
---
TAGの検索では、まずタグ名と軸の範囲を絞り込むことが基本です。追加インデックスは、実際の検索条件と
実行計画を測定して選択します。

<a id="index-tuning-tag"></a>
<a id="original-85-tag-indexes"></a>

## 基本的な検索経路

TAGテーブルは`PRIMARY KEY`のタグ名と`BASETIME`または`BASEDISTANCE`の軸を基準として
検索できるように、必要な構造を自動管理します。アプリケーションは、生成されるシステムオブジェクトの
名前や保存段階に依存しないでください。

| 検索条件 | 調整方針 |
| --- | --- |
| 1つのタグの軸範囲 | タグ名と軸範囲の両方を明示 |
| 複数タグの同じ時間範囲 | まず時間範囲を制限し、対象タグ数を管理 |
| メタデータ属性 | TAG `METADATA`列として定義 |
| 繰り返す時間集計 | ROLLUPを検討 |
| 値条件が中心の検索 | 値列のセカンダリインデックスを実行計画で検証 |

タグ名や軸範囲を指定せず広範囲のデータを検索すると、読み取り範囲が大きくなります。
常に高速と考えず、実際のデータ量で`EXPLAIN`の結果と実行時間を確認してください。

## METADATA列

設置場所や装置タイプなど、タグごとに1回定義する属性は`METADATA`列として設計します。
通常のスカラーMETADATA列には検索インデックスが自動提供されます。ただしJSON列自体には
自動インデックスがないため、必要なJSONパスにインデックスを定義します。数値ARRAYメタデータ列では
自動・明示的インデックスのいずれもサポートされません。詳細は
[TAGメタデータ](../tag-metadata/)を参照してください。

時系列値や頻繁に変化する状態をMETADATAに入れると、更新経路と意味が不明確になります。
値の性質に応じてTAGデータ列、LOOKUP、VOLATILE、またはTRANSACTION（Standard Edition専用）
テーブルを検討してください。

<a id="값-컬럼-secondary-index"></a>

## 値列のセカンダリインデックス

値条件を頻繁に使用する場合は、`INDEX_TYPE TAG`のセカンダリインデックスを検討できます。
追加インデックスは入力・保存コストを増やすため、作成前後の代表的なクエリを比較します。

次の例では専用の名前で値とJSONパスのインデックスを作成し、実行計画を確認して全オブジェクトを
削除します。小規模なサンプルは構文と結果の検証用であり、性能の優位性を示すものではありません。
名前が重複しない独立した環境で実行します。

```sql
CREATE TAG TABLE ch5_index_tag (
    name    VARCHAR(32) PRIMARY KEY,
    time    DATETIME BASETIME,
    value   DOUBLE,
    payload JSON
) METADATA (
    location VARCHAR(64)
);

INSERT INTO ch5_index_tag METADATA VALUES ('TEMP-01', 'LINE-A');
INSERT INTO ch5_index_tag METADATA VALUES ('TEMP-02', 'LINE-B');
INSERT INTO ch5_index_tag VALUES
    ('TEMP-01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
     10.0, '{"state":"normal"}');
INSERT INTO ch5_index_tag VALUES
    ('TEMP-01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'),
     90.0, '{"state":"alarm"}');
INSERT INTO ch5_index_tag VALUES
    ('TEMP-02', TO_DATE('2026-01-01 00:02:00', 'YYYY-MM-DD HH24:MI:SS'),
     95.0, '{"state":"alarm"}');

CREATE INDEX idx_ch5_index_tag_value
    ON ch5_index_tag (value) INDEX_TYPE TAG;
CREATE INDEX idx_ch5_index_tag_json
    ON ch5_index_tag (payload->'$.state');

EXPLAIN SELECT name, time, value
  FROM ch5_index_tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2026-01-01', 'YYYY-MM-DD')
                AND TO_DATE('2026-01-02', 'YYYY-MM-DD')
   AND value > 80.0;

SELECT name, value FROM ch5_index_tag
 WHERE location = 'LINE-A' AND value > 80.0
 ORDER BY name, time;
SELECT name, value FROM ch5_index_tag
 WHERE payload->'$.state' = 'alarm'
 ORDER BY name, time;

DROP INDEX idx_ch5_index_tag_json;
DROP INDEX idx_ch5_index_tag_value;
DROP TABLE ch5_index_tag;
```

最初のSELECTはTEMP-01の90.0を1行、2番目はTEMP-01の90.0とTEMP-02の95.0を返します。
インデックス作成前後で同じ検索結果になることを確認し、本番規模のデータでは検索時間だけでなく
入力コストとインデックスサイズも比較します。

JSONパス演算子の戻り値の型と比較値の型を合わせ、対象パスが実際にインデックスを使用するか
`EXPLAIN`で確認します。

## 適用しない調整

- TAGの軸列には別途インデックスを作成しません。
- LOG用の`MINMAX_CACHE_SIZE`設定をTAGの値列に適用しません。
- 広い期間の繰り返し集計をセカンダリインデックスだけで解決しようとせず、ROLLUPを検討します。

正確なインデックス構文は[SQL構文リファレンス](/dbms/reference/sql/syntax/)、
測定とチューニング手順は[クエリチューニング](/dbms/performance-tuning/performance-query-tuning/)を
参照してください。
