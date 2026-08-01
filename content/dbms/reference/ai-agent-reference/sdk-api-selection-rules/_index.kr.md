---
type: docs
title: '17.10.9 sdk-api-selection-rules'
weight: 90
toc: true
---

이 페이지는 사용자의 요구사항과 언어에 따라 적합한 Machbase SDK를 선택하는 규칙을 정의합니다.

## 기능별 SDK 선택 가이드

| 요구사항 | 권장 SDK | 비고 |
|----------|----------|------|
| Append 필요 + Java | **JDBC** (`MachStatement.executeAppendOpen()`) | [JDBC 가이드](/dbms/application-integration/guide-drivers/#jdbc) |
| Append 필요 + Python | **machbaseAPI** (`machbase()` 클래스의 `append()`) | [Python 가이드](/dbms/application-integration/guide-drivers/#python) |
| Append 필요 + Go | **machcli** (native client) | `database/sql`은 Append 미지원 |
| Append 필요 + .NET | **MachConnector** (`MachAppendWriter`) | [.NET 가이드](/dbms/application-integration/guide-drivers/#net-connector) |
| Append 필요 + Node.js | **@machbase/ts-client** | [Node.js 가이드](/dbms/application-integration/guide-drivers/#node-js-typescript) |
| AUTH KEY 인증 필요 | **JDBC**, **ODBC/CLI**, **machsql** | Python/Go/.NET/Node.js는 AUTH KEY 미지원 |
| TRANSACTION 테이블 트랜잭션 필요 | **JDBC**, **ODBC/CLI** | JDBC 표준 API는 Standard Edition에서 지원 |
| SELECT 결과 Nullable 메타데이터 필요 | **ODBC/CLI**, **JDBC**, **Python**, **Node.js**, **.NET** | Go와 REST API는 공개 결과 메타데이터 API 없음 |
| Prepared Parameter Nullable 메타데이터 필요 | **Native MachCLI**, **SQLCLI/ODBC**, **JDBC** | JDBC는 `getParameterMetaData()` 지원 |
| 서버 Named Bind 필요 | **SQLCLI**, **JDBC**, **Python**, **Node.js** | ODBC/machsql은 ordinal, .NET은 client-side 렌더링 |
| Python에서 동일 SQL 반복 실행 | **machbaseAPI 2.4 prepared cursor** | `cursor(prepared=True)`로 호출 간 statement 재사용 |
| Go 언어 선호 + Append 필요 | **machcli** (native) | [Go 가이드](/dbms/application-integration/guide-drivers/#go) |
| Go 언어 선호 + 표준 인터페이스 | **database/sql** 드라이버 | Append 불필요한 경우 |
| 브라우저 / 웹 / 스크립트 | **REST API** (포트 5657, `/machbase` 엔드포인트) | [REST API 가이드](/dbms/application-integration/rest-api/) |
| 데이터 탐색 / 보고 | **R + RODBC** | 통계 분석에 적합 |
| C/C++ 애플리케이션 | **ODBC/CLI** | [ODBC 가이드](/dbms/application-integration/guide-drivers/#cli-odbc) |

## 언어별 권장 SDK 요약

| 언어 | 기본 권장 | Append 필요 시 | Transaction 필요 시 |
|------|----------|---------------|---------------------|
| Java | JDBC | JDBC (executeAppendOpen) | JDBC |
| Python | machbaseAPI | machbaseAPI (append()) | 미지원 (JDBC/.NET/ODBC 고려) |
| Go | database/sql | machcli (native) | 미지원 (다른 SDK 고려) |
| C# / .NET | MachConnector | MachConnector (MachAppendWriter) | 미지원 (`MachTransaction` 미구현) |
| Node.js | @machbase/ts-client | @machbase/ts-client | 미지원 |
| C / C++ | ODBC/CLI | ODBC/CLI | ODBC/CLI |
| R | RODBC | 미지원 | 미지원 |
| 웹 / curl / HTTP | REST API | REST API (`POST /machbase`) | 미지원 |

## 피해야 할 조합

| 조합 | 이유 | 대안 |
|------|------|------|
| Go `database/sql` + Append | Append 미지원 | `machcli` (native) 사용 |
| Go + Transaction (BEGIN/COMMIT) | `Begin()` / `BeginTx()` 미구현 | ODBC 또는 JDBC 사용 |
| Go + Nullable 결과 메타데이터 | 공개 조회 API 없음 | ODBC/CLI, JDBC, Python, Node.js 또는 .NET 사용 |
| REST API + Transaction | REST API는 단일 요청 기반, Transaction 미지원 | JDBC / ODBC 사용 |
| Node.js + AUTH KEY | Node.js 드라이버 AUTH KEY 미지원 | JDBC / ODBC 사용 |
| Python named mapping에 `?` 사용 | 객체 입력은 `:name` SQL이 필요 | `:name`과 mapping 사용 |
| Go `sql.Named()` 사용 | 이름 기반 파라미터 미지원 | `?`와 positional argument 사용 |

## SDK별 주요 특징 요약

### JDBC

- Append: `MachStatement.executeAppendOpen()` → `executeAppendData()` → `executeAppendClose()`
- AUTH KEY: 지원 (`connectURL`에 키 파일 경로 지정)
- Transaction: Standard Edition에서 `setAutoCommit(false)`, `commit()`, `rollback()` 지원
- Transaction 시작: manual mode의 첫 Statement에서 lazy `BEGIN`
- 파라미터: `?` 또는 `:name`, `MachPreparedStatement.setObject(String, Object)`
- Prepared Parameter 메타데이터: `PreparedStatement.getParameterMetaData()`
- Nullable 메타데이터: `ResultSetMetaData.isNullable()`

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

### Go (machcli / native)

- Append: `stmt.AppendOpen()` → `stmt.AppendData()` → `stmt.AppendClose()`
- AUTH KEY: 미지원
- Transaction: 미지원 (`Begin()` 미구현)
- 파라미터: `?` 플레이스홀더, 이름 기반 API 미지원
- Nullable 메타데이터: 공개 API 없음

### Go (database/sql)

- Append: 미지원
- AUTH KEY: 미지원
- Transaction: 미지원
- 파라미터: `?` 플레이스홀더, `sql.Named()` 미지원
- 적합한 용도: 단순 SELECT, INSERT (TAG 테이블 소량), 시스템 뷰 조회
- Nullable 메타데이터: 공개 API 없음

### .NET (MachConnector)

- Append: `MachAppendWriter` 클래스 사용
- AUTH KEY: 미지원
- Transaction: 미지원 (`MachTransaction` 미구현)
- 파라미터: `MachParameterCollection`의 `:name` 사용
- 실행 방식: client-side typed literal 렌더링 후 ExecDirect
- Nullable 메타데이터: `MachDataReader.GetSchemaTable().AllowDBNull`

### REST API

- 엔드포인트: `http://host:5657/machbase`
- Append: `POST /machbase` 지원
- Transaction / Prepared Statement: 미지원
- Nullable 메타데이터: 결과 메타데이터 API 없음
- 적합한 용도: 단순 쿼리 실행, 웹 애플리케이션, 스크립팅, HTTP JSON Append

## 참조

- SDK 지원 범위 전체: [지원 범위 (SDK)](/dbms/application-integration/support-scope-sdk/)
- 기능 지원 매트릭스: [support-matrix](../support-matrix/)
- 제약 사항: [constraints-index](../constraints-index/)
