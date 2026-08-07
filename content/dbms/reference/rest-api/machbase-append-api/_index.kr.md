---
type: docs
title: '18.6.2 /machbase append API'
weight: 20
toc: true
---

`POST /machbase` 엔드포인트는 여러 행을 한 번에 삽입합니다. 요청 본문에 테이블 이름과 행 배열을 JSON으로 전달하며, 수집성 고빈도 데이터 입력에 적합합니다.

## 엔드포인트

```text
POST /machbase
Content-Type: application/json
```

## 요청 형식

```json
{
  "name": "<테이블 이름>",
  "values": [
    [<컬럼1 값>, <컬럼2 값>, ...],
    [<컬럼1 값>, <컬럼2 값>, ...]
  ]
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `name` | string | 필수 | 데이터를 삽입할 테이블 이름 |
| `values` | array | 필수 | 삽입할 행 배열. 각 행은 테이블 컬럼 순서와 일치하는 배열 |

`values`의 각 행은 테이블 정의의 컬럼 순서와 일치해야 합니다. 컬럼 이름은 요청에 포함하지 않습니다.

## 응답 형식

```json
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "data": [],
  "append_success": 2,
  "append_failure": 0
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `error_code` | integer | `0`이면 요청 처리 성공 |
| `error_message` | string | 오류 메시지 |
| `append_success` | integer | 성공적으로 삽입된 행 수 |
| `append_failure` | integer | 삽입에 실패한 행 수 |

> `error_code`가 `0`이어도 `append_failure`가 `0`보다 크면 일부 행이 삽입되지 않은 상태입니다. 두 값을 모두 확인합니다.

## 요청 헤더

| 헤더 | 필수 | 값 |
|------|------|-----|
| `Content-Type` | 필수 | `application/json` |
| `Authorization` | HTTP_AUTH 활성화 시 | `Basic <base64(user:password)>` |

## curl 예제

```bash
# 테이블 생성 (SQL API 사용)
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=CREATE LOG TABLE sensor_log (c1 INT, c2 VARCHAR(20))"

# 다수 행 Append 삽입
curl -X POST "http://127.0.0.1:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"sensor_log","values":[[1,"aaa"],[2,"bbb"],[3,"ccc"]]}'

# 삽입 결과 확인
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT * FROM sensor_log ORDER BY c1"
```

## TAG 테이블 Append 예제

```bash
curl -X POST "http://127.0.0.1:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "sensor_tag",
    "values": [
      ["sensor-01", "2024-01-01 10:00:00", 23.5],
      ["sensor-01", "2024-01-01 10:01:00", 23.7],
      ["sensor-02", "2024-01-01 10:00:00", 45.1]
    ]
  }'
```

## Python 예제

```python
import requests

BASE_URL = "http://127.0.0.1:5657"

def append_rows(table, rows):
    resp = requests.post(
        f"{BASE_URL}/machbase",
        json={"name": table, "values": rows},
        timeout=10,
    )
    resp.raise_for_status()
    result = resp.json()
    if result.get("error_code") != 0:
        raise RuntimeError(result.get("error_message"))
    if result.get("append_failure", 0) != 0:
        raise RuntimeError(f"append failure: {result['append_failure']}")
    return result["append_success"]

count = append_rows("sensor_tag", [
    ["sensor-01", "2024-01-01 10:00:00", 23.5],
    ["sensor-01", "2024-01-01 10:01:00", 23.7],
])
print(f"삽입된 행 수: {count}")
```

## JavaScript 예제

```javascript
async function appendRows(table, rows) {
  const resp = await fetch("http://127.0.0.1:5657/machbase", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: table, values: rows }),
  });

  const result = await resp.json();
  if (result.error_code !== 0 || result.append_failure > 0) {
    throw new Error(result.error_message || "append failed");
  }
  return result.append_success;
}

appendRows("sensor_tag", [
  ["sensor-01", "2024-01-01 10:00:00", 23.5],
  ["sensor-02", "2024-01-01 10:00:00", 45.1],
]).then(count => console.log(`삽입된 행 수: ${count}`));
```

## INSERT와의 비교

| 방법 | 특징 |
|------|------|
| `GET /machbase?q=INSERT ...` | 소량 데이터, 단일 행, SQL 단위 실행 |
| `POST /machbase` | 여러 행을 한 요청으로 삽입, 수집성 고빈도 데이터에 적합 |

초당 많은 행을 수집하는 애플리케이션에서는 SQL `INSERT`를 반복 실행하기보다 Append API나 네이티브 드라이버의 Append API를 사용합니다.
