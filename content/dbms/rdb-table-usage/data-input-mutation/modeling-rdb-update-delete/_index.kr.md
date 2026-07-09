---
type: docs
title: '8.4.1 UPDATE·DELETE 설계'
weight: 60
---

RDB 테이블은 UPDATE와 DELETE를 모두 지원합니다. WHERE 절 없이도 전체 행을 갱신하거나 삭제할 수 있습니다.

## UPDATE

```sql
-- WHERE 조건 기반 UPDATE
UPDATE orders SET status = 'SHIPPED' WHERE order_id = 1001;

-- 복합 조건 UPDATE
UPDATE inventory SET qty = qty - 5, updated_at = NOW
WHERE item_id = 42 AND warehouse = 'WH-01';

-- 자기 참조 UPDATE (컬럼 계산)
UPDATE score_board SET score = score + 10 WHERE user_id = 'U001';

-- WHERE 없이 전체 행 UPDATE
UPDATE product_catalog SET discount = 0;
```

## DELETE

```sql
-- 조건 기반 DELETE
DELETE FROM orders WHERE order_id = 1001;

-- 범위 DELETE
DELETE FROM orders WHERE status = 'CANCELLED' AND tx_time < '2023-01-01';

-- 전체 삭제 (WHERE 없음)
DELETE FROM temp_staging;
```

## 트랜잭션 내 UPDATE + DELETE 조합

```sql
BEGIN;
-- 재고 차감
UPDATE inventory SET qty = qty - 3 WHERE item_id = 42 AND warehouse = 'WH-01';
-- 출고 이력 기록
INSERT INTO dispatch_log VALUES (NOW, 42, 'WH-01', 3, 'ORDER-9999');
-- 이미 완료된 이전 예약 삭제
DELETE FROM reservations WHERE item_id = 42 AND order_id = 'ORDER-9999';
COMMIT;
```

## 상태 관리 패턴

```sql
-- 주문 상태 전환
UPDATE orders SET status = 'PROCESSING', updated_at = NOW
WHERE order_id = 1001 AND status = 'PENDING';

-- 여러 주문 일괄 상태 변경
UPDATE orders SET status = 'EXPIRED'
WHERE status = 'PENDING' AND created_at < NOW - 86400000000000;
```

## 주의사항

- WHERE 없는 UPDATE는 테이블 전체 행을 수정합니다. 의도치 않은 전체 갱신에 주의합니다.
- 장시간 열린 트랜잭션은 잠금 충돌을 유발할 수 있습니다.
- UPDATE/DELETE 시 WHERE 절 컬럼에 인덱스가 있으면 성능이 크게 향상됩니다.
