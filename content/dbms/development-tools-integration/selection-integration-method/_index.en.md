---
type: docs
title: '11.1 Choose an Integration Method'
weight: 10
toc: true
aliases:
  - /dbms/application-integration/selection-integration-method/
  - /dbms/application-integration/guide-drivers/
---

Choose an integration method for the application language, input pattern, and deployment
environment.

<a id="selection-guide-integration-method"></a>

## Selection guide

| Requirement | Start with |
|---|---|
| Native C/C++ collector | SQLCLI |
| ODBC manager and DSN | ODBC |
| Java or Spring | JDBC |
| Python analysis or automation | `machbaseapi` |
| C# or VB.NET | .NET Connector |
| Go collector or service | Native `machgo` or `database/sql` |
| Node.js or TypeScript backend | `@machbase/ts-client` |
| R analysis | RODBC with the Machbase ODBC driver |
| Large file import or export | machloader, csvimport, or csvexport |
| Continuous TAG or LOG input | The selected SDK's Append API |

Do not connect a browser directly to port 5656. Execute database operations in a backend and return
only the required result.

## Decision sequence

1. Select an official driver that the application team can maintain.
2. Confirm port 5656 connectivity and operating-system and runtime compatibility.
3. Identify required SQL, prepared-statement, Append, and transaction capabilities.
4. Check actual support in [SDK feature support](../sdk-support-scope/).
5. Round-trip representative timestamps, NULLs, numbers, and strings.
6. Load-test the target row size, connection count, and batch size.

Do not select a driver based only on Append availability. Verify acknowledgement, flush latency,
reconnection, and failed-row handling. Do not assume TAG or LOG Append participates in a
TRANSACTION-table rollback unit.

<a id="distinction-sdk-api-canonical-owner"></a>

## Canonical documentation

| Subject | Canonical page |
|---|---|
| SDK installation, connection, API, and complete code | The SDK pages in this chapter |
| Authentication, binding, transactions, and retries | [Common integration concepts](../concepts-common/) |
| Feature availability | [SDK feature support](../sdk-support-scope/) |
| SQL, configuration, and command details | [Reference](../../reference/) |
| Input and export selection | [Data input and export](../data-input-load-export/) |
| External-tool validation | [External tools](../external-tools/) |

Keep SDK function lists and installation procedures in the SDK page instead of copying them into
cross-SDK guidance.
