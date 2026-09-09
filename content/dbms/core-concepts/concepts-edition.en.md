---
type: docs
title: '2.4 Edition Concepts'
weight: 40
toc: true
---

The Edition determines the deployment architecture and supported features. Standard starts with
one server; Cluster divides storage and processing among several nodes. Choose based on the
required SQL features, growth rate, failure recovery, and operational capacity, as well as the
current data size.

<a id="differences-standard-edition-cluster"></a>

## Differences Between Standard and Cluster Editions

### Standard Edition

A single DBMS server handles SQL processing and data storage. You do not need to manage deployment
and communication across distributed nodes, making it suitable for development and single-server
operations. Check whether you need Standard-only features such as TRANSACTION tables, Restore,
or Mount.

Starting with one server does not necessarily mean the data set must be small. Measure whether
the ingestion volume, query workload, and retention period fit within that server's CPU, memory,
and storage capacity.

### Cluster Edition

Coordinator, Deployer, Broker, Warehouse, and Lookup nodes have different roles.

| Node type | Role |
|---|---|
| Coordinator | Manage cluster metadata and node state |
| Deployer | Deploy packages and manage nodes |
| Broker | Accept application SQL connections and distribute queries |
| Warehouse | Store time-series data and execute queries |
| Lookup | Process cluster reference data |

Ordinary SQL applications connect to a Broker. Management tools use role-specific endpoints and
ports, so distinguish SQL connection addresses from management addresses.

Distributing data across Warehouse groups and replicating data within a group serve different
purposes. Distribution expands capacity and throughput; replication helps with failure recovery.
Design node counts, replication state, client reconnection, and recovery procedures together.

### Feature Support Differences

| Item to check | Standard Edition | Cluster Edition |
|---|---|---|
| Main deployment structure | One DBMS server | Multiple nodes with separate roles |
| TRANSACTION tables | Supported | Not supported |
| Restore and Mount | Supported | Not supported |
| Capacity and processing expansion | Expand server resources and storage configuration | Expand distributed groups and node configuration |
| Failure recovery design | Backups, recovery procedures, and server operations | Node and group replication, state, connection handling, and recovery procedures |

Shared features such as LOG, TAG, LOOKUP, VOLATILE, ROLLUP, and Retention do not necessarily have
identical DML, DDL, or operational restrictions. For complete support information, see
[Edition Support](../../reference/support-scope-constraints/edition/) and
[Table Type Support](../../reference/support-scope-constraints/table-types-type/).

### Selection Criteria

1. Identify required features. If you need TRANSACTION tables, Restore, or Mount, first review
   Standard Edition support.
2. Run representative ingestion and queries. Use realistic data types, concurrent connections,
   query ranges, and retention periods to measure available capacity on one server.
3. Account for data growth and failure requirements. If you need distribution beyond one server,
   also consider Cluster's network, replication, and node-management costs.
4. Test failure scenarios. Monitoring nodes does not by itself guarantee uninterrupted recovery.
   Measure recovery time and verify application reconnection and retry behavior.

Changing Editions in production involves more than increasing the server count. First verify
compatibility for your SQL and SDKs, data migration, backups, and recovery methods.

## Related Documentation

- [Storage and Execution Architecture](../storage-execution-architecture/) explains the processing
  flow.
- [Installation, Deployment, and Upgrade](../../installation-deployment-upgrade/) describes
  deployment procedures.
- [Versions and Compatibility](../../reference/support-scope-constraints/compatibility-version/)
  lists version-specific support.
- [Relational Business Models and Time-Series Models](../concepts/#differences-rdbms) explains
  data-model selection criteria.
