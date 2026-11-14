---
type: docs
title: '16.4.9 machdeployeradmin'
weight: 90
toc: true
---

`machdeployeradmin` directly manages Deployer nodes in Machbase Cluster Edition. A Deployer
distributes packages and performs installation on each node as instructed by the Coordinator.

Use `machcoordinatoradmin` to control Deployers under normal conditions. Use `machdeployeradmin`
directly when control through `machcoordinatoradmin` is unavailable.

Included only in the Cluster Edition package.

## Options

```bash
machdeployeradmin -h
```

| Option | Description |
|------|------|
| `-u`, `--startup` | Start the Deployer process |
| `-s`, `--shutdown` | Shut down the Deployer process gracefully |
| `-k`, `--kill` | Force the Deployer process to stop |
| `-c`, `--createdb` | Create Deployer metadata |
| `-d`, `--destroydb` | Delete Deployer metadata |
| `-e`, `--check` | Check whether the Deployer process is running |
| `-i`, `--silent` | Run without a banner |

## Process Management

### Start

```bash
machdeployeradmin -u
```

### Graceful Shutdown

```bash
machdeployeradmin -s
```

### Forced Stop

```bash
machdeployeradmin -k
```

### Check Status

```bash
machdeployeradmin -e
```

Displays the PID if the process is running.

```
Machbase Deployer is running with pid(29373)!
```

## Metadata Management

Create new Deployer metadata.

```bash
machdeployeradmin -c
```

Delete Deployer metadata.

```bash
machdeployeradmin -d
```

## Deployer Responsibilities

The Deployer performs the following tasks under Coordinator instructions.

- Distribute and install Machbase packages on Broker, Warehouse, and Lookup nodes
- Create and manage node configuration files
- Forward node startup/shutdown instructions
- Support node upgrades

## Examples

```bash
# Initialize the Deployer
machdeployeradmin -c
machdeployeradmin -u

# Check status
machdeployeradmin -e

# Shut down gracefully
machdeployeradmin -s

# Force a stop if a problem occurs
machdeployeradmin -k
```

## Notes

Use `machcoordinatoradmin` for most cluster configuration and node management tasks. Use
`machdeployeradmin` for direct intervention when communication with the Coordinator is unavailable
or the Deployer itself has a problem.

For cluster management details, see [machcoordinatoradmin](../machcoordinatoradmin/).
