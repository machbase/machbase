---
type: docs
title: 'UPDATE 정책'
weight: 10
---

테이블 타입별 UPDATE 지원 범위와 구문을 정리합니다.

## 테이블 타입별 UPDATE 지원

| 테이블 타입 | UPDATE 지원 | 조건 |
|------------|------------|------|
| TAG | 메타데이터만 O | 실제 시계열 데이터 UPDATE는 미지원 |
| LOG | X | 미지원 |
| RDB | O | WHERE 유무 모두 가능 |
| VOLATILE | O | Primary key equality 조건. ON DUPLICATE KEY UPDATE도 지원 |
| LOOKUP | O | Primary key equality 조건과 일반 predicate 조건 지원 |

## RDB 테이블 UPDATE

RDB 테이블은 일반 관계형 DB와 동일한 UPDATE 구문을 지원합니다.

```sql
-- WHERE 조건 UPDATE
UPDATE orders SET status = 'SHIPPED', updated_at = NOW
WHERE order_id = 1001;

-- 자기 참조 UPDATE
UPDATE inventory SET qty = qty - 5 WHERE item_id = 42;

-- 전체 행 UPDATE (WHERE 없음)
UPDATE product_catalog SET discount = 0;
```

## VOLATILE 테이블 UPDATE

VOLATILE 테이블은 일반 UPDATE와 ON DUPLICATE KEY UPDATE(UPSERT)를 모두 지원합니다.

```sql
-- 일반 UPDATE
UPDATE device_status SET status = 'ALARM', value = 95.3
WHERE device_id = 'DEV-01';  -- device_id = PRIMARY KEY

-- UPSERT: PK 중복 시 자동 UPDATE
INSERT INTO device_status VALUES ('DEV-01', 'ALARM', 95.3, NOW)
ON DUPLICATE KEY UPDATE SET status = 'ALARM', value = 95.3, updated_at = NOW;
```

## LOOKUP 테이블 UPDATE

LOOKUP 테이블은 PRIMARY KEY equality 조건과 일반 predicate 조건의 UPDATE를 모두 지원합니다.
조건에 맞는 모든 row가 갱신됩니다.

```sql
-- PK 기준 직접 UPDATE
UPDATE alarm_threshold SET high_limit = 90.0, updated_at = NOW
WHERE sensor_id = 'TEMP-01';

-- 일반 조건식 UPDATE
UPDATE alarm_threshold
SET high_limit = high_limit + 5.0
WHERE device_type = 'MOTOR'
  AND active = 1;
```

> 일반 조건식 UPDATE는 여러 row에 적용될 수 있으므로 실행 전에 같은 조건으로 대상 범위를 확인합니다.

## TAG/LOG 테이블 UPDATE

TAG 데이터(실제 시계열 값)와 TAG 메타데이터 UPDATE는 구분해야 합니다.

- **TAG 메타데이터 UPDATE**: `UPDATE ... METADATA SET ...` 구문으로 가능 (현재 지원)
- **TAG 실제 데이터(value) UPDATE**: 현재 미지원
- **LOG 테이블 UPDATE**: 미지원

상세 내용은 하위 페이지를 참고하세요.
