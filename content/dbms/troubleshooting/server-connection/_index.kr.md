---
type: docs
title: '16.2 서버와 연결 문제'
weight: 20
---
서버 프로세스 시작 실패, 네트워크 접속 불가, 인증 오류 등 서버와의 연결에 관련된 문제를 다룹니다.

## 이 섹션의 구성

| 페이지 | 증상 |
|--------|------|
| [서버가 시작되지 않을 때](/dbms/troubleshooting/server-connection/#start-server) | `machadmin -u` 실행 후 서버가 뜨지 않음, 포트 충돌, 라이선스 오류, 디스크 공간 부족 |
| [연결할 수 없을 때](/dbms/troubleshooting/server-connection/#connection) | 서버는 실행 중이나 클라이언트에서 Connection refused, 원격 접속 불가, 최대 연결 수 초과 |
| [인증이 실패할 때](/dbms/troubleshooting/server-connection/#failure-authentication) | 비밀번호 오류, AUTH KEY 인증 실패, 계정 잠금 |

## 빠른 확인

```bash
# 서버 프로세스 상태
machadmin -e

# 서버가 사용하는 포트 확인 (기본: 5656)
netstat -tlnp | grep 5656
```

```sql
-- 현재 접속된 세션 수
SELECT COUNT(*) FROM v$session;
```


<a id="start-server"></a>

## 서버가 시작되지 않을 때

`machadmin -u` 실행 후 서버가 시작되지 않으면 아래 체크리스트를 순서대로 확인합니다.

### 로그에서 원인 먼저 확인

서버 시작 실패의 원인은 항상 로그 파일에 기록됩니다. 다른 항목을 확인하기 전에 로그 맨 끝을 먼저 확인합니다.

```bash
tail -50 $MACHBASE_HOME/trc/machbase.trc
```

### 원인별 체크리스트

#### 1. 포트 충돌

다른 프로세스가 동일한 포트(기본값: 5656)를 사용 중이면 서버가 시작되지 않습니다.

```bash
# 5656 포트 사용 중인 프로세스 확인
netstat -tlnp | grep 5656

# 사용 중인 프로세스 PID 조회
lsof -i :5656
```

포트 충돌이 확인되면 충돌하는 프로세스를 종료하거나, `machbase.conf`의 `PORT_NO`를 다른 값으로 변경합니다.

#### 2. 데이터 디렉터리 권한 문제

Machbase 프로세스가 데이터 디렉터리에 접근할 권한이 없으면 시작할 수 없습니다.

```bash
# 데이터 디렉터리 권한 확인
ls -la $MACHBASE_HOME/dbs/

# Machbase 실행 사용자 확인
whoami
```

디렉터리 소유자와 Machbase를 실행하는 사용자가 일치하는지 확인합니다. 불일치하면 소유권을 변경합니다.

```bash
chown -R machbase:machbase $MACHBASE_HOME/dbs/
```

#### 3. 라이선스 만료 또는 파일 없음

라이선스가 만료되었거나 라이선스 파일이 없으면 서버가 시작되지 않습니다.

```bash
# 라이선스 파일 존재 여부 확인
ls -la $MACHBASE_HOME/conf/license.dat

# 설치된 라이선스 정보 확인
machadmin -f
```

라이선스 파일이 없거나 만료된 경우 Machbase 영업팀에 새 라이선스를 요청합니다.

#### 4. 디스크 공간 부족

데이터 디렉터리가 있는 파티션의 디스크 공간이 부족하면 서버가 시작되지 않을 수 있습니다.

```bash
# 전체 디스크 사용량 확인
df -h

# Machbase 데이터 디렉터리 크기 확인
du -sh $MACHBASE_HOME/dbs/
```

디스크 공간이 부족하면 불필요한 데이터나 오래된 로그 파일을 삭제합니다.

#### 5. 이전 프로세스 잔존

비정상 종료 후 이전 프로세스가 남아있으면 새 프로세스가 시작되지 않을 수 있습니다.

```bash
# Machbase 관련 프로세스 확인
ps aux | grep machbase
```

잔존 프로세스가 있으면 강제 종료합니다.

```bash
machadmin -k
```

강제 종료 후에도 프로세스가 남아있으면 직접 종료합니다.

```bash
kill -9 <PID>
```

### 강제 정리 후 재시작

위 확인을 마친 후 아래 순서로 재시작합니다.

```bash
# 1. 기존 프로세스 강제 종료
machadmin -k

# 2. 잠깐 대기 후 재시작
machadmin -u

# 3. 시작 확인
machadmin -e
```

{{< callout type="warning" >}}
`machadmin -k`는 강제 종료입니다. 재시작 시 서버가 이전 비정상 종료로부터 복구 절차를 실행합니다. 복구 중에는 시작 시간이 평소보다 길어질 수 있습니다.
{{< /callout >}}

### 관련 섹션

- [로그 확인](/dbms/troubleshooting/troubleshooting/#log-logs) — 로그 파일 분석 방법
- [연결할 수 없을 때](#connection) — 서버는 시작됐으나 접속이 안 될 때

<a id="connection"></a>

## 연결할 수 없을 때

서버 프로세스는 실행 중인데 클라이언트에서 접속이 안 되는 경우입니다. 네트워크, 방화벽, 서버 설정 순서로 확인합니다.

### 서버 실행 여부 먼저 확인

접속 문제를 진단하기 전에 서버가 실제로 실행 중인지 확인합니다.

```bash
machadmin -e
```

서버가 실행 중이 아니면 [서버가 시작되지 않을 때](#start-server)를 먼저 참조합니다.

### 네트워크 레벨 진단

#### 포트 접근 가능 여부 확인

```bash
# telnet으로 포트 연결 테스트 (기본 포트: 5656)
telnet <host> 5656

# nc(netcat)으로 확인
nc -zv <host> 5656
```

연결이 즉시 끊기거나 "Connection refused"가 나오면 네트워크 또는 방화벽 문제입니다.

#### 방화벽 규칙 확인

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

### 서버 설정 확인

#### 원격 접속 허용 여부 (GRANT_REMOTE_ACCESS)

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

#### 바인드 IP 주소 확인 (BIND_IP_ADDRESS)

서버가 특정 IP에만 바인딩되어 있으면 다른 IP로 접속할 수 없습니다.

```sql
-- 현재 바인드 IP 확인
SELECT name, value FROM v$property WHERE name = 'BIND_IP_ADDRESS';
```

값이 특정 IP(예: `127.0.0.1`)로 설정되어 있으면 모든 IP에서 접속 가능하도록 변경합니다.

```properties
BIND_IP_ADDRESS = 0.0.0.0
```

#### 최대 연결 수 초과 (MAX_SESSION_COUNT)

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

### 관련 섹션

- [서버가 시작되지 않을 때](#start-server) — 서버 프로세스 시작 문제
- [인증이 실패할 때](/dbms/troubleshooting/server-connection/#failure-authentication) — 접속은 되나 인증 오류가 날 때

<a id="failure-authentication"></a>

## 인증이 실패할 때

서버에 접속은 되지만 인증 단계에서 오류가 발생하는 경우입니다. Machbase는 비밀번호 인증과 AUTH KEY(공개키) 인증 두 가지를 지원합니다.

### 오류 메시지별 원인

| 메시지 | 원인 |
|--------|------|
| `Wrong password` | 비밀번호 불일치 |
| `Authentication failed` | 사용자명 또는 비밀번호 오류 |
| `Account locked` | 연속 인증 실패로 계정 잠금 |
| `Auth key not found` | 서버에 등록된 AUTH KEY 없음 |
| `Invalid auth key` | 키 파일 내용이 올바르지 않음 |
| `Password expired` | 비밀번호 유효기간 만료 (HIGH 보안 정책) |

### 비밀번호 인증 실패

#### 기본 계정 정보 확인

| 항목 | 기본값 |
|------|--------|
| 사용자명 | `SYS` |
| 비밀번호 | `MANAGER` |

Machbase의 사용자명은 대문자로 저장됩니다. `sys`로 입력해도 `SYS`로 처리됩니다.
비밀번호는 대소문자를 구분하지 않습니다. `manager`와 `MANAGER`는 동일합니다.

#### 비밀번호 재설정

SYS 계정으로 접속 가능한 다른 경로(예: 로컬 접속)가 있다면 비밀번호를 재설정합니다.

```sql
-- 사용자 비밀번호 변경
ALTER USER user_name IDENTIFIED BY 'new_password';
```

SYS 계정 자체를 잃었다면 Machbase 지원팀에 문의합니다.

#### 보안 정책 확인

HIGH 보안 정책 적용 시 비밀번호 만료 또는 잠금이 발생할 수 있습니다.

```sql
-- 현재 보안 정책 확인
SELECT name, value FROM v$property WHERE name LIKE '%PASSWORD%';
```

계정 잠금 상태는 SYS 계정으로 해제합니다.

```sql
-- 계정 잠금 해제
ALTER USER locked_user ACCOUNT UNLOCK;
```

### AUTH KEY 인증 실패

Machbase는 공개키/개인키 쌍을 이용한 AUTH KEY 인증을 지원합니다.

#### AUTH_MODE 설정 확인

```sql
-- AUTH_MODE 설정 확인
SELECT name, value FROM v$property WHERE name = 'AUTH_MODE';
```

AUTH KEY 인증을 사용하려면 값이 `CHALLENGE`여야 합니다.

#### 개인키 파일 경로와 권한 확인

```bash
# 개인키 파일 존재 여부와 권한 확인
ls -la ~/.machbase/auth_key

# 개인키 파일 권한은 반드시 600이어야 합니다
chmod 600 ~/.machbase/auth_key
```

개인키 파일의 권한이 너무 넓으면(예: 644) Machbase가 보안 위험으로 판단하여 인증을 거부합니다.

#### 서버에 등록된 공개키 확인

```sql
-- 특정 사용자의 등록된 AUTH KEY 목록
SELECT * FROM m$sys_auth_key WHERE user_name = 'SYS';

-- 모든 사용자의 AUTH KEY 확인
SELECT user_name, key_name, created_time FROM m$sys_auth_key;
```

등록된 키가 없거나 사용 중인 개인키와 쌍이 맞지 않으면 새 키 쌍을 생성하여 등록합니다.

```bash
# 새 키 쌍 생성
machsql -s localhost -u SYS -p MANAGER
```

```sql
-- 공개키 등록 (machsql에서)
CREATE AUTH KEY key_name FOR SYS FROM '/path/to/public_key.pub';
```

### 관련 섹션

- [연결할 수 없을 때](#connection) — 인증 이전에 접속 자체가 안 될 때
- [오류 코드로 원인 찾기](/dbms/troubleshooting/troubleshooting/#cause-lookup-error-codes) — ERR-021xx 권한 오류 코드 목록
