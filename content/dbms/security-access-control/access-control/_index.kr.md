---
type: docs
title: '14.5 접속 제어'
weight: 50
---
접속 제어는 어떤 네트워크 경로에서, 어떤 인증 방식으로 Machbase에 연결할 수 있는지를 결정합니다. 계정 인증보다 앞선 레이어에서 동작하므로, 접속 자체를 차단하는 강력한 보안 수단입니다.

## 이 섹션의 구성

| 항목 | 설명 |
|------|------|
| [원격 접속 설정](/dbms/security-access-control/access-control/#remote-access-configuration) | `GRANT_REMOTE_ACCESS`로 원격 접속 허용 여부 제어 |
| [HTTP 인증 설정](/dbms/security-access-control/access-control/#authentication-configuration-http) | `HTTP_AUTH`로 REST API Basic Auth 활성화 |
| [BIND_IP_ADDRESS와 네트워크 노출 제어](/dbms/security-access-control/access-control/#network-exposure-bind-ip-address) | 리스너가 열리는 네트워크 인터페이스 지정 |

## 접속 제어 관련 주요 설정

| 설정 항목 | 기본값 | 설명 |
|-----------|--------|------|
| `GRANT_REMOTE_ACCESS` | `1` | 원격 접속 허용(1) / 차단(0) |
| `BIND_IP_ADDRESS` | `0.0.0.0` | 리스너 바인드 주소 (모든 인터페이스) |
| `HTTP_AUTH` | `0` | REST API Basic Authentication 활성화(1) / 비활성화(0) |

설정은 `machbase.conf`에서 영구적으로 변경하거나, `ALTER SYSTEM SET` 구문으로 재시작 없이 즉시 반영할 수 있습니다.

```sql
-- 원격 접속 차단
ALTER SYSTEM SET GRANT_REMOTE_ACCESS = 0;

-- REST API Basic Auth 활성화
ALTER SYSTEM SET HTTP_AUTH = 1;
```


<a id="remote-access-configuration"></a>

## 원격 접속 설정

`GRANT_REMOTE_ACCESS`는 로컬호스트 이외의 IP에서 Machbase에 접속할 수 있는지를 제어합니다. 이 설정은 계정 인증 이전에 동작하므로, 차단 시 올바른 계정 정보를 가진 클라이언트라도 연결 자체가 거부됩니다.

### 설정값

| 값 | 동작 |
|----|------|
| `1` (기본값) | 원격 접속 허용. 모든 IP에서 연결 가능 |
| `0` | 원격 접속 차단. 로컬호스트(`127.0.0.1`, `::1`)에서만 연결 가능 |

### 설정 방법

#### machbase.conf에서 영구 설정

```ini
GRANT_REMOTE_ACCESS = 0
```

변경 후 Machbase를 재시작해야 적용됩니다.

#### ALTER SYSTEM SET으로 즉시 반영

```sql
-- 원격 접속 차단 (재시작 불필요)
ALTER SYSTEM SET GRANT_REMOTE_ACCESS = 0;

-- 원격 접속 허용으로 복구
ALTER SYSTEM SET GRANT_REMOTE_ACCESS = 1;
```

현재 설정값은 다음 쿼리로 확인할 수 있습니다.

```sql
SELECT name, value FROM v$property WHERE name = 'GRANT_REMOTE_ACCESS';
```

### 사용 시나리오

#### 개발 / 테스트 환경

외부 노출 위험을 최소화하려면 원격 접속을 차단하고 로컬 접속만 허용합니다.

```sql
ALTER SYSTEM SET GRANT_REMOTE_ACCESS = 0;
```

애플리케이션을 같은 서버에 배포하거나 SSH 터널을 통해 연결하면 됩니다.

#### 운영 환경 (원격 접속 필요)

원격 접속을 허용하되, `BIND_IP_ADDRESS` 설정과 방화벽을 함께 구성해 허용 대역을 제한하는 것을 권장합니다.

```ini
GRANT_REMOTE_ACCESS = 1
BIND_IP_ADDRESS = 192.168.1.100   # 내부 네트워크 인터페이스만 리슨
```

방화벽 규칙으로 허용할 클라이언트 IP를 추가로 제한하면 보안 수준을 높일 수 있습니다.

### 주의사항

- `GRANT_REMOTE_ACCESS = 0`으로 차단한 상태에서 원격 머신에서 연결을 시도하면 인증 오류가 아니라 접속 거부 오류가 반환됩니다.
- `BIND_IP_ADDRESS`와 조합해 사용하면 더욱 세밀한 네트워크 노출 제어가 가능합니다. ([BIND_IP_ADDRESS와 네트워크 노출 제어](/dbms/security-access-control/access-control/#network-exposure-bind-ip-address) 참고)

<a id="authentication-configuration-http"></a>

## HTTP 인증 설정

Machbase는 기본 TCP 연결 외에 REST API를 통한 HTTP 접속을 지원합니다. 현재 내장 HTTP
서버 기준 인증 방식은 `HTTP_AUTH` 설정에 따른 HTTP Basic Authentication입니다.

### 관련 설정 항목

| 설정 항목 | 기본값 | 설명 |
|-----------|--------|------|
| `HTTP_PORT_NO` | `5657` | REST API 리스너 포트 |
| `HTTP_AUTH` | `0` | Basic Authentication 활성화(1) / 비활성화(0) |

`HTTP_AUTH=0`이면 HTTP 요청은 인증 헤더 없이 SYS 세션으로 처리됩니다. 외부 노출
환경에서는 `HTTP_AUTH=1`을 사용하고, HTTPS가 필요하면 reverse proxy나 TLS terminator를
앞단에 배치합니다.

### Basic Authentication 활성화

`HTTP_AUTH = 1`로 설정하면 REST API 요청에 HTTP Basic Authentication 헤더가 필수가 됩니다.

#### machbase.conf에서 영구 설정

```ini
HTTP_AUTH = 1
```

변경 후 Machbase를 재시작해야 적용됩니다.

#### ALTER SYSTEM SET으로 즉시 반영

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

### Basic Auth 사용 예시 (`HTTP_AUTH = 1` 필요)

```bash
curl -G "http://localhost:5657/machbase" \
  -u "sys:manager" \
  --data-urlencode "q=SELECT count(*) FROM sensor_log"
```

{{< callout type="warning" >}}
Basic Authentication은 자격증명이 Base64 인코딩만 되어 평문과 동일합니다. 내장 HTTP
서버를 외부에 노출해야 한다면 외부 reverse proxy에서 HTTPS를 구성하십시오.
{{< /callout >}}

### 권장 운영 환경 구성

```ini
# machbase.conf 권장 설정 (운영)
HTTP_PORT_NO     = 5657
HTTP_AUTH        = 1       # Basic Auth 강제
```

운영 환경에서는 내장 HTTP 포트를 내부망에만 바인딩하거나 방화벽으로 제한하고, 외부 HTTPS는
reverse proxy/TLS terminator에서 처리하는 구성을 권장합니다.

<a id="network-exposure-bind-ip-address"></a>

## BIND_IP_ADDRESS와 네트워크 노출 제어

`BIND_IP_ADDRESS`는 Machbase 리스너(TCP 포트)가 어느 네트워크 인터페이스에서 연결을 수신할지 지정합니다. 서버에 여러 네트워크 인터페이스(NIC)가 있을 때 특정 인터페이스에만 서비스를 노출할 수 있습니다. REST API를 포함한 모든 Machbase 리스너 포트에 동일하게 적용됩니다.

### 설정값

| 설정값 | 동작 |
|--------|------|
| `0.0.0.0` (기본값) | 모든 네트워크 인터페이스에서 연결 수신 |
| `127.0.0.1` | 로컬호스트에서만 연결 수신. REST API 포함 외부 노출 없음 |
| `192.168.1.100` | 지정한 IP를 가진 인터페이스에서만 연결 수신 |

### 설정 방법

`machbase.conf`에서 설정합니다. 변경 후 Machbase를 재시작해야 적용됩니다.

```ini
# 모든 인터페이스 (기본)
BIND_IP_ADDRESS = 0.0.0.0

# 로컬호스트 전용
BIND_IP_ADDRESS = 127.0.0.1

# 내부 네트워크 인터페이스만 노출
BIND_IP_ADDRESS = 192.168.1.100
```

현재 설정값 확인:

```sql
SELECT name, value FROM v$property WHERE name = 'BIND_IP_ADDRESS';
```

### 네트워크 보안 전략

#### 단일 서버, 로컬 접속 전용

Machbase와 애플리케이션이 같은 서버에서 동작할 때는 `127.0.0.1`로 설정해 외부 노출을 완전히 차단합니다.

```ini
BIND_IP_ADDRESS = 127.0.0.1
GRANT_REMOTE_ACCESS = 0
```

이 설정에서는 REST API (`HTTP_PORT_NO`)를 포함한 모든 포트가 외부에서 접근 불가합니다.

#### 내부 네트워크에만 서비스 노출

서버에 공인 IP와 내부 IP가 모두 있을 때, 내부 인터페이스에만 바인드해 공인 인터넷에서의 접근을 차단합니다.

```ini
BIND_IP_ADDRESS = 10.0.0.5       # 내부 네트워크 인터페이스 IP
GRANT_REMOTE_ACCESS = 1
```

#### 방화벽과 함께 사용

`BIND_IP_ADDRESS = 0.0.0.0`으로 모든 인터페이스에서 수신하되, 방화벽(iptables, firewalld, 클라우드 보안 그룹)으로 접근 가능한 클라이언트 IP를 제한하는 방법입니다. 운영 환경에서 가장 일반적인 구성입니다.

```bash
# 예시: iptables로 Machbase 포트(5656)를 특정 대역에만 허용
iptables -A INPUT -p tcp --dport 5656 -s 10.0.0.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 5656 -j DROP
```

### BIND_IP_ADDRESS와 GRANT_REMOTE_ACCESS 조합

두 설정은 독립적으로 동작하므로 함께 구성할 수 있습니다.

| `BIND_IP_ADDRESS` | `GRANT_REMOTE_ACCESS` | 결과 |
|-------------------|-----------------------|------|
| `0.0.0.0` | `1` | 모든 IP에서 접속 가능 (기본) |
| `0.0.0.0` | `0` | 로컬호스트에서만 접속 가능 |
| `127.0.0.1` | `1` | 로컬호스트에서만 접속 가능 (바인드 자체가 로컬) |
| `192.168.1.100` | `1` | 해당 인터페이스 IP로만 접속 가능 |
| `192.168.1.100` | `0` | 해당 인터페이스에서도 로컬호스트 연결만 허용 |

### 주의사항

- `BIND_IP_ADDRESS`는 `machbase.conf`에서만 설정할 수 있으며, `ALTER SYSTEM SET`으로 런타임에 변경할 수 없습니다.
- 잘못된 IP(서버에 없는 인터페이스 주소)를 설정하면 Machbase가 시작되지 않을 수 있습니다.
- IPv6를 사용하는 경우 `::` (모든 인터페이스) 또는 `::1` (로컬호스트)을 사용합니다.
