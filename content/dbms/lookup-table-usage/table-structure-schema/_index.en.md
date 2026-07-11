---
title: '9.2 Table Structure and Schema'
weight: 20
toc: true
---
LOOKUP combines persistence with an in-memory query structure:

1. Changes are written to persistent storage.
2. At server startup, every persisted LOOKUP row is reconstructed in an in-memory row table.
3. Each row is registered in the required `PRIMARY KEY` Red-Black index.
4. SQL queries access these in-memory rows and indexes.

The primary key acts as the key, while the remaining columns form the value. LOOKUP still provides a
SQL table interface, general predicates, joins, and secondary indexes. It does not fetch selected rows
from disk on demand, so row width, variable-length values, JSON values, and secondary indexes must all
be included when estimating memory requirements.


<a id="lookup-table-design"></a>

## LOOKUP Table Design
