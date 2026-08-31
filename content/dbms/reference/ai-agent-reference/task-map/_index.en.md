---
type: docs
title: '17.8.3 task-map'
weight: 30
toc: true
---

Map each user task to canonical documentation and a completion check.

| Task | Reading order | Completion check |
|------|---------------|------------------|
| First installation | [Installation](/dbms/installation-deployment-upgrade/) → [Getting started](/dbms/getting-started/) | Server status, connection, sample query |
| Select a table type | [Modeling and selection](/dbms/data-modeling-table-design/) → table chapter | Edition, DML, axis, and retention requirements match |
| Bulk ingestion | [Integration concepts](/dbms/development-tools-integration/concepts-common/) → SDK page | Success/failure counts and flush verified |
| Generate SQL | [SQL reference](/dbms/reference/sql/) → [Support scope](/dbms/reference/support-scope-constraints/) | Schema and result verified |
| Select an SDK | [Integration selection](/dbms/development-tools-integration/selection-integration-method/) → [SDK support](/dbms/development-tools-integration/sdk-support-scope/) | Server, SDK version, and API match |
| Diagnose performance | [Performance approach](/dbms/performance-tuning/performance-approach/) → symptom guide | Baseline compared with post-change measurement |
| Diagnose failure | [Troubleshooting](/dbms/troubleshooting/) → [Error dictionary](/dbms/reference/error-dictionary-codes/) | Cause, action, and prevention recorded |
| Backup or recovery | [Backup, restore, and mount](/dbms/operations-configuration-recovery/backup-restore-mount/) | Restore or mounted query verified |

Confirm the exact target and impact boundary before any write, delete, restart, or recovery action.
