---
type: docs
title: 'Retention Policy 테이블 적용'
weight: 20
---

생성된 Retention Policy를 TAG, KV, LOG 테이블에 적용합니다. 적용 후에는 지정된 INTERVAL마다 DURATION을 초과한 데이터가 자동으로 삭제됩니다.

## 구문

```sql
ALTER TABLE table_name ADD RETENTION policy_name;
```

## 예시

```sql
-- TAG 테이블에 정책 적용
ALTER TABLE sensor_tag ADD RETENTION policy_30d;

-- LOG 테이블에 정책 적용
ALTER TABLE event_log ADD RETENTION policy_7d;

-- KV 테이블에 정책 적용
ALTER TABLE raw_kv ADD RETENTION policy_30d;

-- 이미 생성된 정책을 다른 테이블에도 적용 (정책 공유)
ALTER TABLE raw_data ADD RETENTION policy_30d;
```

## 적용 상태 확인

```sql
SELECT * FROM V$RETENTION_JOB;
```

```
USER_NAME   TABLE_NAME    POLICY_NAME    STATE     LAST_DELETED_TIME
--------------------------------------------------------------------
SYS         SENSOR_TAG    POLICY_30D     WAITING   NULL
SYS         EVENT_LOG     POLICY_7D      WAITING   NULL
```

- **STATE**: `WAITING`(대기 중), `RUNNING`(실행 중), `STOPPED`(중지)
- **LAST_DELETED_TIME**: 마지막 삭제 작업에 사용한 `DELETE ... BEFORE` 기준 시각 (NULL = 아직 기준 시각이 기록되지 않음)

## 주의 사항

- 한 테이블에는 하나의 정책만 적용할 수 있습니다.
- 이미 정책이 적용된 테이블에 다른 정책을 적용하려면 먼저 기존 정책을 해제해야 합니다.
- 정책 적용 즉시 삭제가 실행되는 것은 아닙니다. 첫 번째 INTERVAL이 경과한 후부터 실행됩니다.
- TAG 테이블의 경우 BASETIME 컬럼 기준으로 DURATION이 적용됩니다.
- LOG 테이블의 경우 `_ARRIVAL_TIME` 컬럼 기준으로 DURATION이 적용됩니다.
