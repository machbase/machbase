---
type: docs
title: '/machbase append REST API'
weight: 30
---

`/db/append/{table_name}` 엔드포인트는 대용량 시계열 데이터를 HTTP로 고속 삽입하기 위한 API입니다. 일반 INSERT SQL 대비 훨씬 높은 처리량을 제공하며, TAG 테이블과 LOG 테이블 모두에 사용할 수 있습니다.

## 엔드포인트

```
POST /db/append/{table_name}
```

`{table_name}` 자리에 데이터를 삽입할 테이블 이름을 입력합니다.

## 요청 형식

Append API는 요청 본문에 CSV 또는 JSON 배열 형식으로 여러 행을 한 번에 전송합니다.

### CSV 형식

```
Content-Type: text/csv
```

각 행을 쉼표로 구분하여 전송합니다. 첫 번째 줄에 헤더를 포함하거나 생략할 수 있습니다.

```
NAME,TIME,VALUE
sensor-01,2024-01-15T10:00:00Z,23.5
sensor-01,2024-01-15T10:01:00Z,23.7
sensor-02,2024-01-15T10:00:00Z,18.3
```

### JSON 형식

```
Content-Type: application/json
```

컬럼 이름 목록(`columns`)과 데이터 행 배열(`rows`)로 구성합니다.

```json
{
  "columns": ["NAME", "TIME", "VALUE"],
  "rows": [
    ["sensor-01", "2024-01-15T10:00:00Z", 23.5],
    ["sensor-01", "2024-01-15T10:01:00Z", 23.7],
    ["sensor-02", "2024-01-15T10:00:00Z", 18.3]
  ]
}
```

## 응답 형식

성공 시 삽입된 행 수를 반환합니다.

```json
{
  "success": true,
  "reason": "success",
  "elapse": "5.432ms",
  "data": {
    "affectedRows": 3
  }
}
```

## curl 예제

### CSV 데이터 삽입

```bash
curl -X POST http://127.0.0.1:5657/db/append/sensor_data \
  -H "Content-Type: text/csv" \
  -H "Authorization: Bearer <token>" \
  --data-binary $'NAME,TIME,VALUE\nsensor-01,2024-01-15T10:00:00Z,23.5\nsensor-01,2024-01-15T10:01:00Z,23.7\nsensor-02,2024-01-15T10:00:00Z,18.3'
```

### CSV 파일 전송

데이터가 파일로 준비되어 있는 경우 파일을 직접 전송합니다.

```bash
curl -X POST http://127.0.0.1:5657/db/append/sensor_data \
  -H "Content-Type: text/csv" \
  -H "Authorization: Bearer <token>" \
  --data-binary @sensor_data.csv
```

### JSON 데이터 삽입

```bash
curl -X POST http://127.0.0.1:5657/db/append/sensor_data \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "columns": ["NAME", "TIME", "VALUE"],
    "rows": [
      ["sensor-01", "2024-01-15T10:00:00Z", 23.5],
      ["sensor-01", "2024-01-15T10:01:00Z", 23.7]
    ]
  }'
```

### Chunked Transfer (대용량 스트리밍)

데이터가 매우 클 경우 HTTP chunked transfer encoding을 사용하여 스트리밍 방식으로 전송할 수 있습니다. 이 방식은 데이터를 메모리에 모두 올리지 않고 실시간으로 생성하면서 전송할 때 유용합니다.

```bash
# 스크립트로 데이터를 생성하면서 chunked 전송
generate_csv() {
  echo "NAME,TIME,VALUE"
  for i in $(seq 1 10000); do
    echo "sensor-01,2024-01-15T10:00:${i}Z,$(echo "scale=1; $RANDOM / 1000" | bc)"
  done
}

generate_csv | curl -X POST http://127.0.0.1:5657/db/append/sensor_data \
  -H "Content-Type: text/csv" \
  -H "Authorization: Bearer <token>" \
  -H "Transfer-Encoding: chunked" \
  --data-binary @-
```

## Python 예제

```python
import requests
import csv
import io

BASE_URL = "http://127.0.0.1:5657"

def get_token():
    resp = requests.post(f"{BASE_URL}/db/login",
                         json={"loginName": "SYS", "password": "MANAGER"})
    return resp.json()["token"]

def append_csv(table, rows, token):
    """CSV 형식으로 Append API 호출"""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerows(rows)
    csv_data = buf.getvalue()

    headers = {
        "Content-Type": "text/csv",
        "Authorization": f"Bearer {token}",
    }
    resp = requests.post(
        f"{BASE_URL}/db/append/{table}",
        headers=headers,
        data=csv_data.encode("utf-8")
    )
    resp.raise_for_status()
    return resp.json()

# 사용 예
token = get_token()

data = [
    ["NAME", "TIME", "VALUE"],  # 헤더 행
    ["sensor-01", "2024-01-15T10:00:00Z", 23.5],
    ["sensor-01", "2024-01-15T10:01:00Z", 23.7],
    ["sensor-02", "2024-01-15T10:00:00Z", 18.3],
]

result = append_csv("sensor_data", data, token)
print(f"삽입된 행 수: {result['data']['affectedRows']}")
```

## INSERT와의 성능 비교

Append API는 내부적으로 네이티브 Append 프로토콜을 사용하기 때문에 SQL INSERT보다 훨씬 높은 처리량을 제공합니다.

| 방법 | 특징 |
|------|------|
| SQL INSERT (`/db/query`) | 건당 실행, 트랜잭션 지원, 소량 삽입에 적합 |
| Append API (`/db/append`) | 다건 배치 처리, 비트랜잭션, 대용량 수집에 최적 |

일반적으로 초당 수천 건 이상의 데이터를 삽입해야 하는 경우 Append API를 사용하십시오.

## 시간 형식

`TIME` 컬럼(DATETIME BASETIME)에 입력할 시각은 다음 형식을 지원합니다.

| 형식 | 예시 |
|------|------|
| RFC3339 (권장) | `2024-01-15T10:00:00Z` |
| RFC3339 with timezone | `2024-01-15T19:00:00+09:00` |
| Unix 나노초 (정수) | `1705312800000000000` |

## 레퍼런스

전체 파라미터와 고급 옵션은 14장 레퍼런스를 참조하십시오.

- [/machbase append API 레퍼런스](../../../reference/rest-api/machbase-append-api/)
