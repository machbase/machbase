---
type: docs
title: '자기 참조·INSERT SELECT'
weight: 80
---

RDB 테이블에서 `INSERT INTO ... SELECT ...` 문을 사용하여 다른 테이블의 데이터를 복사하거나 변환하여 삽입할 수 있습니다.

## INSERT SELECT 기본

```sql
-- 다른 RDB 테이블에서 데이터 복사
INSERT INTO order_archive
SELECT order_id, customer, item_id, amount, order_time, status
FROM order_history
WHERE order_time < '2023-01-01';

-- 조건 가공 후 삽입
INSERT INTO active_orders
SELECT order_id, customer, item_id, amount, order_time, status
FROM order_history
WHERE status = 'PENDING';
```

## LOG 테이블에서 RDB 테이블로 데이터 이관

```sql
-- LOG 테이블 데이터를 RDB 테이블로 집계하여 삽입
INSERT INTO daily_summary (date, sensor, avg_val, max_val, count, region)
SELECT
    DATE_TRUNC('day', event_time),
    sensor_name,
    AVG(value),
    MAX(value),
    COUNT(*),
    region
FROM raw_events
GROUP BY DATE_TRUNC('day', event_time), sensor_name, region;
```

## 자기 참조: 동일 테이블 내 복사

```sql
-- 특정 고객 데이터를 다른 고객으로 복제 (예: 테스트 데이터 생성)
INSERT INTO order_history (order_id, customer, item_id, amount, order_time, status)
SELECT order_id + 10000, 'TEST-001', item_id, amount, order_time, status
FROM order_history
WHERE customer = 'CUST-001'
  AND order_time >= '2024-01-01';
```

## 주의사항

- `INSERT SELECT`는 하나의 트랜잭션으로 처리됩니다. 대량 데이터는 배치로 분할하여 실행합니다.
- SELECT 결과 컬럼 수와 타입이 INSERT 대상 테이블의 컬럼과 일치해야 합니다.
