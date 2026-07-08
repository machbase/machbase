---
type: docs
title: 'REST API 지원표'
weight: 90
---

Machbase REST API는 HTTP를 통해 SQL 실행, Append 쓰기, 태그 데이터 조회 등을 제공합니다. 별도 드라이버 설치 없이 웹 서비스, 마이크로서비스, 스크립트 환경에서 사용할 수 있습니다.

기본 포트는 **5657**입니다 (DB 포트 5656과 별도).

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 기능 |
|-----------|--------|------|
| `/db/query` | GET / POST | SQL 실행 (SELECT, DDL, DML) |
| `/db/append/{table}` | POST | Append 고속 쓰기 |
| `/machbase` | POST | SQL 실행 및 Append (레거시 경로) |
| `/machiot/tags` | GET | 태그 목록 조회 |
| `/machiot/tags/{name}/values` | GET | 특정 태그 값 조회 |
| `/machiot/tags/{name}/values` | POST | 특정 태그 값 입력 |
| `/machiot/tags/{name}/stat` | GET | 특정 태그 통계 조회 |

## 기능별 지원 여부

| 기능 | 지원 여부 | 비고 |
|------|:---------:|------|
| SQL SELECT 실행 | O | |
| SQL DDL 실행 | O | CREATE TABLE 등 |
| SQL DML 실행 | O | INSERT/UPDATE/DELETE |
| Append 고속 쓰기 | O | JSON 배열 형태 |
| 트랜잭션 (COMMIT/ROLLBACK) | X | 단일 요청 단위 자동 커밋 |
| Prepared Statement | X | 서버 사이드 prepare 없음 |
| 파라미터 바인딩 | X | SQL 문자열에 값 직접 포함 |
| AUTH KEY challenge 인증 | X | Basic Auth / Bearer Token 사용 |

## 인증 방식

REST API는 두 가지 인증 방식을 지원합니다.

| 방식 | 설정 | 비고 |
|------|------|------|
| Basic Authentication | `Authorization: Basic base64(user:password)` | `machbase.conf`의 `HTTP_AUTH=basic` |
| Bearer Token | `Authorization: Bearer <token>` | 로그인 엔드포인트로 토큰 발급 후 사용 |

`machbase.conf`에서 `HTTP_AUTH` 설정으로 인증 방식을 제어합니다.

## 사용 예시

### SQL 실행

```bash
# GET 방식
curl -u SYS:MANAGER \
  "http://localhost:5657/db/query?q=SELECT+*+FROM+sensor_data+RECENT+5"

# POST 방식
curl -u SYS:MANAGER \
  -X POST "http://localhost:5657/db/query" \
  -H "Content-Type: application/json" \
  -d '{"q": "SELECT * FROM sensor_data RECENT 5"}'
```

### Append 쓰기

```bash
curl -u SYS:MANAGER \
  -X POST "http://localhost:5657/db/append/sensor_data" \
  -H "Content-Type: application/json" \
  -d '{"data": {"columns": ["name","time","value"], "rows": [["sensor01",1720000000000000000,25.3]]}}'
```

### 태그 값 조회 (IoT API)

```bash
curl -u SYS:MANAGER \
  "http://localhost:5657/machiot/tags/sensor01/values?start=2024-01-01&end=2024-01-02"
```

## 상세 레퍼런스

REST API 전체 엔드포인트 목록, 요청/응답 형식, 에러 코드는 [REST API 레퍼런스](/dbms/reference/rest-api/)를 참고하세요.
