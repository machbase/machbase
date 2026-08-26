---
type: docs
title: '4.2 Choose a Table Type'
weight: 20
toc: true
---

Read [Data model concepts](/dbms/core-concepts/concepts/) for the role of each table. This page makes
the implementation decision from mutation, query, persistence, and transaction requirements.

<a id="table-types-type"></a>

The table-type overview moved to Chapter 2. The following flow is the canonical selection procedure.

<a id="selection-decision"></a>

## Decision flow

1. Use TAG for measurements addressed by tag name and a time or distance axis.
2. Use LOG for append-oriented events and logs ordered by server arrival.
3. Use LOOKUP for persistent, memory-resident reference data.
4. Use VOLATILE for shared in-memory state that can be rebuilt after restart.
5. Use TRANSACTION for relational business data requiring general DML and transactions.

If two choices remain, decide from the required UPDATE and DELETE predicates, restart behavior,
working-set size, transaction boundary, and dominant query key.

<a id="comparison-tag-log-rdb-volatile-lookup"></a>

## Comparison

| Requirement | Start with |
|---|---|
| Repeated measurements by name and axis | TAG |
| Append-only event history | LOG |
| General relational DML and transaction | TRANSACTION |
| Persistent reference lookup | LOOKUP |
| Rebuildable in-memory state | VOLATILE |

Exact DML conditions belong to [Data mutation policy](../alter-data-mutation-policy/) and hard
feature support belongs to [Support scope](/dbms/reference/support-scope-constraints/).

<a id="comparison-rdb-vs-lookup"></a>

## TRANSACTION versus LOOKUP

Choose TRANSACTION for relational changes, transactions, and larger business sets. Choose LOOKUP for
small persistent reference data whose complete runtime rows and indexes can reside in memory. Measure
the expected row set and update pattern instead of selecting by table name alone.
