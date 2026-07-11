---
title: '9.7 Operations and Data Lifecycle'
weight: 70
toc: true
---
LOOKUP data is persistent and included in database backup and recovery. At server startup, Machbase
reads every persisted LOOKUP row into an in-memory row table and builds its primary and secondary
indexes. Runtime SQL queries use this in-memory structure.

Monitor the memory used by all LOOKUP rows and indexes, as well as startup time at the expected data
size. Persistence does not make LOOKUP a disk-oriented large relational table; keep only reference data
that can remain memory-resident.


<a id="recovery-support-scope-backup-lookup"></a>

## LOOKUP Backup and Recovery Scope
