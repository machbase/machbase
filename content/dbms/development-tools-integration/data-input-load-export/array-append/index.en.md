---
type: docs
title: '11.10.1 Sparse ARRAY and Selected-Column Append API'
weight: 10
toc: true
---

Machbase DBMS 8.7.0 supports populating selected positions in a fixed-length `ARRAY`. Use
a sparse ARRAY when positions vary by row. When multiple Append rows populate the same
positions, specify selected columns during Append Open.

A sparse ARRAY represents **a value for one column**. Column selection specifies **which
columns or elements a row supplies**. A full-row append using standard Open can also pass
a sparse object to an ARRAY column. Node.js requires column definitions in `appendOpen()`,
so list all columns to perform the equivalent full-row operation.

For `ARRAY` declarations, ordinary input, queries, and SDK-specific dense ARRAY handling,
see [Numeric ARRAY Types](/dbms/reference/sql/types/array/).

## Choose an Input Method

| Requirement | Recommended method |
|---|---|
| Specify only populated positions in one SQL row | `ARRAY_SPARSE(position => value, ...)` |
| Populate the same positions in multiple Append rows | `A[0]`, `A[3]` targets in Append Open |
| Append full rows with standard Open and varying ARRAY positions | Pass an SDK sparse object as the ARRAY value in each full row |
| Populate selected columns with varying ARRAY positions | A whole `A` target in the selection list and an SDK sparse object |
| A non-NULL ARRAY with all NULL elements | Empty sparse object |
| A NULL ARRAY | SQL `NULL` or the SDK whole-NULL value |

Positions are 0-based in SQL and all Machbase-specific SDK APIs.

## SQL Sparse Input

### ARRAY_SPARSE

In INSERT or UPDATE contexts with a target column, specify only positions and values.

```sql
CREATE LOG TABLE ARRAY_APPEND_EXAMPLE
(
    ID LONG,
    A  INT32[4]
);

INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A)
VALUES (1, ARRAY_SPARSE(0 => 10, 3 => 40));
```

Where the target type cannot be inferred, such as SELECT, specify the element type and
element count first.

```sql
SELECT ARRAY_SPARSE(INT32[4], 0 => 10, 3 => 40);
SELECT ARRAY_SPARSE(DECIMAL(12,4)[4], 1 => 1.2500);
```

- Positions must be integer literals in `0..cardinality-1`.
- Pairs can appear in any order, but positions must be unique.
- Omitted positions and `position => NULL` produce NULL elements.
- `ARRAY_SPARSE()` or `ARRAY_SPARSE(INT32[4])` produces an ARRAY with all NULL elements.
- Use SQL `NULL`, not `ARRAY_SPARSE()`, for a NULL array.
- An invalid position or element conversion fails the entire statement.

### Direct sparse shorthand

Position/value pairs can appear directly inside brackets without the `ARRAY_SPARSE` wrapper.

```sql
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A)
VALUES (2, [0 => 10, 3 => 40]);

SELECT [1 => 12, 33 => 23];
```

With a target ARRAY, its type and element count apply. Standalone expressions infer the
common numeric type as dense ARRAYs do and set the element count to `largest position + 1`.
The second example therefore has type `INT32[34]`.

A standalone all-NULL sparse expression fails because the element type is unknown. Use
`ARRAY_SPARSE(TYPE[N], ...)` in this case. `[]` remains the existing dense empty constructor;
`ARRAY[0 => 1]` is not supported.

### Specify Positions in INSERT Targets

When multiple rows populate the same positions, specify element targets in the column list.

```sql
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A[0], A[3])
VALUES (2, 10, 40);

-- A exists, but all elements are NULL.
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A[0], A[3])
VALUES (3, NULL, NULL);

-- A itself is NULL.
INSERT INTO ARRAY_APPEND_EXAMPLE (ID)
VALUES (4);
```

A statement cannot target both `A` and `A[0]`, or target the same element twice. Targeting
an element of a scalar column or an out-of-range position raises an error.

Element-position targets are supported in `INSERT ... VALUES` and Append selection lists.
They are not supported in `INSERT ... SELECT` or `UPDATE ... SET A[0] = ...`.

## Common Append Rules

### Full-Row and Selected Input

Standard Open uses the table input column order. Selected Open uses the specified target
list order. The standard Open examples below pass two values, `ID` then `A`, without an
extra `_arrival_time`. Each API in these examples handles the automatic LOG timestamp.
Use the SDK timestamp API to provide an explicit arrival time.

Node.js does not have separate standard and selected Open methods. Full-row input also
requires column definitions with `name` and `type`; these examples list `ID` and `A` in
table order. Calling only `appendOpen(table)` or passing an empty column list is unsupported.

### Prepare and Rerun the Examples

The standard and selected examples use separate tables so they can run independently.
Before each example, run the following setup SQL in the database you will connect to.

```sql
CREATE LOG TABLE ARRAY_APPEND_FULL_EXAMPLE (ID LONG, A INT32[4]);
```

Standard example filenames include `full`. Selected examples use `ARRAY_APPEND_EXAMPLE`
created above. The selected C example recreates this table itself; ensure the name is
reserved for this exercise. Before running selected examples for other SDKs, prepare an
empty `ARRAY_APPEND_EXAMPLE` with the same schema.

Run each SDK example **independently**. Running multiple SDKs consecutively against one
table creates duplicate IDs. To rerun, inspect the results, perform [Cleanup](#sparse-append-cleanup),
and recreate the relevant table. Adjust the server address, port, and credentials to your environment.

### Common Results

Both methods create the following four rows. The standard example uses a sparse object
for ID=1; the selected example uses fixed element targets for ID=1.

```text
ID=1  A=[10,null,null,40]       Sparse object or fixed element targets
ID=2  A=[null,200,null,400]     Sparse object in the ARRAY column
ID=3  A=[null,null,null,null]   Empty sparse object
ID=4  A=NULL                    whole NULL
```

ARRAY elements omitted from a sparse object become NULL. `entry_count == 0` or an empty
sparse object produces an array of the declared length with all NULL elements, not a
zero-length array. Whole NULL means the array value itself is absent; `ARRAY_LENGTH` is also NULL.

### Selected Open Rules

These rules apply to **the target list of a selected Open**. Omitting column arguments
from standard Open is not an empty selection list.

Ordinary columns omitted from the selection list follow existing Append rules:

- Nullable columns use NULL.
- Columns with DEFAULT use their default value.
- If a required-value column is missing, Append Open or row input fails.

The target list must be nonempty and unique, ignoring case. It cannot include both a
whole ARRAY and an element of that ARRAY. After Append Open, each row must supply exactly
the number and order of values in the target list.

Close an open Append handle even when row input fails. If Append Open itself fails, the
SDK cleans up internal state and the connection can be reused.

## C SQLCLI

Use the following public types for ARRAY input and retrieval:

| Type or constant | Purpose |
|---|---|
| `SQL_MACHBASE_ARRAY` | Identifies the SQL ARRAY type |
| `SQL_C_MACHBASE_ARRAY` | Dense ARRAY retrieval and binding descriptor |
| `SQL_C_MACHBASE_SPARSE_ARRAY` | Prepared sparse ARRAY input |
| `SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH` | Identifies an Append sparse descriptor |

<a id="c-full-open"></a>

### Append a Sparse ARRAY with Standard Open

Open with `SQLAppendOpen()` and pass `ID` and `A` in a `SQL_APPEND_PARAM` array. For `A`,
set `mVar.mData` to the address of `SQL_MACHBASE_SPARSE_ARRAY_DESC` and `mVar.mLength` to
`SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH`. No columns are selected. Use
`SQLAppendDataV3(..., row, 2)` to specify the value count. This example does not pass the
descriptor directly to the legacy `SQLAppendData(void *[])` API.

Use the empty `ARRAY_APPEND_FULL_EXAMPLE` created by the setup SQL. The descriptor and
position, value, and indicator buffers must remain valid until the Append call returns.
The same open handle sends different positions in the first two rows, then an empty sparse
array and a whole NULL.

```c
/* sparse_append_full.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>

static int ok(SQLRETURN rc)
{
    return rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO;
}

static void fail(SQLHENV env, SQLHDBC dbc, SQLHSTMT stmt, const char *where)
{
    SQLCHAR state[6] = {0};
    SQLCHAR message[1024] = {0};
    SQLINTEGER native = 0;
    SQLSMALLINT length = 0;
    SQLError(env, dbc, stmt, state, &native, message,
             (SQLSMALLINT)sizeof(message), &length);
    fprintf(stderr, "%s: %s %d %s\n", where, state, (int)native, message);
    exit(EXIT_FAILURE);
}

int main(void)
{
    SQLHENV env = SQL_NULL_HENV;
    SQLHDBC dbc = SQL_NULL_HDBC;
    SQLHSTMT sql = SQL_NULL_HSTMT;
    SQLHSTMT append = SQL_NULL_HSTMT;
    SQLCHAR conn[] =
        "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;CONNTYPE=1";
    SQL_APPEND_PARAM row[2];
    SQLUSMALLINT positions[2] = {0, 3};
    SQLINTEGER values[2] = {10, 40};
    SQLLEN indicators[2] = {0, 0};
    SQL_MACHBASE_SPARSE_ARRAY_DESC sparse;
    SQLBIGINT success = 0;
    SQLBIGINT failure = 0;
    SQLINTEGER id;
    SQLLEN idInd;
    SQLLEN textInd;
    SQLCHAR text[128];

    if (!ok(SQLAllocEnv(&env)) || !ok(SQLAllocConnect(env, &dbc)) ||
        !ok(SQLDriverConnect(dbc, NULL, conn, SQL_NTS, NULL, 0, NULL,
                             SQL_DRIVER_NOPROMPT)) ||
        !ok(SQLAllocStmt(dbc, &sql)) || !ok(SQLAllocStmt(dbc, &append)))
        fail(env, dbc, SQL_NULL_HSTMT, "connect");

    memset(&sparse, 0, sizeof(sparse));
    sparse.struct_size = sizeof(sparse);
    sparse.element_c_type = SQL_C_SLONG;
    sparse.cardinality = 4;
    sparse.entry_count = 2;
    sparse.positions = positions;
    sparse.values = values;
    sparse.value_stride = sizeof(values[0]);
    sparse.element_indicators = indicators;

    memset(row, 0, sizeof(row));
    if (!ok(SQLAppendOpen(append,
            (SQLCHAR*)"ARRAY_APPEND_FULL_EXAMPLE", 0)))
        fail(env, dbc, append, "sparse open");

    row[0].mLong = 1;
    row[1].mVar.mData = &sparse;
    row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "first sparse row");
    }

    positions[0] = 1;
    values[0] = 200;
    values[1] = 400;
    row[0].mLong = 2;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "sparse row");
    }

    row[0].mLong = 3;
    sparse.entry_count = 0;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "empty sparse row");
    }

    row[0].mLong = 4;
    row[1].mVar.mData = NULL;
    row[1].mVar.mLength = 0;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "whole NULL row");
    }
    success = 0;
    failure = 0;
    if (!ok(SQLAppendClose(append, &success, &failure)) ||
        success != 4 || failure != 0)
        fail(env, dbc, append, "sparse close");

    if (!ok(SQLExecDirect(sql,
        (SQLCHAR*)"SELECT ID,A FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID", SQL_NTS)))
        fail(env, dbc, sql, "select");
    if (!ok(SQLBindCol(sql, 1, SQL_C_SLONG, &id, sizeof(id), &idInd)) ||
        !ok(SQLBindCol(sql, 2, SQL_C_CHAR, text, sizeof(text), &textInd)))
        fail(env, dbc, sql, "bind verify");
    for (;;) {
        SQLRETURN fetch = SQLFetch(sql);
        if (fetch == SQL_NO_DATA)
            break;
        if (!ok(fetch))
            fail(env, dbc, sql, "fetch verify");
        printf("%d %s\n", (int)id,
               textInd == SQL_NULL_DATA ? "NULL" : (char*)text);
    }

    SQLFreeStmt(append, SQL_DROP);
    SQLFreeStmt(sql, SQL_DROP);
    SQLDisconnect(dbc);
    SQLFreeConnect(dbc);
    SQLFreeEnv(env);
    return EXIT_SUCCESS;
}
```

```bash
cc -I"$MACHBASE_HOME/include" sparse_append_full.c \
  -L"$MACHBASE_HOME/lib" -lmachbasecli -lm -ldl -lrt -pthread \
  -o sparse_append_full
LD_LIBRARY_PATH="$MACHBASE_HOME/lib" ./sparse_append_full
```

The program checks Close for 4 successes and 0 failures, then prints the retrieved IDs
and arrays. Compare them with [Verify Results](#결과-확인). On an input error, it closes
Append before exiting. Check which rows were actually stored before retrying.

<a id="c-selected-open"></a>

### Append with Selected-Column Open

`SQLAppendOpenColumns()` and its wide-character variant accept an array of column-name
pointers terminated by `NULL`. There is no separate column-count argument.

```c
SQLRETURN SQL_API SQLAppendOpenColumns(
    SQLHSTMT     aStmtHandle,
    SQLCHAR     *aTableName,
    SQLCHAR    **aColumnNames,
    SQLINTEGER   aErrorCheckCount);

SQLRETURN SQL_API SQLAppendOpenColumnsW(
    SQLHSTMT     aStmtHandle,
    SQLWCHAR    *aTableName,
    SQLWCHAR   **aColumnNames,
    SQLINTEGER   aErrorCheckCount);
```

`aColumnNames == NULL` or a `NULL` first element raises an error. C pointers do not carry
array lengths, so the caller must provide a valid array through the final `NULL`. Omitting
the terminator can cause an out-of-bounds read; do not assume it can be diagnosed safely.

The following `sparse_append.c` creates the table, appends four rows, and prints the results.

```c
/* sparse_append.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>

static int ok(SQLRETURN rc)
{
    return rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO;
}

static void fail(SQLHENV env, SQLHDBC dbc, SQLHSTMT stmt, const char *where)
{
    SQLCHAR state[6] = {0};
    SQLCHAR message[1024] = {0};
    SQLINTEGER native = 0;
    SQLSMALLINT length = 0;
    SQLError(env, dbc, stmt, state, &native, message,
             (SQLSMALLINT)sizeof(message), &length);
    fprintf(stderr, "%s: %s %d %s\n", where, state, (int)native, message);
    exit(EXIT_FAILURE);
}

int main(void)
{
    SQLHENV env = SQL_NULL_HENV;
    SQLHDBC dbc = SQL_NULL_HDBC;
    SQLHSTMT sql = SQL_NULL_HSTMT;
    SQLHSTMT append = SQL_NULL_HSTMT;
    SQLCHAR conn[] =
        "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;CONNTYPE=1";
    SQLCHAR *fixed[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A[0]",
                        (SQLCHAR*)"A[3]", NULL};
    SQLCHAR *whole[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A", NULL};
    SQL_APPEND_PARAM row[3];
    SQLUSMALLINT positions[2] = {1, 3};
    SQLINTEGER values[2] = {200, 400};
    SQLLEN indicators[2] = {0, 0};
    SQL_MACHBASE_SPARSE_ARRAY_DESC sparse;
    SQLBIGINT success = 0;
    SQLBIGINT failure = 0;
    SQLINTEGER id;
    SQLLEN idInd;
    SQLLEN textInd;
    SQLCHAR text[128];

    if (!ok(SQLAllocEnv(&env)) || !ok(SQLAllocConnect(env, &dbc)) ||
        !ok(SQLDriverConnect(dbc, NULL, conn, SQL_NTS, NULL, 0, NULL,
                             SQL_DRIVER_NOPROMPT)) ||
        !ok(SQLAllocStmt(dbc, &sql)) || !ok(SQLAllocStmt(dbc, &append)))
        fail(env, dbc, SQL_NULL_HSTMT, "connect");

    SQLExecDirect(sql, (SQLCHAR*)"DROP TABLE ARRAY_APPEND_EXAMPLE", SQL_NTS);
    if (!ok(SQLExecDirect(sql,
        (SQLCHAR*)"CREATE LOG TABLE ARRAY_APPEND_EXAMPLE(ID LONG,A INT32[4])",
        SQL_NTS)))
        fail(env, dbc, sql, "create");

    memset(row, 0, sizeof(row));
    row[0].mLong = 1;
    row[1].mInteger = 10;
    row[2].mInteger = 40;
    if (!ok(SQLAppendOpenColumns(append,
            (SQLCHAR*)"ARRAY_APPEND_EXAMPLE", fixed, 0)))
        fail(env, dbc, append, "fixed open");
    if (!ok(SQLAppendDataV3(append, row, 3))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "fixed row");
    }
    if (!ok(SQLAppendClose(append, &success, &failure)) ||
        success != 1 || failure != 0)
        fail(env, dbc, append, "fixed close");

    memset(&sparse, 0, sizeof(sparse));
    sparse.struct_size = sizeof(sparse);
    sparse.element_c_type = SQL_C_SLONG;
    sparse.cardinality = 4;
    sparse.entry_count = 2;
    sparse.positions = positions;
    sparse.values = values;
    sparse.value_stride = sizeof(values[0]);
    sparse.element_indicators = indicators;

    memset(row, 0, sizeof(row));
    if (!ok(SQLAppendOpenColumns(append,
            (SQLCHAR*)"ARRAY_APPEND_EXAMPLE", whole, 0)))
        fail(env, dbc, append, "sparse open");

    row[0].mLong = 2;
    row[1].mVar.mData = &sparse;
    row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "sparse row");
    }

    row[0].mLong = 3;
    sparse.entry_count = 0;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "empty sparse row");
    }

    row[0].mLong = 4;
    row[1].mVar.mData = NULL;
    row[1].mVar.mLength = 0;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "whole NULL row");
    }
    success = 0;
    failure = 0;
    if (!ok(SQLAppendClose(append, &success, &failure)) ||
        success != 3 || failure != 0)
        fail(env, dbc, append, "sparse close");

    if (!ok(SQLExecDirect(sql,
        (SQLCHAR*)"SELECT ID,A FROM ARRAY_APPEND_EXAMPLE ORDER BY ID", SQL_NTS)))
        fail(env, dbc, sql, "select");
    if (!ok(SQLBindCol(sql, 1, SQL_C_SLONG, &id, sizeof(id), &idInd)) ||
        !ok(SQLBindCol(sql, 2, SQL_C_CHAR, text, sizeof(text), &textInd)))
        fail(env, dbc, sql, "bind verify");
    for (;;) {
        SQLRETURN fetch = SQLFetch(sql);
        if (fetch == SQL_NO_DATA)
            break;
        if (!ok(fetch))
            fail(env, dbc, sql, "fetch verify");
        printf("%d %s\n", (int)id,
               textInd == SQL_NULL_DATA ? "NULL" : (char*)text);
    }

    SQLFreeStmt(append, SQL_DROP);
    SQLFreeStmt(sql, SQL_DROP);
    SQLDisconnect(dbc);
    SQLFreeConnect(dbc);
    SQLFreeEnv(env);
    return EXIT_SUCCESS;
}
```

Build and run as follows:

```bash
cc -I"$MACHBASE_HOME/include" sparse_append.c \
  -L"$MACHBASE_HOME/lib" -lmachbasecli -lm -ldl -lrt -pthread \
  -o sparse_append
LD_LIBRARY_PATH="$MACHBASE_HOME/lib" ./sparse_append
```

Descriptor positions are 0-based. They need not be sorted, but must be unique. An entry
indicator of `SQL_NULL_DATA` makes that element NULL. `entry_count == 0` represents an empty
sparse ARRAY. For a whole NULL, set `mVar.mData = NULL` and `mVar.mLength = 0`.

## C++ SQLCLI

<a id="cpp-full-open"></a>

### Append a Sparse ARRAY with Standard Open

Use the same descriptors and `SQLAppendOpen()` as C. Keep position/value buffers in
`std::array` and close Append on both success and exception paths. Prepare the standard
example table first.

```cpp
/* sparse_append_full.cpp */
#include <array>
#include <iostream>
#include <stdexcept>
#include <machbase_sqlcli.h>

static bool ok(SQLRETURN rc) {
    return rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO;
}

struct Handles {
    SQLHENV env{SQL_NULL_HENV};
    SQLHDBC dbc{SQL_NULL_HDBC};
    SQLHSTMT stmt{SQL_NULL_HSTMT};
    ~Handles() {
        if (stmt != SQL_NULL_HSTMT) SQLFreeStmt(stmt, SQL_DROP);
        if (dbc != SQL_NULL_HDBC) { SQLDisconnect(dbc); SQLFreeConnect(dbc); }
        if (env != SQL_NULL_HENV) SQLFreeEnv(env);
    }
};

int main() {
    Handles h;
    SQLCHAR conn[] =
        "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;CONNTYPE=1";
    if (!ok(SQLAllocEnv(&h.env)) || !ok(SQLAllocConnect(h.env, &h.dbc)) ||
        !ok(SQLDriverConnect(h.dbc, nullptr, conn, SQL_NTS, nullptr, 0,
                             nullptr, SQL_DRIVER_NOPROMPT)) ||
        !ok(SQLAllocStmt(h.dbc, &h.stmt)))
        throw std::runtime_error("connect");

    std::array<SQLUSMALLINT, 2> positions{0, 3};
    std::array<SQLINTEGER, 2> values{10, 40};
    std::array<SQLLEN, 2> indicators{0, 0};
    SQL_MACHBASE_SPARSE_ARRAY_DESC sparse{};
    sparse.struct_size = sizeof(sparse);
    sparse.element_c_type = SQL_C_SLONG;
    sparse.cardinality = 4;
    sparse.entry_count = 2;
    sparse.positions = positions.data();
    sparse.values = values.data();
    sparse.value_stride = sizeof(values[0]);
    sparse.element_indicators = indicators.data();
    std::array<SQL_APPEND_PARAM, 2> row{};
    row[1].mVar.mData = &sparse;
    row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;

    SQLBIGINT success = 0, failure = 0;
    if (!ok(SQLAppendOpen(h.stmt, (SQLCHAR*)"ARRAY_APPEND_FULL_EXAMPLE", 0)))
        throw std::runtime_error("SQLAppendOpen");
    try {
        for (int id = 1; id <= 4; ++id) {
            row[0].mLong = id;
            if (id == 2) {
                positions[0] = 1;
                values[0] = 200;
                values[1] = 400;
            } else if (id == 3) {
                sparse.entry_count = 0;
            } else if (id == 4) {
                row[1].mVar.mData = nullptr;
                row[1].mVar.mLength = 0;
            }
            if (!ok(SQLAppendDataV3(h.stmt, row.data(), 2)))
                throw std::runtime_error("SQLAppendDataV3");
        }
    } catch (...) {
        SQLAppendClose(h.stmt, &success, &failure);
        throw;
    }
    if (!ok(SQLAppendClose(h.stmt, &success, &failure)) ||
        success != 4 || failure != 0)
        throw std::runtime_error("SQLAppendClose");

    if (!ok(SQLExecDirect(h.stmt,
        (SQLCHAR*)"SELECT ID,A FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID", SQL_NTS)))
        throw std::runtime_error("verify query");
    SQLINTEGER id{}; SQLLEN idInd{}, arrayInd{}; SQLCHAR value[128]{};
    if (!ok(SQLBindCol(h.stmt, 1, SQL_C_SLONG,
                       &id, sizeof(id), &idInd)) ||
        !ok(SQLBindCol(h.stmt, 2, SQL_C_CHAR,
                       value, sizeof(value), &arrayInd)))
        throw std::runtime_error("bind verify");
    for (;;) {
        SQLRETURN fetch = SQLFetch(h.stmt);
        if (fetch == SQL_NO_DATA) break;
        if (!ok(fetch)) throw std::runtime_error("fetch verify");
        std::cout << id << ' ' <<
            (arrayInd == SQL_NULL_DATA ? "NULL" : (char*)value) << '\n';
    }
}
```

```bash
c++ -std=c++11 -I"$MACHBASE_HOME/include" sparse_append_full.cpp \
  -L"$MACHBASE_HOME/lib" -lmachbasecli -lm -ldl -lrt -pthread \
  -o sparse_append_full_cpp
LD_LIBRARY_PATH="$MACHBASE_HOME/lib" ./sparse_append_full_cpp
```

### Append with Selected-Column Open

Use SQLCLI descriptors without creating a C++-specific transport object. This example
uses an RAII wrapper to ensure close and sends descriptors while the C++ containers remain alive.

```cpp
/* sparse_append.cpp */
#include <array>
#include <iostream>
#include <stdexcept>
#include <machbase_sqlcli.h>

static bool ok(SQLRETURN rc) {
    return rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO;
}

struct Handles {
    SQLHENV env{SQL_NULL_HENV};
    SQLHDBC dbc{SQL_NULL_HDBC};
    SQLHSTMT stmt{SQL_NULL_HSTMT};
    ~Handles() {
        if (stmt != SQL_NULL_HSTMT) SQLFreeStmt(stmt, SQL_DROP);
        if (dbc != SQL_NULL_HDBC) { SQLDisconnect(dbc); SQLFreeConnect(dbc); }
        if (env != SQL_NULL_HENV) SQLFreeEnv(env);
    }
};

static void append(Handles& h, SQLCHAR **columns,
                   SQL_APPEND_PARAM *row, SQLINTEGER count) {
    SQLBIGINT success = 0, failure = 0;
    if (!ok(SQLAppendOpenColumns(h.stmt,
            (SQLCHAR*)"ARRAY_APPEND_EXAMPLE", columns, 0)))
        throw std::runtime_error("SQLAppendOpenColumns");
    try {
        if (!ok(SQLAppendDataV3(h.stmt, row, count)))
            throw std::runtime_error("SQLAppendDataV3");
    } catch (...) {
        SQLAppendClose(h.stmt, &success, &failure);
        throw;
    }
    if (!ok(SQLAppendClose(h.stmt, &success, &failure)) || failure != 0)
        throw std::runtime_error("SQLAppendClose");
}

int main() {
    Handles h;
    SQLCHAR conn[] =
        "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;CONNTYPE=1";
    if (!ok(SQLAllocEnv(&h.env)) || !ok(SQLAllocConnect(h.env, &h.dbc)) ||
        !ok(SQLDriverConnect(h.dbc, nullptr, conn, SQL_NTS, nullptr, 0,
                             nullptr, SQL_DRIVER_NOPROMPT)) ||
        !ok(SQLAllocStmt(h.dbc, &h.stmt)))
        throw std::runtime_error("connect");

    SQLCHAR *fixed[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A[0]",
                        (SQLCHAR*)"A[3]", nullptr};
    std::array<SQL_APPEND_PARAM, 3> row{};
    row[0].mLong = 1; row[1].mInteger = 10; row[2].mInteger = 40;
    append(h, fixed, row.data(), 3);

    std::array<SQLUSMALLINT, 2> pos{1, 3};
    std::array<SQLINTEGER, 2> val{200, 400};
    std::array<SQLLEN, 2> ind{0, 0};
    SQL_MACHBASE_SPARSE_ARRAY_DESC sparse{};
    sparse.struct_size = sizeof(sparse);
    sparse.element_c_type = SQL_C_SLONG;
    sparse.cardinality = 4;
    sparse.entry_count = 2;
    sparse.positions = pos.data();
    sparse.values = val.data();
    sparse.value_stride = sizeof(val[0]);
    sparse.element_indicators = ind.data();

    SQLCHAR *whole[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A", nullptr};
    std::array<SQL_APPEND_PARAM, 2> sparseRow{};
    sparseRow[0].mLong = 2;
    sparseRow[1].mVar.mData = &sparse;
    sparseRow[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
    append(h, whole, sparseRow.data(), 2);

    sparse.entry_count = 0;
    sparseRow[0].mLong = 3;
    append(h, whole, sparseRow.data(), 2);

    sparseRow[0].mLong = 4;
    sparseRow[1].mVar.mData = nullptr;
    sparseRow[1].mVar.mLength = 0;
    append(h, whole, sparseRow.data(), 2);

    if (!ok(SQLExecDirect(h.stmt,
        (SQLCHAR*)"SELECT ID,A FROM ARRAY_APPEND_EXAMPLE ORDER BY ID", SQL_NTS)))
        throw std::runtime_error("verify query");
    SQLINTEGER id{}; SQLLEN idInd{}, arrayInd{}; SQLCHAR value[128]{};
    if (!ok(SQLBindCol(h.stmt, 1, SQL_C_SLONG,
                       &id, sizeof(id), &idInd)) ||
        !ok(SQLBindCol(h.stmt, 2, SQL_C_CHAR,
                       value, sizeof(value), &arrayInd)))
        throw std::runtime_error("bind verify");
    for (;;) {
        SQLRETURN fetch = SQLFetch(h.stmt);
        if (fetch == SQL_NO_DATA) break;
        if (!ok(fetch)) throw std::runtime_error("fetch verify");
        std::cout << id << ' ' <<
            (arrayInd == SQL_NULL_DATA ? "NULL" : (char*)value) << '\n';
    }
}
```

```bash
c++ -std=c++11 -I"$MACHBASE_HOME/include" sparse_append.cpp \
  -L"$MACHBASE_HOME/lib" -lmachbasecli -lm -ldl -lrt -pthread \
  -o sparse_append_cpp
```

## Machbase ODBC extension

<a id="odbc-full-open"></a>

### Append a Sparse ARRAY with Standard Open

A C program linked directly to the Machbase driver can use `sparse_append_full.c` from
the [standard C Open example](#c-full-open) unchanged. It sends sparse descriptors with
`SQLAppendDataV3()` after `SQLAppendOpen()` and does not call `OpenColumns`. Build with
matching versions of the headers and ODBC extension library.

```bash
cc -I"$MACHBASE_HOME/include" sparse_append_full.c \
  -L"$MACHBASE_HOME/lib" -lmachbasecli_dll -lm -ldl -lrt -pthread \
  -o sparse_append_full_odbc
LD_LIBRARY_PATH="$MACHBASE_HOME/lib" ./sparse_append_full_odbc
```

Prepare the standard example table before running. These handles are created directly
by the Machbase driver; do not mix them with generic ODBC Driver Manager handles.

### Append with Selected-Column Open

ODBC C applications linked directly to the Machbase driver library and using
`machbase_sqlcli.h` can use the same extension functions. This example inserts four rows
through the direct Machbase driver API. Create the table first using the preceding DDL.

```c
/* sparse_odbc.c */
#include <stdio.h>
#include <string.h>
#include <machbase_sqlcli.h>

static int ok(SQLRETURN rc) {
    return rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO;
}

int main(void) {
    SQLHENV env = SQL_NULL_HENV;
    SQLHDBC dbc = SQL_NULL_HDBC;
    SQLHSTMT stmt = SQL_NULL_HSTMT;
    SQLBIGINT success = 0, failure = 0;
    SQLCHAR connection[] =
        "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;CONNTYPE=1";

    if (!ok(SQLAllocEnv(&env)) ||
        !ok(SQLAllocConnect(env, &dbc)) ||
        !ok(SQLDriverConnect(dbc, NULL, connection, SQL_NTS,
                             NULL, 0, NULL, SQL_DRIVER_NOPROMPT)) ||
        !ok(SQLAllocStmt(dbc, &stmt)))
        return 1;

    SQLCHAR *fixed[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A[0]",
                        (SQLCHAR*)"A[3]", NULL};
    SQL_APPEND_PARAM row[3] = {0};
    row[0].mLong = 1; row[1].mInteger = 10; row[2].mInteger = 40;
    if (!ok(SQLAppendOpenColumns(stmt,
            (SQLCHAR*)"ARRAY_APPEND_EXAMPLE", fixed, 0))) return 2;
    if (!ok(SQLAppendDataV3(stmt, row, 3))) {
        SQLAppendClose(stmt, &success, &failure);
        return 2;
    }
    if (!ok(SQLAppendClose(stmt, &success, &failure)) ||
        success != 1 || failure != 0) return 2;

    SQLUSMALLINT positions[2] = {1, 3};
    SQLINTEGER values[2] = {200, 400};
    SQLLEN indicators[2] = {0, 0};
    SQL_MACHBASE_SPARSE_ARRAY_DESC sparse = {0};
    sparse.struct_size = sizeof(sparse);
    sparse.element_c_type = SQL_C_SLONG;
    sparse.cardinality = 4;
    sparse.entry_count = 2;
    sparse.positions = positions;
    sparse.values = values;
    sparse.value_stride = sizeof(values[0]);
    sparse.element_indicators = indicators;
    SQLCHAR *whole[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A", NULL};
    memset(row, 0, sizeof(row));
    row[0].mLong = 2;
    row[1].mVar.mData = &sparse;
    row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
    if (!ok(SQLAppendOpenColumns(stmt,
            (SQLCHAR*)"ARRAY_APPEND_EXAMPLE", whole, 0))) return 3;
    if (!ok(SQLAppendDataV3(stmt, row, 2))) {
        SQLAppendClose(stmt, &success, &failure);
        return 3;
    }
    sparse.entry_count = 0;
    row[0].mLong = 3;
    if (!ok(SQLAppendDataV3(stmt, row, 2))) {
        SQLAppendClose(stmt, &success, &failure);
        return 3;
    }
    row[0].mLong = 4;
    row[1].mVar.mData = NULL;
    row[1].mVar.mLength = 0;
    if (!ok(SQLAppendDataV3(stmt, row, 2))) {
        SQLAppendClose(stmt, &success, &failure);
        return 3;
    }
    success = 0;
    failure = 0;
    if (!ok(SQLAppendClose(stmt, &success, &failure)) ||
        success != 3 || failure != 0) return 3;

    SQLFreeStmt(stmt, SQL_DROP);
    SQLDisconnect(dbc);
    SQLFreeConnect(dbc);
    SQLFreeEnv(env);
    puts("ODBC sparse append OK");
    return 0;
}
```

```bash
cc sparse_odbc.c -I/opt/machbase/include -L/opt/machbase/lib \
  -lmachbasecli_dll -lm -ldl -lrt -pthread -o sparse_odbc
LD_LIBRARY_PATH=/opt/machbase/lib ./sparse_odbc
```

{{< callout type="warning" >}}
Do not pass a statement handle created by a generic ODBC Driver Manager to a direct
SQLCLI extension: their handle ABIs differ. Selected-column Append requires the Machbase
driver extension and direct driver handles. Generic ODBC APIs do not provide Append Open
selection targets.
{{< /callout >}}

## JDBC

<a id="jdbc-full-open"></a>

### Append a Sparse ARRAY with Standard Open

Use the `executeAppendOpen(table, errorCheckCount)` overload. Pass `ID` and
`MachSparseArray` according to the returned metadata, without manually adding the standard
example table's automatic timestamp. `null` means whole NULL; an empty `MachSparseArray`
means an array with all NULL elements.

Save as `SparseAppendFull.java` and run with a JDBC JAR that includes ARRAY support.

```java
import com.machbase.jdbc.MachConnection;
import com.machbase.jdbc.MachSparseArray;
import com.machbase.jdbc.MachStatement;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class SparseAppendFull {
    public static void main(String[] args) throws Exception {
        try (MachConnection con = (MachConnection)DriverManager.getConnection(
                 "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER");
             MachStatement st = (MachStatement)con.createStatement()) {
            Map<Integer, Object> entries = new HashMap<Integer, Object>();
            entries.put(0, 10);
            entries.put(3, 40);
            MachSparseArray sparse = con.createSparseArrayOf("INT32", 4, entries);

            try (ResultSet opened = st.executeAppendOpen("ARRAY_APPEND_FULL_EXAMPLE", 0)) {
                try {
                    ResultSetMetaData meta = opened.getMetaData();
                    for (int id = 1; id <= 4; id++) {
                        if (id == 2) sparse.clear().set(1, 200).set(3, 400);
                        if (id == 3) sparse.clear();
                        ArrayList<Object> row = new ArrayList<Object>();
                        row.add(Long.valueOf(id));
                        row.add(id == 4 ? null : sparse);
                        st.executeAppendData(meta, row);
                    }
                } finally {
                    st.executeAppendClose();
                }
            }

            try (ResultSet rs = st.executeQuery(
                     "SELECT ID,A,ARRAY_LENGTH(A) " +
                     "FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID")) {
                int count = 0;
                while (rs.next()) {
                    System.out.println(rs.getLong(1) + " " + rs.getString(2));
                    count++;
                }
                if (count != 4) throw new IllegalStateException("Expected 4 rows");
            }
        }
    }
}
```

```bash
javac -cp "$MACHBASE_JDBC_JAR" SparseAppendFull.java
java -cp ".:$MACHBASE_JDBC_JAR" SparseAppendFull
```

Set `MACHBASE_JDBC_JAR` to the actual JDBC JAR path. The classpath separator above is for
Linux. Confirm that four rows are retrieved without errors, then compare with the
[common expected results](#결과-확인).

### Append with Selected-Column Open

The existing `executeAppendOpen(String, int)` remains the full-row API. Specify selected
targets with the following overload:

```java
ResultSet executeAppendOpen(String tableName,
                            String[] inputColumns,
                            int errorCheckCount)
```

```java
import com.machbase.jdbc.MachConnection;
import com.machbase.jdbc.MachSparseArray;
import com.machbase.jdbc.MachStatement;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class SparseAppend {
    static void append(MachStatement st, String[] columns, Object[][] values)
        throws Exception {
        try (ResultSet metaResult = st.executeAppendOpen(
                 "ARRAY_APPEND_EXAMPLE", columns, 0)) {
            ResultSetMetaData meta = metaResult.getMetaData();
            try {
                for (Object[] value : values) {
                    ArrayList<Object> row = new ArrayList<Object>();
                    for (Object item : value) row.add(item);
                    st.executeAppendData(meta, row);
                }
            } finally {
                st.executeAppendClose();
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Class.forName("com.machbase.jdbc.MachDriver");
        MachConnection con = (MachConnection)DriverManager.getConnection(
            "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER");
        try {
            try (MachStatement st = (MachStatement)con.createStatement()) {
                append(st, new String[] {"ID", "A[0]", "A[3]"},
                       new Object[][] {{1L, 10, 40}});

                Map<Integer,Object> entries = new HashMap<Integer,Object>();
                entries.put(1, 200);
                entries.put(3, 400);
                MachSparseArray sparse = con.createSparseArrayOf(
                    "INT32", 4, entries);
                MachSparseArray empty = con.createSparseArrayOf(
                    "INT32", 4, new HashMap<Integer,Object>());
                append(st, new String[] {"ID", "A"}, new Object[][] {
                    {2L, sparse}, {3L, empty}, {4L, null}
                });

                try (ResultSet rs = st.executeQuery(
                    "SELECT ID,A,ARRAY_LENGTH(A) " +
                    "FROM ARRAY_APPEND_EXAMPLE ORDER BY ID")) {
                    while (rs.next())
                        System.out.println(
                            rs.getLong(1) + " " + rs.getString(2));
                }
            }
        } finally {
            con.close();
        }
    }
}
```

Map keys passed to `createSparseArrayOf()` are 0-based element positions. Reuse an object
with `MachSparseArray.clear()` and `set()`. An empty map means an ARRAY with all NULL
elements; Java `null` means whole NULL.

## Python DB-API

<a id="python-full-open"></a>

### Append a Sparse ARRAY Without a Column List

The DB-API `append()` handles Open, input, and Close internally. Omit `columns=` and pass
`ID` and `SparseArray` in each row. Prepare the standard example table first, then save
and run the following as `sparse_append_full.py`.

```python
from machbaseAPI import SparseArray, connect

conn = connect(host="127.0.0.1", port=5656, user="SYS", password="MANAGER")
try:
    first = SparseArray(4).set(0, 10).set(3, 40)
    second = SparseArray(4).set(1, 200).set(3, 400)
    empty = SparseArray(4)
    conn.append("ARRAY_APPEND_FULL_EXAMPLE", [
        [1, first], [2, second], [3, empty], [4, None],
    ])
    rows = conn.cursor(dictionary=False).execute(
        "SELECT ID,A,ARRAY_LENGTH(A) "
        "FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID"
    ).fetchall()
    expected = [
        (1, [10, None, None, 40], 4),
        (2, [None, 200, None, 400], 4),
        (3, [None, None, None, None], 4),
        (4, None, None),
    ]
    assert rows == expected, rows
    print("Python full-row sparse append OK")
finally:
    conn.close()
```

```bash
python3 sparse_append_full.py
```

If the query results match expectations, it prints `Python full-row sparse append OK`.

### Append with Selected Columns

The existing `append(table, rows)` is unchanged. Use the `columns=` keyword for selected targets.

```python
from machbaseAPI import SparseArray, connect


def main():
    conn = connect(host="127.0.0.1", port=5656,
                   user="SYS", password="MANAGER",
                   database="MACHBASEDB")
    try:
        conn.append(
            "ARRAY_APPEND_EXAMPLE",
            [[1, 10, 40]],
            columns=["ID", "A[0]", "A[3]"],
        )

        sparse = SparseArray(4).set(1, 200).set(3, 400)
        empty = SparseArray(4)
        conn.append(
            "ARRAY_APPEND_EXAMPLE",
            [[2, sparse], [3, empty], [4, None]],
            columns=["ID", "A"],
        )

        rows = conn.cursor(dictionary=False).execute(
            "SELECT ID,A,ARRAY_LENGTH(A) "
            "FROM ARRAY_APPEND_EXAMPLE ORDER BY ID"
        ).fetchall()
        expected = [
            (1, [10, None, None, 40], 4),
            (2, [None, 200, None, 400], 4),
            (3, [None, None, None, None], 4),
            (4, None, None),
        ]
        assert rows == expected, rows
        print("Python sparse append OK")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

`SparseArray.clear()` resets all elements to NULL while preserving the element count.

### Python legacy wrapper

<a id="python-legacy-full-open"></a>

#### Append with Standard appendOpen

Open with `appendOpen(table)`, then use `appendData()`. A sparse array does not require
`appendOpenColumns()`. Prepare the standard example table, then save and run as
`sparse_append_full_legacy.py`.

```python
from machbaseAPI import SparseArray, machbase

db = machbase()
if db.open("127.0.0.1", "SYS", "MANAGER", 5656) != 1:
    raise RuntimeError(db.result())
try:
    if db.appendOpen("ARRAY_APPEND_FULL_EXAMPLE") != 1:
        raise RuntimeError(db.result())
    try:
        sparse = SparseArray(4).set(0, 10).set(3, 40)
        for row_id in range(1, 5):
            if row_id == 2:
                sparse.clear().set(1, 200).set(3, 400)
            if row_id == 3:
                sparse.clear()
            row = [row_id, None if row_id == 4 else sparse]
            if db.appendData("ARRAY_APPEND_FULL_EXAMPLE", None, row) != 1:
                raise RuntimeError(db.result())
    finally:
        if db.appendClose() != 1:
            raise RuntimeError(db.result())
    if db.select(
        "SELECT ID,A,ARRAY_LENGTH(A) "
        "FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID"
    ) != 1:
        raise RuntimeError(db.result())
    print(db.result())
finally:
    db.close()
```

```bash
python3 sparse_append_full_legacy.py
```

Compare the query output from `db.result()` with the [common expected results](#결과-확인).

#### Append with Selected-Column Open

The existing `appendOpen(table, types=None)` remains the full-row API. Use
`appendOpenColumns(table, columns, types=None)` for selected targets.

```python
from machbaseAPI import SparseArray, machbase

db = machbase()
if db.open("127.0.0.1", "SYS", "MANAGER", 5656) != 1:
    raise RuntimeError(db.result())
try:
    if db.appendOpenColumns(
        "ARRAY_APPEND_EXAMPLE", ["ID", "A[0]", "A[3]"]
    ) != 1:
        raise RuntimeError(db.result())
    try:
        if db.appendData(
            "ARRAY_APPEND_EXAMPLE", None, [1, 10, 40]
        ) != 1:
            raise RuntimeError(db.result())
    finally:
        if db.appendClose() != 1:
            raise RuntimeError(db.result())

    sparse = SparseArray(4).set(1, 200).set(3, 400)
    empty = SparseArray(4)
    if db.appendOpenColumns(
        "ARRAY_APPEND_EXAMPLE", ["ID", "A"]
    ) != 1:
        raise RuntimeError(db.result())
    try:
        for row in ([2, sparse], [3, empty], [4, None]):
            if db.appendData("ARRAY_APPEND_EXAMPLE", None, row) != 1:
                raise RuntimeError(db.result())
    finally:
        if db.appendClose() != 1:
            raise RuntimeError(db.result())
finally:
    db.close()
```

The value count and order in `appendData()` follow the open target list. For new code,
prefer the more concise DB-API `append(..., columns=...)`.

## Node.js

<a id="node-full-columns"></a>

### Append a Sparse ARRAY with All Column Definitions

Node.js also uses `appendOpen()` for sparse arrays. However, the current
`@machbase/ts-client` requires `columns` in `appendOpen(table, columns, options?)`. There
is no separate `OpenColumns` method; full and selected input use the same method.

The example defines both input columns, `ID` then `A`, for the standard example table.
It does not specify element targets such as `A[0]` in Open; each row's `SparseArray`
chooses the positions. Save as `sparse_append_full.js` and run in a project using a
package with ARRAY support.

```javascript
'use strict';
const { createConnection, SparseArray } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({
    host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER',
  });
  await conn.connect();
  try {
    const stream = await conn.appendOpen('ARRAY_APPEND_FULL_EXAMPLE', [
      { name: 'ID', type: 'int64' },
      { name: 'A', type: 'int32-array' },
    ]);
    try {
      await stream.append([
        [1n, new SparseArray(4).set(0, 10).set(3, 40)],
        [2n, new SparseArray(4).set(1, 200).set(3, 400)],
        [3n, new SparseArray(4)],
        [4n, null],
      ]);
    } finally {
      await stream.close();
    }
    const [rows] = await conn.query(
      'SELECT ID,A,ARRAY_LENGTH(A) LEN ' +
      'FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID',
    );
    if (rows.length !== 4) throw new Error('Expected 4 rows');
    console.log(rows);
  } finally {
    await conn.end();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
```

```bash
node sparse_append_full.js
```

Check that four rows are retrieved and compare with the [common expected results](#결과-확인).
Calling `appendOpen(table)` without column definitions or passing `[]` for automatic
inference is not supported.

### Append with Selected Column and Element Definitions

Set `AppendColumnDefinition.name` to a whole-column target or an element-position target.

```javascript
'use strict';
const { createConnection, SparseArray } = require('@machbase/ts-client');

async function appendRows(connection, columns, rows) {
  const appender = await connection.appendOpen('ARRAY_APPEND_EXAMPLE', columns);
  try {
    await appender.append(rows);
  } finally {
    await appender.close();
  }
}

(async () => {
  const connection = createConnection({
    host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER',
  });
  await connection.connect();
  try {
    await appendRows(connection, [
      { name: 'ID', type: 'int64' },
      { name: 'A[0]', type: 'int32' },
      { name: 'A[3]', type: 'int32' },
    ], [[1n, 10, 40]]);

    const sparse = new SparseArray(4).set(1, 200).set(3, 400);
    const empty = new SparseArray(4);
    await appendRows(connection, [
      { name: 'ID', type: 'int64' },
      { name: 'A', type: 'int32-array' },
    ], [[2n, sparse], [3n, empty], [4n, null]]);

    const [rows] = await connection.query(
      'SELECT ID,A,ARRAY_LENGTH(A) LEN ' +
      'FROM ARRAY_APPEND_EXAMPLE ORDER BY ID',
    );
    console.log(rows);
  } finally {
    await connection.end();
  }
})().catch((error) => {
  console.error(error.stack || error);
  process.exitCode = 1;
});
```

`SparseArray` is also treated as an ARRAY-compatible value when
`MACHBASE_NATIVE_APPEND=0` selects the prepared fallback path.

## .NET full/legacy provider

<a id="dotnet-full-open"></a>

### Append a Sparse ARRAY with Standard AppendOpen

Open with `AppendOpen(table)` and pass `MachSparseArray` to `AppendData()`. Prepare the
standard example table first. Use this code as `Program.cs` in a C# project referencing
a full/legacy provider with ARRAY support.

```csharp
using System;
using System.Collections.Generic;
using Mach.Data.MachClient;

public class SparseAppendFull
{
    public static void Main()
    {
        using var conn = new MachConnection(
            "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER");
        conn.Open();
        using var command = new MachCommand(conn);
        var writer = command.AppendOpen("ARRAY_APPEND_FULL_EXAMPLE");
        try
        {
            var first = new MachSparseArray(MachDBType.INT32_ARRAY, 4)
                .Set(0, 10).Set(3, 40);
            var second = new MachSparseArray(MachDBType.INT32_ARRAY, 4)
                .Set(1, 200).Set(3, 400);
            var empty = new MachSparseArray(MachDBType.INT32_ARRAY, 4);
            var rows = new List<List<object>> {
                new List<object> { 1L, first },
                new List<object> { 2L, second },
                new List<object> { 3L, empty },
                new List<object> { 4L, DBNull.Value },
            };
            foreach (var row in rows) command.AppendData(writer, row);
        }
        finally
        {
            if (command.IsAppendOpened) command.AppendClose(writer);
        }
        if (writer.FailureCount != 0)
            throw new InvalidOperationException("APPEND row failure");

        using var verify = new MachCommand(
            "SELECT ID,A,ARRAY_LENGTH(A) FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID",
            conn);
        using var reader = verify.ExecuteReader();
        int count = 0;
        while (reader.Read())
        {
            Console.WriteLine(reader.IsDBNull(1)
                ? $"{reader.GetInt64(0)} NULL"
                : $"{reader.GetInt64(0)} " +
                  string.Join(",", (object[])reader.GetValue(1)));
            count++;
        }
        if (count != 4) throw new InvalidOperationException("Expected 4 rows");
    }
}
```

Save the following project file as `SparseAppendFull.csproj` beside `Program.cs`.
The example uses a .NET 8 provider.

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <EnableDefaultCompileItems>false</EnableDefaultCompileItems>
  </PropertyGroup>
  <ItemGroup>
    <Compile Include="Program.cs" />
    <Reference Include="MachbaseProvider">
      <HintPath>$(MachbaseProviderDll)</HintPath>
    </Reference>
  </ItemGroup>
</Project>
```

Replace the path below with the actual path to the .NET 8 provider DLL with ARRAY support.

```bash
dotnet build SparseAppendFull.csproj -p:MachbaseProviderDll=/absolute/path/to/provider.dll
dotnet bin/Debug/net8.0/SparseAppendFull.dll
```

Check that Close reports 0 failures and the query returns four rows, then compare with
the [common expected results](#결과-확인).

### Append with Selected-Column Open

The full API and legacy-compatible MachConnector40 provide overloads accepting selected
targets. The existing `AppendOpen(string)` and error-check overloads are unchanged.

```csharp
MachAppendWriter AppendOpen(string tableName,
                            IList<string> inputColumns);
MachAppendWriter AppendOpen(string tableName,
                            IList<string> inputColumns,
                            int errorCheckCount,
                            MachAppendOption option);
```

```csharp
using System;
using System.Collections.Generic;
using Mach.Data.MachClient;

static void Append(MachConnection connection,
                   IList<string> columns,
                   IList<List<object>> rows)
{
    using var command = new MachCommand(connection);
    var writer = command.AppendOpen("ARRAY_APPEND_EXAMPLE", columns);
    try
    {
        foreach (var row in rows)
            command.AppendData(writer, row);
    }
    finally
    {
        if (command.IsAppendOpened)
            command.AppendClose(writer);
    }
    if (writer.FailureCount != 0)
        throw new InvalidOperationException("APPEND row failure");
}

using var connection = new MachConnection(
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER");
connection.Open();

Append(connection,
    new List<string> { "ID", "A[0]", "A[3]" },
    new List<List<object>> {
        new List<object> { 1L, 10, 40 }
    });

var sparse = new MachSparseArray(MachDBType.INT32_ARRAY, 4)
    .Set(1, 200).Set(3, 400);
var empty = new MachSparseArray(MachDBType.INT32_ARRAY, 4);
Append(connection,
    new List<string> { "ID", "A" },
    new List<List<object>> {
        new List<object> { 2L, sparse },
        new List<object> { 3L, empty },
        new List<object> { 4L, DBNull.Value },
    });

using var verify = new MachCommand(
    "SELECT ID,A,ARRAY_LENGTH(A) FROM ARRAY_APPEND_EXAMPLE ORDER BY ID",
    connection);
using var reader = verify.ExecuteReader();
while (reader.Read())
    Console.WriteLine(reader.IsDBNull(1)
        ? $"{reader.GetInt64(0)} NULL"
        : $"{reader.GetInt64(0)} " +
          string.Join(",", (object[])reader.GetValue(1)));
```

`MachSparseArray.Clear()` resets the object to a reusable state with all NULL elements.
Whole NULL is `DBNull.Value`. If metadata processing fails after Append Open succeeds,
the provider cleans up the open handle and the connection remains reusable.

## Go neo-client

<a id="go-full-open"></a>

### Append with Connect Without Column Arguments

Omit column arguments from `Appender.Connect(ctx, dsn, table)` and send rows with
`Append(id, sparse)`. This LOG example does not pass `_arrival_time` explicitly. A nil
`*api.Array` means whole NULL and is distinct from an empty sparse object.

The code requires `neo-client/v2` source with ARRAY support using 0-based element
positions. Save it as `sparse_append_full.go` in a Go module linked to that source through
`go.work` or `replace`. The source must meet the same version requirements as the selected example below.

```go
package main

import (
    "context"
    "database/sql"
    "errors"
    "fmt"

    client "github.com/machbase/neo-client/v2"
    "github.com/machbase/neo-client/v2/api"
)

func appendFull(ctx context.Context, dsn string) error {
    first, err := api.NewSparseArray(api.SqlTypeInt32, 4)
    if err != nil { return err }
    if err = first.Set(0, int32(10)); err != nil { return err }
    if err = first.Set(3, int32(40)); err != nil { return err }
    second, err := api.NewSparseArray(api.SqlTypeInt32, 4)
    if err != nil { return err }
    if err = second.Set(1, int32(200)); err != nil { return err }
    if err = second.Set(3, int32(400)); err != nil { return err }
    empty, err := api.NewSparseArray(api.SqlTypeInt32, 4)
    if err != nil { return err }
    var wholeNull *api.Array

    appender := &client.Appender{}
    if err = appender.Connect(ctx, dsn, "ARRAY_APPEND_FULL_EXAMPLE"); err != nil {
        return err
    }
    for _, row := range [][]any{
        {int64(1), first}, {int64(2), second},
        {int64(3), empty}, {int64(4), wholeNull},
    } {
        if err = appender.Append(row...); err != nil {
            _, _, closeErr := appender.Close()
            return errors.Join(err, closeErr)
        }
    }
    success, failure, err := appender.Close()
    if err != nil { return err }
    if success != 4 || failure != 0 {
        return fmt.Errorf("success=%d failure=%d", success, failure)
    }
    return nil
}

func main() {
    ctx := context.Background()
    dsn := "server=tcp://sys:manager@127.0.0.1:5656"
    if err := appendFull(ctx, dsn); err != nil { panic(err) }
    db, err := sql.Open(client.DefaultDriverName, dsn)
    if err != nil { panic(err) }
    defer db.Close()
    rows, err := db.QueryContext(ctx,
        "SELECT ID,A,ARRAY_LENGTH(A) FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID")
    if err != nil { panic(err) }
    defer rows.Close()
    count := 0
    for rows.Next() {
        var id int64
        var value sql.NullString
        var length sql.NullInt64
        if err = rows.Scan(&id, &value, &length); err != nil { panic(err) }
        if value.Valid { fmt.Println(id, value.String, length.Int64) } else {
            fmt.Println(id, "NULL")
        }
        count++
    }
    if err = rows.Err(); err != nil { panic(err) }
    if count != 4 { panic("Expected 4 rows") }
}
```

```bash
go run sparse_append_full.go
```

Check that Close reports 4 successes and 0 failures, and verify the query results.

### Append with Selected-Column Connect

This example connects `neo-client` directly to Machbase DBMS, not to a Machbase Neo server.
The 0-based ARRAY and selected-column Append APIs are in v2 module source after
[`neo-client` PR #17](https://github.com/machbase/neo-client/pull/17). Until a public v2
release is specified, do not assume published module versions include these features.

```go
package main

import (
    "context"
    "database/sql"
    "errors"
    "fmt"

    client "github.com/machbase/neo-client/v2"
    "github.com/machbase/neo-client/v2/api"
)

func appendRows(ctx context.Context, dsn, table string,
    columns []string, rows [][]any) error {
    appender := &client.Appender{}
    if err := appender.Connect(ctx, dsn, table, columns...); err != nil {
        return err
    }
    for _, row := range rows {
        if err := appender.Append(row...); err != nil {
            _, _, closeErr := appender.Close()
            return errors.Join(err, closeErr)
        }
    }
    success, failure, err := appender.Close()
    if err != nil { return err }
    if failure != 0 {
        return fmt.Errorf("append success=%d failure=%d", success, failure)
    }
    return nil
}

func main() {
    ctx := context.Background()
    dsn := "server=tcp://sys:manager@127.0.0.1:5656"
    db, err := sql.Open(client.DefaultDriverName, dsn)
    if err != nil { panic(err) }
    defer db.Close()
    if err := db.PingContext(ctx); err != nil { panic(err) }

    if err := appendRows(ctx, dsn, "ARRAY_APPEND_EXAMPLE",
        []string{"ID", "A[0]", "A[3]"},
        [][]any{{int64(1), int32(10), int32(40)}}); err != nil {
        panic(err)
    }

    sparse, err := api.NewSparseArray(api.SqlTypeInt32, 4)
    if err != nil { panic(err) }
    if err := sparse.Set(1, int32(200)); err != nil { panic(err) }
    if err := sparse.Set(3, int32(400)); err != nil { panic(err) }
    empty, err := api.NewSparseArray(api.SqlTypeInt32, 4)
    if err != nil { panic(err) }
    var wholeNull *api.Array
    if err := appendRows(ctx, dsn, "ARRAY_APPEND_EXAMPLE",
        []string{"ID", "A"}, [][]any{
            {int64(2), sparse}, {int64(3), empty}, {int64(4), wholeNull},
        }); err != nil {
        panic(err)
    }

    rows, err := db.QueryContext(ctx,
        "SELECT ID,A,ARRAY_LENGTH(A) FROM ARRAY_APPEND_EXAMPLE ORDER BY ID")
    if err != nil { panic(err) }
    defer rows.Close()
    for rows.Next() {
        var id int64
        var value sql.NullString
        var length sql.NullInt64
        if err := rows.Scan(&id, &value, &length); err != nil { panic(err) }
        if !value.Valid { fmt.Println(id, "NULL"); continue }
        fmt.Println(id, value.String, length.Int64)
    }
    if err := rows.Err(); err != nil { panic(err) }
}
```

The variadic arguments to `Appender.Connect(ctx, dsn, table, columns...)` specify selected
targets. Apply `WithInputColumns(columns...)` before `Connect()`. Do not call `Append`,
`Flush`, and `Close` concurrently on one `Appender`.

<a id="결과-확인"></a>

## Verify Results

After running a standard example, use this query to check values, whole NULL, and NULL elements.

```sql
SELECT ID, A, ARRAY_LENGTH(A), A[0], A[1], A[2], A[3]
  FROM ARRAY_APPEND_FULL_EXAMPLE
 ORDER BY ID;
```

After a selected example, use this query. Both tables have the same expected results.

```sql
SELECT ID, A, ARRAY_LENGTH(A), A[0], A[1], A[2], A[3]
  FROM ARRAY_APPEND_EXAMPLE
 ORDER BY ID;
```

| ID | A | `ARRAY_LENGTH(A)` |
|---:|---|---:|
| 1 | `[10,null,null,40]` | 4 |
| 2 | `[null,200,null,400]` | 4 |
| 3 | `[null,null,null,null]` | 4 |
| 4 | `NULL` | `NULL` |

Running SDK examples consecutively against one table creates duplicate IDs. For validation,
empty the table between examples or use different ID ranges.

<a id="sparse-append-cleanup"></a>

## Clean Up the Examples

After checking results, drop only the tables created for this exercise. Use both statements
if you ran both examples; otherwise, drop only the relevant table.

```sql
DROP TABLE ARRAY_APPEND_FULL_EXAMPLE;
DROP TABLE ARRAY_APPEND_EXAMPLE;
```

Each statement deletes the table and its data. Do not run it against an existing business
table with the same name. To rerun, start with the setup SQL.

## Versions and Limitations

- `ARRAY` and selected-column Append are Machbase DBMS 8.7.0 features.
- Public ARRAY element positions are 0-based. Subtract 1 from sparse ARRAY and selected-target
  positions used by earlier development versions with 1-based positions. Do not change
  separately defined 1-based standard APIs such as JDBC parameter positions.
- Use a Machbase DBMS 8.7.0 server with an SDK build that includes ARRAY support.
- Existing full-row Append Open function and method signatures and semantics are unchanged.
- C API column-name lists are NULL-terminated arrays without a separate count.
- Invalid element counts, duplicate or out-of-range positions, duplicate targets, whole/element
  target conflicts, and mismatched value counts are errors.
- Until an official module release, the Go ARRAY API requires linking development source
  that includes the feature.
- SDKs must not include failed rows in success counts.
