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

-- PK 기준 삭제
DELETE FROM equipment_master WHERE equip_id = 42;

-- 전체 삭제
DELETE FROM session_cache;
```

## UPDATE 조건 설계 지침

1. **PK 조건 필수**: UPDATE/DELETE WHERE 절에는 Primary key equality 조건을 사용합니다.
2. **Non-PK 조건 불가**: 일반 컬럼 조건이나 범위 조건은 현재 빌드에서 오류가 발생합니다.
3. **트랜잭션 제한**: LOOKUP 테이블 DML 예제는 개별 문장 단위로 실행합니다. 현재 빌드에서는
   `BEGIN`/`COMMIT`으로 LOOKUP DML을 묶어 실행할 수 없습니다.

```sql
-- 연관 상태 변경을 순차 실행
UPDATE equipment_master SET status = 'RETIRED' WHERE equip_id = 42;
INSERT INTO equipment_history VALUES (42, 'RETIRED', NOW, 'maintenance');
```

## UPSERT 패턴

존재하면 UPDATE, 없으면 INSERT하는 패턴이 필요한 경우:

```sql
-- INSERT 시도 후 PK 충돌이면 UPDATE
-- (LOOKUP은 ON DUPLICATE KEY UPDATE 미지원 — DELETE + INSERT 패턴 사용)
DELETE FROM threshold_config WHERE sensor_name = 'TEMP-01';
INSERT INTO threshold_config VALUES ('TEMP-01', 0.0, 80.0, 2);
```
