---
type: docs
title: '16.8.3 task-map'
weight: 30
toc: true
---

ユーザーの作業ごとに、正式な参照先の確認順序と完了条件を示します。

| 作業 | 確認順序 | 完了の確認 |
|------|-----------|-----------|
| 初回インストール | [インストール](/dbms/installation-deployment-upgrade/) → [はじめに](/dbms/getting-started/) | サーバー状態、接続、サンプルクエリ |
| テーブルの選択 | [選択基準](/dbms/data-modeling-table-design/) → 該当テーブルの章 | Edition・DML・軸・保持要件を満たすこと |
| 大量データ入力 | [連携の共通概念](/dbms/development-tools-integration/concepts-common/) → SDKページ | 成功/失敗件数とフラッシュの確認 |
| SQLの作成 | [SQLリファレンス](/dbms/reference/sql/) → [サポート範囲](/dbms/reference/support-scope-constraints/) | 実際のスキーマと結果の確認 |
| SDKの選択 | [連携方法の選択](/dbms/development-tools-integration/selection-integration-method/) → [SDKのサポート範囲](/dbms/development-tools-integration/sdk-support-scope/) | サーバー・SDKバージョンとAPIの一致 |
| 性能診断 | [性能改善の進め方](/dbms/performance-tuning/performance-approach/) → 症状別チューニング | 基準値と変更後の測定値の比較 |
| 障害診断 | [トラブルシューティング](/dbms/troubleshooting/) → [エラーコード](/dbms/reference/error-codes/) | 原因、対処、再発防止策の記録 |
| バックアップ・復旧 | [バックアップ・復旧](/dbms/operations-configuration-recovery/backup-restore-mount/) | 復元またはMOUNTによる参照の検証 |

書き込み・削除・再起動を含む作業では、対象と影響範囲を確定してから実行手順を選択します。
