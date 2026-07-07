---
type: docs
title: 'AUTH KEY 삭제'
weight: 50
---

## 개요

`ALTER USER ... DROP AUTH KEY` 구문으로 등록된 AUTH KEY를 영구 삭제합니다. 삭제된 키는 즉시 인증에 사용할 수 없으며 복구할 수 없습니다.

## 구문

```sql
ALTER USER app_user DROP AUTH KEY ID <key_id>;
```

## 예제

```sql
-- key_id 3번 키 삭제
ALTER USER app_user DROP AUTH KEY ID 3;

-- 삭제 전 대상 키 확인
SELECT key_id, user_name, key_algo, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

## key_id 확인

삭제할 KEY의 `key_id`는 `V$USER_AUTH_KEYS`에서 조회합니다.

```sql
SELECT key_id, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

## AUTH KEY 삭제 후 인증 방식

AUTH KEY를 삭제하면 해당 사용자의 남은 AUTH KEY 현황에 따라 인증 가능 여부가 결정됩니다.

| 삭제 후 상황 | 가능한 인증 방식 |
|------------|----------------|
| 다른 활성 AUTH KEY가 남아 있음 | AUTH KEY 인증 계속 가능 |
| 모든 AUTH KEY가 삭제됨 | 비밀번호 인증만 가능 |
| 모든 AUTH KEY가 삭제되고 비밀번호 없음 | 접속 불가 |

## 사용자 삭제 시 연동

`DROP USER` 실행 시 해당 사용자의 모든 AUTH KEY 메타가 함께 정리됩니다. 별도로 AUTH KEY를 먼저 삭제할 필요가 없습니다.

```sql
-- 사용자 삭제 시 AUTH KEY 메타도 자동 정리
DROP USER app_user;
```

## 삭제 전 권장 절차

영구 삭제 전에 먼저 비활성화하고 일정 기간 후 삭제하는 절차를 권장합니다.

```sql
-- 1단계: 비활성화 (접속 차단, 복구 가능)
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;

-- 2단계: 충분한 검증 기간 후 영구 삭제
ALTER USER app_user DROP AUTH KEY ID 3;

-- 3단계: 삭제 확인
SELECT key_id, user_name, key_algo, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```
