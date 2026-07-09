---
type: docs
title: '17.8.9 REST API 지원표'
weight: 90
---

Machbase REST API는 HTTP를 통해 SQL 실행, Append 쓰기, 태그 데이터 조회 등을 제공합니다. 별도 드라이버 설치 없이 웹 서비스, 마이크로서비스, 스크립트 환경에서 사용할 수 있습니다.

기본 포트는 **5657**입니다 (DB 포트 5656과 별도).

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 기능 |
|-----------|--------|------|
| `/machbase` | GET | `q` 파라미터로 SQL 실행 (SELECT, DDL, DML) |
| `/machbase` | POST | JSON body 기반 Append 쓰기 |
| `/machiot/tags/list` | GET | 태그 목록 조회 |
| `/machiot/tags/range` | GET | 태그 시간 범위 조회 |
| `/machiot/tags/min`, `/max`, `/count` | GET | 태그 통계 조회 |
| `/machiot/v1/datapoints/raw` | GET / DELETE | raw datapoint 조회/삭제 |
| `/machiot/v1/datapoints/calculated` | GET | calculated datapoint 조회 |

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
| AUTH KEY challenge 인증 | X | HTTP Basic Auth는 `HTTP_AUTH=1`일 때 사용 |

## 인증 방식

REST API 인증은 `machbase.conf`의 `HTTP_AUTH` 값으로 제어합니다.

| 방식 | 설정 | 비고 |
|------|------|------|
| 인증 없음 | `HTTP_AUTH=0` | 기본 설정 |
| Basic Authentication | `HTTP_AUTH=1` | `Authorization: Basic ...` |

Bearer Token 로그인 엔드포인트는 현재 소스 기준으로 확인되지 않습니다.

## 사용 예시

### SQL 실행

```bash
# GET 방식
curl -u SYS:MANAGER \
  -G "http://localhost:5657/machbase" \
  --data-urlencode "q=SELECT * FROM TAG TABLE sensor_data RECENT 5"
```

### Append 쓰기

```bash
curl -u SYS:MANAGER \
  -X POST "http://localhost:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"sensor_data","values":[["sensor01",1720000000000000000,25.3]]}'
```

### 태그 값 조회 (IoT API)

```bash
curl -u SYS:MANAGER \
  "http://localhost:5657/machiot/v1/datapoints/raw?Table=sensor_data&TagNames=sensor01&Start=2024-01-01T00:00:00,000&End=2024-01-02T00:00:00,000"
```

## 상세 레퍼런스

REST API 전체 엔드포인트 목록, 요청/응답 형식, 에러 코드는 [REST API 레퍼런스](/dbms/reference/rest-api/)를 참고하세요.
