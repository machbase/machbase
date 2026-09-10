---
title : 'Cluster Edition のアップグレード'
type : docs
weight: 60
toc: true
---

## Coordinator のアップグレード {#coordinator-upgrade}

Coordinator と Deployer は手動で更新します。

#### 注意事項 {#precautions}

* 更新中は、ノードの追加、起動、終了、削除などを実行できません。
* DDL と DELETE は実行しないでください。INSERT、APPEND、SELECT は実行できます。

#### Coordinator の停止 {#coordinator-shutdown}


停止しても、Broker/Warehouse の INSERT、APPEND、SELECT には影響しません。

ただし、停止中は Broker/Warehouse の停止を検出できません。再起動後に通常どおり検出します。

```bash
machcoordinatoradmin --shutdown
```

#### Coordinator のバックアップ（任意） {#coordinator-backup-optional}

$MACH_COORDINATOR_HOME の dbs/ と conf/ を保存します。

#### Coordinator の更新 {#coordinator-upgrade-1}

* lightweight ではなく、完全なパッケージを使用してください。

$MACH_COORDINATOR_HOME に展開して上書きします。

```bash
tar zxvf machbase-ent-new.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME
```

#### Coordinator の起動 {#coordinator-startup}

```bash
machcoordinatoradmin --startup
```


## Deployer のアップグレード {#deployer-upgrade}

Coordinator と同じ手順です。

#### 注意事項 {#precautions-1}
 
* 更新中は、ノードの追加、起動、終了、削除などを実行できません。

#### Deployer の停止 {#deployer-shutdown}

```bash
machdeployeradmin --shutdown
```

#### Deployer のバックアップ（任意） {#deployer-backup-optional}

$MACH_DEPLOYER_HOME の dbs/ と conf/ を保存します。

#### Deployer の更新 {#deployer-upgrade-1}

* 同じホストで MWA や Collector を使用していなければ、lightweight パッケージでも更新できます。

$MACH_DEPLOYER_HOME に展開して上書きします。

```bash
tar zxvf machbase-ent-new.official-LINUX-X86-64-release.tgz -C $MACH_DEPLOYER_HOME
```

#### Deployer の起動 {#deployer-startup}

```bash
machdeployeradmin --startup
```


## パッケージの登録 {#package-registration}

Broker/Warehouse を更新するには、Coordinator にパッケージを登録します。

{{< callout type="info" >}}
lightweight 版の登録を推奨します。
{{< /callout >}}

まず、$MACH_COORDINATOR_HOME のあるホストへパッケージを転送します。

次のコマンドで追加します。

```bash
machcoordinatoradmin --add-package=new_package --file-name=./machbase-ent-new.official-LINUX-X86-64-release-lightweight.tgz
```

| オプション | 説明 |
|--|--|
|--add-package|追加するパッケージ名。|
|--file-name|ファイルのパス。**同じファイル名を追加するとエラーになるため、確認してください。**|


#### Broker/Warehouse の更新 {#brokerwarehouse-upgrade}

Coordinator で次の操作を実行します。

## ノードの停止 {#node-shutdown}

```bash
machcoordinatoradmin --shutdown-node=localhost:5656
```

## ノードの更新 {#node-upgrade}

```bash
machcoordinatoradmin --upgrade-node=localhost:5656 --package-name=new_package
```

| オプション | 説明 |
|--|--|
|--upgrade-node|対象ノード名。|
|--package-name|更新先パッケージ名。|

* 稼働中のノードを更新すると、自動的に停止してから更新します。
  ただし、安定した操作のため、事前に明示的に停止してください。

## ノードの起動 {#node-startup}

```bash
machcoordinatoradmin --startup-node=localhost:5656
```


## スナップショットフェイルオーバー {#snapshot-failover}

Machbase 6.5 Cluster Edition で追加された機能です。

正常時のスナップショットを記録し、Warehouse 障害時に正常な部分を除いた差分だけを復旧することで、短時間で回復します。

#### スナップショットの基本概念 {#snapshot-basic-concept}

Warehouse グループごとに、正常なデータの位置を記録します。

グループ内の Warehouse では、スナップショット以前の全データが正常な状態です。記録はグループ単位です。

#### 動作 {#how-snapshot-failover-works}

特定の Warehouse に問題が発生すると scrapped 状態になり、復旧が必要です。

対象 Warehouse の正常なスナップショットを基準に、それ以降のデータを削除します。同じグループの正常な Warehouse から、基準以降のデータを複製して復旧します。

#### 自動実行 {#automatic-snapshot-execution}

既定で有効で、間隔は 60 秒です。複数グループがある場合、間隔ごとに 1 グループずつ順に実行します。

0 にすると、自動実行を無効にします。

間隔の変更は直ちに反映されます。

```bash
#スナップショット間隔を設定
machcoordinatoradmin --snapshot-interval=[sec]
  
#現在のスナップショット間隔を確認
machcoordinatoradmin --configuration
```

#### 手動実行 {#take-snapshot-manually}

machcoordinatoradmin で group_name を指定して実行します。

group_name は group1、group2 などの登録済みの名前です。

複数グループ全体を記録するには、各グループで実行してください。

```bash
#group_name のスナップショットを手動実行
machcoordinatoradmin --exec-snapshot --group='group_name'
```

#### scrapped ノードの復旧 {#recover-scrapped-node-based-on-snapshot}

scrapped のノードを、次のように復旧します。

```bash
#グループを readonly に変更
#後続の処理で normal へ変更されないようにする
machcoordinatoradmin --set-group-state=readonly --group=[groupname]
  
#スナップショットを基に復旧
machcoordinatoradmin --snapshot-recover=[nodename]
  
#スナップショット以降の最新データを複製
#複製完了後、Warehouse は自動的に normal になる
machcoordinatoradmin --exec-sync=[nodename]
  
#グループを normal に変更
machcoordinatoradmin --set-group-state=normal --group=[groupname]
```

#### スナップショットからの復旧処理 {#snapshot-based-recovery-process-of-scrapped-nodes}

復旧時は、次の処理が行われます。

```bash
/* クラスタの初期状態 */
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30420 | group1          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
/* group1 の warehouse 0 が停止 */
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly        | scrapped      | **unknown**   | ----------- |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
#グループを readonly に変更
machcoordinatoradmin --set-group-state=readonly --group=[groupname]
  
kellen@kellen-ku:~$ machcoordinatoradmin --set-group-state=readonly --group=group1
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - 321a012d05.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Group Name: group1
Flag      : 1
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly        | scrapped      | **unknown**   | ----------- |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
#停止した Warehouse を再起動
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly        | scrapped      | scrapped      | ----------- |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
#スナップショットから復旧
machcoordinatoradmin --snapshot-recover=[nodename]
  
kellen@kellen-ku:~$ machcoordinatoradmin --snapshot-recover=localhost:30410
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - 321a012d05.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node-Name: localhost:30410
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly        | scrapped      | scrapped      | ----------- |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
#スナップショット以降の最新データを複製
machcoordinatoradmin --exec-sync=[nodename]
  
kellen@kellen-ku:~$ machcoordinatoradmin --exec-sync=localhost:30410
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - 321a012d05.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node-Name: localhost:30410
Source:
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly        | scrapped      | scrapped      | stopped     |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | stopped     |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly        | sync-standby  | sync-standby  | running     |
| warehouse   | localhost:30420 | group1          | readonly        | sync-active   | sync-active   | running     |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly        | normal        | normal        | stopped     |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | stopped     |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
#グループを normal に変更
machcoordinatoradmin --set-group-state=normal --group=[groupname]
  
kellen@kellen-ku:~$ machcoordinatoradmin --set-group-state=normal --group=group1
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - 321a012d05.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Group Name: group1
Flag      : 0
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | normal          | normal        | normal        | stopped     |
| warehouse   | localhost:30420 | group1          | normal          | normal        | normal        | stopped     |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
```

#### 関連プロパティ {#snapshot-related-properties}

| プロパティ | 説明 | 設定先 |
|--|--|--|
|GROUP_SNAPSHOT_TIMEOUT_SEC|スナップショットのタイムアウト。<br>既定値：60 秒<br>最小値：0（無期限）<br>最大値：uint32_max 秒|各ノードの machbase.conf|
