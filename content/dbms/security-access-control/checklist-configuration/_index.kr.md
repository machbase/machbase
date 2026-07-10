---
type: docs
title: '14.6 보안 설정 체크리스트'
weight: 60
---

운영 환경 배포 전 점검 항목입니다. 환경에 따라 선택적으로 적용할 수 있습니다.

## 계정 보안

### SYS 기본 비밀번호 변경

설치 후 SYS 계정의 기본 비밀번호(`MANAGER`)를 반드시 변경합니다.

```sql
ALTER USER SYS IDENTIFIED BY '새_강력한_비밀번호' PASSWORD POLICY HIGH;
```

### 최소 권한 계정 사용

애플리케이션 용도에 맞게 별도 계정을 생성하고, SYS 계정은 관리 작업 전용으로만 사용합니다.

```sql
-- 읽기 전용 계정
CREATE USER reader IDENTIFIED BY 'Reader#2024!' PASSWORD POLICY HIGH;
GRANT SELECT ON sys.sensor_log TO reader;

-- 데이터 입력 전용 계정
CREATE USER writer IDENTIFIED BY 'Writer#2024!' PASSWORD POLICY HIGH;
GRANT SELECT, INSERT ON sys.sensor_log TO writer;

-- DDL 전용 계정
CREATE USER deploy IDENTIFIED BY 'Deploy#2024!' PASSWORD POLICY HIGH;
GRANT DDL ON machbasedb TO deploy;
```

### 불필요한 계정 제거

현재 등록된 모든 계정을 확인하고 사용하지 않는 계정을 삭제합니다.

```sql
-- 전체 사용자 확인
SELECT * FROM m$user;

-- 비밀번호 정책 및 만료 상태 확인
SELECT user_id, name, pwd_policy_level, valid_before
FROM m$sys_users;
```

## 권한 최소화

### 권한 현황 확인

```sql
-- 데이터베이스 권한 확인
SELECT * FROM m$sys_privileges;

-- 테이블 권한 확인
SELECT * FROM m$obj_privileges;
```

### 과도한 권한 제거

필요 이상으로 부여된 권한을 회수합니다.

```sql
-- 특정 사용자의 BACKUP 권한 회수
REVOKE BACKUP ON machbasedb FROM user1;

-- 특정 테이블에 대한 DELETE 권한 회수
REVOKE DELETE ON sys.sensor_log FROM user2;
```

## 접속 제어

### GRANT_REMOTE_ACCESS 검토

원격 접속이 필요하지 않은 환경이라면 차단합니다.

```sql
-- 현재 설정 확인
SELECT name, value FROM v$property WHERE name = 'GRANT_REMOTE_ACCESS';

-- 원격 접속 차단 (로컬 전용)
ALTER SYSTEM SET GRANT_REMOTE_ACCESS = 0;
```

### BIND_IP_ADDRESS 설정

서버에 여러 인터페이스가 있다면 내부 인터페이스에만 바인드합니다.

```ini
# machbase.conf
BIND_IP_ADDRESS = 10.0.0.5   # 내부 네트워크 인터페이스
```

### REST API 인증 활성화

REST API를 사용 중이라면 인증을 활성화하고, HTTPS가 필요할 때는 외부 reverse proxy 또는
TLS terminator에서 처리합니다.

```sql
ALTER SYSTEM SET HTTP_AUTH = 1;
```

내장 HTTP 서버의 nfx 기준 설정 항목은 `HTTP_ENABLE`, `HTTP_PORT_NO`, `HTTP_AUTH`입니다.

## AUTH KEY 인증 도입 검토

서비스 계정의 비밀번호 유출 위험을 제거하려면 AUTH KEY(공개키 기반 인증)를 도입하십시오.

```bash
# 클라이언트에서 키 생성
openssl ecparam -name prime256v1 -genkey -noout -out app_user_ecdsa.key
openssl ec -in app_user_ecdsa.key -pubout -out app_user_ecdsa.pub
chmod 600 app_user_ecdsa.key
```

```sql
-- 서버에 공개키 등록
ALTER USER app_user ADD AUTH KEY (
    key='공개키_PEM_내용_여기에_입력',
    valid_before='2027-12-31',
    comment='production key'
);
```

설정 방법은 [AUTH KEY 인증](../authentication-auth-key/)을 참고하십시오.

## 정기 점검 항목

운영 중에도 아래 항목을 주기적으로 점검합니다.

| 점검 항목 | 확인 쿼리 | 권장 주기 |
|-----------|-----------|-----------|
| 전체 사용자 목록 | `SELECT * FROM m$user;` | 월 1회 |
| 비밀번호 만료 계정 | `SELECT name, valid_before FROM m$sys_users WHERE valid_before IS NOT NULL;` | 주 1회 |
| 데이터베이스 권한 현황 | `SELECT * FROM m$sys_privileges;` | 월 1회 |
| 테이블 권한 현황 | `SELECT * FROM m$obj_privileges;` | 월 1회 |
| AUTH KEY 유효기간 | `SELECT user_name, key_id, valid_before FROM v$user_auth_keys;` | 월 1회 |

## 빠른 점검 스크립트

```sql
-- 1. 전체 사용자 목록
SELECT user_id, user_name FROM m$user ORDER BY user_id;

-- 2. 비밀번호 정책 및 만료 현황
SELECT user_id, name, pwd_policy_level, valid_before
FROM m$sys_users
ORDER BY user_id;

-- 3. 데이터베이스 권한 현황
SELECT * FROM m$sys_privileges;

-- 4. 테이블 권한 현황
SELECT * FROM m$obj_privileges;

-- 5. 접속 제어 설정 확인
SELECT name, value FROM v$property
WHERE name IN ('GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS', 'HTTP_AUTH');
```
