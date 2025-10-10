---
type: docs
title: '사용자 관리'
weight: 40
---

Machbase에서 사용자를 생성하고 권한을 부여하며 데이터베이스 보안을 관리하는 방법을 학습합니다.

## 사용자 관리 개요

### 기본 사용자

Machbase는 기본 관리자와 함께 제공됩니다:
- **사용자명**: SYS
- **비밀번호**: MANAGER
- **권한**: 전체 관리 권한

**중요**: 즉시 기본 비밀번호를 변경하세요!

```sql
ALTER USER SYS IDENTIFIED BY 'NewStr0ng!Password';
```

## 사용자 생성

### 기본 사용자 생성

```sql
-- 사용자 생성
CREATE USER analyst IDENTIFIED BY 'password123';

-- 강력한 비밀번호로 생성
CREATE USER dataeng IDENTIFIED BY 'Str0ng!P@ss2025';
```

### 사용자 이름 규칙

- 1-128자
- 문자, 숫자, 언더스코어
- 대소문자 구분 안 함
- 숫자로 시작할 수 없음

## 권한 부여

### 테이블 권한

```sql
-- SELECT 부여
GRANT SELECT ON sensors TO analyst;

-- INSERT 부여
GRANT INSERT ON sensors TO dataeng;

-- 여러 권한 부여
GRANT SELECT, INSERT ON sensors TO dataeng;

-- 테이블의 모든 권한 부여
GRANT ALL ON sensors TO admin_user;
```

### 데이터베이스 수준 권한

```sql
-- 모든 테이블에 SELECT 부여
GRANT SELECT ON DATABASE TO readonly_user;

-- 모든 권한 부여
GRANT ALL ON DATABASE TO admin_user;
```

### 시스템 권한

```sql
-- 사용자 관리 권한 부여
GRANT CREATE USER TO admin_user;

-- 테이블 생성 권한 부여
GRANT CREATE TABLE TO developer;
```

## 권한 취소

```sql
-- 특정 권한 취소
REVOKE SELECT ON sensors FROM analyst;

-- 여러 권한 취소
REVOKE INSERT, UPDATE ON sensors FROM dataeng;

-- 모든 권한 취소
REVOKE ALL ON sensors FROM old_user;
```

## 사용자 관리

### 사용자 보기

```sql
-- 모든 사용자 나열
SHOW USERS;

-- 사용자 권한 보기
SELECT * FROM SYSTEM_.SYS_USERS_;
```

### 비밀번호 변경

```sql
-- 자신의 비밀번호 변경
ALTER USER analyst IDENTIFIED BY 'NewPassword2025';

-- SYS는 모든 사용자의 비밀번호 변경 가능
ALTER USER dataeng IDENTIFIED BY 'ResetPassword';
```

### 사용자 삭제

```sql
-- 사용자 삭제
DROP USER analyst;

-- CASCADE와 함께 사용자 삭제 (모든 권한 제거)
DROP USER analyst CASCADE;
```

## 권한 수준

### 권한 매트릭스

| 권한 | SELECT | INSERT | UPDATE | DELETE | CREATE TABLE | DROP TABLE |
|-----------|--------|--------|--------|--------|--------------|------------|
| **READ_ONLY** | ✓ | | | | | |
| **DATA_WRITER** | ✓ | ✓ | ✓ | ✓ | | |
| **TABLE_ADMIN** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **SYS (Admin)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## 일반 사용자 역할

### 읽기 전용 사용자

```sql
CREATE USER readonly IDENTIFIED BY 'password';
GRANT SELECT ON DATABASE TO readonly;
```

### 데이터 분석가

```sql
CREATE USER analyst IDENTIFIED BY 'password';
GRANT SELECT ON sensors TO analyst;
GRANT SELECT ON logs TO analyst;
GRANT SELECT ON devices TO analyst;
```

### 애플리케이션 사용자

```sql
CREATE USER app_user IDENTIFIED BY 'password';
GRANT SELECT, INSERT ON sensors TO app_user;
GRANT SELECT, INSERT ON logs TO app_user;
```

### 관리자

```sql
CREATE USER admin IDENTIFIED BY 'password';
GRANT ALL ON DATABASE TO admin;
GRANT CREATE USER TO admin;
```

## 보안 모범 사례

### 1. 강력한 비밀번호

```sql
-- 좋음: 강력한 비밀번호
CREATE USER secure_user IDENTIFIED BY 'Tr0ng!P@ssw0rd#2025';

-- 나쁨: 약한 비밀번호
CREATE USER weak_user IDENTIFIED BY 'password';  -- 이렇게 하지 마세요!
```

**비밀번호 요구사항**:
- 최소 8자
- 대소문자 혼합
- 숫자 포함
- 특수 문자 포함

### 2. 최소 권한 원칙

```sql
-- 필요한 권한만 부여
CREATE USER report_user IDENTIFIED BY 'password';
GRANT SELECT ON sensors TO report_user;  -- INSERT/UPDATE/DELETE 권한 없음
```

### 3. 정기적인 비밀번호 변경

```bash
# 분기별 비밀번호 변경 정책
*/
ALTER USER analyst IDENTIFIED BY 'NewPasswordQ42025';
```

### 4. 비활성 사용자 제거

```sql
-- 정기적으로 감사 및 제거
DROP USER inactive_user;
```

### 5. 애플리케이션 사용자 분리

```sql
-- 애플리케이션에 SYS 사용 금지
-- 전용 앱 사용자 생성
CREATE USER sensor_app IDENTIFIED BY 'password';
GRANT SELECT, INSERT ON sensors TO sensor_app;
```

## 연결 예제

### 특정 사용자로 연결

```bash
# machsql
machsql -s localhost -u analyst -p password

# JDBC
jdbc:machbase://localhost:5656/MACHBASE?user=analyst&password=password

# Python
conn = machbase.connect('127.0.0.1', 5656, 'analyst', 'password')
```

## 감사

### 사용자 활동 모니터링

```sql
-- 활성 세션 확인
SHOW STATEMENTS;

-- 연결 이력 보기 (로그 확인)
-- $MACHBASE_HOME/trc/machbase.log
```

### 로그 분석

```bash
# 최근 로그인 보기
grep "LOGIN" $MACHBASE_HOME/trc/machbase.log | tail -20

# 로그인 실패 시도 확인
grep "LOGIN FAILED" $MACHBASE_HOME/trc/machbase.log
```

## 문제 해결

### 로그인 실패

```bash
# 사용자명 존재 확인
machsql -u SYS -p MANAGER -f - <<EOF
SHOW USERS;
EOF

# 비밀번호 재설정
machsql -u SYS -p MANAGER -f - <<EOF
ALTER USER analyst IDENTIFIED BY 'newpassword';
EOF
```

### 권한 거부

```sql
-- 사용자 권한 확인
-- (SYS로 연결)
SELECT * FROM SYSTEM_.SYS_USERS_ WHERE name = 'ANALYST';

-- 누락된 권한 부여
GRANT SELECT ON tablename TO analyst;
```

### 사용자 이미 존재

```sql
-- 삭제 후 재생성
DROP USER analyst;
CREATE USER analyst IDENTIFIED BY 'password';
```

## 완전한 예제

### 예제 1: 분석 팀

```sql
-- 분석가 생성
CREATE USER analyst1 IDENTIFIED BY 'Pass#2025!A1';
CREATE USER analyst2 IDENTIFIED BY 'Pass#2025!A2';

-- 읽기 전용 접근 권한 부여
GRANT SELECT ON sensors TO analyst1;
GRANT SELECT ON sensors TO analyst2;
GRANT SELECT ON logs TO analyst1;
GRANT SELECT ON logs TO analyst2;
GRANT SELECT ON devices TO analyst1;
GRANT SELECT ON devices TO analyst2;
```

### 예제 2: 애플리케이션 사용자

```sql
-- 센서 데이터 수집기
CREATE USER sensor_app IDENTIFIED BY 'SensApp#2025!';
GRANT INSERT ON sensors TO sensor_app;

-- 로그 수집기
CREATE USER log_app IDENTIFIED BY 'LogApp#2025!';
GRANT INSERT ON logs TO log_app;

-- 대시보드 애플리케이션
CREATE USER dashboard IDENTIFIED BY 'Dash#2025!';
GRANT SELECT ON sensors TO dashboard;
GRANT SELECT ON logs TO dashboard;
GRANT SELECT ON devices TO dashboard;
```

### 예제 3: 외부 파트너

```sql
-- 파트너를 위한 제한된 접근
CREATE USER partner IDENTIFIED BY 'Partner#2025!';

-- 특정 테이블과 시간 범위만
GRANT SELECT ON public_sensors TO partner;

-- 애플리케이션 로직으로 제한 (SQL이 아님)
-- 애플리케이션이 강제: DURATION 7 DAY만
```

## 사용자 관리 스크립트

```bash
#!/bin/bash
# user_management.sh

# 새 사용자 생성
create_user() {
    local username=$1
    local password=$2

    machsql -u SYS -p MANAGER -f - <<EOF
CREATE USER $username IDENTIFIED BY '$password';
EOF
}

# 권한 부여
grant_select() {
    local username=$1
    local table=$2

    machsql -u SYS -p MANAGER -f - <<EOF
GRANT SELECT ON $table TO $username;
EOF
}

# 사용법
create_user "newanalyst" "SecurePass#2025"
grant_select "newanalyst" "sensors"
grant_select "newanalyst" "logs"
```

## 다음 단계

- **백업 및 복구**: [백업 및 복구](../backup-recovery/) - 사용자 데이터 보호
- **연결하기**: [연결하기](../connecting/) - 사용자를 위한 연결 방법
- **보안**: [문제 해결](../../troubleshooting/) - 보안 모범 사례

---

적절한 사용자 관리로 Machbase 데이터에 대한 안전하고 제어된 접근을 보장하세요!
