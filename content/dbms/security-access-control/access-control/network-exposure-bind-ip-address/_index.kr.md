---
type: docs
title: 'BIND_IP_ADDRESS와 네트워크 노출 제어'
weight: 30
---

`BIND_IP_ADDRESS`는 Machbase 리스너(TCP 포트)가 어느 네트워크 인터페이스에서 연결을 수신할지 지정합니다. 서버에 여러 네트워크 인터페이스(NIC)가 있을 때 특정 인터페이스에만 서비스를 노출할 수 있습니다. REST API를 포함한 모든 Machbase 리스너 포트에 동일하게 적용됩니다.

## 설정값

| 설정값 | 동작 |
|--------|------|
| `0.0.0.0` (기본값) | 모든 네트워크 인터페이스에서 연결 수신 |
| `127.0.0.1` | 로컬호스트에서만 연결 수신. REST API 포함 외부 노출 없음 |
| `192.168.1.100` | 지정한 IP를 가진 인터페이스에서만 연결 수신 |

## 설정 방법

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

## 네트워크 보안 전략

### 단일 서버, 로컬 접속 전용

Machbase와 애플리케이션이 같은 서버에서 동작할 때는 `127.0.0.1`로 설정해 외부 노출을 완전히 차단합니다.

```ini
BIND_IP_ADDRESS = 127.0.0.1
GRANT_REMOTE_ACCESS = 0
```

이 설정에서는 REST API (`HTTP_PORT_NO`)를 포함한 모든 포트가 외부에서 접근 불가합니다.

### 내부 네트워크에만 서비스 노출

서버에 공인 IP와 내부 IP가 모두 있을 때, 내부 인터페이스에만 바인드해 공인 인터넷에서의 접근을 차단합니다.

```ini
BIND_IP_ADDRESS = 10.0.0.5       # 내부 네트워크 인터페이스 IP
GRANT_REMOTE_ACCESS = 1
```

### 방화벽과 함께 사용

`BIND_IP_ADDRESS = 0.0.0.0`으로 모든 인터페이스에서 수신하되, 방화벽(iptables, firewalld, 클라우드 보안 그룹)으로 접근 가능한 클라이언트 IP를 제한하는 방법입니다. 운영 환경에서 가장 일반적인 구성입니다.

```bash
# 예시: iptables로 Machbase 포트(5656)를 특정 대역에만 허용
iptables -A INPUT -p tcp --dport 5656 -s 10.0.0.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 5656 -j DROP
```

## BIND_IP_ADDRESS와 GRANT_REMOTE_ACCESS 조합

두 설정은 독립적으로 동작하므로 함께 구성할 수 있습니다.

| `BIND_IP_ADDRESS` | `GRANT_REMOTE_ACCESS` | 결과 |
|-------------------|-----------------------|------|
| `0.0.0.0` | `1` | 모든 IP에서 접속 가능 (기본) |
| `0.0.0.0` | `0` | 로컬호스트에서만 접속 가능 |
| `127.0.0.1` | `1` | 로컬호스트에서만 접속 가능 (바인드 자체가 로컬) |
| `192.168.1.100` | `1` | 해당 인터페이스 IP로만 접속 가능 |
| `192.168.1.100` | `0` | 해당 인터페이스에서도 로컬호스트 연결만 허용 |

## 주의사항

- `BIND_IP_ADDRESS`는 `machbase.conf`에서만 설정할 수 있으며, `ALTER SYSTEM SET`으로 런타임에 변경할 수 없습니다.
- 잘못된 IP(서버에 없는 인터페이스 주소)를 설정하면 Machbase가 시작되지 않을 수 있습니다.
- IPv6를 사용하는 경우 `::` (모든 인터페이스) 또는 `::1` (로컬호스트)을 사용합니다.
