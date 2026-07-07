---
type: docs
title: '/machbase SQL REST API'
weight: 20
---

`/db/query` 엔드포인트는 SQL 문을 HTTP로 전송하고 결과를 JSON 또는 CSV 형식으로 반환받는 범용 SQL API입니다. SELECT, INSERT, CREATE TABLE 등 모든 SQL 구문을 실행할 수 있습니다.

## 엔드포인트

```
POST /db/query
```

## 요청 형식

요청 본문은 JSON 형식이며 다음 필드를 포함합니다.

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `q` | string | 필수 | 실행할 SQL 문 |
| `format` | string | 선택 | 결과 형식: `json` (기본값) 또는 `csv` |
| `timeformat` | string | 선택 | 시간 표시 형식 (예: `2006-01-02 15:04:05`, `ns`) |
| `tz` | string | 선택 | 타임존 (예: `Asia/Seoul`). `X-Timezone` 헤더로도 지정 가능 |
| `limit` | int | 선택 | 반환할 최대 행 수 |

## 응답 형식 (JSON)

```json
{
  "data": {
    "columns": ["컬럼명1", "컬럼명2"],
    "types": ["데이터타입1", "데이터타입2"],
    "rows": [
      ["값1", "값2"],
      ["값3", "값4"]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "2.345ms"
}
```

| 필드 | 설명 |
|------|------|
| `data.columns` | 컬럼명 목록 |
| `data.types` | 각 컬럼의 데이터 타입 |
| `data.rows` | 결과 행 배열 |
| `success` | 실행 성공 여부 |
| `reason` | 성공 또는 오류 메시지 |
| `elapse` | 서버 측 실행 소요 시간 |

## SELECT 예제

### 기본 SELECT

```bash
curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"q": "SELECT name, time, value FROM example ORDER BY time DESC LIMIT 5"}'
```

응답:

```json
{
  "data": {
    "columns": ["NAME", "TIME", "VALUE"],
    "types": ["string", "datetime", "double"],
    "rows": [
      ["sensor-01", "2024-01-15 10:00:00", 23.5],
      ["sensor-01", "2024-01-15 09:59:00", 23.2]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "3.210ms"
}
```

### 타임존 지정 SELECT

```bash
curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "X-Timezone: Asia/Seoul" \
  -d '{"q": "SELECT name, time, value FROM example LIMIT 3"}'
```

### CSV 형식으로 반환

```bash
curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"q": "SELECT name, time, value FROM example LIMIT 10", "format": "csv"}'
```

CSV 응답 예시:

```
NAME,TIME,VALUE
sensor-01,2024-01-15 10:00:00,23.5
sensor-01,2024-01-15 09:59:00,23.2
```

## INSERT 예제

INSERT 문도 `/db/query`로 실행합니다. 성공 시 `rows`는 빈 배열로 반환됩니다.

```bash
curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"q": "INSERT INTO example (name, time, value) VALUES ('"'"'sensor-01'"'"', TO_DATE('"'"'2024-01-15 10:00:00'"'"'), 23.5)"}'
```

또는 JSON 파일을 사용하면 따옴표 이스케이프를 피할 수 있습니다.

```bash
# query.json 파일 내용:
# {"q": "INSERT INTO example (name, time, value) VALUES ('sensor-01', TO_DATE('2024-01-15 10:00:00'), 23.5)"}

curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d @query.json
```

INSERT 성공 응답:

```json
{
  "data": {
    "columns": [],
    "types": [],
    "rows": []
  },
  "success": true,
  "reason": "success",
  "elapse": "1.102ms"
}
```

## DDL 예제

CREATE TABLE, DROP TABLE 등 DDL 문도 동일하게 실행합니다.

```bash
curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"q": "CREATE TAG TABLE IF NOT EXISTS sensor_data (name VARCHAR(64) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE)"}'
```

## Python 예제

```python
import requests

BASE_URL = "http://127.0.0.1:5657"

def get_token():
    resp = requests.post(f"{BASE_URL}/db/login",
                         json={"loginName": "SYS", "password": "MANAGER"})
    return resp.json()["token"]

def query(sql, token, tz="UTC"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "X-Timezone": tz,
    }
    resp = requests.post(f"{BASE_URL}/db/query",
                         headers=headers,
                         json={"q": sql})
    resp.raise_for_status()
    return resp.json()

# 사용 예
token = get_token()

# 테이블 생성
query("CREATE TAG TABLE IF NOT EXISTS sensor_data "
      "(name VARCHAR(64) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE)",
      token)

# 데이터 조회
result = query("SELECT * FROM sensor_data ORDER BY time DESC LIMIT 10",
               token, tz="Asia/Seoul")

columns = result["data"]["columns"]
rows = result["data"]["rows"]
for row in rows:
    print(dict(zip(columns, row)))
```

## 주의 사항

- 하나의 요청에 하나의 SQL 문만 실행할 수 있습니다. 여러 SQL을 실행하려면 요청을 분리하십시오.
- TAG 테이블에 대량 데이터를 삽입할 때는 INSERT보다 [Append REST API](../machbase-append-rest-api/)를 사용하면 성능이 크게 향상됩니다.
- SELECT 결과가 매우 많을 경우 `limit` 파라미터로 반환 행 수를 제한하거나, 애플리케이션에서 페이징을 구현하십시오.

## 레퍼런스

전체 파라미터 목록과 고급 옵션은 14장 레퍼런스를 참조하십시오.

- [/machbase SQL API 레퍼런스](../../../reference/rest-api/machbase-sql-api/)
