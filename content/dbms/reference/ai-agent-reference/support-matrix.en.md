---
type: docs
title: '16.8.4 support-matrix'
weight: 40
toc: true
---

This page identifies the relevant dimensions of a support question and links to current canonical tables.

## Verification Order

1. Check Standard and Cluster scope in the [Edition Support Matrix](/dbms/reference/support-scope-constraints/edition/).

2. Check the target table's SQL and API scope in the
   [Table Type Support Matrix](/dbms/reference/support-scope-constraints/table-types-type/).
3. Check client APIs and minimum provenance in
   [SDK Support](/dbms/development-tools-integration/sdk-support-scope/).
4. Check conditions and exceptions in detailed feature support tables.

| Feature Group | Canonical Reference |
|--------|------|
| TAG data UPDATE | [TAG UPDATE Support](/dbms/reference/support-scope-constraints/tag-data-update/) |
| ROLLUP | [ROLLUP Support](/dbms/reference/support-scope-constraints/rollup/) |
| TRANSACTION | [TRANSACTION Support](/dbms/reference/support-scope-constraints/rdb/) |
| Backup/MOUNT | [Backup/MOUNT Support](/dbms/reference/support-scope-constraints/backup-mount/) |
| Privileges | [Privilege Support](/dbms/reference/support-scope-constraints/privileges/) |

When answering support questions, provide the edition, table type, server and SDK versions, and
prerequisites along with `O/△/X`.
