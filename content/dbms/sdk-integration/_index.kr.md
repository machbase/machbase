---
type: docs
title: '개발도구 및 라이브러리'
weight: 120
---

다양한 프로그래밍 언어 및 프로토콜을 사용하여 Machbase를 애플리케이션에 통합하세요. 이 섹션에서는 사용 가능한 모든 SDK, API 및 통합 방법을 다룹니다.

## 사용 가능한 SDK 및 API

### ODBC/CLI (C/C++)

최대 성능을 위한 네이티브 C/C++ API:
- 직접 데이터베이스 액세스
- 대량 로딩을 위한 APPEND 프로토콜
- 최저 지연 시간
- 전체 기능 지원

**사용 시점**: C/C++ 애플리케이션 구축, 최대 성능 필요

[전체 레퍼런스](cli-odbc/)

### JDBC (Java)

Java 애플리케이션을 위한 표준 JDBC 드라이버:
- 표준 JDBC 인터페이스
- 커넥션 풀링 지원
- Spring/Hibernate 호환
- APPEND API 지원

**사용 시점**: Java 애플리케이션 구축, 표준 JDBC 필요

[전체 레퍼런스](jdbc/)

### Python

Python 클라이언트 라이브러리:
- Pythonic API
- Pandas 통합
- 간단한 연결 관리
- 쉬운 데이터 가져오기/내보내기

**사용 시점**: 데이터 과학, 스크립팅, Python 애플리케이션

[전체 레퍼런스](python/)

### .NET (C#)

C# 애플리케이션을 위한 .NET 프로바이더:
- ADO.NET 호환
- 커넥션 풀링
- LINQ 지원
- Entity Framework 호환

**사용 시점**: .NET/C# 애플리케이션 구축

[전체 레퍼런스](dotnet/)

### REST API

웹 애플리케이션을 위한 HTTP 기반 API:
- 언어 독립적
- JSON 응답
- 쉬운 통합
- 웹 친화적

**사용 시점**: 웹 애플리케이션, 마이크로서비스, HTTP 전용 환경

[전체 레퍼런스](restful_api/)

## 빠른 시작 예제

### C/C++ (ODBC/CLI)

```c
#include "machbase_cli.h"

SQLHENV env;
SQLHDBC conn;
SQLHSTMT stmt;

// 연결
SQLAllocEnv(&env);
SQLAllocConnect(env, &conn);
SQLConnect(conn, "127.0.0.1", SQL_NTS, "SYS", SQL_NTS, "MANAGER", SQL_NTS);

// 쿼리
SQLAllocStmt(conn, &stmt);
SQLExecDirect(stmt, "SELECT * FROM sensors DURATION 1 HOUR", SQL_NTS);

// 정리
SQLFreeStmt(stmt, SQL_DROP);
SQLDisconnect(conn);
```

### Java (JDBC)

```java
Class.forName("com.machbase.jdbc.driver");
Connection conn = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/MACHBASE",
    "SYS", "MANAGER"
);

Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("SELECT * FROM sensors DURATION 1 HOUR");

while (rs.next()) {
    System.out.println(rs.getString("sensor_id"));
}
```

### Python

```python
import machbase

conn = machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')
cur = conn.cursor()

cur.execute("SELECT * FROM sensors DURATION 1 HOUR")
for row in cur.fetchall():
    print(row)

conn.close()
```

### C# (.NET)

```csharp
using Machbase.Data.MachbaseClient;

string connString = "Server=127.0.0.1;Port=5656;User Id=SYS;Password=MANAGER;";
MachConnection conn = new MachConnection(connString);
conn.Open();

MachCommand cmd = new MachCommand("SELECT * FROM sensors DURATION 1 HOUR", conn);
MachDataReader reader = cmd.ExecuteReader();

while (reader.Read()) {
    Console.WriteLine(reader.GetString(0));
}
```

### REST API (JavaScript)

```javascript
const response = await fetch('http://localhost:5654/machbase', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        sql: 'SELECT * FROM sensors DURATION 1 HOUR',
        format: 'json'
    })
});

const data = await response.json();
console.log(data);
```

## 통합 패턴

### 패턴 1: 실시간 데이터 수집

```python
# 센서 데이터 수집기
import machbase
import time

conn = machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')

while True:
    appender = conn.create_appender('sensors')

    for i in range(1000):
        sensor_id = f'sensor{i % 100:03d}'
        value = read_sensor(sensor_id)
        appender.append(sensor_id, time.time(), value)

    appender.close()
    time.sleep(10)
```

### 패턴 2: 대시보드 애플리케이션

```java
// 실시간 대시보드 백엔드
@RestController
public class DashboardController {
    @Autowired
    private DataSource dataSource;

    @GetMapping("/api/sensors/current")
    public List<SensorData> getCurrentData() {
        String sql = "SELECT * FROM sensors DURATION 5 MINUTE";
        return jdbcTemplate.query(sql, new SensorDataMapper());
    }
}
```

### 패턴 3: 배치 처리

```csharp
// 야간 배치 작업
public class BatchProcessor {
    public void ProcessDailyData() {
        using (var conn = new MachConnection(connString)) {
            conn.Open();

            var sql = @"
                SELECT sensor_id, AVG(value), MAX(value), MIN(value)
                FROM sensors
                WHERE _arrival_time >= SYSDATE - 1
                GROUP BY sensor_id
            ";

            var cmd = new MachCommand(sql, conn);
            var reader = cmd.ExecuteReader();

            while (reader.Read()) {
                ProcessSensorStats(reader);
            }
        }
    }
}
```

## 연결 관리

### 커넥션 풀링 (Java)

```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:machbase://127.0.0.1:5656/MACHBASE");
config.setUsername("SYS");
config.setPassword("MANAGER");
config.setMaximumPoolSize(20);
config.setMinimumIdle(5);

HikariDataSource pool = new HikariDataSource(config);
```

### 연결 재시도 (Python)

```python
def connect_with_retry(max_retries=3):
    for i in range(max_retries):
        try:
            return machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')
        except Exception as e:
            if i == max_retries - 1:
                raise
            time.sleep(1)
```

## 성능 팁

1. **대량 삽입에는 APPEND API 사용**
2. **커넥션 풀링 활성화**
3. **작업 배치화** (1000-10000행)
4. **Prepared Statement 재사용**
5. **리소스를 적절히 닫기**

## 프레임워크 통합

### Spring Boot (Java)

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:machbase://127.0.0.1:5656/MACHBASE
    username: SYS
    password: MANAGER
    driver-class-name: com.machbase.jdbc.driver
```

### Django (Python)

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'machbase_django',
        'NAME': 'MACHBASE',
        'USER': 'SYS',
        'PASSWORD': 'MANAGER',
        'HOST': '127.0.0.1',
        'PORT': '5656',
    }
}
```

## 보안 모범 사례

1. **자격 증명에는 환경 변수 사용**
2. **연결에 SSL/TLS 활성화**
3. **리포팅에는 읽기 전용 사용자 사용**
4. **연결 타임아웃 구현**
5. **입력 유효성 검사 및 살균**

## 문제 해결

### 연결 실패

```python
# 서버 상태 확인
import socket

try:
    sock = socket.socket()
    sock.connect(('127.0.0.1', 5656))
    print("Server is reachable")
except:
    print("Cannot connect to server")
```

### 성능 문제

- 대량 삽입에는 APPEND API 사용
- 커넥션 풀링 활성화
- 작업 배치화
- 네트워크 지연 확인

### 메모리 문제

- 결과 집합 크기 제한
- 서버측 커서 사용
- 데이터를 청크로 처리
- 리소스를 즉시 닫기

## 예제 애플리케이션

### 완전한 Python 애플리케이션

```python
#!/usr/bin/env python3
import machbase
import time
from datetime import datetime

class SensorMonitor:
    def __init__(self):
        self.conn = machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')

    def collect_data(self, sensor_id, value):
        appender = self.conn.create_appender('sensors')
        appender.append(sensor_id, datetime.now(), value)
        appender.close()

    def get_recent_data(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM sensors DURATION 1 HOUR")
        return cur.fetchall()

    def close(self):
        self.conn.close()

# 사용법
monitor = SensorMonitor()
monitor.collect_data('sensor01', 25.3)
data = monitor.get_recent_data()
monitor.close()
```

## 다음 단계

개발 환경에 맞는 SDK를 선택하세요:

- **C/C++**: [CLI/ODBC 레퍼런스](cli-odbc/)
- **Java**: [JDBC 레퍼런스](jdbc/)
- **Python**: [Python SDK 레퍼런스](python/)
- **.NET**: [.NET 레퍼런스](dotnet/)
- **Web/REST**: [REST API 레퍼런스](restful_api/)

## 관련 문서

- [일반 작업: 연결하기](../common-tasks/connecting/) - 연결 예제
- [일반 작업: 데이터 가져오기](../common-tasks/importing-data/) - 대량 로딩
- [튜토리얼](../tutorials/) - 실습 예제
