---
type: docs
title: '원격 접속 설정'
weight: 10
---

`GRANT_REMOTE_ACCESS`는 로컬호스트 이외의 IP에서 Machbase에 접속할 수 있는지를 제어합니다. 이 설정은 계정 인증 이전에 동작하므로, 차단 시 올바른 계정 정보를 가진 클라이언트라도 연결 자체가 거부됩니다.

## 설정값

| 값 | 동작 |
|----|------|
| `1` (기본값) | 원격 접속 허용. 모든 IP에서 연결 가능 |
| `0` | 원격 접속 차단. 로컬호스트(`127.0.0.1`, `::1`)에서만 연결 가능 |

## 설정 방법

### machbase.conf에서 영구 설정

```ini
GRANT_REMOTE_ACCESS = 0
```

변경 후 Machbase를 재시작해야 적용됩니다.

### ALTER SYSTEM SET으로 즉시 반영

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

## 사용 시나리오

### 개발 / 테스트 환경

외부 노출 위험을 최소화하려면 원격 접속을 차단하고 로컬 접속만 허용합니다.

```sql
ALTER SYSTEM SET GRANT_REMOTE_ACCESS = 0;
```

애플리케이션을 같은 서버에 배포하거나 SSH 터널을 통해 연결하면 됩니다.

### 운영 환경 (원격 접속 필요)

원격 접속을 허용하되, `BIND_IP_ADDRESS` 설정과 방화벽을 함께 구성해 허용 대역을 제한하는 것을 권장합니다.

```ini
GRANT_REMOTE_ACCESS = 1
BIND_IP_ADDRESS = 192.168.1.100   # 내부 네트워크 인터페이스만 리슨
```

방화벽 규칙으로 허용할 클라이언트 IP를 추가로 제한하면 보안 수준을 높일 수 있습니다.

## 주의사항

- `GRANT_REMOTE_ACCESS = 0`으로 차단한 상태에서 원격 머신에서 연결을 시도하면 인증 오류가 아니라 접속 거부 오류가 반환됩니다.
- `BIND_IP_ADDRESS`와 조합해 사용하면 더욱 세밀한 네트워크 노출 제어가 가능합니다. ([BIND_IP_ADDRESS와 네트워크 노출 제어](../network-exposure-bind-ip-address/) 참고)
