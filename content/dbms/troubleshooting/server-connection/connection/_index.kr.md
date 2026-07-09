---
type: docs
title: '16.2.2 연결할 수 없을 때'
weight: 20
---

서버 프로세스는 정상 실행 중인데 클라이언트에서 접속이 안 되는 경우를 다룹니다. 네트워크, 방화벽, 서버 설정 순서로 확인합니다.

## 서버 실행 여부 먼저 확인

접속 문제를 진단하기 전에 서버가 실제로 실행 중인지 확인합니다.

```bash
machadmin -e
```

서버가 실행 중이 아니면 [서버가 시작되지 않을 때](../start-server/)를 먼저 참조합니다.

## 네트워크 레벨 진단

### 포트 접근 가능 여부 확인

```bash
# telnet으로 포트 연결 테스트 (기본 포트: 5656)
telnet <host> 5656

# nc(netcat)으로 확인
nc -zv <host> 5656
```

연결이 즉시 끊기거나 "Connection refused"가 나오면 네트워크 또는 방화벽 문제입니다.

### 방화벽 규칙 확인

```bash
# iptables에서 5656 포트 관련 규칙 확인
iptables -L -n | grep 5656

# firewalld 사용 환경
firewall-cmd --list-ports
```

방화벽이 차단하고 있으면 5656 포트를 허용합니다.

```bash
# iptables 포트 허용 (임시)
iptables -A INPUT -p tcp --dport 5656 -j ACCEPT

# firewalld 포트 영구 허용
firewall-cmd --permanent --add-port=5656/tcp
firewall-cmd --reload
```

## 서버 설정 확인

### 원격 접속 허용 여부 (GRANT_REMOTE_ACCESS)

기본 설정에서는 원격 접속이 비허용일 수 있습니다.

```sql
-- 원격 접속 허용 설정 확인
SELECT name, value FROM v$property WHERE name = 'GRANT_REMOTE_ACCESS';
```

값이 `0`이면 원격 접속이 차단됩니다. `machbase.conf`에서 변경합니다.

```properties
GRANT_REMOTE_ACCESS = 1
```

설정 변경 후 서버를 재시작합니다.

### 바인드 IP 주소 확인 (BIND_IP_ADDRESS)

서버가 특정 IP에만 바인딩되어 있으면 다른 IP로 접속할 수 없습니다.

```sql
-- 현재 바인드 IP 확인
SELECT name, value FROM v$property WHERE name = 'BIND_IP_ADDRESS';
```

값이 특정 IP(예: `127.0.0.1`)로 설정되어 있으면 모든 IP에서 접속 가능하도록 변경합니다.

```properties
BIND_IP_ADDRESS = 0.0.0.0
```

### 최대 연결 수 초과 (MAX_SESSION_COUNT)

동시 접속 수가 최대값에 도달하면 새 연결을 거부합니다.

```sql
-- 현재 세션 수와 최대값 확인
SELECT COUNT(*) AS current FROM v$session;
SELECT name, value FROM v$property WHERE name = 'MAX_SESSION_COUNT';
```

현재 세션 수가 최대값에 가까우면 다음을 검토합니다.

- 유휴 세션을 종료하도록 애플리케이션 커넥션 풀 설정을 검토합니다.
- `machbase.conf`에서 `MAX_SESSION_COUNT` 값을 늘립니다.

```sql
-- 세션 목록 확인
SELECT id, login_time, user_name, user_ip, closed
FROM v$session
ORDER BY login_time;
```

{{< callout type="warning" >}}
`MAX_SESSION_COUNT`를 무한정 늘리면 메모리 부족이 발생할 수 있습니다. 세션당 메모리 사용량을 고려하여 적절한 값을 설정합니다.
{{< /callout >}}

## 관련 섹션

- [서버가 시작되지 않을 때](../start-server/) — 서버 프로세스 시작 문제
- [인증이 실패할 때](../failure-authentication/) — 접속은 되나 인증 오류가 날 때
