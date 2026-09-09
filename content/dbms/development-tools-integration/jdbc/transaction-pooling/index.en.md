---
type: docs
title: '11.5.3 Transactions and Connection Pools'
weight: 30
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/transaction-pooling/
---

Machbase JDBC supports standard JDBC local transactions on Standard Edition TRANSACTION tables.
Cluster Edition has no TRANSACTION tables, so the transaction features on this page do not apply.

## Create a TRANSACTION Table

```sql
CREATE TRANSACTION TABLE sensor_tx
(
    id         INTEGER PRIMARY KEY,
    parent_id  INTEGER,
    name       VARCHAR(64),
    value      DECIMAL(20, 4),
    created_at DATETIME,
    payload    BINARY
);
```

## Commit and Rollback

Use `setAutoCommit(false)`, `commit()`, and `rollback()`. Applications do not need to send
SQL `BEGIN` explicitly.

```java
import java.sql.PreparedStatement;
import java.sql.SQLException;

connection.setAutoCommit(false);

try (PreparedStatement statement = connection.prepareStatement(
         "INSERT INTO sensor_tx (id, value) VALUES (?, ?)")) {
    statement.setInt(1, 1);
    statement.setBigDecimal(2, new BigDecimal("10.5000"));
    statement.executeUpdate();
    connection.commit();
} catch (SQLException exception) {
    try {
        connection.rollback();
    } catch (SQLException rollbackException) {
        exception.addSuppressed(rollbackException);
    }
    throw exception;
}
```

`setAutoCommit(false)` does not send `BEGIN` immediately. The transaction starts when the
first Statement runs in manual mode. After commit or rollback, auto-commit remains `false`,
and the next Statement starts a new transaction.

- Switching to `setAutoCommit(true)` first commits any active transaction.
- Calling `commit()` or `rollback()` when auto-commit is `true` raises SQLState `25000`.
- Closing a Connection rolls back unfinished transactions.
- Commit and rollback close open ResultSets; Statements remain reusable.

## Isolation Level and Cursors

The supported isolation level is `Connection.TRANSACTION_SERIALIZABLE`. Requesting another
level raises `SQLFeatureNotSupportedException`.

The supported holdability is `ResultSet.CLOSE_CURSORS_AT_COMMIT`. Consume required results
before committing, or execute the query again after commit.

## Behavior by Table Type

| Operation | Behavior in a manual transaction |
|------|--------------------------|
| TRANSACTION table DML/SELECT | Participates in the transaction. |
| LOG/TAG table SELECT | Allowed. |
| First LOG DML before a TRANSACTION change | May be reexecuted with auto-commit through the compatibility path. |
| Standalone TAG DML | Participates in the transaction and can be rolled back. |
| LOG/TAG DML or DDL after a TRANSACTION change | Raises an error. |

LOG DML reexecuted with auto-commit through the compatibility path cannot be rolled back later.
Use TRANSACTION tables for data that requires rollback. Normal commit and rollback across multiple
TRANSACTION tables are supported, but global atomicity is not guaranteed if a failure occurs during
backend commit. Keep critical atomic operations within one TRANSACTION table.

## DataSource

Use `MachDataSource` to supply connection properties to an application server or framework.

```java
import com.machbase.jdbc.MachDataSource;
import java.sql.Connection;

MachDataSource dataSource = new MachDataSource();
dataSource.setUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
dataSource.setUser("SYS");
dataSource.setPassword(System.getenv("MACHBASE_PASSWORD"));
dataSource.setLoginTimeout(10);

try (Connection connection = dataSource.getConnection()) {
    // Execute SQL.
}
```

DataSource supports the URL, user, password, login timeout, log writer, and JDBC `Wrapper` contract.

## ConnectionPoolDataSource

`MachConnectionPoolDataSource` returns logical Connections without exposing physical connections.

```java
import com.machbase.jdbc.MachConnectionPoolDataSource;
import java.sql.Connection;
import javax.sql.PooledConnection;

MachConnectionPoolDataSource source =
    new MachConnectionPoolDataSource();
source.setUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
source.setUser("SYS");
source.setPassword(System.getenv("MACHBASE_PASSWORD"));

PooledConnection pooled = source.getPooledConnection();
try {
    try (Connection logical = pooled.getConnection()) {
        // Use the logical connection.
    }
} finally {
    pooled.close();
}
```

Only one logical handle is active per PooledConnection. Closing a logical Connection resets
the following state, then fires `connectionClosed` once:

- Roll back unfinished transactions
- Restore auto-commit
- Restore the initial catalog determined by the URL
- Restore the network timeout

The next connection lease is not issued until calls on the closing logical handle finish.
A closed Connection, Statement, or DatabaseMetaData cannot be reused in the next lease; doing
so raises SQLState `08003`. Statement pooling is not supported.

A fatal connection error in SQLState class `08` discards the physical connection and fires
`connectionErrorOccurred`. Class `23` errors, such as duplicate keys, do not indicate a damaged
connection and do not fire a connection error event.

## HikariCP

```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
config.setUsername("SYS");
config.setPassword(System.getenv("MACHBASE_PASSWORD"));
config.setMaximumPoolSize(10);
config.setMinimumIdle(2);
config.setConnectionTimeout(30_000);
config.setIdleTimeout(600_000);
config.setMaxLifetime(1_800_000);
config.addDataSourceProperty("TIMEZONE", "+0900");

try (HikariDataSource dataSource = new HikariDataSource(config);
     Connection connection = dataSource.getConnection()) {
    // Execute SQL.
}
```

Return logical Connections promptly with try-with-resources. Do not retain returned handles.

## Network timeout

`setNetworkTimeout(executor, milliseconds)` sets the socket read timeout in milliseconds;
`0` means no limit. A negative value, null executor, or executor that rejects tasks raises
`SQLException`.

An actual network timeout raises an exception in SQLState class `08` and invalidates the
physical connection. Obtain a new connection instead of reusing Statements or ResultSets from
the failed connection. I/O failures in active transactions are not retried automatically.
