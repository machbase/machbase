---
type: docs
title: '16.4.7 machclusterctl'
weight: 70
toc: true
---

`machclusterctl` manages an entire Machbase Cluster Edition cluster with a single command. It
validates YAML configuration and handles installation, configuration changes on a running cluster,
upgrades, startup/shutdown, and status checks.

## Main Commands

| Command | Description |
|------|------|
| `validate` | Validate `cluster.yaml` |
| `install` | Install a new cluster from `cluster.yaml` |
| `apply` | Apply configuration changes to a running cluster |
| `upgrade` | Upgrade packages (`--online`, `--full-stop`) |
| `export` | Export the running cluster configuration as flat YAML |
| `status` | Check all cluster node statuses |
| `connect` | Connect to a Broker/Warehouse alias with `machsql` |
| `start` | Start all cluster nodes |
| `stop` | Shut down all cluster nodes gracefully |
| `destroy` | Remove the cluster, including its data |

## Usage

```bash
machclusterctl <command> [options]
```

## Command Details

### validate

Validate the YAML configuration file.

```bash
machclusterctl validate -f cluster.yaml
```

### install

Read the YAML configuration file and install a new cluster.

```bash
machclusterctl install -f cluster.yaml
```

### apply

Apply configuration changes to a running cluster.

```bash
machclusterctl apply -f cluster.yaml
```

### upgrade

Upgrade packages.

```bash
machclusterctl upgrade --online broker
machclusterctl upgrade --full-stop
```

### start

Start the entire cluster in this order: Coordinator → Deployer → Broker → Warehouse.

```bash
machclusterctl start
machclusterctl start -f cluster.yaml
```

### stop

Shut down the entire cluster gracefully.

```bash
machclusterctl stop
```

### destroy

Remove the cluster completely. This also deletes database files; use with care.

```bash
machclusterctl destroy
```

### status

Display the current status of each cluster node.

```bash
machclusterctl status
```

### connect

Connect to a Broker node with `machsql`.

```bash
machclusterctl connect
```

### export

Export the current cluster configuration to a YAML file.

```bash
machclusterctl export -o cluster_backup.yaml
```

## YAML Configuration Structure

Basic YAML structure used by `machclusterctl validate`, `install`, and `apply`:

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

## Options

| Option | Description |
|------|------|
| `-f`, `--file` | Cluster configuration YAML path |
| `-s`, `--silent` | Reduce progress log output |
| `-v`, `--verbose` | Display detailed progress logs |
| `--node` | Target node alias for `start`/`stop` |
| `--type` | Target node type for `start`/`stop` |
| `-o`, `--output` | Output path for `export` |
| `-h`, `--help` | Display help |

## Examples

```bash
# Validate YAML
machclusterctl validate -f my_cluster.yaml

# Install a new cluster
machclusterctl install -f my_cluster.yaml

# Apply changes to a running cluster
machclusterctl apply -f my_cluster.yaml

# Start the cluster
machclusterctl start

# Stop/start a specific node or node type
machclusterctl stop --node broker-1
machclusterctl start --type warehouse

# Check status
machclusterctl status

# Connect to a Broker and run SQL
machclusterctl connect

# Stop the cluster
machclusterctl stop

# Export the configuration
machclusterctl export -o cluster_config_backup.yaml
```
