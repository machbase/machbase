---
title: '8.12 TRANSACTION 인덱스와 JSON path 인덱스'
weight: 120
toc: true
---

TRANSACTION 테이블의 PRIMARY KEY·보조 인덱스 전략과 JSON 경로 인덱스 활용법을 다룹니다.


<a id="index-strategy-rdb-primary-key-unique-normal"></a>

## PRIMARY KEY·보조 인덱스 전략

TRANSACTION 테이블은 BTREE 기반 PRIMARY KEY 인덱스와 보조 인덱스를 지원합니다. PRIMARY KEY는 `CREATE PRIMARY KEY INDEX`, 보조 인덱스는 `CREATE INDEX`로 생성합니다.

### PRIMARY KEY 인덱스

TRANSACTION 테이블의 PRIMARY KEY 인덱스는 BTREE 구조로 표시됩니다.

```sql
CREATE TRANSACTION TABLE orders (
    order_id  LONG,
    customer  VARCHAR(64),
    item_id   INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16)
);

-- PRIMARY KEY 인덱스 생성
CREATE PRIMARY KEY INDEX idx_pk_order ON orders(order_id);
```

### 보조 인덱스

```sql
-- 단일 컬럼 보조 인덱스
CREATE INDEX idx_order_customer ON orders(customer);

-- 복합 인덱스
CREATE INDEX idx_order_cust_status ON orders(customer, status);

-- 날짜 범위 조회용 인덱스
CREATE INDEX idx_tx_time ON tx_history(tx_time);
```

### 인덱스를 활용하는 쿼리

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

### 복합 인덱스 설계

```sql
CREATE TRANSACTION TABLE tx_history (
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

### 주의사항

- 인덱스가 없는 컬럼 조건은 풀스캔을 유발합니다.
- UPDATE/DELETE 시에도 WHERE 절 컬럼에 인덱스가 있으면 성능이 향상됩니다.
- 인덱스를 과도하게 생성하면 INSERT/UPDATE 성능이 저하됩니다.
- 복합 인덱스는 앞쪽 컬럼 조건이 포함될 때 효율적으로 사용됩니다.

<a id="index-strategy-rdb-json-path"></a>

## JSON 경로 인덱스

`JSON` 타입 컬럼이 있는 TRANSACTION 테이블에서는 JSON 경로 인덱스를 생성할 수 있습니다. 다만 현재 JSON path 조건은 일반 컬럼 인덱스처럼 쿼리 경로에 푸시다운되지 않을 수 있으므로, 실행 계획을 반드시 확인해야 합니다.

### JSON 컬럼 스키마

```sql
CREATE TRANSACTION TABLE device_state (
    device_id VARCHAR(64),
    ts        DATETIME,
    state     JSON,
    region    VARCHAR(32)
);
```

### JSON 경로 인덱스 생성

```sql
-- JSON 경로 인덱스: state.status 필드
CREATE INDEX idx_state_status ON device_state(state->'$.status');

-- JSON 경로 인덱스: state.code 필드
CREATE INDEX idx_state_code ON device_state(state->'$.code');
```

### JSON 경로 조건 쿼리

```sql
-- state.status 값이 'ALARM'인 디바이스 조회
SELECT device_id, ts, state
FROM device_state
WHERE state->'$.status' = 'ALARM';

-- 복합 조건
SELECT device_id, ts
FROM device_state
WHERE region = 'KR'
  AND state->'$.code' = '500';
```

### 주의사항

- JSON path 조건이 인덱스 경로로 처리되는지 실행 계획으로 확인합니다.
- 중첩 구조가 복잡한 JSON 경로는 선택도가 낮을 수 있습니다.
- 자주 조회하는 JSON 필드는 별도 컬럼으로 추출하여 일반 인덱스를 적용하는 편이 효율적인 경우가 많습니다.

```sql
-- 더 효율적인 패턴: JSON 필드를 컬럼으로 분리
CREATE TRANSACTION TABLE device_state_v2 (
    device_id VARCHAR(64),
    ts        DATETIME,
    status    VARCHAR(16),   -- JSON에서 추출한 필드
    code      INTEGER,       -- JSON에서 추출한 필드
    region    VARCHAR(32),
    extra     JSON           -- 나머지 속성
);

CREATE INDEX idx_ds_status ON device_state_v2(status);
```
