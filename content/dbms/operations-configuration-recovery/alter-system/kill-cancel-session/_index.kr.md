---
type: docs
title: 'KILL / CANCEL SESSION'
weight: 40
---

실행 중인 세션을 제어하는 두 가지 명령어입니다. `KILL SESSION`은 세션 자체를 강제 종료하고, `CANCEL SESSION`은 세션은 유지하면서 현재 실행 중인 쿼리만 중단합니다.

## KILL SESSION

```sql
ALTER SYSTEM KILL SESSION <session_id>;
```

지정한 세션 ID의 연결을 즉시 끊습니다.

- 대상 세션의 접속이 종료되고, 진행 중이던 트랜잭션은 롤백됩니다.
- `SYS` 계정만 실행할 수 있습니다.
- 자신의 세션이나 권한 없는 세션을 대상으로 하면 오류가 발생합니다.

**오류 코드**

| 상황 | 오류 |
|---|---|
| 세션 ID가 존재하지 않음 | `ERR_MM_SESSION_ID_NOT_FOUND` |
| 권한 없음 (자신 또는 다른 사용자) | `ERR-03025: Not enough privileges to manipulate the session.` |

**예시**

```sql
-- 현재 세션 목록 확인
SELECT id, user_id, client_type, query FROM v$session;

-- 세션 ID 12를 강제 종료
ALTER SYSTEM KILL SESSION 12;
```

## CANCEL SESSION

```sql
ALTER SYSTEM CANCEL SESSION <session_id>;
```

지정한 세션에서 현재 실행 중인 SQL만 중단합니다. 세션 연결 자체는 유지됩니다.

- 대상 세션에서는 `ERR-03027: This statement has been canceled.` 오류가 반환됩니다.
- 같은 사용자 또는 `SYS` 계정만 취소할 수 있습니다.
- 자신의 세션을 취소하려 하면 `ERR-03025` 오류가 발생합니다.

**오류 코드**

| 상황 | 오류 |
|---|---|
| 세션 ID가 존재하지 않음 | `ERR_MM_SESSION_ID_NOT_FOUND` |
| 다른 사용자 세션 취소 시도 | `ERR-03026: You should log in with the same user name in the target session.` |
| 자신의 세션 취소 시도 | `ERR-03025: Not enough privileges to manipulate the session.` |

**예시**

```sql
-- 세션 A: 실행 중인 세션 ID 확인
SELECT id, user_id, query FROM v$session;

-- 세션 B (같은 사용자 또는 SYS): 세션 6의 현재 쿼리만 취소
ALTER SYSTEM CANCEL SESSION 6;
```

## KILL vs CANCEL 비교

| 항목 | KILL SESSION | CANCEL SESSION |
|---|---|---|
| 세션 연결 | 종료 | 유지 |
| 실행 중인 쿼리 | 중단 | 중단 |
| 트랜잭션 롤백 | 예 | 예 |
| 실행 권한 | SYS만 가능 | 동일 사용자 또는 SYS |
| 사용 상황 | 응답 없는 세션을 완전히 제거 | 장시간 실행 쿼리만 취소하고 연결 유지 |

## 세션 ID 확인

```sql
-- 전체 세션 목록 조회
SELECT id, user_id, client_type, login_time FROM v$session;

-- 특정 쿼리를 실행 중인 세션 찾기
SELECT id, user_id, query FROM v$session WHERE query IS NOT NULL;
```
