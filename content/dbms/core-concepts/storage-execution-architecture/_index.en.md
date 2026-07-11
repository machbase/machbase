---
type: docs
title: '2.2 Storage and Execution Architecture'
weight: 20
toc: true
---



<a id="architecture-machbase"></a>

## Machbase Architecture Overview

<a id="storage-columnar-compression-column"></a>

## Columnar Storage and Compression

<a id="indexing-basics"></a>

## Indexing Basics

### LOOKUP: Persistent Storage and an In-Memory Red-Black Index

LOOKUP data is persistent, but the server reconstructs every row in an in-memory row table at startup
and builds a Red-Black index on the primary key. The primary key acts as the key and the remaining row
columns form the value. Runtime SQL queries use these in-memory rows and indexes.

This design preserves data across restarts and provides fast key lookup, while making the complete row
set and all secondary indexes part of server memory usage. Use LOOKUP for memory-resident reference
data and consider an RDB table for larger relational data sets.

<a id="execution-concepts-plan-cache"></a>

## Cache and Execution Plan Concepts
