---
type: docs
title: '17.8.6 SDK별 기능 지원표'
weight: 60
---

Machbase는 다양한 프로그래밍 언어와 프로토콜을 위한 SDK를 제공합니다. 각 SDK는 지원하는 기능 범위가 다르므로, 애플리케이션 요구 사항에 맞는 SDK를 선택하는 것이 중요합니다.

## SDK별 주요 기능 지원 현황

| SDK | Append | AUTH KEY | Transaction | Prepared Statement | 비고 |
|-----|:------:|:--------:|:-----------:|:-----------------:|------|
| **JDBC** | O | O | O | O | Java 표준 JDBC 4.2 |
| **Python** | O | X | X | X | `%s` 클라이언트 렌더링, 서버 Prepared Statement 미지원 |
| **Go (native)** | O | X | X | O | `machgo` 네이티브 클라이언트 |
| **Go (database/sql)** | X | X | X | O | 표준 `database/sql` 인터페이스 |
| **.NET** | O | O | O | O | `MachConnection` / `MachCommand` |
| **Node.js** | O | X | X | O | `prepare`, `appendBatch`, `appendOpen` 지원 |
| **REST API** | O | X | X | X | HTTP JSON, 단일 요청 단위 |
| **ODBC/CLI** | O | O | O | O | C 언어 네이티브, 최고 성능 |

> 기호: O = 지원, X = 미지원

## 기능별 상세 안내

각 기능의 SDK별 상세 지원 내용은 ch8 SDK별 지원 범위 안내에서 확인하세요.

| 기능 | 참조 페이지 |
|------|-----------|
| Append API | [SDK별 APPEND 지원 범위 안내](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-append) |
| AUTH KEY 인증 | [SDK별 AUTH KEY 지원 범위 안내](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-auth-key) |
| Transaction / Prepared Statement | [SDK별 transaction / prepare / bind 지원 범위 안내](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-transaction-prepare-bind) |

## 주요 제약 사항

### Python: Prepared Statement 미지원

Python `machbaseAPI`의 커서는 서버 사이드 Prepared Statement를 지원하지 않습니다. `%s` 또는 `%(name)s` 스타일 파라미터는 클라이언트에서 렌더링하여 전송합니다.

```python
cursor = conn.cursor()
cursor.execute("INSERT INTO sensor_log VALUES (%s, %s, %s)", ['sensor01', ts, 25.3])
```

### AUTH KEY: ODBC/CLI, JDBC만 완전 지원

AUTH KEY challenge 인증은 DB 포트(기본 5656)에 접속하는 드라이버 레벨의 기능입니다. Python, Go, Node.js SDK는 현재 AUTH KEY 인증을 지원하지 않습니다.

### Go: Transaction 미지원

Go `database/sql` 드라이버와 Go native 클라이언트 모두 `Begin`/`BeginTx` 트랜잭션이 구현되어 있지 않습니다. Python `machbaseAPI`도 `begin`/`commit`/`rollback`을 지원하지 않습니다. RDB 테이블 트랜잭션이 필요한 경우 JDBC, .NET, ODBC/CLI를 사용하세요.

## SDK 선택 가이드

| 요구 사항 | 권장 SDK |
|----------|---------|
| 최고 성능 대량 쓰기 (Append) | ODBC/CLI, JDBC, Go (native), Python |
| AUTH KEY 키 기반 인증 | JDBC, ODBC/CLI, .NET |
| RDB 테이블 트랜잭션 | JDBC, .NET, ODBC/CLI |
| 웹 서비스/마이크로서비스 통합 | REST API |
| Go 표준 인터페이스 | Go (database/sql) |
| 브라우저/스크립트 연동 | Node.js, REST API |

상세 선택 규칙은 [AI Agent Reference: SDK/API 선택 규칙](/dbms/reference/ai-agent-reference/sdk-api-selection-rules/)을 참고하세요.
