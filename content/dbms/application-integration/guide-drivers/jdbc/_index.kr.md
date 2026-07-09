---
type: docs
title: '11.3.2 JDBC'
weight: 20
---

## JDBC 개요

JDBC(Java DataBase Connectivity)는 자바 프로그래밍 언어로 데이터베이스에 접근하기 위한 표준 API입니다. Machbase JDBC 드라이버를 사용하면 어떤 자바 애플리케이션에서도 코드를 거의 수정하지 않고 Machbase 서버에 연결할 수 있습니다.

- 표준 JDBC 스펙: [JDBC 4.0](https://www.oracle.com/java/technologies/javase/javase-tech-database.html#corespec40)
- 드라이버 클래스: `com.machbase.jdbc.MachDriver`
- Connection URL 형식: `jdbc:machbase://HOST:PORT/machbasedb`

## 드라이버 설치

### JAR 파일 직접 사용

`$MACHBASE_HOME/lib` 디렉터리에서 `machbase.jar` 파일을 확인합니다.

```bash
ls -l $MACHBASE_HOME/lib/machbase.jar
```

클래스패스에 해당 JAR를 추가해 컴파일하고 실행합니다.

```bash
javac -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp.java
java  -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp
```

### Maven

`pom.xml`의 `<dependencies>` 블록에 다음을 추가합니다.

```xml
<dependency>
    <groupId>com.machbase</groupId>
    <artifactId>machjdbc</artifactId>
    <version>8.6.0</version>
</dependency>
```

최신 버전은 [Maven Central](https://mvnrepository.com/artifact/com.machbase/machjdbc)에서 확인하세요.

### Gradle

```groovy
dependencies {
    implementation 'com.machbase:machjdbc:8.6.0'
}
```

## 연결 방법

### 기본 연결

```java
import java.sql.*;
import java.util.Properties;
import com.machbase.jdbc.*;

public class ConnectSample {
    public static Connection connect() throws Exception {
        String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";

        Properties props = new Properties();
        props.put("user", "SYS");
        props.put("password", "MANAGER");

        Class.forName("com.machbase.jdbc.MachDriver");
        return DriverManager.getConnection(url, props);
    }

    public static void main(String[] args) throws Exception {
        try (Connection conn = connect()) {
            System.out.println("Machbase JDBC connected.");
        }
    }
}
```

### 연결 옵션

드라이버는 `Properties` 객체 또는 URL 쿼리 문자열로 옵션을 받습니다.

| 옵션 | 설명 |
|------|------|
| `user` / `password` | 비밀번호 인증 계정 정보 |
| `TIMEZONE` | 세션 타임존 (`+0900` 형식). 잘못된 값은 연결 오류로 처리됩니다. |
| `randomHost` | `true`이면 호스트 목록에서 무작위로 연결 대상을 선택합니다. |
| `maxStatements` | 풀링 연결에서 사용할 최대 캐시 Statement 수 |
| `CONNECTION_TIMEOUT` | 소켓 연결 타임아웃(초). `0`은 무제한 |
| `SOCKET_TIMEOUT` | 소켓 읽기 타임아웃(초). `0`은 무제한 |
| `characterEncoding` | 클라이언트 문자 인코딩 이름 |
| `AUTH_MODE` | `PASSWORD` 또는 `CHALLENGE` (AUTH KEY 인증) |
| `AUTH_SIG_SCHEME` | `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS` 중 선택 |
| `AUTH_KEY_FILE` | 로컬 PEM 개인키 파일 경로 |

#### 타임존 설정 예제

```java
String url = "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
```

또는 `Properties`로 지정:

```java
props.put("TIMEZONE", "+0900");
```

## AUTH KEY 인증

Machbase 8.0 이상에서 공개키 기반 Challenge 인증을 사용할 수 있습니다.

```java
String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";

Properties props = new Properties();
props.put("user", "app_user");
props.put("AUTH_MODE", "CHALLENGE");
props.put("AUTH_SIG_SCHEME", "ECDSA");
props.put("AUTH_KEY_FILE", "/opt/machbase/keys/app_user_ecdsa.pem");

Class.forName("com.machbase.jdbc.MachDriver");
Connection conn = DriverManager.getConnection(url, props);
```

- `AUTH_KEY_FILE`만 지정하고 `AUTH_MODE`를 생략하면 내부적으로 `CHALLENGE`로 처리합니다.
- EC 키는 `ECDSA`, RSA 키는 `RSA_PKCS1_V15`가 기본 스킴으로 자동 선택됩니다.
- 지원 키: ECDSA (`P-256`, `P-384`, `P-521`), RSA (`2048`, `3072`, `4096` bits)
- POSIX 환경에서는 개인키 파일 권한을 `600`으로 설정하는 것을 권장합니다.

## PreparedStatement

```java
import java.sql.*;
import java.util.Properties;
import com.machbase.jdbc.*;

public class PreparedStmtSample {
    public static void main(String[] args) throws Exception {
        String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
        Properties props = new Properties();
        props.put("user", "SYS");
        props.put("password", "MANAGER");

        Class.forName("com.machbase.jdbc.MachDriver");
        try (Connection conn = DriverManager.getConnection(url, props)) {
            // 테이블 생성
            try (Statement stmt = conn.createStatement()) {
                stmt.execute(
                    "CREATE TABLE IF NOT EXISTS sensor_data (" +
                    "  ts DATETIME, device VARCHAR(40), value DOUBLE)"
                );
            }

            // PreparedStatement로 INSERT
            String insertSql = "INSERT INTO sensor_data VALUES (?, ?, ?)";
            try (MachPreparedStatement pstmt =
                     (MachPreparedStatement) conn.prepareStatement(insertSql)) {
                for (int i = 0; i < 5; i++) {
                    pstmt.setLong(1, System.currentTimeMillis() * 1_000_000L); // nanoseconds
                    pstmt.setString(2, "sensor-" + i);
                    pstmt.setDouble(3, 20.0 + i * 0.5);
                    pstmt.executeUpdate();
                }
                System.out.println("5 rows inserted.");
            }

            // SELECT
            String selectSql = "SELECT to_char(ts,'YYYY-MM-DD HH24:MI:SS') as ts, device, value" +
                               " FROM sensor_data ORDER BY ts";
            try (Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery(selectSql)) {
                while (rs.next()) {
                    System.out.printf("ts=%s device=%s value=%.1f%n",
                        rs.getString("ts"),
                        rs.getString("device"),
                        rs.getDouble("value"));
                }
            }
        }
    }
}
```

### IPv4/IPv6 바인딩

`MachPreparedStatement`는 IP 주소 타입을 위한 확장 메서드를 제공합니다.

```java
MachPreparedStatement pstmt =
    (MachPreparedStatement) conn.prepareStatement(
        "INSERT INTO net_log(ts, src_ip, dst_ip) VALUES (?, ?, ?)");
pstmt.setLong(1, System.currentTimeMillis() * 1_000_000L);
pstmt.setIpv4(2, "192.168.1.100");
pstmt.setIpv6(3, "::1");
pstmt.executeUpdate();
```

## Append API

Machbase Append 프로토콜은 대량 데이터를 고속으로 적재할 때 사용합니다. `MachStatement`를 통해 접근합니다.

### Append API 메서드

| 메서드 | 설명 |
|--------|------|
| `executeAppendOpen(tableName, errorCheckCount)` | Append 프로토콜 시작. errorCheckCount마다 오류 확인 |
| `executeAppendData(rsmd, data)` | 행 데이터 전송. 성공 시 1 또는 2 반환 |
| `executeAppendDataByTime(rsmd, time, data)` | 특정 나노초 시간을 지정해 행 전송 |
| `executeAppendFlush()` | Pending 응답 동기화. 성공 시 1 반환 |
| `executeAppendClose()` | Append 세션 종료. 성공 시 1 반환 |
| `executeSetAppendErrorCallback(callback)` | 오류 발생 시 호출할 콜백 등록 |
| `getAppendSuccessCount()` | 성공한 Append 건수 반환 |
| `getAppendFailureCount()` | 실패한 Append 건수 반환 |

### Append 예제

```java
import java.util.*;
import java.sql.*;
import com.machbase.jdbc.*;

public class AppendSample {
    private static final String TABLE = "sensor_data";
    private static final int ERROR_CHECK_COUNT = 100;

    public static void main(String[] args) throws Exception {
        String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
        Properties props = new Properties();
        props.put("user", "SYS");
        props.put("password", "MANAGER");

        Class.forName("com.machbase.jdbc.MachDriver");

        try (Connection conn = DriverManager.getConnection(url, props)) {
            MachStatement stmt = (MachStatement) conn.createStatement();

            // Append 시작
            ResultSet rs = stmt.executeAppendOpen(TABLE, ERROR_CHECK_COUNT);
            ResultSetMetaData rsmd = rs.getMetaData();

            // 오류 콜백 등록
            stmt.executeSetAppendErrorCallback(
                (errNo, errMsg, rowMsg) ->
                    System.err.printf("Append Error [%05d]: %s%n%s%n", errNo, errMsg, rowMsg)
            );

            long startTime = System.nanoTime();
            int count = 10_000;

            for (int i = 0; i < count; i++) {
                ArrayList<Object> row = new ArrayList<>();
                row.add(System.currentTimeMillis() * 1_000_000L + i); // ts (nanoseconds)
                row.add("sensor-" + (i % 10));                         // device
                row.add(20.0 + Math.random() * 10.0);                  // value

                int rc = stmt.executeAppendData(rsmd, row);
                if (rc != 1 && rc != 2) {
                    System.err.println("AppendData error at row " + i);
                    break;
                }
            }

            stmt.executeAppendFlush();
            stmt.executeAppendClose();

            long elapsed = (System.nanoTime() - startTime) / 1_000_000;
            System.out.printf("Appended %d rows in %d ms%n", count, elapsed);
            System.out.printf("Success: %d, Failure: %d%n",
                stmt.getAppendSuccessCount(),
                stmt.getAppendFailureCount());

            rs.close();
            stmt.close();
        }
    }
}
```

> **중요**: Append에서 DATETIME 컬럼 값은 반드시 `long` 타입의 나노초(nanosecond) 단위로 전달해야 합니다.
> `System.currentTimeMillis() * 1_000_000L`로 밀리초를 나노초로 변환합니다.

## 커넥션 풀 (HikariCP)

운영 환경에서는 커넥션 풀을 사용하는 것을 권장합니다. [HikariCP](https://github.com/brettwooldridge/HikariCP)와 연동하는 예시입니다.

### Maven 의존성 추가

```xml
<dependency>
    <groupId>com.zaxxer</groupId>
    <artifactId>HikariCP</artifactId>
    <version>5.1.0</version>
</dependency>
```

### HikariCP 설정 예제

```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
config.setUsername("SYS");
config.setPassword("MANAGER");
config.setDriverClassName("com.machbase.jdbc.MachDriver");

// 풀 크기 설정
config.setMaximumPoolSize(10);
config.setMinimumIdle(2);
config.setConnectionTimeout(30_000);   // 30초
config.setIdleTimeout(600_000);        // 10분
config.setMaxLifetime(1_800_000);      // 30분

// 연결 검증 쿼리
config.setConnectionTestQuery("SELECT 1 FROM V$TABLES LIMIT 1");

// 타임존 설정
config.addDataSourceProperty("TIMEZONE", "+0900");

HikariDataSource dataSource = new HikariDataSource(config);

// 사용 예
try (Connection conn = dataSource.getConnection();
     Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery("SELECT COUNT(*) FROM sensor_data")) {
    if (rs.next()) {
        System.out.println("Row count: " + rs.getLong(1));
    }
}
```

## 전체 예제: INSERT / SELECT

아래 예제는 테이블 생성, 데이터 삽입, 조회까지 한 번에 확인할 수 있는 독립 실행 가능한 코드입니다.

```java
import java.sql.*;
import java.util.Properties;
import com.machbase.jdbc.*;

public class FullExample {
    public static void main(String[] args) throws Exception {
        String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";
        Properties props = new Properties();
        props.put("user", "SYS");
        props.put("password", "MANAGER");
        props.put("TIMEZONE", "+0900");

        Class.forName("com.machbase.jdbc.MachDriver");

        try (Connection conn = DriverManager.getConnection(url, props)) {
            System.out.println("Connected to Machbase.");

            // 테이블 생성
            try (Statement stmt = conn.createStatement()) {
                try {
                    stmt.execute("DROP TABLE ex_sensor");
                } catch (SQLException ignored) {
                    // 테이블이 없으면 무시하고 생성합니다.
                }
                stmt.execute(
                    "CREATE TABLE ex_sensor (" +
                    "  ts DATETIME, tag VARCHAR(40), value DOUBLE)");
            }

            // PreparedStatement로 데이터 삽입
            String insertSql = "INSERT INTO ex_sensor VALUES (?, ?, ?)";
            try (MachPreparedStatement pstmt =
                     (MachPreparedStatement) conn.prepareStatement(insertSql)) {
                long baseTime = System.currentTimeMillis() * 1_000_000L;
                for (int i = 0; i < 10; i++) {
                    pstmt.setLong(1, baseTime + i * 1_000_000_000L);
                    pstmt.setString(2, "tag-" + (i % 3));
                    pstmt.setDouble(3, 20.0 + i);
                    pstmt.executeUpdate();
                }
                System.out.println("Inserted 10 rows.");
            }

            // SELECT
            String selectSql =
                "SELECT to_char(ts,'YYYY-MM-DD HH24:MI:SS') as ts, tag, value" +
                " FROM ex_sensor ORDER BY ts";
            try (Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery(selectSql)) {
                System.out.println("--- Query Results ---");
                while (rs.next()) {
                    System.out.printf("  ts=%-22s tag=%-6s value=%.1f%n",
                        rs.getString("ts"),
                        rs.getString("tag"),
                        rs.getDouble("value"));
                }
            }
        }
    }
}
```

## 주의 사항

- 트랜잭션은 RDB 테이블 작업에서 사용합니다. LOG/TAG 테이블 Append성 입력은 롤백 대상이 아니므로 테이블 타입별 지원 범위를 확인합니다.
- LOG 테이블과 TAG 테이블에는 `UPDATE`를 사용할 수 없습니다.
- `_arrival_time` 컬럼은 기본적으로 숨겨져 있습니다. 표시하려면 URL에 `show_hidden_cols=1`을 추가합니다.
- Append에서 DATETIME 값은 반드시 나노초 단위 `long`으로 전달해야 합니다.
