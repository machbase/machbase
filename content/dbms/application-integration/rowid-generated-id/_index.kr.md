---
type: docs
title: '12.6 ROWID와 INSERT 결과 ID'
weight: 60
toc: true
---

<span class="badge-since">Machbase 8.7.0부터 지원되는 기능</span>

`ROWID`는 테이블 안의 한 행을 다시 찾기 위한 64비트 식별자입니다. 단일 행을 SQL로
INSERT한 직후 SDK에서 해당 행의 ROWID를 받으면, 별도의 조회 없이 저장 결과를 확인하거나
그 행을 다시 조회할 수 있습니다.

이 기능은 Standard Edition에서 지원합니다. 서버와 SDK를 ROWID를 지원하는 버전으로 함께
업데이트해야 합니다. Cluster Edition에서는 사용할 수 없습니다.

## ROWID와 업무 키 구분

ROWID는 현재 테이블의 저장 행 위치를 가리키는 식별자이며, 주문 번호나 장비 ID 같은 영구
업무 키가 아닙니다.

- 일반 컬럼이 아니므로 `SELECT *`에는 포함되지 않습니다. 필요한 경우 명시적으로 조회합니다.
- 다른 테이블의 ROWID와 비교하거나 다른 테이블 조회에 사용하지 않습니다.
- ROWID 값을 분해하거나 산술 연산에 사용하지 않습니다.
- 숫자의 크기가 전체 테이블의 입력 순서를 의미하지는 않습니다.
- 신규 테이블에는 `ROWID`라는 실제 컬럼을 정의할 수 없습니다.
- 이전 버전에서 실제 `ROWID` 컬럼을 만든 테이블은 그 컬럼을 우선합니다. ROWID 의사 컬럼을
  사용하려면 기존 컬럼의 이름을 변경합니다.

```sql
SELECT ROWID, name, time, value
  FROM sensor_tag
 WHERE name = 'TAG-01';
```

## 테이블별 지원 범위

| 테이블 | ROWID의 의미 | 조회 조건 | 단일 INSERT 결과 |
|--------|--------------|-----------|------------------|
| LOG | 저장된 로그 행의 식별자 | `=`, `<`, `<=`, `>`, `>=`, `BETWEEN`, `ORDER BY` | 생성된 ROWID 반환 |
| TAG | 저장된 원본 TAG 행의 식별자 | 최상위 `AND`에 포함된 단일 `ROWID = 값` | 생성된 ROWID 반환 |
| TRANSACTION | 단일 `LONG`/`INT64` PRIMARY KEY 값 | 기존 PK가 지원하는 조건 | PK 값을 ROWID로 반환 |
| LOOKUP | 단일 `LONG`/`INT64` PRIMARY KEY 값 | 기존 PK가 지원하는 조건 | PK 값을 ROWID로 반환 |
| VOLATILE | 단일 `LONG`/`INT64` PRIMARY KEY 값 | 기존 PK가 지원하는 조건 | PK 값을 ROWID로 반환 |

TRANSACTION, LOOKUP, VOLATILE 테이블에서는 `AUTO_INCREMENT` 사용 여부와 관계없이 값이
`0` 이상인 단일 `LONG`/`INT64` PRIMARY KEY를 ROWID로 사용합니다. 애플리케이션이 PK 값을
지정한 경우에는 그 값이 반환되고, `AUTO_INCREMENT` PK를 생략하거나 NULL로 지정한 경우에는
서버가 생성한 값이 반환됩니다. 음수 PK는 ROWID로 사용할 수 없습니다.

LOG와 TAG ROWID는 `0..UINT64_MAX-1`, 세 PRIMARY KEY 기반 테이블은
`0..INT64_MAX` 범위입니다. `0`은 유효한 값이며 `UINT64_MAX`는 ROWID로 사용할 수
없습니다.

### LOG 조회

LOG ROWID는 범위 조회와 정렬에 사용할 수 있습니다. `_ARRIVAL_TIME`은 여러 행에서 같을 수
있으므로 특정 행을 다시 찾는 용도로는 ROWID를 사용합니다.

```sql
SELECT ROWID, message
  FROM app_log
 WHERE ROWID >= ?
   AND ROWID < ?
 ORDER BY ROWID;
```

`ROWID IN (...)`은 지원하지 않습니다.

### TAG 조회

TAG는 단일 ROWID 일치 조회만 지원합니다. 태그 이름, 시간, 값 조건을 `AND`로 함께 지정할
수 있으며 모든 조건을 만족해야 행을 반환합니다.

```sql
SELECT ROWID, name, time, value
  FROM sensor_tag
 WHERE ROWID = ?
   AND name = 'TAG-01'
   AND time >= TO_DATE('2026-08-10 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

TAG ROWID에는 다음 조건을 사용할 수 없습니다.

| 사용법 | 지원 여부 |
|--------|:---------:|
| `ROWID = ?` | O |
| `ROWID > ?`, `BETWEEN` 등 범위 조건 | X |
| `ROWID IN (...)` | X |
| `ROWID = ? OR ...` | X |
| `ORDER BY ROWID` | X |
| `DELETE ... WHERE ROWID = ?` | X |
| rollup, custom rollup, stat 결과와 결합 | X |

### TRANSACTION, LOOKUP, VOLATILE 비교

다음 세 테이블은 같은 `AUTO_INCREMENT` 선언을 사용할 수 있지만 재시작과 입력 기능이
다릅니다.

```sql
CREATE TRANSACTION TABLE orders (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);

CREATE LOOKUP TABLE lookup_orders (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);

CREATE VOLATILE TABLE volatile_orders (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);
```

| 항목 | TRANSACTION | LOOKUP | VOLATILE |
|------|-------------|--------|----------|
| 행과 다음 자동값의 재시작 후 유지 | O | O | X |
| 명시적 트랜잭션 | O | X | X |
| `INSERT ... SELECT`로 자동값 생성 | O | X | X |
| AUTO_INCREMENT 테이블 UPSERT | O (ROWID 반환 X) | X | X |
| 단일 `INSERT ... VALUES` 결과 ROWID | O | O | O |

LOOKUP의 `PROPERTY(SEQUENCE)`와 `NEXTVAL()`은 `AUTO_INCREMENT`와 별개의 기능입니다. 두
방식을 같은 컬럼에 함께 지정하지 않습니다.

명시적 트랜잭션이 진행 중일 때는 TRANSACTION 테이블 DDL을 실행할 수 없습니다.
`CREATE TRANSACTION TABLE`이 `ERR-02362`로 실패하면 먼저 `COMMIT` 또는 `ROLLBACK`한 뒤
다시 실행합니다.

### JOIN, 집계와 View

JOIN 결과에는 전체 결과를 대표하는 ROWID가 없습니다. 필요한 원본 테이블 별칭의 ROWID를
각각 조회합니다.

```sql
SELECT a.ROWID AS order_rowid,
       b.ROWID AS item_rowid,
       a.customer, b.item
  FROM orders a JOIN order_items b ON a.id = b.order_id;
```

| 조회 형태 | ROWID 처리 |
|-----------|------------|
| JOIN | 필요한 원본 테이블 별칭마다 `alias.ROWID` 지정 |
| 집계, `GROUP BY`, `DISTINCT`, 집합 연산 | 결과 행에 새 ROWID를 만들지 않음 |
| View, CTE, inline view | 내부 SELECT에서 ROWID를 명시적으로 선택한 경우에만 전달 |

## INSERT 결과로 ROWID를 받는 조건

`INSERT ... RETURNING ROWID` 문법은 사용하지 않습니다. 지원되는 SDK는 성공한 단일
`INSERT ... VALUES`의 실행 결과에 ROWID를 함께 제공합니다.

| 입력 방식 | generated ROWID | 설명 |
|-----------|:---------------:|------|
| 단일 direct `INSERT ... VALUES` | O | 행 한 개가 성공적으로 생성된 경우 |
| 단일 prepared INSERT | O | 실행할 때마다 현재 결과를 반환 |
| `INSERT ... SELECT` | X | 여러 행을 만들 수 있으므로 단일 값을 반환하지 않음 |
| execute-array, batch, `executemany()` | X | 마지막 내부 행을 대표값으로 노출하지 않음 |
| Append API, append batch | X | 고속 입력 경로에서는 반환하지 않음 |
| loader | X | 파일 입력 경로에서는 반환하지 않음 |
| UPSERT | X | INSERT 또는 UPDATE 중 하나를 단일 ROWID로 대표하지 않음 |
| 실패한 INSERT | X | 이전 실행의 ROWID도 지워짐 |

generated ROWID는 statement별 결과입니다. 연결 전체에서 최근 값을 조회하는 SQL 함수는
제공하지 않습니다.

## SDK별 차이

| SDK/도구 | 확인 방법 | 값이 있을 때 | 값이 없을 때 |
|----------|-----------|--------------|---------------|
| machsql | `SHOW LAST ROWID;` 또는 `SHOW LASTID;` | 64비트 정수 출력 | `NULL` 출력 |
| C SQLCLI/ODBC | `SQLGetGeneratedRowID()` | `SQLUBIGINT`, `SQL_SUCCESS` | `SQL_NO_DATA` |
| JDBC | `Statement.getGeneratedKeys()` | `RowId` 한 행 | 빈 ResultSet |
| Go `database/sql` | `Result.LastInsertId()` | `int64` 비트 패턴 | 오류 반환 |
| Go native (`machgo`) | 지원하지 않음 | - | - |
| Python | `cursor.lastrowid` | Python `int` (`0..UINT64_MAX-1`) | `None` |
| Node.js | 실행 결과의 `rowId` | JavaScript `bigint` | 속성 없음 |
| .NET 4.0/4.0-full, Universal .NET | `MachCommand.RowId` | `UInt64?` 값 | `null` |
| REST API | 지원하지 않음 | - | - |

SDK 실행 객체는 새 statement 실행을 시작할 때 이전 ROWID 상태를 지웁니다. 실패, batch,
append 또는 ROWID를 제공하지 않는 INSERT 뒤에 이전 값이 남아 있다고 가정하지 않습니다.
machsql은 예외적으로 SELECT와 COMMIT 같은 비 INSERT 명령 뒤에도 도구 세션의 마지막 값을
유지하며, 다음 절의 초기화 규칙을 따릅니다.

### machsql

단일 INSERT를 실행한 직후 확인합니다.

```sql
INSERT INTO orders(item) VALUES('pump');
SHOW LAST ROWID;
```

`SHOW LAST ROWID`와 `SHOW LASTID`는 같은 명령입니다. `0`도 유효한 ROWID이므로 값이 없는
상태는 `NULL`로 구분합니다. SELECT와 COMMIT 같은 비 INSERT 명령은 마지막 값을 유지하지만,
INSERT 실패·비대상 INSERT·재접속은 값을 `NULL`로 초기화합니다.

### JDBC

JDBC 표준 generated keys 흐름을 사용합니다. 기본 `executeUpdate()`와
`Statement.RETURN_GENERATED_KEYS` 요청형을 모두 지원하며, 결과에는 `ROWID` 컬럼과 최대
한 행이 포함됩니다.

```java
String sql = "INSERT INTO orders(item) VALUES(?)";
try (PreparedStatement statement = connection.prepareStatement(
         sql, Statement.RETURN_GENERATED_KEYS)) {
    statement.setString(1, "pump");
    statement.executeUpdate();

    try (ResultSet keys = statement.getGeneratedKeys()) {
        if (keys.next()) {
            RowId rowId = keys.getRowId("ROWID");
            byte[] value = rowId.getBytes();
        }
    }
}
```

지원 여부는 `DatabaseMetaData.supportsGetGeneratedKeys()`로 확인합니다. batch와 Append API는
빈 generated-keys ResultSet을 반환합니다.

### Go database/sql

`LastInsertId()`의 반환 타입은 `int64`입니다. LOG/TAG ROWID의 최상위 bit가 1이면 음수처럼
보일 수 있으므로 `uint64`로 변환해 동일한 bit pattern을 복원합니다.

```go
result, err := db.ExecContext(ctx,
    "INSERT INTO orders(item) VALUES(?)", "pump")
if err != nil {
    return err
}

value, err := result.LastInsertId()
if err != nil {
    return err
}
rowID := uint64(value)
```

generated ROWID가 없는 실행에서 `LastInsertId()`를 호출하면 오류가 발생합니다.

### Python

```python
cursor.execute(
    "INSERT INTO orders(item) VALUES(%s)",
    ("pump",),
)
row_id = cursor.lastrowid
```

`lastrowid`는 Python `int` 또는 `None`입니다. Python `int`는 임의 정밀도 정수이며,
드라이버가 ROWID를 unsigned 값으로 변환하므로 최상위 bit가 1이어도 양수로 유지됩니다.
`execute()` 시작과 실패 시 `None`으로 초기화되며, `executemany()` 뒤에도 `None`을
유지합니다.

### Node.js

```javascript
const [result] = await connection.execute(
  "INSERT INTO orders(item) VALUES(?)",
  ["pump"]
);

if (result.rowId !== undefined) {
  const rowId = result.rowId; // bigint
}
```

64비트 정밀도를 보존하기 위해 `number`가 아니라 `bigint`를 사용합니다.

### .NET

```csharp
using var command = new MachCommand(
    "INSERT INTO orders(item) VALUES('pump')",
    connection);

command.ExecuteNonQuery();
ulong? rowId = command.RowId;
```

MachConnector 4.0/4.0-full과 Universal .NET에서 ROWID는 `UInt64?`인 `RowId`로 읽습니다.
기존 32비트 `LastInsertedId`에는 ROWID가 저장되지 않습니다.

### C SQLCLI/ODBC

```c
SQLUBIGINT row_id;
SQLLEN indicator;
SQLRETURN rc;

rc = SQLGetGeneratedRowID(statement, &row_id, &indicator);
if (rc == SQL_SUCCESS && indicator == sizeof(row_id)) {
    /* row_id 사용 */
}
```

generated ROWID가 없으면 `SQL_NO_DATA`를 반환합니다.

## 조회 결과와 오류 구분

형식이 올바른 ROWID가 현재 테이블에 없으면 오류가 아니라 0행을 반환합니다. 삭제된 행,
추가 조건과 일치하지 않는 행도 같습니다. 반면 NULL, 음수 PK, `UINT64_MAX`, 숫자로 변환할
수 없는 값, TAG에서 지원하지 않는 범위·IN·OR·정렬 조건은 오류입니다.

## 유효 기간과 재시도

ROWID를 장기간 보관하는 업무 키로 사용하지 않습니다.

| 상황 | 기존 ROWID |
|------|------------|
| 정상 재시작 | 보존된 행은 유지 |
| ROWID 보존을 지원하는 제품 backup/restore | 보존된 행은 유지 |
| 행 DELETE | 무효 |
| transaction ROLLBACK | 해당 INSERT의 ROWID 무효 |
| snapshot recovery로 폐기된 행 | 무효 |
| LOG TRUNCATE | 과거 값이 재사용될 수 있음 |
| 테이블 DROP 후 재생성 | 과거 값이 다른 행을 가리킬 수 있음 |
| export/import 또는 행 재삽입 | 보존되지 않음 |

INSERT는 성공했지만 네트워크 응답이 끊기면 애플리케이션이 ROWID를 받지 못할 수 있습니다.
이때 같은 INSERT를 자동 재시도하면 중복 행이 생길 수 있으므로 업무 키나 별도의 idempotency
정책으로 실제 반영 여부를 먼저 확인합니다.

## 관련 문서

- [연동 방식 선택](/dbms/application-integration/selection-integration-method/)
- [드라이버별 가이드](/dbms/application-integration/guide-drivers/)
- [AUTO_INCREMENT](/dbms/rdb-table-usage/auto-increment/)
- [LOG 데이터 입력](/dbms/log-table-usage/data-input-mutation/)
- [TAG 데이터 입력](/dbms/tag-table-usage/data-input-mutation/)
