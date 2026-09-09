---
type: docs
title: '11.4 Machbase SQLCLI and ODBC'
weight: 40
toc: true
aliases:
  - /dbms/reference/sdk-api/cli-odbc/
---

<a id="machbase-sqlcli"></a>
<a id="odbc"></a>

Machbase SQLCLI is a Call-Level Interface for C/C++ applications. The ODBC driver serves
standard ODBC applications. Both interfaces share an execution flow based on environment,
connection, and statement handles. SQLCLI adds extension functions for high-speed Append.

## Choose an Interface

| Requirement | Interface |
|----------|------------|
| Develop C/C++ applications with the Machbase installation package | SQLCLI |
| Use generic ODBC tools or a driver manager | ODBC |
| Bulk ingestion through Append extensions | SQLCLI |
| Execute standard SQL and retrieve results | SQLCLI or ODBC |

## Headers and Libraries

Check the following files in the installation directory:

```bash
test -f "$MACHBASE_HOME/include/machbase_sqlcli.h"
test -f "$MACHBASE_HOME/lib/libmachbasecli_dll.so"
```

Example dynamic linking on Linux:

```bash
gcc cli_quickstart.c   -I"$MACHBASE_HOME/include"   -L"$MACHBASE_HOME/lib"   -lmachbasecli_dll   -o cli_quickstart

LD_LIBRARY_PATH="$MACHBASE_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"   MACHBASE_PASSWORD='your-password' ./cli_quickstart
```

Base production builds on the installation package's `install/machbase_env.mk` and
platform-specific linker settings.

## Connection Strings

The basic SQLCLI connection string uses these keys:

```text
SERVER=127.0.0.1;PORT_NO=5656;UID=APP_USER;PWD=secret;CONNTYPE=1
```

For an ODBC data source, specify the DSN, user, and password.

```text
DSN=MACHBASE;UID=APP_USER;PWD=secret
```

Drivers that support an initial database for multi-database operation accept `DATABASE`
or `DBNAME`. Check support in the deployed driver, then run `SELECT CURRENT_DATABASE()`
after connecting to verify the selection.

## Quick Start

This program connects to port 5656, queries a system table, and releases all handles.
The password is supplied through an environment variable.

```c
#include <stdio.h>
#include <stdlib.h>
#include <machbase_sqlcli.h>

int main(void)
{
    SQLHENV env = SQL_NULL_HENV;
    SQLHDBC dbc = SQL_NULL_HDBC;
    SQLHSTMT stmt = SQL_NULL_HSTMT;
    char conn[512];
    const char *password = getenv("MACHBASE_PASSWORD");

    if (password == NULL) {
        fputs("MACHBASE_PASSWORD is required\n", stderr);
        return 2;
    }

    snprintf(conn, sizeof(conn),
        "SERVER=127.0.0.1;PORT_NO=5656;"
        "UID=SYS;PWD=%s;CONNTYPE=1", password);

    if (SQLAllocEnv(&env) != SQL_SUCCESS) {
        return 3;
    }
    if (SQLAllocConnect(env, &dbc) != SQL_SUCCESS) {
        SQLFreeEnv(env);
        return 4;
    }
    if (SQLDriverConnect(
            dbc, NULL, (SQLCHAR *)conn, SQL_NTS,
            NULL, 0, NULL, SQL_DRIVER_NOPROMPT) != SQL_SUCCESS) {
        SQLFreeConnect(dbc);
        SQLFreeEnv(env);
        return 5;
    }
    if (SQLAllocStmt(dbc, &stmt) != SQL_SUCCESS) {
        SQLDisconnect(dbc);
        SQLFreeConnect(dbc);
        SQLFreeEnv(env);
        return 6;
    }
    if (SQLExecDirect(
            stmt, (SQLCHAR *)"SELECT COUNT(*) FROM V$TABLES",
            SQL_NTS) != SQL_SUCCESS) {
        SQLFreeStmt(stmt, SQL_DROP);
        SQLDisconnect(dbc);
        SQLFreeConnect(dbc);
        SQLFreeEnv(env);
        return 7;
    }

    puts("query succeeded");
    SQLFreeStmt(stmt, SQL_DROP);
    SQLDisconnect(dbc);
    SQLFreeConnect(dbc);
    SQLFreeEnv(env);
    return 0;
}
```

To report failures, read SQLSTATE, the native error code, and the message using
`SQLGetDiagRec()` or `SQLError()` in existing code.

## Standard Execution Flow

1. Allocate environment and connection handles.
2. Connect with `SQLDriverConnect()` or `SQLConnect()`.
3. Allocate a statement handle.
4. Execute SQL with `SQLPrepare()` and `SQLExecute()`, or `SQLExecDirect()`.
5. Read SELECT results with `SQLBindCol()` and `SQLFetch()`.
6. Release statement, connection, and environment resources in that order.

Bind input with `SQLBindParameter()` instead of concatenating strings. Check nullability
with the last argument of `SQLDescribeCol()` or with
`SQLColAttribute(..., SQL_DESC_NULLABLE, ...)`.

## Named Bind Parameter

If the server and driver support named parameters, use `:name` placeholders and
`SQLBindParameterByName()`. A repeated name binds one value to all matching positions. See
[Named Bind Parameter](/dbms/reference/sql/syntax/named-bind-parameter-syntax/) for common
constraints and examples.

When support is unverified, use standard `?` placeholders and `SQLBindParameter()`.

## ROWID from INSERT

To obtain the generated ROWID after a successful single `INSERT ... VALUES` in Standard
Edition, use the following:

- SQLCLI extension: `SQLGetGeneratedRowID()`
- Standard ODBC: no standard API dedicated to generated ROWID

Do not assume the same return behavior for batches, Append, `INSERT ... SELECT`, or UPSERT.
See [ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/) for the exact scope.

## Append Extensions

High-speed ingestion uses an Append flow separate from ordinary statements.

| Step | Main functions |
|------|-----------|
| Open | `SQLAppendOpen()`; `SQLAppendOpenColumns()`/`W()` for selected columns |
| Send a row | `SQLAppendDataV2()` or an Append function supported by the version |
| Send a batch | `SQLAppendBatch()` |
| Flush to the server | `SQLAppendFlush()` |
| Error callback | `SQLAppendSetErrorCallback()` |
| Close | `SQLAppendClose()` |

Append column order and types must match the target schema exactly. Represent strings,
binary data, IP addresses, DATETIME, and NULL according to `SQL_APPEND_PARAM` in the
installed `machbase_sqlcli.h`. Record failed rows and server errors in the callback,
without logging passwords or raw sensitive data.

Do not share a connection with an active Append handle with ordinary queries. Check
success and failure counts returned by close.

## Threads and Resource Management

- Use separate connections and statements per thread.
- Do not use a statement or Append handle concurrently from multiple threads.
- Provide cleanup routines that release handles in reverse order on every error path.
- Before retrying, ensure the previous connection and Append state are fully closed.
- Record both success and failure counts for bulk ingestion.

## Check API Details

The installed `$MACHBASE_HOME/include/machbase_sqlcli.h` is the reference for function
prototypes, constants, and structures matching the library. Do not mix examples with
headers from another version. Include compilation, linking, and a port 5656 connection
test in the deployment pipeline.

## DECIMAL Append

For `DECIMAL` or `NUMERIC` input through `SQLAppendDataV2()` and `SQLAppendBatch()`, use
the 32-byte opaque `SQL_APPEND_NUMERIC` type and its public constructors. Do not create
or modify its internal bytes in application code.

| Input | Function |
|---|---|
| UTF-8 numeric string | `SQLAppendNumericFromString()` |
| Signed/unsigned integer | `SQLAppendNumericFromInt64()`, `SQLAppendNumericFromUInt64()` |
| `SQL_NUMERIC_STRUCT` | `SQLAppendNumericFromSQLNumeric()` |
| NULL | `SQLAppendNumericSetNull()` |

Prefer strings or `SQL_NUMERIC_STRUCT` to preserve exact values. Specify
`SQL_APPEND_TYPE_NUMERIC` or `SQL_APPEND_TYPE_DECIMAL` in the type array. Check overflow
and rounding against the target column precision and scale.

## ARRAY and Selected-Column Append

Machbase DBMS 8.7.0 supports typed ARRAY retrieval and binding with
`SQL_MACHBASE_ARRAY_DESC`, and sparse input with `SQL_MACHBASE_SPARSE_ARRAY_DESC`.
Standard Open can also pass a sparse descriptor to an ARRAY column.

```c
SQLAppendOpen(statement, (SQLCHAR *)"ARRAY_APPEND_FULL_EXAMPLE", 0);
row[0].mLong = 1;
row[1].mVar.mData = &sparse;
row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
SQLAppendDataV3(statement, row, 2);
SQLAppendClose(statement, &success, &failure);
```

This code follows the input order of a table with `ID LONG, A INT32[4]`. Start with the
[complete standard Open example](../data-input-load-export/array-append/#c-full-open),
including connection, descriptor and buffer setup, and error handling. This differs
from passing descriptors to the legacy `SQLAppendData(void *[])` API.

To select specific columns or fixed ARRAY elements, use `SQLAppendOpenColumns()` or
`SQLAppendOpenColumnsW()`.

```c
SQLCHAR *targets[] = {
    (SQLCHAR *)"ID",
    (SQLCHAR *)"CHANNELS[0]",
    (SQLCHAR *)"CHANNELS[3]",
    NULL
};

SQLAppendOpenColumns(statement, (SQLCHAR *)"SENSOR_ARRAY", targets, 0);
```

ARRAY element targets and sparse descriptor positions are 0-based. The column-name
list must end with `NULL`. `SQLAppendBatch()` does not support ARRAY. See
[Sparse ARRAY and Selected-Column Append API](../data-input-load-export/array-append/)
for descriptor definitions, whole-array and element NULL handling, and direct ODBC
handle restrictions.
