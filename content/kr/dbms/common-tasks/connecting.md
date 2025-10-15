---
type: docs
title: 'Machbase 연결하기'
weight: 10
---

명령줄 클라이언트부터 프로그래밍 API까지 Machbase에 연결하는 모든 방법을 학습합니다. 이 가이드는 연결 방법, 구성 및 모범 사례를 다룹니다.

## 연결 방법 개요

| 방법 | 최적 용도 | 언어 | 복잡도 |
|--------|----------|----------|------------|
| machsql | 대화형 쿼리, 테스트 | CLI | 쉬움 |
| ODBC/CLI | C/C++ 애플리케이션 | C/C++ | 중간 |
| JDBC | Java 애플리케이션 | Java | 쉬움 |
| Python | Python 애플리케이션 | Python | 쉬움 |
| REST API | HTTP/웹 애플리케이션 | 모든 언어 | 쉬움 |
| .NET | C# 애플리케이션 | C# | 쉬움 |

## machsql (명령줄 클라이언트)

### 기본 연결

```bash
# 대화형 연결
machsql

# 다음 항목을 입력하라는 메시지가 표시됩니다:
# - 서버 주소 (기본값: 127.0.0.1)
# - 사용자 ID (기본값: SYS)
# - 비밀번호 (기본값: MANAGER)
```

### 매개변수를 사용한 연결

```bash
# 모든 매개변수 지정
machsql -s localhost -u SYS -p MANAGER

# 원격 서버
machsql -s 192.168.1.100 -u analyst -p mypassword

# 사용자 정의 포트
machsql -s localhost -P 7878 -u SYS -p MANAGER

# 특정 데이터베이스
machsql -s localhost -u SYS -p MANAGER -d MYDB
```

### 일반 옵션

```bash
# SQL 스크립트 실행
machsql -f script.sql

# 파일로 출력
machsql -o output.txt

# 자동 모드 (배너 없음)
machsql -i

# CSV 출력 형식
machsql -r csv -o results.csv

# 시간대 설정
machsql -z +0900  # 한국 시간대
```

### 연결 문자열

```bash
# 전체 연결 문자열
machsql -s 192.168.1.100 -P 5656 -u analyst -p password123 -d MACHBASE -i -f query.sql -o results.csv -r csv
```

## ODBC/CLI 연결

### C/C++ 애플리케이션

```c
#include "machbase_cli.h"

int main() {
    SQLHENV env;
    SQLHDBC conn;
    SQLHSTMT stmt;
    SQLRETURN rc;

    // 환경 할당
    SQLAllocEnv(&env);

    // 연결 할당
    SQLAllocConnect(env, &conn);

    // 연결
    rc = SQLConnect(conn,
                    (SQLCHAR*)"127.0.0.1", SQL_NTS,  // 서버
                    (SQLCHAR*)"SYS", SQL_NTS,        // 사용자
                    (SQLCHAR*)"MANAGER", SQL_NTS);   // 비밀번호

    if (rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO) {
        printf("Connected!\n");

        // 명령문 할당
        SQLAllocStmt(conn, &stmt);

        // 쿼리 실행
        rc = SQLExecDirect(stmt,
                          (SQLCHAR*)"SELECT * FROM sensors DURATION 1 HOUR",
                          SQL_NTS);

        // 결과 처리...

        // 정리
        SQLFreeStmt(stmt, SQL_DROP);
    }

    SQLDisconnect(conn);
    SQLFreeConnect(conn);
    SQLFreeEnv(env);

    return 0;
}
```

### 컴파일 및 링크

```bash
# Linux
gcc -o myapp myapp.c -I$MACHBASE_HOME/include -L$MACHBASE_HOME/lib -lmachcli

# 실행
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
./myapp
```

## JDBC 연결

### Java 애플리케이션

```java
import java.sql.*;

public class MachbaseExample {
    public static void main(String[] args) {
        String url = "jdbc:machbase://127.0.0.1:5656/MACHBASE";
        String user = "SYS";
        String password = "MANAGER";

        try {
            // 드라이버 로드
            Class.forName("com.machbase.jdbc.driver");

            // 연결
            Connection conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected!");

            // 쿼리 실행
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(
                "SELECT * FROM sensors DURATION 1 HOUR"
            );

            // 결과 처리
            while (rs.next()) {
                String sensorId = rs.getString("sensor_id");
                double value = rs.getDouble("value");
                System.out.println(sensorId + ": " + value);
            }

            // 정리
            rs.close();
            stmt.close();
            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### JDBC URL 형식

```
jdbc:machbase://[host]:[port]/[database]

예시:
jdbc:machbase://localhost:5656/MACHBASE
jdbc:machbase://192.168.1.100:5656/MYDB
```

### 연결 속성

```java
Properties props = new Properties();
props.setProperty("user", "SYS");
props.setProperty("password", "MANAGER");
props.setProperty("connectionTimeout", "30");

Connection conn = DriverManager.getConnection(url, props);
```

## Python 연결

### machbase-python 사용

```python
import machbase

# 연결
conn = machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')

# 커서 생성
cur = conn.cursor()

# 쿼리 실행
cur.execute("SELECT * FROM sensors DURATION 1 HOUR")

# 결과 가져오기
rows = cur.fetchall()
for row in rows:
    print(row)

# 정리
cur.close()
conn.close()
```

### 데이터 삽입

```python
# 단일 삽입
cur.execute("INSERT INTO sensors VALUES (?, ?, ?)",
            ('sensor01', '2025-10-10 14:00:00', 25.3))

# 배치 삽입
data = [
    ('sensor01', '2025-10-10 14:00:01', 25.4),
    ('sensor01', '2025-10-10 14:00:02', 25.5),
    ('sensor02', '2025-10-10 14:00:01', 22.1)
]
cur.executemany("INSERT INTO sensors VALUES (?, ?, ?)", data)

conn.commit()
```

### 커넥션 풀링

```python
from machbase import ConnectionPool

# 풀 생성
pool = ConnectionPool(
    host='127.0.0.1',
    port=5656,
    user='SYS',
    password='MANAGER',
    min_connections=5,
    max_connections=20
)

# 풀에서 연결 가져오기
conn = pool.get_connection()

# 연결 사용...

# 풀로 반환
pool.release_connection(conn)
```

## REST API 연결

### HTTP 엔드포인트

```
기본 URL: http://[host]:5654

엔드포인트:
- POST /machbase - SQL 실행
- POST /machbase/query - SELECT 실행
- POST /machbase/insert - INSERT 실행
- GET /machbase/tables - 테이블 목록
```

### 쿼리 실행 (curl)

```bash
# 데이터 조회
curl -X POST http://localhost:5654/machbase \
  -H "Content-Type: application/json" \
  -d '{
    "sql": "SELECT * FROM sensors DURATION 1 HOUR",
    "format": "json"
  }'

# 데이터 삽입
curl -X POST http://localhost:5654/machbase \
  -H "Content-Type: application/json" \
  -d '{
    "sql": "INSERT INTO sensors VALUES (?, ?, ?)",
    "params": ["sensor01", "2025-10-10 14:00:00", 25.3]
  }'
```

### JavaScript 예제

```javascript
// 데이터 조회
async function querySensors() {
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
}

// 데이터 삽입
async function insertSensor(sensorId, value) {
    const response = await fetch('http://localhost:5654/machbase', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            sql: 'INSERT INTO sensors VALUES (?, ?, ?)',
            params: [sensorId, new Date().toISOString(), value]
        })
    });

    return response.json();
}
```

## .NET 연결

### C# 예제

```csharp
using System;
using System.Data;
using Machbase.Data.MachbaseClient;

class Program {
    static void Main() {
        string connString = "Server=127.0.0.1;Port=5656;User Id=SYS;Password=MANAGER;Database=MACHBASE;";

        using (MachConnection conn = new MachConnection(connString)) {
            conn.Open();
            Console.WriteLine("Connected!");

            // 쿼리 실행
            using (MachCommand cmd = new MachCommand(
                "SELECT * FROM sensors DURATION 1 HOUR", conn)) {

                using (MachDataReader reader = cmd.ExecuteReader()) {
                    while (reader.Read()) {
                        string sensorId = reader.GetString(0);
                        double value = reader.GetDouble(1);
                        Console.WriteLine($"{sensorId}: {value}");
                    }
                }
            }
        }
    }
}
```

## 연결 모범 사례

### 1. 커넥션 풀링 사용

애플리케이션의 경우 커넥션 풀을 유지하세요:

```java
// Java 예제
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:machbase://localhost:5656/MACHBASE");
config.setUsername("SYS");
config.setPassword("MANAGER");
config.setMaximumPoolSize(20);
config.setMinimumIdle(5);

HikariDataSource pool = new HikariDataSource(config);
```

### 2. 연결 오류 처리

```python
import machbase
import time

def get_connection(retries=3):
    for i in range(retries):
        try:
            return machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(1)
```

### 3. 연결 올바르게 종료

```java
try (Connection conn = DriverManager.getConnection(url, user, password);
     Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery(sql)) {

    // 연결 사용...

} // try-with-resources로 자동 종료
```

### 4. 타임아웃 설정

```java
// 연결 타임아웃
props.setProperty("connectionTimeout", "30");  // 초

// 쿼리 타임아웃
stmt.setQueryTimeout(60);  // 초
```

### 5. Prepared Statement 사용

```java
// SQL 인젝션 방지
String sql = "SELECT * FROM sensors WHERE sensor_id = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setString(1, userInput);
ResultSet rs = pstmt.executeQuery();
```

## 연결 문제 해결

### 서버 미실행

```bash
# 서버 상태 확인
machadmin -e

# 예상 출력: "Machbase server is running"

# 실행 중이 아닌 경우 시작
machadmin -u
```

### 연결 거부

```bash
# 포트 리스닝 확인
netstat -an | grep 5656

# 방화벽 확인
sudo iptables -L | grep 5656

# 방화벽에서 포트 허용
sudo iptables -A INPUT -p tcp --dport 5656 -j ACCEPT
```

### 인증 실패

```sql
-- 사용자 존재 확인
SHOW USERS;

-- 비밀번호 재설정
ALTER USER username IDENTIFIED BY 'newpassword';
```

### 네트워크 문제

```bash
# 네트워크 연결 테스트
ping 192.168.1.100

# 포트 연결 테스트
telnet 192.168.1.100 5656

# DNS 해석 확인
nslookup machbase-server.company.com
```

## 보안 고려사항

### 1. 강력한 비밀번호 사용

```sql
-- 강력한 비밀번호로 사용자 생성
CREATE USER analyst IDENTIFIED BY 'Str0ng!P@ssw0rd123';
```

### 2. 네트워크 접근 제한

```bash
# 특정 IP에 바인딩 (machbase.conf에서)
BIND_IP_ADDRESS = 192.168.1.100

# 특정 IP에서만 연결 허용
```

### 3. SSL/TLS 사용

```bash
# SSL 활성화 (machbase.conf에서)
SSL_ENABLE = 1
SSL_CERT = /path/to/cert.pem
SSL_KEY = /path/to/key.pem
```

### 4. 최소 권한 원칙

```sql
-- 필요한 권한만 부여
CREATE USER readonly IDENTIFIED BY 'password';
GRANT SELECT ON sensors TO readonly;
```

## 다음 단계

- **데이터 가져오기**: [데이터 가져오기](../importing-data/) - Machbase에 데이터 로드
- **데이터 조회**: [데이터 조회하기](../querying/) - 쿼리 패턴과 최적화
- **사용자 관리**: [사용자 관리](../user-management/) - 사용자 생성 및 관리

---

애플리케이션에 맞는 연결 방법을 선택하고 Machbase로 구축을 시작하세요!
