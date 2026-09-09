# machclusterctl User Guide

`machclusterctl` is a command-line tool for installing and operating Machbase Cluster Edition with a YAML file. Operators declare the desired cluster layout in `cluster.yaml` and manage the cluster with commands such as `validate`, `install`, `apply`, `upgrade`, `start`, and `stop`.

For YAML authoring details, also see [machclusterctl-yaml-guide-en](../machclusterctl-yaml-guide-en/).

## 1. Basic Concepts

`machclusterctl` works as follows.

1. Read `cluster.yaml` and build the desired cluster state.
2. Compare the current cluster state with the desired state.
3. Execute only the required install, add, remove, upgrade, start, or stop operations.

A typical operation flow is:

```bash
machclusterctl validate -f cluster.yaml
machclusterctl install -f cluster.yaml --dry-run
machclusterctl install -f cluster.yaml --yes
machclusterctl status
```

After installation, use `apply` instead of `install` when you edit YAML to add or remove nodes.

```bash
machclusterctl apply -f cluster.yaml --dry-run
machclusterctl apply -f cluster.yaml --yes
```

## 2. Execution Host And Environment

Run `machclusterctl` on the server where the primary coordinator will be installed, or on the primary coordinator server after installation.

Recommended environment variables:

```bash
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
export MACHBASE_HOME=$MACHBASE_COORDINATOR_HOME
export PATH=$MACHBASE_COORDINATOR_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_COORDINATOR_HOME/lib:$LD_LIBRARY_PATH
```

`MACHBASE_COORDINATOR_HOME` is used by commands that run without YAML, such as `status`, `start`, `stop`, `connect`, and `export`, to find the primary coordinator. After installation, the current topology is read from coordinator metadata, not from a local state file.

Commands that do not require YAML are usually run without options.

```bash
machclusterctl status
machclusterctl connect broker-1
machclusterctl export -o cluster-export.yaml
```

Use `--coordinator` only when changing environment variables is inconvenient or when you need to inspect multiple coordinator homes from one server.

```bash
machclusterctl status --coordinator /home/machbase/coordinator
machclusterctl export --coordinator /home/machbase/coordinator -o cluster-export.yaml
```

## 3. Preparation Before Installation

Prepare the following items before installation.

| Item | Description |
|------|-------------|
| package archive | Machbase Cluster Edition package file on the primary coordinator server |
| SSH key | Private key used by the primary coordinator server to connect to each target server |
| cluster.yaml | Coordinator, deployer, lookup, broker, and warehouse layout to install |
| Directory permissions | Permission to create and write each node's `home_path` parent directory |
| Ports | Ports defined in YAML must not already be in use on each server |

SSH uses non-interactive key-file based access. Do not write a password field in YAML.

Precheck examples:

```bash
ssh -i /home/machbase/.ssh/id_rsa machbase@192.168.0.11 'echo ok'
scp -i /home/machbase/.ssh/id_rsa /etc/hosts machbase@192.168.0.11:/home/machbase/hosts.test
```

## 4. Command Summary

| Command | Purpose |
|---------|---------|
| `validate` | Check YAML syntax, required values, port conflicts, and topology |
| `install` | Install a new cluster into an empty environment |
| `apply` | Apply YAML changes to a running cluster |
| `upgrade` | Upgrade nodes when the package changes |
| `status` | Show the current cluster state |
| `connect` | Connect with `machsql` using a broker or warehouse alias |
| `start` | Start all nodes, nodes by type, or a specific node |
| `stop` | Stop all nodes, nodes by type, or a specific node |
| `export` | Export the running cluster topology as YAML |
| `destroy` | Remove cluster installation traces |

Common options:

| Option | Description |
|--------|-------------|
| `-f`, `--file` | YAML file to use. Default is `./cluster.yaml` |
| `--dry-run` | Print checks and execution plan without changing anything |
| `-y`, `--yes` | Run without confirmation prompts |
| `-v`, `--verbose` | Accepted for compatibility; execution commands print progress by default |
| `-s`, `--silent` | Suppress progress logs; takes precedence over `-v`/`--verbose` |
| `--coordinator` | Primary coordinator home for `status`, `start`, `stop`, `connect`, and `export` when running without YAML |

## 5. YAML Validation

Always validate YAML before installation or changes.

```bash
machclusterctl validate -f cluster.yaml
```

Successful output:

```text
Validation passed.
```

Main validation items:

- Missing required fields
- Duplicate node aliases
- Port conflicts on the same host
- Number of primary coordinators
- Lookup master/monitor layout
- `home_path` and `dbs_path` path formats
- `deployer` references

## 6. Initial Installation

Use `install` only in an empty environment where the cluster has not been installed yet. It fails if installation traces already exist or if the cluster is already running.

First, check whether installation is possible.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

If there is no problem, run the installation.

```bash
machclusterctl install -f cluster.yaml --yes --verbose
```

After installation, check the status.

```bash
machclusterctl status
```

`install` prepares and starts coordinator, deployer, package, lookup, broker, and warehouse nodes based on YAML. After installation, `status`, `start`, `stop`, `connect`, and `export` read current metadata from the running coordinator.

## 7. Applying Operational Changes

After installation, use `apply` when you edit YAML to add, remove, or change nodes.

Recommended procedure:

```bash
machclusterctl validate -f cluster.yaml
machclusterctl apply -f cluster.yaml --dry-run --verbose
machclusterctl apply -f cluster.yaml --yes --verbose
machclusterctl status
```

`apply` works only on a running cluster. If the cluster is shut down, start it first.

```bash
machclusterctl start
machclusterctl apply -f cluster.yaml --dry-run
machclusterctl apply -f cluster.yaml --yes
```

Typical operations handled by `apply`:

- Add lookup, broker, and warehouse nodes
- Remove lookup, broker, and warehouse nodes
- Re-register lookup, broker, and warehouse nodes when their settings change
- Add a secondary coordinator
- Add a deployer
- Upgrade broker/warehouse nodes when the YAML package changes

Replacing or removing the primary coordinator is not supported.

## 8. Start, Stop, And Status

Show the whole cluster status:

```bash
machclusterctl status
```

Start and stop the whole cluster:

```bash
machclusterctl start
machclusterctl stop
```

Start and stop by node type:

```bash
machclusterctl start --type=warehouse
machclusterctl stop --type=warehouse

machclusterctl start --type=broker
machclusterctl stop --type=broker
```

Start and stop a specific node:

```bash
machclusterctl start --node=warehouse-group1-1
machclusterctl stop --node=warehouse-group1-1
```

`--node` takes a YAML `alias`, not `host:port`.

When stopping warehouses, the required warehouse group state changes are performed together. After stopping a single warehouse, the group state is restored to `normal`. When the entire group is stopped, as in a full warehouse stop, the group state transition is requested according to the stop flow.

## 9. SQL Connection

Use `connect` to connect to a broker or warehouse with `machsql`.

```bash
machclusterctl connect broker-1
machclusterctl connect warehouse-group1-1
```

`connect` finds the host and `service_port` for the alias and runs `machsql` in the following form.

```bash
machsql -s <host_ip> -P <service_port>
```

For example, if `broker-1` uses host `192.168.0.11` and `service_port` `5656`, it is equivalent to:

```bash
machsql -s 192.168.0.11 -P 5656
```

By default, aliases and service ports are read from the running coordinator metadata. If you want to resolve the target from a specific YAML file, specify `-f`.

```bash
machclusterctl connect -f cluster.yaml broker-1
```

Notes:

- The alias must point to a broker or warehouse node.
- Use the YAML `alias`; do not pass `host:port` as with `--node`.
- Normal usage relies on `MACHBASE_COORDINATOR_HOME` to identify the primary coordinator home.
- In exceptional cases where environment variables are inconvenient, specify the primary coordinator home directly with `--coordinator`.

## 10. Package Upgrade

To upgrade, change the input package under `cluster.package` in YAML to the new archive and run the upgrade. YAML written by operators usually uses `path`.

```yaml
cluster:
  package:
    name: machbase-v2
    path: /machbase/packages/machbase-v2.tgz
```

YAML produced by `machclusterctl export` can record package paths separately as follows.

```yaml
cluster:
  package:
    name: machbase-v2
    origin_path: /machbase/packages/machbase-v2.tgz
    registered_path: /machbase/coordinator/package/machbase-v2.tgz
```

Field meanings:

- `path`: Simple input archive path written by the operator.
- `origin_path`: Input archive path with the same purpose as `path`. If both `origin_path` and `path` are present, `origin_path` takes precedence.
- `registered_path`: Path where the coordinator stores the package after `--add-package`. This is observed current metadata, not an execution input.

Package changes are detected by comparing the current package name of running broker/warehouse nodes with `cluster.package.name` in YAML. If you keep the same `package.name` and change only the archive contents or `path`/`origin_path`, existing broker/warehouse nodes are not detected as upgrade targets. When applying a new archive, use both a new package name and a unique archive file name.

### 10-1. Package Path Operation Rules

Write `cluster.package.path` or `cluster.package.origin_path` as the **source package archive path** on the primary coordinator server. `install`, new-node `apply`, and `upgrade` automatically run `machcoordinatoradmin --add-package=<name> --file-name=<archive>` when required.

The package archive must be readable from the command execution host. The `--full-stop` precheck verifies that the archive contains `machcoordinatoradmin`, `machdeployeradmin`, `conf/`, and `lib/`.

As a rule, do not use the coordinator-managed package repository path as the source for registering a new package in operational YAML.

```yaml
# Recommended: source archive path kept by the operator
cluster:
  package:
    name: machbase-v2
    path: /machbase/packages/machbase-v2.tgz

# Not recommended: path stored internally after coordinator registration
cluster:
  package:
    name: machbase-v2
    path: /machbase/coordinator/package/machbase-v2.tgz
```

Reasons:

- Files in the coordinator package repository are outputs of `--add-package`. If the same file is used again as the source, behavior can vary depending on whether it is an already registered package or a file-name conflict for a new package.
- If the same `package.name` and file name are already registered, `machclusterctl` may treat the operation as an idempotent no-op.
- If the same file name is reused with a different `package.name`, the coordinator may reject it as a file-name conflict. Manage new packages with unique file names such as `machbase-v2.tgz` and `machbase-v3.tgz`.
- `destroy` can remove the coordinator home and package repository. Keep archives for reinstallation in a separate location outside the coordinator home.

Normal operating rules:

- For `install`, new-node `apply`, and `upgrade`, write `path` or `origin_path` as a preserved source archive path outside the coordinator home.
- When package contents change, change both `package.name` and the archive file name.
- When reusing exported YAML for reinstallation or upgrade, change `origin_path` to the source archive path, or write a new `path` instead of relying on `registered_path`.

### 10-2. Online Upgrade

`--online` applies the package to broker and warehouse nodes. Coordinator, deployer, and lookup nodes are not online-mode targets.

```bash
machclusterctl upgrade -f cluster.yaml --online --dry-run
machclusterctl upgrade -f cluster.yaml --online --yes --verbose
```

If no mode is specified, `upgrade` uses online mode. Use `--online` explicitly in operational procedures for clarity. `--online` and `--full-stop` cannot be used together. The upgrade automatically performed by `apply` when it detects a package change has the same broker/warehouse online upgrade scope.

Main online upgrade flow:

1. Verify that the cluster is running.
2. Verify that YAML and current topology do not contain node additions, removals, or configuration changes.
3. Register the new package archive in the coordinator package repository.
4. For brokers, run `--upgrade-node` and then startup.
5. For warehouses, switch the group to `readonly`, make the target node `inactive`, run `--upgrade-node`, start/activate the node, and restore the group to `normal`.
6. Verify that the target broker/warehouse nodes are running.

Online mode does not stop the whole cluster, but it is not an HA-aware rolling upgrade guarantee. Use `--full-stop` for coordinator/deployer/lookup binary changes, changes with protocol compatibility risk, or changes that require all nodes to use the same package.

### 10-3. Full-Stop Upgrade

Use `--full-stop` when you need to replace binaries on all nodes, including coordinator, deployer, and lookup nodes. This mode assumes full cluster downtime.

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --dry-run
machclusterctl upgrade -f cluster.yaml --full-stop --yes --verbose
```

Main full-stop upgrade flow:

1. Verify that the cluster is running.
2. Verify that YAML and current topology do not contain node additions, removals, or configuration changes.
3. Verify local `tar`, and `ssh`/`scp` if there are remote nodes.
4. Verify that the package archive exists and contains required entries.
5. Verify that every target node's `home_path` exists and is writable.
6. Register the new package in the coordinator package repository.
7. Stop the entire cluster.
8. Extract the archive into a staging path next to each node's `home_path`, then apply it to the node home.
9. Start the primary coordinator first, then start the remaining cluster.
10. Synchronize broker/warehouse package metadata and verify that all target nodes are running.

During node home replacement, the `dbs`, `meta`, and `package` directories are preserved. Existing `conf/machbase.conf` is backed up and restored. If an error occurs during replacement, existing home entries for that node are restored as far as possible.

Topology must be stable before upgrade. If there are node additions, removals, or configuration changes, run `apply` first, then perform the package upgrade.

Post-upgrade checks:

```bash
machclusterctl status
machclusterctl apply -f cluster.yaml --dry-run
```

## 11. Export Current Topology

Use `export` to save the running cluster state as YAML.

```bash
machclusterctl export -o current.yaml
```

To print to standard output:

```bash
machclusterctl export
```

`export` produces flat YAML. It does not generate `cluster.hosts`, `cluster.defaults`, or environment-variable expressions. Package fields are written as `origin_path` and `registered_path` based on coordinator package metadata.

`origin_path` is the source archive path known by the coordinator. If metadata does not contain a source path, `registered_path` is also written to `origin_path` so that the exported YAML remains valid. `registered_path` is the package path stored in the coordinator package repository (`<coordinator_home>/package/<File-Name>`).

This file is useful for saving the current operational state or comparing diffs before and after changes. However, exported `registered_path` does not restore the original archive path used by the operator during initial installation.
`export` fails if package list lookup fails or if it cannot find an absolute registered package path for the current package name. In this case, it does not generate YAML by substituting the package name as a path.

Exported YAML usage rules:

- It can be used as-is to compare with the running cluster or to run a no-op `apply --dry-run` against the same running cluster.
- For reinstallation, preserve the file pointed to by `origin_path` outside the coordinator home before `destroy`, or change `origin_path` or `path` in YAML to the actual source archive path.
- For upgrading to a new package, do not use the exported `registered_path` as an execution input. Change `package.name` and `origin_path` or `path` together to point to the new source archive.
- Add SSH key/user information back to YAML if bootstrap information is required.

## 12. destroy

Use `destroy` to remove the cluster and return to an uninstalled state.

```bash
machclusterctl destroy -f cluster.yaml
```

To include automatic confirmation:

```bash
machclusterctl destroy -f cluster.yaml --yes --verbose
```

Notes:

- It cleans up installation traces for both running and stopped clusters.
- Broker/warehouse data can be deleted.
- Restrict execution privileges in production environments.

## 13. Common Errors

| Error/Situation | Action |
|-----------------|--------|
| `cluster is already installed` | Existing installation traces were found. For a fresh installation, run `destroy` or clean up manually before running `install` again. |
| `cluster is not installed` | Run `install` first. |
| `cluster is installed but not running` | Run `machclusterctl start`, then retry `apply` or `upgrade`. |
| `port conflict` | Fix duplicated `cluster_link_port`, `http_admin_port`, `service_port`, or derived ports on the same host. |
| `undefined host alias` | Check whether the YAML `host` is defined in `cluster.hosts`. |
| `key_file missing` | Check the SSH key path or set `cluster.ssh.key_file`. |
| `ssh.password ... is not supported` | Remove the password field from YAML and use key-file based SSH. |
| `missing cluster.package.origin_path` | Set either `cluster.package.path` or `cluster.package.origin_path` to an input archive path. |
| `package.path changed but package.name stayed` | Use a new `package.name` for the new package archive. The same rule applies when only `origin_path` changes. |
| `package already exists` or `File-Name already exists` | The same archive file name is already registered in the coordinator. For a new package, change both `package.name` and the archive file name, and set `path` or `origin_path` to a source archive path outside the coordinator package repository. |
| `connect target ... must be broker or warehouse alias` | Check that the `connect` target alias is a broker or warehouse. |

When a problem occurs, first inspect the plan and prechecks with `--dry-run --verbose`.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
machclusterctl apply -f cluster.yaml --dry-run --verbose
machclusterctl upgrade -f cluster.yaml --online --dry-run --verbose
```

## 14. Reference Files

- YAML authoring guide: [machclusterctl-yaml-guide-en](../machclusterctl-yaml-guide-en/)
- Environment-variable based sample: [machclusterctl-sample-defaults.yaml](../machclusterctl-sample-defaults.yaml)
- Sample environment variables: [machclusterctl-sample-defaults.env.sh](../machclusterctl-sample-defaults.env.sh)
- Static sample: [machclusterctl-sample-defaults-noenv.yaml](../machclusterctl-sample-defaults-noenv.yaml)
