---
type: docs
title: '12.4 Ingestion Performance Tuning'
weight: 40
toc: true
aliases:
  - /dbms/performance-tuning/data-input-performance/
---

Ingestion performance depends on the ingestion path, row size, batching, concurrency, indexes,
and storage. Tune using representative data and measurements of end-to-end throughput and
server processing response latency.

## Choose an ingestion path

Use [Data Input and Export](/dbms/development-tools-integration/data-input-load-export/) to
choose a path and check SDK and table-type support. This page focuses on throughput and latency
for the selected path.

<a id="performance-tuning-bulk"></a>

## Measurement procedure

1. Prepare a representative schema, row size, and indexes.
2. Measure a baseline with one connection and small batches.
3. Increase batch size incrementally, recording rows/s and flush and server processing response latency.
4. Observe client CPU and memory alongside server CPU, I/O, and memory.
5. Increase connections and compare total throughput and p95/p99 response times. The p99 latency
   is the time within which 99% of requests complete; it reveals the impact of slow requests.
6. Test failures, reconnections, and duplicate handling.

Do not use a universal recommended batch size or thread count. Oversized batches increase
memory use and error reprocessing scope; undersized batches increase network round-trip overhead.

## Append operations

Follow the Append lifecycle, error handling, and duplicate handling contracts in
[Common Integration Concepts](/dbms/development-tools-integration/concepts-common/#append-api-batch)
and the [SDK Append Matrix](/dbms/development-tools-integration/sdk-support-scope/#append-table-type-matrix).
As you vary batch size and connections, record rows/s, p95/p99 latency, server processing
responses, and failure counts together.

## File loading

For file format validation, rejected-row files, exit codes, and final row verification, see
[Data Input and Export](/dbms/development-tools-integration/data-input-load-export/). Compare
performance only after applying the same validation to the workload.

## Classify bottlenecks

| Observation | Check next |
|------|-----------|
| Client CPU saturation | Serialization, conversion, logging |
| Increasing network waits | Batches, round trips, packet loss |
| Server CPU saturation | Index count, SQL parsing, concurrency |
| Increasing storage latency | Checkpoints, device queues, retention jobs |
| Increasing memory usage | Batch buffers, connection count, caches |
| Only some nodes are slow | Key distribution, routing, per-node resources |

## Before and after changes

Judge throughput improvements only after verifying successful and failed row counts. Also
measure latency from ingestion start to server application, and check the impact on query
performance and recovery time.
