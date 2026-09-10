---
title : 'Lookup / Broker / Warehouse のインストール'
type: docs
weight: 30
toc: true
---

## Lookup のインストール {#lookup-installation}

Coordinator で Lookup ノードを追加します。複数のノードを登録できます。

配置先サーバーに Deployer を事前にインストールしてください。

Deployer を配置した後は、すべての操作を Coordinator で実行できます。配置先サーバーへ接続して設定する必要はありません。

```bash
# Lookup Master を追加
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5301"  \
        --node-type=lookup --lookup-type=master --deployer="192.168.0.84:5201"      \
        --home-path="/home/machbase/lookup1"
 
 
# Lookup Monitor を追加
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5302"  \
        --node-type=lookup --lookup-type=monitor --deployer="192.168.0.84:5201"         \
        --home-path="/home/machbase/lookupm1"
 
 
# Lookup Slave を追加
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5303"  \
        --node-type=lookup --lookup-type=slave --deployer="192.168.0.84:5201"       \
        --home-path="/home/machbase/lookup3"
 
  
# Lookup を起動
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5301"
 
# Lookup をまとめて起動することも可能
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-lookup
```

| オプション | 説明 | 例 |
|--|--|--|
|--add-node|追加するノードを IP:PORT で指定。PORT は CLUSTER_LINK_PORT_NO の値。|192.168.0.84:5301|
|--node-type|ノードの種類。coordinator、deployer、lookup、broker、warehouse の 5 種類。|lookup|
|--deployer|配置先サーバーの Deployer ノードを指定。|192.168.0.84:5201|
|--lookup-type|Lookup の種類。master、slave、monitor の 3 種類。|master|
|--home-path|machbase アカウントでのインストール先。/home/machbase/lookup を指定。|/home/machbase/lookup|

### インストール条件 {#installation-conditions}

Lookup には Master、Slave、Monitor の 3 種類があり、次の条件に従って配置します。

    1. Lookup Master ノード
        a. 必ず 1 つだけ配置します。
        b. Monitor と Slave より先に配置します。
    2. Lookup Monitor ノード
        a. 少なくとも 1 つ必要です。
        b. 安定した HA のため、各サーバーに 1 つ配置します。
    3. Lookup Slave ノード
        a. HA のため、1 つ以上の配置を推奨します。ない場合、HA を保証できません。


## Lookup の削除 {#delete-lookup}

Coordinator から Lookup ノードを削除します。

```bash
# Lookup を削除
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.84:5301"
```


## Lookup の終了と強制停止 {#shut-downstop-lookup}

Coordinator で Lookup を終了、または強制停止します。

```bash

# Lookup を終了
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-node="192.168.0.84:5301"
 
# Lookup をまとめて終了することも可能
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-lookup
```


## Lookup Master の変更 {#change-lookup-master}

Coordinator で Lookup Master を変更できます。

Slave だけを Master に昇格できます。従来の Master は Slave になります。

```bash
# Lookup Master を変更
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --set-lookup-master="192.168.0.84:5303"
```


## Broker のインストール {#broker-installation}

Coordinator で Broker ノードを追加します。複数の Broker を登録できます。

配置先サーバーに Deployer を事前にインストールしてください。

Deployer の配置後は、すべての操作を Coordinator で実行でき、配置先へ接続して設定する必要はありません。

最初に登録したノードが Leader Broker、追加ノードが Follower Broker になります。

```bash
# Broker を追加
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5401"  \
        --node-type=broker --deployer="192.168.0.84:5201" --port-no="5656"          \
        --home-path="/home/machbase/broker" --package-name=machbase
  
# Broker を起動
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5401"
```

| オプション | 説明 | 例 |
|--|--|--|
|--add-node|追加するノードを IP:PORT で指定。PORT は CLUSTER_LINK_PORT_NO の値。|192.168.0.84:5401|
|--node-type|ノードの種類。coordinator、deployer、lookup、broker、warehouse の 5 種類。|broker|
|--deployer|配置先サーバーの Deployer ノードを指定。|192.168.0.84:5201|
|--port-no|machbased の接続ポート。Broker の既定値は 5656。クライアントや machsql から接続する。|5656|
|--home-path|machbase アカウントでのインストール先。/home/machbase/broker を指定。|/home/machbase/broker|
|--package-name|パッケージ登録時に指定した名前。|machbase|


## Broker の削除 {#delete-broker}

Coordinator から Broker ノードを削除します。

```bash
# Broker を削除
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.84:5401"
```


## Broker の終了と強制停止 {#shut-downstop-broker}

Coordinator から Broker を終了、または強制停止できます。

```bash
# Broker を正常終了
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-node="192.168.0.84:5401"
  
# Broker を強制停止
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --kill-node="192.168.0.84:5401"
```

配置先のサーバーで、プロセスを直接終了、または強制停止することもできます。

```bash
# Broker を正常終了
$MACHBASE_HOME/bin/machadmin -s
  
# Broker を強制停止
$MACHBASE_HOME/bin/machadmin -k
```


## Warehouse のインストール {#warehouse-installation}

Coordinator からアクティブノードとスタンバイノードを配置します。

事前に配置した Deployer を経由してインストールされます。

### Group 1 のインストール {#group-1-installation}

最初の Warehouse Group1 ノードを配置します。

```bash
# group1 の Warehouse を配置
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5501"  \
        --node-type=warehouse --deployer="192.168.0.83:5201" --port-no="5500"       \
        --home-path="/home/machbase/warehouse_g1" --package-name=machbase           \
        --replication="192.168.0.83:5502"  --group="group1" --no-replicate
  
# 配置したノードを起動
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.83:5501"
```

| オプション | 説明 | 例 |
|--|--|--|
|--add-node|追加するノードを IP:PORT で指定。PORT は CLUSTER_LINK_PORT_NO の値。|192.168.0.83:5501|
|--node-type|ノードの種類。coordinator、deployer、lookup、broker、warehouse の 5 種類。|warehouse|
|--deployer|配置先サーバーの Deployer ノードを指定。|192.168.0.83:5201|
|--port-no|machbased の接続ポート。Broker と同じサーバーでは 5656 以外を指定。ここでは 5500 を使用。クライアントや machsql から接続する。|5500|
|--home-path|インストール先。グループは warehouse_g1、g2、g3 のように区別。|/home/machbase/warehouse_g1|
|--package-name|パッケージ登録時に指定した名前。|machbase|
|--replication|Warehouse のレプリケーションマネージャーを IP:PORT で指定。ポートはサービス用ポート + 2。|192.168.0.83:5502|
|--no-replicate|追加時の既存データのレプリケーションを行わない。| |
|--set-group-state|グループの状態を normal（読み書き可能）または readonly（読み取り専用）に設定。| |

### Group 1 へのノード追加 {#add-node-to-group-1}

Warehouse Group1 に別のノードを追加します。

```bash
# group1 に Warehouse を追加
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5501"  \
        --node-type=warehouse --deployer="192.168.0.84:5201" --port-no="5500"       \
        --home-path="/home/machbase/warehouse_g1" --package-name=machbase           \
        --replication="192.168.0.84:5502" --group="group1" --no-replicate
  
# 配置したノードを起動
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5501"
```

| オプション | 説明 | 例 |
|--|--|--|
|--add-node|追加するノードを IP:PORT で指定。PORT は CLUSTER_LINK_PORT_NO の値。|192.168.0.84:5501|
|--node-type|ノードの種類。coordinator、deployer、lookup、broker、warehouse の 5 種類。|warehouse|
|--deployer|配置先サーバーの Deployer ノードを指定。|192.168.0.84:5201|
|--port-no|machbased の接続ポート。Broker と同じサーバーでは 5656 以外を指定。ここでは 5500 を使用。クライアントや machsql から接続する。|5500|
|--home-path|インストール先。グループは warehouse_g1、g2、g3 のように区別。|/home/machbase/warehouse_g1|
|--package-name|パッケージ登録時に指定した名前。|machbase|
|--replication|Warehouse のレプリケーションマネージャーを IP:PORT で指定。ポートはサービス用ポート + 2。|192.168.0.84:5502|
|--group|グループ名。|group1|
|--no-replicate|追加時の既存データのレプリケーションを行わない。| |
|--set-group-state|グループの状態を normal（読み書き可能）または readonly（読み取り専用）に設定。| |

## Group 2 のインストール {#group-2-installation}

2 番目の Warehouse Group2 ノードを配置します。

```bash
# group2 の Warehouse を配置
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5511"  \
        --node-type=warehouse --deployer="192.168.0.84:5201" --port-no="5510"       \
        --home-path="/home/machbase/warehouse_g2" --package-name=machbase           \
        --replication="192.168.0.84:5512"  --group="group2" --no-replicate
  
# 配置したノードを起動
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5511"
```

| オプション | 説明 | 例 |
|--|--|--|
|--add-node|追加するノードを IP:PORT で指定。PORT は CLUSTER_LINK_PORT_NO の値。|192.168.0.84:5511|
|--node-type|ノードの種類。coordinator、deployer、lookup、broker、warehouse の 5 種類。|warehouse|
|--deployer|配置先サーバーの Deployer ノードを指定。|192.168.0.84:5201|
|--port-no|machbased の接続ポート。Broker と同じサーバーでは 5656 以外を指定。ここでは 5510 を使用。クライアントや machsql から接続する。|5510|
|--home-path|インストール先。グループは warehouse_g1、g2、g3 のように区別。|/home/machbase/warehouse_g2|
|--package-name|パッケージ登録時に指定した名前。|machbase|
|--replication|Warehouse のレプリケーションマネージャーを IP:PORT で指定。ポートはサービス用ポート + 2。|192.168.0.84:5512|
|--group|グループ名。|group2|
|--no-replicate|追加時の既存データのレプリケーションを行わない。| |
|--set-group-state|グループの状態を normal（読み書き可能）または readonly（読み取り専用）に設定。| |

### Group 2 へのノード追加 {#add-node-to-group-2}

Warehouse Group2 に別のノードを追加します。

```bash
# group2 に Warehouse を追加
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5511"  \
        --node-type=warehouse --deployer="192.168.0.83:5201" --port-no="5510"       \
        --home-path="/home/machbase/warehouse_g2" --package-name=machbase           \
        --replication="192.168.0.83:5512" --group="group2" --no-replicate
  
# 配置したノードを起動
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.83:5511"
```

| オプション | 説明 | 例 |
|--|--|--|
|--add-node|追加するノードを IP:PORT で指定。PORT は CLUSTER_LINK_PORT_NO の値。|192.168.0.83:5511|
|--node-type|ノードの種類。coordinator、deployer、lookup、broker、warehouse の 5 種類。|warehouse|
|--deployer|配置先サーバーの Deployer ノードを指定。|192.168.0.83:5201|
|--port-no|machbased の接続ポート。Broker と同じサーバーでは 5656 以外を指定。ここでは 5510 を使用。クライアントや machsql から接続する。|5510|
|--home-path|インストール先。グループは warehouse_g1、g2、g3 のように区別。|/home/machbase/warehouse_g2|
|--package-name|パッケージ登録時に指定した名前。|machbase|
|--replication|Warehouse のレプリケーションマネージャーを IP:PORT で指定。ポートはサービス用ポート + 2。|192.168.0.83:5512|
|--group|グループ名。|group2|
|--no-replicate|追加時の既存データのレプリケーションを行わない。| |
|--set-group-state|グループの状態を normal（読み書き可能）または readonly（読み取り専用）に設定。| |


## Warehouse の削除 {#delete-warehouse}

Coordinator から Warehouse ノードを削除します。

```bash
# Warehouse を削除
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.83:5501"
```


## Warehouse の終了と強制停止 {#shut-downstop-warehouse}

Coordinator から Warehouse を終了、または強制停止できます。

```bash
# Warehouse を正常終了
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-node="192.168.0.83:5501"
  
# Warehouse を強制停止
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --kill-node="192.168.0.83:5501"
```

配置先のサーバーで、プロセスを直接終了、または強制停止することもできます。

```bash
# Warehouse を正常終了
$MACHBASE_HOME/bin/machadmin -s
  
# Warehouse を強制停止
$MACHBASE_HOME/bin/machadmin -k
```
