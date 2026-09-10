---
type: docs
title: '16.6 サポート範囲と制約'
weight: 80
toc: true
aliases:
  - /dbms/reference/support-scope-constraints/limitations-functions/
---

MachbaseのEdition別、テーブルタイプ別、SDK別の機能サポート範囲と既知の制約をまとめた
クイックリファレンスです。動作の仕組みや使用例は各機能の章を参照し、特定環境でのサポート可否は
このセクションで確認してください。

## このセクションの構成

| ページ | 内容 |
|--------|------|
| [Edition別機能サポート表](./edition/) | Standard EditionとCluster Editionの機能比較 |
| [テーブルタイプ別機能サポート表](./table-types-type/) | TAG / LOG / LOOKUP / VOLATILE / TRANSACTIONのサポート機能 |
| [SDK別機能サポート表](/dbms/development-tools-integration/sdk-support-scope/) | JDBC、Python、Go、.NET、Node.jsのサポート範囲 |
| [ROLLUPのサポート範囲](./rollup/) | Edition別・テーブルタイプ別のROLLUPサポート範囲 |
| [バックアップ/マウントサポート表](./backup-mount/) | BACKUP / MOUNT機能のEdition別サポート可否 |
| [権限別機能サポート表](./privileges/) | データベース権限とテーブル権限の一覧 |
| [TRANSACTION機能サポート表](./rdb/) | TRANSACTIONテーブルのサポートSQL機能と制約 |
| [バージョンと互換性](./compatibility-version/) | アップグレード時の注意事項、対応OS/プラットフォーム |
| [サーバーとSDKの互換性](./compatibility-xma-protocol/) | サーバーとSDKのバージョンの組み合わせ別のサポート範囲 |
| [LOOKUP SQL/JSONサポート表](./lookup-sql-json/) | LOOKUPテーブルのSQL/JSONサポート状況と制約 |
| [TAGデータUPDATEサポート表](./tag-data-update/) | TAG UPDATEの条件と対象列のサポート状況 |

サポート表にない内部オブジェクト・フラグ・プロトコルの動作に依存しないでください。
SDKの機能はサーバーとクライアントのバージョンを併せて確認します。機能別のエラー診断は
[トラブルシューティング](/dbms/troubleshooting/)を参照してください。

## 表記規則

<a id="공통-판단-원칙"></a>

このセクションのサポート表では、次の記号を使用します。

| 記号 | 意味 |
|:----:|------|
| O | 完全にサポート |
| X | 非対応 |
| △ | 一部をサポート、または制約あり |
