---
type: docs
title: '12. Performance Tuning'
weight: 120
toc: true
---

Diagnose and tune performance in this order: data model, ingestion path, query execution plan,
memory, and storage. Identify the bottleneck and reproduction conditions before changing
settings, then measure before and after with the same workload.

## Recommended diagnostic order

1. Record latency, throughput, and error rates for the target queries and ingestion operations.
2. Check that the table type matches the data characteristics.
3. Inspect execution state with `EXPLAIN`, `V$STMT`, and `V$SESSION`.
4. Adjust indexes, batch sizes, caches, and storage settings one at a time.
5. Remeasure the effect with the same data and workload.

## Chapter contents

| Order | Section | Content |
|-----:|------|------|
| 12.1 | [Performance Diagnosis](./performance-approach/) | Baselines, bottleneck classification, execution plans, and system views |
| 12.2 | [Data Modeling for Performance](./performance-tuning-modeling/) | Table type and schema design checks |
| 12.3 | [Index Tuning](./index-tuning/) | Index selection by table type and write costs |
| 12.5 | [Query and Analysis Tuning](./performance-query-tuning/) | Time predicates, execution plans, ROLLUP, and window functions |
| 12.6 | [Cache and Memory Tuning](./cache-tuning-memory/) | PVO Cache, Min-Max Cache, and memory usage |
| 12.7 | [Storage and Cluster Tuning](./tuning-storage-cluster/) | Disk I/O, checkpoints, and Cluster configuration |

Throughput and response time depend on hardware, data distribution, schemas, indexes, and
concurrent users. Use sample settings as starting points and validate them with production workloads.
