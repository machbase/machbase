---
type: docs
title: '11.4.5 REST API 오류 처리'
weight: 50
---

Machbase REST API 클라이언트는 HTTP 상태 코드와 응답 JSON의 `error_code`를 함께
확인해야 합니다. SQL 실행 오류는 HTTP `200 OK`와 함께 `error_code != 0`으로 반환될 수
있습니다.

## HTTP 상태 코드

| 상태 코드 | 의미 | 주요 원인 |
|-----------|------|-----------|
| `200 OK` | REST 요청 처리됨 | SQL 성공 또는 SQL 오류 응답 포함 |
| `401 Unauthorized` | 인증 실패 | `HTTP_AUTH` 활성화 상태에서 인증 정보 누락 또는 오류 |
| `404 Not Found` | 엔드포인트 없음 | 존재하지 않는 URL 요청 |
| `500 Internal Server Error` | 서버 오류 | 서버 내부 처리 오류 |

잘못된 REST API URL을 호출하면 HTTP `404`가 반환됩니다.

```bash
curl -i "http://127.0.0.1:5657/db/query"
```

## SQL 오류 응답

SQL 실행에 실패해도 HTTP 상태 코드는 `200`일 수 있습니다. 이 경우 `error_code`와
`error_message`를 확인합니다.

요청:

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELCT * FROM example"
```

응답 예시:

```json
{
  "error_code": 2001,
  "error_message": "Syntax error: near token (SELCT * FROM example).",
  "timezone": "+0900",
  "data": []
}
```

| 필드 | 설명 |
|------|------|
| `error_code` | `0`이면 성공, `0`이 아니면 오류 |
| `error_message` | 오류 원인 |
| `timezone` | 응답 타임존 오프셋 |

## Append 오류 응답

Append 요청은 전체 요청 처리 결과와 행 단위 성공/실패 수를 함께 확인합니다.

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

`error_code`가 `0`이어도 `append_failure`가 `0`보다 크면 일부 행이 삽입되지 않은
상태로 처리해야 합니다.

## 재시도 전략

| 오류 유형 | 재시도 여부 | 처리 |
|-----------|-------------|------|
| 네트워크 오류, 타임아웃 | 재시도 권장 | 지수 백오프 후 재시도 |
| HTTP `500` | 재시도 가능 | 서버 로그와 부하 상태 확인 |
| HTTP `404` | 재시도 불필요 | URL과 엔드포인트 수정 |
| `error_code != 0` SQL 오류 | 재시도 불필요 | SQL, 테이블, 권한, 타입 수정 |
| `append_failure > 0` | 애플리케이션 판단 | 실패 행을 확인하고 보정 후 재전송 |

## Python 재시도 예제

```python
import time
import requests

BASE_URL = "http://127.0.0.1:5657"

def query_with_retry(sql, max_retries=3, base_delay=1.0):
    last_error = None

    for attempt in range(max_retries):
        try:
            resp = requests.get(
                f"{BASE_URL}/machbase",
                params={"q": sql},
                timeout=10,
            )

            if resp.status_code == 404:
                raise ValueError("REST 엔드포인트 URL을 확인하십시오.")
            if resp.status_code >= 500:
                last_error = f"server error: HTTP {resp.status_code}"
            else:
                resp.raise_for_status()
                result = resp.json()
                if result.get("error_code") == 0:
                    return result
                raise ValueError(result.get("error_message"))

        except (requests.ConnectionError, requests.Timeout) as e:
            last_error = str(e)

        if attempt < max_retries - 1:
            time.sleep(base_delay * (2 ** attempt))

    raise RuntimeError(f"최대 재시도 횟수 초과: {last_error}")

result = query_with_retry("SELECT COUNT(*) FROM curl_sample")
print(result)
```

## 타임아웃 처리

REST API 요청에는 타임아웃을 설정합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --connect-timeout 5 \
  --max-time 30 \
  --data-urlencode "q=SELECT COUNT(*) FROM curl_sample"
```

Python에서는 다음처럼 연결 타임아웃과 읽기 타임아웃을 지정합니다.

```python
resp = requests.get(
    "http://127.0.0.1:5657/machbase",
    params={"q": "SELECT COUNT(*) FROM curl_sample"},
    timeout=(5, 30),
)
```

## 오류 처리 체크리스트

- REST 엔드포인트가 `/machbase`인지 확인합니다.
- HTTP 상태 코드가 `404` 또는 `500`이면 URL 또는 서버 상태를 먼저 확인합니다.
- HTTP `200` 응답에서도 `error_code`가 `0`인지 확인합니다.
- Append 요청은 `append_failure`를 함께 확인합니다.
- 모든 요청에 타임아웃을 설정합니다.
- SQL 오류는 재시도보다 SQL 문, 테이블 존재 여부, 컬럼 타입을 수정합니다.

드라이버와 SDK에 공통으로 적용되는 오류 처리 전략은 [오류 처리와 재시도](../../concepts-common/error-handling-retry/)를 참조하십시오.
