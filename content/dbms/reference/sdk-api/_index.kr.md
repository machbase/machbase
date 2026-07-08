---
type: docs
title: 'SDK API 레퍼런스'
weight: 70
---

이 섹션은 Machbase 각 SDK의 주요 API를 빠르게 참조할 수 있도록 정리한 레퍼런스입니다. 각 SDK의 상세 사용 방법과 예제는 [드라이버별 가이드](../../application-integration/guide-drivers/)를 참고하십시오.

## 공통 연결 정보

| 항목 | 기본값 | 설명 |
|------|--------|------|
| HOST | `127.0.0.1` | Machbase 서버 호스트명 또는 IP |
| PORT | `5656` | Machbase 서버 포트 (`machbase.conf`의 `PORT_NO`) |
| USER | `SYS` | 사용자 ID |
| PASSWORD | `MANAGER` | 사용자 비밀번호 |

## JDBC

Java 표준 `java.sql` 인터페이스를 지원합니다. Append를 사용하면 고성능 대량 삽입이 가능합니다.

| API | 설명 |
|-----|------|
| `Class.forName("com.machbase.jdbc.MachDriver")` | JDBC 드라이버 로드 |
| `DriverManager.getConnection(url, user, password)` | 연결 생성 |
| `connection.createStatement()` | Statement 생성 |
| `statement.executeQuery(sql)` | SELECT 실행 |
| `statement.executeUpdate(sql)` | DDL/DML 실행 |
| `MachStatement.executeAppendOpen(table, errorCheckCount)` | Append 세션 열기 |
| `MachStatement.executeAppendData(types, values)` | 행 데이터 추가 |
| `MachStatement.executeAppendClose()` | Append 완료 및 플러시 |
| `MachAppendWriter` | 타입 안전 Append 인터페이스 |

**연결 URL 형식:**

```text
jdbc:machbase://<host>:<port>/machbase
```

**드라이버 가이드:** [JDBC 드라이버](../../application-integration/guide-drivers/jdbc/)

---

## Python (machbaseAPI)

`machbaseAPI` 패키지를 사용한 Python 클라이언트입니다.

| API | 설명 |
|-----|------|
| `machbase()` | 클라이언트 인스턴스 생성 |
| `.open(host, user, password, port)` | 서버 연결 |
| `.close()` | 연결 종료 |
| `.execute(sql)` | SQL 실행 |
| `.result()` | 실행 결과 반환 |
| `.append(table, types, values, format)` | 고성능 Append 삽입 |
| `.tables()` | 테이블 목록 조회 |

**설치:**

```bash
pip install machbaseAPI
```

**드라이버 가이드:** [Python 드라이버](../../application-integration/guide-drivers/python/)

---

## Go (machgo / database/sql)

Go 언어에서 두 가지 방식으로 Machbase에 접근합니다.

### database/sql (표준 SQL 인터페이스)

| API | 설명 |
|-----|------|
| `sql.Open("machbase", dsn)` | 연결 풀 생성 |
| `db.QueryContext(ctx, sql, args...)` | SELECT 실행 |
| `db.ExecContext(ctx, sql, args...)` | DDL/DML 실행 |
| `rows.Scan(dest...)` | 결과 행 스캔 |
| `db.Close()` | 연결 풀 종료 |

**DSN 형식:**

```text
server=<host>;port=<port>;uid=<user>;pwd=<password>
```

### machgo (네이티브 Append)

| API | 설명 |
|-----|------|
| `machgo.New(host, port, user, password, timeout)` | 클라이언트 생성 |
| `client.Exec(ctx, sql)` | SQL 실행 |
| `client.Query(ctx, sql)` | SELECT 실행 |
| `client.Appender(ctx, table)` | Append 세션 생성 |
| `appender.Append(values...)` | 행 데이터 추가 |
| `appender.Close()` | Append 완료 |
| `client.Close()` | 클라이언트 종료 |

**드라이버 가이드:** [Go 드라이버](../../application-integration/guide-drivers/go/)

---

## .NET (net-connector)

C# 및 .NET 환경에서 사용합니다.

| API | 설명 |
|-----|------|
| `MachConnection(connectionString)` | 연결 객체 생성 |
| `connection.Open()` | 서버 연결 |
| `connection.Close()` | 연결 종료 |
| `MachCommand(sql, connection)` | 커맨드 생성 |
| `command.ExecuteReader()` | SELECT 실행, DataReader 반환 |
| `command.ExecuteNonQuery()` | DDL/DML 실행 |
| `MachAppendWriter(connection, table)` | Append 세션 생성 |
| `writer.AddRecord(values)` | 행 데이터 추가 |
| `writer.Close()` | Append 완료 |

**연결 문자열 형식:**

```text
Server=<host>;Port=<port>;Uid=<user>;Pwd=<password>
```

**드라이버 가이드:** [.NET 드라이버](../../application-integration/guide-drivers/net-connector/)

---

## Node.js / TypeScript (@machbase/ts-client)

Node.js 및 TypeScript 환경에서 사용합니다.

| API | 설명 |
|-----|------|
| `new Client(options)` | 클라이언트 인스턴스 생성 |
| `client.connect()` | 서버 연결 |
| `client.query(sql, params)` | SQL 실행, 결과 반환 |
| `client.exec(sql, params)` | DDL/DML 실행 |
| `client.appender(table)` | Append 세션 생성 |
| `appender.append(values)` | 행 데이터 추가 |
| `appender.close()` | Append 완료 |
| `client.disconnect()` | 연결 종료 |

**설치:**

```bash
npm install @machbase/ts-client
```

**드라이버 가이드:** [Node.js 드라이버](../../application-integration/guide-drivers/node-js-typescript/)

---

## CLI/ODBC (C/C++)

C/C++ 네이티브 환경에서 가장 높은 성능을 제공합니다. Machbase 전용 CLI API와 표준 ODBC 인터페이스를 지원합니다.

| API | 설명 |
|-----|------|
| `SQLAllocHandle` | 환경/연결/문장 핸들 할당 |
| `SQLConnect` / `SQLDriverConnect` | 서버 연결 |
| `SQLExecDirect(stmt, sql, len)` | SQL 직접 실행 |
| `SQLFetch(stmt)` | 결과 행 패치 |
| `SQLAppendOpen(stmt, table, errCount)` | Append 세션 열기 |
| `SQLAppendData(stmt, values)` | 행 데이터 추가 |
| `SQLAppendClose(stmt, success, failure)` | Append 완료 |
| `SQLDisconnect` | 연결 해제 |
| `SQLFreeHandle` | 핸들 해제 |

**드라이버 가이드:** [CLI/ODBC 드라이버](../../application-integration/guide-drivers/cli-odbc/)

---

## REST API (HTTP)

별도 드라이버 설치 없이 HTTP 요청으로 Machbase에 접근합니다.

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| `GET` | `/machbase?q=<SQL>` | SQL 실행 |
| `POST` | `/machbase` | 다수 행 Append 삽입 |

**레퍼런스:** [REST API 레퍼런스](../rest-api/)
