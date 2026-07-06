---
type: docs
title: 'UPDATE 정책'
weight: 10
---

테이블 타입별 UPDATE 지원 범위와 구문을 정리합니다.

## 테이블 타입별 UPDATE 지원

| 테이블 타입 | UPDATE 지원 | 조건 |
|------------|------------|------|
| TAG | X | 계획 중 (dbms-nfx#3733) |
| LOG | X | 미지원 |
| RDB | O | WHERE 유무 모두 가능 |
| VOLATILE | O | WHERE 조건 자유. ON DUPLICATE KEY UPDATE도 지원 |
| LOOKUP | O | PK 기준 권장. 일반 조건식은 계획 중 (#3696) |

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
WHERE device_id = 'DEV-01';

-- UPSERT: PK 중복 시 자동 UPDATE
INSERT INTO device_status VALUES ('DEV-01', 'ALARM', 95.3, NOW)
ON DUPLICATE KEY UPDATE status = 'ALARM', value = 95.3, updated_at = NOW;
```

## LOOKUP 테이블 UPDATE

현재 버전에서는 PRIMARY KEY 기준 UPDATE를 권장합니다.

```sql
-- PK 기준 직접 UPDATE
UPDATE alarm_threshold SET high_limit = 90.0, updated_at = NOW
WHERE sensor_id = 'TEMP-01';
```

> 일반 조건식(non-PK 컬럼 기준) UPDATE는 dbms-nfx#3696에서 계획 중입니다.

## TAG/LOG 테이블 UPDATE

TAG 데이터(실제 시계열 값)와 TAG 메타데이터 UPDATE는 구분해야 합니다.

- **TAG 메타데이터 UPDATE**: `UPDATE ... METADATA SET ...` 구문으로 가능 (현재 지원)
- **TAG 실제 데이터(value) UPDATE**: 계획 중 (dbms-nfx#3733)
- **LOG 테이블 UPDATE**: 미지원

상세 내용은 하위 페이지를 참고하세요.
