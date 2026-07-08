---
type: docs
title: 'sdk-api-selection-rules'
weight: 90
---

이 페이지는 사용자의 요구사항과 언어에 따라 적합한 Machbase SDK를 선택하는 규칙을 정의합니다.

## 기능별 SDK 선택 가이드

| 요구사항 | 권장 SDK | 비고 |
|----------|----------|------|
| Append 필요 + Java | **JDBC** (`MachStatement.executeAppendOpen()`) | [JDBC 가이드](../../../application-integration/guide-drivers/jdbc/) |
| Append 필요 + Python | **machbaseAPI** (`machbase()` 클래스의 `append()`) | [Python 가이드](../../../application-integration/guide-drivers/python/) |
| Append 필요 + Go | **machcli** (native client) | `database/sql`은 Append 미지원 |
| Append 필요 + .NET | **MachConnector** (`MachAppendWriter`) | [.NET 가이드](../../../application-integration/guide-drivers/.net/) |
| Append 필요 + Node.js | **machbase-node** | [Node.js 가이드](../../../application-integration/guide-drivers/node/) |
| AUTH KEY 인증 필요 | **JDBC**, **Python(machbaseAPI)**, **.NET**, **ODBC/CLI** | Node.js는 현재 AUTH KEY 미지원 |
| RDB 테이블 트랜잭션 필요 | **JDBC**, **Python(machbaseAPI)**, **.NET**, **ODBC/CLI** | Go는 Transaction 미지원 |
| Go 언어 선호 + Append 필요 | **machcli** (native) | [Go 가이드](../../../application-integration/guide-drivers/go/) |
| Go 언어 선호 + 표준 인터페이스 | **database/sql** 드라이버 | Append 불필요한 경우 |
| 브라우저 / 웹 / 스크립트 | **REST API** (포트 5657, `/machbase` 엔드포인트) | [REST API 가이드](../../../application-integration/guide-drivers/rest-api/) |
| 데이터 탐색 / 보고 | **R + RODBC** | 통계 분석에 적합 |
| C/C++ 애플리케이션 | **ODBC/CLI** | [ODBC 가이드](../../../application-integration/guide-drivers/odbc-cli/) |

## 언어별 권장 SDK 요약

| 언어 | 기본 권장 | Append 필요 시 | Transaction 필요 시 |
|------|----------|---------------|---------------------|
| Java | JDBC | JDBC (executeAppendOpen) | JDBC |
| Python | machbaseAPI | machbaseAPI (append()) | machbaseAPI |
| Go | database/sql | machcli (native) | 미지원 (다른 SDK 고려) |
| C# / .NET | MachConnector | MachConnector (MachAppendWriter) | MachConnector |
| Node.js | machbase-node | machbase-node | 미지원 |
| C / C++ | ODBC/CLI | ODBC/CLI | ODBC/CLI |
| R | RODBC | 미지원 | 미지원 |
| 웹 / curl / HTTP | REST API | 미지원 | 미지원 |

## 피해야 할 조합

| 조합 | 이유 | 대안 |
|------|------|------|
| Go `database/sql` + Append | Append 미지원 | `machcli` (native) 사용 |
| Go + Transaction (BEGIN/COMMIT) | `Begin()` / `BeginTx()` 미구현 | ODBC 또는 JDBC 사용 |
| REST API + Transaction | REST API는 단일 요청 기반, Transaction 미지원 | JDBC / .NET 사용 |
| REST API + Append | Append 프로토콜은 HTTP 미지원 | JDBC / Python / Go(machcli) 사용 |
| Node.js + AUTH KEY | 현재 Node.js 드라이버 AUTH KEY 미지원 | JDBC / Python / .NET 사용 |
| Python `%s` → `?` 플레이스홀더 | machbaseAPI는 `%s` 방식 전용 | `%s` 또는 `%(name)s` 사용 |

## SDK별 주요 특징 요약

### JDBC

- Append: `MachStatement.executeAppendOpen()` → `executeAppendData()` → `executeAppendClose()`
- AUTH KEY: 지원 (`connectURL`에 키 파일 경로 지정)
- Transaction: 지원 (RDB/LOOKUP 테이블)
- 파라미터: `?` 플레이스홀더

### Python (machbaseAPI)

- Append: `conn.append(table, cols, data)` 또는 `machbase()` 클래스
- AUTH KEY: 지원
- Transaction: 지원 (RDB/LOOKUP 테이블)
- 파라미터: `%s` 또는 `%(name)s` (서버 Prepared Statement 미지원, 클라이언트 렌더링)

### Go (machcli / native)

- Append: `stmt.AppendOpen()` → `stmt.AppendData()` → `stmt.AppendClose()`
- AUTH KEY: 지원
- Transaction: 미지원 (`Begin()` 미구현)
- 파라미터: `?` 플레이스홀더

### Go (database/sql)

- Append: 미지원
- AUTH KEY: 지원
- Transaction: 미지원
- 파라미터: `?` 플레이스홀더
- 적합한 용도: 단순 SELECT, INSERT (TAG 테이블 소량), 시스템 뷰 조회

### .NET (MachConnector)

- Append: `MachAppendWriter` 클래스 사용
- AUTH KEY: 지원
- Transaction: 지원
- 파라미터: `?` 플레이스홀더

### REST API

- 엔드포인트: `http://host:5657/machbase`
- Append / Transaction / Prepared Statement: 모두 미지원
- 적합한 용도: 단순 쿼리 실행, 웹 애플리케이션, 스크립팅

## 참조

- SDK 지원 범위 전체: [지원 범위 (SDK)](../../../application-integration/support-scope-sdk/)
- 기능 지원 매트릭스: [support-matrix](../support-matrix/)
- 제약 사항: [constraints-index](../constraints-index/)
