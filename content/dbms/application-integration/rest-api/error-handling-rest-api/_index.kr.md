---
type: docs
title: 'REST API 오류 처리'
weight: 50
---

Machbase REST API를 사용할 때 발생할 수 있는 오류 유형과 처리 방법을 설명합니다. 안정적인 애플리케이션을 작성하려면 HTTP 상태 코드와 응답 본문의 오류 정보를 올바르게 처리해야 합니다.

## HTTP 상태 코드

Machbase REST API는 표준 HTTP 상태 코드를 사용합니다.

| 상태 코드 | 의미 | 주요 원인 |
|-----------|------|-----------|
| `200 OK` | 요청 성공 | 정상 처리 |
| `400 Bad Request` | 잘못된 요청 | 요청 본문 형식 오류, SQL 문법 오류 |
| `401 Unauthorized` | 인증 실패 | Authorization 헤더 누락 또는 토큰 만료 |
| `403 Forbidden` | 권한 없음 | 해당 리소스에 대한 접근 권한 부족 |
| `404 Not Found` | 리소스 없음 | 존재하지 않는 엔드포인트 또는 테이블 |
| `500 Internal Server Error` | 서버 오류 | 서버 내부 처리 오류 |

## 오류 응답 형식

HTTP 상태 코드가 오류를 나타내는 경우에도 응답 본문은 JSON 형식으로 반환됩니다.

```json
{
  "success": false,
  "reason": "오류 메시지",
  "elapse": "0.123ms"
}
```

또는 `data` 필드 없이 다음과 같이 반환될 수 있습니다.

```json
{
  "success": false,
  "reason": "table 'NONEXISTENT' does not exist",
  "elapse": "0.234ms"
}
```

| 필드 | 설명 |
|------|------|
| `success` | `false`이면 오류 발생 |
| `reason` | 오류 원인을 설명하는 메시지 |
| `elapse` | 서버 측 처리 소요 시간 |

## 주요 오류 유형별 처리

### 400 Bad Request - SQL 문법 오류

SQL 문에 문법 오류가 있거나 요청 JSON 형식이 잘못된 경우 발생합니다.

요청:
```bash
curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"q": "SELCT * FROM example"}'
```

응답:
```json
{
  "success": false,
  "reason": "error near 'SELCT': syntax error",
  "elapse": "0.089ms"
}
```

**처리 방법:** SQL 문을 검토하고 수정합니다. 동적으로 SQL을 생성하는 경우 입력값 검증 로직을 추가하십시오.

### 401 Unauthorized - 인증 실패

`Authorization` 헤더가 없거나 토큰이 만료된 경우 발생합니다.

응답:
```json
{
  "success": false,
  "reason": "unauthorized",
  "elapse": "0.045ms"
}
```

**처리 방법:** 토큰을 재발급(`POST /db/login`)하고 요청을 재시도합니다.

### 500 Internal Server Error - 서버 오류

서버 내부 처리 중 예상치 못한 오류가 발생한 경우입니다.

응답:
```json
{
  "success": false,
  "reason": "internal server error",
  "elapse": "10.234ms"
}
```

**처리 방법:** 잠시 후 재시도하거나 서버 로그를 확인합니다.

## 재시도 전략

일시적인 오류(네트워크 단절, 서버 과부하 등)에 대응하기 위해 지수 백오프(exponential backoff) 방식의 재시도를 구현하는 것을 권장합니다.

### 재시도 대상 상태 코드

| 상태 코드 | 재시도 여부 | 이유 |
|-----------|-------------|------|
| `200` | 불필요 | 성공 |
| `400` | 불필요 | 요청 자체의 문제이므로 수정 필요 |
| `401` | 토큰 재발급 후 재시도 | 인증 만료는 복구 가능 |
| `500` | 재시도 권장 | 일시적 서버 오류일 수 있음 |
| 네트워크 오류 | 재시도 권장 | 연결 자체의 일시적 문제 |

### Python 재시도 예제

```python
import requests
import time

BASE_URL = "http://127.0.0.1:5657"

def query_with_retry(sql, token, max_retries=3, base_delay=1.0):
    """지수 백오프 방식으로 쿼리를 재시도합니다."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    last_error = None

    for attempt in range(max_retries):
        try:
            resp = requests.post(
                f"{BASE_URL}/db/query",
                headers=headers,
                json={"q": sql},
                timeout=10  # 타임아웃 설정
            )

            if resp.status_code == 200:
                result = resp.json()
                if result.get("success"):
                    return result
                else:
                    # success=false이지만 HTTP 200인 경우 (SQL 오류 등)
                    # 재시도 없이 즉시 예외 발생
                    raise ValueError(f"쿼리 실패: {result.get('reason')}")

            elif resp.status_code == 401:
                # 인증 만료: 토큰 재발급 후 재시도
                raise PermissionError("인증이 필요합니다. 토큰을 재발급하십시오.")

            elif resp.status_code == 400:
                # 잘못된 요청: 재시도 없음
                result = resp.json()
                raise ValueError(f"잘못된 요청: {result.get('reason')}")

            elif resp.status_code >= 500:
                # 서버 오류: 재시도
                last_error = f"서버 오류 (HTTP {resp.status_code})"

        except (requests.ConnectionError, requests.Timeout) as e:
            last_error = f"연결 오류: {e}"

        if attempt < max_retries - 1:
            delay = base_delay * (2 ** attempt)  # 지수 백오프: 1s, 2s, 4s
            print(f"재시도 {attempt + 1}/{max_retries - 1}: {delay}초 후 재시도...")
            time.sleep(delay)

    raise RuntimeError(f"최대 재시도 횟수 초과: {last_error}")


# 사용 예
try:
    token = "your-token-here"
    result = query_with_retry("SELECT COUNT(*) FROM sensor_data", token)
    print(result)
except ValueError as e:
    print(f"요청 오류 (수정 필요): {e}")
except RuntimeError as e:
    print(f"서버 오류 (나중에 재시도): {e}")
```

## 타임아웃 처리

REST API 요청에는 반드시 타임아웃을 설정하십시오. 타임아웃 없이 요청하면 서버가 응답하지 않을 때 클라이언트가 무한정 대기할 수 있습니다.

### curl 타임아웃

```bash
# 연결 타임아웃 5초, 전체 요청 타임아웃 30초
curl -X POST http://127.0.0.1:5657/db/query \
  --connect-timeout 5 \
  --max-time 30 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"q": "SELECT COUNT(*) FROM sensor_data"}'
```

### Python 타임아웃

```python
import requests

resp = requests.post(
    "http://127.0.0.1:5657/db/query",
    headers={"Content-Type": "application/json", "Authorization": "Bearer <token>"},
    json={"q": "SELECT COUNT(*) FROM sensor_data"},
    timeout=(5, 30)  # (연결 타임아웃, 읽기 타임아웃) 초 단위
)
```

## 오류 처리 체크리스트

애플리케이션에서 다음 항목을 반드시 처리하십시오.

- HTTP 상태 코드를 확인하고 200이 아닌 경우 오류로 처리합니다.
- HTTP 200이더라도 응답 JSON의 `success` 필드가 `false`인 경우를 처리합니다.
- 모든 요청에 적절한 타임아웃을 설정합니다.
- 401 오류 발생 시 토큰을 자동으로 재발급하는 로직을 구현합니다.
- 500 오류 및 네트워크 오류에 대해 지수 백오프 재시도를 구현합니다.
- 400 오류는 재시도하지 않고 요청 자체를 수정합니다.

## 공통 오류 처리 참고

드라이버와 SDK에 공통으로 적용되는 오류 처리 전략은 [오류 처리와 재시도](../../concepts-common/error-handling-retry/)를 참조하십시오.
