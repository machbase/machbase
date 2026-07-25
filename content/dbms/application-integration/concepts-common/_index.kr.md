---
type: docs
title: '11.2 공통 연동 개념'
weight: 20
toc: true
---
드라이버나 언어에 관계없이 공통으로 이해해야 할 연동 개념을 설명합니다. 여기서 다루는 내용을 먼저 파악해 두면 각 SDK 문서를 빠르게 이해할 수 있습니다.

## 이 섹션의 구성

| 문서 | 내용 |
|------|------|
| [연결 문자열과 인증](/dbms/application-integration/concepts-common/#connection-string-authentication) | HOST:PORT, SYS/MANAGER 기본 인증, AUTH KEY 방식, connection pool 권장 설정 |
| [타임존 연결 옵션](/dbms/application-integration/concepts-common/#timezone-connection) | UTC 내부 저장, 연결 시 timezone 설정, TO_CHAR/TO_DATE와 timezone, SYSDATE vs NOW |
| [Prepared statement](/dbms/application-integration/concepts-common/#prepared-statement) | SQL 인젝션 방지, 재사용 성능, TAG/LOG 테이블에서의 사용 |
| [Parameter binding](/dbms/application-integration/concepts-common/#parameter-binding) | 위치 바인딩(`?`), DATETIME nanosecond 처리, NULL 값, SDK별 바인딩 방법 |
| [트랜잭션 처리](/dbms/application-integration/concepts-common/#transaction) | TRANSACTION SQL 트랜잭션과 SDK별 제어 API 범위 |
| [Append API와 Batch INSERT](/dbms/application-integration/concepts-common/#append-api-batch) | TAG/LOG Append와 TRANSACTION batch Append의 차이 |
| [오류 처리와 재시도](/dbms/application-integration/concepts-common/#error-handling-retry) | 연결 오류 코드, exponential backoff, Append flush 실패, connection pool 격리 |

## 핵심 특성

연동 코드를 작성하기 전에 아래 세 가지를 반드시 숙지하십시오.

**테이블 타입에 따른 트랜잭션 지원 차이**

명시적 `BEGIN`/`COMMIT`/`ROLLBACK`은 TRANSACTION 테이블에서 동작합니다. TAG/LOG 입력과 TAG data
UPDATE는 TRANSACTION 테이블 트랜잭션에 참여하지 않습니다.

**시간 데이터는 내부적으로 UTC nanosecond**

모든 시간 데이터는 UTC 기준 nanosecond 정수로 저장됩니다. 연결 시 timezone을 설정하지 않으면 조회 결과가 UTC로 표시되므로, 배포 지역에 맞는 timezone을 연결 옵션에서 지정하십시오.

**대용량 입력에는 Append API 사용**

일반 INSERT를 반복하면 문장별 네트워크 왕복과 SQL 파싱 비용이 누적됩니다. 지속적인 대량 입력에는
여러 행을 버퍼링하는 Append API를 우선 검토합니다.


<a id="connection-string-authentication"></a>

## 연결 문자열과 인증

연결에 필요한 기본 정보와 드라이버별 연결 문자열 형식을 설명합니다.

### 기본 연결 정보

| 항목 | 기본값 | 설명 |
|------|--------|------|
| 호스트 | `127.0.0.1` | Machbase 서버 IP 또는 호스트명 |
| 포트 | `5656` | Machbase 클라이언트 접속 포트 (TCP) |
| 기본 사용자 | `SYS` | 관리자 계정 |
| 기본 비밀번호 | `MANAGER` | 관리자 계정 초기 비밀번호 |

> 운영 환경에서는 반드시 기본 비밀번호를 변경하고, 목적에 맞는 전용 계정을 생성해 사용하십시오.

### 인증 방식

#### 비밀번호 인증 (기본)

모든 드라이버에서 지원하는 기본 인증 방식입니다. 사용자 이름과 비밀번호를 연결 시 전달합니다.

#### AUTH KEY 인증 (Machbase 8.0 이상)

서버에 등록된 공개키와 클라이언트 개인키 파일로 challenge 인증을 수행합니다. 비밀번호를 소스코드나 설정 파일에 기록할 필요가 없습니다. machsql, ODBC/CLI, JDBC 등에서 사용할 수 있습니다.

AUTH KEY는 사용자 생성 또는 변경 SQL로 공개키를 등록합니다.

```text
CREATE USER reporter
WITH AUTH KEY (
    KEY='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    VALID_BEFORE='2047-12-31',
    COMMENT='reporter key'
);
```

AUTH KEY를 사용한 연결은 드라이버별 설정이 다릅니다. 자세한 설정은 [SDK별 AUTH KEY 지원 범위 안내](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-auth-key)를 참조하십시오.

### 드라이버별 연결 문자열 예시

#### JDBC

```java
// 기본 연결
String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
Connection conn = DriverManager.getConnection(url, "SYS", "MANAGER");

// timezone 포함 연결
String url = "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
Connection conn = DriverManager.getConnection(url, "SYS", "MANAGER");
```

#### Python

```python
from machbaseAPI import connect

# 기본 연결
conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

# timezone 포함 연결
conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER',
               timezone='Asia/Seoul')
```

#### ODBC (DSN 없이 직접 연결)

```c
// ODBC 연결 문자열 형식
// "SERVER=호스트;PORT_NO=포트;UID=사용자;PWD=비밀번호;PROTOCOL=버전"
char connStr[] = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";

SQLDriverConnect(conn, NULL, (SQLCHAR*)connStr, SQL_NTS,
                 NULL, 0, NULL, SQL_DRIVER_NOPROMPT);
```

#### ODBC DSN 설정 (odbc.ini)

```ini
[machbase_dsn]
Driver      = /usr/local/machbase/lib/libmachbaseodbc.so
SERVER      = 127.0.0.1
PORT_NO     = 5656
UID         = SYS
PWD         = MANAGER
```

DSN 정의 후 연결:

```c
SQLConnect(conn,
           (SQLCHAR*)"machbase_dsn", SQL_NTS,
           (SQLCHAR*)"SYS", SQL_NTS,
           (SQLCHAR*)"MANAGER", SQL_NTS);
```

#### .NET (MachClient)

```csharp
string connStr = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
MachConnection conn = new MachConnection(connStr);
conn.Open();
```

#### Go

```go
import (
    "database/sql"
    _ "github.com/machbase/neo-client"
)

db, err := sql.Open("machbase", "server=tcp://sys:manager@127.0.0.1:5656;fetch_rows=1000")
```

#### REST API

REST API는 별도 드라이버 없이 HTTP로 연결합니다. 포트는 기본 `5657`입니다.

```bash
# 인증 비활성화 기본 설정
curl -G "http://127.0.0.1:5657/machbase" \
     --data-urlencode "q=SELECT 1"

# HTTP_AUTH 활성화 시 Basic Authentication 사용
curl -u SYS:MANAGER \
     -G "http://127.0.0.1:5657/machbase" \
     --data-urlencode "q=SELECT 1"
```

### Connection Pool 권장 설정

단발성 연결을 반복하면 연결 수립 비용이 누적됩니다. 애플리케이션 서버에서는 반드시 connection pool을 사용하십시오.

#### HikariCP (Java)

```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
config.setUsername("SYS");
config.setPassword("MANAGER");

// 권장 pool 크기: CPU 코어 수 × 2 정도에서 시작
config.setMaximumPoolSize(20);
config.setMinimumIdle(5);

// Machbase는 idle 연결 유지에 비용이 적으므로 넉넉하게 설정 가능
config.setIdleTimeout(600000);       // 10분
config.setConnectionTimeout(30000);  // 30초
config.setMaxLifetime(1800000);      // 30분

HikariDataSource pool = new HikariDataSource(config);
```

#### Python (SQLAlchemy + connection pool)

```python
from sqlalchemy import create_engine

engine = create_engine(
    "machbase+machbaseAPI://SYS:MANAGER@127.0.0.1:5656/MACHBASE",
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800  # 30분마다 연결 갱신
)
```

#### 연결 유효성 검증

장시간 실행 애플리케이션에서는 pool 내 연결이 끊어질 수 있으므로 validation query를 설정합니다.

```java
// HikariCP: 연결 검증 쿼리 설정
config.setConnectionTestQuery("SELECT 1");
```

```python
# SQLAlchemy: pool_pre_ping으로 연결 유효성 자동 검증
engine = create_engine(url, pool_pre_ping=True)
```

### 보안 권장사항

비밀번호를 소스코드에 직접 기록하지 마십시오. 환경 변수나 시크릿 관리 도구를 사용합니다.

```python
import os
from machbaseAPI import connect

conn = connect(
    host=os.environ['MACHBASE_HOST'],
    port=int(os.environ.get('MACHBASE_PORT', '5656')),
    user=os.environ['MACHBASE_USER'],
    password=os.environ['MACHBASE_PASSWORD']
)
```

```java
// 환경 변수에서 연결 정보 읽기
String url = String.format("jdbc:machbase://%s:%s/machbasedb",
    System.getenv("MACHBASE_HOST"),
    System.getenv("MACHBASE_PORT")
);
Connection conn = DriverManager.getConnection(url,
    System.getenv("MACHBASE_USER"),
    System.getenv("MACHBASE_PASSWORD")
);
```

<a id="timezone-connection"></a>

## 타임존 연결 옵션

모든 시간 데이터는 내부적으로 UTC nanosecond 정수로 저장됩니다. 조회 시 표시할 timezone은 연결 옵션 또는 SQL 함수로 제어합니다.

### 내부 저장 방식

```
저장: UTC 기준 nanosecond 정수 (예: 1720000000000000000)
표시: 서버 또는 연결 timezone에 따라 변환
```

timezone 설정 없이 조회하면 서버 기본 timezone으로 표시됩니다. KST(UTC+9)처럼 특정 timezone으로 보려면 연결 시 지정하거나 애플리케이션에서 변환합니다.

### 연결 시 timezone 설정

#### JDBC

```java
// timezone 파라미터를 URL에 포함
String url = "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
Connection conn = DriverManager.getConnection(url, "SYS", "MANAGER");

// 또는 Properties 사용
Properties props = new Properties();
props.setProperty("user", "SYS");
props.setProperty("password", "MANAGER");
props.setProperty("TIMEZONE", "+0900");
Connection conn = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/machbasedb", props);
```

#### Python

```python
from machbaseAPI import connect

conn = connect(
    host='127.0.0.1',
    port=5656,
    user='SYS',
    password='MANAGER',
    timezone='Asia/Seoul'  # IANA timezone 이름
)
```

#### .NET (MachClient)

```csharp
string connStr = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;" +
                 "PROTOCOL=4.0-full;TIMEZONE=Asia/Seoul";
MachConnection conn = new MachConnection(connStr);
conn.Open();
```

#### ODBC

ODBC 연결 문자열에서 timezone을 설정할 수 있습니다. 드라이버별 옵션은 17장 레퍼런스를
확인하십시오.

```c
char connStr[] = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;"
                 "PROTOCOL=4.0-full;TIMEZONE=9";
// TIMEZONE 값: UTC offset (시간 단위), 예: KST = 9
```

### 쿼리에서 시간 문자열 처리

SQL에서는 `TO_CHAR`로 `DATETIME` 값을 문자열로 만들고, `TO_DATE`로 문자열을 `DATETIME` 값으로 변환합니다.

#### TO_CHAR로 포맷 지정

```sql
SELECT name,
       TO_CHAR(time, 'YYYY-MM-DD HH24:MI:SS') AS time_text,
       value
FROM tag_table
WHERE name = 'sensor_01'
LIMIT 10;
```

#### TO_DATE로 문자열 파싱

```sql
SELECT *
FROM tag_table
WHERE time >= TO_DATE('2024-07-03 09:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

#### 연결 timezone과 쿼리 timezone의 관계

`TO_CHAR`에서 timezone 인자를 생략하면 연결 timezone이 기본값으로 적용됩니다.

```sql
-- 연결 timezone이 Asia/Seoul일 때
SELECT TO_CHAR(time, 'YYYY-MM-DD HH24:MI:SS') FROM tag_table;
-- → KST로 표시됨

-- 연결 timezone이 UTC일 때
SELECT TO_CHAR(time, 'YYYY-MM-DD HH24:MI:SS') FROM tag_table;
-- → UTC로 표시됨
```

### SYSDATE vs NOW

현재 시각을 나타내는 두 가지 표현이 있습니다.

| 표현 | 반환값 | 용도 |
|------|--------|------|
| `SYSDATE` | 현재 시각 (UTC nanosecond) | WHERE 조건, 기본값 |
| `NOW` | 현재 시각 | `SYSDATE`와 동일 |

두 표현은 동일한 값을 반환하며, `SYSDATE`가 더 일반적입니다.

```sql
-- 최근 1시간 데이터 조회
SELECT * FROM tag_table WHERE time >= SYSDATE - 3600000000000;
-- 3600000000000 = 1시간을 nanosecond로 표현 (3600 * 10^9)

SELECT * FROM tag_table
WHERE name = 'sensor_01'
  AND time >= SYSDATE - 3600000000000;
```

#### SYSDATE 연산

SYSDATE에 nanosecond 정수를 더하거나 빼는 방식으로 시간 범위를 계산합니다.

```text
-- 1시간 전
SYSDATE - 3600000000000

-- 1일 전
SYSDATE - 86400000000000

-- 30분 후
SYSDATE + 1800000000000
```

자주 사용하는 nanosecond 변환값:

| 단위 | nanosecond |
|------|-----------|
| 1초 | `1,000,000,000` |
| 1분 | `60,000,000,000` |
| 1시간 | `3,600,000,000,000` |
| 1일 | `86,400,000,000,000` |

### timezone 설정 권장사항

- **서비스 단위로 통일**: 같은 서비스 내의 모든 클라이언트는 동일한 timezone으로 연결합니다. timezone이 섞이면 조회 결과가 혼란스러워집니다.
- **UTC 저장, 표시만 변환**: 내부 저장은 항상 UTC이므로, timezone 설정은 표시 형식에만 영향을 줍니다. 데이터 정합성에 영향을 주지 않습니다.
- **IANA timezone 이름 사용**: `Asia/Seoul`, `America/New_York` 등 IANA timezone 이름을 사용합니다. `+09:00` 형식의 offset은 일부 드라이버에서 지원하지 않을 수 있습니다.

<a id="prepared-statement"></a>

## Prepared statement

SQL 문을 먼저 파싱·컴파일한 뒤 파라미터만 바꿔 반복 실행하는 방식입니다. SQL 인젝션 방지와 반복 실행 성능 향상, 두 가지 이점을 동시에 얻을 수 있습니다.

### 왜 Prepared statement를 사용하는가

#### SQL 인젝션 방지

문자열을 직접 SQL에 연결하면 악의적인 입력값이 SQL 구조를 변경할 수 있습니다.

```python
# 위험한 코드: 문자열 직접 연결
sensor_id = "'; DROP TABLE tag_table; --"
sql = f"SELECT * FROM tag_table WHERE name = '{sensor_id}'"
# 실행되는 SQL: SELECT * FROM tag_table WHERE name = ''; DROP TABLE tag_table; --'
```

Prepared statement를 사용하면 파라미터 값은 항상 데이터로만 처리됩니다.

```python
# Python machbaseAPI: %s 파라미터 렌더링 사용
sql = "SELECT * FROM tag_table WHERE name = %s"
cur.execute(sql, ['sensor_id_value'])
```

#### 반복 실행 성능

같은 SQL을 반복 실행할 때 매번 파싱하는 비용을 줄입니다. 수집 루프에서 동일한 INSERT 문을 반복 실행하는 경우에 특히 효과적입니다.

```
일반 execute() × 1000번:
  SQL 파싱 × 1000 + 네트워크 × 1000

Prepared statement × 1000번:
  SQL 파싱 × 1 + 파라미터 전송 × 1000
```

### Machbase에서의 지원 범위

LOG, TAG, TRANSACTION 테이블 모두에서 Prepared statement를 지원합니다.

| 테이블 타입 | INSERT | SELECT |
|------------|--------|--------|
| LOG 테이블 | O | O |
| TAG 테이블 | O | O |
| TRANSACTION 테이블 | O | O |

Append API와는 별개로, Append는 전용 API 호출로 동작합니다. 대용량 입력에는 Append API를, 단건이나 소량 반복 입력에는 Prepared statement를 사용합니다.

### CTE 파라미터 바인딩

Standard Edition에서는 CTE 본문과 주 `SELECT`에 위치 바인드 매개변수를 사용할 수 있습니다.

```sql
WITH selected_data AS (
    SELECT device_id, time, value
    FROM sensor_data
    WHERE device_id = ?
)
SELECT device_id, time, value
FROM selected_data
WHERE value >= ?;
```

매개변수는 SQL 문에 나타나는 순서대로 바인드합니다. 참조하지 않는 CTE에 있는 매개변수도
문장의 매개변수로 등록되므로 반드시 값을 바인드해야 합니다. 같은 CTE를 여러 번
참조하더라도 CTE 본문의 매개변수 개수가 참조 횟수만큼 늘어나지는 않습니다.

전체 CTE 문법과 제한은
[WITH / CTE syntax](/dbms/reference/sql/syntax-dictionary-sql/cte-syntax/)를 참고하십시오.

### 예제

#### INSERT (Python)

Python `machbaseAPI`의 DB-API 스타일 커서는 서버 prepared statement가 아니라 `%s`
자리 표시자를 클라이언트에서 렌더링하는 방식입니다.

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

sql = "INSERT INTO tag_table (name, time, value) VALUES (%s, %s, %s)"

sensor_data = [
    ('sensor_01', 1720000000000000000, 23.5),
    ('sensor_01', 1720000001000000000, 23.7),
    ('sensor_02', 1720000000000000000, 18.2),
]

for row in sensor_data:
    cur.execute(sql, row)

cur.close()
conn.close()
```

#### SELECT (Python)

```python
cur.execute(
    "SELECT name, time, value FROM tag_table WHERE name = %s AND time >= %s",
    ['sensor_01', 1720000000000000000],
)

for row in cur.fetchall():
    print(row)
```

#### INSERT (Java)

```java
String sql = "INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)";
PreparedStatement pstmt = conn.prepareStatement(sql);

List<SensorData> dataList = getSensorData();

for (SensorData data : dataList) {
    pstmt.setString(1, data.getName());
    pstmt.setLong(2, data.getTimestampNano());
    pstmt.setDouble(3, data.getValue());
    pstmt.executeUpdate();
}

pstmt.close();
```

#### SELECT (Java)

```java
String sql = "SELECT name, time, value FROM tag_table WHERE name = ? AND time >= ?";
PreparedStatement pstmt = conn.prepareStatement(sql);

pstmt.setString(1, "sensor_01");
pstmt.setLong(2, 1720000000000000000L);

ResultSet rs = pstmt.executeQuery();
while (rs.next()) {
    String name  = rs.getString("name");
    long   ts    = rs.getLong("time");
    double value = rs.getDouble("value");
    System.out.printf("%s: %d -> %.2f%n", name, ts, value);
}

rs.close();
pstmt.close();
```

#### INSERT (ODBC/C)

```c
#include <machbase_sqlcli.h>

SQLHSTMT stmt;
SQLAllocStmt(conn, &stmt);

char* sql = "INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)";
SQLPrepare(stmt, (SQLCHAR*)sql, SQL_NTS);

// 파라미터 바인딩
char   name[64] = "sensor_01";
long   ts       = 1720000000000000000LL;
double value    = 23.5;

SQLLEN nameLen  = SQL_NTS;
SQLLEN tsLen    = 0;
SQLLEN valueLen = 0;

SQLBindParameter(stmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR,   SQL_VARCHAR,  63, 0, name,  0, &nameLen);
SQLBindParameter(stmt, 2, SQL_PARAM_INPUT, SQL_C_SBIGINT, SQL_BIGINT,  0,  0, &ts,   0, &tsLen);
SQLBindParameter(stmt, 3, SQL_PARAM_INPUT, SQL_C_DOUBLE, SQL_DOUBLE,   0,  0, &value, 0, &valueLen);

SQLExecute(stmt);
SQLFreeStmt(stmt, SQL_DROP);
```

### Prepared statement 재사용 시 주의사항

- `close()`를 너무 빨리 호출하지 마십시오. 반복 실행이 끝난 후 닫습니다.
- connection pool 환경에서는 connection이 반환될 때 statement도 함께 닫히는지 확인하십시오. statement leak은 서버 리소스를 소진시킵니다.
- TAG 테이블에 많은 양의 데이터를 입력할 때는 Prepared statement보다 [Append API](#append-api-batch)가 훨씬 효율적입니다.

파라미터 바인딩의 상세 방법(DATETIME 타입, NULL 처리 등)은 [Parameter binding](/dbms/application-integration/concepts-common/#parameter-binding)을 참조하십시오.

<a id="parameter-binding"></a>

## Parameter binding

SQL 문에 값을 안전하게 전달하는 메커니즘입니다. ODBC, JDBC, .NET, Go, Node.js 드라이버는 `?` 위치 바인딩을, Python `machbaseAPI`는 `%s` 또는 `%(name)s` 자리 표시자를 사용합니다.

### 위치 기반 바인딩 (Positional Binding)

대부분의 드라이버는 `?`를 파라미터 자리 표시자로 사용합니다.

```sql
INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)
--                                                 1  2  3 (위치 순서)
```

파라미터는 왼쪽부터 순서대로 1번이며, 각 드라이버에서 이 위치 순서에 따라 값을 바인딩합니다.

> Machbase 서버 프로토콜의 기본 바인딩은 위치 기반입니다. Python `machbaseAPI`의
> `%(name)s` 형식은 Python 클라이언트가 SQL 문자열을 렌더링하는 편의 기능입니다.

### DATETIME 타입 바인딩

시간 값은 내부적으로 **UTC 기준 nanosecond 정수**로 저장되며, 드라이버마다 바인딩 방식이 다릅니다.

#### 주의: nanosecond vs millisecond

Java의 `System.currentTimeMillis()`는 millisecond 단위입니다. Machbase에 nanosecond로 저장하려면 1,000,000을 곱해야 합니다.

```java
long nowNano = System.currentTimeMillis() * 1_000_000L;
pstmt.setLong(2, nowNano);
```

Python의 `time.time()`은 초(float) 단위입니다.

```python
import time
now_nano = int(time.time() * 1_000_000_000)
cur.execute(sql, ['sensor_01', now_nano, 23.5])
```

#### ODBC (C/C++)

ODBC에서는 `SQL_C_SBIGINT` 타입으로 nanosecond 정수를 바인딩하거나, `SQL_C_TYPE_TIMESTAMP` 구조체를 사용할 수 있습니다.

```c
// nanosecond 정수로 바인딩
long long ts_nano = 1720000000000000000LL;
SQLLEN indicator = 0;
SQLBindParameter(stmt, 2, SQL_PARAM_INPUT,
                 SQL_C_SBIGINT, SQL_BIGINT,
                 0, 0, &ts_nano, 0, &indicator);
```

#### JDBC

JDBC에서는 `setLong()`으로 nanosecond 정수를 직접 바인딩하거나, `setTimestamp()`로 `java.sql.Timestamp`를 사용할 수 있습니다. `setTimestamp()`는 millisecond 해상도이므로 nanosecond 정밀도가 필요하면 `setLong()`을 사용하십시오.

```java
// nanosecond 정수로 바인딩 (권장: 정밀도 손실 없음)
pstmt.setLong(2, 1720000000123456789L);

// Timestamp로 바인딩 (millisecond 해상도)
pstmt.setTimestamp(2, new java.sql.Timestamp(1720000000123L));
```

#### Python

```python
import time

# nanosecond 정수 (권장)
now_ns = int(time.time_ns())  # Python 3.7+
cur.execute("INSERT INTO tag_table VALUES (%s, %s, %s)", ['sensor_01', now_ns, 23.5])

# datetime 객체 사용 (microsecond 해상도)
from datetime import datetime, timezone
now = datetime.now(timezone.utc)
cur.execute("INSERT INTO tag_table VALUES (%s, %s, %s)", ['sensor_01', now, 23.5])
```

### NULL 값 처리

#### Python

Python DB-API 스타일 커서는 `%s` 자리 표시자에 `None`을 전달하면 SQL `NULL`로
렌더링합니다. 타입별 NULL 조회 표현은 Machbase 타입 규칙을 따르므로, 애플리케이션에서
필요한 컬럼 타입별 결과를 확인합니다.

```python
# value 컬럼에 NULL 삽입
cur.execute("INSERT INTO tag_table (name, time, value) VALUES (%s, %s, %s)",
            ['sensor_01', now_ns, None])
```

#### Java

Java에서는 `setNull()` 메서드를 사용합니다.

```java
pstmt.setNull(3, java.sql.Types.DOUBLE);
```

또는 `setObject()`에 `null`을 전달합니다.

```java
pstmt.setObject(3, null);
```

#### ODBC (C/C++)

ODBC에서는 indicator 변수를 `SQL_NULL_DATA`로 설정합니다.

```c
SQLLEN indicator = SQL_NULL_DATA;
SQLBindParameter(stmt, 3, SQL_PARAM_INPUT,
                 SQL_C_DOUBLE, SQL_DOUBLE,
                 0, 0, NULL, 0, &indicator);
```

#### .NET (C#)

```csharp
// DBNull.Value로 NULL 표현
cmd.Parameters.AddWithValue("@value", DBNull.Value);
```

### SDK별 바인딩 메서드 요약

#### ODBC (SQLBindParameter)

```c
// 문자열
SQLBindParameter(stmt, 1, SQL_PARAM_INPUT,
                 SQL_C_CHAR, SQL_VARCHAR, 63, 0,
                 name_buf, 0, &name_len);

// 정수
SQLBindParameter(stmt, 2, SQL_PARAM_INPUT,
                 SQL_C_SBIGINT, SQL_BIGINT, 0, 0,
                 &int_val, 0, &indicator);

// 실수
SQLBindParameter(stmt, 3, SQL_PARAM_INPUT,
                 SQL_C_DOUBLE, SQL_DOUBLE, 0, 0,
                 &double_val, 0, &indicator);
```

#### JDBC (setXxx 메서드)

```java
pstmt.setString(1, "sensor_01");     // VARCHAR, CHAR
pstmt.setLong(2, tsNano);            // DATETIME (nanosecond), BIGINT
pstmt.setInt(3, 42);                 // INTEGER
pstmt.setDouble(4, 23.5);           // DOUBLE
pstmt.setFloat(5, 23.5f);           // FLOAT
pstmt.setShort(6, (short)10);       // SMALLINT
```

#### Python (`%s` 또는 `%(name)s`)

```python
# 위치 파라미터는 %s를 사용합니다.
cur.execute(
    "INSERT INTO tag_table (name, time, value) VALUES (%s, %s, %s)",
    ['sensor_01', now_ns, 23.5]
)

# 이름 파라미터는 %(name)s를 사용합니다.
cur.execute(
    "INSERT INTO tag_table (name, time, value) "
    "VALUES (%(name)s, %(time)s, %(value)s)",
    {"name": "sensor_01", "time": now_ns, "value": 23.5}
)
```

#### .NET (MachCommand.Parameters)

```csharp
MachCommand cmd = new MachCommand(
    "INSERT INTO tag_table (name, time, value) VALUES (?, ?, ?)", conn);

cmd.Parameters.Add(new MachParameter { Value = "sensor_01" });
cmd.Parameters.Add(new MachParameter { Value = 1720000000000000000L });
cmd.Parameters.Add(new MachParameter { Value = 23.5 });

cmd.ExecuteNonQuery();
```

### 타입 변환 주의사항

타입 불일치 시 암묵적 변환을 시도하지만 정밀도 손실이 발생할 수 있습니다. 특히 다음 경우에 주의하십시오.

| 상황 | 권장 처리 |
|------|-----------|
| DATETIME 바인딩 | nanosecond 정수(`BIGINT`)로 바인딩 |
| VARCHAR → BIGINT 자동 변환 | 명시적으로 올바른 타입을 사용할 것 |
| DOUBLE → FLOAT 바인딩 | 정밀도 손실 가능, DOUBLE로 바인딩 권장 |

타임존 관련 처리는 [타임존 연결 옵션](/dbms/application-integration/concepts-common/#timezone-connection)을 참조하십시오.

<a id="transaction"></a>

## 트랜잭션 처리 (TRANSACTION 및 SDK별 지원 범위 분리)

테이블 유형에 따라 트랜잭션 지원 범위가 다릅니다. 애플리케이션 설계 시 반드시 확인하십시오.

### 테이블 유형별 트랜잭션 지원

| 테이블 유형 | 트랜잭션 | COMMIT/ROLLBACK | 이유 |
|-----------|:---:|:---:|------|
| **TRANSACTION** | O | O | `BEGIN` 이후 TRANSACTION DML을 커밋하거나 롤백 |
| **VOLATILE** | X | X | 각 DML 문 단위로 반영 |
| **LOOKUP** | X | X | 각 DML 문 단위로 반영 |
| **TAG** | X | X | 입력과 제한적 data UPDATE를 문 단위로 반영 |
| **LOG** | X | X | append 중심 입력을 문 단위로 반영 |

> 활성 TRANSACTION 테이블 트랜잭션 안에서는 LOG, TAG, LOOKUP, VOLATILE 테이블 쓰기와 DDL이 차단됩니다.
> 여러 테이블 타입의 쓰기를 하나의 트랜잭션으로 묶을 수 없습니다.

### Autocommit 동작

서버 SQL에서는 plain `BEGIN`, `COMMIT`, `ROLLBACK`을 사용합니다. `BEGIN TRANSACTION` 같은 별도 구문은
지원하지 않습니다. SDK의 표준 트랜잭션 편의 API가 이 SQL 흐름을 모두 구현한 것은 아니므로,
아래 지원 표와 각 드라이버 레퍼런스를 함께 확인합니다.

```java
// JDBC: 서버 SQL로 트랜잭션 시작 및 종료
Connection conn = DriverManager.getConnection(url, props);
Statement tx = conn.createStatement();
tx.execute("BEGIN");

try {
    PreparedStatement ps = conn.prepareStatement(
        "INSERT INTO orders (order_id, amount) VALUES (?, ?)");
    ps.setInt(1, 1001);
    ps.setDouble(2, 50000.0);
    ps.executeUpdate();

    ps.setInt(1, 1002);
    ps.setDouble(2, 30000.0);
    ps.executeUpdate();

    tx.execute("COMMIT");
} catch (SQLException e) {
    tx.execute("ROLLBACK");
    throw e;
}
```

```c
/* C/CLI: 트랜잭션 제어 */
SQLExecDirect(stmt, (SQLCHAR *)"BEGIN", SQL_NTS);

/* INSERT 작업 */
SQLExecDirect(stmt, "INSERT INTO orders VALUES (1001, 50000)", SQL_NTS);
SQLExecDirect(stmt, "INSERT INTO orders VALUES (1002, 30000)", SQL_NTS);

/* 커밋 또는 롤백 */
SQLEndTran(SQL_HANDLE_DBC, conn, SQL_COMMIT);
/* 오류 시: SQLEndTran(SQL_HANDLE_DBC, conn, SQL_ROLLBACK); */
```

### TAG/LOG 테이블에 대한 트랜잭션 시도

트랜잭션 밖에서 실행한 TAG/LOG 입력은 해당 문 또는 Append 요청 단위로 반영되며 이후
`ROLLBACK`으로 취소할 수 없습니다. `BEGIN`은 TRANSACTION 테이블 트랜잭션을 시작하므로, 그 안에서
TAG/LOG 쓰기를 실행하면 해당 쓰기가 차단됩니다.

```text
-- TAG INSERT가 활성 TRANSACTION 테이블 트랜잭션 안에서 거부됩니다.
BEGIN;
INSERT INTO sensor_tag (name, time, value) VALUES ('s01', NOW, 25.0);
ROLLBACK;
```

TAG/LOG 테이블에서 잘못 삽입된 데이터를 제거하려면 [DELETE 정책](/dbms/data-modeling-table-design/alter-data-mutation-policy/#policy-delete)을 참고하십시오.

### SDK별 트랜잭션 지원 요약

| SDK | 트랜잭션 편의 API | 비고 |
|-----|:---:|------|
| ODBC/CLI | △ | SQL로 `BEGIN`, `SQLEndTran`으로 종료 가능 |
| JDBC | △ | SQL로 `BEGIN` 실행 필요. `setAutoCommit(false)`는 시작 문을 보내지 않음 |
| Python | X | `begin()`/`commit()`/`rollback()`이 `NotSupportedError` 반환 |
| .NET | X | `MachTransaction` 미구현 |
| Go (database/sql) | X | 현재 Go SQL 드라이버는 `Begin` / `BeginTx` 미지원 |
| Go (native client) | X | Append-only API 중심 |
| Node.js | X | transaction 편의 API 미지원 |
| REST API | X | 단일 요청 단위 처리 |

`X`는 해당 SDK의 표준 트랜잭션 편의 API가 구현되지 않았다는 의미입니다. 같은 물리 연결에서
임의 SQL을 연속 실행할 수 있는 SDK는 Node.js 예제처럼 `BEGIN`/`COMMIT`/`ROLLBACK`을 직접
전송할 수 있습니다. 연결 풀이나 요청마다 연결이 바뀌는 API에서는 이 방식을 사용하지 않습니다.

상세 SDK별 지원 범위는 [SDK별 transaction/prepare/bind 지원 범위](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-transaction-prepare-bind)를 참고하십시오.

<a id="append-api-batch"></a>

## Append API와 Batch API

데이터 입력 방법은 크게 세 가지이며, 각각의 특성과 적합한 상황이 다릅니다.

### 세 가지 입력 방법 비교

| 방법 | 트랜잭션 | 처리 방식 | 권장 사용량 |
|------|----------|-----------|-------------|
| **단건 INSERT** | 지원 (TRANSACTION) | 행 단위 즉시 처리 | 건별 처리, 낮은 빈도 |
| **Batch INSERT** | 지원 (TRANSACTION) | 여러 행을 한 번에 전송 | 수십~수백 건 묶음 처리 |
| **Append API** | 테이블 타입별 상이 | 전용 Append 세션/요청으로 묶음 전송 | 연속 수집·배치 적재 |

### Append API

#### 동작 원리

일반 SQL INSERT 대신 Append 전용 세션으로 행 데이터를 전송합니다. 내부 버퍼링, pending 응답 확인, 오류 확인 시점은 드라이버마다 다르므로 `flush`와 `close`의 정확한 의미는 각 드라이버 문서를 함께 확인하십시오.

```
애플리케이션
  ↓ AppendOpen / appendBatch / POST /machbase
Append 전용 프로토콜 또는 요청
  ↓ flush / close / 응답 확인
Machbase 서버
```

여러 행을 묶어 보내므로 반복적인 단건 INSERT보다 네트워크와 문장 처리 오버헤드를 줄일 수
있습니다. 실제 처리량은 SDK, row 크기, 인덱스와 constraint 구성에 따라 달라집니다.

#### 주요 특성

- **TAG/LOG**: append 최적화 입력 경로를 사용하며, 이미 성공한 행을 TRANSACTION 테이블 트랜잭션으로
  롤백할 수 없습니다.
- **TRANSACTION**: Append open/close와 batch 입력을 지원합니다. TRANSACTION batch는 statement transaction으로
  처리되므로 batch 중 constraint 오류가 발생하면 해당 batch 전체를 롤백합니다.
- **순서 보장 없음**: flush 단위 내에서 행 삽입 순서는 보장되지 않습니다.
- **드라이버별 flush 의미**: 일부 드라이버는 미전송 데이터를 전송하고, 일부 드라이버는 이미 보낸 Append 데이터의 pending 응답을 확인합니다.
- **명시적 종료 권장**: 애플리케이션 종료 전, 또는 일정 주기마다 드라이버가 제공하는 `flush`/`close` 절차를 호출하십시오.

#### SDK별 Append API 지원 현황

| SDK | 지원 여부 | 비고 |
|-----|-----------|------|
| CLI/ODBC | O | `SQLAppendOpen`, `SQLAppendData`, `SQLAppendFlush` |
| JDBC | O | `MachStatement.executeAppendOpen`, `executeAppendData`, `executeAppendFlush` |
| Python SDK | O | `conn.append(table, rows)` |
| .NET (MachClient) | O | `MachCommand.AppendOpen`, `AppendData`, `AppendFlush` |
| Go 드라이버 | O | `Appender` 인터페이스 |
| Node.js 드라이버 | O | `appendBatch`, `appendOpen` |
| REST API | O | `POST /machbase` |

상세 API는 17장 레퍼런스의 각 드라이버 문서를 참조하십시오.

#### 언제 Append API를 써야 하는가

아래 조건 중 하나라도 해당하면 Append API를 우선 검토합니다.

- 지속적인 데이터 수집으로 반복 INSERT의 왕복과 파싱 비용이 누적되는 경우
- 센서, 장비, IoT 디바이스에서 연속적으로 데이터가 수집되는 경우
- 쓰기 성능이 병목이 되어 애플리케이션 전체 처리량이 저하되는 경우

반대로 다음 경우에는 일반 INSERT를 검토합니다.

- 입력 빈도가 낮고 각 문장의 결과를 즉시 확인해야 하는 경우
- 여러 TRANSACTION DML을 명시적 트랜잭션으로 묶어야 하는 경우
- 에러 발생 시 어느 행에서 실패했는지 정확히 추적해야 하는 경우

#### Append API 사용 예 (Python)

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

# rows: 각 요소가 테이블 컬럼 순서에 맞는 리스트
rows = [
    ['sensor_01', 1720000000000000000, 23.5],
    ['sensor_01', 1720000001000000000, 23.7],
    ['sensor_02', 1720000000000000000, 18.2],
]

# append() 호출 시 즉시 flush
conn.append('tag_table', rows)
conn.close()
```

#### Append API 사용 예 (Java)

```java
import java.sql.*;
import java.util.*;
import com.machbase.jdbc.MachStatement;

String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
Connection conn = DriverManager.getConnection(url, "SYS", "MANAGER");
MachStatement stmt = (MachStatement) conn.createStatement();

// Append 세션 열기
ResultSet rs = stmt.executeAppendOpen("tag_table", 100);
ResultSetMetaData rsmd = rs.getMetaData();

// 행 단위로 버퍼에 추가
ArrayList<Object> row = new ArrayList<>();
row.add("sensor_01");
row.add(1720000000000000000L);
row.add(23.5);
stmt.executeAppendData(rsmd, row);

// 명시적 flush
stmt.executeAppendFlush();

// Append 세션 닫기 (내부적으로 flush 포함)
stmt.executeAppendClose();
conn.close();
```

### Batch INSERT

#### 동작 원리

Prepared statement의 파라미터를 바꾸어 여러 행을 입력합니다. TRANSACTION 테이블에서 전체 성공 또는 전체
실패가 필요하면 서버 SQL 트랜잭션을 명시적으로 시작하거나, batch 원자성을 보장하는 TRANSACTION
Append batch를 사용합니다. SDK의 `executeBatch`/`executemany`가 자동으로 명시적
트랜잭션을 시작한다고 가정하지 않습니다.

#### 언제 Batch INSERT를 사용하는가

- TRANSACTION 테이블에 여러 행을 원자적으로 삽입해야 할 때
- 데이터 마이그레이션 또는 ETL 처리에서 수십~수백 건을 묶어 처리할 때
- 실패 시 rollback이 필요한 경우

#### Batch INSERT 사용 예 (Java)

```java
try (Statement tx = conn.createStatement()) {
    tx.execute("BEGIN");
}

String sql = "INSERT INTO rdb_table (id, value, ts) VALUES (?, ?, ?)";
PreparedStatement pstmt = conn.prepareStatement(sql);

for (DataRow row : dataList) {
    pstmt.setString(1, row.getId());
    pstmt.setDouble(2, row.getValue());
    pstmt.setTimestamp(3, row.getTimestamp());
    pstmt.addBatch();  // 배치에 추가
}

pstmt.executeBatch();  // 한 번에 전송
try (Statement tx = conn.createStatement()) {
    tx.execute("COMMIT");
}

pstmt.close();
```

### 요약: 입력 방법 선택 기준

```
지속적인 TAG/LOG 대량 입력
  → Append API

TRANSACTION 여러 문 트랜잭션 필요
  → BEGIN/COMMIT을 지원하는 SQL/SDK 경로

TRANSACTION 여러 행 묶음 입력
  → TRANSACTION Append batch 또는 검증된 SDK batch 경로

단건, 낮은 빈도, 간단한 작업
  → 단건 INSERT
```

<a id="error-handling-retry"></a>

## 오류 처리와 재시도

연결 오류, 쿼리 오류, Append 실패는 각각 다른 전략으로 처리해야 합니다.

### 오류 유형별 분류

| 유형 | 대표 오류 | 재시도 가능 여부 |
|------|-----------|:---:|
| 연결 실패 | Connection refused, timeout | O |
| 인증 실패 | Wrong password, invalid key | X |
| 쿼리 오류 | Syntax error, column not found | X |
| 리소스 부족 | Out of memory, disk full | 상황에 따라 |
| 네트워크 단절 | Connection reset | O |
| Append flush 실패 | Network error during flush | O |

### 연결 오류와 재시도

네트워크 문제나 서버 재시작으로 연결이 실패할 수 있습니다. **지수 백오프(exponential backoff)** 전략으로 재시도합니다.

```python
import time
import machbaseapi

def connect_with_retry(host, port, user, password, max_attempts=5):
    delay = 1.0  # 초기 대기 시간 (초)
    for attempt in range(1, max_attempts + 1):
        try:
            conn = machbaseapi.connect(host, port, user, password)
            return conn
        except Exception as e:
            if attempt == max_attempts:
                raise
            print(f"연결 실패 (시도 {attempt}/{max_attempts}): {e}")
            time.sleep(delay)
            delay = min(delay * 2, 30)  # 최대 30초
    return None
```

```java
// Java JDBC 재시도 예제
int maxAttempts = 5;
long delay = 1000; // ms
for (int i = 1; i <= maxAttempts; i++) {
    try {
        conn = DriverManager.getConnection(url, props);
        break;
    } catch (SQLException e) {
        if (i == maxAttempts) throw e;
        Thread.sleep(delay);
        delay = Math.min(delay * 2, 30000);
    }
}
```

### 쿼리 오류 처리

쿼리 오류는 재시도해도 결과가 같으므로 **로그를 남기고 상위 레이어에 전파**합니다.

```python
cursor = conn.cursor()
try:
    cursor.execute("INSERT INTO sensor_log (name, time, value) VALUES (%s, %s, %s)",
                   ['sensor-01', time_ns, 23.5])
except Exception as e:
    # 오류 코드 확인 후 처리
    print(f"쿼리 오류: {e}")
    raise
finally:
    cursor.close()
```

### Append API 오류 처리

Append API는 버퍼에 누적 후 flush 시점에 오류가 발생합니다. flush 실패 시 재시도 또는 대체 INSERT로 전환합니다.

```python
try:
    appended = conn.append('SENSOR_LOG', data_batch)
    print(f"Append rows: {appended}")
except Exception as e:
    print(f"Append 오류: {e}")
    # flush 실패 시 누적된 데이터를 INSERT로 재시도
    fallback_insert(conn, data_batch)
```

```c
/* C/CLI Append 오류 처리 */
if (SQLAppendFlush(stmt) != SQL_SUCCESS) {
    char err_msg[1024];
    SQLError(env, conn, stmt, NULL, NULL, err_msg, sizeof(err_msg), NULL);
    fprintf(stderr, "Flush 오류: %s\n", err_msg);
    /* 재연결 후 재시도 */
    reconnect_and_retry();
}
```

### Connection Pool 사용 시 오류 격리

오류가 발생한 연결은 pool에서 제거하고 새 연결로 교체합니다.

```java
// HikariCP 설정 예시
HikariConfig config = new HikariConfig();
config.setConnectionTimeout(5000);      // 연결 획득 대기 최대 5초
config.setValidationTimeout(2000);      // 연결 유효성 검사 최대 2초
config.setConnectionTestQuery("SELECT 1 FROM v$version"); // 연결 상태 확인
config.setMaximumPoolSize(10);
```

### 주의사항

- **TAG/LOG 테이블** INSERT/Append는 트랜잭션이 없으므로 부분 실패 가능성 고려
- **인증 실패**는 재시도 전에 자격 증명을 확인 (재시도 반복 시 계정 잠금 가능성)
- 재시도 횟수에 상한을 두고, 최종 실패 시 알림을 발송하는 구조 권장
