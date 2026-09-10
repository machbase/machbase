---
type: docs
title: '7.7 運用とデータライフサイクル'
weight: 70
toc: true
---

入力は正常でもディスク使用量が増え続ける場合は、削除基準を確認します。
LOGは業務条件で特定の行を選んで削除するモデルではなく、古い領域から削除するモデルです。
保持期間と、実際に削除される境界を併せて確認する必要があります。

<a id="original-85-deleting-data"></a>
<a id="delete-log-syntax"></a>

<a id="지우려는-목적에-맞게-명령을-고릅니다"></a>

## 削除方法の選択

| 目的 | コマンド | 基準 |
|---|---|---|
| 古いN行を削除 | OLDEST n ROWS | 古い入力行から削除 |
| 最新のN行のみ保持 | EXCEPT n ROWS | 残す行数 |
| 直近の期間のみ保持 | EXCEPT n DAYなど | サーバーの現在時刻から期間を引いた境界 |
| 固定時刻まで削除 | BEFORE datetime_expr | 指定した_arrival_timeの境界を含む |
| 全データを削除 | 条件なしのDELETEまたはTRUNCATE | 全行 |
| 定期的な期間管理 | Retention Policy | 保持期間と実行周期 |

注意: 削除を元に戻せると考えないでください。LOGデータはTRANSACTIONテーブルのROLLBACK対象ではありません。
本番環境では、バックアップと実際の対象範囲を確認してから実行してください。

<a id="delete-log-examples"></a>

<a id="같은-원본으로-세-가지-삭제를-비교합니다"></a>

## 削除方式の比較

コマンドを連続して実行すると、先の削除が次の結果に影響します。
ここでは、同じ3行を別々のテーブルにコピーして比較します。

```sql
CREATE LOG TABLE ch7_lifecycle (event_id INTEGER);
CREATE LOG TABLE ch7_oldest (event_id INTEGER);
CREATE LOG TABLE ch7_keep (event_id INTEGER);
CREATE LOG TABLE ch7_before (event_id INTEGER);

INSERT INTO ch7_lifecycle(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-01', 'YYYY-MM-DD'), 1);
INSERT INTO ch7_lifecycle(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-02', 'YYYY-MM-DD'), 2);
INSERT INTO ch7_lifecycle(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-03', 'YYYY-MM-DD'), 3);

INSERT INTO ch7_oldest(_arrival_time, event_id)
SELECT _arrival_time, event_id FROM ch7_lifecycle ORDER BY _arrival_time;
INSERT INTO ch7_keep(_arrival_time, event_id)
SELECT _arrival_time, event_id FROM ch7_lifecycle ORDER BY _arrival_time;
INSERT INTO ch7_before(_arrival_time, event_id)
SELECT _arrival_time, event_id FROM ch7_lifecycle ORDER BY _arrival_time;

SELECT COUNT(*) AS delete_candidates FROM ch7_before
 WHERE _arrival_time <= TO_DATE('2026-01-02', 'YYYY-MM-DD');

DELETE FROM ch7_oldest OLDEST 1 ROWS;
DELETE FROM ch7_keep EXCEPT 1 ROWS;
DELETE FROM ch7_before BEFORE TO_DATE('2026-01-02', 'YYYY-MM-DD');

SELECT event_id FROM ch7_oldest ORDER BY event_id;
SELECT event_id FROM ch7_keep ORDER BY event_id;
SELECT event_id FROM ch7_before ORDER BY event_id;
```

削除前に確認した件数は2です。各テーブルに残るイベントは次のとおりです。

| テーブル | 残るevent_id |
|---|---|
| ch7_oldest | 2, 3 |
| ch7_keep | 3 |
| ch7_before | 3 |

BEFOREという名前には注意が必要です。
現在のLOGの削除では、指定時刻と等しい行も含まれます。
`WHERE _arrival_time < 境界`で事前に件数を数えると削除対象と異なる場合があるため、上記のように`<=`で確認してください。

```sql
DELETE FROM ch7_lifecycle;
SELECT COUNT(*) AS remaining_rows FROM ch7_lifecycle;

DROP TABLE ch7_before;
DROP TABLE ch7_keep;
DROP TABLE ch7_oldest;
DROP TABLE ch7_lifecycle;
```

全件DELETE後の件数は0になり、テーブル定義は残ります。

<a id="상대-기간-삭제는-현재-시각을-기준으로-합니다"></a>

## 相対期間による削除

```sql
CREATE LOG TABLE ch7_period (event_id INTEGER);
INSERT INTO ch7_period(_arrival_time, event_id) VALUES (SYSDATE - 2d, 1);
INSERT INTO ch7_period(_arrival_time, event_id) VALUES (SYSDATE, 2);

DELETE FROM ch7_period EXCEPT 1 DAY;
SELECT event_id FROM ch7_period ORDER BY event_id;

DROP TABLE ch7_period;
```

作成から検索まで続けて実行すると、イベント2だけが残ります。
基準は「最後に入力された行の時刻」ではなく、サーバーの現在時刻です。
入力が停止していても時間は進むことを、保持ポリシーにも反映してください。

<a id="retention-log-policy"></a>

<a id="반복-삭제는-retention-policy로-관리합니다"></a>

## Retention Policy

次は保持期間1日・実行周期1分の検証用の例です。
本番環境の推奨値ではありません。ポリシーの作成とテーブルへの適用に必要な権限を持つアカウントを使用してください。

```sql
CREATE LOG TABLE ch7_retention (event_id INTEGER);
INSERT INTO ch7_retention(_arrival_time, event_id) VALUES (SYSDATE - 2d, 1);
INSERT INTO ch7_retention(_arrival_time, event_id) VALUES (SYSDATE, 2);

CREATE RETENTION ch7_policy DURATION 1 DAY INTERVAL 1 MIN;
ALTER TABLE ch7_retention ADD RETENTION ch7_policy;

SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'CH7_POLICY';
SELECT TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB WHERE TABLE_NAME = 'CH7_RETENTION';
SELECT event_id FROM ch7_retention ORDER BY event_id;
```

DURATIONは保持する期間、INTERVALは削除を実行する周期です。
適用直後は2行が表示される場合があります。1周期と処理時間が経過した後、次のクエリを再実行してイベント2だけが残るか確認してください。
LAST_DELETED_TIMEは削除の基準時刻であり、実時計における処理の完了時刻ではありません。

```sql
SELECT TABLE_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB WHERE TABLE_NAME = 'CH7_RETENTION';
SELECT event_id FROM ch7_retention ORDER BY event_id;
```

実習が終わったら、適用を解除してからポリシーとテーブルを削除します。

```sql
ALTER TABLE ch7_retention DROP RETENTION;
SELECT TABLE_NAME FROM V$RETENTION_JOB WHERE TABLE_NAME = 'CH7_RETENTION';
DROP RETENTION ch7_policy;
DROP TABLE ch7_retention;
```

解除後のジョブ検索結果は0件です。削除済みの行は復元されません。
1つのテーブルには1つのポリシーを適用します。使用中のポリシーは、先に解除してから削除してください。
運用基準の全体は[データ保持ポリシー](/dbms/operations-configuration-recovery/policy-data-retention/)を参照してください。

<a id="lifecycle-log-backup"></a>

<a id="삭제-전에-조회-가능한-백업인지-확인합니다"></a>

## 削除前のバックアップ検証

バックアップファイルが存在するだけでは、復旧の準備が完了したとはいえません。
削除対象の期間を、Mountまたは隔離したRestore環境で実際に検索してください。
元データ、バックアップ、別途作成した集計データの保持期間も、それぞれ定める必要があります。
環境別のコマンドは[バックアップ・リストア・マウント](/dbms/operations-configuration-recovery/backup-restore-mount/)に従ってください。

<a id="lifecycle-log-monitoring"></a>

<a id="조회-건수와-디스크-공간은-별도로-봅니다"></a>

## データとディスク領域

行が検索結果から消える時点と、OS上のファイル領域が回収される時点は異なる場合があります。
入力量、残っている行の最古の時刻、インデックスとストレージのクリーンアップ状態、ディスク使用量を併せて確認してください。
削除直後にディスク使用量が減らないことを理由に、さらに広い期間を削除しないでください。

削除結果が予想と異なる場合は、境界時刻と適用されたポリシーを確認してください。
保存義務があるデータでは追加の削除を止め、担当者と対象範囲を先に確認することを推奨します。
