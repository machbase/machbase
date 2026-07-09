---
type: docs
title: '17.6 REST API 레퍼런스'
weight: 60
---

Machbase REST API는 HTTP 요청으로 SQL 실행, 데이터 입력, TAG 데이터 조회를 수행합니다. 이 섹션은 각 엔드포인트의 URL, 메서드, 파라미터, 응답 형식을 빠르게 참조할 수 있도록 정리한 레퍼런스입니다.

## 기본 정보

| 항목 | 값 |
|------|-----|
| 기본 URL | `http://host:5657` |
| 포트 설정 | `machbase.conf`의 `HTTP_PORT_NO` |
| 서비스 활성화 | `machbase.conf`의 `HTTP_ENABLE = 1` |
| 응답 형식 | JSON (`Content-Type: text/json`) |

## 인증

`machbase.conf`의 `HTTP_AUTH` 설정에 따라 인증 방식이 결정됩니다.

| `HTTP_AUTH` 값 | 설명 |
|---------------|------|
| `0` (기본값) | 인증 없이 요청 가능 |
| `1` | Basic Authentication 필요 |

Basic Authentication 사용 시 요청 예시:

```bash
curl -u "SYS:MANAGER" \
  -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT 1"
```

## 공통 응답 필드

모든 REST API 응답은 다음 공통 필드를 포함합니다.

| 필드 | 타입 | 설명 |
|------|------|------|
| `error_code` | integer | `0`이면 성공, `0`이 아니면 오류 |
| `error_message` | string | 오류 메시지. 성공 시 빈 문자열 또는 `"No Error"` |
| `timezone` | string | 응답에 적용된 타임존 오프셋 (예: `"+0900"`) |

## 엔드포인트 목록

| 메서드 | URL | 설명 |
|--------|-----|------|
| `GET` | `/machbase?q=<SQL>` | SQL 실행 (SELECT, DDL, DML) |
| `POST` | `/machbase` | 다수 행 Append 삽입 |
| `GET` | `/machiot/tags/list[/<table>[/<tag_names>]]` | TAG 목록 조회 |
| `POST`/`PUT`/`PATCH`/`DELETE` | `/machiot/tags/list[/<table>[/<tag_names>]]` | TAG 메타데이터 삽입/갱신/삭제 |
| `GET` | `/machiot/tags/range[/<table>[/<tag_names>]]` | TAG 시간 범위 조회 |
| `GET` | `/machiot/tags/min|max|count[/<table>[/<tag_names>]]` | TAG 통계 조회 |
| `GET` | `/machiot/v1/datapoints/raw/...` | TAG raw datapoint 조회 |
| `POST` | `/machiot/v1/datapoints/raw/<table>` | TAG raw datapoint append |
| `GET` | `/machiot/v1/datapoints/calculated/...` | TAG calculated datapoint 조회 |
| `DELETE` | `/machiot/v1/datapoints/raw/...` | TAG raw datapoint 삭제 |

`/machiot-rest-api`는 `/machiot`의 호환 alias로 등록되어 있습니다.

## HTTP 상태 코드

| 상태 코드 | 의미 |
|-----------|------|
| `200 OK` | 요청 처리됨 (SQL 오류도 200으로 반환될 수 있음) |
| `401 Unauthorized` | 인증 실패 |
| `404 Not Found` | 유효하지 않은 엔드포인트 |
| `500 Internal Server Error` | 서버 내부 오류 |

## 하위 섹션

| 섹션 | 설명 |
|------|------|
| [/machbase SQL API](./machbase-sql-api/) | GET /machbase - SQL 실행 엔드포인트 상세 |
| [/machbase append API](./machbase-append-api/) | POST /machbase - 다수 행 삽입 엔드포인트 상세 |
| [TAG 데이터 조회](./machiot-tags-api/) | `/machiot` TAG/Datapoints 엔드포인트와 SQL 조회 패턴 |
