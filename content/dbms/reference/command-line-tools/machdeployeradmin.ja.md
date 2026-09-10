---
type: docs
title: '16.4.9 machdeployeradmin'
weight: 90
toc: true
---

`machdeployeradmin`はMachbase Cluster EditionのDeployerノードを直接管理するツールです。DeployerはCoordinatorの指示に従って各ノードにパッケージを配布し、インストールを行います。

通常は`machcoordinatoradmin`でDeployerを制御することを推奨します。制御できない場合に`machdeployeradmin`を直接使用します。

Cluster Editionパッケージにのみ含まれます。

## オプション一覧

```bash
machdeployeradmin -h
```

| オプション | 説明 |
|------|------|
| `-u`, `--startup` | Deployerプロセスの起動 |
| `-s`, `--shutdown` | Deployerプロセスの正常終了 |
| `-k`, `--kill` | Deployerプロセスの強制停止 |
| `-c`, `--createdb` | Deployerメタデータの作成 |
| `-d`, `--destroydb` | Deployerメタデータの削除 |
| `-e`, `--check` | Deployerプロセスが実行中か確認 |
| `-i`, `--silent` | バナーを表示せずに実行 |

## プロセス管理

### 起動

```bash
machdeployeradmin -u
```

### 正常終了

```bash
machdeployeradmin -s
```

### 強制停止

```bash
machdeployeradmin -k
```

### 実行状態の確認

```bash
machdeployeradmin -e
```

実行中の場合はPIDを表示します。

```
Machbase Deployer is running with pid(29373)!
```

## メタデータ管理

Deployerのメタデータを新規作成します。

```bash
machdeployeradmin -c
```

Deployerのメタデータを削除します。

```bash
machdeployeradmin -d
```

## Deployerの役割

DeployerはCoordinatorの指示に従って次の作業を行います。

- Broker、Warehouse、LookupノードへのMachbaseパッケージの配布とインストール
- ノードの設定ファイルの作成と管理
- ノードの起動/終了指示の転送
- ノードのアップグレードの支援

## 使用例

```bash
# Deployerの初期設定
machdeployeradmin -c
machdeployeradmin -u

# 実行状態の確認
machdeployeradmin -e

# 正常終了
machdeployeradmin -s

# 問題発生時に強制停止
machdeployeradmin -k
```

## 参考

クラスター構成とノード管理の大部分は`machcoordinatoradmin`で行います。`machdeployeradmin`はCoordinatorと通信できない場合やDeployer自体に問題がある場合に直接操作するために使用します。

クラスター管理の詳細は[machcoordinatoradmin](../machcoordinatoradmin/)を参照してください。
