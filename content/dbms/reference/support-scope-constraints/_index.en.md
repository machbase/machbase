---
type: docs
title: '16.6 Support Scope and Constraints'
weight: 80
toc: true
aliases:
  - /dbms/reference/support-scope-constraints/limitations-functions/
---

This section provides quick references to Machbase feature support by edition, table type, and SDK,
along with known constraints. Use individual feature chapters for behavior and examples, and this
section to check support in a specific environment.

## Pages

| Page | Content |
|--------|------|
| [Feature Support by Edition](./edition/) | Standard Edition and Cluster Edition comparison |
| [Feature Support by Table Type](./table-types-type/) | TAG / LOG / LOOKUP / VOLATILE / TRANSACTION support |
| [Feature Support by SDK](/dbms/development-tools-integration/sdk-support-scope/) | JDBC, Python, Go, .NET, and Node.js support |
| [ROLLUP Support](./rollup/) | ROLLUP support by edition and table type |
| [Backup/Mount Support](./backup-mount/) | BACKUP / MOUNT support by edition |
| [Feature Support by Privilege](./privileges/) | Database and table privileges |
| [TRANSACTION Feature Support](./rdb/) | TRANSACTION table SQL support and constraints |
| [Version and Compatibility](./compatibility-version/) | Upgrade considerations and supported operating systems/platforms |
| [Server and SDK Compatibility](./compatibility-xma-protocol/) | Feature support by server/SDK version combination |
| [LOOKUP SQL/JSON Support](./lookup-sql-json/) | LOOKUP table SQL/JSON support and constraints |
| [TAG Data UPDATE Support](./tag-data-update/) | TAG UPDATE predicates and target columns |

Do not depend on internal objects, flags, or protocol behavior absent from these tables. Check both
server and client versions for SDK features. For feature-specific error diagnosis, see
[Troubleshooting](/dbms/troubleshooting/).

## Notation

<a id="공통-판단-원칙"></a>

Support tables in this section use the following symbols.

| Symbol | Meaning |
|:----:|------|
| O | Fully supported |
| X | Not supported |
| △ | Partially supported or subject to constraints |
