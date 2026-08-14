---
type: docs
title: '11. 개발 도구 연동'
weight: 110
toc: true
aliases:
  - /dbms/reference/sdk-api/
  - /dbms/development-tools-integration/support-scope-sdk/
  - /dbms/application-integration/support-scope-sdk/
---

SDK별 API 레퍼런스와 기능 지원 범위를 제공합니다. 설치, 연결, SQL 실행, Append, 예제는 각 하위
페이지에서 확인하고, SDK별 기능 지원 여부와 제약은 이 페이지의 지원 범위에서 확인합니다.

SELECT 결과 컬럼의 NULL 가능 여부와 SDK별 반환 형식은
[Nullable 메타데이터 지원 범위](/dbms/development-tools-integration/#support-scope-sdk-nullable-metadata)를
참고합니다.

SELECT 결과의 PRIMARY KEY 여부와 테이블 카탈로그 조회 방법은
[PRIMARY KEY 메타데이터 지원 범위](/dbms/development-tools-integration/#support-scope-sdk-primary-key-metadata)를
참고합니다.

`:name` SQL 문법, 반복 이름과 SDK별 바인딩 방식은
[Named Bind Parameter syntax](../reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/)를
참고합니다.

## 공통 연결 정보

| 항목 | 기본값 | 설명 |
|------|--------|------|
| HOST | `127.0.0.1` | Machbase 서버 호스트명 또는 IP |
| PORT | `5656` | Machbase 서버 포트 (`machbase.conf`의 `PORT_NO`) |
| USER | `SYS` | 사용자 ID |
| PASSWORD | `MANAGER` | 사용자 비밀번호 |

## SDK별 레퍼런스

| SDK | 설명 |
|-----|------|
| [CLI/ODBC](./cli-odbc/) | C/C++ CLI/ODBC, 이름/ordinal 바인딩, Append, Nullable·PRIMARY KEY 메타데이터 |
| [JDBC](./jdbc/) | Java 8/JDBC 4.2, 트랜잭션, pool, metadata, Named Bind와 Append |
| [Python](./python/) | `machbaseapi` DB-API, named mapping, `null_ok`, 컬럼 PK 메타데이터 |
| [Node.js / TypeScript](./node-js-typescript/) | `@machbase/ts-client`, named object 입력, `ColumnMeta.nullable`, `isPrimaryKey` |
| [.NET Connector](./net-connector/) | ADO.NET 이름 컬렉션, Append, `GetSchemaTable()`의 `IsKey` |
| [Go](./go/) | `machgo`, `database/sql`, 초기 database, positional/named bind, DECIMAL·NULL, 트랜잭션, PK 메타데이터, Appender |

각 SDK의 API와 기능 지원 범위를 비교하고, 애플리케이션 요구사항에 맞는 SDK를 선택할 수 있도록
기능별 지원 여부와 제약을 정리합니다.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [전체 SDK 기능 지원표](#sdk) | 지원 SDK 목록 및 기능별 지원 여부 |
| [APPEND API 지원 범위](#support-scope-sdk-append) | SDK별 고성능 Append 쓰기 지원 여부 |
| [AUTH KEY 인증 지원](#support-scope-sdk-auth-key) | SDK별 AUTH KEY 인증 방식 지원 여부 |
| [Transaction / Prepare / Bind 지원](#support-scope-sdk-transaction-prepare-bind) | SDK별 트랜잭션·Prepared Statement·파라미터 바인딩 지원 여부 |
| [Nullable 메타데이터 지원](#support-scope-sdk-nullable-metadata) | SELECT 결과 컬럼과 Prepared Parameter의 NULL 가능 여부 |
| [PRIMARY KEY 메타데이터 지원](#support-scope-sdk-primary-key-metadata) | SELECT 결과 컬럼과 테이블 카탈로그의 PRIMARY KEY 조회 |
| [INSERT 결과 ROWID 지원](#support-scope-sdk-generated-rowid) | 단일 INSERT 후 SDK별 ROWID 확인 방법 |

## 지원 범위 기반 SDK 선택

애플리케이션 특성에 따라 아래를 참고합니다.

- **지속적인 대량 쓰기**가 필요하면 → ODBC/CLI, JDBC, Go native 등 Append API 지원 드라이버 사용
- **표준 SQL 인터페이스**가 필요하면 → JDBC, Python(DB-API 2.0), Go(`database/sql`)
- **웹 서비스·마이크로서비스 통합**이라면 → REST API
- **트랜잭션이 필요한 TRANSACTION 작업**이라면 → Go `database/sql`, JDBC 표준 트랜잭션 API 또는 ODBC/CLI 사용
- **조회 결과의 NULL 가능 여부를 실행 전에 확인**해야 한다면 → Go, SQLCLI/ODBC,
  JDBC, Node.js, Python 또는 .NET 사용
- **단일 INSERT 직후 입력된 행을 다시 조회**해야 한다면 → generated ROWID를 지원하는
  SQLCLI/ODBC, JDBC, Python, .NET, Go `database/sql` 또는 Node.js 사용

> **참고**: TAG와 LOG 테이블은 append 중심 입력에 최적화되어 있습니다. JDBC manual
> transaction에서 TRANSACTION 테이블을 변경하기 전의 독립 TAG DML은 rollback할 수 있지만,
> Append 입력과 호환 경로에서 auto-commit된 LOG DML은 rollback할 수 없습니다.

<a id="support-scope-sdk-nullable-metadata"></a>

## SELECT 결과 Nullable 메타데이터 지원

Machbase는 SELECT 결과 컬럼과 Prepared Parameter의 NULL 가능 여부를 메타데이터로
제공합니다. Standard Edition과 Cluster Edition에서 같은 의미를 사용합니다.

### Nullable 상태

| 상태 | 숫자 값 | 의미 |
|------|:------:|------|
| `NO_NULLS` | `0` | 결과가 `NULL`이 될 수 없음 |
| `NULLABLE` | `1` | 결과가 `NULL`이 될 수 있음 |
| `UNKNOWN` | `2` | 드라이버가 NULL 가능 여부를 확정할 수 없음 |

`UNKNOWN`은 `NOT NULL`을 의미하지 않습니다. 애플리케이션에서는 `NULLABLE`과
`UNKNOWN`을 모두 `NULL` 처리 대상으로 가정해야 합니다.

### SQL 결과 판정 규칙

| SELECT 결과 컬럼 | Nullable 상태 |
|------------------|----------------|
| `NOT NULL` 또는 `PRIMARY KEY`가 지정된 직접 컬럼 | `NO_NULLS` |
| TAG 이름, `BASETIME`, `SUMMARIZED` 직접 컬럼 | `NO_NULLS` |
| NULL을 허용하는 직접 컬럼 | `NULLABLE` |
| `NULL` 리터럴 | `NULLABLE` |
| NULL이 아닌 숫자, 문자열, 바이너리 리터럴 | `NO_NULLS` |
| OUTER JOIN의 NULL 공급 측 컬럼 | 원본 컬럼이 `NOT NULL`이어도 `NULLABLE` |
| VIEW 또는 집합 연산을 거친 컬럼 | `UNKNOWN` |
| 산술식, 일반 함수, `CASE`, 집계식, 바인드 값 | `UNKNOWN` |
| DECIMAL 형변환 결과 | 입력 식의 Nullable 상태 유지 |

Prepared Parameter는 대상 테이블 컬럼을 식별할 수 있으면 해당 컬럼의 Nullable 상태를
사용합니다. 대상 컬럼을 식별할 수 없으면 `UNKNOWN`을 사용합니다. Append API가 제공하는
컬럼 메타데이터는 대상 테이블의 실제 컬럼 제약을 사용합니다.

다음 SELECT에서 예상 상태는 `ID=0`, `VALUE=1`, `EXPR_VALUE=2`입니다.

```sql
CREATE LOG TABLE T_NULL_META (
    ID INTEGER NOT NULL,
    VALUE INTEGER
);

SELECT ID, VALUE, ID + 1 AS EXPR_VALUE
  FROM T_NULL_META;
```

테이블 스키마의 NULL 제약은 `DESC` 또는 `DESCRIBE`로 확인할 수 있습니다. SELECT 식이나
OUTER JOIN으로 생성된 결과 컬럼은 SDK의 결과 메타데이터 API로 확인합니다.

### SDK별 조회 방법

| SDK | API | `NO_NULLS` | `NULLABLE` | `UNKNOWN` |
|-----|-----|:----------:|:----------:|:---------:|
| SQLCLI/ODBC | `SQLDescribeCol()`, `SQLDescribeParam()`, `SQLColAttribute()`, `SQLGetDescField()` | `SQL_NO_NULLS` | `SQL_NULLABLE` | `SQL_NULLABLE_UNKNOWN` |
| JDBC | `ResultSetMetaData.isNullable()`, `ParameterMetaData.isNullable()` | `columnNoNulls` | `columnNullable` | `columnNullableUnknown` |
| Node.js | `ColumnMeta.nullable` | `ColumnNullable.NoNulls` | `ColumnNullable.Nullable` | `ColumnNullable.Unknown` |
| Python | `cursor.description[i][6]` | `False` | `True` | `None` |
| .NET | `GetSchemaTable()["AllowDBNull"]` | `false` | `true` | `DBNull.Value` |
| Go (native) | `api.Column.Nullability` | `NullabilityNoNulls` | `NullabilityNullable` | `NullabilityUnknown` |
| Go (database/sql) | `Rows.ColumnTypeNullable()` | `false, true` | `true, true` | `false, false` |
| REST API | 결과 메타데이터 API 없음 | - | - | - |

상세 API와 예제는 [CLI/ODBC](/dbms/development-tools-integration/cli-odbc/),
[JDBC](/dbms/development-tools-integration/jdbc/), [Python](/dbms/development-tools-integration/python/),
[Node.js](/dbms/development-tools-integration/node-js-typescript/),
[.NET](/dbms/development-tools-integration/net-connector/), [Go](/dbms/development-tools-integration/go/) 레퍼런스를
참고합니다.

### 테이블 카탈로그와 PRIMARY KEY 조회

SELECT 결과 메타데이터와 테이블 스키마 카탈로그는 서로 다른 API입니다.

| 조회 대상 | SQLCLI/ODBC | JDBC |
|----------|-------------|------|
| 테이블 컬럼의 NULL 제약 | `SQLColumns()`의 `NULLABLE`, `IS_NULLABLE` | `DatabaseMetaData.getColumns()`의 `NULLABLE`, `IS_NULLABLE` |
| `PRIMARY KEY` | `SQLPrimaryKeys()` | `DatabaseMetaData.getPrimaryKeys()` |

TAG 이름, `BASETIME`, `SUMMARIZED` 컬럼은 카탈로그에서도 NULL을 허용하지 않는 것으로
반환됩니다. `IS_NULLABLE`의 문자열 값은 API에서 정의한 `YES`와 `NO`를 사용합니다.

Nullable 메타데이터는 컬럼의 NULL 가능 여부만 나타냅니다. `PRIMARY KEY` 여부는 Nullable
값으로 판단하지 않고 카탈로그 API로 확인해야 합니다.

<a id="support-scope-sdk-primary-key-metadata"></a>

## PRIMARY KEY 메타데이터 지원

PRIMARY KEY 메타데이터는 SELECT 결과의 직접 컬럼에 표시되는 결과 메타데이터와 테이블의
PRIMARY KEY 목록을 반환하는 카탈로그 메타데이터로 나뉩니다. 두 메타데이터는 서로 대체할 수
없습니다.

### SELECT 결과 컬럼

| SDK | 조회 방법 | 구형 프로토콜 |
|-----|-----------|---------------|
| JDBC | Machbase 확장 `MachResultSetMetaData.isPrimaryKey(column)` | `false` |
| Node.js | `fields[i].isPrimaryKey` | `false` |
| Python | `cursor.column_metadata[i].is_primary_key` | `false` |
| .NET 4.0 / 4.0-full | `GetSchemaTable()["IsKey"]` | `false` |
| Go native | `rows.Columns()`, `row.Columns()`, `Appender.Columns()`의 `api.Column.PrimaryKey` | 플래그 없음 |
| Go (`database/sql`) | 표준 `ColumnType` PRIMARY KEY API 없음 | 플래그 없음 |

직접 참조한 PK 컬럼과 TAG 테이블의 `NAME`은 `true`로 반환됩니다. 일반 컬럼, LOG 컬럼,
표현식·집계식, 외부 조인의 NULL 공급 측 컬럼은 `false`입니다. 별칭을 사용한 직접 컬럼은
원본 컬럼의 PK 상태를 유지합니다.

### 테이블 카탈로그와 명령줄

| 도구 또는 API | PRIMARY KEY 조회 방법 | 비고 |
|--------------|----------------------|------|
| SQLCLI | 별도 표준 API 없음 | 기존 `DescribeCol` 계약은 변경하지 않음 |
| ODBC | `SQLPrimaryKeys()` | TRANSACTION·LOOKUP·VOLATILE PK와 TAG `NAME` 반환 |
| JDBC | `DatabaseMetaData.getPrimaryKeys()` | `KEY_SEQ`를 함께 반환 |
| machsql | `DESC`의 `[ PRIMARY KEY ]` 섹션 | PK 이름, 컬럼, key sequence 표시 |

Machbase 8.7.0에서 CMI 4.0.3 메타데이터를 협상한 경우 결과 컬럼 PK 플래그를 전달합니다.
CMI 4.0.2 이하에서는 기존 클라이언트 호환성을 위해 플래그를 전달하지 않습니다. Go
`database/sql`처럼 표준 결과 메타데이터에 PK API가 없는 인터페이스에서는 카탈로그 SQL 또는
해당 SDK의 전용 메타데이터 API를 사용합니다.

<a id="support-scope-sdk-generated-rowid"></a>

## SDK별 INSERT 결과 ROWID 지원

Machbase 8.7.0 Standard Edition에서 성공한 단일 `INSERT ... VALUES`는 입력된 행의 ROWID를
지원 SDK에 제공합니다.

| SDK 또는 도구 | 확인 방법 | ROWID가 없을 때 |
|---------------|-----------|-----------------|
| machsql | `SHOW LAST ROWID` 또는 `SHOW LASTID` | `NULL` |
| SQLCLI/ODBC | `SQLGetGeneratedRowID()` | `SQL_NO_DATA` |
| JDBC | `Statement.getGeneratedKeys()` | 빈 `ResultSet` |
| Python DB-API | `cursor.lastrowid` | `None` |
| .NET | `MachCommand.RowId` | `null` |
| Go `database/sql` | `Result.LastInsertId()` | 오류 |
| Go native | 미지원 | - |
| Node.js | 실행 결과의 `rowId` | 속성 없음 |
| REST API | 미지원 | - |

batch, `executemany()`, Append, loader, `INSERT ... SELECT`, UPSERT에서는 단일 ROWID를
반환하지 않습니다. 테이블별 조회 조건, 64비트 타입과 유효 기간은
[ROWID와 INSERT 결과 ID](/dbms/application-integration/rowid-generated-id/)를 참고하십시오.


<a id="support-scope-sdk-append"></a>

## SDK별 APPEND 지원 범위 안내

**Append API**는 여러 행을 묶어 입력하기 위한 전용 프로토콜입니다. 반복적인 단건
`INSERT`보다 네트워크와 문장 처리 오버헤드를 줄일 수 있으며, 시계열 데이터 수집에서
핵심적으로 사용됩니다.

### SDK별 Append API 지원 현황

| SDK | Append 지원 | API / 메서드 | 비고 |
|-----|:-----------:|--------------|------|
| **ODBC / CLI** | O | `SQLAppendOpen` / `SQLAppendData` / `SQLAppendClose` | 버퍼와 flush 직접 제어 |
| **JDBC** | O | `MachStatement` Append 메서드 | `executeAppendOpen` / `executeAppendData` / `executeAppendFlush` |
| **Python** | O | `conn.append(table, rows)` | `machbaseAPI` 패키지 |
| **.NET** | O | `MachCommand` + `MachAppendWriter` | `MachCommand.AppendOpen(tableName)` |
| **Go (native)** | O | `AppendWriter` | `conn.Appender(ctx, tableName)` |
| **Go (database/sql)** | △ | `machbase.Conn.Appender()` | 표준 `sql.DB`/`sql.Tx`에는 없으며 `sql.Conn.Raw()`에서 선택적으로 사용 |
| **Node.js** | O | `appendBatch` / `appendOpen` | LOG/TAG Append 지원 |
| **REST API** | O | `POST /machbase` | HTTP JSON Append |

- **O**: 완전 지원
- **X**: 미지원

### ODBC / CLI: Append 사용 예시

```c
#include <machbase_sqlcli.h>

SQLHSTMT stmt;
SQLAllocStmt(conn, &stmt);

// Append 세션 시작
SQLAppendOpen(stmt, "sensor_data", 0);

// 데이터 행 추가
SQL_APPEND_PARAM param[3];
// name, time(나노초), value 순으로 바인딩
param[0].mVarchar.mLength = strlen("sensor01");
strcpy(param[0].mVarchar.mData, "sensor01");
param[1].mDateTime.mTime = 1720000000000000000LL; // 나노초 타임스탬프
param[2].mDouble          = 25.3;

SQLAppendDataV2(stmt, param);

// Append 세션 종료 및 커밋
SQLAppendClose(stmt, NULL, NULL);
SQLFreeStmt(stmt, SQL_DROP);
```

### JDBC: MachStatement Append 사용 예시

```java
import java.sql.*;
import java.util.*;
import com.machbase.jdbc.MachStatement;

Connection conn = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER"
);
MachStatement stmt = (MachStatement) conn.createStatement();

// Append 세션 시작
ResultSet rs = stmt.executeAppendOpen("sensor_data", 100);
ResultSetMetaData rsmd = rs.getMetaData();

// 행 추가 (컬럼 순서대로 값 추가)
ArrayList<Object> row = new ArrayList<>();
row.add("sensor01");
row.add(System.currentTimeMillis() * 1_000_000L);
row.add(25.3);
stmt.executeAppendData(rsmd, row);

// pending 응답 확인 및 종료
stmt.executeAppendFlush();
stmt.executeAppendClose();
conn.close();
```

### Python: conn.append() 사용 예시

```python
from machbaseAPI import connect
from datetime import datetime

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

# 여러 행을 한 번에 Append
rows = [
    ['sensor01', datetime.now(), 25.3],
    ['sensor02', datetime.now(), 30.1],
    ['sensor03', datetime.now(), 18.7],
]
conn.append('sensor_data', rows)

conn.close()
```

### .NET: MachAppendWriter 사용 예시

```csharp
using System.Collections.Generic;
using Mach.Data.MachClient;

string connString = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
using var conn = new MachConnection(connString);
conn.Open();

using var appendCmd = new MachCommand(conn);
var writer = appendCmd.AppendOpen("sensor_data");

// 행 추가
var row = new List<object> { "sensor01", DateTime.UtcNow, 25.3 };
appendCmd.AppendData(writer, row);

// 완료
appendCmd.AppendFlush(writer);
appendCmd.AppendClose(writer);
```

### Go (native): Appender 사용 예시

```go
package main

import (
    "context"
    "log"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
)

func main() {
    ctx := context.Background()
    mdb, err := machgo.NewDatabase(&machgo.Config{
        Host: "127.0.0.1",
        Port: 5656,
    })
    if err != nil {
        log.Fatal(err)
    }

    conn, err := mdb.Connect(ctx, api.WithPassword("SYS", "MANAGER"))
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    appender, err := conn.Appender(ctx, "sensor_data")
    if err != nil {
        log.Fatal(err)
    }
    defer appender.Close()

    if err := appender.Append("sensor01", time.Now(), 25.3); err != nil {
        log.Fatal(err)
    }
}
```

### REST API: POST /machbase

REST API를 통한 Append는 JSON 본문에 테이블 이름과 행 배열을 전달합니다.

```bash
curl -X POST "http://localhost:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"sensor_data","values":[["sensor01",1720000000000000000,25.3],["sensor02",1720000000000000001,30.1]]}'
```

성공 시 Append 결과 건수가 반환됩니다.

```json
{
  "error_code": 0,
  "error_message": "",
  "append_success": 2,
  "append_failure": 0
}
```

### Append API 성능 특성

| 특성 | 설명 |
|------|------|
| **원자성** | TAG/LOG는 append 응답 단위, TRANSACTION batch는 statement transaction 단위 |
| **대상 테이블** | TAG, LOG와 지원되는 TRANSACTION client batch/stream 경로 |
| **배치 크기** | 1,000 ~ 10,000행 단위로 플러시하는 것을 권장 |
| **병렬 처리** | 여러 스레드에서 각각 독립적인 Appender 사용 가능 |
| **롤백** | 완료된 TAG/LOG Append는 롤백할 수 없음. TRANSACTION batch 실패는 해당 batch 롤백 |

> **참고**: TRANSACTION 테이블은 지원되는 client의 appendBatch 또는 append stream 경로를 사용합니다.
> TAG/LOG의 고속 append 버퍼와 내부 경로 및 처리량 특성이 다릅니다.

<a id="support-scope-sdk-auth-key"></a>

## SDK별 AUTH KEY 지원 범위 안내

Machbase는 사용자 이름/비밀번호 방식 외에 **AUTH KEY challenge 인증**을 지원합니다.
서버에는 사용자의 공개키를 등록하고, 클라이언트는 개인키 파일로 서버 challenge에
서명합니다. 비밀번호를 연결 문자열에 넣지 않고 키 기반으로 접속할 때 사용합니다.

### AUTH KEY 인증 방식 개요

1. 서버 사용자에 공개키를 AUTH KEY로 등록합니다.
2. 클라이언트가 `AUTH_MODE=CHALLENGE`로 연결을 요청합니다.
3. 서버가 challenge 값을 보냅니다.
4. 클라이언트가 `AUTH_KEY_FILE` 개인키로 challenge에 서명합니다.
5. 서버가 등록된 공개키로 서명을 검증하고 연결을 허용합니다.

지원되는 서명 방식은 `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`입니다. 키 파일만으로 방식을
추론할 수 있는 경우에는 `AUTH_SIG_SCHEME`을 생략할 수 있습니다.

### AUTH KEY 등록과 조회

사용자를 생성할 때 공개키를 함께 등록할 수 있습니다.

```text
CREATE USER app_auth_key
WITH AUTH KEY (
    KEY='-----BEGIN RSA PUBLIC KEY-----\n...\n-----END RSA PUBLIC KEY-----\n',
    VALID_BEFORE='2047-12-31',
    COMMENT='key only user'
);
```

기존 사용자에 AUTH KEY를 추가하는 것도 가능합니다.

```text
ALTER USER app_auth_key ADD AUTH KEY (
    KEY='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    VALID_BEFORE='2047-12-31',
    COMMENT='second key'
);
```

등록된 키는 `V$USER_AUTH_KEYS`에서 확인합니다.

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
FROM v$user_auth_keys
WHERE user_name = 'APP_AUTH_KEY'
ORDER BY key_id;
```

키를 비활성화, 활성화, 삭제할 때는 `key_id`를 지정합니다.

```text
ALTER USER app_auth_key DEACTIVATE AUTH KEY ID 3;
ALTER USER app_auth_key ACTIVATE AUTH KEY ID 3;
ALTER USER app_auth_key DROP AUTH KEY ID 3;
```

### SDK별 AUTH KEY 인증 지원 현황

| SDK | AUTH KEY 지원 | 설정 방법 |
|-----|:------------:|-----------|
| **machsql** | O | `-K <private-key-file>`, `--auth-sig-scheme` |
| **ODBC / CLI** | O | 연결 문자열 `AUTH_MODE`, `AUTH_KEY_FILE`, `AUTH_SIG_SCHEME` |
| **JDBC** | O | JDBC Properties 또는 URL 속성 |
| **Go / Python / Node.js / .NET** | X | 현재 드라이버 연결 옵션에 challenge 인증 설정 없음 |
| **REST API** | 별도 방식 | `HTTP_AUTH` 기반 Basic Authentication 설정 사용 |

### machsql 예제

```bash
cat > /tmp/auth_key_check.sql <<'SQL'
SELECT COUNT(*) FROM v$tables;
SQL

machsql -s 127.0.0.1 -P 5656 \
  -u app_auth_key \
  -K ./auth_ecdsa_p256.pem \
  --auth-sig-scheme=ECDSA \
  -i -f /tmp/auth_key_check.sql
```

RSA 키를 사용할 때는 서명 방식을 지정합니다.

```bash
machsql -s 127.0.0.1 -P 5656 \
  -u app_auth_key \
  -K ./auth_rsa_2048.pem \
  --auth-sig-scheme=RSA_PSS \
  -i -f /tmp/auth_key_check.sql
```

### ODBC / CLI 연결 문자열

```ini
SERVER=127.0.0.1;
UID=APP_AUTH_KEY;
CONNTYPE=1;
PORT_NO=5656;
NLS_USE=UTF8;
TIMEZONE=+0900;
AUTH_MODE=CHALLENGE;
AUTH_KEY_FILE=./auth_ecdsa_p256.pem;
AUTH_SIG_SCHEME=ECDSA;
```

`AUTH_MODE=CHALLENGE`를 지정하면 `AUTH_KEY_FILE`이 필수입니다. 잘못된 파일 경로,
키와 맞지 않는 `AUTH_SIG_SCHEME`, 등록되지 않은 사용자 키는 연결 실패로 처리됩니다.

### JDBC 예제

```java
Properties props = new Properties();
props.setProperty("user", "app_auth_key");
props.setProperty("AUTH_MODE", "CHALLENGE");
props.setProperty("AUTH_KEY_FILE", "/path/to/auth_ecdsa_p256.pem");
props.setProperty("AUTH_SIG_SCHEME", "ECDSA");

String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
Connection conn = DriverManager.getConnection(url, props);
```

키 알고리즘으로 서명 방식을 추론할 수 있으면 `AUTH_SIG_SCHEME`을 생략할 수
있습니다.

### REST API와 AUTH KEY

AUTH KEY challenge 인증은 DB 포트(기본 5656)에 접속하는 드라이버/CLI
인증 방식입니다. REST API(기본 5657)는 별도의 로그인 토큰 발급 엔드포인트나 Bearer
토큰 교환 방식으로 AUTH KEY를 처리하지 않습니다. REST API 인증은 `machbase.conf`의
`HTTP_AUTH` 설정에 따라 Basic Authentication을 사용합니다.

### 보안 권장 사항

1. 개인키 파일은 파일 권한을 제한하고 애플리케이션 설정 또는 시크릿 관리 도구로
   배포합니다.
2. 공개키는 사용자별로 등록하고, 사용하지 않는 키는 `DEACTIVATE` 또는 `DROP`합니다.
3. `VALID_BEFORE`를 설정해 키 만료 시점을 운영 정책에 맞게 관리합니다.
4. 네트워크 구간 보호가 필요한 환경에서는 TLS/SSL 터널 또는 보안 네트워크와 함께
   사용합니다.

<a id="support-scope-sdk-transaction-prepare-bind"></a>

## SDK별 transaction / prepare / bind 지원 범위 안내

각 SDK가 지원하는 트랜잭션, Prepared Statement, Parameter Binding 기능을 정리합니다.

> 서버 SQL 트랜잭션은 TRANSACTION 테이블에 적용됩니다. SDK 표준 편의 API의 구현 여부는 별도로
> 확인해야 합니다.

### 지원 범위 표

| SDK | Transaction API | Server Prepared | Parameter Binding | 이름 기반 API | 비고 |
|-----|:---:|:---:|:---:|:---:|------|
| **ODBC/CLI** | △ | O | O | △ | SQLCLI는 이름 API, ODBC는 ordinal API 사용 |
| **JDBC** | O | O | O | O | 표준 Connection 트랜잭션 API와 이름 기반 bind 지원 |
| **Python** | X | O | O | O | 2.4 prepared cursor로 호출 간 statement 재사용 |
| **.NET Connector** | X | X | O | △ | client-side typed literal 렌더링 후 ExecDirect |
| **Go (database/sql)** | O | O | O | O | `BeginTx`, `db.Prepare()`, `sql.Named()` 지원 |
| **Go (native client)** | △ | O | O | O | `BEGIN`/`COMMIT`/`ROLLBACK` SQL 직접 실행, `api.Named()` 지원 |
| **Node.js** | X | O | O | O | 배열은 positional, 객체는 named 입력 |
| **REST API** | X | X | X | X | 단일 요청 단위, 서버 파라미터 없음 |

- O: 지원
- △: SDK별로 제한된 방식으로 지원
- X: 미지원

표의 Transaction 열은 SDK가 제공하는 표준 편의 API 기준입니다. Go `database/sql`은
기본 isolation level의 `Begin`/`BeginTx`, `Commit`, `Rollback`을 제공합니다. Go native는
전용 `Begin` 메서드 대신 같은 연결에서 트랜잭션 SQL을 직접 실행합니다. JDBC는
`setAutoCommit(false)`, `commit()`과 `rollback()`을 제공합니다. ODBC/CLI처럼 임의 SQL을
같은 물리 연결로 계속 실행하는 SDK는 SQL `BEGIN`/`COMMIT`/`ROLLBACK`을 사용할 수 있지만,
연결 유지와 오류 처리를 애플리케이션이 책임져야 합니다.

### 트랜잭션 (Transaction)

JDBC의 표준 트랜잭션 API는 Standard Edition의 TRANSACTION 테이블 작업에 사용합니다.
`setAutoCommit(false)`는 즉시 `BEGIN`을 보내지 않고 첫 Statement 실행 시 트랜잭션을
시작합니다.

```java
conn.setAutoCommit(false);
try {
    stmt.executeUpdate("INSERT INTO orders VALUES (1, 50000)");
    stmt.executeUpdate("INSERT INTO orders VALUES (2, 30000)");
    conn.commit();
} catch (SQLException e) {
    conn.rollback();
    throw e;
}
```

독립 TAG DML은 JDBC manual transaction에 참여해 rollback할 수 있습니다. TRANSACTION
테이블을 변경하기 전의 첫 LOG DML은 호환 경로에서 auto-commit으로 재실행될 수 있어
rollback 대상이 아닙니다. TRANSACTION 테이블을 변경한 뒤에는 LOG/TAG DML과 DDL이
거절됩니다. 자세한 내용은
[JDBC 트랜잭션과 커넥션 풀](/dbms/development-tools-integration/jdbc/transaction-pooling/)을
참고합니다.

### Prepared Statement

반복 실행할 쿼리를 미리 파싱·컴파일하여 성능을 높입니다. SQL 인젝션 방지 효과도 있습니다.

Python `machbaseAPI` 2.4는 `cursor(prepared=True)`로 재사용 가능한 prepared cursor를
생성합니다. 동일한 원본 SQL 문자열을 사용하는 `execute()`와 `executemany()` 호출은
cursor가 보유한 server statement를 재사용합니다.

```python
# Python
cursor = conn.cursor(prepared=True)
sql = """
    INSERT INTO sensor_log (name, time, value)
    VALUES (:name, :time, :value)
"""
cursor.executemany(
    sql,
    [
        {"name": name, "time": ts, "value": val}
        for name, ts, val in data_list
    ],
)
```

prepared cursor는 cursor 하나당 server statement 하나를 유지합니다. 원본 SQL 문자열이
달라지면 기존 statement를 해제하고 새 SQL을 준비하며, 여러 SQL을 각각 유지하려면 SQL별
cursor를 생성합니다. 일반 cursor는 기존 동작을 유지합니다. 일반 cursor의 `%s`와
`%(name)s`는 클라이언트 렌더링 방식이지만 prepared cursor에서는 각각 `?`와 `:name`으로
변환하여 서버에 바인딩합니다.

```go
// Go database/sql
stmt, _ := db.Prepare("INSERT INTO sensor_log (name, time, value) VALUES (?, ?, ?)")
defer stmt.Close()
for _, row := range dataList {
    stmt.Exec(row.Name, row.Time, row.Value)
}
```

### Parameter Binding

파라미터 바인딩 시 DATETIME 타입은 **나노초 정수**로 전달하는 것을 권장합니다.

Machbase 8.7.0은 값 위치에 `:name` marker를 사용할 수 있습니다. 이름 API를 지원하는
JDBC, Node.js와 Python은 이름으로 값을 전달합니다. SQLCLI는
`SQLBindParameterByName()`을 제공하며, ODBC와 machsql은 `:name` SQL을 발생 순서의
ordinal로 바인딩합니다. .NET의 이름 컬렉션은 client-side 렌더링 방식입니다. 공통
문법과 SDK별 차이는
[Named Bind Parameter syntax](/dbms/reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/)를
참고하십시오.

```java
// JDBC - DATETIME 나노초 바인딩
PreparedStatement ps = conn.prepareStatement(
    "INSERT INTO sensor_log (name, time, value) VALUES (?, ?, ?)");
ps.setString(1, "sensor-01");
ps.setLong(2, System.currentTimeMillis() * 1_000_000L); // ms → ns
ps.setDouble(3, 23.5);
ps.executeUpdate();
```

```c
/* ODBC/CLI - SQLBindParameter */
SQLLEN nameLen = SQL_NTS;
SQLLEN timeInd = 0;
SQLLEN valueInd = 0;
char name[64] = "sensor-01";
SQLBIGINT time_ns = current_time_ns();
double value = 23.5;

SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR,
                 64, 0, name, 0, &nameLen);
SQLBindParameter(stmt, 2, SQL_PARAM_INPUT, SQL_C_SBIGINT, SQL_BIGINT,
                 0, 0, &time_ns, 0, &timeInd);
SQLBindParameter(stmt, 3, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_DOUBLE,
                 0, 0, &value, 0, &valueInd);
SQLExecute(stmt);
```

### NULL 처리

각 SDK에서 NULL 값을 바인딩하는 방법은 다음과 같습니다.

| SDK | NULL 바인딩 방법 |
|-----|----------------|
| JDBC | `ps.setNull(idx, java.sql.Types.INTEGER)` |
| Python | `:name` mapping 값에 `None` 전달 |
| .NET | `DBNull.Value` |
| Go | `sql.NullString{Valid: false}` 등 Null 타입 |
| ODBC/CLI | indicator를 `SQL_NULL_DATA`로 설정 |

상세 내용은 각 [드라이버별 가이드](/dbms/application-integration/guide-drivers/)를 참고합니다.

<a id="sdk"></a>

## 전체 SDK 기능 지원표

Machbase DBMS가 지원하는 SDK 목록과 기능별 지원 범위를 안내합니다. 각 SDK의 상세 API
레퍼런스는 이 장의 SDK별 하위 페이지를 참고합니다.

### 지원 SDK 목록

| SDK | 언어 / 환경 | 연결 포트 | 상세 레퍼런스 |
|-----|------------|-----------|---------------|
| **ODBC / CLI** | C / C++ | TCP 5656 | 11장 개발 도구 연동 → ODBC/CLI |
| **JDBC** | Java | TCP 5656 | 11장 개발 도구 연동 → JDBC |
| **Python** | Python 3.7+ | TCP 5656 | 11장 개발 도구 연동 → Python |
| **.NET** | C# / VB.NET | TCP 5656 | 11장 개발 도구 연동 → .NET |
| **Go (native)** | Go 1.22+ | TCP 5656 | 11장 개발 도구 연동 → Go |
| **Go (database/sql)** | Go 1.22+ | TCP 5656 | 11장 개발 도구 연동 → Go |
| **Node.js** | JavaScript / TypeScript | TCP 5656 | 11장 개발 도구 연동 → Node.js |
| **REST API** | 언어 독립 (HTTP) | TCP 5657 | 18장 레퍼런스 → REST API |

### SDK 특성 요약

#### ODBC / CLI (C/C++)
네이티브 C 인터페이스로 가장 낮은 레이턴시와 최대 처리량을 제공합니다. 임베디드 시스템이나 성능이 중요한 데이터 수집 에이전트에 적합합니다.

- 표준 ODBC 인터페이스 준수
- Machbase 고유 APPEND 프로토콜 지원 (`SQLAppendOpen` / `SQLAppendData` / `SQLAppendClose`)
- 전체 기능 지원

#### JDBC (Java)
Java 8/JDBC 4.2 핵심 인터페이스를 구현하여 Spring JDBC, HikariCP와 MyBatis 등 Java
생태계 프레임워크에서 사용할 수 있습니다.

- HikariCP 등 커넥션 풀링 지원
- Standard Edition TRANSACTION 테이블의 표준 Connection 트랜잭션 API 지원
- `MachStatement.executeAppendOpen()` 계열 메서드를 통한 Append API 지원
- AUTH KEY challenge 인증 지원 (Machbase 8.5 이상)

#### Python
Python DB-API 2.0(PEP 249) 인터페이스를 제공합니다.

- `machbaseAPI` 패키지 사용
- Pandas DataFrame과 연계 가능
- Append API 지원

#### .NET (C#)
ADO.NET 인터페이스를 구현하여 .NET 애플리케이션에서 표준적으로 사용할 수 있습니다.

- `Mach.Data.MachClient` 네임스페이스
- `MachCommand.AppendOpen()`과 `MachAppendWriter`를 통한 Append API 지원
- Entity Framework 연동 가능

#### Go
두 가지 방식으로 사용할 수 있습니다.

- **Go native 드라이버**: Machbase 고유 기능(Append, 세밀한 연결 제어) 활용 가능
- **`database/sql` 인터페이스**: 표준 Go DB 추상화 레이어, 범용 ORM과 호환

#### Node.js
JavaScript / TypeScript 환경에서 사용합니다.

- Promise 기반 비동기 API
- `appendBatch` / `appendOpen`을 통한 LOG/TAG Append API 지원

#### REST API
HTTP 기반으로 언어·프레임워크에 독립적입니다. Machbase Neo의 HTTP 서버(포트 5657)에 직접 요청을 보냅니다.

- JSON 요청·응답
- `/machbase?q=<SQL>` (SQL 실행), `/machbase` POST (Append)
- 인증: `HTTP_AUTH` 활성화 시 Basic Authentication

### 기능별 지원 범위 상세

각 기능의 SDK별 지원 여부는 아래 페이지를 참고합니다.

- [APPEND API 지원 범위](#support-scope-sdk-append)
- [AUTH KEY 인증 지원](#support-scope-sdk-auth-key)
- [Transaction / Prepare / Bind 지원](#support-scope-sdk-transaction-prepare-bind)
- [Nullable 메타데이터 지원](#support-scope-sdk-nullable-metadata)
- [INSERT 결과 ROWID 지원](#support-scope-sdk-generated-rowid)

REST API는 [REST API 레퍼런스](../reference/rest-api/)에서 별도로 확인합니다.
