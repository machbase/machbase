---
title: '8.5 조회와 분석'
weight: 50
toc: true
---

TRANSACTION 테이블의 SELECT, 집계, 필터링 등 조회 관련 내용을 다룹니다. TRANSACTION 테이블은 PRIMARY KEY와 보조 인덱스를 기반으로 단건 조회, 범위 조회, JOIN, 집계를 수행합니다.

<a id="query-rdb-basic-select"></a>

## 기본 SELECT

TRANSACTION 테이블은 일반 SQL SELECT 문으로 조회합니다.

```sql
CREATE TRANSACTION TABLE order_history (
    order_id   LONG PRIMARY KEY,
    customer   VARCHAR(64),
    item_id    LONG,
    amount     DOUBLE,
    status     VARCHAR(16),
    order_time DATETIME
);

CREATE TRANSACTION TABLE product_catalog (
    product_id LONG PRIMARY KEY,
    name       VARCHAR(128)
);

INSERT INTO product_catalog VALUES (42, 'Temperature Sensor');
INSERT INTO order_history
VALUES (1001, 'CUST-001', 42, 19900, 'ORDERED',
        TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));

SELECT order_id, customer, amount, status
FROM order_history
WHERE order_id = 1001;
```

조건 컬럼에 인덱스가 있으면 조회 성능이 향상됩니다.

```sql
SELECT order_id, amount, order_time
FROM order_history
WHERE customer = 'CUST-001'
  AND order_time >= '2026-01-01 00:00:00';
```

<a id="query-rdb-filter-sort-limit"></a>

## 필터링, 정렬, 제한

일반 조건식, 범위 조건, 정렬, `LIMIT`을 사용할 수 있습니다.

```sql
SELECT order_id, customer, amount, status
FROM order_history
WHERE status = 'PENDING'
ORDER BY order_time DESC
LIMIT 100;
```

복합 인덱스는 앞쪽 컬럼 조건이 함께 사용될 때 효율적입니다.

```sql
CREATE INDEX idx_order_status_time ON order_history(status, order_time);

SELECT order_id, amount
FROM order_history
WHERE status = 'PENDING'
  AND order_time >= '2026-01-01 00:00:00';
```

<a id="query-rdb-join"></a>

## JOIN 조회

TRANSACTION 테이블은 다른 TRANSACTION 테이블이나 TAG/LOG 테이블에서 가공한 결과와 함께 사용할 수 있습니다.

```sql
SELECT o.order_id, o.customer, p.name, o.amount
FROM order_history o
JOIN product_catalog p ON o.item_id = p.product_id
WHERE o.status = 'ORDERED';
```

TAG 또는 LOG 테이블의 원본 데이터를 집계한 뒤 TRANSACTION 테이블에 적재하면, 이후 업무 기준
조회와 JOIN을 단순하게 구성할 수 있습니다.

<a id="query-rdb-aggregation"></a>

## 집계 조회

TRANSACTION 테이블은 업무 상태나 집계 결과를 다시 그룹화할 때 사용합니다.

```sql
SELECT status, COUNT(*) AS cnt, SUM(amount) AS total_amount
FROM order_history
GROUP BY status;
```

시간 또는 카테고리별 집계가 반복되면 집계 기준 컬럼에 인덱스를 추가하거나, 주기적으로 별도 요약 테이블을 생성합니다.

<a id="query-rdb-json"></a>

## JSON 경로 조회

`JSON` 컬럼을 사용하는 TRANSACTION 테이블은 JSON path 조건을 조회에 사용할 수 있습니다.

```sql
CREATE TRANSACTION TABLE device_state (
    device_id VARCHAR(64),
    ts        DATETIME,
    state     JSON,
    region    VARCHAR(32)
);

SELECT device_id, ts
FROM device_state
WHERE state->'$.status' = 'ALARM';

DROP TABLE device_state;
DROP INDEX idx_order_status_time;
DROP TABLE product_catalog;
DROP TABLE order_history;
```

자주 조회하는 JSON 필드는 별도 컬럼으로 분리하거나 JSON path 인덱스 적용 여부를 검토합니다.
자세한 내용은 [인덱스와 성능](/dbms/rdb-table-usage/index-performance/#index-strategy-rdb-json-path)을
참고합니다.

<a id="query-rdb-performance"></a>

## 조회 성능 기준

- 단건 조회는 PRIMARY KEY 조건을 우선 사용합니다.
- UPDATE/DELETE 조건에 쓰는 컬럼에도 인덱스를 설계합니다.
- 대량 데이터 조회는 시간, 상태, 카테고리 등 선택도가 있는 조건으로 범위를 줄입니다.
- JSON path 조건은 실행 계획을 확인하고, 고빈도 조건은 일반 컬럼으로 분리합니다.
- JOIN 대상 컬럼은 타입과 값 형식을 일치시킵니다.
