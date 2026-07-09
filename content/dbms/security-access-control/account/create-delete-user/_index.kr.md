---
type: docs
title: '14.2.1 사용자 생성과 삭제'
weight: 10
---

## 사용자 생성

`CREATE USER` 구문으로 새 사용자를 생성합니다.

```sql
-- 기본 생성
CREATE USER new_user IDENTIFIED BY 'password';

-- 비밀번호 정책 지정 (Machbase 8.5 이상)
CREATE USER app_user IDENTIFIED BY 'Aa!StrongPwd1' PASSWORD POLICY LOW;
CREATE USER ops_user IDENTIFIED BY 'Bb@StrongPwd2' PASSWORD POLICY HIGH;
```

사용자명은 생성 시 **대문자로 변환되어 저장**됩니다. `CREATE USER app_user ...`로 생성하면 메타 테이블과 권한 구문에서는 `APP_USER`로 조회됩니다.

비밀번호 정책을 지정하지 않으면 `NONE`이 기본 적용됩니다. 정책에 대한 자세한 설명은 [비밀번호 정책](../policy-password/)을 참고하세요.

## 사용자 삭제

`DROP USER` 구문으로 사용자를 삭제합니다.

```sql
DROP USER user_name;
```

삭제 시 주의사항:

- `SYS` 계정은 삭제할 수 없습니다.
- 현재 연결 중인 계정(자기 자신)은 삭제할 수 없습니다.
- 삭제 대상 사용자가 소유한 테이블이 있으면 오류가 발생합니다. 해당 테이블을 먼저 삭제해야 합니다.

```sql
-- 테이블을 보유한 사용자 삭제 순서 예시
-- 1) 해당 사용자로 연결해 테이블 삭제
CONNECT user1/password;
DROP TABLE user1_table;

-- 2) SYS로 다시 연결해 사용자 삭제
CONNECT SYS/manager_password;
DROP USER user1;
```

## 비밀번호 변경

`ALTER USER` 구문으로 비밀번호를 변경합니다.

```sql
-- 비밀번호만 변경
ALTER USER user_name IDENTIFIED BY 'new_password';

-- 비밀번호와 정책 동시 변경 (Machbase 8.5 이상)
ALTER USER user_name IDENTIFIED BY 'new_password' PASSWORD POLICY HIGH;
```

다른 사용자의 비밀번호는 SYS 계정에서만 변경할 수 있습니다. 일반 사용자는 자신의 비밀번호만 변경할 수 있습니다.

## 사용자 목록 확인

```sql
-- 기본 사용자 목록
SELECT user_id, user_name FROM m$user;

-- 비밀번호 정책과 만료 시각 포함
SELECT user_id, name, pwd_policy_level, valid_before
FROM m$sys_users;
```

`PWD_POLICY_LEVEL` 값은 `0 = NONE`, `1 = LOW`, `2 = HIGH`를 의미합니다.

## 사용자 간 전환 (재연결)

machadmin이나 machsql 등 CLI 도구에서 애플리케이션을 종료하지 않고 다른 사용자로 전환할 수 있습니다.

```sql
CONNECT user1/password;
```

## 실행 예시

```
-- SYS 계정으로 사용자 생성
Mach> CREATE USER demo IDENTIFIED BY 'demo';
Created successfully.

-- 사용자 삭제
Mach> DROP USER demo;
Dropped successfully.

-- SYS 계정 삭제 시도 (오류)
Mach> DROP USER SYS;
[ERR-02083 : Drop user error. You cannot drop yourself(SYS).]

-- 테이블을 보유한 사용자 삭제 시도 (오류)
Mach> DROP USER demo1;
[ERR-02084 : DROP user error. The user's tables still exist. Drop those tables first.]

-- 다른 사용자의 비밀번호 변경 시도 (오류, 일반 사용자)
Mach> ALTER USER demo2 IDENTIFIED BY 'demo22';
[ERR-02085 : ALTER user error. The user(DEMO2) does not have ALTER privileges.]
```
