---
type: docs
title: '13.9 Cluster Operations'
weight: 100
toc: true
aliases:
---

Perform Cluster operations with a verified runbook after checking node configuration, roles,
replication, and data state. Use the checks on this page to assess change impact and recovery
paths, then include commands from the installed management tool version in the runbook.

## Components

| Role | Check |
|------|------|
| Coordinator | Node configuration and status |
| Deployer | Package and node deployment |
| Broker | Client connections and query routing |
| Warehouse | Data storage and query processing |
| Lookup | Reference data service |

Design node counts and placement around availability, throughput, and failure domain requirements.
Do not apply a fixed node count or hardware specification to every environment.

<a id="status-check-state-cluster"></a>

## Check status

Before and after a change, check the full node configuration from the Coordinator and each
node's processes and resources. Use the installed tool's help for status strings and options.

```bash
machcoordinatoradmin --help
machclusterctl --help
```

- Are all expected nodes registered?
- Do node roles, hosts, ports, and groups match deployment records?
- Are service, replication, and scrap states normal?
- Are CPU, memory, disk, or network resources unevenly used across nodes?
- Do actual connections and queries through the Broker succeed?

<a id="machclusterctl-connect-export"></a>

<a id="connect와-설정-export"></a>

## Connect and export configuration

When using `machclusterctl connect`, specify the target Broker and native port, then verify
`CURRENT_DATABASE()` and a sample query. Configuration exports may contain hosts, ports, paths,
and operational information. Restrict access and review the diff before importing.

<a id="node-start-cluster"></a>

<a id="node-시작종료"></a>

## Start and stop nodes

Before controlling a node, check:

1. Target node name, alias, host, and role.
2. Client connections and active queries and Appenders.
3. Warehouse group redundancy and data state.
4. Remaining capacity while the node is stopped.
5. Startup and shutdown order and rollback steps.
6. Acceptance criteria after maintenance.

Use a forced shutdown only after normal shutdown repeatedly fails and you have assessed its
data and recovery impact. Do not immediately kill a process on a timeout.

<a id="machclusterctl-start-stop-destroy"></a>

## Control the entire Cluster and use destroy

For full startup and shutdown, check the dependency order of Coordinator, Deployer, Broker,
Warehouse, and Lookup in the runbook for the current release. `destroy` is destructive and may
remove node configuration and data.

- Confirm that the target is not another cluster with a similar name.
- Verify a recent backup and a successful restore.
- Obtain service owner approval and block clients.
- Check the deletion scope, including external `DBS_PATH` locations.
- Identify changes that cannot be rolled back.
- After execution, check each host for remaining processes and paths.

Do not use `destroy` for routine state recovery.

<a id="node-cluster"></a>

<a id="node-추가제거"></a>

## Add and remove nodes

Before adding a node, check the package, version, ports, paths, file systems, and network.
Before removal, verify data redundancy and completed migration, along with aliases, groups,
and monitoring that reference the node. Removing a node may delete its home and data paths;
check the command's help and validate the exact scope in a test environment.

<a id="state-alter-status-cluster"></a>

## Change state

Disabling a Broker, making a Warehouse group read-only, and scrapping a node serve different
purposes. Do not change state arbitrarily to hide a failing node.

| Purpose | Check first |
|------|-----------|
| Block new connections | Broker draining and existing connections |
| Stop writes | Warehouse group and active Append operations |
| Isolate a node | Evidence of replication problems or data corruption |
| Return to service | Health, data synchronization, and sample queries |

<a id="recovery-state-status-warehouse"></a>

## Recover a Warehouse

1. Preserve the failure time and first error.
2. Check processes, disks, network, and replication state.
3. Assess redundancy on remaining nodes and the service impact.
4. Choose a supported recovery path: restart, reattach, or rebuild.
5. Monitor progress and errors.
6. After recovery, compare row counts, time ranges, and query results across nodes.

Do not force a node to normal state without checking for data corruption.

<a id="limitations-cluster"></a>

## Constraints and checklist

For edition-specific support for SQL, ROLLUP, backups, and ALTER SYSTEM, see
[Support Scope](/dbms/reference/support-scope-constraints/).

- Are all node and client SDK releases compatible?
- Are permitted reads and writes during maintenance defined?
- Have backup, restore, and node recovery drills been completed?
- Have two operators cross-checked hosts, ports, and paths?
- Do monitoring and alerts reflect the new node configuration?
- Have Broker connections, queries, Append, and metadata been verified after the change?
