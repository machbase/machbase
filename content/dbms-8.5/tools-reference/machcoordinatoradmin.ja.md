---
title : 'machcoordinatoradmin'
type : docs
weight: 50
toc: true
---

Coordinator はクラスタ全体を管理します。

このツールは Cluster Edition にのみ含まれます。

## オプションと機能 {#options-and-features}

machcoordinatoradmin のオプションを示します。前節で説明した機能は省略しています。

```
mach@localhost:~$ machcoordinatoradmin -h
```


| オプション | 説明 |
|--|--|
|-u, --startup | Coordinator を起動 |
|-s, --shutdown | Coordinator を正常終了 |
|-k, --kill| Coordinator を強制停止 |
|-c, --createdb | Coordinator のメタデータを作成 |
|-d, --destroydb| メタデータと $MACHBASE_COORDINATOR_HOME/package のパッケージを削除 |
|-e, --check | 稼働状態を確認 |
|-i, --silent | バナーを非表示 |
|--configuration[=name] | 設定のキーと値を表示（キーの絞り込み可能） |
|--configure | システムプロパティの一覧 |
|--activate | クラスタを Service 状態に変更 |
|--deactivate | クラスタを Deactivate 状態に変更 |
|--list-package[=package] | 登録パッケージ情報を表示（絞り込み可能） |
|--add-package=package | パッケージを追加 |
|--remove-package=package | パッケージを削除 |
|--list-node[=node] | ノード情報を表示（絞り込み可能） |
|`--add-node`=node | ノードを追加 |
|`--remove-node`=node | ノードを削除 |
|`--attach-node`=node | 既存ノードをクラスタメタデータに接続 |
|`--detach-node`=node | ノードをクラスタメタデータから切り離す |
|`--upgrade-node`=node | ノードをアップグレード |
|`--startup-node`=node | ノードを起動 |
|`--shutdown-node`=node | ノードを正常終了 |
|`--kill-node`=node | ノードを強制停止 |
|--startup-lookup | Lookup ノードを起動 |
|--shutdown-lookup | Lookup ノードを停止 |
|`--set-lookup-master`=node | Lookup Master を設定 |
|--cluster-status | 各ノードの状態を表示 |
|--cluster-status-full | 各ノードの詳細な状態を表示 |
|--verbose | クラスタ状態に Deployer も表示 |
|--cluster-node | クラスタ情報を表示 |
|--set-group-state=`[normal \| readonly]` | 指定 Warehouse グループの状態を変更 |
|`--set-warehouse-state`=`[normal \| scrapped]` | `--node` で指定した Warehouse の状態を変更 |
|`--force-restore-warehouse`=node | scrapped の Warehouse を強制復元 |
|--get-host-resource | 各ノードのホストリソース情報を表示 |
|--host-resource-enable | ホストリソース情報の収集を開始 |
|--host-resource-disable | ホストリソース情報の収集を停止 |
|--deactivate-broker=node | Broker を非アクティブに変更 |
|--activate-broker=node | Broker を通常状態に変更 |
|--snapshot-interval=sec | スナップショット間隔を設定 |
|--exec-snapshot | スナップショットを実行（`--group` が必要） |
|`--snapshot-recover`=node | 指定ノードのスナップショットデータを復元 |
|`--exec-sync`=node | 指定ノードの同期を実行 |
|--snapshot-clean | スナップショットを削除 |

| 追加オプション | 説明 | 併用するオプション |
|--|--|--|
|--file-name=filename | ファイル名 | --add-package|
|`--port-no`=portno | サービスポート | `--add-node`, `--attach-node`|
|`--http-port-no`=portno | HTTP 管理ポート | `--add-node`, `--attach-node`|
|`--deployer`=node | Deployer ノード名 | `--add-node`|
|`--package-name`=packagename | インストール元のパッケージ名 | `--add-node`, `--upgrade-node`|
|`--home-path`=path | Deployer サーバーを基準とした配置先 | `--add-node`, `--attach-node`|
|`--node-type`=`[broker \| warehouse \| lookup]` | ノードの種類 | `--add-node`, `--attach-node` |
|`--lookup-type`=`[master \| slave \| monitor]` | Lookup の種類 | `--add-node`, `--attach-node` |
|`--node`=node | 状態変更対象のノード名または別名 | `--set-warehouse-state`|
|`--alias`=alias | 追加または接続するノードの別名 | `--add-node`, `--attach-node`|
|`--dbs-path`=path | Broker/Warehouse のデータベースファイルパス | `--add-node`|
|`--group`=groupname | 配置先グループ名 | `--add-node`, `--attach-node`, --set-group-state, --exec-snapshot |
|--replication=host:port | レプリケーション用 host:port | `--add-node`, `--attach-node` |
|--no-replicate | 配置するノードでレプリケーションを使用しない |`--add-node`, `--attach-node`|
|--primary=host:port | Secondary 起動時の Primary Coordinator |-u, --startup|
|--host=host | 情報を表示するホストを指定 | --get-host-resource|
|--metric=`[cpu\|memory\|disk\|network]` | 情報を表示するメトリクスを指定 | --get-host-resource|

## 稼働状態の確認 {#check-running-status}

例：

```
mach@localhost:~$ machcoordinatoradmin -e
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Machbase Coordinator is running with pid(29245)!
```

## メタデータの作成と削除 {#create--delete-meta}

例：

```
mach@localhost:~$ machcoordinatoradmin -c
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Coordinator metadata created successfully.

mach@localhost:~$ machcoordinatoradmin -d
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Coordinator metadata destroyed successfully.
```

## 設定の表示 {#output-configuration}

構文：

```
machcoordinatoradmin --configuration[=name]
```

例：

```
mach@localhost:~$ machcoordinatoradmin --configuration
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Name  : CLUSTER
Value : 3

Name  : DECISION
Value : ON

Name  : HOST-RESOURCE
Value : OFF

mach@localhost:~$ machcoordinatoradmin --configuration=decision
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : DECISION
             Value : ON
            Format : text/plain
```

## システムプロパティの一覧 {#list-the-system-properties}

構文

```
machcoordinatoradmin --configure
```

例

```
mach@localhost:~$ machcoordinatoradmin --configure

CLUSTER_LINK_HOST=192.168.0.30
CLUSTER_LINK_PORT_NO=36110
CLUSTER_LINK_THREAD_COUNT=16
CLUSTER_LINK_MAX_LISTEN=512
CLUSTER_LINK_MAX_POLL=4096
CLUSTER_LINK_ACCEPT_TIMEOUT=5000000
CLUSTER_LINK_CHECK_INTERVAL=1000000
CLUSTER_LINK_CONNECT_RETRY_TIMEOUT=60000000
CLUSTER_LINK_CONNECT_TIMEOUT=5000000
CLUSTER_LINK_HANDSHAKE_TIMEOUT=5000000
CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL=1000000
CLUSTER_LINK_LONG_WAIT_INTERVAL=1000000
CLUSTER_LINK_RECEIVE_TIMEOUT=5000000
CLUSTER_LINK_REQUEST_TIMEOUT=60000000
CLUSTER_LINK_SEND_TIMEOUT=5000000
CLUSTER_LINK_SESSION_TIMEOUT=3600000000
CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST=0
CLUSTER_LINK_BUFFER_SIZE=33554432
..
..
```


## クラスタ状態の変更 {#change-cluster-status}

例：

```
mach@localhost:~$ machcoordinatoradmin --activate
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : CLUSTER
             Value : 3
            Format : text/plain


mach@localhost:~$ machcoordinatoradmin --deactivate
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : CLUSTER
             Value : 0
            Format : text/plain
```

## パッケージ情報の一覧 {#list-package-information}

構文：

```
machcoordinatoradmin --list-package[=package]
```

例：

```
mach@localhost:~$ machcoordinatoradmin --list-package
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Package Name : machbase
File Name    : machbase-cluster-6bab497c9.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64630670 bytes

Package Name : machbase2
File Name    : machbase-cluster-e3c0717.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64677030 bytes


mach@localhost:~$ machcoordinatoradmin --list-package=machbase
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Package Name : machbase
File Name    : machbase-cluster-6bab497c9.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64630670 bytes
```

## ノード、別名、`DBS_PATH` の指定 {#add-node-alias-and-dbs_path}

Broker または Warehouse の追加時は、`--node-type`、`--deployer`、`--package-name`、`--home-path`、`--port-no` を併用します。HTTP 管理ポートが必要なら `--http-port-no` も指定します。

例：

```
machcoordinatoradmin \
  --add-node=192.168.0.32:5401 \
  --node-type=warehouse \
  --deployer=192.168.0.32:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/warehouse_a1 \
  --port-no=5400 \
  --http-port-no=5402 \
  --group=Group1 \
  --alias=warehouse-a1 \
  --dbs-path=/data/machbase/warehouse_a1_dbs
```

Lookup の追加または接続には、`--node-type=lookup` と `--lookup-type` を併用します。

例：

```
machcoordinatoradmin \
  --add-node=192.168.0.32:5601 \
  --node-type=lookup \
  --lookup-type=master \
  --deployer=192.168.0.32:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/lookup1 \
  --alias=lookup-master-1
```

既存のノードをクラスタメタデータに接続するには `--attach-node` を使用します。`--alias` は併用できますが、`--dbs-path` は使えません。

```
machcoordinatoradmin \
  --attach-node=192.168.0.32:5401 \
  --node-type=warehouse \
  --home-path=/home/machbase/warehouse_a1 \
  --port-no=5400 \
  --http-port-no=5402 \
  --group=Group1 \
  --alias=warehouse-a1
```

`--alias` は `--add-node` と `--attach-node` に指定できます。省略すると種類に応じて `coordinator-N`、`deployer-N`、`broker-N`、`warehouse-N`、`lookup-N` の形式で自動生成します。

別名は 1 文字以上で、英字、数字、`-`、`_`、`.` だけを使用できます。クラスタ内で一意であり、実際のノード名とも重複してはいけません。

登録後に別名だけを変更するコマンドはありません。

コマンド対象は、実ノード名、別名の順に解決されます。そのため、`--startup-node`、`--shutdown-node`、`--kill-node`、`--remove-node`、`--detach-node`、`--upgrade-node`、`--set-lookup-master`、`--set-warehouse-state`、`--force-restore-warehouse`、`--snapshot-recover`、`--exec-sync` に別名を指定できます。状態表示では `alias(real-node-name)` 形式になる場合があります。

`--dbs-path` は `--add-node` で Broker または Warehouse を追加する場合のみ使用できます。Lookup、Coordinator、Deployer や、`--attach-node`、`--upgrade-node` などとの併用はできません。

`--dbs-path` は `/` または `?` で始めます。改行、タブ、末尾の空白は使用できません。`/`、`/etc`、`/usr`、`/home`、`/bin` などのシステムパスそのものは拒否されます。`/home/machbase/warehouse_a1_dbs` のような、その配下の実データ用ディレクトリは指定できます。

絶対パスを指定する場合、追加時点でディレクトリが存在してはいけません。Deployer が `machadmin -c` の前に作成します。既存の場合は `DBS_PATH already exists` で失敗します。省略すると、Broker/Warehouse の設定に `DBS_PATH = ?/dbs` が記録されます。`--remove-node` で削除すると、明示した絶対パスの `DBS_PATH` もホームパスとは別に削除されます。


## ノード情報の一覧 {#list-node-information}

構文：

```
machcoordinatoradmin --list-node[=node]
```

例：

```
mach@localhost:~$  machcoordinatoradmin --list-node
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node Name             : 192.168.0.32:5101
Node Type             : coordinator
HTTP Admin Port       : 5102
Group Name            : Coordinator
Desired State         : primary
Actual State          : primary
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497590
Last Modify Time      : 421020408
Last Response Elapsed : 1006148

Node Name             : 192.168.0.32:5201
Node Type             : deployer
Group Name            : Deployer
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497594
Last Modify Time      : 404915419
Last Response Elapsed : 1006128

Node Name             : 192.168.0.32:5301
Node Type             : broker
Port Number           : 5757
Http Port             : 5302
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/machbase/broker1
Group Name            : Broker
Desired State         : leader
Actual State          : leader
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497544
Last Modify Time      : 353606480
Last Response Elapsed : 1006157

Node Name             : 192.168.0.32:5401
Node Type             : warehouse
Port Number           : 5400
Http Port             : 5402
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/machbase/warehouse_a1
Group Name            : Group1
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497556
Last Modify Time      : 332480933
Last Response Elapsed : 1006160

mach@localhost:~$  machcoordinatoradmin --list-node=192.168.0.32:5401
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node Name             : 192.168.0.32:5401
Node Type             : warehouse
Port Number           : 5400
Http Port             : 5402
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/cumulus/warehouse_a1
Group Name            : Group1
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 648879
Last Modify Time      : 419153148
Last Response Elapsed : 1005962
```


## クラスタノードの状態表示 {#output-cluster-node-status}

例：

```
mach@localhost:~$ machcoordinatoradmin --cluster-status
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary      |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal       |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader       |
| warehouse   | 192.168.0.32:5401 | Group1            | normal            | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+

mach@localhost:~$ machcoordinatoradmin --cluster-status-full
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+-------------------------------+-------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |    Desired & Actual State     |  RP State   |
+-------------+-------------------+-------------------+-------------------+-------------------------------+-------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary       | primary       | ----------- |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal        | normal        | ----------- |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader        | leader        | ----------- |
| warehouse   | 192.168.0.32:5401 | Group1            | normal            | normal        | normal        | ----------- |
+-------------+-------------------+-------------------+-------------------+-------------------------------
```


## クラスタ情報の表示 {#output-cluster-information}

例：

```
mach@localhost:~$ machcoordinatoradmin --cluster-node
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Token Pid      : 29245
Token Time     : 1553153902646178
Modify Time    : 1553154010296715
Modify Count   : 8
Cluster Status : Service
Broker         : 192.168.0.32:5301
Warehouse      : 192.168.0.32:5401
```


## グループ状態の変更 {#change-group-state}

構文：

```
machcoordinatoradmin --set-group-state=[ normal | readonly ] --group=group
```

例：

```
mach@localhost:~$ machcoordinatoradmin --set-group-state=readonly --group=Group1
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Group Name: Group1
Flag      : 1

mach@localhost:~$ machcoordinatoradmin --cluster-status
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary      |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal       |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader       |
| warehouse   | 192.168.0.32:5401 | Group1            | readonly          | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+
```

## ホストリソースの表示 {#output-host-resource}

構文：

```
machcoordinatoradmin --host-resource-enable [--metric=metric] [host=host]
```

例：

```
mach@localhost:~$ machcoordinatoradmin --host-resource-enable
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : HOST-RESOURCE
             Value : ON
            Format : text/plain

mach@localhost:~$ machcoordinatoradmin --get-host-resource
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.32
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 14.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 99.1%
      Virtual Memory Utilization  : 98.6%
   Network Info :
      Receive Bytes(per second)    : 42809
      Receive Packets(per second)  : 337
      Transmit Bytes(per second)   : 42885
      Transmit Packets(per second) : 332
   Disk Info :
      /dev/sda1 : 87.4%
         |-> 192.168.0.32:5101   /home/cumulus/coordinator1
         |-> 192.168.0.32:5301   /home/cumulus/broker1
         |-> 192.168.0.32:5401   /home/cumulus/warehouse_a1
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 2.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 46.9%
      Virtual Memory Utilization  : 22.8%
   Network Info :
      Receive Bytes(per second)    : 12336
      Receive Packets(per second)  : 103
      Transmit Bytes(per second)   : 13500
      Transmit Packets(per second) : 103
   Disk Info :
      /dev/sda1 : 64.2%
         |-> 192.168.0.33:5101   /home/cumulus/coordinator2
         |-> 192.168.0.33:5401   /home/cumulus/warehouse_a2

mach@localhost:~$ machcoordinatoradmin --get-host-resource --metric=cpu
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.32
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 13.9%
      CPU IOWait Ratio    : 0.0%
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 1.9%
      CPU IOWait Ratio    : 0.0%

mach@localhost:~$ machcoordinatoradmin --get-host-resource --host=192.168.0.33
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 2.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 46.9%
      Virtual Memory Utilization  : 22.8%
   Network Info :
      Receive Bytes(per second)    : 12588
      Receive Packets(per second)  : 106
      Transmit Bytes(per second)   : 13330
      Transmit Packets(per second) : 100
   Disk Info :
      /dev/sda1 : 64.2%
         |-> 192.168.0.33:5101   /home/cumulus/coordinator2
         |-> 192.168.0.33:5401   /home/cumulus/warehouse_a2

mach@localhost:~$ machcoordinatoradmin --host-resource-disable
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : HOST-RESOURCE
             Value : OFF
            Format : text/plain
```
