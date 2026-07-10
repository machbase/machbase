---
title: '8.5 조회와 분석'
weight: 50
toc: true
---

RDB 테이블의 SELECT, 집계, 필터링 등 조회 관련 내용을 다룬다. RDB 테이블은 PRIMARY KEY와 보조 인덱스를 기반으로 단건 조회, 범위 조회, JOIN, 집계를 수행한다.

<a id="query-rdb-basic-select"></a>

## 기본 SELECT

RDB 테이블은 일반 SQL SELECT 문으로 조회한다.

```sql
SELECT order_id, customer, amount, status
FROM order_history
WHERE order_id = 1001;
```

조건 컬럼에 인덱스가 있으면 조회 성능이 향상된다.

```sql
SELECT order_id, amount, order_time
FROM order_history
WHERE customer = 'CUST-001'
  AND order_time >= '2026-01-01 00:00:00';
```

<a id="query-rdb-filter-sort-limit"></a>

## 필터링, 정렬, 제한

일반 조건식, 범위 조건, 정렬, `LIMIT`을 사용할 수 있다.

```sql
SELECT order_id, customer, amount, status
FROM order_history
WHERE status = 'PENDING'
ORDER BY order_time DESC
LIMIT 100;
```

복합 인덱스는 앞쪽 컬럼 조건이 함께 사용될 때 효율적이다.

```sql
CREATE INDEX idx_order_status_time ON order_history(status, order_time);

SELECT order_id, amount
FROM order_history
WHERE status = 'PENDING'
  AND order_time >= '2026-01-01 00:00:00';
```

<a id="query-rdb-join"></a>

## JOIN 조회

RDB 테이블은 다른 RDB 테이블이나 TAG/LOG 테이블에서 가공한 결과와 함께 사용할 수 있다.

```sql
SELECT o.order_id, o.customer, p.name, o.amount
FROM order_history o
JOIN product_catalog p ON o.item_id = p.product_id
WHERE o.status = 'ORDERED';
```

TAG 또는 LOG 테이블의 원본 데이터를 집계한 뒤 RDB 테이블에 적재하면, 이후 업무 기준 조회와 JOIN을 단순하게 구성할 수 있다.

```sql
SELECT s.sensor_id, s.avg_value, m.site, m.unit
FROM daily_sensor_summary s
JOIN sensor_master m ON s.sensor_id = m.sensor_id
WHERE s.summary_date = '2026-01-01';
```

<a id="query-rdb-aggregation"></a>

## 집계 조회

RDB 테이블은 업무 상태나 집계 결과를 다시 그룹화할 때 사용한다.

```sql
SELECT status, COUNT(*) AS cnt, SUM(amount) AS total_amount
FROM order_history
GROUP BY status;
```

시간 또는 카테고리별 집계가 반복되면 집계 기준 컬럼에 인덱스를 추가하거나, 주기적으로 별도 요약 테이블을 생성한다.

<a id="query-rdb-json"></a>

## JSON 경로 조회

`JSON` 컬럼을 사용하는 RDB 테이블은 JSON path 조건을 조회에 사용할 수 있다.

```sql
CREATE RDB TABLE device_state (
    device_id VARCHAR(64),
    ts        DATETIME,
    state     JSON,
    region    VARCHAR(32)
);

SELECT device_id, ts
FROM device_state
WHERE state->'$.status' = 'ALARM';
```

자주 조회하는 JSON 필드는 별도 컬럼으로 분리하거나 JSON path 인덱스 적용 여부를 검토한다. 자세한 내용은 [RDB 인덱스와 JSON path 인덱스](/dbms/rdb-table-usage/rdb-index-json-path/)를 참고한다.

<a id="query-rdb-performance"></a>

## 조회 성능 기준

- 단건 조회는 PRIMARY KEY 조건을 우선 사용한다.
- UPDATE/DELETE 조건에 쓰는 컬럼에도 인덱스를 설계한다.
- 대량 데이터 조회는 시간, 상태, 카테고리 등 선택도가 있는 조건으로 범위를 줄인다.
- JSON path 조건은 실행 계획을 확인하고, 고빈도 조건은 일반 컬럼으로 분리한다.
- JOIN 대상 컬럼은 타입과 값 형식을 일치시킨다.
