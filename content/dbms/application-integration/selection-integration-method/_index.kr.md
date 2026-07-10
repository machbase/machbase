---
type: docs
title: '11.1 연동 방식 선택'
weight: 10
toc: true
---
C/C++, Java, Python, .NET, Go, Node.js, REST API 등 여러 연동 경로 중 프로젝트에 가장 적합한 방식을 고르는 기준을 정리합니다.

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
초당 수만 건 이상의 대용량 시계열 데이터를 입력해야 한다면 Append API를 지원하는 CLI/ODBC, JDBC, Python SDK, .NET, Go native, Node.js 드라이버가 적합합니다. REST API도 `/machbase` POST Append를 지원하지만 HTTP JSON 요청 단위로 동작하므로 네이티브 드라이버가 어려운 환경에서 우선 검토합니다.

**운영 환경**
방화벽으로 인해 TCP 5656 포트를 사용할 수 없는 환경이라면 HTTP 기반 REST API를 검토합니다. Windows 환경의 산업용 애플리케이션이라면 .NET 드라이버나 ODBC를 우선 고려합니다.


<a id="selection-guide-integration-method"></a>

## 연동 방식 선택 가이드

프로젝트의 언어, 성능 요구사항, 운영 환경에 따라 적합한 연동 방식이 달라집니다.

### 언어별 기본 선택

| 개발 언어 | 권장 연동 방식 | 비고 |
|-----------|---------------|------|
| C / C++ | CLI/ODBC | 최저 지연, 최고 처리량 |
| Java | JDBC | Spring Boot, Hibernate 호환 |
| Python | Python SDK (machbaseAPI) | Pandas 통합, 스크립트 자동화 |
| C# / VB.NET | .NET (MachClient) | ADO.NET 호환, Windows 친화적 |
| Go | Go 드라이버 | database/sql 인터페이스 |
| JavaScript / TypeScript | Node.js 드라이버 또는 REST API | 웹 백엔드, IoT 게이트웨이 |
| 언어 무관 | REST API | HTTP 환경, 마이크로서비스 |

### 성능 요구사항별 선택

#### 대용량 고속 입력 (초당 10만 건 이상)

CLI/ODBC의 Append API를 권장합니다. C/C++로 구현된 수집 에이전트가 직접 Machbase에 데이터를 밀어넣는 구조입니다.

```
센서 → C 수집 에이전트 (Append API) → Machbase
```

#### 고속 입력 (초당 수천~수만 건)

JDBC, Python SDK, .NET, Go native, Node.js 드라이버의 Append API를 활용합니다. Java 기반 Spring Boot 수집 서비스, Python 기반 데이터 파이프라인, Go/Node.js 기반 수집 에이전트에 적합합니다.

```
IoT 게이트웨이 → Java/Python/Go/Node.js 수집 서비스 (Append API) → Machbase
```

#### 일반 트랜잭션 처리 (초당 수백~수천 건)

어떤 드라이버든 충분히 처리할 수 있습니다. Prepared statement와 connection pool을 조합하면 됩니다.

#### 저빈도 조회 위주 (관리, 대시보드)

REST API만으로 충분합니다. 별도 드라이버 설치 없이 HTTP 요청으로 데이터를 조회할 수 있습니다.

### 환경별 선택

| 환경 | 권장 방식 | 이유 |
|------|-----------|------|
| Linux 임베디드 시스템 | CLI/ODBC | 경량, 의존성 최소 |
| Windows 산업용 PC | ODBC 또는 .NET | Windows 생태계 호환 |
| Kubernetes / 컨테이너 | JDBC, Python, Go | 언어별 드라이버 경량 배포 |
| 방화벽으로 5656 차단 | REST API (HTTP 5657) | HTTP만 허용되는 환경 |
| Grafana 연동 | Grafana 플러그인(MWA 5001 경유) | 시각화 도구 직접 연결 |
| 로그 수집 파이프라인 | Fluentd 플러그인 | 이벤트·로그 수집 |

### 결정 트리

```
개발 언어가 C/C++인가?
  → YES: CLI/ODBC 사용
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

Node.js 또는 HTTP 환경인가?
  → YES: Node.js 드라이버 또는 REST API
  → NO: REST API (언어 무관)
```

### 기능 지원 매트릭스

| 기능 | CLI/ODBC | JDBC | Python | .NET | Go | Node.js | REST API |
|------|----------|------|--------|------|----|---------|----------|
| Append API | O | O | O | O | Go native만 O | O | O |
| Prepared statement | O | O | O | O | O | O | - |
| Connection pool | 수동 구현 | O (HikariCP 등) | O | O | O | O | - |
| AUTH KEY 인증 | O | O | - | - | - | - | 별도 방식 |
| Pandas 통합 | - | - | O | - | - | - | - |
| ADO.NET 호환 | - | - | - | O | - | - | - |

> `-` 는 미지원 또는 해당 없음을 의미합니다. REST API 인증은 DB 포트의 AUTH KEY challenge가
> 아니라 `HTTP_AUTH` 기반 Basic Authentication을 사용합니다. 각 드라이버의 지원 현황은
> 17장 레퍼런스를 참조합니다.

### Append API 지원 여부가 중요한 이유

Machbase는 시계열 데이터베이스이므로 대부분의 운영 환경에서 **초당 수천 건 이상의 쓰기**가 발생합니다. Append API는 트랜잭션 없이 전용 세션이나 요청 형식으로 데이터를 입력하므로, 일반 INSERT 반복 실행 대비 훨씬 높은 쓰기 처리량을 제공합니다.

대용량 수집이 요구사항에 포함된다면 Append API를 지원하는 드라이버를 반드시 선택해야 합니다.

자세한 동작 원리는 [Append API와 Batch INSERT](/dbms/application-integration/concepts-common/#append-api-batch)를 참조합니다.

<a id="distinction-sdk-api-canonical-owner"></a>

## SDK/API/도구별 canonical owner 구분

Machbase 문서는 역할에 따라 두 곳으로 나뉩니다.

- **8장 (이 장)**: 연동 방식 선택, 공통 개념, 실무 가이드
- **17장 레퍼런스**: 각 SDK의 완전한 API 명세, 함수 목록, 파라미터 상세

### SDK/드라이버별 canonical owner

| SDK / 드라이버 | 이 장(11장)에서 다루는 내용 | 17장 레퍼런스의 내용 |
|---------------|--------------------------|---------------------|
| **CLI/ODBC** | 언제 선택할지, 연결 방법 개요 | `SQLConnect`, `SQLAppendOpen`, `SQLBindParameter` 등 전체 함수 명세 |
| **JDBC** | 언제 선택할지, 연결 문자열 예시 | `MachConnection`, `MachPreparedStatement`, Append API 메서드 상세 |
| **Python SDK** | 언제 선택할지, 기본 연결 패턴 | `connect()`, `cursor()`, `append()` 등 전체 메서드 명세 |
| **.NET (MachClient)** | 언제 선택할지, ADO.NET 패턴 개요 | `MachConnection`, `MachCommand`, `MachDataReader` 상세 |
| **Go 드라이버** | 언제 선택할지, database/sql 패턴 | `Open()`, `Prepare()`, Append 인터페이스 상세 |
| **Node.js 드라이버** | 언제 선택할지, 기본 사용 패턴 | 전체 API 메서드, 콜백/Promise 인터페이스 |
| **REST API** | 언제 선택할지, 엔드포인트 개요 | 전체 엔드포인트 목록, 요청/응답 형식, 인증 방법 |

### 문서 구조 원칙

**8장 → "무엇을 선택하고, 어떻게 시작하는가"**

처음 Machbase에 연동하는 개발자가 읽는 장입니다. 드라이버 선택 근거, 공통 개념(인증, 타임존, 트랜잭션 범위 등), 그리고 각 드라이버의 기본 사용 패턴을 다룹니다. 코드 예제는 개념 설명 수준의 축약 예시입니다.

**17장 → "정확히 어떻게 동작하는가"**

특정 함수나 옵션의 정확한 동작을 확인해야 할 때 참조합니다. 함수 시그니처, 반환값, 에러 코드, 옵션 파라미터의 전체 목록이 있습니다.

### 외부 도구의 문서 위치

Machbase와 연동하는 외부 도구는 8장의 외부 도구 섹션에서 다룹니다.

| 도구 | 문서 위치 |
|------|-----------|
| Grafana | 8장 > 외부 도구 > Grafana plugin |
| Fluentd | 8장 > 외부 도구 > Fluentd plugin |
| Tableau | 8장 > 외부 도구 > Tableau connector |

> 외부 도구 자체의 상세 사용법은 각 도구의 공식 문서를 참조합니다. Machbase 문서에서는 Machbase와의 연동 설정에만 집중합니다.

### 이 장에서 다루지 않는 것

- 각 SDK의 전체 함수/메서드 목록
- 드라이버 설치 및 빌드 방법 (17장 레퍼런스 참조)
- 드라이버별 버전 호환성 표 (17장 레퍼런스 참조)
- REST API 전체 엔드포인트 명세 (17장 레퍼런스 참조)
