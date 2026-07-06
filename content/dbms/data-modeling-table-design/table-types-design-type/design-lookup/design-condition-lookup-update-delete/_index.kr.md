---
type: docs
title: 'UPDATE·DELETE 조건 설계'
weight: 80
---

LOOKUP 테이블은 PRIMARY KEY 기준 UPDATE와 DELETE를 지원합니다.

## UPDATE

```sql
-- PK 기준 업데이트
UPDATE country_code SET name = 'Korea' WHERE code = 'KR';

-- 여러 컬럼 동시 업데이트
UPDATE equipment_master
SET location = 'Line-3', status = 'ACTIVE', updated_at = NOW
WHERE equip_id = 42;

-- 복합 PK 기준
UPDATE product_region_price SET price = 99.0
WHERE product_id = 'PROD-01' AND region = 'KR';
```

## DELETE

```sql
-- PK 기준 삭제
DELETE FROM country_code WHERE code = 'XX';

-- 조건 기반 삭제
DELETE FROM equipment_master WHERE status = 'RETIRED';

-- 전체 삭제
DELETE FROM session_cache;
```

## UPDATE 조건 설계 지침

1. **PK 조건 필수**: UPDATE/DELETE WHERE 절에 반드시 PK 또는 인덱스 컬럼을 포함합니다.
2. **범위 업데이트 주의**: PK가 없는 조건으로 UPDATE하면 풀스캔이 발생합니다.
3. **트랜잭션 활용**: 연관된 UPDATE/DELETE는 하나의 트랜잭션으로 묶습니다.

```sql
-- 연관 업데이트 트랜잭션
BEGIN;
UPDATE equipment_master SET status = 'RETIRED' WHERE equip_id = 42;
INSERT INTO equipment_history VALUES (42, 'RETIRED', NOW, 'maintenance');
COMMIT;
```

## UPSERT 패턴

존재하면 UPDATE, 없으면 INSERT하는 패턴이 필요한 경우:

```sql
-- INSERT 시도 후 PK 충돌이면 UPDATE
-- (Machbase는 표준 UPSERT 문법 미지원 — DELETE + INSERT 패턴 사용)
BEGIN;
DELETE FROM threshold_config WHERE sensor_name = 'TEMP-01';
INSERT INTO threshold_config VALUES ('TEMP-01', 0.0, 80.0, 2);
COMMIT;
```
