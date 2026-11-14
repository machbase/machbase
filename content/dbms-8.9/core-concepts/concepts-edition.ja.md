---
type: docs
title: '2.4 Edition の概念'
weight: 40
toc: true
---

Edition はデプロイ構成と機能のサポート範囲を決定します。Standard は単一サーバーから始める構成、
Cluster は複数ノードで保存と処理を分担する構成です。現在のデータサイズだけでなく、必要な SQL 機能、
増加率、障害対応、運用体制を考慮して選びます。

<a id="differences-standard-edition-cluster"></a>

## Standard Edition と Cluster Edition の違い

### Standard Edition

1台の DBMS サーバーで SQL 処理とデータ保存を行います。分散ノード間のデプロイや通信を管理する
必要がなく、開発や単一サーバー運用の開始に適しています。TRANSACTION テーブルや Restore・Mount など、
Standard 専用機能が必要かも確認します。

単一サーバー構成だからといって、データ量が小さい必要はありません。入力量、クエリ負荷、保持期間が
サーバーの CPU・メモリ・ストレージの容量に収まるかを測定して判断します。

### Cluster Edition

Coordinator、Deployer、Broker、Warehouse、Lookup の各ノードが役割を分担します。

| ノードタイプ | 役割 |
|---|---|
| Coordinator | クラスターメタデータとノード状態の管理 |
| Deployer | パッケージの配布とノード管理 |
| Broker | アプリケーションの SQL 接続とクエリ分配 |
| Warehouse | 時系列データの保存とクエリ実行 |
| Lookup | クラスターの参照データ処理 |

通常の SQL アプリケーションは Broker に接続します。管理ツールの接続先とポートは役割別に異なるため、
SQL 接続先と管理接続先を区別します。

複数の Warehouse グループにデータを分散することと、同じグループ内でデータを複製することは目的が異なります。
分散は容量・スループットの拡張、複製は障害対応に使います。ノード数、複製状態、クライアントの再接続、
障害時の運用手順をまとめて設計する必要があります。

### 機能のサポート差

| 確認項目 | Standard Edition | Cluster Edition |
|---|---|---|
| 主なデプロイ構成 | 単一 DBMS サーバー | 役割を分担する複数ノード |
| TRANSACTION テーブル | サポート | 非サポート |
| Restore・Mount | サポート | 非サポート |
| 容量・処理の拡張 | サーバーリソースとストレージ構成の拡張 | 分散グループとノード構成の拡張 |
| 障害対応の設計 | バックアップ・復旧手順、サーバー運用計画 | ノード・グループの複製と状態、接続・復旧手順 |

LOG・TAG・LOOKUP・VOLATILE、ROLLUP、Retention などの共通機能も、DML・DDL・運用の細かい制約が
すべて同じとは限りません。全体のサポート範囲は
[Edition 別サポート](../../reference/support-scope-constraints/edition/)と
[テーブルタイプ別サポート](../../reference/support-scope-constraints/table-types-type/)で確認します。

### 選択基準

1. 必須機能を確認します。TRANSACTION や Restore・Mount が必要なら、まず Standard のサポート範囲を確認します。
2. 代表的な入力とクエリを実行します。データ型、同時接続数、クエリ範囲、保持期間を実業務に近づけ、
   単一サーバーの余力を確認します。
3. データ増加率と障害要件を考慮します。単一サーバーを超える分散が必要なら、Cluster のネットワーク、
   複製、ノード運用コストも評価します。
4. 障害シナリオを試験します。ノード監視があることと無停止で復旧できることは別です。
   復旧時間とアプリケーションの再接続・再試行動作を確認します。

運用中の Edition 変更も、サーバー数を増やすだけの作業ではありません。使用中の SQL・SDK と、
データ移行・バックアップ・復旧方法の互換性を先に確認します。

## 関連文書

- [ストレージと実行の構造](../storage-execution-architecture/)で処理の流れを説明します。
- [インストール・デプロイ・アップグレード](../../installation-deployment-upgrade/)でデプロイ手順を説明します。
- [バージョンと互換性](../../reference/support-scope-constraints/compatibility-version/)でバージョン別のサポート範囲を確認します。
- [関係型業務モデルと時系列モデル](../concepts/#differences-rdbms)でデータモデルの選択基準を説明します。
