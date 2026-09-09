---
type: docs
title: '12.7 Storage and Cluster Tuning'
weight: 70
toc: true
---

Base storage and Cluster tuning on workload measurements, recovery objectives, and per-node
resource usage. Do not apply fixed hardware specifications or arbitrary configuration values
to every environment.

<a id="tuning-storage-checkpoint"></a>

<a id="스토리지와-checkpoint"></a>

## Storage and checkpoints

Compare the following over the same time range:

- Ingestion rows/s and server processing response latency
- Query response time and read volume
- Per-device IOPS, throughput, queue depth, and latency
- Checkpoint start and end times and duration
- Changes in memory usage and swap
- Acceptable recovery time after a failure

```bash
iostat -x 1 5
df -h
```

Check current checkpoint interval and I/O settings in the
[Configuration Reference](/dbms/reference/configuration/configuration/). Change one property
at a time and record restart requirements and rollback values.

## Paths and capacity

- Check ownership and free space for data, backup, and export paths.
- Separate paths on the same physical device do not necessarily distribute I/O.
- Do not manually move data files while the server runs.
- Account for retention policies and backup space growth together.
- Verify support and recovery procedures before changing file system or mount options.

Do not locate and delete internal partition tables to remove old data. Use public SQL and
operational features, such as table-specific `DELETE ... BEFORE`, retention policies, and
backup policies.

<a id="performance-considerations-cluster-edition"></a>

## Cluster measurements

Inspect client, Broker, Warehouse, and Coordinator metrics separately.

| Segment | Check |
|------|------|
| Client → Broker | Connections, round trips, batch size |
| Broker | Sessions, routing, CPU, network |
| Warehouse | Per-node ingestion, query, and disk imbalance |
| Inter-node communication | Bandwidth, packet loss, latency |
| Coordinator | Node state and disk-full policy |

If load concentrates on a node, inspect tag and key distribution, routing, Warehouse groups,
and per-node storage and network together. Do not use `TAG_PARTITION_COUNT` to control
distribution across Cluster nodes.

<a id="property-변경-원칙"></a>

## Configuration change principles

- Check names, allowed ranges, and defaults in the installed version's configuration reference.
- Record the current baseline and target instead of choosing arbitrary recommended numbers.
- When increasing buffers, measure memory and tail latency as well as throughput.
- Before changing replication settings, compare recovery time in both normal and failure scenarios.
- Use hysteresis between disk-full upper and lower thresholds, linked to actual expansion and cleanup procedures.
- Check edition-specific exclusions in [Support Scope](/dbms/reference/support-scope-constraints/).

## Change checklist

1. Is there evidence of a bottleneck by node and segment?
2. Have you recorded current settings and their sources?
3. Have you measured normal and failure scenarios in a test environment?
4. Have you checked deployment order and restart requirements by node?
5. Do you have rollback values and procedures if results worsen?
6. Have you verified backup and recovery after the change?
