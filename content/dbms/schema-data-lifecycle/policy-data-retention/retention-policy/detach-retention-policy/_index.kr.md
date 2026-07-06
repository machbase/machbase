---
type: docs
title: 'Retention Policy 적용 해제'
weight: 30
---

테이블에 적용된 Retention Policy를 해제합니다. 해제 후에는 데이터가 자동으로 삭제되지 않고 영구 보관됩니다.

## 구문

```sql
ALTER TABLE table_name DROP RETENTION;
```

## 예시

```sql
-- TAG 테이블에서 정책 해제
ALTER TABLE sensor_tag DROP RETENTION;

-- LOG 테이블에서 정책 해제
ALTER TABLE event_log DROP RETENTION;
```

## 해제 후 상태 확인

```sql
-- V$RETENTION_JOB에서 해당 테이블이 사라져야 합니다
SELECT * FROM V$RETENTION_JOB;
```

정책 해제 후에는 `V$RETENTION_JOB`에서 해당 테이블 항목이 제거됩니다.

## 일시 중지가 필요한 경우

데이터 마이그레이션이나 점검 중에 자동 삭제를 일시적으로 중단해야 할 때 사용합니다. 작업 완료 후 다시 정책을 적용하면 됩니다.

```sql
-- 정책 임시 해제
ALTER TABLE sensor_tag DROP RETENTION;

-- ... 점검 작업 수행 ...

-- 정책 재적용
ALTER TABLE sensor_tag ADD RETENTION policy_30d;
```

## 주의 사항

- 정책 해제는 이미 삭제된 데이터를 복구하지 않습니다.
- 정책 해제 후 데이터는 `DROP TABLE` 또는 수동 `DELETE ... BEFORE`로만 삭제됩니다.
- 정책 자체(policy 객체)는 `DROP RETENTION`으로 별도 삭제해야 합니다. `DROP RETENTION`과 `ALTER TABLE DROP RETENTION`은 다른 명령입니다.
