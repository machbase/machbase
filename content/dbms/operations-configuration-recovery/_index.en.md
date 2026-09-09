---
type: docs
title: '13. Operations, Configuration, and Recovery'
weight: 130
toc: true
---

This chapter covers starting and stopping Machbase servers, configuration changes, observability,
backup and restore, and Cluster operations. Establish routine procedures first, then perform
changes and recovery according to a plan.

## Chapter contents

| Order | Section | Content |
|-----:|------|------|
| 13.1 | [Server and Database Operations](./server-database/) | Server startup and shutdown, database creation and deletion, licenses |
| 13.2 | [Multiple Databases](./multi-database/) | Logical databases, privileges, backup and restore, client integration |
| 13.3 | [Configuration Management](./configuration/) | Configuration files, memory, network, storage, time zones |
| 13.4 | [ALTER SYSTEM Operations](./alter-system/) | Runtime configuration changes and system control |
| 13.5 | [Data Retention Policies](./policy-data-retention/) | Create, attach, inspect, and detach retention policies |
| 13.6 | [Observability and Diagnostics](./diagnosis-observability/) | System views, logs, sessions, capacity, and signs of failure |
| 13.7 | [Schema Change Checklist](./checklist-schema-alter/) | Impact analysis and validation before and after DDL |
| 13.8 | [Backup, Restore, and Mount](./backup-restore-mount/) | Online backup, offline restore, read-only mounts |
| 13.9 | [Cluster Operations](./cluster/) | Topology, adding and removing nodes, state management |

For routine checks, use [Server and Database Operations](./server-database/),
[Configuration Management](./configuration/), and
[Observability and Diagnostics](./diagnosis-observability/).
Before introducing multiple databases, read [Multiple Databases](./multi-database/). For schema or
configuration changes, use [ALTER SYSTEM Operations](./alter-system/) and the
[Schema Change Checklist](./checklist-schema-alter/). For failure recovery and backup validation,
see [Backup, Restore, and Mount](./backup-restore-mount/).
