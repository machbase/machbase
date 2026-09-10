---
type: docs
title: '8.4 データ入力と変更'
weight: 40
toc: true
aliases:
  - /dbms/rdb-table-usage/sdk-append-scope/
---

UPDATEの成功応答と、注文1件が意図した状態に変わったことは別です。
条件に一致する行がなければ、エラーなしで0行が処理される場合があるためです。
変更前の対象、影響行数、変更後の値を併せて確認する習慣が必要です。

<a id="modeling-rdb-update-delete"></a>

<a id="현재-상태를-조건에-넣어-변경합니다"></a>

## 条件付きUPDATEとDELETE

```sql
CREATE TRANSACTION TABLE ch8_mutation (
    order_id LONG PRIMARY KEY,
    amount   DECIMAL(18,2),
    status   VARCHAR(16),
    ordered  DATETIME
);
INSERT INTO ch8_mutation VALUES (
    1001, 19900.25, 'PENDING', TO_DATE('2026-01-01', 'YYYY-MM-DD'));
INSERT INTO ch8_mutation VALUES (
    1002, 29900.50, 'CANCELLED', TO_DATE('2026-01-02', 'YYYY-MM-DD'));

BEGIN;
UPDATE ch8_mutation SET status = 'SHIPPED'
 WHERE order_id = 1001 AND status = 'PENDING';
SELECT order_id, status FROM ch8_mutation ORDER BY order_id;
COMMIT;
```

1001はSHIPPED、1002はCANCELLEDです。
同じUPDATEを再実行すると、PENDINGではないため影響行数は0です。
アプリケーションはSDKの影響行数を確認し、処理成功・処理済み・対象なしなどを業務規則に合わせて区別する必要があります。

次の削除も、対象件数を確認してからトランザクション内で実行します。

```sql
BEGIN;
SELECT COUNT(*) AS delete_candidates FROM ch8_mutation WHERE status = 'CANCELLED';
DELETE FROM ch8_mutation WHERE status = 'CANCELLED';
SELECT order_id, amount, status FROM ch8_mutation ORDER BY order_id;
COMMIT;
```

対象は1行で、削除後は1001の1行だけが残ります。
WHEREのないUPDATE・DELETEは全行が対象です。
運用では事前SELECTと実際の変更の間に他のセッションがデータを変更し得るため、事前件数だけを成功の根拠にしないでください。

<a id="reference-self-rdb-insert-select"></a>

<a id="복사할-컬럼과-자기-참조-범위를-명시합니다"></a>

## INSERT SELECTと自己参照

```sql
CREATE TRANSACTION TABLE ch8_archive (
    order_id LONG PRIMARY KEY,
    amount   DECIMAL(18,2),
    status   VARCHAR(16),
    ordered  DATETIME
);
INSERT INTO ch8_archive(order_id, amount, status, ordered)
SELECT order_id, amount, status, ordered FROM ch8_mutation
 WHERE ordered < TO_DATE('2026-02-01', 'YYYY-MM-DD');

INSERT INTO ch8_mutation(order_id, amount, status, ordered)
SELECT order_id + 10000, amount, status, ordered FROM ch8_mutation
 WHERE order_id = 1001;

SELECT order_id FROM ch8_archive ORDER BY order_id;
SELECT order_id FROM ch8_mutation ORDER BY order_id;
```

アーカイブには1001、元テーブルには1001・11001があります。
自身のテーブルから読んだ結果を再挿入しても、この例では新しい行を無限に再入力することはありません。
ただし、キーを変えずにコピーすると一意性違反が起こり得ます。
出力先の列数と型を合わせ、コピー範囲を再実行可能な単位に分けてください。

通常の制約エラーと接続障害を同じ失敗として扱わないでください。
文の失敗はBEGIN全体を自動的にロールバックせず、コミット応答を失った場合は反映の有無を再検索する必要があります。
[トランザクション](../transaction/)で処理境界を説明します。

```sql
DROP TABLE ch8_archive;
DROP TABLE ch8_mutation;
```

<a id="unsupported-rejected-rdb-append-api"></a>
<a id="support-scope-rdb-sdk"></a>

<a id="대량-입력에서는-배치의-실제-경계를-확인합니다"></a>

## 大量取り込みとバッチ境界

TRANSACTIONもAppend APIをサポートしています。
古いファイル名やアンカーにreject・unsupportedが残っていることを理由に、現在も未サポートと判断しないでください。
言語別の公開APIは、[SDK機能のサポート範囲](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-append)を基準に選択します。

| 取り込み方式 | 確認基準 |
|---|---|
| SQL INSERT・プリペアド実行 | 文ごとのエラーと明示的トランザクション境界 |
| ドライバーのbatch | 実際の送信単位、部分成功、自動コミット |
| Append | SDKバッファ・サーバーバッチの境界、エラーコールバック・戻り値 |
| machloader | マッピングと失敗行、処理区間の記録 |

現在のSQLCLI SQLAppendBatch処理は、別のアクティブなトランザクションがなければ、サーバーバッチをトランザクションとして扱います。
この処理の制約エラーの回帰検証では、失敗したバッチ全体がロールバックされます。
これを、すべてのSDKの論理バッチ、複数回のflush、Appenderの全ライフサイクルにわたる単一のアトミック操作と解釈しないでください。

AUTO_INCREMENTとDECIMALの取り込みでは、[SQLCLIとODBC](/dbms/development-tools-integration/cli-odbc/)の専用規則も確認してください。
Appendプロトコルの到着時刻フィールドが、TRANSACTIONにLOGの自動時間列を作るわけではありません。

導入前には、正常行に重複キー・NULLエラーの行を1行混ぜ、成功・失敗件数と保存結果を確認してください。
ネットワークエラー後の再送では、コミット済みデータの重複処理も考慮する必要があります。
