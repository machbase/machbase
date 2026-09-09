---
type: docs
title: '11.5 JDBC'
weight: 50
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/
---

The Machbase JDBC driver provides core JDBC 4.2 APIs with a Java 8 baseline. Use standard
JDBC APIs for connections, PreparedStatements, typed retrieval and binding, database
metadata, local transactions, and connection pools.

| Item | Value |
|------|----|
| Java bytecode baseline | Java 8 |
| Reported JDBC version | 4.2 |
| Driver version | 3.0.0 |
| JDBC URL | `jdbc:machbase://<host-list>/[database]` |
| `Driver.jdbcCompliant()` | `false` |

A `false` result from `jdbcCompliant()` concerns full SQL-92 Entry Level compliance,
not JDBC 4.2 API support. Check required optional features through `DatabaseMetaData`
capability methods.

## Multiple Databases

Specify the initial database in the URL path or the `database` connection property.

```java
String url = "jdbc:machbase://127.0.0.1:5656/factory_a";
Connection conn = DriverManager.getConnection(url, "APP_A", password);

System.out.println(conn.getCatalog());
conn.setCatalog("FACTORY_A");
```

`getCatalog()` and `setCatalog()` synchronize with the server's current database. If both
the URL path and property specify a database, their values must match. In JDBC metadata,
a catalog is a database and a schema is an owner. Check that pooled connections restore
the initial catalog when returned. Prepared statements and append handles remain bound
to the database in which they were created.

## Install the Driver

### Use a JAR File

Add `machbase.jar` from the Machbase installation directory to the classpath.

```bash
ls -l "$MACHBASE_HOME/lib/machbase.jar"
javac -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp.java
java -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp
```

The JAR includes `META-INF/services/java.sql.Driver`. In JDBC 4.0 and later environments,
the driver registers automatically without
`Class.forName("com.machbase.jdbc.MachDriver")`. Existing explicit calls remain valid.

### Maven

```xml
<dependency>
    <groupId>com.machbase</groupId>
    <artifactId>machjdbc</artifactId>
    <version>{{< jdbc_version >}}</version>
</dependency>
```

### Gradle

```groovy
dependencies {
    implementation 'com.machbase:machjdbc:{{< jdbc_version >}}'
}
```

Check artifact versions in [Maven Central](https://mvnrepository.com/artifact/com.machbase/machjdbc).
The runtime metadata version `3.0.0` and distribution artifact versions use different
versioning schemes.

## Connect to the Server

Supply user names and passwords through environment variables or a secret manager
instead of embedding them in source code.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.Properties;

String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";

Properties properties = new Properties();
properties.setProperty("user", "SYS");
properties.setProperty("password", System.getenv("MACHBASE_PASSWORD"));

try (Connection connection =
         DriverManager.getConnection(url, properties)) {
    // Execute SQL.
}
```

### Connection Options

Specify connection options through `Properties` or URL query parameters. Set
`randomHost` in `Properties`, or use `^` separators in a multi-host URL.

| Option | Description |
|------|------|
| `user`, `password` | Password authentication credentials |
| `TIMEZONE` | Session time zone in `+0900` format |
| `randomHost` | Selects the first connection host randomly from the list |
| `maxStatements` | Maximum cached Statements for a pooled connection |
| `CONNECTION_TIMEOUT` | Socket connection timeout in seconds; `0` means unlimited |
| `SOCKET_TIMEOUT` | Socket read timeout in seconds; `0` means unlimited |
| `characterEncoding` | Client character encoding |
| `AUTH_MODE` | `PASSWORD` or `CHALLENGE` |
| `AUTH_SIG_SCHEME` | `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS` |
| `AUTH_KEY_FILE` | Path to a PEM private key file |

```java
String url =
    "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
```

<a id="jdbc-multi-host"></a>

### Multiple Hosts

The Machbase 8.7.0 JDBC driver accepts multiple hosts in one URL.

| Selection | Syntax | Behavior |
|-----------|-----------|------|
| Sequential | Separate hosts with `,` | Attempts connections in URL order |
| Random start | Separate hosts with `^` | Randomly selects the first host |
| Random start | Set `randomHost=true` in `Properties` | Randomly selects the first host from a comma-separated list |

This URL tries `db2` if connecting to `db1` fails:

```java
String url =
    "jdbc:machbase://db1.example.com:5656,db2.example.com:5656/" +
    "machbasedb?CONNECTION_TIMEOUT=5";
```

The `^` separator selects the first host randomly:

```java
String url =
    "jdbc:machbase://db1.example.com:5656^db2.example.com:5656/" +
    "machbasedb?CONNECTION_TIMEOUT=5";
```

When using the `randomHost` property, separate hosts with commas:

```java
Properties properties = new Properties();
properties.setProperty("randomHost", "true");

String url =
    "jdbc:machbase://db1.example.com:5656,db2.example.com:5656/" +
    "machbasedb?CONNECTION_TIMEOUT=5";
```

- Do not mix `,` and `^` separators in one URL.
- Connection-stage I/O errors, such as connection refusal, connection timeout, or socket
  errors, cause an attempt to the next host. If all hosts fail,
  `DriverManager.getConnection()` throws `SQLException`.
- `CONNECTION_TIMEOUT` applies per host attempt. Total connection wait time can therefore
  increase with the number of hosts and their response times.
- `SOCKET_TIMEOUT` limits reads on the connected socket; it does not change host selection order.

Multi-host failover applies to socket establishment for new connections or reconnections.
Even if automatic reconnection succeeds after a disconnect, do not reuse earlier Statements,
PreparedStatements, or ResultSets. It does not guarantee whether in-flight SQL succeeded
or can be safely retried. On a connection error in an active transaction, discard the
connection and retry the entire transaction according to the application idempotency policy.

## AUTH KEY Authentication

Public-key challenge authentication signs the server challenge with a local private
key instead of using a password.

```java
Properties properties = new Properties();
properties.setProperty("user", "app_user");
properties.setProperty("AUTH_MODE", "CHALLENGE");
properties.setProperty("AUTH_SIG_SCHEME", "ECDSA");
properties.setProperty(
    "AUTH_KEY_FILE", "/opt/machbase/keys/app_user_ecdsa.pem");

Connection connection = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/machbasedb", properties);
```

- `AUTH_MODE=CHALLENGE` does not use `password` for authentication.
- `AUTH_KEY_FILE` is required.
- If `AUTH_SIG_SCHEME` is omitted, a default scheme is selected for the key type.
- On POSIX systems, restrict private key file permissions to `600`.

## Quick Start

This example inserts values into a LOG table and queries them.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Properties;

public class JdbcQuickStart {
    public static void main(String[] args) throws Exception {
        Properties properties = new Properties();
        properties.setProperty("user", "SYS");
        properties.setProperty(
            "password", System.getenv("MACHBASE_PASSWORD"));

        try (Connection connection = DriverManager.getConnection(
                 "jdbc:machbase://127.0.0.1:5656/machbasedb",
                 properties);
             Statement statement = connection.createStatement()) {
            statement.execute(
                "CREATE LOG TABLE jdbc_sensor " +
                "(ts DATETIME, name VARCHAR(40), value DOUBLE)");

            try (PreparedStatement insert = connection.prepareStatement(
                     "INSERT INTO jdbc_sensor VALUES (?, ?, ?)")) {
                insert.setLong(1, System.currentTimeMillis() * 1_000_000L);
                insert.setString(2, "sensor-1");
                insert.setDouble(3, 25.3);
                insert.executeUpdate();
            }

            try (ResultSet result = statement.executeQuery(
                     "SELECT name, value FROM jdbc_sensor")) {
                while (result.next()) {
                    System.out.printf("%s %.1f%n",
                        result.getString("NAME"),
                        result.getDouble("VALUE"));
                }
            }
        }
    }
}
```

Use `long` to pass DATETIME values as epoch nanoseconds. If the example table already
exists, omit `CREATE LOG TABLE` or use a different name.

## ROWID from INSERT

After a successful single `INSERT ... VALUES` in Standard Edition, use the standard
JDBC generated keys API to retrieve the inserted row's ROWID.

```java
String sql = "INSERT INTO jdbc_sensor VALUES (?, ?, ?)";
try (PreparedStatement insert = connection.prepareStatement(
         sql, Statement.RETURN_GENERATED_KEYS)) {
    insert.setLong(1, System.currentTimeMillis() * 1_000_000L);
    insert.setString(2, "sensor-2");
    insert.setDouble(3, 26.1);
    insert.executeUpdate();

    try (ResultSet keys = insert.getGeneratedKeys()) {
        if (keys.next()) {
            java.sql.RowId rowId = keys.getRowId("ROWID");
        }
    }
}
```

The result has one `ROWID` column and at most one row. If there is no ROWID to return,
the `ResultSet` is empty. Check `DatabaseMetaData.supportsGetGeneratedKeys()` for support.
See [ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/) for differences in batches,
Append, `INSERT ... SELECT`, and UPSERT.

## Check Versions

```java
import java.sql.DatabaseMetaData;

DatabaseMetaData metadata = connection.getMetaData();

System.out.println(metadata.getDriverName());
System.out.println(metadata.getDriverVersion());
System.out.println(metadata.getJDBCMajorVersion()); // 4
System.out.println(metadata.getJDBCMinorVersion()); // 2
```

## Related Documents

| Document | Content |
|------|------|
| [PreparedStatement and Types](./prepared-types/) | Parameter metadata, named binding, SQLType, NULL, and type conversion |
| [ResultSet, Statement, and LOB](./resultset-lob/) | Typed retrieval, streams, LOBs, timeouts, and resource management |
| [Transactions and Connection Pools](./transaction-pooling/) | Standard local transactions, DataSource, and connection pools |
| [DatabaseMetaData](./database-metadata/) | Tables, columns, keys, indexes, and capabilities |
| [Append API](./append-api/) | High-speed ingestion through `MachStatement` |
| [Migration and Troubleshooting](./migration-troubleshooting/) | Migration from earlier drivers, unsupported features, and error handling |
