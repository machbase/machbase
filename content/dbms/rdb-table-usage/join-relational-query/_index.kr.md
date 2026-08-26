---
title: '8.11 JOIN과 관계형 조회 설계'
weight: 110
toc: true
---

TRANSACTION 테이블과 다른 테이블 타입 간의 JOIN 패턴과 성능 최적화 방법을 다룹니다.


<a id="join-design-rdb"></a>

## JOIN 설계

TRANSACTION 테이블은 TAG, LOG, LOOKUP 등 다른 테이블 타입과 JOIN할 수 있습니다.

### TRANSACTION - LOOKUP JOIN

기준 정보(LOOKUP)와 이력 데이터(TRANSACTION)를 조인하는 패턴입니다.

```sql
-- 제품 코드(LOOKUP) + 주문 이력(TRANSACTION)
SELECT o.order_id, p.name AS product_name, o.qty, o.amount
FROM order_history o
JOIN product_lookup p ON o.item_id = p.product_id
WHERE o.customer = 'CUST-001'
  AND o.order_time >= '2024-01-01';
```

### TRANSACTION - TAG JOIN

센서 계측값(TAG)과 이벤트 이력(TRANSACTION)을 조인하는 패턴입니다.

```sql
-- 알람 이력(TRANSACTION) + 해당 시점 센서값(TAG)
SELECT a.alarm_id, a.alarm_time, s.value AS sensor_value
FROM alarm_history a
JOIN sensor_data s ON a.sensor = s.name
WHERE s.time BETWEEN a.alarm_time - 5000000000 AND a.alarm_time + 5000000000
  AND a.level >= 3;
```

### TRANSACTION - TRANSACTION JOIN

두 TRANSACTION 테이블 간 조인입니다.

```sql
SELECT o.order_id, o.amount, t.status AS tx_status
FROM order_history o
JOIN tx_history t ON o.order_id = t.order_id
WHERE o.customer = 'CUST-001';
```

### JOIN 성능 최적화

- JOIN 조건 컬럼에 인덱스를 생성합니다.
- 큰 테이블을 드라이빙 테이블로 사용하지 않습니다.
- 필요한 컬럼만 SELECT합니다.

```sql
-- 인덱스 생성으로 JOIN 성능 향상
CREATE INDEX idx_order_item ON order_history(item_id);
CREATE INDEX idx_tx_order   ON tx_history(order_id);
```
