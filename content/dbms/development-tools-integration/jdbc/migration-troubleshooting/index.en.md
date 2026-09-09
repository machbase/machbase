---
type: docs
title: '11.5.6 Migration and Troubleshooting'
weight: 60
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/migration-troubleshooting/
---

The current Machbase JDBC driver targets Java 8/JDBC 4.2 and aligns version reporting,
metadata, type conversion, transactions, and resource lifecycles with standard JDBC contracts.
Applications that rely on earlier behavior should review these differences.

## Migrate from an Earlier Driver

| Area | Current behavior | Application checks |
|------|-----------|------------------------|
| Java/JDBC baseline | Java 8 bytecode; reports JDBC 4.2 | Run on JDK 8 or later. |
| Driver version | Driver and metadata report 3.0.0 | Update version-detection logic. |
| Automatic discovery | JDBC service provider included | Explicit `Class.forName()` is optional. |
| ParameterMetaData | Returns JDBC precision, database type names, and Java classes | Interpret precision by type, not as storage bytes. |
| Transactions | Lazy `BEGIN`; actual commit/rollback | Explicitly complete Standard TRANSACTION operations. |
| Holdability | `CLOSE_CURSORS_AT_COMMIT` | Requery ResultSets after commit. |
| DatabaseMetaData | Standard result structure and capabilities | Use standard column names instead of driver-specific positions. |
| Type APIs | Typed `getObject()`, `JDBCType`, Boolean, unsigned, LOB | Retrieve and bind using the Java classes in metadata. |
| Errors | Standard `SQLException` for invalid states | Classify errors by SQLState. |
| Timeouts | Query and network timeouts supported | Discard connections after a network timeout. |
| Connection pools | Logical connection leases and state reset | Do not reuse closed handles or metadata. |
| Generated keys | Returns ROWID for a single Standard INSERT | Read `ROWID` from `getGeneratedKeys()`. |

Use named binding with a compatible server. An older server without named binding support
raises SQLState `0A000`; switch to positional `?` parameters.

## Unsupported Features

The following optional JDBC features are not supported:

- Savepoints
- XA and distributed transactions
- Stored procedures and successful CallableStatement execution
- Scrollable or updatable ResultSets
- Statement pooling
- Multiple open results
- Struct, Ref, SQLXML, and UDT type mapping
- Separate NClob storage and factories
- A Machbase-specific RowSet provider
- JDBC 4.3 sharding and request boundary APIs

Machbase DBMS 8.7.0 with an ARRAY-capable JDBC build supports `java.sql.Array`,
`createArrayOf()`, and `setArray()`. Do not apply older drivers' ARRAY restrictions. Check
the version and index conventions in [ARRAY and Selected-Column Append](../append-api/#array와-선택-컬럼).

Unsupported features generally raise `SQLFeatureNotSupportedException` with SQLState
`0A000`. Check DatabaseMetaData capabilities before calling a feature.

## `No suitable driver`

**Symptom**

`DriverManager.getConnection()` raises `No suitable driver`.

**Checks and Resolution**

1. Check that `machbase.jar` is on the runtime classpath.
2. Check that the JAR contains `META-INF/services/java.sql.Driver`.
3. Check that the URL uses `jdbc:machbase://<host>:<port>/machbasedb`.
4. Check that multiple Machbase JDBC JAR versions are not included together.

## SQLState `0A000`

The selected feature or server does not support the API. Use alternatives to savepoints,
scrollable cursors, and XA. Generated keys require Standard Edition and a server/JDBC
combination with ROWID support; check `DatabaseMetaData.supportsGetGeneratedKeys()`.
For named binding errors, use positional `?` parameters.

## ResultSet Closes After Commit

This is expected. Machbase transaction holdability is `CLOSE_CURSORS_AT_COMMIT`. Consume
results before committing or run the query again afterward. Statements and PreparedStatements
remain reusable.

## LOG DML Is Not Rolled Back

The first LOG DML executed before a TRANSACTION table change in a manual transaction may
be reexecuted with auto-commit through the compatibility path. This input cannot be rolled
back later. Use TRANSACTION tables for data that requires rollback.

## Commit Multiple TRANSACTION Tables Together

Normal commit and rollback are supported, but global atomicity across multiple TRANSACTION
tables is not guaranteed if a failure occurs during backend commit. Keep critical atomic
operations within one TRANSACTION table.

## Network Timeout or Connection Error

After a socket read timeout or a connection error in SQLState class `08`, do not reuse the
physical connection. Obtain a new connection from the pool and restart active transactions
according to the application idempotency policy. Do not infer commit success from an exception alone.

## Reuse of Closed Pool Objects

Reusing Statements, ResultSets, or DatabaseMetaData from a closed logical Connection in the
next connection lease raises SQLState `08003`. Keep each lease's objects within its
try-with-resources scope.
