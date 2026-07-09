---
type: docs
title: '11. 애플리케이션 연동'
weight: 110
---

Machbase는 다양한 프로그래밍 언어와 프로토콜을 통해 애플리케이션에 연동할 수 있습니다. 이 장에서는 각 연동 방식의 특성을 설명하고, 상황에 맞는 방식을 선택할 수 있도록 안내합니다.

## 연동 방식 개요

| 연동 방식 | 언어/환경 | 대표 use case |
|-----------|-----------|---------------|
| **CLI/ODBC** | C, C++ | 임베디드 시스템, 최대 성능이 요구되는 수집기 |
| **JDBC** | Java | Spring Boot 기반 백엔드, 엔터프라이즈 애플리케이션 |
| **Python** | Python | 데이터 분석, 스크립트 기반 수집, Pandas 연동 |
| **.NET** | C#, VB.NET | Windows 환경의 산업용 애플리케이션, ADO.NET |
| **Go** | Go | 고성능 수집 에이전트, 클라우드 네이티브 마이크로서비스 |
| **Node.js** | JavaScript/TypeScript | 실시간 웹 대시보드, IoT 게이트웨이 |
| **REST API** | 언어 독립 | 웹 프론트엔드, 마이크로서비스, HTTP 전용 환경 |
| **외부 도구** | Grafana, Fluentd, Tableau | 시각화, 로그 수집, BI 도구 연동 |

## 하위 섹션

이 장은 연동 방식 선택, 공통 개념, 드라이버별 가이드, REST API, 외부 도구 연동으로 구성됩니다.

### 연동 방식 선택

어떤 드라이버나 API를 선택할지 결정하는 데 도움이 되는 가이드입니다.

| 문서 | 내용 |
|------|------|
| [연동 방식 선택 가이드](/dbms/application-integration/selection-integration-method/#selection-guide-integration-method) | 사용 목적, 언어, 성능 요구사항별 선택 매트릭스 |
| [SDK/API canonical owner 구분](/dbms/application-integration/selection-integration-method/#distinction-sdk-api-canonical-owner) | 각 SDK의 완전한 API 명세가 어느 장에 있는지 안내 |

### 공통 연동 개념

드라이버나 언어에 관계없이 Machbase 연동 시 공통으로 이해해야 할 개념입니다.

| 문서 | 내용 |
|------|------|
| [연결 문자열과 인증](/dbms/application-integration/concepts-common/#connection-string-authentication) | HOST:PORT, SYS/MANAGER, AUTH KEY, connection pool |
| [타임존 연결 옵션](/dbms/application-integration/concepts-common/#timezone-connection) | UTC 내부 저장, 연결 시 timezone 설정, SYSDATE vs NOW |
| [Prepared statement](/dbms/application-integration/concepts-common/#prepared-statement) | SQL 인젝션 방지, 재사용 성능, TAG/LOG 테이블 지원 |
| [Parameter binding](/dbms/application-integration/concepts-common/#parameter-binding) | 위치 바인딩, DATETIME nanosecond 처리, NULL 값 |
| [트랜잭션 처리](/dbms/application-integration/concepts-common/#transaction) | RDB: ACID 완전 지원, TAG/LOG: append-only 비트랜잭션 |
| [Append API와 Batch INSERT](/dbms/application-integration/concepts-common/#append-api-batch) | 고속 비트랜잭션 입력 vs 트랜잭션 기반 배치 INSERT |
| [오류 처리와 재시도](/dbms/application-integration/concepts-common/#error-handling-retry) | 오류 코드, exponential backoff, connection pool 격리 |

### 드라이버별 가이드와 REST API

| 문서 | 내용 |
|------|------|
| [드라이버별 가이드](guide-drivers/) | CLI/ODBC, JDBC, Python, .NET, Go, Node.js, R/RODBC 사용 패턴 |
| [REST API](rest-api/) | `/machbase` SQL 실행과 POST Append, 인증 및 오류 처리 |
| [SDK별 지원 범위 안내](support-scope-sdk/) | Append, AUTH KEY, Transaction/Prepare/Bind 지원 범위 |

### 외부 도구 연동

| 문서 | 내용 |
|------|------|
| [외부 도구](external-tools/) | Grafana 플러그인, Fluentd 플러그인, Tableau JDBC/ODBC 연결 |

## 각 드라이버의 완전한 API 명세 위치

이 장(8장)은 연동 방식에 대한 **실무 가이드**입니다. 각 드라이버의 완전한 API 명세와 레퍼런스는 **14장 레퍼런스**에 있습니다.

```
8장 (이 장)  → 연동 방식 선택, 공통 개념, 실무 예제
14장 레퍼런스 → 각 SDK의 완전한 API 명세, 함수 목록, 옵션 상세
```

## 빠른 시작

처음 연동을 시도한다면 다음 순서를 권장합니다.

1. [연동 방식 선택 가이드](/dbms/application-integration/selection-integration-method/#selection-guide-integration-method)에서 환경에 맞는 드라이버를 결정합니다.
2. [연결 문자열과 인증](/dbms/application-integration/concepts-common/#connection-string-authentication)에서 기본 연결 방법을 확인합니다.
3. 사용 패턴에 따라 [Append API](/dbms/application-integration/concepts-common/#append-api-batch) 또는 [Prepared statement](/dbms/application-integration/concepts-common/#prepared-statement)를 선택합니다.
4. 14장 레퍼런스에서 해당 드라이버의 상세 API를 참조합니다.
