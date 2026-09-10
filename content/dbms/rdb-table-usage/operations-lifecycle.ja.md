---
type: docs
title: '8.7 運用とデータライフサイクル'
weight: 70
toc: true
---

古い業務データを削除するときは、日付だけの確認では不十分です。
キャンセル済みの注文と処理中の注文では保持基準が異なり、削除処理自体も他の書き込みと競合し得ます。
業務条件と処理単位を先に決めてから削除してください。

<a id="operations-rdb-lifecycle"></a>

<a id="원본과-업무-상태의-보관-목적을-나눕니다"></a>

## データの保持基準

TAG・LOGには元の時系列データ、TRANSACTIONには変更可能な状態や要約結果を格納できます。
両方の保持期間が同じである必要はありません。
TRANSACTIONにはTAG・LOGのRetention Policyをそのまま適用しません。
業務条件に適したDELETEと外部ジョブスケジュールを設計してください。

<a id="operations-rdb-transaction"></a>
<a id="operations-rdb-cleanup"></a>

<a id="삭제-전후를-같은-실습에서-확인합니다"></a>

## 削除とロールバック

```sql
CREATE TRANSACTION TABLE ch8_cleanup (
    id      LONG PRIMARY KEY,
    status  VARCHAR(16),
    created DATETIME
);
INSERT INTO ch8_cleanup VALUES (1, 'CANCELLED', TO_DATE('2025-12-01', 'YYYY-MM-DD'));
INSERT INTO ch8_cleanup VALUES (2, 'PENDING', TO_DATE('2025-12-01', 'YYYY-MM-DD'));
INSERT INTO ch8_cleanup VALUES (3, 'CANCELLED', TO_DATE('2026-02-01', 'YYYY-MM-DD'));

BEGIN;
SELECT COUNT(*) AS delete_candidates FROM ch8_cleanup
 WHERE status = 'CANCELLED' AND created < TO_DATE('2026-01-01', 'YYYY-MM-DD');
DELETE FROM ch8_cleanup
 WHERE status = 'CANCELLED' AND created < TO_DATE('2026-01-01', 'YYYY-MM-DD');
SELECT id, status FROM ch8_cleanup ORDER BY id;
ROLLBACK;

SELECT COUNT(*) AS after_rollback FROM ch8_cleanup;
```

対象は1件で、削除中は行2・3、ロールバック後は3件です。
確認用の実習ではロールバックしていますが、運用で確定する場合は業務承認と結果確認後にCOMMITを選択します。
結果カーソルは終了前に閉じる必要があります。

事前の検索件数と実際の影響行数を同じものと見なさないよう注意してください。
同時変更とスナップショット競合を考慮し、実行時に得た影響行数と最終状態まで記録してください。
[ロックと再試行](../locking-conflict-timeout/)で関連する状況を確認できます。

<a id="큰-작업은-다시-시작할-기준을-남깁니다"></a>

## バッチ処理と再開

削除全体を1つの長いトランザクションで処理するより、日付区間や一意キー範囲で分割してください。
各区間の境界、処理件数、コミット結果を記録します。
途中の障害後に、どこから処理を再開するか分かる必要があります。

マスターデータの移動で、他のテーブルへコピーしてから元データを削除する場合も注意が必要です。
現在、障害時に複数のTRANSACTIONテーブルのアトミックコミットが保証されるとは考えないでください。
[トランザクションの保証範囲](../transaction/)に合わせてコピー結果の確認と再開手順を設計します。
外部API呼び出しや長いファイル処理をBEGIN内で待たないことも重要です。

<a id="operations-rdb-backup-recovery"></a>

<a id="삭제-전에-백업을-실제로-읽어-봅니다"></a>

## バックアップの検証

バックアップコマンドの成功だけでなく、マウントしたバックアップで業務キー・行数・合計・インデックスを点検してください。
マウントしたデータの検索には、`マウント名.所有者.テーブル名`の3部構成の名前を使用します。
2部構成の名前を使い、本番データと混同しないでください。

TRANSACTIONは、増分バックアップでもその時点のテーブルストレージ全体のスナップショットを含みます。
変更行数に比例してだけ容量が増えると計算しないでください。
具体的な実習は[バックアップ・リストア・マウント](../backup-restore-mount/)にあります。

<a id="operations-rdb-checklist"></a>

<a id="정리-후에도-조회와-공간을-따로-확인합니다"></a>

## 削除後の運用点検

行数が減っても、OS上のファイルサイズが直ちに同じ割合で減るわけではありません。
業務データの件数、実際のファイル使用量、バックアップ保持量を個別に確認してください。
ファイルサイズを減らすために、内部SQLiteファイルへ直接接続したり、ファイルを任意に削除したりしないでください。

```sql
DROP TABLE ch8_cleanup;
```

削除処理が失敗したら、追加削除を試す前に、最後に成功した区間とコミット結果を確認してください。
これらの記録が、データの欠落と重複処理を減らすために必要です。
