---
type: docs
title: '13.4.4.2 세션과 실행 쿼리 확인'
weight: 20
---

현재 접속된 세션 목록과 실행 중인 쿼리를 확인하고, 문제가 있는 세션을 강제 종료하는 방법을 설명합니다.

## 현재 세션 목록 확인

`V$SESSION` 가상 테이블에서 현재 서버에 접속된 모든 세션을 조회합니다.

```sql
-- 현재 접속 세션 전체 목록
SELECT id, user_name, user_ip, client_type, login_time
  FROM v$session
 WHERE closed = 0
 ORDER BY login_time;
```

```sql
-- 세션 수 요약
SELECT count(*) AS active_session_count
  FROM v$session
 WHERE closed = 0;
```

### V$SESSION 주요 컬럼

| 컬럼 이름 | 설명 |
|---------|------|
| ID | 세션 식별자 |
| USER_NAME | 접속 사용자 이름 |
| USER_IP | 클라이언트 IP 주소 |
| CLIENT_TYPE | 클라이언트 타입 (JDBC, ODBC, CLI 등) |
| LOGIN_TIME | 접속 시각 |
| CLOSED | 0 = 활성, 1 = 종료됨 |
| IDLE_TIMEOUT | 유휴 세션 자동 종료 시간 (초) |
| QUERY_TIMEOUT | 쿼리 타임아웃 시간 |

## 실행 중인 쿼리 확인

`V$STMT` 가상 테이블에서 현재 서버에서 처리 중인 SQL 문을 조회합니다.

```sql
-- 실행/Fetch/Append 진행 중인 쿼리 조회
SELECT id, sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%'
    OR state LIKE 'Append in progress%';
```

```sql
-- 세션 정보와 함께 실행 중인 쿼리 확인
SELECT s.id        AS session_id,
       s.user_name,
       s.user_ip,
       st.id       AS stmt_id,
       st.state,
       st.query
  FROM v$session s
  JOIN v$stmt    st ON s.id = st.sess_id
 WHERE st.state LIKE 'Execute in progress%'
    OR st.state LIKE 'Fetch in progress%'
    OR st.state LIKE 'Append in progress%'
 ORDER BY s.login_time;
```

> **참고**: `V$STMT`에는 `elapsed_time` 컬럼이 없습니다. 실행 시간 통계가 필요한 경우 `V$SESTIME`의 `ACCUM_MSEC` 값을 참조하십시오.

## 세션별 시간 통계

`V$SESTIME`에서 세션별로 누적 실행 시간 통계를 확인할 수 있습니다.

```sql
-- 세션별 누적 실행 시간 확인
SELECT st.sid, s.user_name, s.user_ip,
       st.id      AS time_unit_id,
       st.accum_msec,
       st.max_msec
  FROM v$sestime st
  JOIN v$session s ON st.sid = s.id
 WHERE s.closed = 0
 ORDER BY st.accum_msec DESC;
```

## 특정 세션 강제 종료

문제가 있는 세션(장시간 블로킹, 잘못된 쿼리 등)을 강제로 종료합니다.

```sql
-- 특정 세션 강제 종료 (세션 ID = 7)
ALTER SYSTEM KILL SESSION 7;
```

강제 종료 전에 반드시 세션 ID를 `V$SESSION`에서 확인하고, 해당 세션이 처리 중인 트랜잭션이 없는지 확인하십시오.

```sql
-- 종료 대상 세션 확인
SELECT id, user_name, user_ip, login_time
  FROM v$session
 WHERE id = 7;

-- 해당 세션의 실행 중인 쿼리 확인
SELECT id, state, query
  FROM v$stmt
 WHERE sess_id = 7;

-- 확인 후 종료
ALTER SYSTEM KILL SESSION 7;
```

## 세션 메모리 사용량 확인

```sql
-- 세션별 메모리 사용량
SELECT sm.sid,
       s.user_name,
       sm.id     AS mem_manager_id,
       sm.usage  AS memory_bytes
  FROM v$sesmem sm
  JOIN v$session s ON sm.sid = s.id
 WHERE s.closed = 0
 ORDER BY sm.usage DESC;
```

## 최대 세션 수 설정 확인

```sql
-- 현재 설정된 최대 세션 수
SELECT name, value
  FROM v$property
 WHERE name = 'MAX_SESSION_COUNT';

-- 현재 세션 수와 최대 세션 수 비교
SELECT (SELECT value FROM v$property WHERE name = 'MAX_SESSION_COUNT') AS max_sessions,
       (SELECT count(*) FROM v$session WHERE closed = 0)               AS current_sessions;
```

현재 세션 수가 최대 세션 수의 80%를 초과하면 새 연결 실패 위험이 있습니다. `MAX_SESSION_COUNT` 값을 조정하거나 오래된 세션을 정리하십시오.

## 세션 설정 변경

특정 세션의 타임아웃 설정을 변경합니다.

```sql
-- 현재 세션의 쿼리 타임아웃 설정 (단위: 초)
ALTER SESSION SET QUERY_TIMEOUT = 300;

-- 현재 세션의 유휴 타임아웃 설정 (단위: 초, 0 = 무제한)
ALTER SESSION SET IDLE_TIMEOUT = 1800;
```
