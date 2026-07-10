---
title: '8.4 데이터 입력과 변경'
weight: 40
toc: true
---

RDB 테이블의 INSERT, UPDATE, DELETE 사용법과 INSERT SELECT 패턴을 다룬다.

RDB 테이블에서 "없으면 INSERT, 있으면 UPDATE"가 필요한 경우에는 [INSERT ON DUPLICATE KEY UPDATE](/dbms/rdb-table-usage/insert-on-duplicate-key-update/)를 사용한다. 자동 번호 PRIMARY KEY가 필요한 INSERT 패턴은 [AUTO_INCREMENT](/dbms/rdb-table-usage/auto-increment/)에서 다룬다.


<a id="modeling-rdb-update-delete"></a>

## UPDATE·DELETE 설계

RDB 테이블은 UPDATE와 DELETE를 모두 지원한다. WHERE 절 없이 전체 행을 대상으로 실행할 수도 있다.

### UPDATE

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

### DELETE

```sql
-- 조건 기반 DELETE
DELETE FROM orders WHERE order_id = 1001;

-- 범위 DELETE
DELETE FROM orders WHERE status = 'CANCELLED' AND tx_time < '2023-01-01';

-- 전체 삭제 (WHERE 없음)
DELETE FROM temp_staging;
```

### 트랜잭션 내 UPDATE + DELETE 조합

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

### 상태 관리 패턴

```sql
-- 주문 상태 전환
UPDATE orders SET status = 'PROCESSING', updated_at = NOW
WHERE order_id = 1001 AND status = 'PENDING';

-- 여러 주문 일괄 상태 변경
UPDATE orders SET status = 'EXPIRED'
WHERE status = 'PENDING' AND created_at < NOW - 86400000000000;
```

### 주의사항

- WHERE 없는 UPDATE는 테이블 전체 행을 수정한다. 의도치 않은 전체 갱신에 주의할 것.
- 장시간 열린 트랜잭션은 잠금 충돌을 유발할 수 있다.
- UPDATE/DELETE 시 WHERE 절 컬럼에 인덱스가 있으면 성능이 크게 향상된다.

<a id="reference-self-rdb-insert-select"></a>

## 자기 참조·INSERT SELECT

`INSERT INTO ... SELECT ...` 문으로 다른 테이블의 데이터를 복사하거나 변환하여 삽입할 수 있다.

### INSERT SELECT 기본

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

### LOG 테이블에서 RDB 테이블로 데이터 이관

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

### 자기 참조: 동일 테이블 내 복사

```sql
-- 특정 고객 데이터를 다른 고객으로 복제 (예: 테스트 데이터 생성)
INSERT INTO order_history (order_id, customer, item_id, amount, order_time, status)
SELECT order_id + 10000, 'TEST-001', item_id, amount, order_time, status
FROM order_history
WHERE customer = 'CUST-001'
  AND order_time >= '2024-01-01';
```

### 주의사항

- `INSERT SELECT`는 하나의 트랜잭션으로 처리된다. 대량 데이터는 배치로 분할하여 실행한다.
- SELECT 결과의 컬럼 수와 타입이 INSERT 대상 테이블의 컬럼과 일치해야 한다.
- `INSERT SELECT`와 `ON DUPLICATE KEY UPDATE`의 결합은 지원하지 않는다.
