---
type: docs
title: '5.7 運用とデータライフサイクル'
weight: 70
toc: true
---
TAGデータのライフサイクルは、手動削除、Retention Policy、重複入力の防止で管理します。
このページでは運用上の選択基準を説明します。全SQL構文は関連リファレンスを参照してください。

<a id="original-85-deleting-data"></a>

## TAGデータの削除

TAGデータはタグ識別子と軸条件を使用して削除範囲を制限します。時間軸TAGの代表的な選択肢は
次のとおりです。

| 目的 | 条件 |
| --- | --- |
| 1つのタグの全データを削除 | タグの`PRIMARY KEY`の一致 |
| 1つのタグの時間範囲を削除 | タグの一致 + BASETIME範囲 |
| 全タグの過去データを削除 | BASETIME条件または`BEFORE` |
| テーブルの全データを削除 | 条件なしのTAG `DELETE` |

次の例では専用の検証テーブルを作成し、削除範囲を確認して後片付けします。

```sql
CREATE TAG TABLE ch5_lifecycle (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);

INSERT INTO ch5_lifecycle VALUES
    ('TAG_0001', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1.0);
INSERT INTO ch5_lifecycle VALUES
    ('TAG_0001', TO_DATE('2026-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2.0);
INSERT INTO ch5_lifecycle VALUES
    ('TAG_0002', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3.0);

DELETE FROM ch5_lifecycle
 WHERE name = 'TAG_0001'
   AND time < TO_DATE('2026-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');

SELECT name, time, value
  FROM ch5_lifecycle
 ORDER BY name, time;

DELETE FROM ch5_lifecycle;
SELECT COUNT(*) FROM ch5_lifecycle;
DROP TABLE ch5_lifecycle;
```

最初の削除後は、TAG_0001の2026-01-02の値2.0とTAG_0002の値3.0が残ります。
全削除後のCOUNTは0です。DATAの削除とMETADATAの削除は別の操作です。
タグの登録情報まで削除する場合は[METADATAの削除](../tag-metadata/)の条件も確認します。

削除条件の演算子とEditionごとのサポート範囲は
[TAG DELETE構文](/dbms/reference/sql/syntax/dml-syntax/)を参照してください。
手動削除を定期的に繰り返す必要がある場合は、
[Retention Policy](/dbms/operations-configuration-recovery/policy-data-retention/)を使用してください。

### ROLLUPデータの処理

元のTAGデータの削除と計算済みROLLUPの処理は別です。生データを訂正・削除した後に集計も変更する
必要がある場合は、対象範囲のROLLUPを再構築します。ROLLUPの削除構文を保持ポリシーのように
繰り返し実行しないでください。

- [ROLLUPの部分削除と再構築](/dbms/tag-rollup-usage/rollup-rebuild/)
- [TAGデータ訂正後のROLLUP再構築](../tag-data-update-correction/)

<a id="original-85-duplication-removal"></a>

## 自動重複排除

`TAG_DUPLICATE_CHECK_DURATION`は重複検査期間を分単位で設定します。
Standard Editionでは0～43200分を指定でき、0は無効化を表します。
Cluster Editionでは0のみ許可されるため、以下の有効化の実習はStandard Edition専用です。

サーバー時刻を基準とする検査期間内のデータで、タグ・軸・データ値が同じ行を重複と判定します。
インデックス処理と重複行の整理中に実行されるため、Appendの成功応答を「重複排除済みの行数」と
解釈しないでください。遅延到着データが検査期間外の場合は期待した重複排除が行われない場合があり、
業務キーの一意制約の代わりにはなりません。

```sql
CREATE TAG TABLE ch5_dedup (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
) TAG_DUPLICATE_CHECK_DURATION = 1440;

INSERT INTO ch5_dedup VALUES ('TAG_0001', NOW, 1.0);
INSERT INTO ch5_dedup SELECT name, time, value FROM ch5_dedup;

EXEC TABLE_FLUSH(ch5_dedup);
EXEC INDEX_FLUSH(ch5_dedup);

SELECT name, time, value
  FROM ch5_dedup
 WHERE name = 'TAG_0001';

ALTER TABLE ch5_dedup SET TAG_DUPLICATE_CHECK_DURATION = 60;
DROP TABLE ch5_dedup;
```

2回目の入力は最初の行のコピーなので、軸の時刻も完全に同じです。この実習は運用中の同時入力が
ないことを前提とします。ストレージバッファとインデックスの処理を待ち、1行が残ることを確認します。
通常の収集ループで行ごとに2つのフラッシュを呼び出すパターンは使用しません。

全属性と制約は現在のバージョンの
[CREATE TAG TABLE構文](/dbms/reference/sql/syntax/ddl-syntax/)で確認してください。
保持ポリシーですでに削除されたデータは、重複判定の対象として残っていません。

## 運用の確認手順

1. 生データとROLLUPの保持期間をそれぞれ決めます。
2. 遅延到着データの最大遅延を測定し、重複検査期間を決めます。
3. 削除・訂正前に対象タグと時間範囲を`SELECT`で確認します。
4. 大量変更後にROLLUPと代表的な検索結果を検証します。
5. 入力量、ディスク使用量、Retentionの実行状態をまとめて監視します。
