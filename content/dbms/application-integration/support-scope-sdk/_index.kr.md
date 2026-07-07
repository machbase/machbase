---
type: docs
title: 'SDK별 지원 범위 안내'
weight: 60
---

Machbase Neo는 다양한 프로그래밍 언어와 프로토콜을 위한 SDK를 제공합니다. 각 SDK는 지원하는 기능 범위가 다르므로, 애플리케이션 요구 사항에 맞는 SDK를 선택하는 것이 중요합니다.

이 섹션에서는 SDK별 주요 기능 지원 여부를 정리합니다.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [전체 SDK 기능 지원표](sdk/) | 지원 SDK 목록 및 14장 레퍼런스 링크 |
| [APPEND API 지원 범위](support-scope-sdk-append/) | SDK별 고성능 Append 쓰기 지원 여부 |
| [AUTH KEY 인증 지원](support-scope-sdk-auth-key/) | SDK별 AUTH KEY 인증 방식 지원 여부 |
| [Transaction / Prepare / Bind 지원](support-scope-sdk-transaction-prepare-bind/) | SDK별 트랜잭션·Prepared Statement·파라미터 바인딩 지원 여부 |

## SDK 선택 기이드

애플리케이션 특성에 따라 아래를 참고하세요.

- **최고 성능의 대량 쓰기**가 필요하다면 → ODBC/CLI 또는 JDBC의 Append API 사용
- **표준 SQL 인터페이스**가 필요하다면 → JDBC, Python(DB-API 2.0), Go(`database/sql`)
- **웹 서비스·마이크로서비스 통합**이 필요하다면 → REST API
- **트랜잭션이 필요한 RDB 호환 작업**이 필요하다면 → ODBC/CLI, JDBC, Python, .NET, Go(`database/sql`)

> **참고**: TAG 테이블과 LOG 테이블은 Append-only 구조로, 트랜잭션이 필요 없는 고속 스트리밍 쓰기에 최적화되어 있습니다.
