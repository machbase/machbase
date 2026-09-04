---
type: docs
title: '11.10.1 Sparse ARRAY와 선택 컬럼 Append API'
weight: 10
toc: true
---

Machbase DBMS 8.7.0에서는 고정 길이 `ARRAY`의 일부 위치만 입력할 수 있습니다. 행마다
입력 위치가 달라지는 경우에는 sparse ARRAY를 사용하고, 여러 Append 행이 같은 위치를
입력하는 경우에는 Append Open 단계에서 선택 컬럼을 지정합니다.

`ARRAY` 타입 선언, 일반 입력, 조회와 SDK별 dense ARRAY 처리는
[숫자 ARRAY 타입](/dbms/reference/sql/type-data-types-dictionary/array/)을 참고하십시오.

## 입력 방식 선택

| 요구사항 | 권장 방식 |
|---|---|
| SQL 한 행에서 값이 있는 위치만 지정 | `ARRAY_SPARSE(position => value, ...)` |
| 여러 Append 행이 항상 같은 위치를 입력 | Append Open의 `A[1]`, `A[4]` target |
| Append 행마다 입력 위치가 다름 | whole `A` target과 SDK sparse 객체 |
| 모든 요소가 NULL인 non-NULL ARRAY | 빈 sparse 객체 |
| ARRAY 자체가 NULL | SQL `NULL` 또는 SDK의 whole-NULL 값 |

위치는 SQL과 모든 SDK 공개 API에서 1부터 시작합니다.

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
VALUES (1, ARRAY_SPARSE(1 => 10, 4 => 40));
```

SELECT처럼 대상 타입을 추론할 수 없는 문맥에서는 요소 타입과 cardinality를 먼저
지정합니다.

```sql
SELECT ARRAY_SPARSE(INT32[4], 1 => 10, 4 => 40);
SELECT ARRAY_SPARSE(DECIMAL(12,4)[4], 2 => 1.2500);
```

- position은 `1..cardinality` 범위의 정수 literal이어야 합니다.
- pair 순서는 자유지만 같은 position을 중복 지정할 수 없습니다.
- 생략한 위치와 `position => NULL`은 element NULL입니다.
- `ARRAY_SPARSE()` 또는 `ARRAY_SPARSE(INT32[4])`는 all-element-NULL ARRAY입니다.
- whole NULL은 `ARRAY_SPARSE()`가 아니라 SQL `NULL`로 입력합니다.
- 잘못된 position이나 요소 변환은 문장 전체를 실패시킵니다.

### INSERT target에 위치 지정

여러 행이 같은 위치를 입력하면 컬럼 목록에 element target을 직접 지정합니다.

```sql
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A[1], A[4])
VALUES (2, 10, 40);

-- A는 존재하지만 모든 element가 NULL입니다.
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A[1], A[4])
VALUES (3, NULL, NULL);

-- A 자체가 NULL입니다.
INSERT INTO ARRAY_APPEND_EXAMPLE (ID)
VALUES (4);
```

같은 문장에서 `A`와 `A[1]`을 함께 지정하거나 같은 element를 두 번 지정할 수 없습니다.
scalar 컬럼이나 범위 밖 위치를 element target으로 사용하면 오류입니다.

indexed target은 `INSERT ... VALUES`와 Append 선택 target에서 지원합니다.
`INSERT ... SELECT`와 `UPDATE ... SET A[1] = ...`에서는 지원하지 않습니다.

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

선택 target 목록은 비어 있을 수 없으며 대소문자를 무시해 중복될 수 없습니다. whole
ARRAY target과 같은 ARRAY의 element target을 함께 열 수 없습니다. 한 번 Append Open한
뒤에는 각 행의 값 개수와 순서가 target 목록과 정확히 같아야 합니다.

행 입력 중 오류가 발생해도 열린 Append handle은 닫아야 합니다. Append Open 자체가
실패하면 SDK가 내부 상태를 정리하므로 같은 connection을 다시 사용할 수 있습니다.

## C SQLCLI

ARRAY 입력과 조회에는 다음 공개 타입을 사용합니다.

| 타입 또는 상수 | 용도 |
|---|---|
| `SQL_MACHBASE_ARRAY` | SQL ARRAY 타입 식별 |
| `SQL_C_MACHBASE_ARRAY` | dense ARRAY 조회와 bind descriptor |
| `SQL_C_MACHBASE_SPARSE_ARRAY` | prepared sparse ARRAY 입력 |
| `SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH` | Append sparse descriptor 식별 |

### 선택 컬럼으로 Append Open

`SQLAppendOpenColumns()`와 wide 문자 버전은 마지막 원소가 `NULL`인 컬럼명 포인터
배열을 받습니다. 별도의 컬럼 수 인자는 없습니다.

```c
SQLRETURN SQL_API SQLAppendOpenColumns(
    SQLHSTMT     stmtHandle,
    SQLCHAR     *tableName,
    SQLCHAR    **columnNames,
    SQLINTEGER   errorCheckCount);

SQLRETURN SQL_API SQLAppendOpenColumnsW(
    SQLHSTMT     stmtHandle,
    SQLWCHAR    *tableName,
    SQLWCHAR   **columnNames,
    SQLINTEGER   errorCheckCount);
```

`columnNames == NULL`이거나 첫 원소가 `NULL`이면 오류입니다. C 포인터에는 배열 길이
정보가 없으므로 호출자는 반드시 마지막 `NULL`까지 유효한 배열을 제공해야 합니다.

```c
SQLCHAR *targets[] = {
    (SQLCHAR *)"ID",
    (SQLCHAR *)"A[1]",
    (SQLCHAR *)"A[4]",
    NULL
};
SQL_APPEND_PARAM row[3] = {0};
SQLBIGINT success = 0;
SQLBIGINT failure = 0;

row[0].mLong = 1;
row[1].mInteger = 10;
row[2].mInteger = 40;

SQLAppendOpenColumns(stmt, (SQLCHAR *)"ARRAY_APPEND_EXAMPLE", targets, 0);
SQLAppendDataV3(stmt, row, 3);
SQLAppendClose(stmt, &success, &failure);
```

### sparse ARRAY descriptor

whole ARRAY target에 sparse 값을 전달할 때는 `SQL_MACHBASE_SPARSE_ARRAY_DESC`를
사용합니다.

```c
SQLUSMALLINT positions[2] = {2, 4};
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

SQLCHAR *targets[] = {
    (SQLCHAR *)"ID",
    (SQLCHAR *)"A",
    NULL
};
SQL_APPEND_PARAM row[2] = {0};

row[0].mLong = 2;
row[1].mVar.mData = &sparse;
row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
```

descriptor position은 정렬하지 않아도 되지만 중복될 수 없습니다.
`element_indicators`의 값이 `SQL_NULL_DATA`이면 해당 위치는 element NULL입니다.
`entry_count == 0`은 빈 sparse ARRAY입니다. whole NULL은 다음과 같이 지정합니다.

```c
row[1].mVar.mData = NULL;
row[1].mVar.mLength = 0;
```

다음과 같이 빌드합니다.

```bash
cc -I"$MACHBASE_HOME/include" sparse_append.c \
  -L"$MACHBASE_HOME/lib" -lmachbasecli -lm -ldl -lrt -pthread \
  -o sparse_append
LD_LIBRARY_PATH="$MACHBASE_HOME/lib" ./sparse_append
```

## C++ SQLCLI

C++도 SQLCLI descriptor를 사용합니다. Append가 끝날 때까지 container의 주소가 바뀌지
않도록 크기를 먼저 고정합니다.

```cpp
std::array<SQLUSMALLINT, 2> positions{2, 4};
std::array<SQLINTEGER, 2> values{200, 400};
std::array<SQLLEN, 2> indicators{0, 0};
SQL_MACHBASE_SPARSE_ARRAY_DESC sparse{};

sparse.struct_size = sizeof(sparse);
sparse.element_c_type = SQL_C_SLONG;
sparse.cardinality = 4;
sparse.entry_count = positions.size();
sparse.positions = positions.data();
sparse.values = values.data();
sparse.value_stride = sizeof(values[0]);
sparse.element_indicators = indicators.data();

SQLCHAR *targets[] = {
    (SQLCHAR *)"ID",
    (SQLCHAR *)"A",
    nullptr
};
```

모든 예외 경로에서 `SQLAppendClose()`를 호출하도록 RAII wrapper 또는 정리 함수를
사용합니다.

## Machbase ODBC extension

Machbase driver library를 직접 링크하고 `machbase_sqlcli.h`를 사용하는 ODBC C
애플리케이션은 같은 extension 함수를 사용할 수 있습니다.

```bash
cc sparse_odbc.c -I/opt/machbase/include -L/opt/machbase/lib \
  -lmachbasecli_dll -lm -ldl -lrt -pthread -o sparse_odbc
LD_LIBRARY_PATH=/opt/machbase/lib ./sparse_odbc
```

{{< callout type="warning" >}}
범용 ODBC Driver Manager가 만든 statement handle을 direct SQLCLI extension에 넘기면
handle ABI가 다르므로 혼용하지 마십시오. 선택 컬럼 Append는 Machbase driver extension과
direct driver handle을 사용해야 합니다.
{{< /callout >}}

## JDBC

기존 `executeAppendOpen(String, int)`는 full-row API로 유지됩니다. 다음 overload에서
선택 target을 지정합니다.

```java
ResultSet executeAppendOpen(String tableName,
                            String[] inputColumns,
                            int errorCheckCount)
```

```java
try (MachStatement statement =
         (MachStatement) connection.createStatement()) {
    ResultSet metadataResult = statement.executeAppendOpen(
        "ARRAY_APPEND_EXAMPLE",
        new String[] {"ID", "A[1]", "A[4]"},
        0);
    ResultSetMetaData metadata = metadataResult.getMetaData();

    ArrayList<Object> row = new ArrayList<Object>();
    row.add(Long.valueOf(1));
    row.add(Integer.valueOf(10));
    row.add(Integer.valueOf(40));
    statement.executeAppendData(metadata, row);
    statement.executeAppendClose();
}
```

행마다 다른 위치를 입력하려면 `createSparseArrayOf()`를 사용합니다. map key는 1-based
position입니다.

```java
Map<Integer, Object> entries = new HashMap<Integer, Object>();
entries.put(Integer.valueOf(2), Integer.valueOf(200));
entries.put(Integer.valueOf(4), Integer.valueOf(400));

MachSparseArray sparse = connection.createSparseArrayOf(
    "INT32", 4, entries);
MachSparseArray empty = connection.createSparseArrayOf(
    "INT32", 4, new HashMap<Integer, Object>());
```

`MachSparseArray.set()`과 `clear()`로 같은 객체를 재사용할 수 있습니다. empty map은
all-element-NULL ARRAY이고 Java `null`은 whole NULL입니다.

## Python DB-API

기존 `append(table, rows)`는 유지되며 `columns=` keyword로 선택 target을 지정합니다.

```python
from machbaseAPI import SparseArray, connect

connection = connect(
    host="127.0.0.1",
    port=5656,
    user="SYS",
    password="MANAGER",
    database="MACHBASEDB",
)
try:
    connection.append(
        "ARRAY_APPEND_EXAMPLE",
        [[1, 10, 40]],
        columns=["ID", "A[1]", "A[4]"],
    )

    sparse = SparseArray(4).set(2, 200).set(4, 400)
    empty = SparseArray(4)
    connection.append(
        "ARRAY_APPEND_EXAMPLE",
        [[2, sparse], [3, empty], [4, None]],
        columns=["ID", "A"],
    )
finally:
    connection.close()
```

`SparseArray.clear()`는 cardinality를 유지하면서 모든 요소를 NULL로 되돌립니다.

### Python legacy wrapper

기존 `appendOpen(table, types=None)`는 full-row API로 유지됩니다. 선택 target에는
`appendOpenColumns(table, columns, types=None)`를 사용합니다.

```python
from machbaseAPI import SparseArray, machbase

db = machbase()
if db.open("127.0.0.1", "SYS", "MANAGER", 5656) != 1:
    raise RuntimeError(db.result())
try:
    if db.appendOpenColumns(
        "ARRAY_APPEND_EXAMPLE", ["ID", "A[1]", "A[4]"]
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
finally:
    db.close()
```

`appendData()`의 값 개수와 순서는 열린 target 목록을 따릅니다. 새 코드에서는 더 간결한
DB-API `append(..., columns=...)` 사용을 권장합니다.

## Node.js

`AppendColumnDefinition.name`에 whole 컬럼 또는 indexed target을 지정합니다.

```javascript
const { createConnection, SparseArray } = require('@machbase/ts-client');

const connection = createConnection({
  host: '127.0.0.1',
  port: 5656,
  user: 'SYS',
  password: 'MANAGER',
});
await connection.connect();
try {
  let appender = await connection.appendOpen('ARRAY_APPEND_EXAMPLE', [
    { name: 'ID', type: 'int64' },
    { name: 'A[1]', type: 'int32' },
    { name: 'A[4]', type: 'int32' },
  ]);
  await appender.append([[1n, 10, 40]]);
  await appender.close();

  const sparse = new SparseArray(4).set(2, 200).set(4, 400);
  const empty = new SparseArray(4);
  appender = await connection.appendOpen('ARRAY_APPEND_EXAMPLE', [
    { name: 'ID', type: 'int64' },
    { name: 'A', type: 'int32-array' },
  ]);
  await appender.append([[2n, sparse], [3n, empty], [4n, null]]);
  await appender.close();
} finally {
  await connection.end();
}
```

`MACHBASE_NATIVE_APPEND=0`으로 prepared fallback을 선택하면 `SparseArray`를 Append 값으로
사용할 수 없습니다. sparse Append는 기본 Append 경로를 사용합니다.

## .NET full/legacy provider

full API와 legacy MachConnector40은 선택 target을 받는 overload를 제공합니다. 기존
`AppendOpen(string)`과 error-check overload는 유지됩니다.

```csharp
MachAppendWriter AppendOpen(string tableName,
                            IList<string> inputColumns);
MachAppendWriter AppendOpen(string tableName,
                            IList<string> inputColumns,
                            int errorCheckCount,
                            MachAppendOption option);
```

```csharp
using var command = new MachCommand(connection);
var writer = command.AppendOpen(
    "ARRAY_APPEND_EXAMPLE",
    new List<string> { "ID", "A[1]", "A[4]" });
try
{
    command.AppendData(
        writer, new List<object> { 1L, 10, 40 });
}
finally
{
    if (command.IsAppendOpened)
        command.AppendClose(writer);
}
```

행마다 다른 위치를 입력할 때는 `MachSparseArray`를 사용합니다.

```csharp
var sparse = new MachSparseArray(MachDBType.INT32_ARRAY, 4)
    .Set(2, 200)
    .Set(4, 400);
var empty = new MachSparseArray(MachDBType.INT32_ARRAY, 4);
```

`MachSparseArray.Clear()`는 객체를 all-element-NULL 상태로 되돌립니다. whole NULL은
`DBNull.Value`입니다. Append Open 성공 후 metadata 처리에 실패하면 provider가 열린
handle을 정리하고 connection은 재사용할 수 있습니다.

## Go neo-client

이 예제는 Machbase Neo 서버가 아니라 `neo-client`가 Machbase DBMS에 직접 연결하는
경로입니다. ARRAY와 선택 컬럼 Append API가 포함된 개발 브랜치 소스를 사용해야 하며,
공개 모듈 버전에 같은 기능이 포함되었다고 가정하지 마십시오.

```go
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
    if err != nil {
        return err
    }
    if failure != 0 {
        return fmt.Errorf(
            "append success=%d failure=%d", success, failure)
    }
    return nil
}
```

```go
sparse, err := api.NewSparseArray(api.SqlTypeInt32, 4)
if err != nil {
    panic(err)
}
if err := sparse.Set(2, int32(200)); err != nil {
    panic(err)
}
if err := sparse.Set(4, int32(400)); err != nil {
    panic(err)
}

err = appendRows(
    ctx,
    dsn,
    "ARRAY_APPEND_EXAMPLE",
    []string{"ID", "A"},
    [][]any{{int64(2), sparse}},
)
```

`Appender.Connect(ctx, dsn, table, columns...)`의 가변 인자가 선택 target입니다.
`WithInputColumns(columns...)`를 사용할 때는 `Connect()`보다 먼저 적용합니다. 하나의
`Appender`에서 `Append`, `Flush`, `Close`를 동시에 호출하지 마십시오.

## 결과 확인

모든 SDK 예제 실행 후 다음 쿼리로 결과를 확인합니다.

```sql
SELECT ID, A, ARRAY_LENGTH(A), A[1], A[2], A[3], A[4]
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
- Machbase DBMS 8.7.0 서버와 ARRAY 기능이 포함된 SDK 빌드를 함께 사용합니다.
- 기존 full-row Append Open 함수와 메서드의 시그니처와 의미는 유지됩니다.
- C API의 컬럼명 목록은 NULL-terminated 배열이며 별도의 count를 받지 않습니다.
- 잘못된 cardinality, 중복 또는 범위 밖 position, 중복 target, whole/element target
  충돌과 값 개수 불일치는 오류입니다.
- Node.js prepared fallback은 `SparseArray`를 지원하지 않습니다.
- Go ARRAY API는 정식 모듈 릴리스 전까지 기능이 포함된 개발 소스를 연결해야 합니다.
- SDK는 실패한 행을 성공 건수에 포함해서는 안 됩니다.
