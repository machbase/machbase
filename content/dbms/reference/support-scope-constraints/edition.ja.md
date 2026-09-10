---
type: docs
title: '16.6.1 Edition別機能サポート表'
weight: 10
toc: true
---

Machbaseは、単一サーバー向けの**Standard Edition**と、複数ノードで水平スケーリングする
**Cluster Edition**を提供します。基本的な時系列機能は共通ですが、拡張性と高可用性の要件に応じて
サポート範囲が異なります。

## Edition別の機能比較

| 機能 | Standard | Cluster | 備考 |
|------|:--------:|:-------:|------|
| **テーブルタイプ** | | | |
| TAGテーブル | O | O | |
| LOGテーブル | O | O | |
| LOOKUPテーブル | O | O | |
| TRANSACTIONテーブル | O | X | Cluster Editionでは非対応 |
| VOLATILEテーブル | O | O | メモリ上のデータのノード・再起動に伴うライフサイクルはデプロイ構成で確認 |
| **データ管理** | | | |
| ROLLUP（基本） | O | O | |
| Custom ROLLUP | O | X | Cluster Editionでは非対応 |
| ROLLUP_REBUILD | O | X | Cluster Editionでは非対応 |
| **バックアップと復旧** | | | |
| 複数の論理データベース | O | X | Standard Edition専用。DBごとのCPU・メモリ・ディスクの物理クォータは提供しない |
| BACKUP DATABASE | O | O | |
| BACKUP TABLE | O | O | |
| MOUNT DATABASE | O | X | Cluster Editionでは非対応 |
| UMOUNT DATABASE | O | X | Cluster Editionでは非対応 |
| machadmin -rによる復元 | O | X | Cluster Editionでは非対応 |
| **拡張性とHA** | | | |
| 水平スケーリング | X | O | Warehouseノードの追加で拡張 |
| HA（高可用性） | X | O | Broker/Warehouseの冗長化 |
| AUTH KEY認証 | O | O | |

## Cluster Editionの制約の概要

Cluster Editionには、単一ノードを中心とするローカルファイル操作とTRANSACTION機能に制約があります。

- **TRANSACTIONテーブル**: 分散環境でACIDトランザクションを保証するTRANSACTIONテーブルは非対応です。トランザクションが必要なデータは外部RDBMSと連携してください。
- **VOLATILEテーブル**: 作成・DMLはサポートしますが、メモリ上のデータはノードローカルで、ノード間では共有しません。接続先Broker・ルーティングとノード再起動によるデータの範囲を検証してください。
- **MOUNT/UMOUNT**: ローカルファイルシステムのバックアップのマウントは、分散環境では非対応です。
- **Custom ROLLUP / ROLLUP_REBUILD**: 分散集計の構造が異なるため、カスタムロールアップの再定義と再構築は非対応です。

## Editionの選択基準

| 要件 | 推奨Edition |
|-----------|-------------|
| 単一サーバーのスループットと保存容量で運用できるワークロード | Standard Edition |
| 単一サーバーを超える水平スケーリングが必要なワークロード | Cluster Edition |
| 高可用性（障害からの自動復旧）が必要 | Cluster Edition |
| TRANSACTIONテーブルまたはMOUNT機能が必要 | Standard Edition |
| リアルタイムの収集量が単一サーバーの容量を超え、ノードの追加が必要 | Cluster Edition |
