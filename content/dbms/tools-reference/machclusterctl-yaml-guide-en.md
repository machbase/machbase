# machclusterctl YAML Authoring Guide

This document describes how to write the `cluster.yaml` file used by `machclusterctl`. For command execution procedures, see [machclusterctl-user-guide-en](../machclusterctl-user-guide-en/).

YAML describes the desired cluster state. `machclusterctl` reads the YAML and then applies `cluster.defaults`, `cluster.hosts`, and environment-variable substitution to produce the final resolved configuration.

## 1. Minimal Configuration

Use `cluster.defaults` and `cluster.hosts` to collect repeated values, and leave only `alias`, `host`, and role fields on each node. In a typical layout where each server has one node of each type, ports do not need to be repeated for every node. If two or more nodes of the same type are placed on the same host, the first node can use the type defaults, and the second and later nodes usually override conflicting ports and `home_path`.

The following example configures two coordinators, two deployers, lookup master/monitor, one broker, and one warehouse group on two servers.

```yaml
version: "1"

cluster:
  name: mc-minimal

  hosts:
    node1:
      address: machbase@192.168.0.11
    node2:
      address: machbase@192.168.0.12

  package:
    name: machbase
    path: /machbase/packages/machbase-ent-release-lightweight.tgz

  ssh:
    key_file: /home/machbase/.ssh/id_rsa

  defaults:
    coordinator:
      home_path: /machbase/coordinator
      cluster_link_port: 5101
      http_admin_port: 5102
    deployer:
      home_path: /machbase/deployer
      cluster_link_port: 5201
      http_admin_port: 5202
    lookup:
      home_path: /machbase/lookup
      cluster_link_port: 5301
      http_admin_port: 5302
    broker:
      home_path: /machbase/broker
      cluster_link_port: 5401
      http_admin_port: 5402
      service_port: 5656
    warehouse:
      home_path: /machbase/warehouse
      cluster_link_port: 5501
      http_admin_port: 5502
      service_port: 5500

  coordinators:
    - alias: coord-primary-1
      host: node1
      role: primary

    - alias: coord-secondary-1
      host: node2
      role: secondary

  deployers:
    - alias: deployer-1
      host: node1

    - alias: deployer-2
      host: node2

  lookup:
    - alias: lookup-master-1
      host: node1
      deployer: deployer-1
      type: master

    - alias: lookup-monitor-1
      host: node2
      deployer: deployer-2
      type: monitor

  brokers:
    - alias: broker-1
      host: node1
      deployer: deployer-1

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node1
          deployer: deployer-1

        - alias: warehouse-group1-2
          host: node2
          deployer: deployer-2
```

Resolution result:

- `node1` and `node2` are converted to the actual `machbase@IP` values from `cluster.hosts`.
- The SSH user is obtained from `address: machbase@...`, and `cluster.ssh.key_file` is used as the common SSH key.
- `home_path`, `cluster_link_port`, `http_admin_port`, and `service_port` are inherited from type-specific `defaults`.
- The same default port can be used on different hosts without conflict.
- If two or more nodes of the same type are placed on the same host, the first node uses the default ports, and the second and later nodes explicitly override ports and usually `home_path`.

Example with two warehouses on the same host:

```yaml
defaults:
  warehouse:
    home_path: /machbase/warehouse
    cluster_link_port: 5501
    http_admin_port: 5502
    service_port: 5500

warehouse_groups:
  - name: group1
    nodes:
      - alias: warehouse-group1-1
        host: node1
        deployer: deployer-1

  - name: group2
    nodes:
      - alias: warehouse-group2-1
        host: node1
        deployer: deployer-1
        home_path: /machbase/warehouse-group2
        cluster_link_port: 5511
        http_admin_port: 5512
        service_port: 5510
```

## 2. Mixing Environment Variables, Common Values, And Overrides

Values that differ by environment can be written as `${VAR}` or `${VAR:-default}`. Put common values in `defaults`, and override only ports, home paths, or `dbs_path` for specific nodes.

Supported environment-variable syntax:

- `${VAR}`: Error if the environment variable is not set.
- `${VAR:-default}`: Use `default` if the environment variable is not set or is an empty string.

Example environment variables:

```bash
export MC_PACKAGE_PATH=/machbase/packages/machbase-ent-release-lightweight.tgz
export MC_SSH_KEY=/home/machbase/.ssh/id_rsa
export MC_NODE1=machbase@192.168.0.11
export MC_NODE2=machbase@192.168.0.12
export MC_NODE3=machbase@192.168.0.13
export MC_HOME_BASE=/machbase
```

YAML example:

```yaml
version: "1"

cluster:
  name: "${MC_CLUSTER_NAME:-mc-mixed}"

  hosts:
    node1:
      address: "${MC_NODE1}"
    node2:
      address: "${MC_NODE2}"
    node3:
      address: "${MC_NODE3:-machbase@192.168.0.13}"

  package:
    name: "${MC_PACKAGE_NAME:-machbase}"
    path: "${MC_PACKAGE_PATH}"

  ssh:
    key_file: "${MC_SSH_KEY}"

  defaults:
    coordinator:
      home_path: "${MC_HOME_BASE:-/machbase}/coordinator"
      cluster_link_port: "${MC_COORD_PORT:-5101}"
      http_admin_port: "${MC_COORD_HTTP_PORT:-5102}"
    deployer:
      home_path: "${MC_HOME_BASE:-/machbase}/deployer"
      cluster_link_port: "${MC_DEPLOYER_PORT:-5201}"
      http_admin_port: "${MC_DEPLOYER_HTTP_PORT:-5202}"
    lookup:
      home_path: "${MC_HOME_BASE:-/machbase}/lookup"
      cluster_link_port: "${MC_LOOKUP_PORT:-5301}"
      http_admin_port: "${MC_LOOKUP_HTTP_PORT:-5302}"
    broker:
      home_path: "${MC_HOME_BASE:-/machbase}/broker"
      cluster_link_port: "${MC_BROKER_PORT:-5401}"
      http_admin_port: "${MC_BROKER_HTTP_PORT:-5402}"
      service_port: "${MC_BROKER_SERVICE_PORT:-5656}"
    warehouse:
      home_path: "${MC_HOME_BASE:-/machbase}/warehouse"
      cluster_link_port: "${MC_WAREHOUSE_PORT:-5501}"
      http_admin_port: "${MC_WAREHOUSE_HTTP_PORT:-5502}"
      service_port: "${MC_WAREHOUSE_SERVICE_PORT:-5500}"

  coordinators:
    - alias: coord-primary-1
      host: node1
      role: primary

    - alias: coord-secondary-1
      host: node2
      role: secondary
      # Only the coordinator on node2 uses a separate home path.
      home_path: "${MC_HOME_BASE:-/machbase}/coordinator-secondary"

  deployers:
    - alias: deployer-1
      host: node1

    - alias: deployer-2
      host: node2

    - alias: deployer-3
      host: node3

  lookup:
    - alias: lookup-master-1
      host: node1
      deployer: deployer-1
      type: master

    - alias: lookup-monitor-1
      host: node2
      deployer: deployer-2
      type: monitor

    - alias: lookup-slave-1
      host: node3
      deployer: deployer-3
      type: slave
      # Override only the slave ports in case another lookup node is added on node3.
      cluster_link_port: "${MC_LOOKUP_SLAVE_PORT:-5311}"
      http_admin_port: "${MC_LOOKUP_SLAVE_HTTP_PORT:-5312}"

  brokers:
    - alias: broker-1
      host: node1
      deployer: deployer-1

    - alias: broker-2
      host: node2
      deployer: deployer-2
      # Override only broker-2's service port and dbs path.
      service_port: "${MC_BROKER2_SERVICE_PORT:-5666}"
      dbs_path: "${MC_HOME_BASE:-/machbase}/dbs/broker-2"

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node1
          deployer: deployer-1

        - alias: warehouse-group1-2
          host: node2
          deployer: deployer-2
          dbs_path: "${MC_HOME_BASE:-/machbase}/dbs/warehouse-group1-2"

    - name: group2
      nodes:
        - alias: warehouse-group2-1
          host: node2
          deployer: deployer-2
          # Because this is the second warehouse on node2, override ports and home_path.
          home_path: "${MC_HOME_BASE:-/machbase}/warehouse-group2"
          cluster_link_port: "${MC_WAREHOUSE_G2_PORT:-5511}"
          http_admin_port: "${MC_WAREHOUSE_G2_HTTP_PORT:-5512}"
          service_port: "${MC_WAREHOUSE_G2_SERVICE_PORT:-5510}"

        - alias: warehouse-group2-2
          host: node3
          deployer: deployer-3
```

Operating rules:

- Environment-variable substitution runs before YAML decoding. Values substituted into numeric fields must be convertible to integers.
- If `cluster.hosts.<alias>.address` uses `user@host`, the SSH user does not need to be repeated separately.
- `cluster.ssh.key_file` is for defining one common key. If each host uses a different key, override it with `cluster.hosts.<alias>.ssh.key_file`.
- `deployer` is the deployer alias used by lookup, broker, and warehouse nodes. It can be omitted when there is only one deployer on the same host, but specifying it is safer.
- `dbs_path` can be used only on broker and warehouse nodes. It cannot be placed in defaults.

## 3. All Configurable Fields

### 3-1. Top-Level Structure

| YAML path | Type | Required | Description |
|-----------|------|----------|-------------|
| `version` | string | Yes | YAML schema version. Use `"1"` currently. |
| `cluster` | object | Yes | Entire cluster definition. |
| `cluster.name` | string | Yes | Cluster name. Used in `validate`, `install`, `apply`, and `destroy` confirmation messages and for human identification. |

### 3-2. `cluster.hosts`

`cluster.hosts` collects IP addresses or hostnames in one place so node settings can refer to host aliases.

| YAML path | Type | Required | Fallback | Description |
|-----------|------|----------|----------|-------------|
| `cluster.hosts` | map | No | None | Host alias definition list. |
| `cluster.hosts.<alias>.address` | string | Yes if the host alias is used | None | Actual IP/DNS endpoint, or `user@ip` / `user@hostname`. |
| `cluster.hosts.<alias>.ssh` | object | No | `cluster.ssh` | SSH overrides applied to nodes that use this host alias. |
| `cluster.hosts.<alias>.ssh.user` | string | No | User from `address` or common SSH user | SSH user for compatibility or exceptions. New YAML should prefer `address: user@host`. |
| `cluster.hosts.<alias>.ssh.port` | int | No | `cluster.ssh.port` or 22 | SSH connection port. |
| `cluster.hosts.<alias>.ssh.key_file` | string | No | `cluster.ssh.key_file` | SSH private key path for this host. |

If a `host` value is a simple string not found in `cluster.hosts` and it does not look like an IP/DNS name, `undefined host alias` is raised. `localhost`, IP addresses, and hostnames containing `.` or `:` are treated as direct host values.

### 3-3. `cluster.defaults`

`defaults` is a `machclusterctl` feature for reducing repeated values by node type.

| YAML path | Type | Required | Description |
|-----------|------|----------|-------------|
| `cluster.defaults.common.ssh_user` | string | No | Common SSH user for backward compatibility. New YAML should prefer `user@host`. |
| `cluster.defaults.coordinator` | object | No | Coordinator defaults. |
| `cluster.defaults.deployer` | object | No | Deployer defaults. |
| `cluster.defaults.lookup` | object | No | Lookup defaults. |
| `cluster.defaults.broker` | object | No | Broker defaults. |
| `cluster.defaults.warehouse` | object | No | Warehouse defaults. |

Fields available in node-type defaults:

| Field | Applies To | Description |
|-------|------------|-------------|
| `home_path` | All node types | Node home path. Only absolute paths are allowed. |
| `cluster_link_port` | All node types | Cluster link communication port. |
| `http_admin_port` | All node types | HTTP admin port. Required for coordinator/deployer. Lookup/broker/warehouse can configure it, and defaults or per-node values are recommended. |
| `service_port` | broker, warehouse | Broker client connection port or warehouse service port. |

Node-level values take precedence. If a node value is omitted, the default for that node type is used.

### 3-4. `cluster.package`

| YAML path | Type | Required | Description |
|-----------|------|----------|-------------|
| `cluster.package.name` | string | Yes | Package name to register in the coordinator. A new package name is recommended for upgrades. |
| `cluster.package.path` | string | Conditional | Input archive path written by operators. Used when `origin_path` is absent. |
| `cluster.package.origin_path` | string | Conditional | Input archive path. Takes precedence when both `path` and `origin_path` are present. Exported YAML writes this field. |
| `cluster.package.registered_path` | string | No | Path where the coordinator stores the package. This is observed current metadata in exported YAML and is not used as an install/upgrade input. |

Either `path` or `origin_path` must be set. For `install`, `upgrade`, and new-node `apply`, this archive must actually exist and must contain Machbase binaries plus `bin/`, `lib/`, and `conf/` components.

Package changes are detected by comparing the current package name of running broker/warehouse nodes with `cluster.package.name` in YAML. If you keep the same `cluster.package.name` and change only the archive contents or `cluster.package.path` / `cluster.package.origin_path`, existing broker/warehouse nodes are not detected as upgrade targets. To apply an archive with different contents, use a new `cluster.package.name` and a unique archive file name.

#### Package Input Path And Coordinator Package Repository

As a rule, `cluster.package.path` or `cluster.package.origin_path` in desired YAML should point to the **source archive path** kept outside the coordinator home.

Recommended:

```yaml
cluster:
  package:
    name: machbase-v2
    path: /machbase/packages/machbase-v2.tgz
```

Not recommended:

```yaml
cluster:
  package:
    name: machbase-v2
    path: /machbase/coordinator/package/machbase-v2.tgz
```

The coordinator's `package/` directory is an internal repository where `machcoordinatoradmin --add-package` stores registered packages. If a file from this path is reused as the source for registering a new package, the following situations can occur.

- If the same `package.name` and file name are already registered, the operation may pass as an idempotent no-op.
- If the same file name is registered with a different `package.name`, the coordinator may reject it as a file-name conflict.
- After `destroy`, the package repository can be deleted together with the coordinator home. Reinstallation can fail if you rely only on the package path in exported YAML.

Manage new archives for upgrade with these rules.

- When archive contents change, change `cluster.package.name`.
- Make the archive file name unique and aligned with the new package name, for example `machbase-v2.tgz` or `machbase-v3.tgz`.
- Set `cluster.package.path` or `cluster.package.origin_path` to a preserved source path outside the coordinator home, such as `/machbase/packages/...`.
- Do not use `registered_path` from `machclusterctl export` as a reinstall or new-upgrade input. If necessary, change `origin_path` to the source archive path or write a new `path`.

If YAML contains an undefined field, loading fails. Typos are not silently ignored, so check and fix the field name shown in the error message.

### 3-5. SSH Settings

SSH settings are used by commands that directly access remote servers, such as `install`, new-node add, `destroy`, and `upgrade --full-stop`.

Precedence:

```text
cluster.defaults.common.ssh_user
  -> cluster.ssh
  -> user from user@host or hosts.<alias>.address
  -> cluster.hosts.<alias>.ssh
  -> node.ssh
```

| YAML path | Type | Required | Description |
|-----------|------|----------|-------------|
| `cluster.ssh.user` | string | Conditional | Common SSH user. New YAML should prefer `address: user@host`. |
| `cluster.ssh.port` | int | No | Common SSH port. If omitted, SSH default port 22 is used. |
| `cluster.ssh.key_file` | string | Yes for remote operations | Common SSH private key path. |
| `node.ssh.user` | string | No | Node-specific SSH user override. |
| `node.ssh.port` | int | No | Node-specific SSH port override. |
| `node.ssh.key_file` | string | No | Node-specific SSH key override. |

The YAML schema does not include an SSH password field. If `ssh.password` is written, configuration loading fails.

### 3-6. Common Node Fields

The following fields are used commonly by coordinator, deployer, lookup, broker, and warehouse nodes. However, `deployer`, `service_port`, and `dbs_path` are limited to specific node types.

| Field | Type | Required | Fallback | Description |
|-------|------|----------|----------|-------------|
| `alias` | string | No | Auto-generated | Logical node name. Explicit aliases are recommended in production. Commands use aliases for `--node`. |
| `host` | string | Yes | None | Actual host, `user@host`, or a host alias defined in `cluster.hosts`. |
| `cluster_link_port` | int | Yes if defaults are absent | `defaults.<type>.cluster_link_port` | Node cluster link port. The actual identity is `host:cluster_link_port`. |
| `http_admin_port` | int | Yes for coordinator/deployer if defaults are absent | `defaults.<type>.http_admin_port` | HTTP admin port. |
| `home_path` | string | Yes if defaults are absent | `defaults.<type>.home_path` | Node home path. Only absolute paths are allowed. |
| `deployer` | string | Recommended for lookup/broker/warehouse | Deployer on the same host | Deployer alias or `host:cluster_link_port` to use. Required when multiple deployers exist on the same host. |
| `service_port` | int | Yes for broker/warehouse if defaults are absent | `defaults.broker.service_port`, `defaults.warehouse.service_port` | Broker client connection port or warehouse service port. |
| `dbs_path` | string | No | None | Broker/warehouse data path. Only absolute paths or paths starting with `?` are allowed. |
| `dbs-path` | string | No | None | Compatibility alias for `dbs_path`. Allowed only on broker/warehouse nodes. |
| `ssh` | object | No | host/common SSH settings | Node-specific SSH override. |

Notes:

- `cluster_link_port`, `http_admin_port`, `service_port`, and internally derived ports must not conflict on the same host. Validation fails when they do.
- Coordinator/deployer use `cluster_link_port + 1` as their internal `PORT_NO`. This port must not conflict with other node ports.
- Warehouse uses `service_port + 2` as the replication manager port. This port must not conflict with another node's `cluster_link_port`, `http_admin_port`, or `service_port`.
- `dbs_path` is invalid outside broker/warehouse nodes.
- `dbs_path` cannot be placed in defaults.

### 3-7. coordinator

Path: `cluster.coordinators[]`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `alias` | string | No | Coordinator alias. |
| `host` | string | Yes | Host alias or actual host. |
| `role` | string | Yes | `primary` or `secondary`. There must be exactly one primary. |
| `cluster_link_port` | int | Yes if defaults are absent | Cluster link port. |
| `http_admin_port` | int | Yes if defaults are absent | HTTP admin port. |
| `home_path` | string | Yes if defaults are absent | Coordinator home path. |
| `ssh` | object | No | Node-specific SSH override. |

### 3-8. deployer

Path: `cluster.deployers[]`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `alias` | string | No | Deployer alias. |
| `host` | string | Yes | Host alias or actual host. |
| `cluster_link_port` | int | Yes if defaults are absent | Cluster link port. |
| `http_admin_port` | int | Yes if defaults are absent | HTTP admin port. |
| `home_path` | string | Yes if defaults are absent | Deployer home path. |
| `ssh` | object | No | Node-specific SSH override. |

The `deployer` field of lookup/broker/warehouse nodes refers to this deployer's `alias` or `host:cluster_link_port`.

### 3-9. lookup

Path: `cluster.lookup[]`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `alias` | string | No | Lookup alias. |
| `host` | string | Yes | Host alias or actual host. |
| `deployer` | string | Recommended | Deployer alias or `host:cluster_link_port` used for installation. |
| `type` | string | Yes | One of `master`, `monitor`, or `slave`. Exactly one master is required, and at least one monitor is required. |
| `cluster_link_port` | int | Yes if defaults are absent | Cluster link port. |
| `http_admin_port` | int | No | HTTP admin port. |
| `home_path` | string | Yes if defaults are absent | Lookup home path. |
| `ssh` | object | No | Node-specific SSH override. |

### 3-10. broker

Path: `cluster.brokers[]`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `alias` | string | No | Broker alias. |
| `host` | string | Yes | Host alias or actual host. |
| `deployer` | string | Recommended | Deployer alias or `host:cluster_link_port` used for installation. |
| `cluster_link_port` | int | Yes if defaults are absent | Cluster link port. |
| `http_admin_port` | int | No | HTTP admin port. |
| `service_port` | int | Yes if defaults are absent | Client/machsql connection port. |
| `home_path` | string | Yes if defaults are absent | Broker home path. |
| `dbs_path` or `dbs-path` | string | No | Broker `DBS_PATH` override. |
| `ssh` | object | No | Node-specific SSH override. |

### 3-11. warehouse group / warehouse node

Paths:

- `cluster.warehouse_groups[]`
- `cluster.warehouse_groups[].nodes[]`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `warehouse_groups[].name` | string | Yes | Warehouse group name. This is the replication unit. |
| `warehouse_groups[].nodes[].alias` | string | No | Warehouse alias. |
| `warehouse_groups[].nodes[].host` | string | Yes | Host alias or actual host. |
| `warehouse_groups[].nodes[].deployer` | string | Recommended | Deployer alias or `host:cluster_link_port` used for installation. |
| `warehouse_groups[].nodes[].cluster_link_port` | int | Yes if defaults are absent | Cluster link port. |
| `warehouse_groups[].nodes[].http_admin_port` | int | No | HTTP admin port. |
| `warehouse_groups[].nodes[].service_port` | int | Yes if defaults are absent | Warehouse service port. |
| `warehouse_groups[].nodes[].home_path` | string | Yes if defaults are absent | Warehouse home path. |
| `warehouse_groups[].nodes[].dbs_path` or `dbs-path` | string | No | Warehouse `DBS_PATH` override. |
| `warehouse_groups[].nodes[].ssh` | object | No | Node-specific SSH override. |

When adding a warehouse, `machclusterctl` calculates that warehouse's own `host:service_port+2` as the replication manager address. This is not the peer address; it corresponds to `REPLICATION_MANAGER_PORT_NO` in the warehouse configuration to be generated. If `--no-replicate` is required, such as for the first warehouse in a group, `--replication` is not passed together.

### 3-12. Relationship With Exported Flat YAML

YAML generated by `machclusterctl export` is output for saving the final values of a running cluster or comparing them with diffs. `export` always outputs flat YAML without extra options.

Flat YAML characteristics:

- It does not use `cluster.hosts`.
- It does not use `cluster.defaults`.
- It does not use environment-variable expressions.
- It explicitly writes actual `host`, `cluster_link_port`, `http_admin_port`, `service_port`, `home_path`, `dbs_path`, and similar values for each node as much as possible.
- Output order is stable so diffs are easy to compare.

Therefore, when writing YAML manually, use the compact style from chapter 1 or 2. Use flat export when saving the actual running cluster state or comparing change history.

Notes:

- `cluster.package.origin_path` in exported YAML is the source archive path known by the coordinator. If metadata does not contain a source path, it can be filled with the `registered_path` value.
- `cluster.package.registered_path` in exported YAML is the package file path currently registered and stored in the coordinator. This value is closer to a current metadata snapshot than to the source package archive location.
- `export` fails if package list lookup fails or if it cannot find an absolute registered package path for the current package name.
- Exported YAML can be used as-is for `validate`, `apply --dry-run`, and structure diffs against the same running cluster.
- When using exported YAML for reinstallation after `destroy` or for a new package upgrade, change `cluster.package.origin_path` or `cluster.package.path` to a source archive path outside the coordinator home.
- SSH settings required for adding new nodes or reinstallation cannot be restored from coordinator metadata, so add them back to YAML.
