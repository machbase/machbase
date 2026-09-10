---
type: docs
title: '16.8.11 error-resolution-map'
weight: 110
toc: true
---

エラー番号や原因を推測せず、エラー全文と実行時の状況を保存します。

## 診断順序

1. `ERR-XXXXX`メッセージ全文、SQL・コマンド、発生時刻を収集します。
2. サーバーとSDKのバージョン、Edition、対象のデータベース・所有者・テーブル、接続オプションを記録します。
3. [エラーコード辞典](/dbms/reference/error-codes/)でメッセージを確認します。
4. [トラブルシューティング](/dbms/troubleshooting/)の症状別診断手順を適用します。
5. 対処後、同じ入力と確認クエリで復旧を検証します。

| 症状 | 正式な参照先 |
|------|------|
| サーバー・認証・接続 | [サーバーと接続の問題](/dbms/troubleshooting/server-connection/) |
| 入力・Append・ファイル | [入力とロードの問題](/dbms/troubleshooting/item/) |
| クエリ・性能・メモリ | [クエリと性能の問題](/dbms/troubleshooting/performance/) |
| バックアップ・復旧 | [バックアップと復旧の問題](/dbms/troubleshooting/recovery-backup/) |
| Cluster | [Clusterの問題](/dbms/troubleshooting/cluster/) |

エラーメッセージの一部だけから任意のエラーコードを割り当てたり、問題を再現せずに
破壊的な回避策を推奨したりしないでください。
