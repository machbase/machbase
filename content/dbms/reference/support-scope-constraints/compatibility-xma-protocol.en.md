---
type: docs
title: '16.6.9 Server and SDK Compatibility'
weight: 90
toc: true
---

When Machbase server and SDK versions differ, basic connections may work while newer authentication,
metadata, and named bind parameter features remain limited. This section describes support by
server/SDK version combination and upgrade order.

## Server and SDK Compatibility Matrix

| Server Version | 8.5 Client Driver | 8.7.0 Client Driver |
|-----------|:---------------------:|:---------------------:|
| **8.7.0 server** | Limited compatibility | Full compatibility |
| **8.5 server** | Full compatibility | Backward compatible; 8.7.0 named APIs unavailable |

- **Full compatibility**: Matching versions. Actual feature availability depends on edition, table
  type, SDK support, and use of a build containing the feature.
- **Limited compatibility**: Basic connections work, but new 8.7.0 features such as AUTH KEY extensions may be unavailable.
- **Backward compatible**: Only features within the 8.5 server's scope are available.

## Main Changes in the Machbase 8.7.0 SDKs

### AUTH KEY Authentication Extensions

8.7.0 extends AUTH KEY challenge authentication.

- Supported signature schemes: `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`
- Drivers at 8.5 or earlier may not support the new `RSA_PSS` signature scheme.
- Update drivers to 8.7.0 when using AUTH KEY authentication.

```text
-- Register an AUTH KEY on the server
ALTER USER app_user ADD AUTH KEY (
    KEY='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    VALID_BEFORE='2047-12-31'
);
```

### Connection String Compatibility

AUTH KEY parameters for Machbase SQLCLI and ODBC:

```ini
AUTH_MODE=CHALLENGE;
AUTH_KEY_FILE=./private_key.pem;
AUTH_SIG_SCHEME=ECDSA;
```

8.5 drivers may ignore `AUTH_SIG_SCHEME`.

### Nullable Metadata

For APIs that report whether result columns allow NULL and constraints by server/SDK combination,
see
[Nullable Metadata Support](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-nullable-metadata).
Record both server and client versions when checking compatibility.

### Named Bind Parameter

Whether named parameters are sent to a server-prepared statement, bound positionally,
or converted into SQL text on the client depends on the SDK.
Check the client's behavior in
[SDK Feature Support](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-transaction-prepare-bind).

### ARRAY and Selected-column Append

Fixed-length numeric ARRAYs and selected-column Append are supported in Machbase DBMS 8.7.0.
Use a DBMS 8.7.0 server with an SDK build containing ARRAY support. Older servers or SDKs without
this feature do not substitute legacy scalar types for ARRAY metadata or values; they reject
such requests with an error.

SQL ARRAY element positions and Machbase-specific SDK positions are 0-based. Decrement positions
in legacy 1-based SQL, sparse objects, and indexed Append targets by one. Stored data and dense
ARRAY element order are unchanged. Positions defined as 1-based by standard APIs, such as JDBC
parameter ordinals or `java.sql.Array` slices, are unaffected.

In Cluster Edition, all Coordinators, Brokers, and Warehouses must use the same ARRAY-capable DBMS
8.7.0 build. Do not start ARRAY DDL or operations using ARRAY data while versions are mixed.


For SQL and SDK requirements, see
[Numeric ARRAY Types](/dbms/reference/sql/types/array/) and
[Sparse ARRAY and Selected-column Append APIs](/dbms/development-tools-integration/data-input-load-export/array-append/).


## Checking SDK Versions

JDBC:

```java
Connection conn = DriverManager.getConnection(url, props);
DatabaseMetaData meta = conn.getMetaData();
System.out.println("Driver: " + meta.getDriverVersion());
```

Machbase SQLCLI:

```c
SQLGetInfo(conn, SQL_DRIVER_VER, buf, sizeof(buf), NULL);
```

ODBC:

```c
SQLGetInfo(conn, SQL_DRIVER_VER, buf, sizeof(buf), NULL);
```

## Upgrade Recommendations

1. Upgrade the server and SDKs together to the same version (8.7.0).
2. During a phased SDK upgrade, remember that 8.5 SDK connections to 8.7.0 servers have limited compatibility.
3. When using AUTH KEY authentication, upgrade SDKs first.
4. If application logic depends on nullable metadata, upgrade both the server and SDKs
   to 8.7.0.
5. If using SDK APIs that bind parameters by name, upgrade both the server and SDKs
   to 8.7.0.
6. If using ARRAY or selected-column Append, upgrade the server to Machbase DBMS 8.7.0 and
   clients to SDK builds containing those features. In Cluster Edition, align
   all nodes.
