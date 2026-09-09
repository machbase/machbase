---
type: docs
title: '11.5.4 DatabaseMetaData'
weight: 40
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/database-metadata/
---

`Connection.getMetaData()` returns information about the driver, server, schema objects,
and JDBC capabilities. Result columns use JDBC standard names and ordering; read columns
by name rather than numeric position.

```java
import java.sql.DatabaseMetaData;

DatabaseMetaData metadata = connection.getMetaData();

System.out.println(metadata.getDriverName());
System.out.println(metadata.getDriverVersion());
System.out.println(metadata.getDatabaseProductName());
System.out.println(metadata.getDatabaseProductVersion());
```

## Tables and Views

```java
try (ResultSet tables = metadata.getTables(
         null, null, "%", new String[] {"TABLE", "VIEW"})) {
    while (tables.next()) {
        System.out.printf("%s %s%n",
            tables.getString("TABLE_NAME"),
            tables.getString("TABLE_TYPE"));
    }
}
```

`getTables()` distinguishes TABLE from VIEW. See `REMARKS` for the specific Machbase table
type. Applications should use standard column names instead of depending on column positions.

## Columns

```java
try (ResultSet columns = metadata.getColumns(
         null, null, "SENSOR_TX", "%")) {
    while (columns.next()) {
        System.out.printf(
            "%s %s size=%d nullable=%s%n",
            columns.getString("COLUMN_NAME"),
            columns.getString("TYPE_NAME"),
            columns.getInt("COLUMN_SIZE"),
            columns.getString("IS_NULLABLE"));
    }
}
```

`NULLABLE` returns a numeric constant; `IS_NULLABLE` returns `YES`, `NO`, or an empty string.
PRIMARY KEY columns in LOOKUP and VOLATILE tables return `columnNoNulls` and `NO` even
without an explicit NOT NULL clause.

`DECIMAL_DIGITS` and `NUM_PREC_RADIX` are SQL NULL for columns without these numeric
attributes, such as VARCHAR, DATETIME, BINARY, BLOB, and CLOB. Check NULL with `getObject()`
or `wasNull()` instead of relying on a 0 returned by `getInt()`.

## Primary Keys and Indexes

```java
try (ResultSet keys = metadata.getPrimaryKeys(
         null, null, "SENSOR_TX")) {
    while (keys.next()) {
        System.out.printf("%s position=%d%n",
            keys.getString("COLUMN_NAME"),
            keys.getShort("KEY_SEQ"));
    }
}

try (ResultSet indexes = metadata.getIndexInfo(
         null, null, "SENSOR_TX", false, false)) {
    while (indexes.next()) {
        System.out.printf("%s %s%n",
            indexes.getString("INDEX_NAME"),
            indexes.getString("COLUMN_NAME"));
    }
}
```

Do not infer PRIMARY KEY membership from `ResultSetMetaData.isNullable()`.
Use `getPrimaryKeys()` and `getIndexInfo()`.

For a direct column in a SELECT result, the Machbase JDBC extension
`MachResultSetMetaData.isPrimaryKey(column)` reports PRIMARY KEY membership.

```java
import com.machbase.jdbc.MachResultSetMetaData;

try (ResultSet result = statement.executeQuery(
         "SELECT ID, ID + 1 AS ID_EXPR FROM SENSOR_TX")) {
    MachResultSetMetaData resultMetadata =
        (MachResultSetMetaData) result.getMetaData();
    System.out.println(resultMetadata.isPrimaryKey(1)); // true or false
    System.out.println(resultMetadata.isPrimaryKey(2)); // expression: false
}
```

`getPrimaryKeys()` reads primary keys from the table catalog; `isPrimaryKey()` reads column
metadata for the current SELECT result. An older server or SDK may return `false` for the
result-column primary key flag.

## Schema and Type Information

The following methods return ResultSets in the standard JDBC format:

- `getSchemas()`, `getCatalogs()`, `getTableTypes()`
- `getTypeInfo()`
- `getTables()`, `getColumns()`
- `getPrimaryKeys()`, `getIndexInfo()`

Unsupported optional metadata queries may return an empty ResultSet with standard columns
instead of null or a nonstandard ResultSet. Check the capability methods before using a feature.

```java
if (metadata.supportsSavepoints()) {
    // Use savepoints only where supported.
}
```

## catalog

`Connection.getCatalog()` and `setCatalog()` manage the current catalog value exposed by
the driver. Catalog arguments to metadata methods filter requests against this value.

```java
String initialCatalog = connection.getCatalog();
connection.setCatalog(initialCatalog);
```

Returning a logical Connection to a pool restores the initial catalog determined by the URL.
Do not reuse a DatabaseMetaData object from a previous connection lease in the next lease.

## Check Supported Features

Machbase JDBC capability methods reflect actual support. For example, check transaction
isolation levels, ResultSet types, savepoints, generated keys, and multiple open results as follows:

```java
System.out.println(metadata.supportsTransactions());
System.out.println(metadata.supportsTransactionIsolationLevel(
    Connection.TRANSACTION_SERIALIZABLE));
System.out.println(metadata.supportsResultSetType(
    ResultSet.TYPE_FORWARD_ONLY));
System.out.println(metadata.supportsSavepoints());
System.out.println(metadata.supportsGetGeneratedKeys());
System.out.println(metadata.supportsMultipleOpenResults());
```

A `false` result from `Driver.jdbcCompliant()` is separate from support for individual JDBC
APIs. Applications should check the features they require.

When connected to a Standard Edition server that supports ROWID, `supportsGetGeneratedKeys()`
returns `true`, and `getRowIdLifetime()` returns `ROWID_VALID_OTHER`. On an unsupported server
or Cluster Edition, they return `false` and `ROWID_UNSUPPORTED`, respectively. See
[ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/) for examples.
