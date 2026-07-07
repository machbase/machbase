---
type: docs
title: '비밀번호 정책'
weight: 20
---

Machbase 8.5부터 사용자별로 비밀번호 강도 정책을 지정할 수 있습니다. 정책은 `CREATE USER`와 `ALTER USER ... IDENTIFIED BY ...` 구문에서 비밀번호가 요건을 충족하는지 검증합니다.

## 정책 종류

| 정책 | 최소 길이 | 조합 규칙 | 비밀번호 재사용 제한 | 만료(`VALID_BEFORE`) |
|------|----------|-----------|---------------------|----------------------|
| `NONE` | 없음 | 없음 | 없음 | NULL (만료 없음) |
| `LOW` | 10자 이상 | 대문자 + 소문자 + 특수문자 포함 | 없음 | NULL (만료 없음) |
| `HIGH` | 10자 이상 | LOW 규칙 모두 적용 | 최근 24개 비밀번호 재사용 불가 | 설정 시점 기준 90일 후 자동 설정 |

### NONE

비밀번호 강도 제약이 없습니다. 정책을 지정하지 않을 때 기존 호환성을 위해 기본 적용됩니다.

### LOW

다음 요건을 모두 충족해야 합니다.

- 최소 10자 이상
- 대문자, 소문자, 특수문자를 포함
- 5자리 이상 연속 숫자 사용 불가 (예: `12345`)
- 증가/감소 숫자 연번 사용 불가 (예: `123456`, `654321`)
- 키보드 연속 문자열 사용 불가 (예: `qwerty`)

### HIGH

LOW의 모든 규칙을 적용하고 다음을 추가합니다.

- 현재 비밀번호와 최근 24개 이내 과거 비밀번호 재사용 불가
- 비밀번호 설정 시점으로부터 90일 후 자동 만료

만료된 계정은 로그인이 불가합니다. 만료 후에는 SYS 등 관리자 계정에서 새 비밀번호로 변경해야 합니다.

## 정책 지정 예시

```sql
-- 정책 없음 (기본값)
CREATE USER user1 IDENTIFIED BY 'password' PASSWORD POLICY NONE;

-- LOW 정책: 대소문자 + 특수문자 + 10자 이상
CREATE USER user2 IDENTIFIED BY 'Aa!StrongPwd1' PASSWORD POLICY LOW;

-- HIGH 정책: LOW 규칙 + 재사용 제한 + 90일 만료
CREATE USER user3 IDENTIFIED BY 'Bb@StrongPwd2' PASSWORD POLICY HIGH;
```

## 정책 변경

`ALTER USER ... IDENTIFIED BY ... PASSWORD POLICY ...` 구문으로 정책을 변경합니다. 정책을 변경할 때는 새 비밀번호를 반드시 함께 지정해야 합니다.

```sql
-- user2의 정책을 LOW에서 HIGH로 변경
ALTER USER user2 IDENTIFIED BY 'Cc#NewPwd33' PASSWORD POLICY HIGH;

-- user3의 정책을 HIGH에서 NONE으로 낮춤 (VALID_BEFORE가 NULL로 초기화됨)
ALTER USER user3 IDENTIFIED BY 'simplePwd' PASSWORD POLICY NONE;
```

> **주의**: `ALTER USER user_name PASSWORD POLICY HIGH`처럼 비밀번호 없이 정책만 단독으로 변경하는 구문은 허용되지 않습니다.

## 정책 적용 규칙 상세

- `ALTER USER ... IDENTIFIED BY ...`(정책 미지정): 해당 사용자에 저장된 현재 정책으로 새 비밀번호를 검증합니다.
- `ALTER USER ... IDENTIFIED BY ... PASSWORD POLICY ...`(정책 지정): 지정한 새 정책으로 새 비밀번호를 검증합니다.
- 정책을 `HIGH`로 설정하거나 `HIGH` 사용자의 비밀번호를 변경하면 `VALID_BEFORE`가 현재 시각 기준 90일 후로 갱신됩니다.
- 정책을 `LOW` 또는 `NONE`으로 변경하면 `VALID_BEFORE`는 `NULL`로 초기화됩니다.

## 정책 현황 조회

```sql
SELECT user_id, name, pwd_policy_level, valid_before
FROM m$sys_users;
```

`PWD_POLICY_LEVEL` 값: `0 = NONE`, `1 = LOW`, `2 = HIGH`

`VALID_BEFORE` 값이 있을 때는 `YYYY-MM-DD` 형식으로 표시됩니다.
