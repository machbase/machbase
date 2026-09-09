---
type: docs
title: '16.8.11 error-resolution-map'
weight: 110
toc: true
---

Preserve the complete error and execution context instead of guessing an error number or cause.

## Diagnosis Order

1. Collect the full `ERR-XXXXX` message, SQL/command, and occurrence time.
2. Record server and SDK versions, edition, target database/owner/table, and connection options.
3. Check the message in the [Error Code Dictionary](/dbms/reference/error-codes/).
4. Apply symptom-specific procedures from [Troubleshooting](/dbms/troubleshooting/).
5. Verify recovery with the same input and validation queries after corrective action.

| Symptom | Canonical Reference |
|------|------|
| Server/authentication/connection | [Server and Connection Issues](/dbms/troubleshooting/server-connection/) |
| Ingestion/Append/files | [Ingestion and Loading Issues](/dbms/troubleshooting/item/) |
| Queries/performance/memory | [Query and Performance Issues](/dbms/troubleshooting/performance/) |
| Backup/recovery | [Backup and Recovery Issues](/dbms/troubleshooting/recovery-backup/) |
| Cluster | [Cluster Issues](/dbms/troubleshooting/cluster/) |

Do not assign an arbitrary error code from part of a message or recommend a destructive workaround
without reproducing the problem.
