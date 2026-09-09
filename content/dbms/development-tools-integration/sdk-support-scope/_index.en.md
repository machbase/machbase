---
type: docs
title: '11.3 SDK Feature Support'
weight: 30
toc: true
aliases:
  - /dbms/development-tools-integration/support-scope-sdk/
  - /dbms/application-integration/support-scope-sdk/
  - /dbms/reference/support-scope-constraints/sdk/
---

Compare feature support and API entry points to choose an SDK for your application.
See each SDK page for installation, connections, functions, and runnable examples.

If choosing an SDK for the first time, read [Choose an Integration Method](../selection-integration-method/)
first, then use this page to compare required features and exact API paths.

<a id="support-scope-sdk-nullable-metadata"></a>

## Nullable Metadata

Machbase reports SELECT result column nullability as `NO_NULLS`, `NULLABLE`, or `UNKNOWN`.
Applications must handle NULL for both `NULLABLE` and `UNKNOWN`.

| SDK | Retrieval method |
|---|---|
| JDBC | `ResultSetMetaData.isNullable()` |
| Python | `cursor.description[i][6]` |
| Go native | `api.Column.Nullability` |
| Go `database/sql` | `Rows.ColumnTypeNullable()` |
| Node.js | `ColumnMeta.nullable` |
| .NET | `AllowDBNull` in `GetSchemaTable()` |
| SQLCLI/ODBC | Descriptor nullable attribute |

Expressions, aggregates, VIEWs, and JOIN results may report `UNKNOWN`. Do not equate
a source column schema constraint with query result metadata.

<a id="support-scope-sdk-primary-key-metadata"></a>

## PRIMARY KEY Metadata

| SDK | Result columns | Table catalog |
|---|:---:|:---:|
| JDBC | O | `DatabaseMetaData.getPrimaryKeys()` |
| Python | O | Catalog SQL |
| Go native | O | Catalog SQL |
| Go `database/sql` | No standard API | Catalog SQL |
| Node.js | O | Catalog SQL |
| .NET | O | Catalog SQL |
| ODBC | No separate result API | `SQLPrimaryKeys()` |

Expressions, aggregates, and the NULL-supplying side of an outer join may not preserve
the source column primary key attribute.

<a id="support-scope-sdk-generated-rowid"></a>

## ROWID from INSERT

In Machbase 8.7.0 Standard Edition, a successful single `INSERT ... VALUES` can provide
a ROWID to supported SDKs.

| SDK/tool | Retrieval method | When absent |
|---|---|---|
| machsql | `SHOW LAST ROWID` | `NULL` |
| Machbase SQLCLI | `SQLGetGeneratedRowID()` | `SQL_NO_DATA` |
| Standard ODBC | No dedicated standard API | - |
| JDBC | `Statement.getGeneratedKeys()` | Empty `ResultSet` |
| Python | `cursor.lastrowid` | `None` |
| .NET | `MachCommand.RowId` | `null` |
| Go `database/sql` | `Result.LastInsertId()` | Error |
| Go native | Unsupported | - |
| Node.js | Execution result `rowId` | `undefined` |

Batches, `executemany()`, Append, loaders, `INSERT ... SELECT`, and UPSERT do not return
a single ROWID. See [ROWID](/dbms/reference/sql/rowid/) for SQL semantics and table-specific
constraints.

<a id="support-scope-sdk-append"></a>
<a id="append-table-type-matrix"></a>

## Append APIs and Table Types

| API path | LOG | TAG | LOOKUP | VOLATILE | TRANSACTION | Basis |
|---|:---:|:---:|:---:|:---:|:---:|---|
| SQLCLI `SQLAppend*` extension | O | O | O | O | O | TRANSACTION requires Standard |
| JDBC `MachStatement.executeAppend*` | O | O | O | O | O | NFX cce422d source/tests |
| Python 2.4 `append*` | O | O | O | O | O | NFX cce422d source/tests |
| .NET `MachAppendWriter` | O | O | O | O | O | NFX cce422d provider |
| Go v1.8.4 native `Appender` | O | O | X | X | O | TRANSACTION requires Standard |
| Go `database/sql` standard API | X | X | X | X | X | `sql.Conn.Raw()` extensions follow the native contract |
| Node source `appendBatch()` | O | △ | △ | △ | O | NFX cce422d source build |
| Node source `appendOpen()` | O | O | △ | △ | △ | Generic native/fallback path; table-specific validation required |

Keep ordinary query connections and Append handle lifecycles distinct, and check close
and flush results. `O` indicates support verified in the cited source/tests. `△` means
only a generic path is available and further table-specific regression testing is needed.
Append extensions are not standard ODBC or `database/sql` features.

### ARRAY and Selected-Column Append

Machbase DBMS 8.7.0 ARRAY support is as follows:

| SDK | Dense ARRAY retrieval/input | Sparse ARRAY | Selected-column Append |
|---|:---:|:---:|:---:|
| SQLCLI/C++ | O | O | O |
| Machbase ODBC extension | O | O | O |
| JDBC | O | O | O |
| Python | O | O | O |
| Node.js | O | O | O |
| .NET full/legacy provider | O | O | O |
| Go | v2 main source | v2 main source | v2 main source |

Use a Machbase DBMS 8.7.0 server with an SDK build that includes ARRAY support. SQL ARRAY
element positions and Machbase-specific SDK positions are 0-based. Existing full-row
scalar Append APIs are unchanged. The Node.js prepared fallback also supports `SparseArray`.
Go requires v2 main source after [`neo-client` PR #17](https://github.com/machbase/neo-client/pull/17);
until a public v2 release is specified, do not assume a published module version provides
support. See [Sparse ARRAY and Selected-Column Append API](../data-input-load-export/array-append/)
for input methods and APIs.

<a id="support-scope-sdk-auth-key"></a>

## AUTH KEY

| SDK/tool | Support |
|---|:---:|
| machsql, Machbase SQLCLI, ODBC, JDBC | O |
| Go native, Go `database/sql` | O (neo-client v1.5.0+) |
| Python, Node.js, .NET | X |

See [AUTH KEY Authentication](/dbms/security-access-control/authentication-auth-key/) for
key generation, registration, and rotation. See supported SDK pages for connection options.

<a id="support-scope-sdk-transaction-prepare-bind"></a>

## Transactions, Prepare, and Binding

| SDK | Transaction API | Server prepared | Named bind API |
|---|:---:|:---:|:---:|
| JDBC | O | O | △ (Machbase extension) |
| Python | X | O | O |
| Go native | △ | O | O |
| Go `database/sql` | O | O | O |
| .NET | X | X | △ |
| Node.js | X | O | O |
| SQLCLI | △ | O | O |
| ODBC | △ | O | Positional binding |

Prepared statements and parameter binding are separate from transaction support. See
[Named Bind Parameter](/dbms/reference/sql/syntax/named-bind-parameter-syntax/) for placeholder syntax.

For TAG data UPDATE in Machbase 8.7.0 Standard Edition, existing positional/named SDK
APIs can bind NAME and BASETIME predicate values. NFX #4127 regression tests cover C/C++
SQLCLI, Go `database/sql`, JDBC, Node.js, Python, and .NET. ODBC is not included in that
SDK regression matrix; it binds `?` or named SQL placeholders by ordinal through standard
`SQLBindParameter()`. See
[TAG Data UPDATE Binding](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind)
for predicate requirements.

`△` in the Transaction column means executing transaction SQL on the same connection
instead of using a dedicated object. `△` in Named bind means a driver extension or a
client path that converts values to SQL literals, rather than a standard named binding API.

## Verified Versions and Provenance

| SDK | Verification basis |
|---|---|
| SQLCLI/JDBC/Python | NFX `cce422d2972`; Python package 2.4 |
| Node.js | NFX `cce422d2972` source build (`package.json` 1.0.1) |
| .NET | Uni 8.0.55, limited 3.1.3, full 3.2.2 |
| Go | Released neo-client v1.8.4; AUTH KEY v1.5.0+, database selection v1.8.3+ |

Some Node features in NFX cce422d were added after the public npm 1.0.1 release. Do not
assume feature parity from the registry package version string. Check the artifact
commit provenance or use an NFX source build.

ARRAY and selected-column Append were verified against NFX
`655d1333870313c4951698b89c9a3c9ada11d630` and merge commit
`f756986c4836982723e2aa7727ec05b7e05e9707`. Use Machbase DBMS 8.7.0 as the server baseline
and verified SDK artifacts containing those changes as the client baseline.

<a id="sdk"></a>

## SDK References

| SDK | Detailed documentation |
|---|---|
| Machbase SQLCLI/ODBC | [SQLCLI and ODBC](../cli-odbc/) |
| JDBC | [JDBC](../jdbc/) |
| Python | [Python](../python/) |
| Node.js / TypeScript | [Node.js / TypeScript](../node-js-typescript/) |
| .NET Connector | [.NET Connector](../net-connector/) |
| Go | [Go](../go/) |
