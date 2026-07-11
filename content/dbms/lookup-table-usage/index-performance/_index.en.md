---
title: '9.6 Indexes and Performance'
weight: 60
toc: true
---
LOOKUP and VOLATILE tables use Red-Black indexes. A LOOKUP table automatically creates a primary
Red-Black index, whose entries reference complete in-memory rows. Primary-key lookup is therefore the
preferred access pattern even though the data also has a persistent copy.


<a id="index-tuning-lookup-volatile"></a>

## LOOKUP/VOLATILE Index Tuning

<a id="original-85-lookup-indexes"></a>

## LOOKUP Indexes

Create Red-Black secondary indexes only for non-primary-key columns used frequently in predicates or
joins. Without an applicable index, the query scans the complete in-memory row set. Each secondary
index improves its target access path but increases memory use and DML cost.

<a id="index-strategy-lookup"></a>

## LOOKUP Index Strategy

Size a LOOKUP table using actual row width, variable-length values, row count, and all indexes. Server
startup reads every persisted row and rebuilds the in-memory rows and indexes, so validate both memory
usage and startup time. Use an RDB table when the complete relational data set should not reside in
memory.
