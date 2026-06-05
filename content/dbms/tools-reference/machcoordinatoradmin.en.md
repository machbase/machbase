---
title : 'machcoordinatoradmin'
type : docs
weight: 50
---

Coordinator is a cluster-wide management tool.

Only exists in Cluster Edition Package.

## Options and Features

The options for machcoordinatoradmin are as follows. The functions described in the previous section are omitted.

```
mach@localhost:~$ machcoordinatoradmin -h
```


|Options| Description|
|--|--|
|-u, --startup | Runs the Coordinator process|
|-s, --shutdown | Terminates Coordinator process|
|-k, --kill| Stops Coordinator process|
|-c, --createdb | Creates Coordinator meta|
|-d, --destroydb| Removes Coordinator meta, Deletes the package files in $MACHBASE_COORDINATOR_HOME/package|
|-e, --check | Checks that the Coordinator process is running|
|-i, --silence | Runs without output|
|--configuration[=name] | Outputs keys and values in configuration settings (only certain keys can be output)|
|--configure | Lists the system properties |
|--activate | Switches Cluster status to Service|
|--deactivate | Switches Cluster status to Deactivate|
|--list-package[=package] | Lists information of registered packages (only specific packages can be output)|
|--add-package=package | Adds package|
|--remove-package=package | Deletes package|
|--list-node[=node] | Lists information of nodes (only specific nodes can be output)|
|--add-node=node | Adds node|
|--remove-node=node | Deletes node|
|--attach-node=node | Attaches an existing node to cluster metadata|
|--detach-node=node | Detaches a node from cluster metadata|
|--upgrade-node=node | Upgrades node|
|--startup-node=node | Runs node|
|--shutdown-node=node | Terminates node|
|--kill-node=node | Stops node|
|--startup-lookup | Starts lookup nodes|
|--shutdown-lookup | Stops lookup nodes|
|--set-lookup-master=node | Sets the lookup master node|
|--cluster-status | Outputs each node status of the cluster|
|--cluster-status-full | Outputs of each node status of cluster in detail|
|--verbose | Prints deployer status together in cluster status output|
|--cluster-node | Outputs information of cluster|
|--set-group-state=`[normal | readonly]` | Changes the status of a specific warehouse group|
|--set-warehouse-state=`[normal | scrapped]` | Changes the state of the warehouse node specified by `--node`|
|--force-restore-warehouse=node | Force-restores a scrapped warehouse node|
|--get-host-resource | Outputs host resource information where each node is located|
|--host-resource-enable | Starts collecting Host resource information of each node|
|--host-resource-disable | Stops collecting Host resource information for each node|
|--deactivate-broker=node | Changes the specified node to inactive state|
|--activate-broker=node | Changes the specified node to normal state|
|--snapshot-interval=sec | Sets the snapshot interval|
|--exec-snapshot | Executes a snapshot (requires `--group`)|
|--snapshot-recover=node | Recovers snapshot data for the specified node|
|--exec-sync=node | Executes sync for the specified node|
|--snapshot-clean | Cleans snapshots|

|Additional Options|Description|Required Options|
|--|--|--|
|--file-name=filename | File name| --add-package|
|--port-no=portno | Service port number| --add-node, --attach-node|
|--http-port-no=portno | HTTP administration port number| --add-node, --attach-node|
|--deployer=node | Deployer node name| --add-node|
|--package-name=packagename | Package name to use as the installation source| --add-node, --upgrade-node|
|--home-path=path | Installation path of the current node, based on the Deployer server| --add-node, --attach-node|
|--node-type=`[broker | warehouse | lookup]` | Node type| --add-node, --attach-node |
|--lookup-type=`[master | slave | monitor]` | Lookup node type| --add-node, --attach-node |
|--node=node | Target node name or alias for state changes| --set-warehouse-state|
|--alias=alias | Alias of the node to add or attach| --add-node, --attach-node|
|--dbs-path=path | Database file path for broker/warehouse nodes| --add-node|
|--group=groupname | Group name of the node to install| --add-node, --attach-node, --set-group-state, --exec-snapshot |
|--replication=host:port | host:port to exchange replication| --add-node, --attach-node |
|--no-replicate |Does not use Replication on the node to install |--add-node, --attach-node|
|--primary=host:port | Specifies the node name of the Primary Coordinator when installing the Secondary Coordinator |-u, --startup|
|--host=host | Specifies specific host to output Host resource information| --get-host-resource|
|--metric=`[cpu|memory|disk|network]` | Specifies specific metric to output Host resource information| --get-host-resource|

## Check Running Status

Example:

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

## Create / Delete Meta

Example:

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

## Output Configuration

Syntax:

```
machcoordinatoradmin --configuration[=name]
```

Example:

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

## List the system properties

Syntax

```
machcoordinatoradmin --configure
```

Example

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


## Change Cluster Status

Example:

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

## List Package Information

Syntax:

```
machcoordinatoradmin --list-package[=package]
```

Example:

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

## Add Node, Alias, And DBS_PATH

When adding a broker or warehouse node, specify `--node-type`, `--deployer`, `--package-name`, `--home-path`, and `--port-no` together. If an HTTP administration port is required, specify `--http-port-no`.

Example:

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

When adding or attaching a lookup node, specify `--node-type=lookup` and `--lookup-type` together.

Example:

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

Use `--attach-node` to attach an existing node to cluster metadata. `--attach-node` can use `--alias`, but it cannot use `--dbs-path`.

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

`--alias` can be specified with `--add-node` and `--attach-node`. If it is omitted, the coordinator automatically generates an alias in the form `coordinator-N`, `deployer-N`, `broker-N`, `warehouse-N`, or `lookup-N` according to the node type.

An alias must be at least one character and can contain only letters, digits, `-`, `_`, and `.`. It must be unique across the cluster and must not collide with any real node name.

There is no separate command to change only the alias after registration.

When resolving a command target, the coordinator checks the real node name first and then checks the alias. Therefore aliases can be used with `--startup-node`, `--shutdown-node`, `--kill-node`, `--remove-node`, `--detach-node`, `--upgrade-node`, `--set-lookup-master`, `--set-warehouse-state`, `--force-restore-warehouse`, `--snapshot-recover`, and `--exec-sync`. Status output can display a node as `alias(real-node-name)` when an alias exists.

`--dbs-path` can be used only when adding a broker or warehouse node with `--add-node`. It cannot be used for lookup, coordinator, or deployer nodes, and it cannot be combined with other commands such as `--attach-node` or `--upgrade-node`.

The `--dbs-path` value must start with `/` or `?`. Newlines, tabs, and trailing blanks are not allowed. Values that directly specify system paths such as `/`, `/etc`, `/usr`, `/home`, and `/bin` are rejected. A real data directory under a system path, such as `/home/machbase/warehouse_a1_dbs`, can be specified as a separate directory.

When an absolute path is specified as a custom `DBS_PATH`, the directory must not exist when the node is added. The deployer creates the directory before running `machadmin -c`. If the directory already exists, adding the node fails with `DBS_PATH already exists`. If `--dbs-path` is omitted, the broker/warehouse configuration records the default value `DBS_PATH = ?/dbs`. When a broker/warehouse node is removed with `--remove-node`, an explicit absolute `DBS_PATH` is cleaned up separately from the node home path.


## List Node Information

Syntax:

```
machcoordinatoradmin --list-node[=node]
```

Example:

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


## Output Cluster Node Status

Example:

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


## Output Cluster Information

Example:

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


## Change Group State

Syntax:

```
machcoordinatoradmin --set-group-state=[ normal | readonly ] --group=group
```

Example:

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

## Output Host Resource

Syntax:

```
machcoordinatoradmin --host-resource-enable [--metric=metric] [host=host]
```

Example:

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
