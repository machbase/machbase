---
type: docs
title: '16.4.7 machclusterctl'
weight: 70
toc: true
---

`machclusterctl`は、Machbase Cluster Editionのクラスター全体を単一のコマンドで管理するツールです。YAML設定の検証、新規インストール、稼働中の構成変更、アップグレード、起動/終了、状態確認などを行います。

## 主なコマンド

| コマンド | 説明 |
|------|------|
| `validate` | `cluster.yaml`の検証 |
| `install` | `cluster.yaml`に基づく新規クラスターのインストール |
| `apply` | 稼働中のクラスターに設定変更を反映 |
| `upgrade` | パッケージのアップグレード（`--online`、`--full-stop`） |
| `export` | 稼働中のクラスター構成をフラットなYAMLでエクスポート |
| `status` | クラスター全ノードの状態確認 |
| `connect` | Broker/Warehouseのエイリアスへ`machsql`で接続 |
| `start` | クラスター全ノードの起動 |
| `stop` | クラスター全ノードの正常終了 |
| `destroy` | クラスターの削除（データを含む） |

## 使用方法

```bash
machclusterctl <command> [options]
```

## コマンドの詳細

### validate

YAML設定ファイルを検証します。

```bash
machclusterctl validate -f cluster.yaml
```

### install

YAML設定ファイルを読み込み、新規クラスターをインストールします。

```bash
machclusterctl install -f cluster.yaml
```

### apply

稼働中のクラスターに設定変更を反映します。

```bash
machclusterctl apply -f cluster.yaml
```

### upgrade

パッケージをアップグレードします。

```bash
machclusterctl upgrade --online broker
machclusterctl upgrade --full-stop
```

### start

Coordinator → Deployer → Broker → Warehouseの順にクラスター全体を起動します。

```bash
machclusterctl start
machclusterctl start -f cluster.yaml
```

### stop

クラスター全体を正常終了します。

```bash
machclusterctl stop
```

### destroy

クラスターを完全に削除します。データベースファイルも削除するため、注意して使用してください。

```bash
machclusterctl destroy
```

### status

クラスターの各ノードの現在の状態を表示します。

```bash
machclusterctl status
```

### connect

Brokerノードへ`machsql`で接続します。

```bash
machclusterctl connect
```

### export

現在のクラスター構成をYAMLファイルへエクスポートします。

```bash
machclusterctl export -o cluster_backup.yaml
```

## YAML設定ファイルの構造

`machclusterctl validate`、`install`、`apply`で使用するYAML設定ファイルの基本構造です。

```yaml
cluster:
  coordinator:
    host: 192.168.0.32
    port: 5101
    http_port: 5102
    home: /home/machbase/coordinator1

  deployer:
    - host: 192.168.0.32
      port: 5201
      home: /home/machbase/deployer1

  broker:
    - host: 192.168.0.32
      port: 5301
      http_port: 5302
      home: /home/machbase/broker1
      service_port: 5757

  warehouse:
    - group: Group1
      host: 192.168.0.32
      port: 5401
      http_port: 5402
      home: /home/machbase/warehouse_a1
      service_port: 5400
```

## オプション

| オプション | 説明 |
|------|------|
| `-f`, `--file` | クラスター設定YAMLファイルのパス |
| `-s`, `--silent` | 進行ログの出力を削減 |
| `-v`, `--verbose` | 詳細な進行ログを表示 |
| `--node` | `start`/`stop`の対象ノードのエイリアスを指定 |
| `--type` | `start`/`stop`の対象ノードタイプを指定 |
| `-o`, `--output` | 出力ファイルのパス（`export`で使用） |
| `-h`, `--help` | ヘルプを表示 |

## 使用例

```bash
# YAMLの検証
machclusterctl validate -f my_cluster.yaml

# クラスターの新規インストール
machclusterctl install -f my_cluster.yaml

# 稼働中のクラスターに変更を反映
machclusterctl apply -f my_cluster.yaml

# クラスターの起動
machclusterctl start

# 特定タイプまたはノードのみ停止/起動
machclusterctl stop --node broker-1
machclusterctl start --type warehouse

# 状態確認
machclusterctl status

# Brokerに接続してSQLを実行
machclusterctl connect

# クラスターの終了
machclusterctl stop

# 設定のエクスポート
machclusterctl export -o cluster_config_backup.yaml
```
