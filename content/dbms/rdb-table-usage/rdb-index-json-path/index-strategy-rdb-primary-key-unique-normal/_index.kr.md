---
type: docs
title: '8.12.1 PRIMARY KEY·보조 인덱스 전략'
weight: 30
---

RDB 테이블은 BTREE 기반 PRIMARY KEY 인덱스와 보조 인덱스를 지원합니다. 보조 인덱스는 `CREATE INDEX`, PRIMARY KEY 인덱스는 `CREATE PRIMARY KEY INDEX` 문으로 생성합니다.

## PRIMARY KEY 인덱스

RDB 테이블의 PRIMARY KEY 인덱스는 BTREE 구조로 표시됩니다.

```sql
CREATE RDB TABLE orders (
    order_id  LONG,
    customer  VARCHAR(64),
    item_id   INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16)
);

-- PRIMARY KEY 인덱스 생성
CREATE PRIMARY KEY INDEX idx_pk_order ON orders(order_id);
```

## 보조 인덱스

```sql
-- 단일 컬럼 보조 인덱스
CREATE INDEX idx_order_customer ON orders(customer);

-- 복합 인덱스
CREATE INDEX idx_order_cust_status ON orders(customer, status);

-- 날짜 범위 조회용 인덱스
CREATE INDEX idx_tx_time ON tx_history(tx_time);
```

## 인덱스를 활용하는 쿼리

```sql
-- PK 인덱스 활용
SELECT order_id, amount, status FROM orders WHERE order_id = 1001;

-- 보조 인덱스 활용
SELECT order_id, amount FROM orders WHERE customer = 'CUST-001';

-- 복합 인덱스 활용 (앞쪽 컬럼부터 적용)
SELECT order_id, amount FROM orders
WHERE customer = 'CUST-001' AND status = 'PENDING';

-- UPDATE with index
UPDATE orders SET status = 'SHIPPED' WHERE customer = 'CUST-001' AND status = 'PENDING';
```

## 복합 인덱스 설계

```sql
CREATE RDB TABLE tx_history (
    tx_id      LONG,
    account_id VARCHAR(32),
    tx_time    DATETIME,
    amount     DOUBLE,
    status     VARCHAR(16)
);

-- 계좌별 날짜 범위 조회 최적화
CREATE INDEX idx_tx_acct_time ON tx_history(account_id, tx_time);

-- 조회 예시 (복합 인덱스 활용)
SELECT tx_id, amount, status
FROM tx_history
WHERE account_id = 'ACC-001'
  AND tx_time BETWEEN '2024-01-01' AND '2024-12-31';
```

## 주의사항

- 인덱스가 없는 컬럼 조건은 풀스캔이 발생합니다.
- UPDATE/DELETE 시에도 WHERE 절의 컬럼에 인덱스가 있으면 성능이 향상됩니다.
- 인덱스를 과도하게 생성하면 INSERT/UPDATE 성능이 저하됩니다.
- 복합 인덱스는 앞쪽 컬럼 조건이 있을 때 효율적으로 사용됩니다.
