---
type: docs
title: '16.4.8 machcoordinatoradmin'
weight: 80
toc: true
---

`machcoordinatoradmin`はMachbase Cluster EditionのCoordinatorノードを管理し、クラスター構成を制御するツールです。Cluster Editionパッケージにのみ含まれます。

## オプション一覧

```bash
machcoordinatoradmin -h
```

### 基本管理オプション

| オプション | 説明 |
|------|------|
| `-u`, `--startup` | Coordinatorプロセスの起動 |
| `-s`, `--shutdown` | Coordinatorプロセスの正常終了 |
| `-k`, `--kill` | Coordinatorプロセスの強制停止 |
| `-c`, `--createdb` | Coordinatorメタデータの作成 |
| `-d`, `--destroydb` | Coordinatorのメタデータとパッケージファイルの削除 |
| `-e`, `--check` | Coordinatorプロセスが実行中か確認 |
| `-i`, `--silent` | バナーを表示せずに実行 |
| `--home-path=path` | Machbaseホームパスの指定 |

### 設定参照オプション

| オプション | 説明 |
|------|------|
| `--configuration[=name]` | 設定のキーと値を表示。特定キーのみの表示も可能 |
| `--configure` | システムプロパティ一覧をすべて表示 |

### クラスター状態の制御

| オプション | 説明 |
|------|------|
| `--activate` | クラスター状態をServiceへ変更 |
| `--deactivate` | クラスター状態をDeactivateへ変更 |
| `--cluster-status` | クラスターの各ノードの状態概要を表示 |
| `--cluster-status-full` | クラスターの各ノードの詳細状態を表示 |
| `--cluster-node` | クラスター情報を表示 |
| `--verbose` | 状態表示にDeployerの状態を含める |

### パッケージ管理

| オプション | 説明 |
|------|------|
| `--list-package[=package]` | 登録済みパッケージ一覧を表示。特定パッケージのみの表示も可能 |
| `--add-package=package` | パッケージの追加 |
| `--remove-package=package` | パッケージの削除 |

### ノード管理

| オプション | 説明 |
|------|------|
| `--list-node[=node]` | ノード情報一覧を表示 |
| `--add-node=node` | ノードの追加 |
| `--remove-node=node` | ノードの削除 |
| `--attach-node=node` | 既存ノードをクラスターのメタデータに接続 |
| `--detach-node=node` | ノードをクラスターのメタデータから切り離す |
| `--upgrade-node=node` | ノードのアップグレード |
| `--startup-node=node` | 特定ノードの起動 |
| `--shutdown-node=node` | 特定ノードの正常終了 |
| `--kill-node=node` | 特定ノードの強制停止 |

### Lookup ノード管理

| オプション | 説明 |
|------|------|
| `--startup-lookup` | Lookupノードの起動 |
| `--shutdown-lookup` | Lookupノードの終了 |
| `--set-lookup-master=node` | Lookup masterノードの指定 |

### Warehouseのグループ/状態管理

| オプション | 説明 |
|------|------|
| `--set-group-state=[normal\|readonly]` | 特定Warehouseグループの状態変更 |
| `--set-warehouse-state=[normal\|scrapped]` | `--node`で指定したWarehouseノードの状態変更 |
| `--force-restore-warehouse=node` | scrapped状態のWarehouseノードを強制復旧 |

### Broker管理

| オプション | 説明 |
|------|------|
| `--deactivate-broker=node` | 指定ノードをinactive状態へ変更 |
| `--activate-broker=node` | 指定ノードをnormal状態へ変更 |

### スナップショット管理

| オプション | 説明 |
|------|------|
| `--snapshot-interval=sec` | スナップショット実行間隔（秒）の設定 |
| `--exec-snapshot` | スナップショットの即時実行（`--group`が必要） |
| `--snapshot-recover=node` | 指定ノードをスナップショットから復旧 |
| `--exec-sync=node` | 指定ノードの同期を実行 |
| `--snapshot-clean` | スナップショットの整理 |

### ホストリソース監視

| オプション | 説明 |
|------|------|
| `--get-host-resource` | 各ノードのホストリソース情報を表示 |
| `--host-resource-enable` | ホストリソース情報の収集開始 |
| `--host-resource-disable` | ホストリソース情報の収集停止 |

### 追加オプション（他のオプションと併用）

| 追加オプション | 必須オプション | 説明 |
|----------|----------|------|
| `--file-name=filename` | `--add-package` | パッケージファイル名 |
| `--port-no=portno` | `--add-node`, `--attach-node` | サービスポート番号 |
| `--http-admin-port=portno` | Coordinator/Deployer `--add-node`, `--attach-node` | 管理RESTポート番号 |
| `--deployer=node` | `--add-node` | Deployerノード名 |
| `--package-name=name` | `--add-node`, `--upgrade-node` | インストール元のパッケージ名 |
| `--home-path=path` | `--add-node`, `--attach-node` | ノードのインストール先 |
| `--node-type=[broker\|warehouse\|lookup]` | `--add-node`, `--attach-node` | ノードタイプ |
| `--lookup-type=[master\|slave\|monitor]` | `--add-node`, `--attach-node` | Lookup ノードタイプ |
| `--node=node` | `--set-warehouse-state` | 状態変更の対象ノード |
| `--alias=alias` | `--add-node`, `--attach-node` | ノードのエイリアス |
| `--dbs-path=path` | `--add-node` (Broker/Warehouse) | データベースファイルのパス |
| `--group=groupname` | `--add-node`, `--attach-node`, `--set-group-state`, `--exec-snapshot` | ノードのグループ名 |
| `--replication=host:port` | `--add-node`, `--attach-node` | レプリケーション先のhost:port |
| `--no-replicate` | `--add-node`, `--attach-node` | レプリケーションを無効化 |
| `--primary=host:port` | `-u`, `--startup` | Secondary CoordinatorのPrimaryを指定 |
| `--host=host` | `--get-host-resource` | 特定ホストを指定 |
| `--metric=[cpu\|memory\|disk\|network]` | `--get-host-resource` | 表示するメトリクスの種類 |

## 使用例

### 実行状態の確認

```bash
machcoordinatoradmin -e
```

### クラスターの状態確認

```bash
machcoordinatoradmin --cluster-status
machcoordinatoradmin --cluster-status-full
```

### クラスターの有効化/無効化

```bash
machcoordinatoradmin --activate
machcoordinatoradmin --deactivate
```

### Warehouse ノードの追加

```bash
machcoordinatoradmin \
  --add-node=192.168.0.32:5401 \
  --node-type=warehouse \
  --deployer=192.168.0.32:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/warehouse_a1 \
  --port-no=5400 \
  --group=Group1 \
  --alias=warehouse-a1 \
  --dbs-path=/data/machbase/warehouse_a1_dbs
```

### ノード一覧の確認

```bash
machcoordinatoradmin --list-node
machcoordinatoradmin --list-node=192.168.0.32:5401
```

### Warehouseグループを読み取り専用に変更

```bash
machcoordinatoradmin --set-group-state=readonly --group=Group1
```

### 設定の参照

```bash
machcoordinatoradmin --configuration
machcoordinatoradmin --configuration=decision
```

### ホストリソース監視

```bash
machcoordinatoradmin --host-resource-enable
machcoordinatoradmin --get-host-resource
machcoordinatoradmin --get-host-resource --metric=cpu
machcoordinatoradmin --get-host-resource --host=192.168.0.33
machcoordinatoradmin --host-resource-disable
```
