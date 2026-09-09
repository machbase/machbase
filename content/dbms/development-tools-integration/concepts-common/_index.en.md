---
type: docs
title: '11.2 Common Integration Concepts'
weight: 20
toc: true
aliases:
  - /dbms/application-integration/concepts-common/
---

This page covers connection, binding, transaction, bulk ingestion, and error-handling
principles shared across drivers and languages. See the SDK pages for function names
and complete code.

<a id="connection-string-authentication"></a>

## Connection Strings and Authentication

Connections require a host, native port, user, and authentication information. The
default port is `5656`; check `machbase.conf` in the deployed environment.

| Item | Check |
|------|-----------|
| Host/port | TCP reachability from the application host |
| User | Minimum privileges for the target database and tables |
| Password | Supply through environment variables or a secret manager |
| Database | SDK support for initial database selection |
| Timeouts | Connection, command, and read limits appropriate for the workload |
| Time zone | Supported option names and scope in the SDK and server |

Example `SYS`/`MANAGER` credentials are for local validation. Create dedicated accounts
for production applications; do not record passwords in source, command history, or logs.

AUTH KEY signs challenges with a private key instead of a password. Check key formats,
file permissions, and SDK options in
[AUTH KEY Authentication](/dbms/security-access-control/authentication-auth-key/)
and the driver documentation.

With connection pools, verify reset behavior so a returned connection's database,
session settings, and open statements do not affect the next request.

<a id="timezone-connection"></a>

## Time Zones and Time Values

Machbase `DATETIME` supports nanosecond precision. Manage the meaning of a timestamp
separately from its representation.

- Specify the time reference for collected data: UTC or the business time zone.
- Fix both format and time zone when binding strings.
- Check whether the SDK expects epoch seconds, milliseconds, microseconds, or nanoseconds.
- Round-trip output time zones through the actual connection options or `TO_CHAR()` path.
- Do not interchange `NOW` and `SYSDATE` in business rules; check their meanings in
  the SQL reference.

For string round-trip tests, compare input, query output, and output after a time zone
change on the same connection. See [SQL Functions](/dbms/reference/sql/functions/functions-full/)
for function details.

<a id="prepared-statement"></a>

## Prepared statement

Prepared statements separate SQL structure from values and support repeated execution
of the same SQL.

```text
INSERT INTO sensor_data VALUES (?, ?, ?)
SELECT value FROM sensor_data WHERE name = ? AND time >= ?
```

Check that the preparing connection and current database have not changed. Close the
statement after use. For SDK statement caches, check cache scope, eviction policy,
and reset behavior on database changes.

Some syntax positions, such as CTEs or LIMIT, may not allow parameter placeholders.
On a syntax error, check [Named Bind Parameter](/dbms/reference/sql/syntax/named-bind-parameter-syntax/)
and SDK placeholder support before concatenating values into SQL.

<a id="parameter-binding"></a>

## Parameter binding

| Value | Recommended method |
|---------|-----------|
| Integers/floating-point numbers | Match fixed-width language types to SQL ranges |
| Strings | Check encoding and maximum length |
| DATETIME | Use SDK time objects or the specified epoch unit |
| NULL | Specify the language NULL representation and SQL type |
| DECIMAL | Prefer the SDK exact fixed-point type over string conversion |
| Binary/IP | Use SDK-required byte arrays or dedicated types |

Positional `?` placeholders bind in occurrence order. Use named `:name` placeholders
only with supported servers and SDKs, and check repeated-name rules. Identifiers and
SQL keywords cannot be bound as values; validate them against an allowlist before
constructing SQL.

<a id="dml-affected-rows"></a>

## DML Affected-Row Counts

After `INSERT`, `UPDATE`, or `DELETE`, check the SDK affected-row count. A success
response alone does not prove the intended business record changed.

- For a single-row change, check that the count is 1.
- For 0 rows, check whether no row matched or the change was already applied.
- Check error codes and exceptions separately for insufficient privileges or unsupported DML.
- Before bulk changes, check the scope with `COUNT(*)` using the same condition.
- For Append, check success/failure counts from close/server responses instead of SQL affected rows.

<a id="transaction"></a>

## Transactions

Use explicit `BEGIN`, `COMMIT`, and `ROLLBACK` for relational DML on TRANSACTION tables.
Do not assume LOG/TAG Append shares the same rollback scope.

1. Check whether the SDK provides a transaction API.
2. If not, execute supported transaction-control SQL on the same connection.
3. Verify rollback and connection reuse on error paths.
4. Leave no unfinished transaction when returning a pooled connection.
5. For mixed table types, verify each statement's commit scope in advance.

See [TRANSACTION Table Transactions](/dbms/rdb-table-usage/transaction/) for complete SQL examples.

<a id="append-api-batch"></a>

## Append APIs and Batches

See [Data Ingestion and Export](../data-input-load-export/) for input choices and result
checks, and the [SDK Append Matrix](../sdk-support-scope/#append-table-type-matrix) for
client/table-type support. Separate Append and ordinary query connections, and check
flush, close, and failed rows.

<a id="error-handling-retry"></a>

## Error Handling and Retries

Classify errors as connection, authentication/authorization, SQL/schema, data, or resource exhaustion.

- Retry only disconnects and transient timeouts, with bounded attempts and backoff.
- Do not automatically retry authentication, privilege, syntax, or type errors before fixing them.
- Clean up statements, cursors, Append handles, and connections before retrying.
- Make INSERT retries idempotent with business keys or duplicate-handling policies.
- Log server error codes and messages, excluding credentials and raw sensitive data.
- Validate failed pooled connections before returning them, or discard them.

See [Troubleshooting](/dbms/troubleshooting/) for operational error classification and diagnosis.
