---
type: docs
title: '16.8.1 エージェント利用ガイド'
weight: 10
toc: true
---

このガイドは、正式なドキュメントを根拠にMachbaseの質問へ回答する手順を定義します。

## 質問の分類

| 質問の種類 | 最初に確認するドキュメント |
|----------|------------------|
| インストール・アップグレード | [インストール、デプロイ、アップグレード](/dbms/installation-deployment-upgrade/) |
| テーブルの選択・設計 | [テーブルタイプの概念と選択](/dbms/data-modeling-table-design/) |
| SQL構文・関数 | [SQLリファレンス](/dbms/reference/sql/) |
| SDK・連携 | [開発とアプリケーション連携](/dbms/development-tools-integration/) |
| サポート可否・制約 | [サポート範囲と制約](/dbms/reference/support-scope-constraints/) |
| 運用・復旧 | [運用、設定、復旧](/dbms/operations-configuration-recovery/) |
| エラー・性能 | [トラブルシューティング](/dbms/troubleshooting/)と[パフォーマンスチューニング](/dbms/performance-tuning/) |

## 回答の作成順序

1. 質問から製品バージョン、Edition、テーブルタイプ、SDK、作業対象を特定します。
2. [用語の区別](../terminology-disambiguation/)でMachbaseでの意味を確認します。
3. [サポート表](../support-matrix/)と[制約インデックス](../constraints-index/)を確認します。
4. 構文・API・運用手順の正規ページで実際の形式を確認します。
5. 例には前提条件、実行、結果確認、後処理を含めます。
6. 不確かな事実は断定せず、確認に必要なバージョン・コマンド・ドキュメントを提示します。

## 根拠とリンク

- 公開の回答にはdocs.machbase.comの正規URLを使用します。
- 内部issue、commit、ソースパスを公開製品の動作を裏付ける根拠の代わりに使用しません。
- ドキュメント間に矛盾があれば、対象バージョンの最新の正式リファレンスと実際のサポート範囲を優先します。

## 安全性

まず参照クエリと診断を提示します。データ削除、サーバー再起動、セッション終了、設定変更、復旧は、
ユーザーの対象と承認範囲を確認せずに実行手順として提示しないでください。
