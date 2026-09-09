---
type: docs
title: '16.8.3 task-map'
weight: 30
toc: true
---

This map links user tasks to canonical reading order and completion criteria.

| Task | Verification Order | Completion Check |
|------|-----------|-----------|
| First installation | [Installation](/dbms/installation-deployment-upgrade/) → [Getting Started](/dbms/getting-started/) | Server status, connection, and sample query |
| Table selection | [Selection Criteria](/dbms/data-modeling-table-design/) → Table chapter | Edition, DML, axis, and retention requirements met |
| Bulk ingestion | [Common Integration Concepts](/dbms/development-tools-integration/concepts-common/) → SDK page | Success/failure counts and flush verified |
| SQL authoring | [SQL Reference](/dbms/reference/sql/) → [Support Scope](/dbms/reference/support-scope-constraints/) | Actual schema and results verified |
| SDK selection | [Choosing an Integration Method](/dbms/development-tools-integration/selection-integration-method/) → [SDK Support](/dbms/development-tools-integration/sdk-support-scope/) | Server/SDK versions and APIs match |
| Performance diagnosis | [Performance Approach](/dbms/performance-tuning/performance-approach/) → Symptom-specific tuning | Baseline and post-change measurements compared |
| Failure diagnosis | [Troubleshooting](/dbms/troubleshooting/) → [Error Codes](/dbms/reference/error-codes/) | Cause, action, and recurrence prevention recorded |
| Backup/recovery | [Backup/Recovery](/dbms/operations-configuration-recovery/backup-restore-mount/) | Restore or mounted queries verified |

For tasks involving writes, deletion, or restarts, establish the target and impact scope before
selecting the procedure.
