---
type: docs
title: '/machbase SQL REST API'
weight: 20
---

`/machbase` SQL REST API는 HTTP GET 요청의 `q` 파라미터로 SQL 문을 전달하고 실행
결과를 JSON으로 반환합니다. `SELECT`, `INSERT`, `CREATE TABLE`, `DROP TABLE` 등
Machbase에서 지원하는 SQL을 요청 단위로 실행할 수 있습니다.

## 엔드포인트

```text
GET /machbase?q=<SQL>
```

SQL은 URL 인코딩해야 합니다. `curl`에서는 `-G`와 `--data-urlencode` 옵션을 사용하면
공백과 따옴표를 안전하게 전달할 수 있습니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT 1"
```

## 응답 형식

성공한 `SELECT` 응답은 다음 필드를 포함합니다.

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

| 필드 | 설명 |
|------|------|
| `error_code` | `0`이면 성공, `0`이 아니면 오류 |
| `error_message` | 오류 메시지. 성공 시 빈 문자열 |
| `columns` | 컬럼 이름, 내부 타입, 길이 정보 |
| `data` | 결과 행. 각 행은 컬럼명을 키로 갖는 JSON 객체 |
| `timezone` | 응답에 적용된 타임존 오프셋 |

DDL이나 DML처럼 결과 행이 없는 SQL도 `error_code`가 `0`이면 성공입니다. 이때
`effect_rows`가 함께 반환될 수 있습니다.

```json
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "effect_rows": "0",
  "data": []
}
```

## SELECT 예제

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT C1, C2 FROM curl_sample ORDER BY C1"
```

응답:

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

## DDL 예제

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=CREATE TABLE curl_sample (c1 INT, c2 VARCHAR(20))"
```

테이블을 삭제할 때도 같은 엔드포인트를 사용합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=DROP TABLE curl_sample"
```

## INSERT 예제

소량 데이터는 SQL `INSERT`로 입력할 수 있습니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=INSERT INTO curl_sample VALUES (3, 'ccc')"
```

다건 입력이나 수집성 데이터는 [Append REST API](../machbase-append-rest-api/)를
사용합니다.

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

query("DROP TABLE curl_sample")
query("CREATE TABLE curl_sample (c1 INT, c2 VARCHAR(20))")
query("INSERT INTO curl_sample VALUES (1, 'aaa')")

result = query("SELECT * FROM curl_sample ORDER BY c1")
for row in result["data"]:
    print(row)
```

`DROP TABLE`처럼 대상이 없으면 실패할 수 있는 SQL은 `error_code`를 확인하여 애플리케이션
로직에 맞게 처리합니다.

## 주의 사항

- 하나의 요청에는 하나의 SQL 문을 전달합니다.
- SQL 문은 URL 인코딩해서 전달합니다.
- HTTP 상태 코드가 `200`이어도 SQL 실행 오류는 `error_code`와 `error_message`로
  반환될 수 있습니다.
- 대량 삽입은 `/machbase` POST Append API를 사용합니다.
