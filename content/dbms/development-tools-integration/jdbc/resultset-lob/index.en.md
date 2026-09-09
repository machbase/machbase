---
type: docs
title: '11.5.2 ResultSet, Statement, and LOB'
weight: 20
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/resultset-lob/
---

Machbase JDBC ResultSet is a forward-only, read-only cursor. Close Connections, Statements,
and ResultSets with try-with-resources.

```java
statement.getResultSetType();        // ResultSet.TYPE_FORWARD_ONLY
statement.getResultSetConcurrency(); // ResultSet.CONCUR_READ_ONLY
```

Scrollable and updatable ResultSets are not supported. Getter calls before `next()`, after
the last row, or after close, and out-of-range column indexes raise `SQLException`.

## Typed Retrieval

Both `getObject(index, Class<T>)` and `getObject(label, Class<T>)` are supported.

```java
import java.math.BigDecimal;
import java.sql.Timestamp;

try (ResultSet result = statement.executeQuery(
         "SELECT id, value, created_at FROM sensor_tx")) {
    while (result.next()) {
        Integer id = result.getObject("ID", Integer.class);
        BigDecimal value =
            result.getObject("VALUE", BigDecimal.class);
        Timestamp createdAt =
            result.getObject("CREATED_AT", Timestamp.class);
    }
}
```

| Java type | Typical Machbase type |
|-----------|-------------------------|
| `String` | CHAR, VARCHAR, TEXT, IPV4, IPV6, JSON |
| `Short`, `Integer`, `Long` | Integer types |
| `Float`, `Double` | Floating-point types |
| `BigDecimal` | DECIMAL, NUMERIC |
| `Boolean` | BOOLEAN |
| `Timestamp`, `Date`, `Time` | DATETIME |
| `byte[]` | BINARY |
| `Blob`, `Clob` | BLOB, CLOB |

Object getters return Java `null` for SQL NULL. Primitive getters return 0 or `false`; call
`wasNull()` immediately afterward to check for SQL NULL. Unsupported conversions and a null
target class raise `SQLException`.

In Machbase SQL, the empty string literal `''` is SQL `NULL`. For that result column,
`ResultSetMetaData.isNullable()` returns `columnNullable`, and `getObject()` returns `null`.
The literal `''''` is a single quote character, so it is a non-NULL string.

The default object mappings for unsigned types are:

| Machbase type | `getObject()` return type |
|---------------|-------------------------|
| `USHORT` | `Integer` |
| `UINTEGER` | `Long` |
| `ULONG` | `BigInteger` |

`SHORT` returns an `Integer` object; 32-bit `FLOAT` returns a `Float` object. BOOLEAN strings
accept only `true` and `false`.

## Character and Binary Streams

`setAsciiStream()`, `setBinaryStream()`, and `setCharacterStream()` provide overloads with
`int` length, `long` length, or no length. `setNCharacterStream()` and `setNString()` are
aliases for the VARCHAR path, not a separate NCHAR storage type.

ResultSet supports the following getters by index or column name:

- `getAsciiStream()`, `getBinaryStream()`
- `getCharacterStream()`, `getNCharacterStream()`
- `getNString()`

Input shorter than its declared length, a negative length, or a length greater than
`Integer.MAX_VALUE` raises `SQLException`. Streams currently materialize in client memory;
do not use them for constant-memory streaming of large values.

## BLOB and CLOB

Use standard `Blob` and `Clob` objects to retrieve and bind BLOB/CLOB columns in LOG tables.

```java
import java.io.ByteArrayInputStream;
import java.io.StringReader;
import java.sql.Blob;
import java.sql.Clob;

try (PreparedStatement insert = connection.prepareStatement(
         "INSERT INTO event_log (payload, message) VALUES (?, ?)")) {
    insert.setBlob(1, new ByteArrayInputStream(payload));
    insert.setClob(2, new StringReader(message));
    insert.executeUpdate();
}

try (ResultSet result = statement.executeQuery(
         "SELECT payload, message FROM event_log")) {
    while (result.next()) {
        Blob payloadObject = result.getBlob("PAYLOAD");
        Clob messageObject = result.getClob("MESSAGE");

        byte[] payloadBytes = payloadObject.getBytes(
            1, (int) payloadObject.length());
        String messageText = messageObject.getSubString(
            1, (int) messageObject.length());

        payloadObject.free();
        messageObject.free();
    }
}
```

Create mutable objects with `Connection.createBlob()` and `createClob()`, then use
`setBytes()`, `setString()`, `setBinaryStream()`, `setCharacterStream()`, or `truncate()`.
Call `free()` when finished.

LOB positions are 1-based, as required by JDBC. The entire requested partial-stream range
must fit within the value. A range beyond the end raises SQLState `22003` instead of returning
a truncated result. A negative length or a length that a Java array cannot represent raises
`HY090`. Reusing an object after `free()` raises `SQLException`.

LOBs materialize the entire value in client memory. This is not a streaming LOB implementation
that processes values of hundreds of MiB or more with constant memory.

## ResultSet Metadata

Use `ResultSetMetaData.isNullable()` to inspect nullability of SELECT result columns.

```java
ResultSetMetaData metadata = result.getMetaData();
int nullable = metadata.isNullable(columnIndex);
```

`columnNullableUnknown` does not mean NOT NULL. Check table column constraints with
`DatabaseMetaData.getColumns()` and retrieve PRIMARY KEY information separately with
`DatabaseMetaData.getPrimaryKeys()`.

## Row Counts and Fetch Settings

The JDBC 4.2 large update API returns affected-row counts as `long`.

```java
long count = statement.executeLargeUpdate(
    "DELETE FROM sensor_tx WHERE id < 100");
long[] counts = statement.executeLargeBatch();
```

`setLargeMaxRows()` and `getLargeMaxRows()` are also available. `setMaxRows()` or
`setLargeMaxRows()` limits the number of rows retrieved from a ResultSet without changing
the Statement `fetchSize`.

## Statement Lifecycle

- With `closeOnCompletion()`, the Statement closes when its last ResultSet closes.
- Close the previous ResultSet before reexecuting a Statement.
- Commit closes ResultSets, but Statements and PreparedStatements remain reusable.
- Do not call `next()` and getters concurrently from multiple threads on one ResultSet.

## Cancellation and Query Timeout

`Statement.cancel()` cancels the current statement through a separate session. If no statement
is running, it does nothing. PreparedStatement bindings and metadata are preserved.

When `setQueryTimeout(seconds)` expires, it raises `SQLTimeoutException` with SQLState
`HYT00`. After handling the exception, you can reuse the Statement for the next query.
A timeout task from a previous execution does not cancel the next execution.

To run independent queries in parallel, obtain one logical Connection per worker from a
connection pool instead of sharing one Connection. To stop an ongoing fetch, another thread
may call `close()`, `cancel()`, or `Connection.abort()`.
