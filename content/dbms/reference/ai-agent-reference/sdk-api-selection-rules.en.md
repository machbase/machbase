---
type: docs
title: '16.8.9 sdk-api-selection-rules'
weight: 90
toc: true
---

Check requirements and actual support instead of inferring features from an SDK name.

## Selection Order

1. Check language and standard interface requirements in [Choosing an Integration Method](/dbms/development-tools-integration/selection-integration-method/).
2. List requirements for Append, transactions, prepared statements, named binds, metadata, and AUTH KEY.
3. Check support and provenance in [SDK Support](/dbms/development-tools-integration/sdk-support-scope/).
4. Verify installation, connection options, type mappings, and error handling on the selected SDK page.

| Environment | Canonical Reference |
|------|------|
| C/C++ SQLCLI/ODBC | [SQLCLI and ODBC](/dbms/development-tools-integration/cli-odbc/) |
| Java | [JDBC](/dbms/development-tools-integration/jdbc/) |
| Python | [Python](/dbms/development-tools-integration/python/) |
| Node.js·TypeScript | [Node.js / TypeScript](/dbms/development-tools-integration/node-js-typescript/) |
| .NET | [.NET Connector](/dbms/development-tools-integration/net-connector/) |
| Go | [Go](/dbms/development-tools-integration/go/) |

Also check server/SDK version combinations in
[Compatibility](/dbms/reference/support-scope-constraints/compatibility-xma-protocol/).
