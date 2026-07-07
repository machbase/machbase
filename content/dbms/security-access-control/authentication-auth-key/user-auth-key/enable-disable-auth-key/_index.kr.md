---
type: docs
title: 'AUTH KEY 활성화/비활성화'
weight: 30
---

## 개요

등록된 AUTH KEY를 키 삭제 없이 임시로 비활성화하거나 다시 활성화할 수 있습니다. 비활성화된 키는 챌린지 인증에 사용할 수 없습니다.

## 구문

```sql
-- AUTH KEY 비활성화
ALTER USER app_user DEACTIVATE AUTH KEY ID <key_id>;

-- AUTH KEY 활성화
ALTER USER app_user ACTIVATE AUTH KEY ID <key_id>;
```

## 예제

```sql
-- key_id 3번 키 비활성화
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;

-- key_id 3번 키 다시 활성화
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

## 활용 사례

**키 롤오버 중 이전 키 차단**

신규 키로 클라이언트 전환이 완료된 후 이전 키를 비활성화합니다. 이전 키를 바로 삭제하지 않고 비활성화 상태로 잠시 보관하면, 문제 발생 시 빠르게 복구할 수 있습니다.

```sql
-- 이전 키(key_id=1) 비활성화
ALTER USER app_user DEACTIVATE AUTH KEY ID 1;

-- 충분한 검증 기간 후 삭제
ALTER USER app_user DROP AUTH KEY ID 1;
```

**보안 이슈 발생 시 즉각 차단**

특정 클라이언트 호스트에서 이상 접속이 감지된 경우, 해당 호스트의 키를 즉시 비활성화하여 접속을 차단합니다.

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 2;
```

**유지보수 기간 중 임시 차단**

클라이언트 점검이나 유지보수 중 해당 계정의 AUTH KEY 인증을 임시로 차단합니다.

```sql
-- 유지보수 시작 시 비활성화
ALTER USER app_user DEACTIVATE AUTH KEY ID 1;

-- 유지보수 완료 후 재활성화
ALTER USER app_user ACTIVATE AUTH KEY ID 1;
```

## 활성화 상태 확인

```sql
SELECT key_id, user_name, key_algo, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

`ACTIVATED` 컬럼 값:
- `1`: 활성 상태 — 챌린지 인증에 사용 가능
- `0`: 비활성 상태 — 챌린지 인증에 사용 불가

## 주의 사항

- 한 사용자의 모든 AUTH KEY가 비활성화되면 해당 사용자는 AUTH KEY 인증을 사용할 수 없습니다. `AUTH_MODE=PASSWORD`로 접속하거나, SYS 계정에서 키를 재활성화해야 합니다.
- 비활성화와 달리 삭제(`DROP AUTH KEY`)는 복구할 수 없습니다. 일시적 차단에는 비활성화를 사용하세요.
