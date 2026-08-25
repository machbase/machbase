---
type: docs
title: '11.2 Common Integration Concepts'
weight: 20
toc: true
aliases:
  - /dbms/application-integration/concepts-common/
---

Apply these connection, binding, transaction, bulk-input, and error-handling rules regardless of
the application language. Use the SDK pages in this chapter for exact functions and complete code.

<a id="connection-string-authentication"></a>

## Connection strings and authentication

| Item | Check |
|---|---|
| Host and port | TCP connectivity from the application host |
| User | Minimum privileges for the target database and tables |
| Password | Injection through an environment variable or secret manager |
| Database | Whether the SDK supports initial database selection |
| Timeout | Connection, command, and read limits for the workload |
| Timezone | The SDK option name and its scope |

Port `5656` is the default native port; confirm `PORT_NO` in the deployment's `machbase.conf`.
`SYS`/`MANAGER` in examples is for local verification. Use a dedicated production account and do not
record passwords in source, shell history, or logs.

AUTH KEY signs a server challenge with a private key. Verify key format, file permissions, and SDK
support in [AUTH KEY authentication](../../security-access-control/authentication-auth-key/) and the
selected SDK page. When using a pool, verify that database and session state are reset before a
connection is reused.

<a id="timezone-connection"></a>

## Timezone and time values

Machbase `DATETIME` supports nanosecond precision. Keep the meaning of a timestamp separate from its
representation.

- Declare whether collected values use UTC or a business timezone.
- Fix both format and timezone when binding strings.
- Confirm whether epoch values use seconds, milliseconds, microseconds, or nanoseconds.
- Round-trip values through the actual connection option or SQL conversion path.
- Do not mix `NOW` and `SYSDATE` without confirming their required semantics.

See [SQL functions](../../reference/sql/dictionary/functions-full/) for conversion functions.

<a id="prepared-statement"></a>

## Prepared statements

Use prepared statements to separate SQL structure from values and to repeat the same statement.

```text
INSERT INTO sensor_data VALUES (?, ?, ?)
SELECT value FROM sensor_data WHERE name = ? AND time >= ?
```

Prepare and execute on the same connection and current database, then close the statement. If the
SDK caches statements, verify cache lifetime and reset behavior when switching databases.

<a id="parameter-binding"></a>

## Parameter binding

| Value | Guidance |
|---|---|
| Integer and floating point | Match language widths to SQL type ranges |
| String | Confirm encoding and maximum length |
| DATETIME | Use the SDK time object or an explicitly documented epoch unit |
| NULL | Supply both the language NULL representation and SQL type when required |
| DECIMAL | Prefer the SDK's exact decimal type |
| Binary and IP | Use the SDK byte array or dedicated type |

Bind positional `?` markers in occurrence order. Use named `:name` markers only when both server and
SDK support them. Identifiers and SQL keywords cannot be value parameters; validate them against an
allowlist before constructing SQL.

<a id="dml-affected-rows"></a>

## Affected rows

Check the affected-row count after `INSERT`, `UPDATE`, or `DELETE`. A successful call does not prove
that the intended row changed. For Append, check acknowledgement, close or flush results, and the
successful and failed row counts instead of a SQL affected-row count.

<a id="transaction"></a>

## Transactions

Use explicit transaction control for relational DML on TRANSACTION tables. Do not assume LOG or TAG
Append belongs to the same rollback unit.

1. Confirm that the SDK exposes a transaction API.
2. If it does not, use supported transaction SQL on the same connection.
3. Roll back on error and validate the connection before reuse.
4. Do not return a connection with an unfinished transaction to a pool.
5. Verify commit boundaries before mixing table types.

See [TRANSACTION table transactions](../../rdb-table-usage/transaction/) for executable SQL.

<a id="append-api-batch"></a>

## Append API and batch input

| Method | Suitable workload | Verify |
|---|---|---|
| Single INSERT | Low volume and immediate error handling | Affected rows and generated ID |
| Prepared batch | Repeated SQL at medium volume | Per-item results and failures |
| Append API | Continuous high-volume TAG or LOG input | Ack, success/failure counts, flush and close |
| File tool | Large file import | Log, bad file, input and failure counts |

Keep Append and query connections separate. Match column order and types to the table schema. See
[SDK feature support](../sdk-support-scope/#support-scope-sdk-append) for the supported SDKs.

<a id="error-handling-retry"></a>

## Error handling and retries

- Retry only transient connection loss and timeouts, with a bounded count and backoff.
- Do not retry authentication, privilege, syntax, or type errors before correcting the cause.
- Close statements, cursors, Append handles, and connections before retrying.
- Make INSERT retries idempotent through a business key or duplicate policy.
- Record server error codes and messages without credentials or sensitive source data.
- Validate or discard a failed pooled connection before returning it.

See [Troubleshooting](../../troubleshooting/) for operational diagnosis.
