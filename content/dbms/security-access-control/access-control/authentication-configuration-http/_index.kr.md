---
type: docs
title: '14.5.2 HTTP 인증 설정'
weight: 20
---

Machbase는 기본 TCP 연결 외에 REST API를 통한 HTTP 접속을 지원합니다. 현재 내장 HTTP
서버 기준 인증 방식은 `HTTP_AUTH` 설정에 따른 HTTP Basic Authentication입니다.

## 관련 설정 항목

| 설정 항목 | 기본값 | 설명 |
|-----------|--------|------|
| `HTTP_PORT_NO` | `5657` | REST API 리스너 포트 |
| `HTTP_AUTH` | `0` | Basic Authentication 활성화(1) / 비활성화(0) |

`HTTP_AUTH=0`이면 HTTP 요청은 인증 헤더 없이 SYS 세션으로 처리됩니다. 외부 노출
환경에서는 `HTTP_AUTH=1`을 사용하고, HTTPS가 필요하면 reverse proxy나 TLS terminator를
앞단에 배치합니다.

## Basic Authentication 활성화

`HTTP_AUTH = 1`로 설정하면 REST API 요청에 HTTP Basic Authentication 헤더가 필수가 됩니다.

### machbase.conf에서 영구 설정

```ini
HTTP_AUTH = 1
```

변경 후 Machbase를 재시작해야 적용됩니다.

### ALTER SYSTEM SET으로 즉시 반영

```sql
-- Basic Auth 활성화
ALTER SYSTEM SET HTTP_AUTH = 1;

-- Basic Auth 비활성화
ALTER SYSTEM SET HTTP_AUTH = 0;
```

현재 설정값 확인:

```sql
SELECT name, value FROM v$property WHERE name = 'HTTP_AUTH';
```

## Basic Auth 사용 예시 (`HTTP_AUTH = 1` 필요)

```bash
curl -G "http://localhost:5657/machbase" \
  -u "sys:manager" \
  --data-urlencode "q=SELECT count(*) FROM sensor_log"
```

{{< callout type="warning" >}}
Basic Authentication은 자격증명이 Base64 인코딩만 되어 평문과 동일합니다. 내장 HTTP
서버를 외부에 노출해야 한다면 외부 reverse proxy에서 HTTPS를 구성하십시오.
{{< /callout >}}

## 권장 운영 환경 구성

```ini
# machbase.conf 권장 설정 (운영)
HTTP_PORT_NO     = 5657
HTTP_AUTH        = 1       # Basic Auth 강제
```

운영 환경에서는 내장 HTTP 포트를 내부망에만 바인딩하거나 방화벽으로 제한하고, 외부 HTTPS는
reverse proxy/TLS terminator에서 처리하는 구성을 권장합니다.
