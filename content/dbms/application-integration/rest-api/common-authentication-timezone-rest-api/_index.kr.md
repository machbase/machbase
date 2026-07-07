---
type: docs
title: 'REST API 공통 설정'
weight: 10
---

Machbase REST API를 사용할 때 공통으로 확인해야 할 HTTP 포트, 인증 설정, 요청 헤더를
설명합니다.

## HTTP 포트

REST API는 `machbase.conf`의 HTTP 설정을 사용합니다. 기본 샘플 설정에서는 다음 값을
사용합니다.

```text
HTTP_ENABLE = 1
HTTP_PORT_NO = 5657
HTTP_AUTH = 0
```

`HTTP_ENABLE`이 `1`이면 REST API 서비스가 활성화됩니다. `HTTP_PORT_NO`는 REST API가
수신하는 포트입니다.

## 인증

기본 샘플 설정의 `HTTP_AUTH = 0` 상태에서는 REST API 요청에 별도 인증 헤더가 필요하지
않습니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT 1"
```

`machbase.conf` 샘플 파일에는 `HTTP_AUTH`가 “REST API 서비스의 Basic Authentication
활성화” 항목으로 제공됩니다. 운영 환경에서 HTTP 인증을 활성화하는 경우 배포 환경의
인증 정책에 맞게 Basic Authentication 설정과 계정을 확인한 뒤 클라이언트에
`Authorization` 헤더를 추가합니다.

```bash
curl -u "SYS:MANAGER" \
  -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT 1"
```

현재 REST 샘플과 서버 검증 기준으로 별도 로그인 토큰 발급 API나 Bearer 토큰 방식은
사용하지 않습니다.

## Content-Type

요청 본문이 있는 Append 요청은 JSON 본문을 사용하므로 `Content-Type:
application/json` 헤더를 지정합니다.

```bash
curl -X POST "http://127.0.0.1:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"curl_sample","values":[[1,"aaa"]]}'
```

SQL 실행처럼 본문이 없는 GET 요청에는 `Content-Type` 헤더가 필요하지 않습니다.

## 타임존

REST SQL 응답에는 `timezone` 필드가 포함됩니다.

```json
{
  "error_code": 0,
  "error_message": "",
  "data": [
    {"NOW": "2026-07-07 12:00:00 000:000:000"}
  ],
  "timezone": "+0000"
}
```

시간 조건을 작성할 때는 Machbase SQL의 `DATETIME`, `NOW`, `SYSDATE`,
`TO_DATE`, `TO_CHAR` 함수와 나노초 단위 시간 연산을 사용합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT TO_CHAR(NOW, 'YYYY-MM-DD HH24:MI:SS') AS now_text"
```

클라이언트가 특정 지역 시간 문자열을 사용자에게 보여야 하는 경우에는 SQL에서
`TO_CHAR`로 원하는 문자열을 만들거나 애플리케이션에서 응답 값을 변환합니다.

## 공통 헤더 요약

| 헤더 | 필수 여부 | 설명 |
|------|-----------|------|
| `Content-Type: application/json` | POST Append 요청에서 필수 | JSON 본문 파싱 |
| `Authorization` | `HTTP_AUTH` 활성화 시 필요 | Basic Authentication 설정에 맞게 지정 |

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

print(query("SELECT 1"))
```
