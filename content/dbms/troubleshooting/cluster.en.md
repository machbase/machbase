---
type: docs
title: '15.6 Cluster Problems'
weight: 60
toc: true
---

<a id="node-state-status-abnormal-cluster"></a>

## Abnormal Cluster node state

Collect the overall state and first error before changing topology or restarting nodes.

```bash
machcoordinatoradmin --cluster-status
machclusterctl status
```

1. Identify which role first became abnormal: Coordinator, Broker, or Warehouse.
2. Align and compare logs from that node and its upstream roles.
3. Check host, process, disk, network, and configuration file change history.
4. Record replication and redistribution state and the client impact.
5. Apply the approved recovery procedures in Chapter 13 one node at a time, then verify overall state again.

Do not guess node names, service ports, or inter-node ports when running start/add/remove
commands. Use the actual `cluster.yaml` and deployment tool help. For detailed operational
restrictions, see [Cluster Operations](/dbms/operations-configuration-recovery/cluster/).

<a id="error-cluster-edition"></a>

## Cluster Edition restriction errors

```sql
SELECT * FROM V$VERSION;
```

To determine whether an error is an edition restriction, compare the current edition with
[Support by Edition](/dbms/reference/support-scope-constraints/). Do not use unofficial
workarounds for Standard-only features. Consider a supported Cluster feature that meets the
same requirement or a separate Standard environment.
