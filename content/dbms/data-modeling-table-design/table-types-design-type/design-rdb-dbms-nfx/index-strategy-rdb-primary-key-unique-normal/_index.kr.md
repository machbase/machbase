---
type: docs
title: 'PRIMARY KEY·UNIQUE·일반 인덱스 전략'
weight: 30
---

RDB 테이블은 KV Secondary 인덱스를 사용합니다. `CREATE INDEX` 문으로 인덱스를 생성합니다.

## 인덱스 생성

```sql
-- 단일 컬럼 인덱스
CREATE INDEX idx_name ON table_name(column1);

-- 복합 인덱스
CREATE INDEX idx_composite ON table_name(col1, col2);
```

## 인덱스 유형

RDB 테이블에서 `CREATE INDEX`로 생성되는 인덱스는 내부적으로 KV Secondary 인덱스를 사용합니다.

| 구분 | 문법 | 설명 |
|------|------|------|
| 일반 인덱스 | `CREATE INDEX idx ON tbl(col)` | 조회 최적화 |
| 복합 인덱스 | `CREATE INDEX idx ON tbl(col1, col2)` | 다중 컬럼 조건 최적화 |

## 설계 지침

인덱스는 자주 사용하는 WHERE 조건 컬럼에 생성합니다.

```sql
CREATE RDB TABLE order_history (
    order_id   LONG,
    customer   VARCHAR(64),
    item_id    INTEGER,
    amount     DOUBLE,
    order_time DATETIME
);

-- 고객별 조회용 인덱스
CREATE INDEX idx_order_customer ON order_history(customer);

-- 날짜 범위 조회용 인덱스
CREATE INDEX idx_order_time ON order_history(order_time);

-- 복합 조건 최적화 (고객 + 날짜)
CREATE INDEX idx_order_cust_time ON order_history(customer, order_time);
```

## 인덱스 사용 조회

```sql
-- 인덱스를 활용하는 조회
SELECT order_id, amount, order_time
FROM order_history
WHERE customer = 'CUST-001'
  AND order_time >= '2024-01-01';

-- 복합 인덱스 활용
SELECT order_id, amount
FROM order_history
WHERE customer = 'CUST-001'
  AND order_time BETWEEN '2024-01-01' AND '2024-12-31';
```

## 주의사항

- 인덱스가 없는 컬럼 조건은 풀스캔이 발생합니다.
- 인덱스를 과도하게 생성하면 INSERT 성능이 저하됩니다.
- 컬럼 선택도(selectivity)가 높은 컬럼에 인덱스를 생성합니다.
