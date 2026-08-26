---
type: docs
title: '2.1 Data Model Concepts'
weight: 10
toc: true
---

This page explains why Machbase separates time-series, event, relational, reference, and rebuildable
state workloads. Use Chapter 4 to make the final table and schema decision.

<a id="time-series"></a>

## Understand time-series data

Measurements have a subject, an axis, and values recorded repeatedly. Events arrive when something
happens and often vary in frequency and shape. Machbase uses TAG for measurement series and LOG for
append-oriented event streams.

### Table-type roles

| Table | Conceptual role |
|---|---|
| TAG | Measurements identified by name and a time or distance axis |
| LOG | Events and logs appended in server-arrival order |
| TRANSACTION | Relational business data requiring transactions and general DML |
| LOOKUP | Persistent reference rows loaded into memory |
| VOLATILE | Shared in-memory state that can be rebuilt after restart |

See [Choose a table type](/dbms/data-modeling-table-design/table-types-selection-type/) to apply
mutation, query, and persistence requirements.

<a id="differences-rdbms"></a>

### Difference from a general relational workload

Time-series input is predominantly append and range scan. Relational business data is commonly
updated by key and protected by transactions. Do not apply the storage and mutation assumptions of
one workload to the other.

<a id="write-oriented-append-only"></a>

## Write-oriented and append-centered models

TAG and LOG reduce write contention by appending new time-series rows. TRANSACTION provides
relational DML; LOOKUP and VOLATILE provide key-centered mutable reference or state data. Exact
UPDATE, DELETE, and TRUNCATE conditions belong to
[Data mutation policy](/dbms/data-modeling-table-design/alter-data-mutation-policy/).

SQL INSERT and SDK Append are different input paths. API lifecycle, acknowledgement, and retry rules
belong to [Data input and export](/dbms/development-tools-integration/data-input-load-export/).

<a id="time-model-arrival-time"></a>

## Time models

LOG supplies `_ARRIVAL_TIME` as the server-receipt time. TAG uses a declared BASETIME or BASEDISTANCE
axis. LOOKUP, VOLATILE, and TRANSACTION DATETIME columns are ordinary columns without either special
meaning. Choose the final table type in Chapter 4 after deciding which time meaning the application
must preserve.
