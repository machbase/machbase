---
type: docs
title: '/machiot/tags API'
weight: 30
---

TAG 테이블 데이터는 `/machbase` SQL REST API로 조회합니다. 현재 빌드에서 고수준 `/machiot/tags` 엔드포인트는 유효한 REST API로 동작하지 않습니다. TAG 이름 목록, 시간 범위 조회, 최신값 조회는 SQL을 작성해 `GET /machbase?q=<SQL>`로 실행합니다.

## TAG 테이블 준비

```bash
# TAG 테이블 생성
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=CREATE TAG TABLE sensor_tag (name VARCHAR(64) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)"

# 데이터 입력 (Append API 사용)
curl -X POST "http://127.0.0.1:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"sensor_tag","values":[["sensor-01","2024-01-01 10:00:00",23.5],["sensor-01","2024-01-01 10:01:00",23.7]]}'

# 메모리 데이터 반영
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=EXEC TABLE_FLUSH(sensor_tag)"
```

## TAG 이름 목록 조회

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT DISTINCT name FROM sensor_tag ORDER BY name"
```

응답:

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [{"name": "name", "type": 5, "length": 64}],
  "data": [{"name": "sensor-01"}],
  "timezone": "+0900"
}
```

## 특정 TAG 값 조회

```bash
# 최근 10개 값
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_tag WHERE name = 'sensor-01' ORDER BY time DESC LIMIT 10"
```

## 최신 값 조회

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_tag WHERE name = 'sensor-01' ORDER BY time DESC LIMIT 1"
```

## 시간 범위 조회

Machbase 시간 연산은 나노초 단위를 사용합니다.

```bash
# 최근 1시간 데이터 (나노초 단위: 3600 * 10^9)
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_tag WHERE name = 'sensor-01' AND time >= SYSDATE - 3600000000000 ORDER BY time DESC LIMIT 100"

# 고정 시간 범위
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_tag WHERE time >= TO_DATE('2024-01-01 10:00:00') AND time < TO_DATE('2024-01-01 11:00:00') ORDER BY time"
```

## 집계 조회

`DATE_TRUNC`로 시간 버킷을 만들고 집계합니다. 단위는 `sec`, `min`, `hour`, `day` 등을 사용합니다.

```bash
# 1분 단위 평균값
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT DATE_TRUNC('min', time, 1) AS time, AVG(value) AS avg_value FROM sensor_tag WHERE name = 'sensor-01' GROUP BY time ORDER BY time"

# 1시간 단위 최대/최소/평균
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT DATE_TRUNC('hour', time, 1) AS time, MIN(value), MAX(value), AVG(value) FROM sensor_tag WHERE name = 'sensor-01' GROUP BY time ORDER BY time"
```

## Python 예제

```python
import requests

BASE_URL = "http://127.0.0.1:5657"

def query(sql):
    resp = requests.get(f"{BASE_URL}/machbase", params={"q": sql}, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    if result.get("error_code") != 0:
        raise RuntimeError(result.get("error_message"))
    return result.get("data", [])

# TAG 이름 목록
tags = query("SELECT DISTINCT name FROM sensor_tag ORDER BY name")
print(tags)

# 최신 10개 값
rows = query(
    "SELECT name, time, value "
    "FROM sensor_tag "
    "WHERE name = 'sensor-01' "
    "ORDER BY time DESC LIMIT 10"
)
for row in rows:
    print(row)
```

## /machiot/tags 요청이 실패하는 경우

현재 빌드에서 `/machiot/tags`를 호출하면 다음과 같은 오류가 반환됩니다.

```json
{
  "error_code": 3126,
  "error_message": "The requested URL for the REST API is not valid"
}
```

이 경우 `/machbase` SQL REST API로 동일한 조회를 수행합니다.
