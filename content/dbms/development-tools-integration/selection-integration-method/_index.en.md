---
type: docs
title: '11.1 Choose an Integration Method'
weight: 10
toc: true
aliases:
  - /dbms/application-integration/selection-integration-method/
  - /dbms/application-integration/guide-drivers/
---

Choose an integration method for the project language, ingestion pattern, and deployment environment.

<a id="selection-guide-integration-method"></a>

## Selection Criteria

| Requirement | First option to consider |
|----------|------------------|
| Native C/C++ collector | SQLCLI |
| ODBC manager/DSN application | ODBC |
| Java/Spring | JDBC |
| Python analytics/automation | `machbaseapi` |
| C#/VB.NET | .NET Connector |
| Go collector/service | Native `machgo` or `database/sql` |
| Node.js/TypeScript backend | `@machbase/ts-client` |
| R analytics | Machbase ODBC driver with RODBC |
| Bulk file ingestion/export | machloader, csvimport, csvexport |
| Continuous bulk TAG/LOG ingestion | The chosen SDK's Append API |

Do not connect a browser directly to port 5656. Execute queries in a backend and return
only the required results.

## Decision Sequence

1. Choose an official driver maintainable in the application language.
2. Check port 5656 connectivity, operating system support, and runtime compatibility.
3. Identify required SQL, prepared statement, Append, and transaction features.
4. Check actual support in the [SDK Feature Matrix](../sdk-support-scope/).
5. Round-trip sample timestamps, NULLs, numbers, and strings.
6. Load-test target row sizes, concurrent connections, and batch sizes.

Do not choose a driver on Append support alone. Verify flush latency, server error
responses, reconnection, and failed-row handling in the actual SDK. For TRANSACTION
DML, check explicit transaction support. Do not assume TAG/LOG Append shares its rollback scope.

<a id="distinction-sdk-api-canonical-owner"></a>

<a id="정본-구분"></a>

## Detailed Documentation by Topic

| Topic | Detailed documentation |
|------|------|
| SDK installation, connections, APIs, complete code | SDK pages in this chapter |
| Shared authentication, binding, transactions, retries | [Common Integration Concepts](../concepts-common/) |
| SDK feature support | [SDK Feature Support](../sdk-support-scope/) |
| SQL, configuration, command-line details | [Chapter 16 Reference](/dbms/reference/) |
| Choose ingestion/export methods | [Data Ingestion and Export](../data-input-load-export/) |

After choosing an integration method, run its SDK installation and connection examples.
Check both documented versions and actual deployment artifacts for feature support.
