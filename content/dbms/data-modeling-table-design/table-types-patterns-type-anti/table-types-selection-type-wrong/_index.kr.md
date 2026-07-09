---
type: docs
title: '4.2.3 잘못된 타입 선택'
weight: 30
---

데이터 특성에 맞지 않는 테이블 타입을 선택하는 대표적인 안티패턴을 설명합니다.

## 안티패턴 1: 이벤트 로그를 TAG 테이블에 저장

```sql
-- 잘못됨: 이벤트 로그를 TAG로 저장
CREATE TAG TABLE error_log_wrong (
    name   VARCHAR(256) PRIMARY KEY,  -- 이벤트 내용이 태그 이름이 됨
    time   DATETIME     BASETIME,
    level  SHORT
);
-- 문제: 이벤트마다 고유 이름 → 태그 수 폭발
```

**올바른 설계**: LOG 테이블 사용

```sql
CREATE TABLE error_log (
    level   SHORT,
    msg     VARCHAR(512),
    src     VARCHAR(128)
);
```

## 안티패턴 2: 센서 값을 LOG 테이블에 저장

```sql
-- 잘못됨: 센서 값을 LOG로 저장
CREATE TABLE sensor_wrong (
    sensor_id VARCHAR(64),
    value     DOUBLE
    -- 태그별 시간 범위 집계 쿼리가 매우 비효율적
);
```

**올바른 설계**: TAG 테이블 사용

```sql
CREATE TAG TABLE sensor_data (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

## 안티패턴 3: 대용량 이력을 LOOKUP에 저장

```sql
-- 잘못됨: 수천만 건 주문 이력을 LOOKUP에
CREATE LOOKUP TABLE order_history_wrong (
    order_id LONG PRIMARY KEY,
    customer VARCHAR(64)
    -- LOOKUP은 소규모 전용, 대용량에서 성능 저하
);
```

**올바른 설계**: RDB 테이블 사용

```sql
CREATE RDB TABLE order_history (
    order_id  LONG,
    customer  VARCHAR(64),
    item_id   INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16)
);
-- UPDATE/DELETE/SELECT 모두 지원
UPDATE order_history SET status = 'SHIPPED' WHERE order_id = 1001;
```

## 안티패턴 4: 시계열 데이터를 RDB에 저장

시계열 데이터(센서값)를 RDB 테이블에 저장하면 시간 범위 쿼리 성능이 나쁘고, Append API의 고속 버퍼 최적화도 사용할 수 없습니다. 자세한 내용은 [시계열 데이터 RDB 오용](/dbms/data-modeling-table-design/table-types-patterns-type-anti/time-series-storage-misuse-rdb/) 항목을 참고하십시오.
