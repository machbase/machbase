---
type: docs
title: '3.3 Cluster Edition Installation and Deployment'
weight: 30
toc: true
---

Cluster Edition separates SQL connections, storage, replication, and node management into
different roles. Before installation, assign each role to a host and choose its ports and
storage paths. Ordinary SQL connections go to Brokers; administration commands go to the
appropriate management node.

## Node Roles

| Node | Role |
|---|---|
| Coordinator | Manage cluster metadata and monitor node state |
| Deployer | Deploy packages and initialize nodes |
| Lookup | Process reference data and related requests |
| Broker | Accept client SQL, parse it, and distribute queries |
| Warehouse | Store data and execute queries |

The YAML example below uses three hosts with two Coordinators, three Deployers, two Lookup
nodes (one master and one monitor), two Brokers, and two Warehouses in one replication group.
Choose actual node counts and placement according to availability, throughput, and the
capacity that must remain after a failure.

## Deployment Methods

| Method | Description | When to use it |
|---|---|---|
| [machclusterctl](#machclusterctl) | Automated deployment from `cluster.yaml` | Recommended starting point for new installations |
| [Manual administration](#manual-machcoordinatoradmin) | Register and deploy nodes through Coordinator commands | When individual steps require direct control |

## Installation Order

1. Understand the [Cluster Configuration](#overview).
2. Complete [Environment Preparation](#preparation-environment-cluster-edition), including SSH,
   kernel settings, and clock synchronization.
3. Prepare packages, paths, and the [License](../pre-install-preparation/#license) installation method.
4. Deploy, start, and verify licensing using the chosen method.
5. Complete [Installation Validation](../validation-checklist/).

<a id="overview"></a>

## Cluster Configuration Overview

Coordinator, Deployer, Lookup, Broker, and Warehouse have separate responsibilities.
Understand their relationships before planning deployment.

### Node Roles in Detail

#### Coordinator

The Coordinator manages metadata, node registration, and monitoring. Consider Primary/Secondary
redundancy. Although management and running data-processing paths are separate, Coordinator
failure alone does not establish whether all SQL will continue. Check other nodes and client
impact and follow a tested recovery procedure.

- Configuration: `$MACHBASE_COORDINATOR_HOME/conf/machbase.conf`
- Tool: `machcoordinatoradmin`
- Main ports: `CLUSTER_LINK_PORT_NO`, `HTTP_ADMIN_PORT`

The defaults are `CLUSTER_LINK_PORT_NO=3868` and `HTTP_ADMIN_PORT=5779`. This chapter
explicitly uses `5101` and `5102` for the Coordinator link and management ports to avoid conflicts.

#### Deployer

The Deployer carries out package deployment and initialization requested by the Coordinator.
Place one on each node host or operate it on a separate deployment server.

- Tool: `machdeployeradmin`

#### Lookup

Lookup nodes process reference data. Their configured roles are `master`, `monitor`, or
`slave`.

#### Broker

Brokers accept and parse client SQL and distribute work to Warehouses. Ordinary applications
connect to Broker addresses. Direct Warehouse connections are for management diagnostics,
such as comparing replicas, and are separate from application connection paths. Redundant Brokers
are recommended.

- Default client connection port: 5656

#### Warehouse

Warehouses store data and execute queries. Members of the same group replicate data for
availability. At least two members per group are recommended.

### Configuration Illustration

```
[Client]
     │ (SQL, 5656)
     ▼
[Broker ×2]  ──────────────────────────────────────────
     │ (Query distribution)
     ├─► [Warehouse group1-node1] ◄──Replication──► [Warehouse group1-node2]
     └─► [Warehouse group2-node1] ◄──Replication──► [Warehouse group2-node2]

[Coordinator Primary] ◄──HA──► [Coordinator Secondary]
     │ (Metadata and node monitoring)
[Deployer]
     │
[Lookup master / monitor]
```

### Edition Comparison

See
[Standard and Cluster Differences](../../core-concepts/concepts-edition/#differences-standard-edition-cluster).

<a id="preparation-environment-cluster-edition"></a>

## Prepare the Cluster Environment

Prepare the following on the relevant hosts before deployment.

### File Descriptor Limit

Edit the limit configuration on each node host:

```bash
sudo vi /etc/security/limits.conf
```

```
*  hard  nofile  65535
*  soft  nofile  65535
```

Check the result in a new login session as the server account. If a service manager starts
the process, also check that service's file descriptor limit.

```bash
ulimit -Sn
# 65535
```

### Create OS Users

Create the `machbase` account on each host:

```bash
sudo useradd -m machbase --home-dir /home/machbase
sudo passwd machbase
```

### SSH Key Authentication

For `machclusterctl`, the deployment host must be able to connect to all target hosts using
noninteractive key-based SSH.

```bash
# Create a key on the deployment host; skip if one already exists
ssh-keygen -t rsa -b 4096

# Register the public key on each target host
ssh-copy-id machbase@192.168.1.11
```

The address is an example; repeat registration and verification for every target host.
Check that the connection works without a password:

```bash
ssh machbase@192.168.1.11 'hostname'
```

### Network Kernel Parameters

These are tuning examples, not required values for every server. First measure current
kernel settings, memory use, and network bottlenecks. Compare memory and latency as well as
throughput after changes, and persist only changes that have been validated.

```bash
sudo sysctl -w net.core.rmem_default=33554432
sudo sysctl -w net.core.wmem_default=33554432
sudo sysctl -w net.core.rmem_max=268435456
sudo sysctl -w net.core.wmem_max=268435456
sudo sysctl -w 'net.ipv4.tcp_rmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_wmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_mem=8388608 8388608 8388608'
```

To make validated settings persistent, add them to `/etc/sysctl.conf`.

### Time Synchronization

Synchronize all node clocks with NTP or `chrony`.

```bash
# Example with chrony
sudo systemctl enable chronyd
sudo systemctl start chronyd
chronyc tracking
```

An isolated installation environment without a time server can set its initial clock manually.
Replace this illustrative timestamp with the actual current time. A manual setting does not
continuously correct clock drift; establish clock synchronization before production.

```bash
sudo date -s "2025-01-02 12:34:56"
```

### Reserve Ports

Reserve the ports used by Machbase on each host.

```bash
current=$(cat /proc/sys/net/ipv4/ip_local_reserved_ports)
ports=5101-5110,5201-5202,5301-5302,5401,5500-5503,5656
sudo sysctl -w net.ipv4.ip_local_reserved_ports="${current:+$current,}$ports"
```

Merge existing reservations rather than overwriting them. Adjust the ranges for the actual
configuration, including cluster links, Coordinator/Deployer management, service ports, and
Warehouse replication-manager ports.

<a id="machclusterctl"></a>

## Deploy with machclusterctl

`machclusterctl` deploys and manages a cluster from `cluster.yaml`. It uses SSH to deploy
packages, initialize nodes, and coordinate startup and shutdown.

### Prerequisites

- Run commands on the host that will contain the Primary Coordinator. The package and SSH
  private key must be readable there.
- Configure key-based SSH from that host to every target host.
- Ensure permission to create and write the parent directories of each node's `home_path`
  and `dbs_path`.
- If a separate license is required, prepare the package and licensing procedure before automatic
  startup. Do not invent a license property in the YAML.
- Complete [Cluster Environment Preparation](#preparation-environment-cluster-edition).

### Workflow

| Step | Document |
|---|---|
| 1. Write cluster.yaml | [YAML Configuration](#machclusterctl-cluster-yaml) |
| 2. Validate it | [YAML Validation](#machclusterctl-validation-yaml) |
| 3. Install and start | [Initial Installation](#machclusterctl-initial) |
| 4. Inspect state | [Status Checks](#machclusterctl-status-check-state) |
| 5. Make later configuration changes | [Cluster Operations](../../operations-configuration-recovery/cluster/) |
| 6. Diagnose a failure | [Cluster Troubleshooting](../../troubleshooting/cluster/) |

<a id="machclusterctl-cluster-yaml"></a>

### Write cluster.yaml

`cluster.yaml` declares the nodes and their paths. Replace the example addresses with actual hosts.
`origin_path` is the archive read on the Primary Coordinator host where the command runs.
`home_path` and `dbs_path` belong to the node's host. `deployer` references the Deployer
that will deploy and control that node.

#### Example File

```yaml
version: "1"

cluster:
  name: mc-prod

  hosts:
    node1:
      address: machbase@192.168.1.10
    node2:
      address: machbase@192.168.1.11
    node3:
      address: machbase@192.168.1.12

  package:
    name: machbase
    origin_path: /home/machbase/packages/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz

  ssh:
    key_file: /home/machbase/.ssh/id_rsa

  defaults:
    coordinator:
      home_path: /home/machbase/coordinator
      cluster_link_port: 5101
      http_admin_port: 5102
    deployer:
      home_path: /home/machbase/deployer
      cluster_link_port: 5201
      http_admin_port: 5202
    lookup:
      home_path: /home/machbase/lookup
      cluster_link_port: 5301
    broker:
      home_path: /home/machbase/broker
      cluster_link_port: 5401
      service_port: 5656
    warehouse:
      home_path: /home/machbase/warehouse
      cluster_link_port: 5501
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

  brokers:
    - alias: broker-1
      host: node1
      deployer: deployer-1
      dbs_path: /data/machbase/broker-1/dbs

    - alias: broker-2
      host: node2
      deployer: deployer-2

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node2
          deployer: deployer-2
          dbs_path: /data/machbase/warehouse-group1-1/dbs

        - alias: warehouse-group1-2
          host: node3
          deployer: deployer-3
          dbs_path: /data/machbase/warehouse-group1-2/dbs
```

#### Field Reference

| Field | Meaning |
|---|---|
| `version` | YAML schema version; currently `"1"` |
| `cluster.name` | Cluster identifier, also used for `destroy` confirmation |
| `cluster.hosts` | Host aliases and SSH `address` values in `user@host` form |
| `cluster.package.name` | Package name registered with the Coordinator |
| `cluster.package.origin_path` | Input archive for `install`, `apply`, and `upgrade` |
| `cluster.package.registered_path` | Observed Coordinator package-store path recorded by `export`; not an input archive |
| `cluster.ssh.key_file` | SSH private-key path; no password field is used |
| `cluster.defaults` | Role-specific `home_path`, `cluster_link_port`, and `service_port` defaults |
| `cluster.coordinators` | Coordinator nodes; `role` is `primary` or `secondary` |
| `cluster.deployers` | Deployer nodes |
| `cluster.lookup` | Lookup nodes; `type` is `master`, `monitor`, or `slave` |
| `cluster.brokers` | Broker nodes; clients connect to `service_port` |
| `cluster.warehouse_groups` | Warehouse groups and their members |

#### Redundancy and Placement

Recommended configuration:

- Two Coordinators: Primary and Secondary for high availability.
- One or more Deployers.
- One Lookup `master` and at least one `monitor`.
- Two or more Brokers for load balancing.
- Two Warehouses per group for replication and high availability.

If several nodes of the same type share one host, explicitly give the additional nodes
different `home_path` values and ports. Coordinator and Deployer management use `http_admin_port`.

Broker and Warehouse nodes can specify `dbs_path`; it is a path on the node's host. If omitted,
the normal `DBS_PATH` behavior of `machcoordinatoradmin --add-node` applies.
The legacy `cluster.package.path` remains a compatibility input, but new YAML should use
`origin_path`. Only Coordinator and Deployer use `http_admin_port`; do not configure HTTP
ports for Broker, Lookup, or Warehouse.

Validate the file after editing.

<a id="machclusterctl-validation-yaml"></a>

### Validate the YAML

`validate` statically checks syntax, required values, aliases, port conflicts, and topology.

#### Validation Command

```bash
machclusterctl validate -f cluster.yaml
```

#### Checks

| Item | Validation |
|---|---|
| YAML syntax | Parsing errors |
| Environment substitution | `${VAR}` and `${VAR:-default}` expressions |
| Required fields | Cluster, hosts, package, and required node values |
| Aliases | Duplicate node aliases |
| Ports | Declared conflicts on the same host |
| Topology | Primary Coordinator, Lookup master/monitor, and Deployer references |

#### Example Output

```text
Validation passed.
```

Correct reported errors and validate again.

#### Inspect the Installation Plan

Use `install --dry-run --verbose` to inspect SSH access, package availability, remote directory
permissions, and the proposed actions.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

After installation, `apply --dry-run` compares current state with the YAML and displays the
change plan without applying remote changes.

```bash
machclusterctl apply -f cluster.yaml --dry-run --verbose
```

#### Common Errors

| Error | Cause | Correction |
|---|---|---|
| `field ... not found` | Unsupported YAML key | Use a supported `cluster.*` field |
| `required field ...` | Missing value | Add the reported field |
| `duplicate alias` | Reused alias | Assign unique node aliases |
| `port conflict` | Same port on the same host | Change the conflicting port; changing only the home path does not resolve it |
| `deployer ... not found` | Unknown Deployer reference | Set `deployer` to a configured Deployer alias or host:port |

<a id="machclusterctl-initial"></a>

### Initial Installation

After preparing and validating the YAML, inspect the plan before installing.

#### 1. Install the Cluster

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

If the checks pass, perform the installation:

```bash
machclusterctl install -f cluster.yaml --yes --verbose
```

The command automatically performs these steps:

1. Copies and extracts packages on each node.
2. Generates each node's `machbase.conf` and configures ports.
3. Initializes the Coordinator database.
4. Registers each node with the Coordinator.

#### 2. Start the Cluster

`install` prepares and starts the Coordinator, Deployers, Lookup, Brokers, and Warehouses.
Use the following only when you need to start the installed cluster again:

```bash
machclusterctl start
```

<a id="machclusterctl-status-check-state"></a>

#### 3. Check State

```bash
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
machclusterctl status
```

To explicitly select a Coordinator home when several are managed from one host:

```bash
machclusterctl status --coordinator /home/machbase/coordinator
```

Output follows `machcoordinatoradmin --cluster-status-full --verbose`. The following is a
partial illustration of the columns, not the complete node list from the YAML. Coordinator
and Broker can show role states such as `primary` or `leader`. Compare registered node counts
and role-specific desired and actual states, rather than requiring every row to say `normal`.

```
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
|  Node Type  |           Node Name            |           Group Name           |           Group State          |    Desired & Actual State     |  RP State   | Disk(%) (00/00) | Ping(μs) |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
| coordinator | coord-1(192.168.1.10:5101)     | Coordinator                    | normal                         | primary       | primary       | ----------- | --------------- |      214 |
| deployer    | deployer-1(192.168.1.10:5201)  | Deployer                       | normal                         | running       | running       | ----------- | --------------- |      100 |
| broker      | broker-1(192.168.1.11:5401)    | Broker                         | normal                         | leader        | leader        | ----------- | --------------- |      100 |
| warehouse   | wh-g1-1(192.168.1.13:5501)     | group1                         | normal                         | normal        | normal        | running     | 26.9            |      100 |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
```

#### 4. Test Client Connections

Connect to a Broker IP and its SQL port:

```bash
machsql -s 192.168.1.11 -P 5656 -u SYS -p MANAGER
# Mach>
```

#### Stop the Cluster

```bash
machclusterctl stop
```

<a id="cluster-post-install-operations"></a>
<a id="machclusterctl-configuration-change-alter"></a>
<a id="machclusterctl-failure-recovery"></a>

### After Installation

For topology changes, node addition/removal, and recovery, follow
[Cluster Operations](../../operations-configuration-recovery/cluster/).
For failure classification and recovery decisions, see
[Cluster Troubleshooting](../../troubleshooting/cluster/).

<a id="manual-machcoordinatoradmin"></a>

## Deploy Manually with machcoordinatoradmin

If `machclusterctl` is unavailable, prepare Coordinator and Deployer processes directly,
then register packages and nodes. Do not repeat creation commands in an already deployed
cluster. The manual example is separate from the YAML example above.
Run each command on the host for its corresponding role.

| Host | Roles |
|---|---|
| `192.168.1.10` | Primary Coordinator, Deployer, Lookup master |
| `192.168.1.11` | Deployer, Lookup monitor, Broker |
| `192.168.1.13` | Deployer, first Warehouse in group1 |
| `192.168.1.14` | Deployer, replica Warehouse in group1 |
| `192.168.1.20` | Optional Secondary Coordinator |

Separate homes and ports for roles on the same host. Prepare a Deployer on each host containing
data-processing nodes and match the node's `--deployer` address to that host.

### Manual Deployment Order

1. Read [Package Preparation](#manual-machcoordinatoradmin-package) and prepare full and lightweight
   packages.
2. Install and start [Coordinator and Deployers](#manual-machcoordinatoradmin-coordinator-deployer).
3. [Register the lightweight package](#manual-machcoordinatoradmin-package) with the running Coordinator.
4. Register and start [Lookup, Broker, and Warehouse](#manual-machcoordinatoradmin-lookup-broker-warehouse).
5. [Check overall state](#manual-machcoordinatoradmin-lookup-broker-warehouse) after registration and startup.

### Comparison with machclusterctl

| Item | machclusterctl | Manual deployment |
|---|---|---|
| Configuration | One `cluster.yaml` | Edit each node's `machbase.conf` |
| Package deployment | Automated remote copy | Direct Coordinator/Deployer installation; Deployer installs data-processing nodes |
| Node registration | Automatic | `machcoordinatoradmin --add-node` |
| Start and stop | `machclusterctl start/stop` | Individual node commands |

Manual deployment offers direct control but requires tracking every host and role.
For new installations, start with `machclusterctl` when available.

<a id="manual-machcoordinatoradmin-package"></a>

### Package Preparation and Registration

Install the full package on Coordinator and Deployer hosts. Register the lightweight package
used for Broker and Warehouse deployment only after the Coordinator is running.

#### Package Types

| Package | Target | Contents |
|---|---|---|
| Full | Coordinator and Deployer | All executables |
| Lightweight | Broker and Warehouse | Only data-processing files; smaller package |

Example filenames:

- Full: `machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz`
- Lightweight: `machbase-cluster-8.7.0.official-LINUX-X86-64-release-lightweight.tgz`

#### Install Full Packages

##### Coordinator Host

```bash
# Run on the Coordinator host
mkdir -p /home/machbase/coordinator
scp machbase@package-host:/path/to/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz /home/machbase/
tar zxf /home/machbase/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz -C /home/machbase/coordinator
```

##### Each Deployer Host

```bash
mkdir -p /home/machbase/deployer
scp machbase@package-host:/path/to/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz /home/machbase/
tar zxf /home/machbase/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz -C /home/machbase/deployer
```

Do not manually extract the lightweight package into Broker or Warehouse homes here.
After it is registered, the Deployer selected by `--add-node` deploys it to `--home-path`.

#### Register the Package with the Coordinator

Install Coordinator and Deployer first, then register the package with the running Coordinator:

```bash
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-package=machbase \
  --file-name="/home/machbase/machbase-cluster-8.7.0.official-LINUX-X86-64-release-lightweight.tgz"
```

Broker and Warehouse registration later references it as `--package-name=machbase`.

#### Set Role-Specific Environments

Replace `package-host` and `/path/to/` with the actual package location.
Use separate management shells for Coordinator and Deployer even when they share a host.
Apply these settings to the appropriate shell and use the same values for services or login
initialization files.

```bash
# Coordinator management shell
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
export MACHBASE_HOME=$MACHBASE_COORDINATOR_HOME
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

```bash
# Separate Deployer management shell
export MACHBASE_DEPLOYER_HOME=/home/machbase/deployer
export MACHBASE_HOME=$MACHBASE_DEPLOYER_HOME
export PATH="$MACHBASE_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$MACHBASE_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

<a id="manual-machcoordinatoradmin-coordinator-deployer"></a>

### Install Coordinator and Deployers

Prepare the packages first, then start the Coordinator before registering Deployers.

#### Coordinator

##### 1. Configure machbase.conf

Edit `$MACHBASE_COORDINATOR_HOME/conf/machbase.conf`:

```bash
vi $MACHBASE_COORDINATOR_HOME/conf/machbase.conf
```

Use this host's address and the planned ports:

```
CLUSTER_LINK_HOST    = 192.168.1.10   # This host's IP
CLUSTER_LINK_PORT_NO = 5101
HTTP_ADMIN_PORT      = 5102
```

##### 2. Create Metadata and Start

```bash
machcoordinatoradmin -c
machcoordinatoradmin -u
```

##### 3. Register the Coordinator Itself

```bash
machcoordinatoradmin --add-node="192.168.1.10:5101" \
  --node-type=coordinator \
  --http-admin-port=5102
```

##### 4. Verify Registration

```bash
machcoordinatoradmin --cluster-status
```

#### Optional Secondary Coordinator

For redundancy, prepare the Secondary package and configuration on its own host.
Register it from the **Primary Coordinator first**, then start it on the Secondary host.

```bash
# Register from the Primary first
machcoordinatoradmin --add-node="192.168.1.20:5101" \
  --node-type=coordinator \
  --http-admin-port=5102

# Then start on the Secondary host, specifying the Primary
machcoordinatoradmin -u --primary=192.168.1.10:5101
```

Complete Primary registration before starting the Secondary.

#### Deployer

Perform these steps on every Deployer host in the manual layout. Replace
`CLUSTER_LINK_HOST` with that host's own IP. Copying another host's address would make the
communication address inconsistent with the actual process location.

##### 1. Configure machbase.conf

```
CLUSTER_LINK_HOST    = 192.168.1.10   # Deployer host IP
CLUSTER_LINK_PORT_NO = 5201
HTTP_ADMIN_PORT      = 5202
```

##### 2. Start the Deployer

```bash
machdeployeradmin -c
machdeployeradmin -u
```

##### 3. Register Deployers with the Coordinator

After all Deployers are running, use the Primary Coordinator's management shell:

```bash
machcoordinatoradmin --add-node="192.168.1.10:5201" \
  --node-type=deployer \
  --http-admin-port=5202

machcoordinatoradmin --add-node="192.168.1.11:5201" \
  --node-type=deployer --http-admin-port=5202
machcoordinatoradmin --add-node="192.168.1.13:5201" \
  --node-type=deployer --http-admin-port=5202
machcoordinatoradmin --add-node="192.168.1.14:5201" \
  --node-type=deployer --http-admin-port=5202
```

<a id="manual-machcoordinatoradmin-lookup-broker-warehouse"></a>

### Install Lookup, Broker, and Warehouse

Prepare Coordinator and Deployers first. Register the lightweight package with the Coordinator
with `--add-package` before adding Broker or Warehouse nodes.

<a id="lookup-노드-선택"></a>

#### Lookup Nodes

Register and start the master and monitor. This example places them on the Primary and Broker
hosts, using the local Deployer on each. Confirm that the homes are not used by existing Lookup
nodes.

```bash
machcoordinatoradmin --add-node="192.168.1.10:5301" \
  --node-type=lookup \
  --lookup-type=master \
  --deployer="192.168.1.10:5201" \
  --home-path="/home/machbase/lookup"

machcoordinatoradmin --add-node="192.168.1.11:5301" \
  --node-type=lookup \
  --lookup-type=monitor \
  --deployer="192.168.1.11:5201" \
  --home-path="/home/machbase/lookup"

machcoordinatoradmin --startup-node="192.168.1.10:5301"
machcoordinatoradmin --startup-node="192.168.1.11:5301"
```

#### Broker

##### 1. Check Registration Settings

The node configuration is generated during `--add-node` and deployed through the Deployer. Choose
the cluster link and
SQL service ports before registration. Do not configure an HTTP management port for Broker.

```
CLUSTER_LINK_HOST    = 192.168.1.11   # Broker host IP
CLUSTER_LINK_PORT_NO = 5401
PORT_NO              = 5656           # Client SQL port
```

##### 2. Register from the Coordinator

```bash
machcoordinatoradmin --add-node="192.168.1.11:5401" \
  --node-type=broker \
  --deployer="192.168.1.11:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/broker" \
  --dbs-path="/data/machbase/broker_dbs" \
  --port-no=5656
```

| Parameter | Meaning |
|---|---|
| `--add-node` | Node IP:CLUSTER_LINK_PORT_NO |
| `--node-type` | `broker`, `warehouse`, or `lookup` |
| `--deployer` | IP:CLUSTER_LINK_PORT_NO of the Deployer that installs and controls the node |
| `--package-name` | Registered package name |
| `--home-path` | Node installation home |
| `--dbs-path` | Broker/Warehouse data path; otherwise uses the default `DBS_PATH` |
| `--port-no` | SQL or node service port |
| `--replication` | Warehouse replication-manager address in `host:port` form |

##### 3. Start the Node

From the Coordinator:

```bash
machcoordinatoradmin --startup-node="192.168.1.11:5401"
```

#### Warehouses

Warehouse nodes belong to groups. Nodes in the same group replicate data.

##### 1. Check Registration Settings

The configuration is generated during registration and deployed through the Deployer. Establish the
cluster link,
service port, and replication-manager address beforehand.

```
CLUSTER_LINK_HOST    = 192.168.1.13
CLUSTER_LINK_PORT_NO = 5501
PORT_NO              = 5500
```

##### 2. Register the Nodes

```bash
machcoordinatoradmin --add-node="192.168.1.13:5501" \
  --node-type=warehouse \
  --deployer="192.168.1.13:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/warehouse_g1_1" \
  --dbs-path="/data/machbase/warehouse_g1_1_dbs" \
  --port-no=5500 \
  --replication=192.168.1.13:5502 \
  --group=group1 \
  --no-replicate

machcoordinatoradmin --add-node="192.168.1.14:5501" \
  --node-type=warehouse \
  --deployer="192.168.1.14:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/warehouse_g1_2" \
  --dbs-path="/data/machbase/warehouse_g1_2_dbs" \
  --port-no=5500 \
  --replication=192.168.1.14:5502 \
  --group=group1
```

There is no separate `--add-group` step. Specify the Warehouse group with `--group` when
registering each node.

##### 3. Start the Nodes

```bash
machcoordinatoradmin --startup-node="192.168.1.13:5501"
machcoordinatoradmin --startup-node="192.168.1.14:5501"
```

<a id="manual-machcoordinatoradmin-status-check-node-state"></a>

#### Check All Nodes

```bash
machcoordinatoradmin --cluster-status
```

Compare role-specific states: Coordinator may be `primary`, Broker `leader`, and Warehouses
`normal`, `sync-active`, or `sync-standby`. Verify the configured node list rather than
one universal state string.

#### Verify the First Connection

Connect to the Broker SQL port and run `SELECT CURRENT_DATABASE();` and a representative query.
For subsequent node control and recovery, use
[Cluster Operations](../../operations-configuration-recovery/cluster/) and
[Cluster Troubleshooting](../../troubleshooting/cluster/).
