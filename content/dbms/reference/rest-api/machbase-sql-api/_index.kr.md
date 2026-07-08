---
type: docs
title: '/machbase SQL API'
weight: 10
---

`GET /machbase` 엔드포인트는 `q` 파라미터로 SQL 문을 전달하고 실행 결과를 JSON으로 반환합니다. `SELECT`, `INSERT`, `CREATE TABLE`, `DROP TABLE` 등 Machbase에서 지원하는 모든 SQL을 실행할 수 있습니다.

## 엔드포인트

```text
GET /machbase?q=<URL-encoded SQL>
```

## 요청 파라미터

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `q` | 필수 | 실행할 SQL 문 (URL 인코딩 필요) |

SQL은 URL 인코딩이 필요합니다. `curl`에서는 `-G`와 `--data-urlencode` 옵션을 사용합니다.

## 응답 형식

### SELECT 성공 응답

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {"name": "C1", "type": 8, "length": 11},
    {"name": "C2", "type": 5, "length": 20}
  ],
  "data": [
    {"C1": 1, "C2": "aaa"},
    {"C1": 2, "C2": "bbb"}
  ],
  "timezone": "+0900"
}
```

### DDL/DML 성공 응답

```json
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "effect_rows": "0",
  "data": []
}
```

### 오류 응답

```json
{
  "error_code": 2001,
  "error_message": "Syntax error: near token (SELCT * FROM example).",
  "timezone": "+0900",
  "data": []
}
```

## 응답 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `error_code` | integer | `0`이면 성공, `0`이 아니면 오류 |
| `error_message` | string | 오류 메시지 |
| `columns` | array | 컬럼 이름(`name`), 내부 타입(`type`), 길이(`length`) |
| `data` | array | 결과 행. 각 행은 컬럼명을 키로 갖는 JSON 객체 |
| `timezone` | string | 응답에 적용된 타임존 오프셋 |
| `effect_rows` | string | DDL/DML에서 영향받은 행 수 |

## 예제

### SELECT

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_tag ORDER BY time DESC LIMIT 10"
```

### CREATE TABLE

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=CREATE TAG TABLE sensor_tag (name VARCHAR(64) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)"
```

### DROP TABLE

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=DROP TABLE sensor_tag"
```

### INSERT (소량 데이터)

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=INSERT INTO sensor_tag VALUES ('sensor-01', NOW, 23.5)"
```

### 인증 사용

```bash
curl -u "SYS:MANAGER" \
  -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT COUNT(*) FROM sensor_tag"
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
    return result

result = query("SELECT name, time, value FROM sensor_tag ORDER BY time DESC LIMIT 10")
for row in result["data"]:
    print(row)
```

## 주의 사항

- 하나의 요청에는 하나의 SQL 문만 전달합니다.
- HTTP 상태 코드가 `200`이어도 SQL 실행 오류는 `error_code`로 반환됩니다. 반드시 `error_code`를 확인합니다.
- 대량 삽입은 `POST /machbase` [Append API](../machbase-append-api/)를 사용합니다.
- TAG 테이블 데이터 조회 패턴은 [TAG 데이터 조회](../machiot-tags-api/)를 참고하십시오.
