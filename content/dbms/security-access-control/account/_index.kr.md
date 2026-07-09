---
type: docs
title: '14.2 계정 관리'
weight: 20
---
Machbase에서 데이터베이스에 접근하는 모든 주체는 사용자 계정으로 식별됩니다. 계정 관리는 사용자를 생성하고 삭제하는 기본 작업부터, 비밀번호 정책으로 계정 보안 수준을 강화하는 것까지 포함합니다.

## 이 섹션의 구성

| 항목 | 설명 |
|------|------|
| [사용자 생성과 삭제](/dbms/security-access-control/account/#create-delete-user) | CREATE USER, DROP USER, ALTER USER, 사용자 목록 조회 |
| [비밀번호 정책](/dbms/security-access-control/account/#policy-password) | NONE/LOW/HIGH 정책, 비밀번호 만료, 정책 변경 방법 |

## 계정 관리 핵심 사항

- 사용자명은 대문자로 저장됩니다. `CREATE USER app_user ...`로 생성하면 메타 테이블에는 `APP_USER`로 기록됩니다.
- `SYS` 계정은 삭제할 수 없습니다.
- 테이블을 보유한 사용자는 해당 테이블을 먼저 삭제해야 계정을 삭제할 수 있습니다.
- Machbase 8.5부터 비밀번호 정책(NONE/LOW/HIGH)을 계정별로 지정할 수 있습니다.
- AUTH KEY(공개키 기반 인증) 등록은 [AUTH KEY 인증](../authentication-auth-key/) 섹션을 참고하세요.


<a id="create-delete-user"></a>

## 사용자 생성과 삭제

### 사용자 생성

`CREATE USER` 구문으로 새 사용자를 생성합니다.

```sql
-- 기본 생성
CREATE USER new_user IDENTIFIED BY 'password';

-- 비밀번호 정책 지정 (Machbase 8.5 이상)
CREATE USER app_user IDENTIFIED BY 'Aa!StrongPwd1' PASSWORD POLICY LOW;
CREATE USER ops_user IDENTIFIED BY 'Bb@StrongPwd2' PASSWORD POLICY HIGH;
```

사용자명은 생성 시 **대문자로 변환되어 저장**됩니다. `CREATE USER app_user ...`로 생성하면 메타 테이블과 권한 구문에서는 `APP_USER`로 조회됩니다.

비밀번호 정책을 지정하지 않으면 `NONE`이 기본 적용됩니다. 정책에 대한 자세한 설명은 [비밀번호 정책](/dbms/security-access-control/account/#policy-password)을 참고하세요.

### 사용자 삭제

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

### 비밀번호 변경

`ALTER USER` 구문으로 비밀번호를 변경합니다.

```sql
-- 비밀번호만 변경
ALTER USER user_name IDENTIFIED BY 'new_password';

-- 비밀번호와 정책 동시 변경 (Machbase 8.5 이상)
ALTER USER user_name IDENTIFIED BY 'new_password' PASSWORD POLICY HIGH;
```

다른 사용자의 비밀번호는 SYS 계정에서만 변경할 수 있습니다. 일반 사용자는 자신의 비밀번호만 변경할 수 있습니다.

### 사용자 목록 확인

```sql
-- 기본 사용자 목록
SELECT user_id, user_name FROM m$user;

-- 비밀번호 정책과 만료 시각 포함
SELECT user_id, name, pwd_policy_level, valid_before
FROM m$sys_users;
```

`PWD_POLICY_LEVEL` 값은 `0 = NONE`, `1 = LOW`, `2 = HIGH`를 의미합니다.

### 사용자 간 전환 (재연결)

machadmin이나 machsql 등 CLI 도구에서 애플리케이션을 종료하지 않고 다른 사용자로 전환할 수 있습니다.

```sql
CONNECT user1/password;
```

### 실행 예시

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

<a id="policy-password"></a>

## 비밀번호 정책

Machbase 8.5부터 사용자별로 비밀번호 강도 정책을 지정할 수 있습니다. 정책은 `CREATE USER`와 `ALTER USER ... IDENTIFIED BY ...` 구문에서 비밀번호가 요건을 충족하는지 검증합니다.

### 정책 종류

| 정책 | 최소 길이 | 조합 규칙 | 비밀번호 재사용 제한 | 만료(`VALID_BEFORE`) |
|------|----------|-----------|---------------------|----------------------|
| `NONE` | 없음 | 없음 | 없음 | NULL (만료 없음) |
| `LOW` | 10자 이상 | 영문자 + 특수문자 포함 | 없음 | NULL (만료 없음) |
| `HIGH` | 10자 이상 | LOW 규칙 모두 적용 | 최근 24개 비밀번호 재사용 불가 | 설정 시점 기준 90일 후 자동 설정 |

#### NONE

비밀번호 강도 제약이 없습니다. 정책을 지정하지 않을 때 기존 호환성을 위해 기본 적용됩니다.

#### LOW

다음 요건을 모두 충족해야 합니다.

- 최소 10자 이상
- 기본값인 `ENABLE_CASE_SENSITIVE_PASSWORD=0`에서는 대문자/소문자를 구분하지 않고 영문자 1자 이상과 특수문자 1자 이상을 포함
- `ENABLE_CASE_SENSITIVE_PASSWORD=1`에서는 대문자, 소문자, 특수문자를 모두 포함
- 5자리 이상 연속 숫자 사용 불가 (예: `12345`)
- 증가/감소 숫자 연번 사용 불가 (예: `123456`, `654321`)
- 키보드 연속 문자열 사용 불가 (예: `qwerty`)

#### HIGH

LOW의 모든 규칙을 적용하고 다음을 추가합니다.

- 현재 비밀번호와 최근 24개 이내 과거 비밀번호 재사용 불가
- 비밀번호 설정 시점으로부터 90일 후 자동 만료

만료된 계정은 로그인이 불가합니다. 만료 후에는 SYS 등 관리자 계정에서 새 비밀번호로 변경해야 합니다.

### 정책 지정 예시

```sql
-- 정책 없음 (기본값)
CREATE USER user1 IDENTIFIED BY 'password' PASSWORD POLICY NONE;

-- LOW 정책: 영문자 + 특수문자 + 10자 이상
CREATE USER user2 IDENTIFIED BY 'Aa!StrongPwd1' PASSWORD POLICY LOW;

-- HIGH 정책: LOW 규칙 + 재사용 제한 + 90일 만료
CREATE USER user3 IDENTIFIED BY 'Bb@StrongPwd2' PASSWORD POLICY HIGH;
```

### 정책 변경

`ALTER USER ... IDENTIFIED BY ... PASSWORD POLICY ...` 구문으로 정책을 변경합니다. 정책을 변경할 때는 새 비밀번호를 반드시 함께 지정해야 합니다.

```sql
-- user2의 정책을 LOW에서 HIGH로 변경
ALTER USER user2 IDENTIFIED BY 'Cc#NewPwd33' PASSWORD POLICY HIGH;

-- user3의 정책을 HIGH에서 NONE으로 낮춤 (VALID_BEFORE가 NULL로 초기화됨)
ALTER USER user3 IDENTIFIED BY 'simplePwd' PASSWORD POLICY NONE;
```

> **주의**: `ALTER USER user_name PASSWORD POLICY HIGH`처럼 비밀번호 없이 정책만 단독으로 변경하는 구문은 허용되지 않습니다.

### 정책 적용 규칙 상세

- `ALTER USER ... IDENTIFIED BY ...`(정책 미지정): 해당 사용자에 저장된 현재 정책으로 새 비밀번호를 검증합니다.
- `ALTER USER ... IDENTIFIED BY ... PASSWORD POLICY ...`(정책 지정): 지정한 새 정책으로 새 비밀번호를 검증합니다.
- 정책을 `HIGH`로 설정하거나 `HIGH` 사용자의 비밀번호를 변경하면 `VALID_BEFORE`가 현재 시각 기준 90일 후로 갱신됩니다.
- 정책을 `LOW` 또는 `NONE`으로 변경하면 `VALID_BEFORE`는 `NULL`로 초기화됩니다.
- `ENABLE_CASE_SENSITIVE_PASSWORD=1`일 때만 LOW/HIGH 정책에서 대문자와 소문자를
  각각 요구합니다. 기본값 `0`에서는 대소문자 구분 없이 영문자와 특수문자 조합을 검사합니다.

### 정책 현황 조회

```sql
SELECT user_id, name, pwd_policy_level, valid_before
FROM m$sys_users;
```

`PWD_POLICY_LEVEL` 값: `0 = NONE`, `1 = LOW`, `2 = HIGH`

`VALID_BEFORE` 값이 있을 때는 `YYYY-MM-DD` 형식으로 표시됩니다.
