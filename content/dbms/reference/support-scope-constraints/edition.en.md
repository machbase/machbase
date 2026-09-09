---
type: docs
title: '16.6.1 Feature Support by Edition'
weight: 10
toc: true
---

Machbase provides **Standard Edition** for a single server and **Cluster Edition** for horizontal
scaling across nodes. They share core time-series features, but supported features differ according
to scalability and high availability requirements.

## Feature Comparison

| Feature | Standard | Cluster | Notes |
|------|:--------:|:-------:|------|
| **Table Types** | | | |
| TAG tables | O | O | |
| LOG tables | O | O | |
| LOOKUP tables | O | O | |
| TRANSACTION tables | O | X | Not supported in Cluster Edition |
| VOLATILE tables | O | O | Check the node and restart lifecycle of in-memory data in your deployment |
| **Data Management** | | | |
| ROLLUP (basic) | O | O | |
| Custom ROLLUP | O | X | Not supported in Cluster Edition |
| ROLLUP_REBUILD | O | X | Not supported in Cluster Edition |
| **Backup and Recovery** | | | |
| Multiple logical databases | O | X | Standard Edition only. No physical CPU, memory, or disk quotas per database |
| BACKUP DATABASE | O | O | |
| BACKUP TABLE | O | O | |
| MOUNT DATABASE | O | X | Not supported in Cluster Edition |
| UMOUNT DATABASE | O | X | Not supported in Cluster Edition |
| machadmin -r restore | O | X | Not supported in Cluster Edition |
| **Scalability and HA** | | | |
| Horizontal scaling | X | O | Scale by adding Warehouse nodes |
| HA (high availability) | X | O | Broker/Warehouse redundancy |
| AUTH KEY authentication | O | O | |

## Cluster Edition Constraints

Cluster Edition has constraints on local file operations centered on a single node and on
TRANSACTION features.

- **TRANSACTION tables**: TRANSACTION tables providing ACID transactions are not supported in the distributed environment. Integrate with an external RDBMS for data requiring transactions.
- **VOLATILE tables**: Creation and DML are supported, but in-memory data is local to each node and is not shared
  across nodes. Verify data visibility with the connected Broker, routing, and node restarts.
- **MOUNT/UMOUNT**: Local filesystem backup mounts are not supported in the distributed environment.
- **Custom ROLLUP / ROLLUP_REBUILD**: Custom rollup redefinition and rebuilding are not supported because the distributed aggregation architecture differs.

## Choosing an Edition

| Requirement | Recommended Edition |
|-----------|-------------|
| Workload within one server's throughput and storage capacity | Standard Edition |
| Workload requiring horizontal scaling beyond one server | Cluster Edition |
| High availability with automatic failure recovery | Cluster Edition |
| TRANSACTION tables or MOUNT | Standard Edition |
| Real-time ingestion exceeds one server's capacity and requires more nodes | Cluster Edition |
