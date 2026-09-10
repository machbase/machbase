---
type: docs
title: '16.8.8 sql-generation-rules'
weight: 80
toc: true
---

AIがSQLを生成するときに適用する検証順序です。実際の構文は
[SQLリファレンス](/dbms/reference/sql/)を正式な参照先とします。

## 生成前の確認

1. サーバーバージョンとEditionを確認します。
2. 対象のデータベース、所有者、テーブルタイプ、`DESC`の結果を確認します。
3. [SQL構文辞典](/dbms/reference/sql/syntax/)でステートメントの形式を確認します。
4. [関数辞典](/dbms/reference/sql/functions/)で引数と戻り値の型を確認します。
5. [サポート範囲](/dbms/reference/support-scope-constraints/)でEdition・テーブルの制約を確認します。

## 生成規則

- 他のDBMSのキーワード、関数、ヒント、トランザクション動作を推測で使用しないでください。
- 識別子をパラメーターマーカーで置き換えないでください。
- 時間・距離範囲、DELETE、UPDATEでは、対象となる予定の行を先に参照できるようにします。
- 結果の順序が必要な場合は`ORDER BY`を明示します。
- 変更の例には結果確認と後処理を含めます。

エラーが発生したら構文を任意に変更せず、エラー全文とスキーマを使って
[トラブルシューティング](/dbms/troubleshooting/)の手順で確認します。
