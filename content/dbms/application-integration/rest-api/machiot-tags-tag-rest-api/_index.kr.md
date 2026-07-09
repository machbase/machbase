---
type: docs
title: '11.4.4 TAG 테이블 REST 조회'
weight: 40
---

TAG 테이블 데이터는 `/machbase` SQL REST API로 조회합니다. 현재 빌드에서 고수준
`/machiot/tags` 엔드포인트는 유효한 REST API로 동작하지 않습니다. TAG 이름 목록, 시간
범위 조회, 최신값 조회는 SQL을 작성해 `/machbase?q=<SQL>`로 실행합니다.

## TAG 테이블 준비

예제에서는 다음 TAG 테이블을 사용합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=CREATE TAG TABLE sensor_data (name VARCHAR(64) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)"
```

데이터는 Append REST API로 입력합니다.

```bash
curl -X POST "http://127.0.0.1:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"sensor_data","values":[["sensor-01","2026-07-07 10:00:00",23.5],["sensor-01","2026-07-07 10:01:00",23.7]]}'
```

필요하면 조회 전 `EXEC TABLE_FLUSH(sensor_data)`를 실행해 메모리의 Append 데이터를
조회 가능 상태로 반영합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=EXEC TABLE_FLUSH(sensor_data)"
```

## TAG 이름 목록 조회

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT DISTINCT name FROM sensor_data ORDER BY name"
```

응답 예시:

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {"name": "name", "type": 5, "length": 64}
  ],
  "data": [
    {"name": "sensor-01"}
  ],
  "timezone": "+0900"
}
```

## 특정 TAG 값 조회

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_data WHERE name = 'sensor-01' ORDER BY time DESC LIMIT 10"
```

## 시간 범위 조회

Machbase 시간 연산은 나노초 단위를 사용합니다. 다음 예제는 최근 1시간 데이터를
조회합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_data WHERE name = 'sensor-01' AND time >= SYSDATE - 3600000000000 ORDER BY time DESC LIMIT 100"
```

고정된 시간 범위를 사용할 때는 `TO_DATE`로 시각 문자열을 변환합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_data WHERE time >= TO_DATE('2026-07-07 10:00:00') AND time < TO_DATE('2026-07-07 11:00:00') ORDER BY time"
```

## 최신 값 조회

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_data WHERE name = 'sensor-01' ORDER BY time DESC LIMIT 1"
```

## 집계 조회

`DATE_TRUNC`로 시간 버킷을 만들고 집계할 수 있습니다. 단위는 `sec`, `min`, `hour`,
`day` 등을 사용합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT DATE_TRUNC('min', time, 1) AS time, AVG(value) AS avg_value FROM sensor_data WHERE name = 'sensor-01' GROUP BY time ORDER BY time"
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

tags = query("SELECT DISTINCT name FROM sensor_data ORDER BY name")
print(tags)

rows = query(
    "SELECT name, time, value "
    "FROM sensor_data "
    "WHERE name = 'sensor-01' "
    "ORDER BY time DESC LIMIT 10"
)
for row in rows:
    print(row)
```

## `/machiot/tags` 요청이 실패하는 경우

현재 빌드에서 `/machiot/tags`를 호출하면 다음과 같은 REST API URL 오류가 반환될 수
있습니다.

```json
{
  "error_code": 3126,
  "error_message": "The requested URL for the REST API is not valid"
}
```

이 경우 `/machbase` SQL REST API로 동일한 조회를 수행합니다.
