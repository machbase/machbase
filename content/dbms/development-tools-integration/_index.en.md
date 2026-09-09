---
type: docs
title: '11. Development and Application Integration'
weight: 110
toc: true
aliases:
  - /dbms/reference/sdk-api/
  - /dbms/application-integration/
---

Choose an integration method for your application, then review SDK installation, APIs,
and shared operational principles. Use SDK pages for language-specific implementations
and the selection, concepts, and support pages for guidance shared across SDKs.

## Reading Order

1. [Choose an Integration Method](selection-integration-method/) for your language and input pattern.
2. Review authentication, time values, binding, transactions, and retries in
   [Common Integration Concepts](concepts-common/).
3. Compare actual support in [SDK Feature Support](sdk-support-scope/).
4. Follow the relevant SDK page for installation, connections, and executable code.
5. Apply task-specific procedures in [Data Ingestion and Export](data-input-load-export/).
   For SQL ROWID semantics, see [ROWID](../reference/sql/rowid/). For partial ARRAY
   input in Machbase DBMS 8.7.0, see
   [Sparse ARRAY and Selected-Column Append API](data-input-load-export/array-append/).

## SDK References

| Environment | Documentation |
|---|---|
| Native C/C++ or ODBC | [Machbase SQLCLI and ODBC](cli-odbc/) |
| Java/Spring | [JDBC](jdbc/) |
| Python | [Python](python/) |
| Node.js/TypeScript | [Node.js / TypeScript](node-js-typescript/) |
| C#/VB.NET | [.NET Connector](net-connector/) |
| Native Go/`database/sql` | [Go](go/) |

## Common Connection Information

| Item | Default | Description |
|---|---|---|
| HOST | `127.0.0.1` | Server host name or IP address |
| PORT | `5656` | Server port (`PORT_NO` in `machbase.conf`) |
| USER | `SYS` | User ID |
| PASSWORD | `MANAGER` | User password |

Use a dedicated user with the minimum required privileges in production. See
[Accounts, Privileges, and Access Control](../security-access-control/) for account
and authentication settings.

## Existing Support Links

See [SDK Feature Support](sdk-support-scope/) for NULL/PRIMARY KEY metadata, ROWID,
Append, and AUTH KEY support by SDK.

<a id="support-scope-sdk-nullable-metadata"></a>
<a id="support-scope-sdk-primary-key-metadata"></a>
<a id="support-scope-sdk-generated-rowid"></a>
<a id="support-scope-sdk-append"></a>
<a id="support-scope-sdk-auth-key"></a>
<a id="support-scope-sdk-transaction-prepare-bind"></a>
<a id="sdk"></a>
