---
type: docs
title: 'HTTP 인증 설정'
weight: 20
---

Machbase는 기본 TCP 연결 외에 REST API를 통한 HTTP 접속을 지원합니다. HTTP 접속에는 JWT Bearer Token 방식과 Basic Authentication 방식 두 가지를 사용할 수 있으며, `HTTP_AUTH` 설정으로 Basic Auth를 활성화합니다.

## 관련 설정 항목

| 설정 항목 | 기본값 | 설명 |
|-----------|--------|------|
| `HTTP_PORT_NO` | `5657` | REST API 리스너 포트 |
| `HTTP_AUTH` | `0` | Basic Authentication 활성화(1) / 비활성화(0) |
| `HTTP_ENABLE_TLS` | `0` | HTTPS(TLS) 활성화(1) / 비활성화(0) |
| `HTTP_TLS_CERT_FILE` | (없음) | TLS 인증서 파일 경로 |
| `HTTP_TLS_KEY_FILE` | (없음) | TLS 개인키 파일 경로 |

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

## Bearer Token 방식 vs Basic Auth 비교

| 구분 | Bearer Token (JWT) | Basic Authentication |
|------|-------------------|----------------------|
| 활성화 방법 | 항상 사용 가능 | `HTTP_AUTH = 1` 필요 |
| 인증 절차 | `/db/login` 엔드포인트로 토큰 발급 후 사용 | 요청마다 사용자명/비밀번호를 Base64 인코딩해 전송 |
| 보안 | 토큰 만료 시간 제한 가능 | 요청마다 자격증명 전송 (HTTPS 필수) |
| 사용 적합 | 웹 애플리케이션, 장기 세션 | 스크립트, 간단한 API 테스트 |

### Bearer Token 사용 예시

```bash
# 1단계: 로그인해 토큰 발급
TOKEN=$(curl -s -X POST "http://localhost:5657/db/login" \
  -H "Content-Type: application/json" \
  -d '{"loginName":"sys","password":"manager"}' \
  | jq -r '.data.accessToken')

# 2단계: 토큰으로 API 요청
curl -X POST "http://localhost:5657/db/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"q":"SELECT count(*) FROM sensor_log"}'
```

### Basic Auth 사용 예시 (`HTTP_AUTH = 1` 필요)

```bash
curl -X POST "http://localhost:5657/db/query" \
  -u "sys:manager" \
  -H "Content-Type: application/json" \
  -d '{"q":"SELECT count(*) FROM sensor_log"}'
```

> **주의**: Basic Authentication은 자격증명이 Base64 인코딩만 되어 평문과 동일합니다. 반드시 HTTPS와 함께 사용해야 합니다.

## HTTPS 설정 (TLS)

REST API를 HTTPS로 노출하려면 TLS 인증서와 키 파일을 준비하고 `machbase.conf`에 설정합니다.

```ini
HTTP_ENABLE_TLS  = 1
HTTP_TLS_CERT_FILE = /path/to/server.crt
HTTP_TLS_KEY_FILE  = /path/to/server.key
```

자체 서명 인증서(테스트용) 생성 예시:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt \
  -days 365 -nodes -subj "/CN=machbase.local"
```

HTTPS 활성화 후 클라이언트 접속:

```bash
# 자체 서명 인증서는 -k 또는 --cacert로 처리
curl -k -X POST "https://localhost:5657/db/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"q":"SELECT count(*) FROM sensor_log"}'
```

## 권장 운영 환경 구성

```ini
# machbase.conf 권장 설정 (운영)
HTTP_PORT_NO     = 5657
HTTP_AUTH        = 1       # Basic Auth 강제
HTTP_ENABLE_TLS  = 1       # HTTPS 필수
HTTP_TLS_CERT_FILE = /etc/machbase/tls/server.crt
HTTP_TLS_KEY_FILE  = /etc/machbase/tls/server.key
```

운영 환경에서는 HTTPS와 Basic Auth를 함께 활성화하거나, HTTPS 없이는 Bearer Token 방식만 사용하는 것을 권장합니다.
