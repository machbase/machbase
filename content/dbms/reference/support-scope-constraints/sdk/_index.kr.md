---
type: docs
title: '18.6.6 SDK별 기능 지원표'
weight: 60
toc: true
---

Machbase는 다양한 프로그래밍 언어를 위한 SDK를 제공합니다. 각 SDK는 지원하는 기능 범위가 다르므로, 애플리케이션 요구 사항에 맞는 SDK를 선택하는 것이 중요합니다.

## SDK별 주요 기능 지원 현황

| SDK | Append | AUTH KEY | Transaction API | Server Prepared | Named Bind API | Nullable 메타데이터 | 초기 database |
|-----|:------:|:--------:|:---------------:|:---------------:|:--------------:|:-------------------:|:--------------:|
| **JDBC** | O | O | O | O | O | O | O |
| **Python** | O | X | X | O | O | O | O |
| **Go (native)** | O | X | △ | O | O | O | v1.8.3+ `api.WithDatabase()` 또는 SQL `USE` |
| **Go (database/sql)** | △ | X | O | O | O | O | v1.8.3+ DSN `database`/`db`, URL path/query |
| **.NET** | O | X | X | X | △ | O | O (initial) |
| **Node.js** | O | X | X | O | O | O | O |
| **Machbase SQLCLI** | O | O | △ | O | O | O | O |
| **ODBC** | O | O | △ | O | △ | O | O |

> 기호: O = 지원, △ = SDK별로 제한된 방식으로 지원, X = 미지원
>
> Go `database/sql`의 Transaction API는 기본 isolation level의 읽기/쓰기 트랜잭션에 한하며,
> named bind와 DECIMAL/NULL/PRIMARY KEY 메타데이터는 Machbase 8.7.0 서버와 해당 버전용
> 클라이언트 SDK를 기준으로 합니다.
> Go `database/sql`의 Append는 표준 `sql.DB`/`sql.Tx` API에 없지만, neo-client의 `machbase.Conn.Appender()`를
> `sql.Conn.Raw()`에서 선택적으로 사용할 수 있습니다. 신규 대량 입력에는 native `machgo`를 권장합니다.
>
> Python 2.4는 `cursor(prepared=True)`로 동일 SQL의 server statement를 여러
> `execute()`와 `executemany()` 호출에서 재사용합니다. 일반 cursor의 기존 일회성 실행
> 방식도 유지합니다. .NET은 이름 컬렉션을 client-side typed literal로 렌더링한 뒤
> ExecDirect로 실행합니다. 이름 기반 API는 Machbase SQLCLI에서만 제공되며 ODBC는 ordinal
> `SQLBindParameter()`를 사용합니다.

## 기능별 상세 안내

다중 데이터베이스는 Standard Edition에서 지원합니다. client별 초기 database 선택과
catalog 변경, connection pool 주의사항은 [다중 데이터베이스 운영 가이드](/dbms/operations-configuration-recovery/multi-database/#9-client에서-데이터베이스-선택)를
참조하십시오. 다중 데이터베이스를 사용할 때는 Machbase 8.7.0 서버와 해당 버전용 클라이언트
SDK를 함께 사용합니다.

각 기능의 SDK별 상세 지원 내용은 [11장 개발 도구 연동의 SDK 지원 범위](/dbms/development-tools-integration/#sdk)에서 확인하십시오.

| 기능 | 참조 페이지 |
|------|-----------|
| Append API | [SDK별 APPEND 지원 범위 안내](/dbms/development-tools-integration/#support-scope-sdk-append) |
| AUTH KEY 인증 | [SDK별 AUTH KEY 지원 범위 안내](/dbms/development-tools-integration/#support-scope-sdk-auth-key) |
| Transaction / Prepared Statement | [SDK별 transaction / prepare / bind 지원 범위 안내](/dbms/development-tools-integration/#support-scope-sdk-transaction-prepare-bind) |
| Named Bind Parameter | [Named Bind Parameter syntax](/dbms/reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/) |
| Nullable 메타데이터 | [SELECT 결과 Nullable 메타데이터 지원](/dbms/development-tools-integration/#support-scope-sdk-nullable-metadata) |
| PRIMARY KEY 메타데이터 | [SELECT 결과·카탈로그 PRIMARY KEY 지원](/dbms/development-tools-integration/#support-scope-sdk-primary-key-metadata) |

## 주요 제약 사항

### Python: Prepared Cursor

Python `machbaseAPI` 2.4는 `cursor(prepared=True)`를 제공합니다. prepared cursor는
동일한 원본 SQL 문자열에 대해 cached server statement를 재사용하고, SQL이 달라지거나
cursor를 닫을 때 기존 statement를 해제합니다.

```python
cursor = conn.cursor(prepared=True)
cursor.execute(
    "INSERT INTO sensor_log VALUES (%s, %s, %s)",
    ("sensor01", ts, 25.3),
)
```

cursor 하나는 server statement 하나만 보유합니다. 여러 SQL을 각각 계속 재사용해야 하면
SQL별 prepared cursor를 생성합니다. `%s`, `?`, `%(name)s`, `:name`을 지원하며 named
marker에는 Machbase 8.7.0 서버와 해당 버전용 클라이언트 SDK가 필요합니다.

### AUTH KEY: SQLCLI, ODBC, JDBC만 완전 지원

AUTH KEY challenge 인증은 DB 포트(기본 5656)에 접속하는 드라이버 레벨의 기능입니다. Python, Go, Node.js SDK는 현재 AUTH KEY 인증을 지원하지 않습니다.

### Go: Transaction 지원 범위

Go `database/sql` 드라이버는 기본 isolation level에서 `Begin`/`BeginTx`, `Commit`, `Rollback`을
제공합니다. Go native 클라이언트에는 전용 `Begin` 메서드가 없지만 같은 연결에서 `BEGIN`,
`COMMIT`, `ROLLBACK` SQL을 직접 실행할 수 있습니다. Python `machbaseAPI`는
`begin`/`commit`/`rollback`을 지원하지 않으며, `.NET`의 `MachTransaction`도 구현되어 있지
않습니다. Standard Edition의 TRANSACTION 테이블에는 Go SQL 드라이버의 `BeginTx` 또는
JDBC의 `setAutoCommit(false)`, `commit()`, `rollback()`을 사용할 수 있습니다.

### Go: Nullable 메타데이터

Go native는 `api.Column.Nullability`, Go `database/sql`은 `Rows.ColumnTypeNullable()`로
SELECT 결과 컬럼의 Nullable 상태를 조회할 수 있습니다. 두 API 모두 서버가 정보를 알 수
없는 경우 unknown 상태를 반환할 수 있으므로 실제 scan에는 nullable 대상 타입을 사용합니다.

### PRIMARY KEY 결과 메타데이터

Go native는 `api.Column.PrimaryKey`로 직접 컬럼의 PK 상태를 확인할 수 있습니다. Go
`database/sql`의 표준 `ColumnType`에는 PK 메서드가 없으므로 native API 또는 카탈로그 SQL을
사용합니다. JDBC, Python, Node.js, .NET, ODBC는 각각의 결과 메타데이터 또는 카탈로그 API로
PK를 조회할 수 있습니다. 상세한 API 이름과 직접 컬럼·표현식의 차이는
[PRIMARY KEY 메타데이터 지원 범위](/dbms/development-tools-integration/#support-scope-sdk-primary-key-metadata)를
참고하십시오.

## SDK 선택 가이드

| 요구 사항 | 권장 SDK |
|----------|---------|
| 지속적인 대량 쓰기 (Append) | Machbase SQLCLI, ODBC, JDBC, Go (native), Python |
| AUTH KEY 키 기반 인증 | JDBC, Machbase SQLCLI, ODBC, machsql |
| TRANSACTION 테이블 트랜잭션 | Go (`database/sql`), JDBC 표준 Connection API, Machbase SQLCLI, ODBC |
| SELECT 결과의 NULL 가능 여부 확인 | Go, Machbase SQLCLI, ODBC, JDBC, Python, Node.js, .NET |
| 웹 서비스/마이크로서비스 통합 | 백엔드 언어용 JDBC, Python, Go, Node.js, .NET 또는 ODBC |
| Go 표준 인터페이스 | Go (database/sql) |
| 브라우저/스크립트 연동 | Node.js 또는 Python 기반 백엔드 |

상세 선택 규칙은 [AI Agent Reference: SDK/API 선택 규칙](/dbms/reference/ai-agent-reference/sdk-api-selection-rules/)을 참고하십시오.
