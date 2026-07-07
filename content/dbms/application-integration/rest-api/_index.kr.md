---
type: docs
title: 'REST API 연동'
weight: 40
---

Machbase는 HTTP 기반의 REST API를 제공하여 특정 드라이버나 SDK 없이 모든 언어와 환경에서 데이터베이스에 접근할 수 있습니다. curl, wget, Python requests, JavaScript fetch 등 HTTP를 지원하는 모든 도구에서 바로 사용할 수 있습니다.

## REST API 포트

REST API는 DB 연결 포트(5656)와 **별도의 포트(5657)**를 사용합니다.

| 포트 | 용도 |
|------|------|
| 5656 | ODBC/JDBC/네이티브 드라이버 연결 |
| **5657** | **REST API (HTTP)** |

기본 URL 구조는 다음과 같습니다.

```
http://<host>:5657/<endpoint>
```

예를 들어 로컬 서버에 접속하는 경우 기본 URL은 `http://127.0.0.1:5657`입니다.

## 주요 API 엔드포인트

Machbase REST API는 세 가지 주요 엔드포인트로 구성됩니다.

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/db/query` | POST | SQL 실행 및 결과 반환 (SELECT, INSERT, DDL 모두 지원) |
| `/db/append/{table_name}` | POST | 대용량 데이터 고속 삽입 (Append 프로토콜) |
| `/machiot/tags` | GET | TAG 테이블 전용 고수준 데이터 조회 API |

## 빠른 시작 예제

다음은 REST API를 사용해 간단한 SQL을 실행하는 예제입니다.

```bash
curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -d '{"q": "SELECT 1 + 1"}'
```

응답 예시:

```json
{
  "data": {
    "columns": ["1 + 1"],
    "types": ["int32"],
    "rows": [[2]]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.234ms"
}
```

## 이 섹션의 구성

| 문서 | 내용 |
|------|------|
| [공통 인증과 타임존](common-authentication-timezone-rest-api/) | Bearer token 인증, X-Timezone 헤더, Content-Type 설정 |
| [SQL REST API](machbase-sql-rest-api/) | `/db/query` 엔드포인트 상세: SELECT, INSERT, DDL, format 옵션 |
| [Append REST API](machbase-append-rest-api/) | `/db/append` 엔드포인트 상세: 대용량 고속 삽입 |
| [TAG REST API](machiot-tags-tag-rest-api/) | `/machiot/tags` 엔드포인트 상세: TAG 전용 고수준 조회 |
| [오류 처리](error-handling-rest-api/) | HTTP 상태 코드, 오류 응답 형식, 재시도 전략 |

## REST API vs 드라이버 연결

REST API는 설치 없이 바로 사용할 수 있다는 장점이 있으나, 드라이버 연결 대비 다음과 같은 차이점이 있습니다.

| 항목 | REST API | 드라이버 (ODBC/JDBC 등) |
|------|----------|-------------------------|
| 설치 | 불필요 | 드라이버 설치 필요 |
| 언어 | 모든 언어 | 해당 언어/런타임 |
| 연결 방식 | HTTP (상태 없음) | TCP 영구 연결 |
| 대용량 삽입 | `/db/append` (chunked) | Append API (네이티브) |
| 트랜잭션 | SQL API로 제한적 지원 | 완전 지원 |
| 오버헤드 | HTTP 헤더 오버헤드 있음 | 낮음 |

일반적으로 **웹 프론트엔드, 마이크로서비스, 언어 독립 환경, 간단한 통합** 시나리오에서 REST API가 적합합니다. 초고성능 시계열 수집이 필요한 경우에는 네이티브 드라이버의 Append API 사용을 권장합니다.

## 레퍼런스

REST API의 전체 엔드포인트 목록과 파라미터 명세는 **14장 레퍼런스**를 참조하십시오.

- [REST API 레퍼런스](../../reference/rest-api/)
