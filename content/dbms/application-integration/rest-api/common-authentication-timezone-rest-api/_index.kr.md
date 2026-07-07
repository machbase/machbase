---
type: docs
title: 'REST API 공통 인증과 타임존'
weight: 10
---

Machbase REST API를 사용할 때 모든 엔드포인트에 공통으로 적용되는 인증 방법과 타임존 설정을 설명합니다.

## 인증

Machbase REST API는 두 가지 인증 방식을 지원합니다.

### Bearer Token 인증

로그인 API(`/db/login`)로 토큰을 발급받은 후 `Authorization` 헤더에 포함합니다.

**토큰 발급:**

```bash
curl -X POST http://127.0.0.1:5657/db/login \
  -H "Content-Type: application/json" \
  -d '{"loginName": "SYS", "password": "MANAGER"}'
```

응답 예시:

```json
{
  "success": true,
  "reason": "success",
  "elapse": "0.512ms",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**토큰 사용:**

발급받은 토큰을 이후 요청의 `Authorization` 헤더에 `Bearer` 접두사와 함께 포함합니다.

```bash
curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"q": "SELECT * FROM example LIMIT 5"}'
```

### AUTH KEY 인증

서버 설정에서 미리 지정한 AUTH KEY를 `Authorization` 헤더에 직접 사용합니다. 토큰 발급 과정 없이 정적 키로 인증할 때 사용합니다.

```bash
curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -H "Authorization: <AUTH_KEY>" \
  -d '{"q": "SELECT COUNT(*) FROM example"}'
```

> AUTH KEY는 `machbase.conf`의 `HTTP_AUTH_KEY` 항목에서 설정합니다.

### 인증 없는 접근 (개발 환경)

서버가 인증을 요구하지 않도록 설정된 경우(개발 환경 등) `Authorization` 헤더를 생략할 수 있습니다. 운영 환경에서는 반드시 인증을 활성화하십시오.

## Content-Type

요청 본문(body)이 있는 경우 반드시 `Content-Type: application/json` 헤더를 포함해야 합니다.

```
Content-Type: application/json
```

누락 시 서버가 요청 본문을 올바르게 파싱하지 못해 오류가 발생합니다.

## 타임존 설정

Machbase는 내부적으로 모든 시각을 UTC로 저장합니다. REST API를 통해 데이터를 조회하거나 삽입할 때 타임존을 지정하면 서버가 해당 타임존으로 변환하여 반환합니다.

타임존은 다음 두 가지 방법으로 지정할 수 있습니다.

### X-Timezone 헤더

요청 헤더에 `X-Timezone`을 포함합니다. IANA 타임존 이름 형식을 사용합니다.

```bash
curl -X POST http://127.0.0.1:5657/db/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "X-Timezone: Asia/Seoul" \
  -d '{"q": "SELECT name, time FROM example LIMIT 3"}'
```

### Query Parameter

URL 파라미터로 `tz`를 지정합니다.

```bash
curl -X POST "http://127.0.0.1:5657/db/query?tz=Asia/Seoul" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"q": "SELECT name, time FROM example LIMIT 3"}'
```

### 지원되는 타임존 값

| 값 | 설명 |
|----|------|
| `UTC` | 협정 세계시 (기본값) |
| `Asia/Seoul` | 한국 표준시 (KST, UTC+9) |
| `America/New_York` | 미국 동부 시간 |
| `Europe/London` | 영국 표준시 |

IANA Time Zone Database에 등록된 모든 타임존 이름을 사용할 수 있습니다.

## 공통 헤더 요약

| 헤더 | 필수 여부 | 예시 값 |
|------|-----------|---------|
| `Content-Type` | 필수 (본문이 있는 경우) | `application/json` |
| `Authorization` | 인증 활성화 시 필수 | `Bearer <token>` 또는 `<AUTH_KEY>` |
| `X-Timezone` | 선택 | `Asia/Seoul` |

## Python 예제

Python `requests` 라이브러리를 사용한 인증 및 타임존 설정 예제입니다.

```python
import requests

# 1. 토큰 발급
login_resp = requests.post(
    "http://127.0.0.1:5657/db/login",
    json={"loginName": "SYS", "password": "MANAGER"}
)
token = login_resp.json()["token"]

# 2. 공통 헤더 구성
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "X-Timezone": "Asia/Seoul",
}

# 3. 쿼리 실행
resp = requests.post(
    "http://127.0.0.1:5657/db/query",
    headers=headers,
    json={"q": "SELECT * FROM example LIMIT 5"}
)
print(resp.json())
```
