---
type: docs
title: '17.7.2 JDBC'
weight: 20
toc: true
---

Machbase JDBC 드라이버는 Java 8을 기준으로 JDBC 4.2 핵심 API를 제공합니다. 표준 JDBC
API로 서버에 연결하고 PreparedStatement, 타입 지정 조회와 바인딩, 데이터베이스
메타데이터, 로컬 트랜잭션과 커넥션 풀을 사용할 수 있습니다.

| 항목 | 값 |
|------|----|
| Java bytecode 기준 | Java 8 |
| 드라이버가 보고하는 JDBC 버전 | 4.2 |
| 드라이버 버전 | 3.0.0 |
| JDBC URL | `jdbc:machbase://<host>:<port>/machbasedb` |
| `Driver.jdbcCompliant()` | `false` |

`jdbcCompliant()`의 `false`는 JDBC 4.2 API 지원 여부가 아니라 SQL-92 Entry Level 전체
지원 여부를 나타냅니다. 애플리케이션에서는 필요한 선택 기능을
`DatabaseMetaData`의 capability 메서드로 확인합니다.

## 드라이버 설치

### JAR 파일 사용

Machbase 설치 디렉터리의 `machbase.jar`를 classpath에 추가합니다.

```bash
ls -l "$MACHBASE_HOME/lib/machbase.jar"
javac -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp.java
java -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp
```

JAR에는 `META-INF/services/java.sql.Driver`가 포함되어 있습니다. JDBC 4.0 이후 환경에서는
`Class.forName("com.machbase.jdbc.MachDriver")`를 호출하지 않아도 드라이버가 자동으로
등록됩니다. 기존 애플리케이션의 명시적 호출은 그대로 사용할 수 있습니다.

### Maven

```xml
<dependency>
    <groupId>com.machbase</groupId>
    <artifactId>machjdbc</artifactId>
    <version>{{< jdbc_version >}}</version>
</dependency>
```

### Gradle

```groovy
dependencies {
    implementation 'com.machbase:machjdbc:{{< jdbc_version >}}'
}
```

배포 artifact 버전은 [Maven Central](https://mvnrepository.com/artifact/com.machbase/machjdbc)에서
확인합니다. 드라이버가 런타임 메타데이터로 반환하는 `3.0.0`과 artifact 버전은 서로 다른
버전 체계입니다.

## 서버에 연결

사용자 이름과 비밀번호는 소스 코드에 기록하지 않고 환경 변수나 secret manager로
전달합니다.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.Properties;

String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";

Properties properties = new Properties();
properties.setProperty("user", "SYS");
properties.setProperty("password", System.getenv("MACHBASE_PASSWORD"));

try (Connection connection =
         DriverManager.getConnection(url, properties)) {
    // SQL을 실행합니다.
}
```

### 연결 옵션

연결 옵션은 `Properties` 또는 URL query string으로 지정합니다.

| 옵션 | 설명 |
|------|------|
| `user`, `password` | 비밀번호 인증 정보 |
| `TIMEZONE` | 세션 타임존. `+0900` 형식을 사용합니다. |
| `randomHost` | 호스트 목록에서 연결 대상을 무작위로 선택합니다. |
| `maxStatements` | 풀링 연결의 최대 캐시 Statement 수 |
| `CONNECTION_TIMEOUT` | 소켓 연결 timeout(초). `0`은 제한 없음입니다. |
| `SOCKET_TIMEOUT` | 소켓 읽기 timeout(초). `0`은 제한 없음입니다. |
| `characterEncoding` | 클라이언트 문자 인코딩 |
| `AUTH_MODE` | `PASSWORD` 또는 `CHALLENGE` |
| `AUTH_SIG_SCHEME` | `ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS` |
| `AUTH_KEY_FILE` | PEM 개인키 파일 경로 |

```java
String url =
    "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
```

연결이 끊긴 뒤 자동 reconnect가 성공해도 이전 Statement, PreparedStatement와 ResultSet은
재사용하지 않습니다. 활성 트랜잭션에서 연결 오류가 발생하면 연결을 폐기하고 업무의
멱등성 정책에 따라 전체 트랜잭션을 다시 실행합니다.

## AUTH KEY 인증

공개키 기반 challenge 인증에서는 비밀번호 대신 로컬 개인키로 서버 challenge에
서명합니다.

```java
Properties properties = new Properties();
properties.setProperty("user", "app_user");
properties.setProperty("AUTH_MODE", "CHALLENGE");
properties.setProperty("AUTH_SIG_SCHEME", "ECDSA");
properties.setProperty(
    "AUTH_KEY_FILE", "/opt/machbase/keys/app_user_ecdsa.pem");

Connection connection = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/machbasedb", properties);
```

- `AUTH_MODE=CHALLENGE`에서는 `password`를 인증에 사용하지 않습니다.
- `AUTH_KEY_FILE`은 필수입니다.
- `AUTH_SIG_SCHEME`을 생략하면 키 종류에 맞는 기본 서명 방식을 선택합니다.
- POSIX 환경에서는 개인키 파일 권한을 `600`으로 제한합니다.

## 빠른 시작

다음 예제는 LOG 테이블에 값을 입력하고 다시 조회합니다.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Properties;

public class JdbcQuickStart {
    public static void main(String[] args) throws Exception {
        Properties properties = new Properties();
        properties.setProperty("user", "SYS");
        properties.setProperty(
            "password", System.getenv("MACHBASE_PASSWORD"));

        try (Connection connection = DriverManager.getConnection(
                 "jdbc:machbase://127.0.0.1:5656/machbasedb",
                 properties);
             Statement statement = connection.createStatement()) {
            statement.execute(
                "CREATE LOG TABLE jdbc_sensor " +
                "(ts DATETIME, name VARCHAR(40), value DOUBLE)");

            try (PreparedStatement insert = connection.prepareStatement(
                     "INSERT INTO jdbc_sensor VALUES (?, ?, ?)")) {
                insert.setLong(1, System.currentTimeMillis() * 1_000_000L);
                insert.setString(2, "sensor-1");
                insert.setDouble(3, 25.3);
                insert.executeUpdate();
            }

            try (ResultSet result = statement.executeQuery(
                     "SELECT name, value FROM jdbc_sensor")) {
                while (result.next()) {
                    System.out.printf("%s %.1f%n",
                        result.getString("NAME"),
                        result.getDouble("VALUE"));
                }
            }
        }
    }
}
```

DATETIME에 epoch nanosecond 값을 전달할 때는 `long`을 사용합니다. 예제의 테이블이 이미
존재하면 `CREATE LOG TABLE`을 생략하거나 다른 이름을 사용합니다.

## 버전 확인

```java
import java.sql.DatabaseMetaData;

DatabaseMetaData metadata = connection.getMetaData();

System.out.println(metadata.getDriverName());
System.out.println(metadata.getDriverVersion());
System.out.println(metadata.getJDBCMajorVersion()); // 4
System.out.println(metadata.getJDBCMinorVersion()); // 2
```

## 관련 문서

| 문서 | 내용 |
|------|------|
| [PreparedStatement와 타입](./prepared-types/) | parameter metadata, named bind, SQLType, NULL과 타입 변환 |
| [ResultSet, Statement와 LOB](./resultset-lob/) | typed 조회, stream, LOB, timeout과 자원 관리 |
| [트랜잭션과 커넥션 풀](./transaction-pooling/) | Standard 로컬 트랜잭션, DataSource와 pool |
| [DatabaseMetaData](./database-metadata/) | 테이블, 컬럼, 키, 인덱스와 capability 조회 |
| [Append API](./append-api/) | `MachStatement` 기반 고속 입력 |
| [마이그레이션과 문제 해결](./migration-troubleshooting/) | 이전 드라이버 전환, 미지원 기능과 오류 처리 |
