---
title: 'Coordinator / Deployer のインストールとパッケージの追加'
type: docs
weight: 20
toc: true
---

## Coordinator のインストール {#installing-coordinator}

### 環境設定 {#configuration}

machbase アカウントでログインし、その権限で実行します。

インストール先とパス情報を設定します。

```bash
# .bashrc を編集
export MACHBASE_COORDINATOR_HOME=~/coordinator
export MACHBASE_DEPLOYER_HOME=~/deployer
export MACHBASE_HOME=~/coordinator
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH

# 変更を反映
source .bashrc
```

### ディレクトリの作成と展開 {#create-and-unzip-directory}

専用ディレクトリを作成し、パッケージを展開します。

```bash
# ディレクトリを作成
mkdir $MACHBASE_COORDINATOR_HOME

# 展開
tar zxvf machbase-ent-x.y.z.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME
```

### ポート設定とサービスの開始 {#port-configuration-and-service-activation}

machbase.conf でポートを設定し、サービスを開始します。

```bash
# machbase.conf でポートを設定
cd $MACHBASE_COORDINATOR_HOME/conf
vi machbase.conf
CLUSTER_LINK_HOST       = 192.168.0.83 # 追加するノードの IP
CLUSTER_LINK_PORT_NO    = 5101
HTTP_ADMIN_PORT         = 5102

# メタデータを作成し、サービスを開始
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -c
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -u
```

### ノードの登録と確認 {#node-registration-and-verification}

Coordinator ノードを追加して確認します。

```bash
# ノードを登録
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5101" --node-type=coordinator

# ノードを確認
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

| オプション | 説明 | 例 |
| ----------- | ------------------------------------------------------------------------------------------------------- | ----------------- |
| --add-node | 追加するノードを IP:PORT で指定。PORT は CLUSTER_LINK_PORT_NO の値。 | 192.168.0.83:5101 |
| --node-type | ノードの種類。coordinator / deployer / lookup / broker / warehouse の 5 種類。 | coordinator |

## Coordinator の削除 {#delete-coordinator}

配置先のサーバーに接続し、Coordinator プロセスを正常終了してから、ディレクトリを削除します。

```bash
# Coordinator を終了し、ディレクトリを削除
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -s
rm -rf $MACHBASE_COORDINATOR_HOME
```

## Secondary Coordinator のインストール {#secondary-coordinator-installation}

Primary Coordinator に加えて Secondary Coordinator を配置する場合は、次の点に注意してください。

- Secondary の起動前に、Primary で Secondary を add-node します。
- Secondary の起動時に、--primary で Primary を指定します。
- Secondary に Primary を add-node してはいけません。

この手順を守らないと、Secondary が Primary として動作します。

各コマンドは指定されたノードの環境で実行します。同じホストに配置する場合、Secondary のインストール先は Primary と別にし、その作業時の `MACHBASE_COORDINATOR_HOME` と `MACHBASE_HOME` を Secondary のディレクトリへ設定してください。Primary での登録操作には Primary の環境を使用します。

### ディレクトリの作成と展開 {#create-and-unzip-directory-1}

専用ディレクトリを作成し、パッケージを展開します。

```bash

# ディレクトリを作成
mkdir $MACHBASE_COORDINATOR_HOME

# 展開
tar zxvf machbase-ent-x.y.z.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME
```

### ポートの設定 {#port-settings}

machbase.conf でポートだけを設定します。**この段階でサービスを起動すると、Primary として動作してしまいます。**

```bash
# machbase.conf でポートを設定
cd $MACHBASE_COORDINATOR_HOME/conf
vi machbase.conf
CLUSTER_LINK_HOST       = 192.168.0.83 # 追加するノードの IP
CLUSTER_LINK_PORT_NO    = 5111
HTTP_ADMIN_PORT         = 5112
```

### ノードの登録と確認 {#node-registration-and-verification-1}

**Primary Coordinator で** Secondary ノードを追加して確認します。

```bash
# ノードを登録
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5111" --node-type=coordinator

# ノードを確認
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

### サービスの開始 {#run-service}

Secondary を開始します。起動時に **--primary** で Primary Coordinator を指定してください。

```bash
# メタデータを作成し、サービスを開始
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -c
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -u --primary="192.168.0.83:5101"
```

## Secondary Coordinator の削除 {#delete-secondary-coordinator}

Primary から Secondary の登録を削除してから、Secondary を正常終了します。

```bash
# Primary の環境で実行：Secondary の登録を削除
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.83:5111"

# Secondary の環境で実行：正常終了し、Secondary のディレクトリを削除
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -s
rm -rf $MACHBASE_COORDINATOR_HOME

# Primary の環境に戻って実行：ノードを確認
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

| オプション | 説明 | 例 |
| ------------- | ---------------------------------------------------------------------------------------------------------------- | ----------------- |
| --remove-node | 削除するノードを IP:PORT で指定。PORT は CLUSTER_LINK_PORT_NO の値。 | 192.168.0.83:5111 |

## Deployer のインストール {#deployer-installation}

- **補足**
  Broker と Warehouse を配置するすべてのホスト（サーバー）に、事前に Deployer をインストールしてください。

### 環境設定 {#configuration-1}

インストール先とパス情報を設定します。

```bash
# .bashrc を編集
export MACHBASE_DEPLOYER_HOME=~/deployer
export MACHBASE_HOME=~/deployer
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH

# 変更を反映
source .bashrc
```

### ディレクトリの作成と展開 {#create-and-unzip-directory-2}

専用ディレクトリを作成し、パッケージを展開します。

```bash
# ディレクトリを作成
mkdir $MACHBASE_DEPLOYER_HOME

# 展開
tar zxvf machbase-ent-x.y.z.official-LINUX-X86-64-release.tgz -C $MACHBASE_DEPLOYER_HOME
```

### ポート設定とサービスの開始 {#port-configuration-and-service-activation-1}

machbase.conf でポートを設定し、サービスを開始します。

```bash
# machbase.conf でポートを設定
cd $MACHBASE_DEPLOYER_HOME/conf
vi machbase.conf
CLUSTER_LINK_HOST       = 192.168.0.84
CLUSTER_LINK_PORT_NO    = 5201
HTTP_ADMIN_PORT         = 5202

# メタデータを作成し、サービスを開始
$MACHBASE_DEPLOYER_HOME/bin/machdeployeradmin -c
$MACHBASE_DEPLOYER_HOME/bin/machdeployeradmin -u
```

### ノードの登録と確認 {#node-registration-and-verification-2}

- **注意**
  この操作は Coordinator ノードで実行します。

Deployer ノードを追加して確認します。

```bash
# ノードを登録
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5201" --node-type=deployer

# ノードを確認
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

| オプション | 説明 | 例 |
| ----------- | ------------------------------------------------------------------------------------------------------- | ----------------- |
| --add-node | 追加するノードを IP:PORT で指定。PORT は CLUSTER_LINK_PORT_NO の値。 | 192.168.0.84:5201 |
| --node-type | ノードの種類。coordinator / deployer / lookup / broker / warehouse の 5 種類。 | deployer |

## Deployer の削除 {#delete-deployer}

Coordinator から Deployer の登録を削除し、配置先サーバーで Deployer プロセスを正常終了します。

```bash
# ノードを削除
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.84:5201"

# Deployer を終了し、ディレクトリを削除
$MACHBASE_DEPLOYER_HOME/bin/machdeployeradmin -s
rm -rf $MACHBASE_DEPLOYER_HOME

# ノードを確認
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

## パッケージの追加 {#add-package}

Broker と Warehouse 用のパッケージを Coordinator に登録します。MWA を含まない lightweight 版を使用します。

```bash
# 配置用パッケージを登録
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-package=machbase \
    --file-name="/home/machbase/machbase-ent-x.y.z.official-LINUX-X86-64-release-lightweight.tgz"
```

| オプション | 説明 | 例 |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| --add-package | 登録するパッケージ名。 | machbase |
| --file-name | パッケージの絶対パスとファイル名。Broker/Warehouse 専用なので、MWA を含まない lightweight パッケージを指定。 | /home/machbase/machbase-ent-x.y.z.official-LINUX-X86-64-release-lightweight.tgz |

## パッケージの削除 {#delete-package}

Coordinator に登録したパッケージを削除します。

```bash
# 登録パッケージを削除
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-package=machbase
```
