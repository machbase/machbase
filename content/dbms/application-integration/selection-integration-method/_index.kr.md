---
type: docs
title: '12.1 연동 방식 선택'
weight: 10
toc: true
---
C/C++, Java, Python, .NET, Go, Node.js 등 여러 연동 경로 중 프로젝트에 가장 적합한 방식을 고르는 기준을 정리합니다.

## 이 섹션의 구성

| 문서 | 내용 |
|------|------|
| [연동 방식 선택 가이드](/dbms/application-integration/selection-integration-method/#selection-guide-integration-method) | 언어, 성능 요구사항, 환경별 선택 매트릭스와 결정 트리 |
| [SDK/API canonical owner 구분](/dbms/application-integration/selection-integration-method/#distinction-sdk-api-canonical-owner) | 각 SDK의 완전한 API 명세 위치 안내 |

## 선택 시 고려사항

연동 방식을 선택할 때는 세 가지 관점에서 검토합니다.

**개발 언어와 생태계**
프로젝트에서 사용하는 언어와 기존 라이브러리 생태계를 우선 고려합니다. Java 프로젝트라면 JDBC, Python 데이터 파이프라인이라면 Python SDK가 자연스러운 선택입니다.

**데이터 입력 성능**
지속적인 대량 시계열 데이터를 입력한다면 Append API를 지원하는 Machbase SQLCLI, ODBC, JDBC, Python SDK,
.NET, Go native, Node.js 드라이버를 검토합니다.

**운영 환경**
애플리케이션 서버에서 Machbase의 TCP 5656 포트에 연결할 수 있어야 합니다. Windows 환경의 산업용 애플리케이션이라면 .NET 드라이버나 ODBC를 우선 고려합니다.


<a id="selection-guide-integration-method"></a>

## 연동 방식 선택 가이드

프로젝트의 언어, 성능 요구사항, 운영 환경에 따라 적합한 연동 방식이 달라집니다.

### 언어별 기본 선택

| 개발 언어 | 권장 연동 방식 | 비고 |
|-----------|---------------|------|
| C / C++ (직접 연결) | Machbase SQLCLI | `<machbase_sqlcli.h>`와 Machbase 라이브러리 사용 |
| C / C++ (ODBC 환경) | ODBC | ODBC 드라이버 관리자와 DSN 사용 |
| Java | JDBC | Spring JDBC, HikariCP, MyBatis 연동 |
| Python | Python SDK (machbaseAPI) | Pandas 통합, 스크립트 자동화 |
| C# / VB.NET | .NET (MachClient) | ADO.NET 호환, Windows 친화적 |
| Go | `machgo` 또는 Go `database/sql` | native Appender, 표준 SQL 인터페이스, named bind와 트랜잭션 지원 범위가 다름 |
| JavaScript / TypeScript | Node.js 드라이버 | 웹 백엔드, IoT 게이트웨이 |

### 입력 특성별 선택

#### 지연과 처리량을 직접 제어하는 수집기

Machbase SQLCLI 또는 ODBC의 Append API를 권장합니다. C/C++로 구현된 수집 에이전트가 직접 Machbase에 데이터를 밀어넣는 구조입니다.

```
센서 → C 수집 에이전트 (Append API) → Machbase
```

#### 언어별 애플리케이션에서 지속적으로 입력하는 경우

JDBC, Python SDK, .NET, Go native, Node.js 드라이버의 Append API를 활용합니다. Java 기반 Spring Boot 수집 서비스, Python 기반 데이터 파이프라인, Go/Node.js 기반 수집 에이전트에 적합합니다.

```
IoT 게이트웨이 → Java/Python/Go/Node.js 수집 서비스 (Append API) → Machbase
```

#### 일반 트랜잭션 처리

TRANSACTION DML과 명시적 트랜잭션을 지원하는 드라이버를 선택하고 prepared statement와 connection
pool을 조합합니다. 목표 처리량은 실제 문장과 트랜잭션 크기로 측정합니다.

#### 저빈도 조회 위주 (관리, 대시보드)

운영 언어에 맞는 JDBC, Python, Go, Node.js, .NET 드라이버나 ODBC를 사용합니다. 브라우저가
Machbase에 직접 연결하지 않도록 애플리케이션 백엔드에서 쿼리를 실행하고 필요한 결과만 전달합니다.

### 환경별 선택

| 환경 | 권장 방식 | 이유 |
|------|-----------|------|
| Linux 임베디드 시스템 | Machbase SQLCLI | Machbase 라이브러리로 직접 연결 |
| Linux/Windows ODBC 환경 | ODBC | 기존 ODBC 관리자와 DSN 활용 |
| Windows 산업용 PC | ODBC 또는 .NET | Windows 생태계 호환 |
| Kubernetes / 컨테이너 | JDBC, Python, Go | 언어별 드라이버 경량 배포 |
| Grafana 연동 | JDBC 또는 ODBC 데이터 소스 | 지원 드라이버로 서버에 연결 |
| 로그 수집 파이프라인 | Fluentd 플러그인 | 이벤트·로그 수집 |

### 결정 트리

```
개발 언어가 C/C++인가?
  → YES: Machbase SQLCLI 또는 ODBC 사용
  → NO: 계속

Java인가?
  → YES: JDBC 사용 (Append API 필요 시 JDBC Append 활성화)
  → NO: 계속

Python인가?
  → YES: machbaseAPI (Python SDK) 사용
  → NO: 계속

C#/.NET인가?
  → YES: MachClient (.NET) 사용
  → NO: 계속

Go인가?
  → YES: Go 드라이버 사용
  → NO: 계속

Node.js 환경인가?
  → YES: Node.js 드라이버 사용
  → NO: 애플리케이션 언어에 맞는 JDBC, Python, Go, .NET 또는 ODBC 사용
```

### 기능 지원 매트릭스

| 기능 | Machbase SQLCLI | ODBC | JDBC | Python | .NET | Go | Node.js |
|------|:---------------:|:----:|------|--------|------|----|---------|
| Append API | O | O | O | O | O | Go native만 O | O |
| Prepared statement | O | O | O | O | O | O | O |
| Connection pool | 수동 구현 | 수동 구현 | O (HikariCP 등) | O | O | O | O |
| TRANSACTION table transaction | △ | △ | O (Standard) | - | - | Go SQL: O, native: △ | - |
| AUTH KEY 인증 | O | O | O | - | - | - | - |
| 단일 INSERT 결과 ROWID | O (Machbase 확장) | X (표준 API 없음) | O | O | O | O (`database/sql`) | O |
| Pandas 통합 | - | - | - | O | - | - | - |
| ADO.NET 호환 | - | - | - | - | O | - | - |

> `-` 는 미지원 또는 해당 없음을 의미합니다. 각 드라이버의 지원 현황은 11장 개발 도구 연동을 참조합니다.

generated ROWID는 Standard Edition에서 지원되는 단일 `INSERT ... VALUES`에만 제공됩니다.
Machbase SQLCLI 열의 `O`는 `SQLGetGeneratedRowID()` 확장을 뜻하며, ODBC 열의 `X`는
표준 ODBC API에 generated ROWID 조회 함수가 없다는 뜻입니다. 반환 API와 64비트 타입 차이는
[ROWID와 INSERT 결과 ID](../rowid-generated-id/)를 참고하십시오.

### Append API 지원 여부가 중요한 이유

Append API는 전용 세션이나 요청 형식으로 여러 행을 버퍼링하여 반복 INSERT의 네트워크 왕복과
SQL 파싱 횟수를 줄입니다. 실제 처리량과 flush 지연은 드라이버, 행 크기, 배치 크기, 네트워크와
서버 자원에 따라 측정합니다.

지속적인 대량 수집이 요구사항에 포함되면 Append API를 지원하는 드라이버를 우선 검토합니다.

자세한 동작 원리는 [Append API와 Batch INSERT](/dbms/application-integration/concepts-common/#append-api-batch)를 참조합니다.

<a id="distinction-sdk-api-canonical-owner"></a>

## SDK/API/도구별 canonical owner 구분

Machbase 문서는 역할에 따라 두 곳으로 나뉩니다.

- **12장 (이 장)**: 연동 방식 선택, 공통 개념, 실무 가이드
- **11장 개발 도구 연동**: 각 SDK의 완전한 API 명세, 함수 목록, 파라미터 상세

### SDK/드라이버별 canonical owner

| SDK / 드라이버 | 이 장(12장)에서 다루는 내용 | 11장 개발 도구 연동의 내용 |
|---------------|--------------------------|---------------------|
| **Machbase SQLCLI** | 언제 선택할지, 연결 방법 개요 | `SQLConnect`, `SQLAppendOpen`, `SQLBindParameterByName` 등 전체 함수 명세 |
| **ODBC** | 언제 선택할지, 연결 방법 개요 | `SQLConnect`, `SQLAppendOpen`, `SQLBindParameter` 등 전체 함수 명세 |
| **JDBC** | 언제 선택할지, 연결 문자열 예시 | `MachConnection`, `MachPreparedStatement`, Append API 메서드 상세 |
| **Python SDK** | 언제 선택할지, 기본 연결 패턴 | `connect()`, `cursor()`, `append()` 등 전체 메서드 명세 |
| **.NET (MachClient)** | 언제 선택할지, ADO.NET 패턴 개요 | `MachConnection`, `MachCommand`, `MachDataReader` 상세 |
| **Go 드라이버** | 언제 선택할지, database/sql 패턴 | `Open()`, `Prepare()`, Append 인터페이스 상세 |
| **Node.js 드라이버** | 언제 선택할지, 기본 사용 패턴 | 전체 API 메서드, 콜백/Promise 인터페이스 |

### 문서 구조 원칙

**12장 → "무엇을 선택하고, 어떻게 시작하는가"**

처음 Machbase에 연동하는 개발자가 읽는 장입니다. 드라이버 선택 근거, 공통 개념(인증, 타임존, 트랜잭션 범위 등), 그리고 각 드라이버의 기본 사용 패턴을 다룹니다. 코드 예제는 개념 설명 수준의 축약 예시입니다.

**11장 → "정확히 어떻게 동작하는가"**

특정 함수나 옵션의 정확한 동작을 확인해야 할 때 참조합니다. 함수 시그니처, 반환값, 에러 코드, 옵션 파라미터의 전체 목록이 있습니다.

### 외부 도구의 문서 위치

Machbase와 연동하는 외부 도구는 12장의 외부 도구 섹션에서 다룹니다.

| 도구 | 문서 위치 |
|------|-----------|
| Grafana | 12장 > 외부 도구 > Grafana |
| Fluentd | 12장 > 외부 도구 > Fluentd plugin |
| Tableau | 12장 > 외부 도구 > Tableau connector |

> 외부 도구 자체의 상세 사용법은 각 도구의 공식 문서를 참조합니다. Machbase 문서에서는 Machbase와의 연동 설정에만 집중합니다.

### 이 장에서 다루지 않는 것

- 각 SDK의 전체 함수/메서드 목록
- 드라이버 설치 및 빌드 방법 (11장 개발 도구 연동 참조)
- 드라이버별 버전 호환성 표 (11장 개발 도구 연동 참조)
