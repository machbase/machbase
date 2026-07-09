---
type: docs
title: '11.6.4 전체 SDK 기능 지원표 링크 (canonical owner: 14. 레퍼런스)'
weight: 40
---

이 페이지는 Machbase Neo가 지원하는 SDK 목록과 각 SDK의 상세 레퍼런스 위치를 안내합니다. 기능별 상세 API 레퍼런스는 **14장 레퍼런스** 섹션을 참고하세요.

## 지원 SDK 목록

| SDK | 언어 / 환경 | 연결 포트 | 상세 레퍼런스 |
|-----|------------|-----------|---------------|
| **ODBC / CLI** | C / C++ | TCP 5656 | 14장 레퍼런스 → ODBC/CLI |
| **JDBC** | Java | TCP 5656 | 14장 레퍼런스 → JDBC |
| **Python** | Python 3.7+ | TCP 5656 | 14장 레퍼런스 → Python |
| **.NET** | C# / VB.NET | TCP 5656 | 14장 레퍼런스 → .NET |
| **Go (native)** | Go 1.18+ | TCP 5656 | 14장 레퍼런스 → Go |
| **Go (database/sql)** | Go 1.18+ | TCP 5656 | 14장 레퍼런스 → Go |
| **Node.js** | JavaScript / TypeScript | TCP 5656 | 14장 레퍼런스 → Node.js |
| **REST API** | 언어 독립 (HTTP) | TCP 5657 | 14장 레퍼런스 → REST API |

## SDK 특성 요약

### ODBC / CLI (C/C++)
네이티브 C 인터페이스로 가장 낮은 레이턴시와 최대 처리량을 제공합니다. 임베디드 시스템이나 성능이 중요한 데이터 수집 에이전트에 적합합니다.

- 표준 ODBC 인터페이스 준수
- Machbase 고유 APPEND 프로토콜 지원 (`SQLAppendOpen` / `SQLAppendData` / `SQLAppendClose`)
- 전체 기능 지원

### JDBC (Java)
표준 JDBC 4.x 인터페이스를 구현하여 Spring, Hibernate, MyBatis 등 Java 생태계 프레임워크와 호환됩니다.

- HikariCP 등 커넥션 풀링 지원
- `MachStatement.executeAppendOpen()` 계열 메서드를 통한 Append API 지원
- AUTH KEY challenge 인증 지원 (Machbase 8.0 이상)

### Python
Python DB-API 2.0(PEP 249) 인터페이스를 제공합니다.

- `machbaseAPI` 패키지 사용
- Pandas DataFrame과 연계 가능
- Append API 지원

### .NET (C#)
ADO.NET 인터페이스를 구현하여 .NET 애플리케이션에서 표준적으로 사용할 수 있습니다.

- `Mach.Data.MachClient` 네임스페이스
- `MachCommand.AppendOpen()`과 `MachAppendWriter`를 통한 Append API 지원
- Entity Framework 연동 가능

### Go
두 가지 방식으로 사용할 수 있습니다.

- **Go native 드라이버**: Machbase 고유 기능(Append, 세밀한 연결 제어) 활용 가능
- **`database/sql` 인터페이스**: 표준 Go DB 추상화 레이어, 범용 ORM과 호환

### Node.js
JavaScript / TypeScript 환경에서 사용합니다.

- Promise 기반 비동기 API
- `appendBatch` / `appendOpen`을 통한 LOG/TAG Append API 지원

### REST API
HTTP 기반으로 언어·프레임워크에 독립적입니다. Machbase Neo의 HTTP 서버(포트 5657)에 직접 요청을 보냅니다.

- JSON 요청·응답
- `/machbase?q=<SQL>` (SQL 실행), `/machbase` POST (Append)
- 인증: `HTTP_AUTH` 활성화 시 Basic Authentication

## 기능별 지원 범위 상세

각 기능의 SDK별 지원 여부는 아래 페이지를 참고하세요.

- [APPEND API 지원 범위](../support-scope-sdk-append/)
- [AUTH KEY 인증 지원](../support-scope-sdk-auth-key/)
- [Transaction / Prepare / Bind 지원](../support-scope-sdk-transaction-prepare-bind/)
