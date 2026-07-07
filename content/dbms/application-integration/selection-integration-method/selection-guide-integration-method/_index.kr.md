---
type: docs
title: '연동 방식 선택 가이드'
weight: 10
---

프로젝트의 언어, 성능 요구사항, 운영 환경에 따라 적합한 연동 방식이 다릅니다. 이 문서는 선택 기준을 체계적으로 정리합니다.

## 언어별 기본 선택

| 개발 언어 | 권장 연동 방식 | 비고 |
|-----------|---------------|------|
| C / C++ | CLI/ODBC | 최저 지연, 최고 처리량 |
| Java | JDBC | Spring Boot, Hibernate 호환 |
| Python | Python SDK (machbaseAPI) | Pandas 통합, 스크립트 자동화 |
| C# / VB.NET | .NET (MachClient) | ADO.NET 호환, Windows 친화적 |
| Go | Go 드라이버 | database/sql 인터페이스 |
| JavaScript / TypeScript | Node.js 드라이버 또는 REST API | 웹 백엔드, IoT 게이트웨이 |
| 언어 무관 | REST API | HTTP 환경, 마이크로서비스 |

## 성능 요구사항별 선택

### 대용량 고속 입력 (초당 10만 건 이상)

CLI/ODBC의 Append API를 권장합니다. C/C++로 구현된 수집 에이전트가 직접 Machbase에 데이터를 밀어넣는 구조입니다.

```
센서 → C 수집 에이전트 (Append API) → Machbase
```

### 고속 입력 (초당 수천~수만 건)

JDBC, Python SDK, .NET, Go native, Node.js 드라이버의 Append API를 활용합니다. Java 기반 Spring Boot 수집 서비스, Python 기반 데이터 파이프라인, Go/Node.js 기반 수집 에이전트에 적합합니다.

```
IoT 게이트웨이 → Java/Python/Go/Node.js 수집 서비스 (Append API) → Machbase
```

### 일반 트랜잭션 처리 (초당 수백~수천 건)

어떤 드라이버도 충분히 처리합니다. Prepared statement와 connection pool을 조합하면 됩니다.

### 저빈도 조회 위주 (관리, 대시보드)

REST API도 충분합니다. 별도 드라이버 설치 없이 HTTP 요청으로 데이터를 조회할 수 있습니다.

## 환경별 선택

| 환경 | 권장 방식 | 이유 |
|------|-----------|------|
| Linux 임베디드 시스템 | CLI/ODBC | 경량, 의존성 최소 |
| Windows 산업용 PC | ODBC 또는 .NET | Windows 생태계 호환 |
| Kubernetes / 컨테이너 | JDBC, Python, Go | 언어별 드라이버 경량 배포 |
| 방화벽으로 5656 차단 | REST API (HTTP 5657) | HTTP만 허용되는 환경 |
| Grafana 연동 | Grafana 플러그인(MWA 5001 경유) | 시각화 도구 직접 연결 |
| 로그 수집 파이프라인 | Fluentd 플러그인 | 이벤트·로그 수집 |

## 결정 트리

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

## 기능 지원 매트릭스

| 기능 | CLI/ODBC | JDBC | Python | .NET | Go | Node.js | REST API |
|------|----------|------|--------|------|----|---------|----------|
| Append API | O | O | O | O | Go native만 O | O | O |
| Prepared statement | O | O | O | O | O | O | - |
| Connection pool | 수동 구현 | O (HikariCP 등) | O | O | O | O | - |
| AUTH KEY 인증 | O | O | - | - | - | - | 별도 방식 |
| Pandas 통합 | - | - | O | - | - | - | - |
| ADO.NET 호환 | - | - | - | O | - | - | - |

> `-` 는 미지원 또는 해당 없음을 의미합니다. REST API 인증은 DB 포트의 AUTH KEY challenge가 아니라 `HTTP_AUTH` 기반 Basic Authentication을 사용합니다. 각 드라이버의 최신 지원 현황은 14장 레퍼런스를 참조하세요.

## Append API 지원 여부가 중요한 이유

Machbase는 시계열 데이터베이스이므로 대부분의 운영 환경에서 **초당 수천 건 이상의 쓰기**가 발생합니다. Append API는 트랜잭션 없이 전용 세션이나 요청 형식으로 데이터를 입력하므로, 일반 INSERT 반복 실행 대비 높은 쓰기 처리량을 제공합니다.

대용량 수집이 요구사항에 포함된다면 Append API를 지원하는 드라이버를 반드시 선택하세요.

자세한 동작 원리는 [Append API와 Batch INSERT](../../concepts-common/append-api-batch/)를 참조하세요.
