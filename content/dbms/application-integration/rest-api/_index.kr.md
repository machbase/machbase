---
type: docs
title: 'REST API 연동'
weight: 40
---

Machbase는 HTTP 기반 REST API를 제공합니다. 별도 드라이버를 설치하지 않고 `curl`,
Python `requests`, JavaScript `fetch` 등 HTTP 클라이언트에서 SQL 실행과 Append 삽입을
수행할 수 있습니다.

## REST API 포트

REST API는 DB 연결 포트와 별도의 HTTP 포트를 사용합니다.

| 포트 | 용도 |
|------|------|
| 5656 | ODBC/JDBC/네이티브 드라이버 연결 |
| 5657 | REST API (HTTP) |

기본 URL은 다음과 같습니다.

```text
http://<host>:5657
```

로컬 서버에 접속하는 경우 기본 URL은 `http://127.0.0.1:5657`입니다.

## 주요 API 엔드포인트

현재 Machbase REST 샘플과 서버에서 확인되는 기본 엔드포인트는 다음과 같습니다.

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/machbase?q=<SQL>` | GET | SQL 실행 및 결과 반환 |
| `/machbase` | POST | JSON 본문으로 여러 행 Append 삽입 |
| `/machbase/tables` | GET | 테이블 목록 조회 |
| `/machbase/columns/<table>` | GET | 지정한 테이블의 컬럼 정보 조회 |

## 빠른 시작 예제

다음은 REST API를 사용해 SQL을 실행하는 예제입니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT 1"
```

응답 예시:

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {"name": "1", "type": 8, "length": 11}
  ],
  "data": [
    {"1": 1}
  ],
  "timezone": "+0900"
}
```

## 이 섹션의 구성

| 문서 | 내용 |
|------|------|
| [공통 설정](common-authentication-timezone-rest-api/) | HTTP 포트, 인증 설정, 요청 헤더 |
| [SQL REST API](machbase-sql-rest-api/) | `/machbase` GET SQL 실행 |
| [Append REST API](machbase-append-rest-api/) | `/machbase` POST Append 삽입 |
| [TAG 조회](machiot-tags-tag-rest-api/) | TAG 테이블을 SQL REST API로 조회하는 방법 |
| [오류 처리](error-handling-rest-api/) | `error_code`, HTTP 상태 코드, 재시도 전략 |

## REST API vs 드라이버 연결

| 항목 | REST API | 드라이버 (ODBC/JDBC 등) |
|------|----------|-------------------------|
| 설치 | 불필요 | 드라이버 설치 필요 |
| 언어 | 모든 언어 | 해당 언어/런타임 |
| 연결 방식 | HTTP 요청 | TCP 연결 |
| SQL 실행 | `/machbase?q=<SQL>` | 드라이버 API |
| 대량 삽입 | `/machbase` POST Append | 네이티브 Append API |
| 트랜잭션 | HTTP 요청 단위 실행 | RDB 테이블에서 트랜잭션 사용 가능 |

REST API는 간단한 통합, 웹 서비스, 언어 독립 환경에 적합합니다. 초고성능 수집이나
세밀한 연결 제어가 필요한 경우에는 네이티브 드라이버의 Append API를 사용합니다.
