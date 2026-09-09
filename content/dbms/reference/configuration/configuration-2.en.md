---
type: docs
title: '16.2.2 Cluster Configuration Property Dictionary'
weight: 20
toc: true
---

Cluster Edition is configured through each node's configuration files in
`$MACHBASE_COORDINATOR_HOME/conf/`, `$MACHBASE_BROKER_HOME/conf/`, and
`$MACHBASE_WAREHOUSE_HOME/conf/`.

This page lists the main cluster properties used during operation.

## Coordinator Settings

The Coordinator manages cluster-wide metadata and node status.

| Property | Default | Description |
|----------|--------|------|
| `CLUSTER_LINK_HOST` | - | IP address to which the Coordinator binds |
| `CLUSTER_LINK_PORT_NO` | 3868 | Internal cluster communication port |
| `CLUSTER_LINK_THREAD_COUNT` | 16 | Number of cluster link processing threads |
| `CLUSTER_LINK_MAX_LISTEN` | 512 | Maximum cluster link listen connections |
| `CLUSTER_LINK_MAX_POLL` | 4096 | Maximum cluster link poll events |
| `CLUSTER_LINK_BUFFER_SIZE` | 33554432 | Cluster link buffer size in bytes. Default: 32MB |
| `HTTP_ADMIN_PORT` | 5779 | Coordinator/Deployer administration REST port |
| `HTTP_THREAD_COUNT` | 2 | Number of administration REST request threads |

`HTTP_ADMIN_PORT` can also be set with the `MACHBASE_HTTP_ADMIN_PORT` environment variable. This port
is used exclusively for cluster administration requests, rather than SQL queries or data ingestion.

## Cluster Link Timeouts

All values are in microseconds (μs).

| Property | Default (μs) | Description |
|----------|-----------|------|
| `CLUSTER_LINK_ACCEPT_TIMEOUT` | 5000000 | Accept timeout (5 seconds) |
| `CLUSTER_LINK_CHECK_INTERVAL` | 1000000 | Connection status check interval (1 second) |
| `CLUSTER_LINK_CONNECT_RETRY_TIMEOUT` | 60000000 | Maximum connection retry duration (60 seconds) |
| `CLUSTER_LINK_CONNECT_TIMEOUT` | 5000000 | Connection timeout (5 seconds) |
| `CLUSTER_LINK_HANDSHAKE_TIMEOUT` | 5000000 | Handshake timeout (5 seconds) |
| `CLUSTER_LINK_RECEIVE_TIMEOUT` | 30000000 | Receive timeout (30 seconds) |
| `CLUSTER_LINK_SEND_TIMEOUT` | 30000000 | Send timeout (30 seconds) |
| `CLUSTER_LINK_REQUEST_TIMEOUT` | 60000000 | Request timeout (60 seconds) |
| `CLUSTER_LINK_SESSION_TIMEOUT` | 3600000000 | Session timeout (1 hour) |
| `CLUSTER_LINK_LONG_WAIT_INTERVAL` | 1000000 | Long wait interval (1 second) |
| `CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL` | 1000000 | Long-term callback interval (1 second) |

## Broker Settings

A Broker accepts client queries and distributes processing across Warehouses. Its `machbase.conf`
contains common server and cluster settings. Supported properties and defaults vary by edition
and node role; do not apply a Standard Edition configuration file unchanged.

| Property | Default | Description |
|----------|--------|------|
| `PORT_NO` | 5656 | Client connection port |
| `QUERY_PARALLEL_FACTOR` | 4 | Number of parallel query processing threads (Cluster default) |
| `CLUSTER_LINK_HOST` | - | IP address to which the Broker binds for cluster communication |
| `CLUSTER_LINK_PORT_NO` | - | Broker cluster communication port |

## Warehouse Settings

A Warehouse stores and processes the actual data. It uses the following cluster settings in addition
to storage settings. Properties exclusive to Standard Edition, such as `DDL_LOCK_TIMEOUT`,
are not supported in Cluster Edition.

| Property | Default | Description |
|----------|--------|------|
| `PORT_NO` | 5656 | Warehouse service port |
| `CLUSTER_LINK_HOST` | - | IP address to which the Warehouse binds for cluster communication |
| `CLUSTER_LINK_PORT_NO` | - | Warehouse cluster communication port |
| `DBS_PATH` | ?/dbs | Warehouse data file directory |

## Checking Cluster Configuration

Use `machcoordinatoradmin --configure` to display cluster settings.

```bash
machcoordinatoradmin --configure
```

To check an individual setting, use `--configuration=name`.

```bash
machcoordinatoradmin --configuration=decision
```

## Example Cluster Port Allocation

The following example assigns ports for a cluster on a single host.

| Node | Service Port | HTTP Port | Cluster Link Port |
|------|------------|-----------|------------------|
| Coordinator | - | 5102 | 5101 |
| Deployer | - | - | 5201 |
| Broker | 5757 | 5302 | 5301 |
| Warehouse-A1 | 5400 | 5402 | 5401 |
| Warehouse-A2 | 5500 | 5502 | 5501 |
