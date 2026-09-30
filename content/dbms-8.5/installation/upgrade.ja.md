---
title : 'Cluster Edition のアップグレード'
type : docs
weight: 60
toc: true
---

## Coordinator のアップグレード {#coordinator-upgrade}

Coordinator / Deployer は手動でアップグレードする必要があります。

#### 注意事項 {#precautions}

* アップグレード中は、ノードの追加、起動、停止、削除などのコマンドを実行できません。
* DDL と DELETE は実行中であってはいけません（INSERT、APPEND、SELECT は実行しても問題ありません）。

#### Coordinator の停止 {#coordinator-shutdown}


Coordinator / Deployer を停止しても、Broker / Warehouse の INSERT、APPEND、SELECT には影響しません。

ただし、Coordinator / Deployer の停止中は、Broker / Warehouse が停止してもそれを検出できません（通常は再起動後に検出します）。

```bash
machcoordinatoradmin --shutdown
```

#### Coordinator のバックアップ（任意） {#coordinator-backup-optional}

`$MACHBASE_COORDINATOR_HOME` にある `dbs/` と `conf/` ディレクトリをバックアップします。

#### Coordinator のアップグレード {#coordinator-upgrade-1}

* 軽量パッケージではなく、フルパッケージを使用してください。

パッケージを `$MACHBASE_COORDINATOR_HOME` に展開し、既存のファイルを上書きします。

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

* アップグレード中は、ノードの追加、起動、停止、削除などのコマンドを実行できません。

#### Deployer の停止 {#deployer-shutdown}

```bash
machdeployeradmin --shutdown
```

#### Deployer のバックアップ（任意） {#deployer-backup-optional}

`$MACHBASE_DEPLOYER_HOME` にある `dbs/` と `conf/` ディレクトリをバックアップします。

#### Deployer のアップグレード {#deployer-upgrade-1}

* Deployer をインストールしたホストで MWA や Collector を実行していなければ、軽量パッケージを使用できます。

パッケージを `$MACHBASE_DEPLOYER_HOME` に展開し、既存のファイルを上書きします。

```bash
tar zxvf machbase-ent-new.official-LINUX-X86-64-release.tgz -C $MACHBASE_DEPLOYER_HOME
```

#### Deployer の起動 {#deployer-startup}

```bash
machdeployeradmin --startup
```


## パッケージの登録 {#package-registration}

Broker / Warehouse をアップグレードするには、Coordinator にパッケージを登録してからアップグレードを実行します。

{{< callout type="info" >}}
軽量パッケージの登録を推奨します。
{{< /callout >}}

まず、`$MACHBASE_COORDINATOR_HOME` のあるホストへパッケージを移動します。

次に、以下のコマンドでパッケージを追加します。

```bash
machcoordinatoradmin --add-package=new_package --file-name=./machbase-ent-new.official-LINUX-X86-64-release-lightweight.tgz
```

| オプション | 説明 |
|--|--|
|--add-package|追加するパッケージの名前を指定します。|
|--file-name|追加するパッケージファイルのパスを指定します。<br>**既存のパッケージと同じファイル名のパッケージを追加するとエラーになるため、ファイル名を確認してください。**|


#### Broker/Warehouse のアップグレード {#brokerwarehouse-upgrade}

Coordinator で次のコマンドを実行します。

## ノードの停止 {#node-shutdown}

```bash
machcoordinatoradmin --shutdown-node=localhost:5656
```

## ノードのアップグレード {#node-upgrade}

```bash
machcoordinatoradmin --upgrade-node=localhost:5656 --package-name=new_package
```

| オプション | 説明 |
|--|--|
|--upgrade-node|アップグレードするノードの名前を指定します。|
|--package-name|アップグレードに使用するパッケージの名前を指定します。|

* ノードを停止せずにアップグレードすると、ノードを自動的に停止してからアップグレードします。
  ただし、安定性のため、アップグレード前にノードを明示的に停止してください。

## ノードの起動 {#node-startup}

```bash
machcoordinatoradmin --startup-node=localhost:5656
```


## スナップショットフェイルオーバー {#snapshot-failover}

スナップショットフェイルオーバーは Machbase 6.5 Cluster Edition から使用できます。

スナップショットフェイルオーバーは、DBMS が正常な状態のときにスナップショットを記録しておき、特定の Warehouse に障害が発生した場合に、正常なスナップショットまでのデータを除き、問題が発生した部分だけをフェイルオーバーして迅速に復旧する機能です。

#### スナップショットの基本概念 {#snapshot-basic-concept}

Cluster Edition のグループごとに、グループ内の Warehouse のデータがどこまで正常かを示す位置を記録します。

グループ内の Warehouse で作成されたスナップショットより前のデータは、すべて正常な状態です。スナップショットはグループ単位で記録されます。

#### スナップショットフェイルオーバーの動作 {#how-snapshot-failover-works}

特定の Warehouse に問題が発生すると、その Warehouse は scrapped 状態になり、データの復旧が必要になります。

Snapshot Recovery を実行すると、問題が発生した Warehouse で正常なスナップショットより後のデータを削除します。続いて、同じグループの正常な Warehouse から基準スナップショット以降のデータを問題の Warehouse へ複製し、復旧が完了します。

#### スナップショットの自動実行 {#automatic-snapshot-execution}

スナップショットの自動実行は既定で有効で、実行間隔は 60 秒です。クラスターに複数の Warehouse グループがある場合は、間隔ごとに 1 グループずつ順番にスナップショットを実行します。

実行間隔を 0 にすると、自動実行は無効になります。

スナップショット間隔の設定は、コマンドを実行するとすぐに反映されます。

```bash
#スナップショット間隔を設定
machcoordinatoradmin --snapshot-interval=[sec]
  
#現在のスナップショット間隔を確認
machcoordinatoradmin --configuration
```

#### スナップショットの手動実行 {#take-snapshot-manually}

`machcoordinatoradmin` ツールで **group_name** を指定し、スナップショットを手動で実行します。

**group_name** は group1、group2 のようにあらかじめ決められたグループ名です。

クラスターに複数のグループがある場合、クラスター全体のスナップショットを取るには、グループごとにスナップショットを実行する必要があります。

```bash
#group_name のスナップショットを手動実行
machcoordinatoradmin --exec-snapshot --group='group_name'
```

#### スナップショットによる scrapped ノードの復旧 {#recover-scrapped-node-based-on-snapshot}

scrapped ノードが発生した場合は、次のように復旧します。

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

#### スナップショットによる scrapped ノードの復旧過程 {#snapshot-based-recovery-process-of-scrapped-nodes}

スナップショットで scrapped ノードを復旧すると、次の処理が行われます。

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

#### スナップショット関連プロパティ {#snapshot-related-properties}

| プロパティ | 説明 | 設定先 |
|--|--|--|
|GROUP_SNAPSHOT_TIMEOUT_SEC|スナップショット実行時のタイムアウト<br>既定値：60（秒）<br>最小値：0（無期限に待機）<br>最大値：uint32_max（秒）|各ノードの `machbase.conf` ファイルに設定|
