---
type: docs
title: 'UPDATE·DELETE 모델링'
weight: 60
---

RDB 테이블은 **UPDATE를 지원하지 않습니다**. 행을 수정해야 하는 경우 DELETE 후 INSERT하는 패턴을 사용합니다.

## DELETE 지원

RDB 테이블은 DELETE를 지원합니다.

```sql
-- 조건 기반 DELETE
DELETE FROM order_history WHERE order_id = 1001;

-- 범위 DELETE
DELETE FROM order_history
WHERE order_time < '2023-01-01';

-- 전체 삭제 (TRUNCATE 대체)
DELETE FROM order_history;
```

## UPDATE 대체 패턴: DELETE + INSERT

```sql
-- 특정 주문 상태 변경 (UPDATE 미지원이므로 DELETE + INSERT)
BEGIN;
-- 기존 레코드 삭제
DELETE FROM order_history WHERE order_id = 1001;
-- 새 값으로 재삽입
INSERT INTO order_history VALUES (1001, 'CUST-001', 5, 49.99, NOW, 'COMPLETED');
COMMIT;
```

## 상태 변경 이력 패턴

상태 변경 이력을 남겨야 하는 경우, 별도 이력 테이블을 사용합니다.

```sql
-- 현재 상태 (최신 레코드만 유지)
CREATE RDB TABLE order_current (
    order_id    LONG,
    customer    VARCHAR(64),
    item_id     INTEGER,
    amount      DOUBLE,
    status      VARCHAR(16),
    updated_at  DATETIME
);

-- 상태 변경 이력 (LOG 테이블)
CREATE TABLE order_status_log (
    order_id    LONG,
    old_status  VARCHAR(16),
    new_status  VARCHAR(16),
    changed_at  DATETIME
);

-- 상태 변경 처리
BEGIN;
DELETE FROM order_current WHERE order_id = 1001;
INSERT INTO order_current VALUES (1001, 'CUST-001', 5, 49.99, 'SHIPPED', NOW);
INSERT INTO order_status_log VALUES (1001, 'PENDING', 'SHIPPED', NOW);
COMMIT;
```

## 주의사항

- 빈번한 DELETE + INSERT는 성능 저하를 유발할 수 있습니다.
- 행을 자주 수정해야 하는 데이터는 LOOKUP 테이블(UPDATE 지원)을 고려합니다.
- DELETE 작업 후 스토리지 공간이 즉시 반환되지 않을 수 있습니다.
