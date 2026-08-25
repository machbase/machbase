---
type: docs
title: '11.3 SDK Feature Support'
weight: 30
toc: true
aliases:
  - /dbms/development-tools-integration/support-scope-sdk/
  - /dbms/application-integration/support-scope-sdk/
---

Compare SDK capabilities before selecting an interface. Use each SDK page as the canonical source
for installation, connection options, functions, and complete code.

## Choose by requirement

| Requirement | Start with |
|---|---|
| Continuous high-volume TAG or LOG input | An SDK with an Append API |
| Standard SQL interface | JDBC, Python DB-API, Go `database/sql`, or ODBC |
| TRANSACTION table transactions | An SDK whose transaction support is documented |
| Public-key authentication | An SDK with documented AUTH KEY challenge support |
| Result-column nullability or key metadata | An SDK exposing the required metadata |

Append support does not make TAG or LOG input part of a TRANSACTION-table rollback unit. Verify
commit, retry, and duplicate-handling behavior for the selected input path.

<a id="support-scope-sdk-nullable-metadata"></a>

## Nullable metadata

Machbase reports result-column nullability as `NO_NULLS`, `NULLABLE`, or `UNKNOWN`. Treat both
`NULLABLE` and `UNKNOWN` as values that may require NULL handling. See the SDK page for its metadata
type and accessor.

<a id="support-scope-sdk-primary-key-metadata"></a>

## PRIMARY KEY metadata

Drivers may expose key information through result metadata, table catalog APIs, or both. Derived
expressions, views, and joins may not retain direct-column key metadata. Use catalog APIs when the
application needs table-schema facts.

<a id="support-scope-sdk-generated-rowid"></a>

## Generated ROWID

Generated ROWID support applies to a single SQL INSERT when the selected SDK exposes the generated
identifier. It does not apply to Append or bulk-file input. See
[ROWID and INSERT result IDs](../rowid-generated-id/) for table and SDK constraints.

<a id="support-scope-sdk-append"></a>

## Append API

SQLCLI, ODBC, JDBC, Python, .NET, and native Go interfaces provide different Append entry points and
acknowledgement behavior. Confirm table-type support, flush behavior, error reporting, and retry
handling in the SDK reference before choosing Append.

<a id="support-scope-sdk-auth-key"></a>

## AUTH KEY authentication

AUTH KEY requires explicit challenge-response support in the client. Do not infer support from a
driver's ability to set a password or TLS option. See the selected SDK page and
[AUTH KEY authentication](../../security-access-control/authentication-auth-key/) for the verified workflow.

<a id="support-scope-sdk-transaction-prepare-bind"></a>

## Transaction, prepare, and bind support

Prepared statements and parameter binding are distinct from transaction control. Check all three
capabilities independently, including placeholder syntax and supported parameter types. Named bind
syntax is defined in the
[SQL syntax dictionary](../../reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/).

<a id="sdk"></a>

## SDK index

| SDK | Canonical reference |
|---|---|
| Machbase SQLCLI and ODBC | [SQLCLI and ODBC](../cli-odbc/) |
| JDBC | [JDBC](../jdbc/) |
| Python | [Python](../python/) |
| Node.js / TypeScript | [Node.js / TypeScript](../node-js-typescript/) |
| .NET Connector | [.NET Connector](../net-connector/) |
| Go | [Go](../go/) |
