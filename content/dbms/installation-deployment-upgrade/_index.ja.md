---
type: docs
title: '3. インストール、デプロイ、アップグレード'
weight: 30
toc: true
---

本章ではMachbase DBMS 8.7.0をインストールし、データを入力・検索できる状態か確認します。
新しいサーバーの準備と、既存データを保持するアップグレードでは出発点が異なります。
まず必要な機能とデプロイ環境を決め、状況に合う手順を選択します。

第2章のデータモデルとEditionの違いはインストールにも影響します。TRANSACTIONテーブルやRestore・Mountが
必要ならStandard Editionのサポート範囲を確認します。分散保存とレプリケーションが必要なら、Clusterの
ノードの役割、ネットワーク、障害対応も設計します。

## インストール経路の選択

| Edition | デプロイ構造 | 選択時の確認事項 |
|---|---|---|
| Standard Edition | 1つのDBMSサーバーがSQL処理と保存を実行 | 必要な機能と入力・検索・保管の負荷をサーバーリソースで処理できるか |
| Cluster Edition | Coordinator・Deployer・Lookup・Broker・Warehouseの役割を分離 | 分散グループ、レプリケーション、通信経路、ノード運用手順をまとめて準備できるか |

単一サーバーが小規模データしか扱えないという意味ではありません。必要な保存容量と性能を代表データで
測定して判断します。一方、Clusterもノード数を増やせば全クエリが比例して速くなるわけではありません。
詳しい選択基準は
[Editionの違い](/dbms/core-concepts/concepts-edition/#differences-standard-edition-cluster)を参照してください。

### インストール前に区別する対象

| 対象 | 意味 | 確認例 |
|---|---|---|
| 配布パッケージ | 実行ファイル、ライブラリ、サンプル設定 | バージョン・Edition・OS・CPUアーキテクチャー |
| インストールホーム | 1つのサーバーまたはノードが使用する実行・設定パス | `MACHBASE_HOME`、`conf/machbase.conf` |
| データ保存パス | DBMSが実データを読み書きする場所 | `DBS_PATH`、空き容量、アクセス権 |
| サーバーインスタンス・ノード | その設定で実行されるDBMSプロセス | 起動状態、ログ、接続ポート |
| 論理データベース | 接続後にSQLオブジェクトを作成・使用する空間 | 現在のデータベース、ユーザー・権限・テーブル |

パッケージの展開、新規インスタンスのデータベース作成、サーバー起動、テーブル作成は別々の段階です。
既存データがあるホームに新規インストール用の初期化コマンドを実行しないでください。
インストールホームと実際のデータパスが異なる場合もあるため、バックアップ・アップグレード前に両方を確認します。

SQLの論理データベースはインストールホームとは別の概念です。
複数データベース運用時の選択・作成・権限は
[マルチデータベース運用](/dbms/operations-configuration-recovery/multi-database/)で説明します。

## インストール手順

### Standard Edition

1. [インストール前の準備](./pre-install-preparation/)でパッケージ、サーバーアカウント、リソース、ポートを確認します。
2. OSに合う手順で専用ホームと環境変数を準備します。
   - [Linux — Tarballインストール](./standard-edition/#linux-tarball)
   - [Linux — Dockerインストール](./standard-edition/#linux-docker)
   - [Windows — パッケージインストール](./standard-edition/#windows-package)
3. 設定とデータパスを確認し、別途ライセンスを使用する場合は初回起動前に
   [ライセンスのインストール](./pre-install-preparation/#license)を行います。
4. 選択した手順に従い、新しいデータベースを作成してサーバーを起動します。
5. [インストール検証チェックリスト](./validation-checklist/)でプロセス・ポート・接続・バージョン・
   ライセンスと、少量データの入力・検索を確認します。

コンテナーでもパッケージのバージョン、データボリューム、実行アカウントの書き込み権限を確認します。
コンテナーの起動とDBMSの初期化・起動の関係はイメージにより異なるため、該当する手順に従います。

### Cluster Edition

1. [インストール前の準備](./pre-install-preparation/)と
   [クラスター環境の準備](./cluster-edition/#preparation-environment-cluster-edition)を確認します。
2. ノード別のホスト、ホーム、SQL・管理・ノード間通信のポートとWarehouseレプリケーショングループを決めます。
3. 使用するパッケージとライセンスを準備し、デプロイ方式を選択します。
   - [machclusterctlによるデプロイ](./cluster-edition/#machclusterctl): 設定ファイルでデプロイし、実行計画を確認
   - [手動インストール](./cluster-edition/#manual-machcoordinatoradmin): 管理ツールで段階的に登録・起動
4. ノードの役割に応じた状態とレプリケーション構成を確認し、BrokerへSQLで接続します。
5. [インストール検証チェックリスト](./validation-checklist/)でデータの入力・検索とグループ内の
   レプリケーション状態を区別して確認します。

SQL接続の成功と全レプリカの正常状態は別の確認です。異なるWarehouseグループが必ず同じデータを
持つわけでもありません。障害対応は[Cluster運用](/dbms/operations-configuration-recovery/cluster/)で
続けて確認してください。

## アップグレード

既存システムには[アップグレード](./upgrade/)の手順を使用します。新パッケージの実行可否だけでなく、
データファイル、SQL・SDK、設定・ライセンス、バックアップ・復旧経路の互換性を確認します。
本番設定を新パッケージのサンプルで上書きしたり、実行ファイルを交換しただけで完了と判断したりしないでください。

アップグレード前の基準測定値とバックアップを確保し、隔離環境で復旧に必要な時間も確認します。
旧バージョンへ戻せるかの判断には、バイナリだけでなく旧バージョンで読めるデータと設定が必要です。

## 次のステップ

インストール検証は本番準備の始まりです。まず[クイックスタート](/dbms/getting-started/quick-start/)で
SQLの流れを学び、[テーブルタイプの選択とスキーマ設計](../data-modeling-table-design/)で実データを
モデル化します。本番投入前に専用アカウント、収集エラー処理、保管・バックアップ、代表負荷テスト、
監視メトリクスを準備します。

[観測と診断](/dbms/operations-configuration-recovery/diagnosis-observability/)と
[性能チューニングの進め方](/dbms/performance-tuning/performance-approach/)で、その過程を案内します。
