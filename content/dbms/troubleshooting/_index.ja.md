---
type: docs
title: '15. トラブルシューティング'
weight: 150
toc: true
---

Machbase 運用中の問題を、症状確認、原因診断、解決、再発防止の順に説明します。

{{< callout type="info" >}}
問題を分類する前に `machadmin -e` で状態を確認し、`$MACHBASE_HOME/trc/machbase.trc` の
直近のエラーとクライアントの `ERR-XXXXX` コードを記録します。
{{< /callout >}}

## この章の構成

| 順序 | 節 | 内容 |
|-----:|------|------|
| 15.1 | [問題解決へのアプローチ](./troubleshooting/) | 症状収集、診断コマンド、ログとエラーコードの分析 |
| 15.2 | [サーバーと接続の問題](./server-connection/) | 起動、リモート接続、認証エラー |
| 15.3 | [入力とロードの問題](./item/) | Append と CSV インポートのエラー |
| 15.4 | [クエリと性能の問題](./performance/) | 遅いクエリ、空の結果、メモリ、トランザクション競合 |
| 15.5 | [バックアップと復旧の問題](./recovery-backup/) | BACKUP、RESTORE、MOUNT、UMOUNT のエラー |
| 15.6 | [Cluster の問題](./cluster/) | ノード状態と Cluster Edition のエラー |
| 15.7 | [ROLLUP の問題](./rollup/) | 集計遅延、結果の不一致、再構築の判断 |

TAG・LOOKUP の UPDATE・DELETE 条件エラーは、各テーブルの制約・トラブルシューティングを参照してください。

解決後は、原因、対策、確認クエリ、再発防止策を運用記録に残します。
