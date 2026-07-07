---
type: docs
title: '연결 문자열과 인증'
weight: 10
---

Machbase에 연결하기 위한 기본 정보와 각 드라이버별 연결 문자열 형식을 설명합니다.

## 기본 연결 정보

| 항목 | 기본값 | 설명 |
|------|--------|------|
| 호스트 | `127.0.0.1` | Machbase 서버 IP 또는 호스트명 |
| 포트 | `5656` | Machbase 클라이언트 접속 포트 (TCP) |
| 기본 사용자 | `SYS` | 관리자 계정 |
| 기본 비밀번호 | `MANAGER` | 관리자 계정 초기 비밀번호 |

> 운영 환경에서는 반드시 기본 비밀번호를 변경하고, 목적에 맞는 전용 계정을 생성해 사용하세요.

## 인증 방식

### 비밀번호 인증 (기본)

모든 드라이버에서 지원하는 기본 인증 방식입니다. 사용자 이름과 비밀번호를 연결 시 전달합니다.

### AUTH KEY 인증 (Machbase 8.0 이상)

비밀번호 대신 사전에 발급된 AUTH KEY를 사용하는 인증 방식입니다. 비밀번호를 소스코드나 설정 파일에 직접 기록하지 않아도 됩니다. JDBC, Python SDK, REST API에서 지원합니다.

AUTH KEY는 Machbase 관리자 콘솔 또는 SQL로 발급합니다.

```sql
-- AUTH KEY 발급 (관리자 권한 필요)
ALTER USER reporter ADD AUTH_KEY 'my-secret-key-string';
```

AUTH KEY를 사용한 연결은 드라이버별 설정이 다릅니다. 상세 방법은 14장 레퍼런스의 각 드라이버 문서를 참조하세요.

## 드라이버별 연결 문자열 예시

### JDBC

```java
// 기본 연결
String url = "jdbc:machbase://127.0.0.1:5656/MACHBASE";
Connection conn = DriverManager.getConnection(url, "SYS", "MANAGER");

// timezone 포함 연결
String url = "jdbc:machbase://127.0.0.1:5656/MACHBASE?timezone=Asia/Seoul";
Connection conn = DriverManager.getConnection(url, "SYS", "MANAGER");
```

### Python

```python
from machbaseAPI import connect

# 기본 연결
conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

# timezone 포함 연결
conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER',
               timezone='Asia/Seoul')
```

### ODBC (DSN 없이 직접 연결)

```c
// ODBC 연결 문자열 형식
// "SERVER=호스트;PORT_NO=포트;UID=사용자;PWD=비밀번호;PROTOCOL=버전"
char connStr[] = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";

SQLDriverConnect(conn, NULL, (SQLCHAR*)connStr, SQL_NTS,
                 NULL, 0, NULL, SQL_DRIVER_NOPROMPT);
```

### ODBC DSN 설정 (odbc.ini)

```ini
[machbase_dsn]
Driver      = /usr/local/machbase/lib/libmachbasecli_odbc.so
Server      = 127.0.0.1
Port        = 5656
User        = SYS
Password    = MANAGER
```

DSN 정의 후 연결:

```c
SQLConnect(conn,
           (SQLCHAR*)"machbase_dsn", SQL_NTS,
           (SQLCHAR*)"SYS", SQL_NTS,
           (SQLCHAR*)"MANAGER", SQL_NTS);
```

### .NET (MachClient)

```csharp
string connStr = "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;PROTOCOL=4.0-full";
MachConnection conn = new MachConnection(connStr);
conn.Open();
```

### Go

```go
import (
    "database/sql"
    _ "github.com/machbase/neo-gomach"
)

db, err := sql.Open("machbase", "SYS:MANAGER@127.0.0.1:5656/MACHBASE")
```

### REST API

REST API는 별도 드라이버 없이 HTTP로 연결합니다. 포트는 기본 `5657`입니다.

```bash
# 기본 인증 (비밀번호)
curl -u SYS:MANAGER \
     "http://127.0.0.1:5657/db/query?q=SELECT+1"

# AUTH KEY 인증
curl -H "Authorization: Bearer my-secret-key-string" \
     "http://127.0.0.1:5657/db/query?q=SELECT+1"
```

## Connection Pool 권장 설정

단발성 연결(연결 → 쿼리 → 해제)을 반복하면 연결 수립 비용이 누적되어 성능이 저하됩니다. 애플리케이션 서버에서는 connection pool을 사용하세요.

### HikariCP (Java)

```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:machbase://127.0.0.1:5656/MACHBASE");
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

### Python (SQLAlchemy + connection pool)

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

### 연결 유효성 검증

Long-running 애플리케이션에서는 pool 내 연결이 끊어질 수 있습니다. connection pool의 validation query를 설정하세요.

```java
// HikariCP: 연결 검증 쿼리 설정
config.setConnectionTestQuery("SELECT 1");
```

```python
# SQLAlchemy: pool_pre_ping으로 연결 유효성 자동 검증
engine = create_engine(url, pool_pre_ping=True)
```

## 보안 권장사항

비밀번호를 소스코드에 직접 기록하지 마세요. 환경 변수 또는 시크릿 관리 도구를 사용합니다.

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
String url = String.format("jdbc:machbase://%s:%s/MACHBASE",
    System.getenv("MACHBASE_HOST"),
    System.getenv("MACHBASE_PORT")
);
Connection conn = DriverManager.getConnection(url,
    System.getenv("MACHBASE_USER"),
    System.getenv("MACHBASE_PASSWORD")
);
```
