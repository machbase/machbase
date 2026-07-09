---
type: docs
title: 'JOIN 설계'
weight: 90
---

RDB 테이블은 다른 테이블 타입(TAG, LOG, LOOKUP 등)과 JOIN할 수 있습니다.

## RDB ↔ LOOKUP JOIN

기준 정보(LOOKUP)와 이력 데이터(RDB)를 조인합니다.

```sql
-- 제품 코드(LOOKUP) + 주문 이력(RDB)
SELECT o.order_id, p.name AS product_name, o.qty, o.amount
FROM order_history o
JOIN product_lookup p ON o.item_id = p.product_id
WHERE o.customer = 'CUST-001'
  AND o.order_time >= '2024-01-01';
```

## RDB ↔ TAG JOIN

센서 계측값(TAG)과 이벤트 이력(RDB)을 조인합니다.

```sql
-- 알람 이력(RDB) + 해당 시점 센서값(TAG)
SELECT a.alarm_id, a.alarm_time, s.value AS sensor_value
FROM alarm_history a
JOIN sensor_data s ON a.sensor = s.name
WHERE s.time BETWEEN a.alarm_time - 5000000000 AND a.alarm_time + 5000000000
  AND a.level >= 3;
```

## RDB ↔ RDB JOIN

두 RDB 테이블을 조인합니다.

```sql
SELECT o.order_id, o.amount, t.status AS tx_status
FROM order_history o
JOIN tx_history t ON o.order_id = t.order_id
WHERE o.customer = 'CUST-001';
```

## JOIN 성능 최적화

- JOIN 조건 컬럼에 인덱스를 생성합니다.
- 큰 테이블을 드라이빙 테이블로 사용하지 않습니다.
- 필요한 컬럼만 SELECT합니다.

```sql
-- 인덱스 생성으로 JOIN 성능 향상
CREATE INDEX idx_order_item ON order_history(item_id);
CREATE INDEX idx_tx_order   ON tx_history(order_id);
```
