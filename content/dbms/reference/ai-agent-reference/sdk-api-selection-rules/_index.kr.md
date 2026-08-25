---
type: docs
title: '18.8.9 sdk-api-selection-rules'
weight: 90
toc: true
---

이 페이지는 사용자의 요구사항과 언어에 따라 적합한 Machbase SDK를 선택하는 규칙을 정의합니다.

## 기능별 SDK 선택 가이드

| 요구사항 | 권장 SDK | 비고 |
|----------|----------|------|
| Append 필요 + Java | **JDBC** (`MachStatement.executeAppendOpen()`) | [JDBC 레퍼런스](/dbms/development-tools-integration/jdbc/) |
| Append 필요 + Python | **machbaseAPI** (`machbase()` 클래스의 `append()`) | [Python 레퍼런스](/dbms/development-tools-integration/python/) |
| Append 필요 + Go | **machgo** (native client) | `database/sql` 표준 API에는 없으며 `machbase.Conn.Appender()`는 `sql.Conn.Raw()` 확장으로만 제공 |
| Append 필요 + .NET | **MachConnector** (`MachAppendWriter`) | [.NET 레퍼런스](/dbms/development-tools-integration/net-connector/) |
| Append 필요 + Node.js | **@machbase/ts-client** | [Node.js 레퍼런스](/dbms/development-tools-integration/node-js-typescript/) |
| AUTH KEY 인증 필요 | **JDBC**, **Machbase SQLCLI**, **ODBC**, **machsql** | Python/Go/.NET/Node.js는 AUTH KEY 미지원 |
| TRANSACTION 테이블 트랜잭션 필요 | **Go (`database/sql`)**, **JDBC**, **Machbase SQLCLI**, **ODBC** | Go SQL은 기본 isolation level, JDBC는 Standard Edition에서 지원 |
| SELECT 결과 Nullable 메타데이터 필요 | **Go**, **Machbase SQLCLI**, **ODBC**, **JDBC**, **Python**, **Node.js**, **.NET** | Go native는 `api.Column`, SQL은 `ColumnTypeNullable` 사용 |
| SELECT 결과 PRIMARY KEY 메타데이터 필요 | **Go native**, **JDBC**, **Python**, **Node.js**, **.NET**, **ODBC** | Go `database/sql` 표준 `ColumnType`에는 PK API가 없음 |
| Prepared Parameter Nullable 메타데이터 필요 | **Go**, **Machbase SQLCLI**, **ODBC**, **JDBC** | Go는 결과 컬럼 메타데이터를 제공 |
| 서버 Named Bind 필요 | **Go**, **SQLCLI**, **JDBC**, **Python**, **Node.js** | Go는 `api.Named()` 또는 `sql.Named()` 사용 |
| Python에서 동일 SQL 반복 실행 | **machbaseAPI 2.4 prepared cursor** | `cursor(prepared=True)`로 호출 간 statement 재사용 |
| Go 언어 선호 + Append 필요 | **machgo** (native) | [Go 레퍼런스](/dbms/development-tools-integration/go/) |
| Go 언어 선호 + 표준 인터페이스 | **database/sql** 드라이버 | Append 불필요한 경우 |
| 브라우저 / 웹 / 스크립트 | 백엔드 언어에 맞는 **JDBC, Python, Go, Node.js, .NET 또는 ODBC** | 브라우저가 DB에 직접 연결하지 않도록 백엔드에서 쿼리 실행 |
| 데이터 탐색 / 보고 | **R + RODBC** | 통계 분석에 적합 |
| C/C++ 직접 연결 | **Machbase SQLCLI** | [Machbase SQLCLI 레퍼런스](/dbms/development-tools-integration/cli-odbc/) |
| C/C++ ODBC 환경 | **ODBC** | [ODBC 레퍼런스](/dbms/development-tools-integration/cli-odbc/) |

## 다중 데이터베이스 선택 규칙

| 요구사항 | 권장 방식 | 주의사항 |
|----------|----------|----------|
| 초기 database를 지정하는 JDBC/ODBC/Python/Node.js | 각 client의 database/catalog 연결 옵션 | 연결 직후 `CURRENT_DATABASE()` 확인 |
| Go native에서 database 전환 | `api.WithDatabase()`, SQL `USE`, 3-part 이름 | `Conn.Appender()`의 target database와 권한 확인 |
| Go `database/sql` pool에서 여러 DB 사용 | DSN `database`/`db` 또는 URL path/query | 설정된 database가 있으면 `ResetSession()`에서 해당 DB로 복원 |
| mounted backup 조회 | `USAGE ON DATABASE` + table `SELECT` | mounted DB는 READ ONLY, `USE` 불가 |

다중 데이터베이스의 정규 동작은 [운영 가이드](/dbms/operations-configuration-recovery/multi-database/)를
참조합니다.

## 언어별 권장 SDK 요약

| 언어 | 기본 권장 | Append 필요 시 | Transaction 필요 시 |
|------|----------|---------------|---------------------|
| Java | JDBC | JDBC (executeAppendOpen) | JDBC |
| Python | machbaseAPI | machbaseAPI (append()) | 미지원 (JDBC/.NET/ODBC 고려) |
| Go | database/sql | machgo (native) | `database/sql` 또는 native SQL 트랜잭션 |
| C# / .NET | MachConnector | MachConnector (MachAppendWriter) | 미지원 (`MachTransaction` 미구현) |
| Node.js | @machbase/ts-client | @machbase/ts-client | 미지원 |
| C / C++ (Machbase SQLCLI) | Machbase SQLCLI | Machbase SQLCLI | Machbase SQLCLI |
| C / C++ (ODBC) | ODBC | ODBC | ODBC |
| R | RODBC | 미지원 | 미지원 |
| 웹 백엔드 | 백엔드 언어용 SDK | 같은 SDK의 Append API | SDK별 지원 범위 확인 |

## 피해야 할 조합

| 조합 | 이유 | 대안 |
|------|------|------|
| Go `database/sql` + Append | 표준 `sql.DB`/`sql.Tx`에는 없음. `sql.Conn.Raw()` 확장 사용 가능 | 신규 대량 입력은 `machgo` (native) 권장 |
| Go native + Transaction (BEGIN/COMMIT) | 전용 `Begin` 메서드 없음 | 같은 연결에서 트랜잭션 SQL 직접 실행 |
| Go + Nullable 결과 메타데이터 | native는 `api.Column`, SQL은 `ColumnTypeNullable` 사용 | nullable 대상 타입으로 scan |
| Node.js + AUTH KEY | Node.js 드라이버 AUTH KEY 미지원 | JDBC / ODBC 사용 |
| Python named mapping에 `?` 사용 | 객체 입력은 `:name` SQL이 필요 | `:name`과 mapping 사용 |
| Go `sql.Named()` 사용 | `database/sql`에서 지원 | named marker와 `sql.Named()` 사용. positional과 혼용 금지 |

## SDK별 주요 특징 요약

### JDBC

- Append: `MachStatement.executeAppendOpen()` → `executeAppendData()` → `executeAppendClose()`
- AUTH KEY: 지원 (`connectURL`에 키 파일 경로 지정)
- Transaction: Standard Edition에서 `setAutoCommit(false)`, `commit()`, `rollback()` 지원
- Transaction 시작: manual mode의 첫 Statement에서 lazy `BEGIN`
- 파라미터: `?` 또는 `:name`, `MachPreparedStatement.setObject(String, Object)`
- Prepared Parameter 메타데이터: `PreparedStatement.getParameterMetaData()`
- Nullable 메타데이터: `ResultSetMetaData.isNullable()`
- PRIMARY KEY 메타데이터: `MachResultSetMetaData.isPrimaryKey(column)`, 카탈로그는 `getPrimaryKeys()`

### Python (machbaseAPI)

- Append: `conn.append(table, cols, data)` 또는 `machbase()` 클래스
- AUTH KEY: 미지원
- Transaction: 미지원
- 일반 cursor: `:name`과 mapping은 서버 prepare/bind, `%s`와 `%(name)s`는
  client-side 렌더링
- Prepared cursor: `cursor(prepared=True)`. `%s`, `?`, `%(name)s`, `:name` 지원
- Statement 재사용: 동일한 원본 SQL을 여러 `execute()`와 `executemany()` 호출에서 재사용
- Cache 제약: cursor당 statement 하나, SQL 변경 또는 cursor close 시 해제
- Nullable 메타데이터: `cursor.description[i][6]`
- PRIMARY KEY 메타데이터: `cursor.column_metadata[i].is_primary_key`

### Go (machgo / native)

- Append: `stmt.AppendOpen()` → `stmt.AppendData()` → `stmt.AppendClose()`
- AUTH KEY: 미지원
- Transaction: 전용 편의 API 없음. `BEGIN` / `COMMIT` / `ROLLBACK` SQL 직접 실행
- 파라미터: positional `?`와 `api.Named()` 이름 기반 API
- Nullable 메타데이터: `api.Column.Nullability`
- PRIMARY KEY 메타데이터: `api.Column.PrimaryKey`

### Go (database/sql)

- Append: 표준 API에는 없음. `sql.Conn.Raw()`에서 `machbase.Conn.Appender()` 확장 사용 가능
- AUTH KEY: 미지원
- Transaction: 기본 isolation level의 `Begin` / `BeginTx`, `Commit`, `Rollback` 지원
- 파라미터: positional `?`와 `sql.Named()` 이름 기반 API
- 적합한 용도: 단순 SELECT, INSERT (TAG 테이블 소량), 시스템 뷰 조회
- Nullable 메타데이터: `Rows.ColumnTypeNullable()`
- PRIMARY KEY 메타데이터: 표준 API 없음. native `machgo` 또는 카탈로그 SQL 사용

### .NET (MachConnector)

- Append: `MachAppendWriter` 클래스 사용
- AUTH KEY: 미지원
- Transaction: 미지원 (`MachTransaction` 미구현)
- 파라미터: `MachParameterCollection`의 `:name` 사용
- 실행 방식: client-side typed literal 렌더링 후 ExecDirect
- Nullable 메타데이터: `MachDataReader.GetSchemaTable().AllowDBNull`
- PRIMARY KEY 메타데이터: `MachDataReader.GetSchemaTable()["IsKey"]`

## 참조

- SDK 지원 범위 전체: [지원 범위 (SDK)](/dbms/development-tools-integration/#sdk)
- 기능 지원 매트릭스: [support-matrix](../support-matrix/)
- 제약 사항: [constraints-index](../constraints-index/)
