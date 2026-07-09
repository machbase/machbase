---
type: docs
title: '11.4.3 /machbase append REST API'
weight: 30
---

`/machbase` Append REST API는 HTTP POST 요청으로 여러 행을 한 번에 삽입합니다. 요청
본문에는 대상 테이블 이름과 행 배열을 JSON으로 전달합니다.

## 엔드포인트

```text
POST /machbase
```

## 요청 형식

요청 본문은 `application/json` 형식입니다.

```json
{
  "name": "curl_sample",
  "values": [
    [1, "aaa"],
    [2, "bbb"]
  ]
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `name` | string | 데이터를 삽입할 테이블 이름 |
| `values` | array | 삽입할 행 배열. 각 행은 테이블 컬럼 순서와 같은 배열 |

컬럼 이름은 요청에 포함하지 않습니다. `values`의 각 행은 테이블 정의의 컬럼 순서와
일치해야 합니다.

## 응답 형식

삽입 성공 시 다음과 같이 Append 성공/실패 건수를 반환합니다.

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

| 필드 | 설명 |
|------|------|
| `error_code` | `0`이면 요청 처리 성공 |
| `error_message` | 오류 메시지. 성공 시 빈 문자열 |
| `append_success` | 성공적으로 삽입된 행 수 |
| `append_failure` | 삽입에 실패한 행 수 |

## curl 예제

먼저 SQL REST API로 예제 테이블을 생성합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=CREATE TABLE curl_sample (c1 INT, c2 VARCHAR(20))"
```

다음 요청은 두 행을 Append로 삽입합니다.

```bash
curl -X POST "http://127.0.0.1:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"curl_sample","values":[[1,"aaa"],[2,"bbb"]]}'
```

삽입 결과를 확인합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT * FROM curl_sample ORDER BY c1"
```

## JavaScript 예제

```javascript
async function appendRows(rows) {
  const resp = await fetch("http://127.0.0.1:5657/machbase", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      name: "curl_sample",
      values: rows,
    }),
  });

  const result = await resp.json();
  if (result.error_code !== 0 || result.append_failure > 0) {
    throw new Error(result.error_message || "append failed");
  }
  return result.append_success;
}

appendRows([[1, "aaa"], [2, "bbb"]]).then(console.log);
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

count = append_rows("curl_sample", [[1, "aaa"], [2, "bbb"]])
print(f"inserted rows: {count}")
```

## INSERT와의 비교

| 방법 | 특징 |
|------|------|
| SQL `INSERT` (`GET /machbase?q=...`) | 소량 데이터, SQL 문 단위 실행 |
| Append (`POST /machbase`) | 여러 행을 한 요청으로 삽입, 수집성 데이터에 적합 |

초당 많은 행을 수집하는 애플리케이션에서는 SQL `INSERT`를 반복 실행하기보다 Append API나
네이티브 드라이버의 Append API를 사용합니다.

## 주의 사항

- 요청 본문은 JSON이어야 하며 `Content-Type: application/json`을 지정합니다.
- `values`의 컬럼 순서와 타입은 테이블 정의와 일치해야 합니다.
- SQL 실행 오류와 마찬가지로 HTTP 상태 코드와 함께 `error_code`, `append_failure`를
  확인합니다.
