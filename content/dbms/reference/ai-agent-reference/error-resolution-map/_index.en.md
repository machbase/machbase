---
type: docs
title: '17.8.11 error-resolution-map'
weight: 110
toc: true
---

Preserve the complete error and execution context instead of guessing an error number or cause.

1. Capture the full `ERR-XXXXX` message, SQL or command, and occurrence time.
2. Record server and SDK version, Edition, database, owner, table, and connection options.
3. Check the [Error dictionary](/dbms/reference/error-dictionary-codes/).
4. Apply the symptom workflow in [Troubleshooting](/dbms/troubleshooting/).
5. Re-run the same input and verification query after the action.

| Symptom | Canonical reference |
|---------|---------------------|
| Server, authentication, or connection | [Server and connection](/dbms/troubleshooting/server-connection/) |
| Ingestion, Append, or files | [Input and ingestion](/dbms/troubleshooting/item/) |
| Query, performance, or memory | [Query and performance](/dbms/troubleshooting/performance/) |
| Backup or recovery | [Backup and recovery](/dbms/troubleshooting/recovery-backup/) |
| Cluster | [Cluster](/dbms/troubleshooting/cluster/) |

Do not assign an error code from a partial message or recommend a destructive workaround
without a verified reproduction and target.
