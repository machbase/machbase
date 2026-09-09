---
type: docs
title: '16.4.8 machcoordinatoradmin'
weight: 80
toc: true
---

`machcoordinatoradmin` manages Coordinator nodes and controls cluster configuration in Machbase
Cluster Edition. It is included only in the Cluster Edition package.

## Options

```bash
machcoordinatoradmin -h
```

### Basic Administration

| Option | Description |
|------|------|
| `-u`, `--startup` | Start the Coordinator process |
| `-s`, `--shutdown` | Shut down the Coordinator process gracefully |
| `-k`, `--kill` | Force the Coordinator process to stop |
| `-c`, `--createdb` | Create Coordinator metadata |
| `-d`, `--destroydb` | Delete Coordinator metadata and package files |
| `-e`, `--check` | Check whether the Coordinator process is running |
| `-i`, `--silent` | Run without a banner |
| `--home-path=path` | Set the Machbase home path |

### Configuration Queries

| Option | Description |
|------|------|
| `--configuration[=name]` | Display configuration keys and values, optionally for one key |
| `--configure` | Display all system properties |

### Cluster State Control

| Option | Description |
|------|------|
| `--activate` | Change cluster state to Service |
| `--deactivate` | Change cluster state to Deactivate |
| `--cluster-status` | Display a summary of each cluster node's status |
| `--cluster-status-full` | Display detailed status for each cluster node |
| `--cluster-node` | Display cluster information |
| `--verbose` | Include Deployer status in status output |

### Package Management

| Option | Description |
|------|------|
| `--list-package[=package]` | List registered packages, optionally for one package |
| `--add-package=package` | Add a package |
| `--remove-package=package` | Remove a package |

### Node Management

| Option | Description |
|------|------|
| `--list-node[=node]` | List node information |
| `--add-node=node` | Add a node |
| `--remove-node=node` | Remove a node |
| `--attach-node=node` | Attach an existing node to cluster metadata |
| `--detach-node=node` | Detach a node from cluster metadata |
| `--upgrade-node=node` | Upgrade a node |
| `--startup-node=node` | Start a specific node |
| `--shutdown-node=node` | Shut down a specific node gracefully |
| `--kill-node=node` | Force a specific node to stop |

### Lookup Node Management

| Option | Description |
|------|------|
| `--startup-lookup` | Start Lookup nodes |
| `--shutdown-lookup` | Stop Lookup nodes |
| `--set-lookup-master=node` | Set the Lookup master node |

### Warehouse Group and State Management

| Option | Description |
|------|------|
| `--set-group-state=[normal\|readonly]` | Change a Warehouse group's state |
| `--set-warehouse-state=[normal\|scrapped]` | Change the state of the Warehouse specified by `--node` |
| `--force-restore-warehouse=node` | Force recovery of a scrapped Warehouse |

### Broker Management

| Option | Description |
|------|------|
| `--deactivate-broker=node` | Set the specified node to inactive |
| `--activate-broker=node` | Set the specified node to normal |

### Snapshot Management

| Option | Description |
|------|------|
| `--snapshot-interval=sec` | Set the snapshot interval in seconds |
| `--exec-snapshot` | Run a snapshot immediately (requires `--group`) |
| `--snapshot-recover=node` | Recover the specified node from a snapshot |
| `--exec-sync=node` | Synchronize the specified node |
| `--snapshot-clean` | Clean up snapshots |

### Host Resource Monitoring

| Option | Description |
|------|------|
| `--get-host-resource` | Display host resource information for each node |
| `--host-resource-enable` | Start collecting host resource information |
| `--host-resource-disable` | Stop collecting host resource information |

### Additional Options (Used with Other Options)

| Additional Option | Required Option | Description |
|----------|----------|------|
| `--file-name=filename` | `--add-package` | Package filename |
| `--port-no=portno` | `--add-node`, `--attach-node` | Service port |
| `--http-admin-port=portno` | Coordinator/Deployer `--add-node`, `--attach-node` | Administration REST port |
| `--deployer=node` | `--add-node` | Deployer node name |
| `--package-name=name` | `--add-node`, `--upgrade-node` | Installation source package name |
| `--home-path=path` | `--add-node`, `--attach-node` | Node installation path |
| `--node-type=[broker\|warehouse\|lookup]` | `--add-node`, `--attach-node` | Node type |
| `--lookup-type=[master\|slave\|monitor]` | `--add-node`, `--attach-node` | Lookup node type |
| `--node=node` | `--set-warehouse-state` | Node whose state to change |
| `--alias=alias` | `--add-node`, `--attach-node` | Node alias |
| `--dbs-path=path` | `--add-node` (Broker/Warehouse) | Database file path |
| `--group=groupname` | `--add-node`, `--attach-node`, `--set-group-state`, `--exec-snapshot` | Node group name |
| `--replication=host:port` | `--add-node`, `--attach-node` | Replication target host:port |
| `--no-replicate` | `--add-node`, `--attach-node` | Disable replication |
| `--primary=host:port` | `-u`, `--startup` | Set the Primary for a Secondary Coordinator |
| `--host=host` | `--get-host-resource` | Select a specific host |
| `--metric=[cpu\|memory\|disk\|network]` | `--get-host-resource` | Metric to display |

## Examples

### Checking Process Status

```bash
machcoordinatoradmin -e
```

### Checking Cluster Status

```bash
machcoordinatoradmin --cluster-status
machcoordinatoradmin --cluster-status-full
```

### Activating/Deactivating the Cluster

```bash
machcoordinatoradmin --activate
machcoordinatoradmin --deactivate
```

### Adding a Warehouse Node

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

### Listing Nodes

```bash
machcoordinatoradmin --list-node
machcoordinatoradmin --list-node=192.168.0.32:5401
```

### Setting a Warehouse Group to Read-only

```bash
machcoordinatoradmin --set-group-state=readonly --group=Group1
```

### Querying Configuration

```bash
machcoordinatoradmin --configuration
machcoordinatoradmin --configuration=decision
```

### Monitoring Host Resources

```bash
machcoordinatoradmin --host-resource-enable
machcoordinatoradmin --get-host-resource
machcoordinatoradmin --get-host-resource --metric=cpu
machcoordinatoradmin --get-host-resource --host=192.168.0.33
machcoordinatoradmin --host-resource-disable
```
