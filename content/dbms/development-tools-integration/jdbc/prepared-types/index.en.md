---
type: docs
title: '11.5.1 PreparedStatement and Types'
weight: 10
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/prepared-types/
---

PreparedStatement prepares SQL on the server and executes it repeatedly with different parameter values.
Machbase JDBC supports standard positional parameters and a named-parameter extension.

## ParameterMetaData

Use `PreparedStatement.getParameterMetaData()` to inspect parameter counts and types before execution.
The same API applies to INSERT, UPDATE, and SELECT.

```java
import java.sql.ParameterMetaData;
import java.sql.PreparedStatement;

try (PreparedStatement statement = connection.prepareStatement(
         "INSERT INTO sensor_tx " +
         "(id, value, created_at) VALUES (?, ?, ?)")) {
    ParameterMetaData metadata = statement.getParameterMetaData();

    for (int index = 1; index <= metadata.getParameterCount(); index++) {
        System.out.printf(
            "%d: type=%s precision=%d scale=%d nullable=%d%n",
            index,
            metadata.getParameterTypeName(index),
            metadata.getPrecision(index),
            metadata.getScale(index),
            metadata.isNullable(index));
    }
}
```

Parameter indexes start at 1. An index of 0 or greater than the parameter count raises
`SQLException`. Interpret precision according to the type: for numeric types, it is the JDBC
number of decimal digits, not storage size in bytes. DATETIME maps to
`java.sql.Types.TIMESTAMP`, but its database type name is `DATETIME`.

## Named Bind Parameter

The `:name` placeholder and `MachPreparedStatement.setObject(String, Object)` are Machbase
extensions. When a name occurs more than once, the value is bound to every matching position.

```java
import com.machbase.jdbc.MachPreparedStatement;

try (MachPreparedStatement statement =
         (MachPreparedStatement) connection.prepareStatement(
             "SELECT id FROM sensor_tx " +
             "WHERE id = :id OR parent_id = :id")) {
    statement.setObject("id", Integer.valueOf(10));

    try (ResultSet result = statement.executeQuery()) {
        while (result.next()) {
            System.out.println(result.getInt("ID"));
        }
    }
}
```

- Names may include or omit the leading colon.
- Names are case-sensitive.
- Do not mix named setters and numeric-index setters in one statement.
- An unknown name or mixed named/positional binding raises SQLState `07009`.
- An older server without named binding support raises SQLState `0A000`.

For portability, use the JDBC standard `?` placeholder and numeric-index setters. See
[Named Bind Parameter](/dbms/reference/sql/syntax/named-bind-parameter-syntax/) for the shared syntax.

## Reexecute a Prepared SELECT

You can execute SELECT repeatedly with the same PreparedStatement. Close the previous ResultSet
and bind new values; the next execution returns a new ResultSet.

```java
try (PreparedStatement statement = connection.prepareStatement(
         "SELECT id, name FROM sensor_tx WHERE id = ?")) {
    ResultSetMetaData metadata = statement.getMetaData();
    System.out.println(metadata.getColumnCount());

    for (int id = 1; id <= 2; id++) {
        statement.setInt(1, id);
        try (ResultSet result = statement.executeQuery()) {
            while (result.next()) {
                System.out.println(result.getString("NAME"));
            }
        }
    }
}
```

Machbase JDBC does not support multiple open results on one Statement. Consume and close each
ResultSet before the next execution. You can retrieve prepare-time `ResultSetMetaData` again
while the Statement remains open.

## JDBC 4.2 SQLType Binding

Use Java 8 `JDBCType` to specify a parameter SQL type.

```java
import java.math.BigDecimal;
import java.sql.JDBCType;
import java.sql.Timestamp;

try (PreparedStatement statement = connection.prepareStatement(
         "INSERT INTO sensor_tx " +
         "(id, name, value, created_at, payload) " +
         "VALUES (?, ?, ?, ?, ?)")) {
    statement.setObject(1, Integer.valueOf(1), JDBCType.INTEGER);
    statement.setObject(2, "sensor-1", JDBCType.VARCHAR);
    statement.setObject(
        3, new BigDecimal("12.3400"), JDBCType.DECIMAL, 4);
    statement.setObject(
        4, Timestamp.valueOf("2026-07-26 10:00:00"),
        JDBCType.TIMESTAMP);
    statement.setObject(5, new byte[] {1, 2, 3}, JDBCType.BINARY);
    statement.executeUpdate();
}
```

An unknown vendor `SQLType` raises `SQLFeatureNotSupportedException`. Use `BigDecimal` for
DECIMAL and NUMERIC; values are bound with the specified scale.

### SQL NULL

`setNull()` or `setObject(index, null, JDBCType)` sends SQL NULL for the target type.
The following types also support typed NULL:

- `REAL`, `BIT`, `TINYINT`, `BOOLEAN`
- `VARBINARY`, `LONGVARBINARY`, `BLOB`, `CLOB`
- `LONGVARCHAR`

NULL for an unsigned parameter is converted to the native NULL value using ParameterMetaData.
The wire NULL sentinel, one greater than the maximum unsigned data value, cannot be stored as
data. Passing that value raises SQLState `22003`.

| Machbase type | Java type | Data range |
|---------------|-----------|-------------|
| `USHORT` | `Integer` | 0–65534 |
| `UINTEGER` | `Long` | 0–4294967294 |
| `ULONG` | `BigInteger` | 0–18446744073709551614 |

Use `setNull()` to insert NULL instead of passing the sentinel directly.

## Boolean

`setBoolean()` and `setObject(index, value, JDBCType.BOOLEAN)` send 1 for `true` and 0 for
`false`. String input accepts only `true` and `false`, case-insensitively. Other values raise
SQLState `22018`.

## IPv4 and IPv6

Use the `MachPreparedStatement` extension setters for IP address columns.

```java
MachPreparedStatement statement =
    (MachPreparedStatement) connection.prepareStatement(
        "INSERT INTO net_log(ts, src_ip, dst_ip) VALUES (?, ?, ?)");

statement.setLong(1, System.currentTimeMillis() * 1_000_000L);
statement.setIpv4(2, "192.168.1.100");
statement.setIpv6(3, "::1");
statement.executeUpdate();
```

## Nullable Metadata

`ParameterMetaData.isNullable()` returns `parameterNoNulls`, `parameterNullable`, or
`parameterNullableUnknown`. Do not interpret `parameterNullableUnknown` as NOT NULL. See
[Nullable Metadata Support](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-nullable-metadata)
for rules for each SQL statement.
