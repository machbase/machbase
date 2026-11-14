---
type: docs
title: '8.8 制約、エラー、トラブルシューティング'
weight: 80
toc: true
---

他のRDBMSのSQLを移行するときは、名前が似ていることを理由に同じ機能を期待しがちです。
まずEditionと公開構文を確認し、次にデータ制約と同時アクセスの問題を分けて調べてください。

<a id="limitations-rdb-edition"></a>

<a id="지원-범위부터-확인합니다"></a>

## 機能のサポート範囲

TRANSACTIONはStandard Edition専用です。
ClusterではCREATE TABLE・CREATE TRANSACTION TABLE・CREATE TXN TABLEはすべて拒否されます。
LOGはCREATE LOG TABLEで明示する必要があります。

| 要求 | 対応・代替方法 |
|---|---|
| 一般的なSELECT・INSERT・UPDATE・DELETE | サポート。WHEREなしの変更は全行が対象 |
| 単一のPRIMARY KEY | サポート。テーブルごとに1つ |
| 単一・複合UNIQUE INDEX | サポート。テーブル作成後に別途作成 |
| 列の後のUNIQUE・テーブルレベルPRIMARY KEY | 該当する作成構文は未サポート |
| FOREIGN KEY・Trigger・Stored Procedure | 未サポート |
| BEGIN・COMMIT・ROLLBACK | サポート。ネストしたBEGIN・SAVEPOINTは未サポート |
| ADD・DROP・RENAME COLUMN、RENAME TO | サポート条件を確認 |
| MODIFY COLUMN | 未サポート |
| Append | SDK別の公開手段とバッチ境界を確認 |
| TAGのMETADATA・BASETIME・BASEDISTANCE | TRANSACTIONには適用しない |

Clusterで小規模なマスターデータを変更する場合はLOOKUPを検討できますが、明示的なリレーショナルトランザクションの完全な代替ではありません。
元のイベントはLOG・TAG、リレーショナルトランザクションは別のRDBMSなど、要件に応じて分ける必要があります。

<a id="오류별로-확인-대상을-좁힙니다"></a>

## エラー別の診断

| 症状 | 確認箇所 | 次の対処 |
|---|---|---|
| ERR-01418 一意性違反 | PK・UNIQUEキーと既存データ | 入力修正またはUPSERT規則の確認 |
| NOT NULL違反 | 省略・NULL・空文字列・DEFAULT | 入力値と制約を確認 |
| UPDATEの処理が0行 | キーと現在状態の条件 | 対象なし・処理済みなどの業務状態を確認 |
| Resource busy | 他の書き込み、古い読み取りスナップショット、開いたカーソル | 原因に応じて待機・新規トランザクション・カーソル終了 |
| COMMIT・ROLLBACKがbusy | 同じ接続の開いた結果セット | 結果セットを閉じて終了を再試行 |
| エラー後の後続SQLも拒否 | ロールバック専用状態か | ROLLBACK後に新しい処理を開始 |
| DDL失敗 | 参照インデックス・VIEW・アクティブなトランザクション | 依存関係と変更タイミングを調整 |
| マウント先の値が予想と異なる | マウント名・所有者・テーブル名 | 本番データとバックアップデータを区別 |

同じResource busyでも、再試行の方法は異なります。
2接続による詳細な実習は、[ロックとbusy timeout](../locking-conflict-timeout/)を参照してください。
エラー文字列にTRANSACTIONがあることだけを理由に、繰り返し実行しないでください。

<a id="작은-표본에서-제약과-상태-보존을-확인합니다"></a>

## 制約エラーとデータ保持

```sql
CREATE TRANSACTION TABLE ch8_error (
    id    LONG PRIMARY KEY,
    code  VARCHAR(32) NOT NULL,
    value INTEGER
);
CREATE UNIQUE INDEX ch8_error_code ON ch8_error(code);
INSERT INTO ch8_error VALUES (1, 'A', 10);
```

以下は、それぞれ意図的に失敗する任意の実習です。
正常なSQLとまとめず、確認する文だけを実行してください。

```sql
-- PRIMARY KEYの重複
INSERT INTO ch8_error VALUES (1, 'B', 20);
-- UNIQUEの重複
INSERT INTO ch8_error VALUES (2, 'A', 20);
-- 必須値の違反
INSERT INTO ch8_error VALUES (3, NULL, 30);
-- 未サポートのスキーマ変更
ALTER TABLE ch8_error MODIFY COLUMN (code VARCHAR(64));
```

```sql
SELECT id, code, value FROM ch8_error ORDER BY id;
DROP TABLE ch8_error;
```

最後のクエリには(1, A, 10)だけが残ります。
単一文の失敗で状態が保持されることと、BEGIN内で先に成功した文まで自動的に取り消されるわけではないことを区別する必要があります。
[トランザクション](../transaction/)に比較例があります。

<a id="진단-정보는-민감한-값을-가리고-공유하세요"></a>

## 診断情報の収集

サーバーバージョン・Edition、DDLとインデックス、実行SQL、エラーコードとメッセージ全文、実際の影響行数を併せて用意してください。
接続障害では、COMMITの要求・応答時刻と業務キーも必要です。
パスワード・個人情報・機密の業務値を伏せ、再現に必要な最小限のサンプルだけを共有してください。

復旧のために内部保存ファイルを直接変更したり、本番テーブルを再作成したりしないでください。
先に原因と反映状態を確認することが、データ損失の低減につながります。
