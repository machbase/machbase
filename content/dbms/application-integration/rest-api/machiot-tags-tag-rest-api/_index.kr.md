---
type: docs
title: '/machiot/tags TAG REST API'
weight: 40
---

`/machiot/tags` 엔드포인트는 TAG 테이블을 위한 고수준 REST API입니다. SQL을 직접 작성하지 않고도 TAG 메타데이터 조회, 시간 범위 기반 값 조회 등 일반적인 IoT/시계열 작업을 간단한 HTTP GET 요청으로 수행할 수 있습니다.

## 주요 엔드포인트 목록

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/machiot/tags` | GET | 등록된 TAG 목록 및 메타데이터 조회 |
| `/machiot/tags/{name}/values` | GET | 특정 TAG의 시계열 값 조회 |

## TAG 목록 조회

`GET /machiot/tags`는 TAG 테이블에 등록된 TAG 이름 목록과 메타데이터를 반환합니다.

### 요청

```bash
curl -X GET "http://127.0.0.1:5657/machiot/tags" \
  -H "Authorization: Bearer <token>"
```

### 응답

```json
{
  "success": true,
  "reason": "success",
  "elapse": "1.234ms",
  "data": {
    "columns": ["NAME"],
    "types": ["string"],
    "rows": [
      ["sensor-01"],
      ["sensor-02"],
      ["sensor-03"]
    ]
  }
}
```

### 쿼리 파라미터

| 파라미터 | 설명 | 예시 |
|----------|------|------|
| `name` | 특정 TAG 이름으로 필터링 | `?name=sensor-01` |
| `limit` | 반환할 최대 TAG 수 | `?limit=100` |
| `offset` | 페이징을 위한 시작 위치 | `?offset=50` |

```bash
# 이름이 "sensor"로 시작하는 TAG 조회
curl -X GET "http://127.0.0.1:5657/machiot/tags?name=sensor" \
  -H "Authorization: Bearer <token>"
```

## TAG 값 조회

`GET /machiot/tags/{name}/values`는 지정한 TAG의 시계열 데이터를 시간 범위와 함께 조회합니다.

### 요청

```bash
curl -X GET "http://127.0.0.1:5657/machiot/tags/sensor-01/values" \
  -H "Authorization: Bearer <token>"
```

### 쿼리 파라미터

| 파라미터 | 설명 | 예시 |
|----------|------|------|
| `from` | 조회 시작 시각 (RFC3339) | `?from=2024-01-15T00:00:00Z` |
| `to` | 조회 종료 시각 (RFC3339) | `?to=2024-01-15T23:59:59Z` |
| `limit` | 반환할 최대 행 수 | `?limit=1000` |
| `offset` | 페이징을 위한 시작 위치 | `?offset=0` |
| `format` | 응답 형식 (`json` 또는 `csv`) | `?format=csv` |

### 시간 범위 조회 예제

```bash
curl -X GET "http://127.0.0.1:5657/machiot/tags/sensor-01/values?from=2024-01-15T00:00:00Z&to=2024-01-15T23:59:59Z&limit=100" \
  -H "Authorization: Bearer <token>" \
  -H "X-Timezone: Asia/Seoul"
```

응답:

```json
{
  "success": true,
  "reason": "success",
  "elapse": "4.567ms",
  "data": {
    "columns": ["NAME", "TIME", "VALUE"],
    "types": ["string", "datetime", "double"],
    "rows": [
      ["sensor-01", "2024-01-15 09:00:00", 23.5],
      ["sensor-01", "2024-01-15 09:01:00", 23.7],
      ["sensor-01", "2024-01-15 09:02:00", 23.4]
    ]
  }
}
```

### 최신 값 조회

`limit=1`과 `offset=0`으로 가장 최근 값만 조회할 수 있습니다.

```bash
curl -X GET "http://127.0.0.1:5657/machiot/tags/sensor-01/values?limit=1" \
  -H "Authorization: Bearer <token>"
```

### CSV 형식 조회

```bash
curl -X GET "http://127.0.0.1:5657/machiot/tags/sensor-01/values?from=2024-01-15T00:00:00Z&to=2024-01-15T01:00:00Z&format=csv" \
  -H "Authorization: Bearer <token>"
```

CSV 응답:

```
NAME,TIME,VALUE
sensor-01,2024-01-15 00:00:00,23.5
sensor-01,2024-01-15 00:01:00,23.7
```

## Python 예제

```python
import requests
from datetime import datetime, timezone, timedelta

BASE_URL = "http://127.0.0.1:5657"

def get_token():
    resp = requests.post(f"{BASE_URL}/db/login",
                         json={"loginName": "SYS", "password": "MANAGER"})
    return resp.json()["token"]

def list_tags(token, limit=100):
    """등록된 TAG 목록 조회"""
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/machiot/tags",
                        headers=headers,
                        params={"limit": limit})
    resp.raise_for_status()
    result = resp.json()
    return [row[0] for row in result["data"]["rows"]]

def get_tag_values(tag_name, token, from_dt=None, to_dt=None, limit=1000):
    """TAG 시계열 값 조회"""
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Timezone": "Asia/Seoul",
    }
    params = {"limit": limit}
    if from_dt:
        params["from"] = from_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    if to_dt:
        params["to"] = to_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    resp = requests.get(f"{BASE_URL}/machiot/tags/{tag_name}/values",
                        headers=headers,
                        params=params)
    resp.raise_for_status()
    return resp.json()["data"]

# 사용 예
token = get_token()

# TAG 목록 조회
tags = list_tags(token)
print(f"등록된 TAG: {tags}")

# 최근 1시간 데이터 조회
now = datetime.now(timezone.utc)
one_hour_ago = now - timedelta(hours=1)

data = get_tag_values("sensor-01", token, from_dt=one_hour_ago, to_dt=now)
columns = data["columns"]
for row in data["rows"]:
    print(dict(zip(columns, row)))
```

## SQL API와의 비교

| 항목 | TAG REST API (`/machiot/tags`) | SQL REST API (`/db/query`) |
|------|-------------------------------|---------------------------|
| SQL 지식 | 불필요 | 필요 |
| 유연성 | TAG 테이블 전용, 정해진 파라미터 | 임의의 SQL 실행 가능 |
| 용도 | 단순 TAG 조회, IoT 대시보드 | 복잡한 집계, 조인, DDL |

단순한 TAG 값 조회에는 `/machiot/tags` API가 편리하며, 복잡한 집계나 JOIN이 필요한 경우 `/db/query`를 사용하십시오.

## 레퍼런스

전체 엔드포인트 목록과 고급 옵션은 14장 레퍼런스를 참조하십시오.

- [/machiot/tags API 레퍼런스](../../../reference/rest-api/machiot-tags-api/)
