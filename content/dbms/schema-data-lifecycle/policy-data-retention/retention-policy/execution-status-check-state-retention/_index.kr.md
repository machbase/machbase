---
type: docs
title: 'Retention 실행 상태 확인'
weight: 60
---

Retention Policy가 적용된 테이블의 실행 상태를 `V$RETENTION_JOB` 뷰로 모니터링합니다.

## V$RETENTION_JOB 조회

```sql
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
FROM V$RETENTION_JOB;
```

```
USER_NAME   TABLE_NAME    POLICY_NAME    STATE     LAST_DELETED_TIME
--------------------------------------------------------------------
SYS         SENSOR_TAG    POLICY_30D     WAITING   2024-01-15 03:00:00
SYS         EVENT_LOG     POLICY_7D      RUNNING   2024-01-15 02:00:00
SYS         RAW_DATA      POLICY_30D     DONE      2024-01-15 01:00:00
```

## STATE 값 의미

| STATE | 설명 |
|-------|------|
| `WAITING` | 다음 INTERVAL을 기다리는 상태 |
| `RUNNING` | 현재 삭제 작업 실행 중 |
| `DONE` | 마지막 실행 완료 |

## LAST_DELETED_TIME

마지막으로 삭제 작업이 완료된 시각입니다. `NULL`이면 아직 한 번도 실행되지 않은 것입니다.

## 적용 정책 전체 확인

```sql
-- 생성된 정책 전체 목록 (초 단위 값)
SELECT POLICY_NAME,
       DURATION / 86400 AS duration_days,
       INTERVAL / 3600  AS interval_hours
FROM M$RETENTION;
```

```
POLICY_NAME    DURATION_DAYS   INTERVAL_HOURS
---------------------------------------------
POLICY_30D     30              24
POLICY_7D      7               1
POLICY_1H_10M  0               0
```

## 모니터링 쿼리 패턴

```sql
-- 오랫동안 실행되지 않은 정책 확인 (예: 24시간 이상)
SELECT TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
FROM V$RETENTION_JOB
WHERE LAST_DELETED_TIME < DATEADD('h', -24, NOW)
   OR LAST_DELETED_TIME IS NULL;

-- 현재 실행 중인 정책
SELECT TABLE_NAME, POLICY_NAME
FROM V$RETENTION_JOB
WHERE STATE = 'RUNNING';
```

## 삭제 실행 여부 확인

정책 적용 후 실제로 삭제가 일어나고 있는지 확인하는 방법:

```sql
-- 1. 적용 전 데이터 수 확인
SELECT COUNT(*) FROM sensor_tag;

-- 2. INTERVAL 경과 후 재확인
SELECT COUNT(*) FROM sensor_tag;
-- DURATION을 초과한 데이터가 감소했으면 정상 동작 중
```
