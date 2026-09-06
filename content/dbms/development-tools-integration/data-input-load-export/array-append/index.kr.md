---
type: docs
title: '11.10.1 Sparse ARRAY와 선택 컬럼 Append API'
weight: 10
toc: true
---

Machbase DBMS 8.7.0에서는 고정 길이 `ARRAY`의 일부 위치만 입력할 수 있습니다. 행마다
입력 위치가 달라지는 경우에는 희소 ARRAY를 사용하고, 여러 Append 행이 같은 위치를
입력하는 경우에는 Append Open 단계에서 선택 컬럼을 지정합니다.

`ARRAY` 타입 선언, 일반 입력, 조회와 SDK별 밀집 ARRAY 처리는
[숫자 ARRAY 타입](/dbms/reference/sql/type-data-types-dictionary/array/)을 참고하십시오.

## 입력 방식 선택

| 요구사항 | 권장 방식 |
|---|---|
| SQL 한 행에서 값이 있는 위치만 지정 | `ARRAY_SPARSE(position => value, ...)` |
| 여러 Append 행이 항상 같은 위치를 입력 | Append Open의 `A[0]`, `A[3]` 대상 |
| Append 행마다 입력 위치가 다름 | whole `A` 대상과 SDK 희소 객체 |
| 모든 요소가 NULL인 non-NULL ARRAY | 빈 희소 객체 |
| ARRAY 자체가 NULL | SQL `NULL` 또는 SDK의 whole-NULL 값 |

위치는 SQL과 모든 Machbase 전용 SDK API에서 0부터 시작합니다.

## SQL sparse 입력

### ARRAY_SPARSE

대상 컬럼이 있는 INSERT 또는 UPDATE 문맥에서는 위치와 값만 지정합니다.

```sql
CREATE LOG TABLE ARRAY_APPEND_EXAMPLE
(
    ID LONG,
    A  INT32[4]
);

INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A)
VALUES (1, ARRAY_SPARSE(0 => 10, 3 => 40));
```

SELECT처럼 대상 타입을 추론할 수 없는 문맥에서는 요소 타입과 요소 수를 먼저
지정합니다.

```sql
SELECT ARRAY_SPARSE(INT32[4], 0 => 10, 3 => 40);
SELECT ARRAY_SPARSE(DECIMAL(12,4)[4], 1 => 1.2500);
```

- 위치는 `0..cardinality-1` 범위의 정수 literal이어야 합니다.
- pair 순서는 자유지만 같은 위치를 중복 지정할 수 없습니다.
- 생략한 위치와 `position => NULL`은 요소 NULL입니다.
- `ARRAY_SPARSE()` 또는 `ARRAY_SPARSE(INT32[4])`는 모든 요소가 NULL인 ARRAY입니다.
- 배열 전체 NULL은 `ARRAY_SPARSE()`가 아니라 SQL `NULL`로 입력합니다.
- 잘못된 위치나 요소 변환은 문장 전체를 실패시킵니다.

### Direct sparse shorthand

`ARRAY_SPARSE` 래퍼 없이 bracket 안에 위치와 value pair를 직접 쓸 수 있습니다.

```sql
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A)
VALUES (2, [0 => 10, 3 => 40]);

SELECT [1 => 12, 33 => 23];
```

대상 ARRAY가 있으면 대상 타입과 요소 수를 사용합니다. standalone에서는 밀집
ARRAY와 같은 숫자 공통 타입을 추론하고 요소 수를 `가장 큰 position + 1`로
결정합니다. 따라서 두 번째 예제는 `INT32[34]`입니다.

standalone all-NULL 희소는 요소 타입을 알 수 없어 오류입니다. 이 경우
`ARRAY_SPARSE(TYPE[N], ...)` 형식을 사용합니다. `[]`는 기존 밀집 empty constructor로
유지되며 `ARRAY[0 => 1]`은 지원하지 않습니다.

### INSERT target에 위치 지정

여러 행이 같은 위치를 입력하면 컬럼 목록에 요소 대상을 직접 지정합니다.

```sql
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A[0], A[3])
VALUES (2, 10, 40);

-- A는 존재하지만 모든 element가 NULL입니다.
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A[0], A[3])
VALUES (3, NULL, NULL);

-- A 자체가 NULL입니다.
INSERT INTO ARRAY_APPEND_EXAMPLE (ID)
VALUES (4);
```

같은 문장에서 `A`와 `A[0]`을 함께 지정하거나 같은 요소를 두 번 지정할 수 없습니다.
스칼라 컬럼이나 범위 밖 위치를 요소 대상으로 사용하면 오류입니다.

요소 위치를 지정한 대상은 `INSERT ... VALUES`와 Append 선택 대상에서 지원합니다.
`INSERT ... SELECT`와 `UPDATE ... SET A[0] = ...`에서는 지원하지 않습니다.

## Append 공통 규칙

이 문서의 SDK 예제는 다음 네 행을 만듭니다.

```text
ID=1  A=[10,null,null,40]       고정 element target
ID=2  A=[null,200,null,400]     whole target과 sparse 객체
ID=3  A=[null,null,null,null]   빈 sparse 객체
ID=4  A=NULL                    whole NULL
```

선택 목록에 없는 일반 컬럼은 기존 Append 규칙에 따라 처리됩니다.

- nullable 컬럼은 NULL을 사용합니다.
- DEFAULT가 있는 컬럼은 DEFAULT를 사용합니다.
- 값을 반드시 요구하는 컬럼이 빠지면 Append Open 또는 행 입력이 실패합니다.

선택 대상 목록은 비어 있을 수 없으며 대소문자를 무시해 중복될 수 없습니다. whole
ARRAY 대상과 같은 ARRAY의 요소 대상을 함께 열 수 없습니다. 한 번 Append Open한
뒤에는 각 행의 값 개수와 순서가 대상 목록과 정확히 같아야 합니다.

행 입력 중 오류가 발생해도 열린 Append 핸들은 닫아야 합니다. Append Open 자체가
실패하면 SDK가 내부 상태를 정리하므로 같은 연결을 다시 사용할 수 있습니다.

## C SQLCLI

ARRAY 입력과 조회에는 다음 공개 타입을 사용합니다.

| 타입 또는 상수 | 용도 |
|---|---|
| `SQL_MACHBASE_ARRAY` | SQL ARRAY 타입 식별 |
| `SQL_C_MACHBASE_ARRAY` | 밀집 ARRAY 조회와 bind 디스크립터 |
| `SQL_C_MACHBASE_SPARSE_ARRAY` | prepared 희소 ARRAY 입력 |
| `SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH` | Append 희소 디스크립터 식별 |

`SQLAppendOpenColumns()`와 와이드 문자 버전은 마지막 원소가 `NULL`인 컬럼명 포인터
배열을 받습니다. 별도의 컬럼 수 인자는 없습니다.

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

`aColumnNames == NULL`이거나 첫 원소가 `NULL`이면 오류입니다. C 포인터에는 배열 길이
정보가 없으므로 호출자는 반드시 마지막 `NULL`까지 유효한 배열을 제공해야 합니다. 종단
`NULL`을 빠뜨리면 배열 경계를 벗어나 읽을 수 있으므로 안전하게 진단된다고 가정하면 안
됩니다.

다음 `sparse_append.c`는 테이블을 만들고 네 행을 Append한 뒤 결과를 출력합니다.

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

다음과 같이 빌드하고 실행합니다.

```bash
cc -I"$MACHBASE_HOME/include" sparse_append.c \
  -L"$MACHBASE_HOME/lib" -lmachbasecli -lm -ldl -lrt -pthread \
  -o sparse_append
LD_LIBRARY_PATH="$MACHBASE_HOME/lib" ./sparse_append
```

디스크립터 위치는 0부터 시작하는 인덱스입니다. 정렬하지 않아도 되지만 중복될 수 없습니다.
entry indicator가
`SQL_NULL_DATA`이면 해당 위치는 요소 NULL입니다. `entry_count == 0`은 빈 희소
ARRAY이고, 배열 전체 NULL은 `mVar.mData = NULL`, `mVar.mLength = 0`으로 지정합니다.

## C++ SQLCLI

C++ 전용 전송 객체를 새로 만들지 않고 SQLCLI 디스크립터를 사용합니다. 다음 예제는
RAII 래퍼로 close를 보장하고 C++ 컨테이너가 살아 있는 동안 디스크립터를 전송합니다.

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

Machbase 드라이버 라이브러리를 직접 링크하고 `machbase_sqlcli.h`를 사용하는 ODBC C
애플리케이션은 같은 extension 함수를 사용할 수 있습니다. 다음 예제는 direct Machbase
드라이버 API로 네 행을 입력합니다. 테이블은 앞 절의 DDL로 미리 만듭니다.

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
범용 ODBC Driver Manager가 만든 문장 핸들을 direct SQLCLI extension에 넘기면
핸들 ABI가 다르므로 혼용하지 마십시오. 선택 컬럼 Append는 Machbase 드라이버 extension과
direct 드라이버 핸들을 사용해야 합니다. 범용 ODBC API에는 Append Open 선택 대상이
없습니다.
{{< /callout >}}

## JDBC

기존 `executeAppendOpen(String, int)`는 전체 행 API로 유지됩니다. 다음 오버로드에서
선택 대상을 지정합니다.

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

`createSparseArrayOf()`에 전달하는 맵의 키는 0부터 시작하는 요소 위치입니다. `MachSparseArray.clear()`와
`set()`으로 같은 객체를 재사용할 수 있습니다. 빈 맵은 모든 요소가 NULL인 ARRAY이고
Java `null`은 배열 전체 NULL입니다.

## Python DB-API

기존 `append(table, rows)`는 유지되며 `columns=` keyword로 선택 대상을 지정합니다.

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

`SparseArray.clear()`는 요소 수를 유지하면서 모든 요소를 NULL로 되돌립니다.

### Python legacy wrapper

기존 `appendOpen(table, types=None)`는 전체 행 API로 유지됩니다. 선택 대상에는
`appendOpenColumns(table, columns, types=None)`를 사용합니다.

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

`appendData()`의 값 개수와 순서는 열린 대상 목록을 따릅니다. 새 코드에서는 더 간결한
DB-API `append(..., columns=...)` 사용을 권장합니다.

## Node.js

`AppendColumnDefinition.name`에 컬럼 전체 또는 요소 위치를 지정한 대상을 지정합니다.

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

`MACHBASE_NATIVE_APPEND=0`으로 prepared 대체 경로를 선택해도 `SparseArray`를
ARRAY-compatible 값으로 처리합니다.

## .NET full/legacy provider

full API와 기존 호환 MachConnector40은 선택 대상을 받는 오버로드를 제공합니다. 기존
`AppendOpen(string)`과 error-check 오버로드는 유지됩니다.

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

`MachSparseArray.Clear()`는 객체를 재사용 가능한 모든 요소가 NULL인 상태로 되돌립니다.
배열 전체 NULL은 `DBNull.Value`입니다. Append Open 성공 후 메타데이터 처리에 실패하면
프로바이더가 열린 핸들을 정리하고 연결은 재사용할 수 있습니다.

## Go neo-client

이 예제는 Machbase Neo 서버가 아니라 `neo-client`가 Machbase DBMS에 직접 연결하는
경로입니다. 요소 위치가 0부터 시작하는 ARRAY와 선택 컬럼 Append API는
[`neo-client` PR #17](https://github.com/machbase/neo-client/pull/17) 이후의 v2 module
소스에 있습니다. 공개 v2 릴리스가 지정되기 전에는 공개 모듈 버전에 같은 기능이
포함되었다고 가정하지 마십시오.

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

`Appender.Connect(ctx, dsn, table, columns...)`의 가변 인자가 선택 대상입니다.
`WithInputColumns(columns...)`를 사용할 때는 `Connect()`보다 먼저 적용합니다. 하나의
`Appender`에서 `Append`, `Flush`, `Close`를 동시에 호출하지 마십시오.

## 결과 확인

모든 SDK 예제 실행 후 다음 쿼리로 결과를 확인합니다.

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

각 SDK 예제를 같은 테이블에 연속으로 실행하면 ID가 중복됩니다. 실제 검증에서는 예제마다
테이블을 비우거나 서로 다른 ID 범위를 사용합니다.

## 버전과 제한 사항

- `ARRAY`와 선택 컬럼 Append는 Machbase DBMS 8.7.0 기능입니다.
- ARRAY의 공개 요소 위치는 0부터 시작합니다. 이전 개발 버전에서 위치를 1부터 지정했던
  희소 ARRAY와 선택 대상 호출은 위치를 1씩 낮춰야 합니다. JDBC의 매개변수 순번처럼
  별도로 1부터 시작하는 표준 API까지 변경하지 마십시오.
- Machbase DBMS 8.7.0 서버와 ARRAY 기능이 포함된 SDK 빌드를 함께 사용합니다.
- 기존 전체 행 Append Open 함수와 메서드의 시그니처와 의미는 유지됩니다.
- C API의 컬럼명 목록은 NULL-terminated 배열이며 별도의 건수를 받지 않습니다.
- 잘못된 요소 수, 중복 또는 범위 밖 위치, 중복 대상, whole/element 대상
  충돌과 값 개수 불일치는 오류입니다.
- Go ARRAY API는 정식 모듈 릴리스 전까지 기능이 포함된 개발 소스를 연결해야 합니다.
- SDK는 실패한 행을 성공 건수에 포함해서는 안 됩니다.
