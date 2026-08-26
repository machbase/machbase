---
type: docs
title: '11. Development and Application Integration'
weight: 110
toc: true
aliases:
  - /dbms/reference/sdk-api/
  - /dbms/application-integration/
---

Choose an integration method for the application, then use the SDK-specific reference and the
cross-SDK operational guidance in this chapter. SDK pages own installation, API, and complete code;
the selection, common-concepts, and support-scope pages own cross-SDK decisions.

## Reading order

1. Use [Choose an integration method](selection-integration-method/) to select an interface for the
   application language and workload.
2. Review authentication, time values, binding, transactions, and retries in
   [Common integration concepts](concepts-common/).
3. Compare required capabilities in [SDK feature support](sdk-support-scope/).
4. Follow the SDK page for installation, connection, and executable code.
5. Apply the task-specific guidance for [Data input and export](data-input-load-export/). See
   [ROWID](../reference/sql/rowid/) for SQL semantics.

## SDK references

| Environment | Documentation |
|---|---|
| Native C/C++ or ODBC | [Machbase SQLCLI and ODBC](cli-odbc/) |
| Java and Spring | [JDBC](jdbc/) |
| Python | [Python](python/) |
| Node.js and TypeScript | [Node.js / TypeScript](node-js-typescript/) |
| C# and VB.NET | [.NET Connector](net-connector/) |
| Native Go or `database/sql` | [Go](go/) |

## Common connection information

| Item | Default | Description |
|---|---|---|
| HOST | `127.0.0.1` | Machbase server host name or IP address |
| PORT | `5656` | Machbase server port (`PORT_NO` in `machbase.conf`) |
| USER | `SYS` | User ID |
| PASSWORD | `MANAGER` | User password |

Use a dedicated user with the minimum required privileges in production. See
[Accounts, privileges, and access control](../security-access-control/) for account and
authentication configuration.

## Legacy support-scope anchors

The following anchors remain for existing bookmarks. Use
[SDK feature support](sdk-support-scope/) for the current content.

<a id="support-scope-sdk-nullable-metadata"></a>
<a id="support-scope-sdk-primary-key-metadata"></a>
<a id="support-scope-sdk-generated-rowid"></a>
<a id="support-scope-sdk-append"></a>
<a id="support-scope-sdk-auth-key"></a>
<a id="support-scope-sdk-transaction-prepare-bind"></a>
<a id="sdk"></a>
