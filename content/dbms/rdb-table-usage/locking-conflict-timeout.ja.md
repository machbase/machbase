---
type: docs
title: '8.10 ロック、競合、busy timeout'
weight: 100
toc: true
---

別々の行を変更しているのにResource busyが発生する場合、行ロックだけを考えると原因を特定しにくくなります。
TRANSACTIONの書き込み競合は、同じテーブルの異なる行の間でも発生し得ます。
待てば解消する競合と、トランザクションを再開始する必要がある競合を区別します。

<a id="transaction-locking-conflict-rdb"></a>
<a id="design-locking-conflict-rdb-busy-timeout-ddl-dml"></a>

<a id="두-연결을-준비합니다"></a>

## 実習環境

この実習は、デフォルトのWAL設定を使用する検証用Standard環境を対象とします。
A・Bは同じアカウント・データベースに接続した別々の接続です。
各コードブロックを示した順に実行し、SELECT結果は最後まで読み取ってカーソルを閉じてください。
スナップショット実習のために、本番サーバーのジャーナルモードを変更しないでください。

Aで準備します。

```sql
SELECT NAME, VALUE FROM V$PROPERTY WHERE NAME = 'TRANSACTION_JOURNAL_MODE';

CREATE TRANSACTION TABLE ch8_lock (id INTEGER PRIMARY KEY, val INTEGER);
INSERT INTO ch8_lock VALUES (1, 10);
INSERT INTO ch8_lock VALUES (2, 20);
```

TRANSACTION_JOURNAL_MODE=4がWALです。
他の値の場合は、次のWALスナップショット実習と同じ結果を期待せず、環境を先に確認してください。

<a id="같은-테이블의-서로-다른-행도-쓰기가-충돌합니다"></a>

## 同時書き込みの競合

Aでトランザクションを開始し、終了せずに待ちます。

```sql
BEGIN;
UPDATE ch8_lock SET val = 11 WHERE id = 1;
```

続いてBで検索します。実習用のB接続だけ、待機時間を0に変更します。

```sql
ALTER SESSION SET TRANSACTION_BUSY_TIMEOUT_MS = 0;
SELECT id, val FROM ch8_lock ORDER BY id;
```

Bには、Aの未コミット値11ではなく、既存値10・20が見えます。
次のBのUPDATEは、意図的にResource busyエラーを発生させる段階です。

```sql
-- B: Aとは異なる行でも、同じテーブルへの書き込みのため失敗が想定されます。
UPDATE ch8_lock SET val = val + 1 WHERE id = 2;
```

AでCOMMITしてから、BのUPDATEを再実行します。

```sql
-- A
COMMIT;
```

```sql
-- B
UPDATE ch8_lock SET val = val + 1 WHERE id = 2;
SELECT id, val FROM ch8_lock ORDER BY id;
```

値は11・21になります。
これは、同じテーブルの書き込み競合を一般的な行単位ロックと解釈してはいけないことを示します。

<a id="wal의-오래된-읽기-스냅샷은-대기로-해결되지-않습니다"></a>

## WALスナップショット競合

前の手順がすべて完了したら、Aで読み取りトランザクションを開始します。

```sql
-- A
BEGIN;
SELECT val FROM ch8_lock WHERE id = 1;
```

Aが11を読み取った後、Bで値を変更します。Bには明示的なトランザクションがない状態です。

```sql
-- B
UPDATE ch8_lock SET val = val + 10 WHERE id = 1;
```

続いてAが書き込みに移行すると、スナップショット競合が想定されます。

```sql
-- A: 意図的に失敗する段階
UPDATE ch8_lock SET val = val + 1 WHERE id = 1;
```

別の接続がすでにコミットしたため、Aの古い読み取りスナップショットをそのまま書き込みに移行できません。
現在、この競合はbusy timeoutを延長したり-1に設定したりしても、待機では解決しません。
同じUPDATEだけを繰り返さず、Aのトランザクションを終了して新しい状態で再判断します。

```sql
-- A
ROLLBACK;
BEGIN;
UPDATE ch8_lock SET val = val + 1 WHERE id = 1;
COMMIT;
SELECT id, val FROM ch8_lock ORDER BY id;
```

最終値は22・21です。
業務で読み取った値を使って次の変更を計算した場合は、新しいトランザクションで読み取りと判断からやり直す必要があります。

<a id="timeout은-보장된-대기-시간이-아닙니다"></a>

## busy timeout

サーバーのデフォルトのTRANSACTION_BUSY_TIMEOUT_MSは30000msで、新しいセッションにコピーされます。
現在のセッションではALTER SESSIONで変更できます。

| 値 | 一時的なロック競合の処理 |
|---|---|
| -1 | キャンセル・接続終了またはロック解放まで待機 |
| 0 | 待機せずbusyを返す |
| 正数 | 指定ミリ秒の範囲内で待機し、処理するかbusyを返す |

スナップショット移行競合のように、再試行で解消できない場合はこのポリシーの例外です。
-1をすべての競合に対する無限再試行と解釈しないでください。
DDL_LOCK_TIMEOUTは別のDDLロック待機設定で、変更してもスナップショット競合は解決しません。

<a id="오류-문자열-하나로-재시도하지-마세요"></a>

## エラーと再試行

メッセージにTRANSACTIONがあることだけで再試行すると、型・制約・権限エラーまで繰り返してしまいます。
ドライバーのエラーコード、診断全文、操作の種類を併せて確認し、再試行可能なロック競合かを区別してください。

明示的なトランザクションで再試行するには、開いている結果セットを閉じてROLLBACKした後、
回数と要求全体の時間に上限を設け、新しいトランザクションで再実行します。
接続消失やCOMMIT応答の消失は別のケースです。
業務キーで処理済みかを確認せず、カウンター増加や注文処理を再実行すると、重複して反映される場合があります。

<a id="실행-중인-작업을-찾아-원인을-좁힙니다"></a>

## 競合の診断

```sql
SELECT id, user_name, user_ip, transaction_busy_timeout_ms
  FROM V$SESSION WHERE closed = 0 ORDER BY id;

SELECT id, sess_id, state, query FROM V$STMT
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%';
```

このクエリはロック所有者を直接対応付けるものではありません。
V$MUTEXもサーバー内部のミューテックス統計であり、業務行のロック一覧ではありません。
接続情報とアプリケーションのBEGIN・終了記録を併せて確認してください。
セッションの強制終了は未コミット業務を取り消す場合があるため、最初の対処にはしないでください。

両方の接続に開いたトランザクションがないことを確認してから、Aでクリーンアップします。

```sql
DROP TABLE ch8_lock;
```

実習用接続A・Bを終了すると、Bに指定したセッション単位のtimeoutも影響しなくなります。
運用では、外部API呼び出しや長い計算をBEGINの外へ移すだけでも、待機の原因を減らせます。
