---
type: docs
title: 'TAG/KV DELETE 허용 조건과 BEFORE 조건'
weight: 30
---

TAG, KV, LOG 테이블은 `BEFORE` 조건으로 특정 시점 이전 데이터를 일괄 삭제할 수 있습니다. LOG 테이블은 `OLDEST`, `EXCEPT`, `BEFORE` 등 로그 보존형 DELETE를 사용하고, TAG/KV 테이블은 `BEFORE` 외에도 태그 이름과 축 조건을 사용한 `WHERE` 삭제를 지원합니다.

## BEFORE 조건의 역할

`BEFORE` 조건은 오래된 데이터를 빠르게 정리할 때 사용하는 보존형 삭제 조건입니다. 지정한 시각은 현재 시각보다 과거여야 하며, 미래 시각을 지정하면 오류가 발생합니다.

## TAG 테이블 DELETE

```sql
-- 특정 날짜 이전 데이터 삭제
DELETE FROM tag BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- 특정 시각 이전 데이터 삭제
DELETE FROM tag BEFORE '2024-01-01 00:00:00 000:000:000';

-- NOW 기준 상대 시간
DELETE FROM tag BEFORE NOW - 7776000000000000;  -- 90일 이전 삭제
```

## LOG 테이블 DELETE

```sql
-- 30일 이전 데이터 삭제
DELETE FROM sensor_log BEFORE NOW - 2592000000000000;

-- 특정 날짜 이전 삭제
DELETE FROM event_log BEFORE TO_DATE('2023-12-31', 'YYYY-MM-DD');
```

## WHERE 조건 삭제와 구분

TAG/KV 테이블에서는 태그 이름 또는 축 조건으로 `WHERE` 삭제도 사용할 수 있습니다. 반면 LOG 테이블에서는 임의의 일반 `WHERE` 조건 삭제가 아니라 로그 전용 삭제 구문을 사용합니다.

```sql
-- TAG: tag name 기준 삭제 가능
DELETE FROM tag WHERE name = 'TEMP-01';

-- LOG: 일반 WHERE 조건 삭제는 사용하지 않음
DELETE FROM sensor_log WHERE value > 100.0;
-- → 오류 발생
```

## Retention Policy와의 관계

BEFORE 조건을 이용한 수동 DELETE 대신, [Retention Policy](/dbms/schema-data-lifecycle/policy-data-retention/)를 사용하면 지정된 주기마다 자동으로 오래된 데이터를 삭제할 수 있습니다. 운영 편의성 측면에서는 Retention Policy 설정이 권장됩니다.

```sql
-- 자동 삭제 정책 적용 (수동 DELETE 불필요)
ALTER TABLE sensor_log ADD RETENTION policy_30d;
```

## 주의 사항

- BEFORE 조건으로 삭제된 데이터는 복구할 수 없습니다.
- 대량 데이터 삭제 시 성능 영향이 있을 수 있으므로, 업무 시간 외 실행을 권장합니다.
- TAG 테이블의 경우 BEFORE 조건은 BASETIME 컬럼 기준으로 적용됩니다.
