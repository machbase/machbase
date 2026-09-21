---
title : 'Cluster Edition Upgrade'
type : docs
weight: 60
---

## Coordinator Upgrade

Coordinator / Deployer must be upgraded manually.

#### Precautions

* During the upgrade, you cannot run commands such as adding / starting / shutting down / deleting nodes.
* DDL and DELETE must not be running. (INSERT, APPEND, and SELECT are allowed.)

#### Coordinator Shutdown


Shutting down the Coordinator / Deployer does not affect INSERT, APPEND, or SELECT on the Broker / Warehouse.

However, while the Coordinator / Deployer is shut down, it cannot detect that a Broker / Warehouse has shut down. (This is normally detected after restart.)

```bash
machcoordinatoradmin --shutdown
```

#### Coordinator Backup (Optional)

Back up the `dbs/` and `conf/` directories in `$MACHBASE_COORDINATOR_HOME`.

#### Coordinator Upgrade

* Use the full package, not the lightweight package.

Extract the package into `$MACHBASE_COORDINATOR_HOME`, overwriting the existing files.

```bash
tar zxvf machbase-ent-new.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME
```

#### Coordinator Startup

```bash
machcoordinatoradmin --startup
```


## Deployer Upgrade

The process is the same as for the Coordinator.

#### Precautions

* During the upgrade, you cannot run commands such as adding / starting / shutting down / deleting nodes.

#### Deployer Shutdown

```bash
machdeployeradmin --shutdown
```

#### Deployer Backup (Optional)

Back up the `dbs/` and `conf/` directories in `$MACHBASE_DEPLOYER_HOME`.

#### Deployer Upgrade

* If MWA or Collector is not running on the host where the Deployer is installed, you can use the lightweight package.

Extract the package into `$MACHBASE_DEPLOYER_HOME`, overwriting the existing files.

```bash
tar zxvf machbase-ent-new.official-LINUX-X86-64-release.tgz -C $MACHBASE_DEPLOYER_HOME
```

#### Deployer Startup

```bash
machdeployeradmin --startup
```


## Package Registration

To upgrade a Broker / Warehouse, register the package in the Coordinator and then run the upgrade.

{{< callout type="info" >}}
We recommend registering the lightweight package.
{{< /callout >}}

First, move the package to the host where `$MACHBASE_COORDINATOR_HOME` is located.

Next, add the package using the following command.

```bash
machcoordinatoradmin --add-package=new_package --file-name=./machbase-ent-new.official-LINUX-X86-64-release-lightweight.tgz
```

|Option|Description|
|--|--|
|--add-package|Specifies the name of the package to add.|
|--file-name|Specifies the path of the package file to add.<br>**Adding a package with the same file name as an existing one causes an error, so check the file name.**|


#### Broker/Warehouse Upgrade

In the Coordinator, run the following command.

## Node Shutdown

```bash
machcoordinatoradmin --shutdown-node=localhost:5656
```

## Node Upgrade

```bash
machcoordinatoradmin --upgrade-node=localhost:5656 --package-name=new_package
```

|Option|Description|
|--|--|
|--upgrade-node|Specifies the name of the node to upgrade.|
|--package-name|Specifies the name of the package to upgrade to.|

* If you upgrade a node without shutting it down, the node is shut down automatically and then upgraded.
  However, for stability, shut down the node explicitly before upgrading.

## Node Startup

```bash
machcoordinatoradmin --startup-node=localhost:5656
```


## Snapshot Failover

Snapshot Failover is available from Machbase 6.5 Cluster Edition.

Snapshot failover records snapshots while the DBMS is in a normal state. When a specific warehouse fails, it performs failover only for the part where the problem occurred, excluding the data covered by the normal snapshot, which enables quick recovery.

#### Snapshot basic concept

For each group in Cluster Edition, a snapshot records the position up to which data is normal across the warehouses in the group.

All data before the snapshot created in the warehouses of a group is in a normal state, and snapshots are recorded per group.

#### How Snapshot Failover Works

When a problem occurs in a specific warehouse, the warehouse changes to the scrapped state and its data must be recovered.

During Snapshot Recovery, the data after the normal snapshot of the failed warehouse is cleared. Then the data after the same baseline snapshot is replicated from a normal warehouse in the same group to the failed warehouse, which completes the recovery.

#### Automatic Snapshot Execution

Automatic snapshot execution is enabled by default, and the snapshot interval is 60 seconds. If a cluster has multiple warehouse groups, one group at a time takes a snapshot at each interval, in turn.

Setting the interval to 0 disables automatic snapshot execution.

A change to the snapshot interval takes effect as soon as the command is executed.

```bash
## Snapshot Interval Setting
machcoordinatoradmin --snapshot-interval=[sec]
  
## Check the current snapshot interval
machcoordinatoradmin --configuration
```

#### Take Snapshot manually

Use the `machcoordinatoradmin` tool with **group_name** to take a snapshot manually.

**group_name** is a preset group name such as group1 or group2.

If a cluster has multiple groups, take a snapshot of each group to get a snapshot of the whole cluster.

```bash
## Manually take a snapshot for group_name
machcoordinatoradmin --exec-snapshot --group='group_name'
```

#### Recover scrapped node based on Snapshot

Recover a scrapped node as follows.

```bash
## Change the group state to readonly
## Prevents group from being changed to normal state in later steps
machcoordinatoradmin --set-group-state=readonly --group=[groupname]
  
## Recover based on Snapshot
machcoordinatoradmin --snapshot-recover=[nodename]
  
## Replicate the latest data after snapshot through replication
## When replication is finished, the state of the warehouse is automatically changed to normal.
machcoordinatoradmin --exec-sync=[nodename]
  
## Change the group state to normal
machcoordinatoradmin --set-group-state=normal --group=[groupname]
```

#### Snapshot-based recovery process of scrapped nodes

When recovering a scrapped node with a snapshot, the following process is performed.

```bash
/* Initial cluster state */
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
  
/* warehouse 0 of group1 dies */
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
  
## Change the group state to readonly
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
  
## Restart the dead warehouse
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
  
## Recovery based on snapshot
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
  
## Replicate the latest data after snapshot through replication
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
  
## Change the group state to normal
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

#### Snapshot-related properties

|Property|Description|Applies to|
|--|--|--|
|GROUP_SNAPSHOT_TIMEOUT_SEC|Timeout for taking a snapshot<br>Default : 60 (sec)<br>Minimum : 0 (wait infinitely)<br>Maximum : uint32_max (sec)|Set in the `machbase.conf` file of each node|
