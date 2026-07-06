---
type: docs
title: 'Retention Policy 삭제'
weight: 40
---

더 이상 사용하지 않는 Retention Policy 객체를 삭제합니다.

## 구문

```sql
DROP RETENTION policy_name;
```

## 예시

```sql
DROP RETENTION policy_1d_1h;
DROP RETENTION policy_30d;
```

## 적용 중인 정책 삭제 시 오류

Retention Policy가 하나 이상의 테이블에 적용 중이면 삭제할 수 없습니다.

```sql
-- 정책이 적용 중인 상태에서 삭제 시도
DROP RETENTION policy_1d_1h;
-- [ERR-02702: Policy (POLICY_1D_1H) is in use.]
```

## 올바른 삭제 순서

1. 정책을 사용 중인 모든 테이블에서 먼저 해제
2. 정책 삭제

```sql
-- 1단계: 적용된 테이블 확인
SELECT * FROM V$RETENTION_JOB WHERE POLICY_NAME = 'POLICY_1D_1H';

-- 2단계: 각 테이블에서 정책 해제
ALTER TABLE sensor_tag DROP RETENTION;
ALTER TABLE event_log DROP RETENTION;

-- 3단계: 정책 삭제
DROP RETENTION policy_1d_1h;
-- Dropped successfully.
```

## 삭제 후 확인

```sql
SELECT * FROM M$RETENTION;
-- 해당 정책 이름이 사라져야 합니다
```

## 주의 사항

- 정책 삭제는 테이블 데이터에는 영향을 주지 않습니다. 이후에는 자동 삭제만 중단됩니다.
- 같은 이름의 정책을 재생성하려면 먼저 기존 정책을 삭제해야 합니다.
