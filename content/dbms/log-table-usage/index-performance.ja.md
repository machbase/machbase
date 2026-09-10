---
type: docs
title: '7.6 インデックスとパフォーマンス'
weight: 60
toc: true
---

インデックスを作成してもクエリが速くならない場合は、まずそのクエリがインデックスを使用できるか確認します。
インデックスは読み取りコストを減らす一方、入力・保存・バックグラウンド処理のコストを増やします。
カラムごとに作成するより、代表的な検索条件を決めるところから始めてください。

<a id="index-tuning-log"></a>

<a id="조회-조건에-맞춰-선택합니다"></a>

## インデックスの選択

| 検索条件 | 検討するインデックス | 確認事項 |
|---|---|---|
| 数値・DATETIMEなどの値と範囲 | LSM | 条件に適したサポート型と実際の実行計画 |
| VARCHAR・TEXTの単語・トークンパターン | KEYWORD | SEARCH・ESEARCHを使用し、LIKEとの結果の意味の違いを確認 |
| サポート型の繰り返し値の分析 | BITMAP | 値の分布とエンコーディング、入力・保存コスト |

LOGの`_arrival_time`範囲には、まず標準の時間アクセス経路を利用します。
同じ目的のインデックスを慣習的に追加する必要はありません。
サポート型と属性は[INDEX構文](/dbms/reference/sql/syntax/index-syntax/)で確認してください。
一般的なRDBMSの複合インデックス設計をそのまま適用しないでください。

<a id="같은-데이터에서-생성-전후를-비교합니다"></a>

## インデックス作成前後の比較

```sql
CREATE LOG TABLE ch7_index (
    event_id   INTEGER,
    event_time DATETIME,
    severity   SHORT,
    message    VARCHAR(256)
);
INSERT INTO ch7_index VALUES (
    1, TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1, 'service started');
INSERT INTO ch7_index VALUES (
    2, TO_DATE('2026-01-01 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 'database timeout');
INSERT INTO ch7_index VALUES (
    3, TO_DATE('2026-01-01 10:02:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 'connection timeout');

EXPLAIN SELECT event_id FROM ch7_index WHERE severity = 3;

CREATE INDEX ch7_index_time ON ch7_index(event_time) INDEX_TYPE LSM;
CREATE INDEX ch7_index_message ON ch7_index(message) INDEX_TYPE KEYWORD;
CREATE INDEX ch7_index_severity ON ch7_index(severity)
    INDEX_TYPE BITMAP BITMAP_ENCODE = RANGE;

EXEC TABLE_FLUSH(ch7_index);
EXEC INDEX_FLUSH(ch7_index);

EXPLAIN SELECT event_id FROM ch7_index WHERE severity = 3;
EXPLAIN SELECT event_id FROM ch7_index WHERE message SEARCH 'timeout';

SELECT event_id FROM ch7_index
 WHERE message SEARCH 'timeout'
 ORDER BY event_id;
SHOW INDEXES;
```

検索結果はイベント2と3です。実行計画で値条件とSEARCHが使用するアクセス経路を比較し、
SHOW INDEXESで作成された名前を確認してください。
この3行は動作を理解するためのサンプルであり、性能測定用のデータではありません。

<a id="저장-반영과-인덱스-반영은-별도-단계입니다"></a>

## データとインデックスの反映

`TABLE_FLUSH`はテーブルデータを反映する操作、`INDEX_FLUSH`はインデックス構築が進むまで待機する操作です。
実習で作成前後の計画と時間を比較するときは、上記のように区別して使用してください。

インデックスが存在しても、入力データ全体のインデックスへの反映が完了したとは限りません。
構築の遅延は検索コストに影響し得ます。ただし、行を入力するたびに両方のコマンドを呼ぶと、バッチ入力の利点が減ります。
運用では入力レートとバックグラウンド処理速度を併せて監視し、必要な同期タイミングだけを決めてください。

インデックスへの反映が遅いことを理由に、同じデータを再入力しないよう注意してください。
重複を避けるため、再入力前に元データの検索件数とインデックス状態を個別に確認する必要があります。

<a id="실제-성능은-대표-부하에서-판단합니다"></a>

## 性能測定の基準

作成前後で同じデータ量・条件値・同時入力負荷を使用してください。
1回の実行時間だけでなく、繰り返し検索の時間、入力スループット、インデックス容量、構築遅延を併せて記録します。
LIKE・REGEXPは元の文字列に対して条件を評価するため、先に時間範囲を制限すると検査対象を減らせます。
KEYWORDインデックスが存在しても、LIKEがSEARCHに変わるわけではありません。

```sql
DROP INDEX ch7_index_severity;
DROP INDEX ch7_index_message;
DROP INDEX ch7_index_time;
DROP TABLE ch7_index;
```

計画を読み取りにくい場合は、クエリとEXPLAINの結果を比較してください。
[インデックスチューニング](/dbms/performance-tuning/index-tuning/)の診断手順が、次の確認箇所を決める参考になります。
