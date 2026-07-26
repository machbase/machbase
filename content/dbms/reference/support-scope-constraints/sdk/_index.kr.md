---
type: docs
title: '17.8.6 SDK별 기능 지원표'
weight: 60
toc: true
---

Machbase는 다양한 프로그래밍 언어와 프로토콜을 위한 SDK를 제공합니다. 각 SDK는 지원하는 기능 범위가 다르므로, 애플리케이션 요구 사항에 맞는 SDK를 선택하는 것이 중요합니다.

## SDK별 주요 기능 지원 현황

| SDK | Append | AUTH KEY | Transaction API | Server Prepared | Named Bind API | Nullable 메타데이터 |
|-----|:------:|:--------:|:---------------:|:---------------:|:--------------:|:-------------------:|
| **JDBC** | O | O | △ | O | O | O |
| **Python** | O | X | X | O | O | O |
| **Go (native)** | O | X | X | O | X | X |
| **Go (database/sql)** | X | X | X | O | X | X |
| **.NET** | O | X | X | X | △ | O |
| **Node.js** | O | X | X | O | O | O |
| **REST API** | O | X | X | X | X | X |
| **ODBC/CLI** | O | O | △ | O | △ | O |

> 기호: O = 지원, △ = SDK별로 제한된 방식으로 지원, X = 미지원
>
> Python은 서버 prepare/bind를 지원합니다. `execute()`는 호출마다 prepare하고 닫으며,
> `executemany()`는 한 번 prepare한 statement를 호출 내부에서 재사용합니다. 공개
> `prepare()` 객체는 없습니다. .NET은 이름 컬렉션을 client-side typed literal로 렌더링한
> 뒤 ExecDirect로 실행합니다. ODBC/CLI의 이름 API는 SQLCLI에서만 제공되며 ODBC는 ordinal
> `SQLBindParameter()`를 사용합니다.

## 기능별 상세 안내

각 기능의 SDK별 상세 지원 내용은 11장 SDK별 지원 범위 안내에서 확인하십시오.

| 기능 | 참조 페이지 |
|------|-----------|
| Append API | [SDK별 APPEND 지원 범위 안내](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-append) |
| AUTH KEY 인증 | [SDK별 AUTH KEY 지원 범위 안내](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-auth-key) |
| Transaction / Prepared Statement | [SDK별 transaction / prepare / bind 지원 범위 안내](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-transaction-prepare-bind) |
| Named Bind Parameter | [Named Bind Parameter syntax](/dbms/reference/sql/syntax-dictionary-sql/named-bind-parameter-syntax/) |
| Nullable 메타데이터 | [SELECT 결과 Nullable 메타데이터 지원](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-nullable-metadata) |

## 주요 제약 사항

### Python: 명시적 Prepared Statement 객체 미지원

Python `machbaseAPI`는 Server Prepared Statement를 지원하지만 별도의 공개 `prepare()`
객체를 제공하지 않습니다. `:name` SQL과 mapping을 사용하면 `execute()`는 호출마다
prepare/execute/close하고, `executemany()`는 한 번 prepare한 뒤 각 mapping을 실행하고
닫습니다. 따라서 statement를 여러 `execute()` 호출에 걸쳐 직접 재사용할 수는 없습니다.
기존 `%s` 또는 `%(name)s` 형식은 클라이언트 렌더링 방식으로 유지됩니다.

```python
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO sensor_log VALUES (:name, :time, :value)",
    {"name": "sensor01", "time": ts, "value": 25.3},
)
```

### AUTH KEY: ODBC/CLI, JDBC만 완전 지원

AUTH KEY challenge 인증은 DB 포트(기본 5656)에 접속하는 드라이버 레벨의 기능입니다. Python, Go, Node.js SDK는 현재 AUTH KEY 인증을 지원하지 않습니다.

### Go: Transaction 미지원

Go `database/sql` 드라이버와 Go native 클라이언트 모두 `Begin`/`BeginTx` 트랜잭션이 구현되어
있지 않습니다. Python `machbaseAPI`도 `begin`/`commit`/`rollback`을 지원하지 않으며,
`.NET`의 `MachTransaction`도 구현되어 있지 않습니다. TRANSACTION 테이블 트랜잭션은 SQL `BEGIN`을 직접
실행할 수 있는 JDBC 또는 ODBC/CLI 경로를 사용합니다.

### Go와 REST API: Nullable 메타데이터 미지원

Go native, Go `database/sql`, REST API에는 SELECT 결과 컬럼의 Nullable 상태를 조회하는
공개 API가 없습니다. 결과를 읽기 전에 NULL 가능 여부를 확인해야 하는 애플리케이션은
Native MachCLI, SQLCLI/ODBC, JDBC, Python, Node.js 또는 .NET을 사용합니다.

## SDK 선택 가이드

| 요구 사항 | 권장 SDK |
|----------|---------|
| 지속적인 대량 쓰기 (Append) | ODBC/CLI, JDBC, Go (native), Python |
| AUTH KEY 키 기반 인증 | JDBC, ODBC/CLI, machsql |
| TRANSACTION 테이블 트랜잭션 | JDBC, ODBC/CLI (SQL `BEGIN` 직접 실행) |
| SELECT 결과의 NULL 가능 여부 확인 | ODBC/CLI, JDBC, Python, Node.js, .NET |
| 웹 서비스/마이크로서비스 통합 | REST API |
| Go 표준 인터페이스 | Go (database/sql) |
| 브라우저/스크립트 연동 | Node.js, REST API |

상세 선택 규칙은 [AI Agent Reference: SDK/API 선택 규칙](/dbms/reference/ai-agent-reference/sdk-api-selection-rules/)을 참고하십시오.
