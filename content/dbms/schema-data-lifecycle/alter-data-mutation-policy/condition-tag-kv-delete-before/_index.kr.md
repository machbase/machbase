---
type: docs
title: 'TAG/KV DELETE 허용 조건과 BEFORE 조건'
weight: 30
---

TAG와 LOG(KV 포함) 테이블의 DELETE는 **BEFORE 조건이 반드시 필요**합니다. 특정 시점 이전의 데이터를 일괄 삭제하는 방식으로만 동작하며, 임의의 WHERE 조건으로 개별 행을 삭제할 수 없습니다.

## BEFORE 조건 필수 이유

TAG와 LOG 테이블은 시계열 데이터를 파티션 단위로 관리합니다. 파티션 내부에서 특정 행만을 선택적으로 삭제하는 것은 구조적으로 지원되지 않으며, BEFORE 조건으로 파티션 단위 삭제를 수행합니다.

## TAG 테이블 DELETE

```sql
-- 특정 날짜 이전 데이터 삭제
DELETE FROM tag BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- 특정 시각 이전 데이터 삭제
DELETE FROM tag BEFORE '2024-01-01 00:00:00 000:000:000';

-- NOW 기준 상대 시간
DELETE FROM tag BEFORE DATEADD('d', -90, NOW);  -- 90일 이전 삭제
```

## LOG 테이블 DELETE

```sql
-- 30일 이전 데이터 삭제
DELETE FROM sensor_log BEFORE DATEADD('d', -30, NOW);

-- 특정 날짜 이전 삭제
DELETE FROM event_log BEFORE TO_DATE('2023-12-31', 'YYYY-MM-DD');
```

## BEFORE 없이 DELETE 시도 시

BEFORE 조건 없이 DELETE를 실행하면 오류가 발생합니다.

```sql
-- 오류: BEFORE 조건 없음
DELETE FROM tag WHERE name = 'TEMP-01';
-- → 오류 발생

-- 오류: 일반 WHERE 조건
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
