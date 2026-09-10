---
type: docs
title: '8.9 トランザクション'
weight: 90
toc: true
---

複数のSQLを実行中に途中の文が失敗すると、それまでの変更も消えたと考えがちです。
しかし、通常の制約エラーでは、失敗した文とトランザクション全体を区別して処理します。
この節では、同じテーブル内の変更でCOMMIT・ROLLBACKの境界を先に確認します。

<a id="design-transaction-rdb"></a>

<a id="begin부터-종료까지-같은-연결을-사용합니다"></a>

## トランザクションの実行

```sql
CREATE TRANSACTION TABLE ch8_tx (
    item_id LONG PRIMARY KEY,
    qty     INTEGER NOT NULL
);
INSERT INTO ch8_tx VALUES (1, 10);
INSERT INTO ch8_tx VALUES (2, 20);

BEGIN;
UPDATE ch8_tx SET qty = qty - 3 WHERE item_id = 1 AND qty >= 3;
UPDATE ch8_tx SET qty = qty + 3 WHERE item_id = 2;
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
ROLLBACK;

SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
```

トランザクション内では7・23、ROLLBACK後は10・20が返されます。
アプリケーションは、2つのUPDATEがそれぞれ想定した1行を処理したことを確認する必要があります。
条件不一致で更新が0行になるのはSQLエラーではないため、データベースが業務失敗を自動判定することはありません。

次は同じ変更を確定する通常の実習です。

```sql
BEGIN;
UPDATE ch8_tx SET qty = qty - 3 WHERE item_id = 1 AND qty >= 3;
UPDATE ch8_tx SET qty = qty + 3 WHERE item_id = 2;
COMMIT;
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
```

確定後の値は7・23です。
公開構文はBEGINであり、BEGIN TRANSACTION、ネストしたBEGIN、SAVEPOINTはサポートしていません。
明示的なトランザクションがなければ、TRANSACTIONのDMLは文単位で処理されます。
ドライバーの自動コミット・トランザクションAPIは別途確認してください。

<a id="문장-오류-뒤에도-앞선-변경은-남아-있을-수-있습니다"></a>

## 文のエラーとロールバック

次はエラー処理を学ぶための流れです。重複INSERTは意図的に失敗します。
SQL実行ツールがエラーで停止した場合は、必ず同じ接続でROLLBACKまで実行してください。

```sql
BEGIN;
UPDATE ch8_tx SET qty = 100 WHERE item_id = 1;
```

```sql
-- 意図的に失敗: item_idの重複
INSERT INTO ch8_tx VALUES (1, 999);
```

```sql
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
ROLLBACK;
SELECT item_id, qty FROM ch8_tx ORDER BY item_id;
```

最初の検索結果は100・23、ROLLBACK後は7・23です。
通常の制約エラーで失敗した文が取り消されても、先に成功した文はトランザクション内に残ります。
業務全体を取り消すには、アプリケーションがROLLBACKを選ぶ必要があります。
すべてのエラー後に続行できるわけではありません。復旧処理でロールバック専用状態になった場合は、ROLLBACKで終了する必要があります。

<a id="truncate도-테이블-타입에-따라-다릅니다"></a>

## TRUNCATEとロールバック

```sql
BEGIN;
TRUNCATE TABLE ch8_tx;
SELECT COUNT(*) AS during_truncate FROM ch8_tx;
ROLLBACK;
SELECT COUNT(*) AS after_rollback FROM ch8_tx;
```

結果は0と2です。
現在のTRANSACTIONのTRUNCATEは全行削除として、明示的トランザクションに含まれます。
LOG・TAGのデータ削除や、CREATE・ALTER・DROPなどのスキーマ変更と混同しないでください。
スキーマ操作は業務トランザクションの外で行うことが運用基準です。

<a id="다른-테이블-조회와-쓰기의-경계가-다릅니다"></a>

## テーブルタイプ別のトランザクション範囲

アクティブなTRANSACTIONトランザクション内でも、LOG・TAG・LOOKUP・VOLATILEの検索と混合結合は許可されます。
一方、これらのタイプへの書き込みを同じトランザクションにまとめることはできません。
検索が許可されても、そのタイプがTRANSACTIONと同じスナップショット・ロールバック保証を得るわけではありません。
元データの収集と業務状態の変更の間の整合性は、別途設計してください。

TRANSACTIONテーブルの読み取りには、他のセッションの未コミット変更が見えないスナップショットを使用します。
BEGIN呼び出し時に、すべてのテーブルで共通の読み取り時点が一括で固定されるとは考えないでください。
読み取りから書き込みへの移行時の競合は、[ロックと再試行](../locking-conflict-timeout/)で説明します。

<a id="여러-테이블과-장애-시-커밋을-구분하세요"></a>

## 複数テーブルのコミットと障害

複数のTRANSACTIONテーブルのDMLをBEGINでまとめ、通常どおりCOMMIT・ROLLBACKすることはできます。
ただし、現在のストレージはテーブルごとにハンドルを使用し、COMMITもハンドルごとに順次処理します。
したがって、コミット中に障害が発生しても、複数テーブル全体が必ず一緒に確定または取り消されるアトミックコミットを保証すると解釈しないでください。

複数テーブルの不可分な処理が必須の業務では、この制限を先に検討してください。
コミット失敗や応答消失後にROLLBACKを送信したことだけで、すべてのテーブルが元に戻ったと判断せず、
業務キーで反映状態を再確認する必要があります。
この節の基本実習を1つのテーブルの2行で構成したのも、このためです。

<a id="열린-결과-집합을-닫고-종료합니다"></a>

## カーソルとトランザクション終了

開いているTRANSACTIONカーソルがある場合、COMMIT・ROLLBACKがResource busyで失敗することがあります。
SDKの結果セット・ステートメントを終了してから、終了文を再実行してください。
接続終了時に未コミット変更はロールバックされますが、接続を失う前にサーバーですでにコミットされたかどうかは、クライアントが別途確認する必要があります。

```sql
DROP TABLE ch8_tx;
```

BEGIN内で外部API呼び出しや長い計算を待たないでください。
トランザクションを短く保ち、失敗時に再実行するのか、先に結果を確認するのかを区別すると、運用中の判断が明確になります。
