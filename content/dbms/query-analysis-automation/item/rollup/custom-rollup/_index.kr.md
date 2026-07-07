---
type: docs
title: '사용자 정의 ROLLUP (Custom Rollup)'
weight: 90
---

Custom Rollup은 사용자가 직접 SELECT 쿼리를 정의하고, 그 결과를 대상 TAG 테이블에 주기적으로 저장하는 ROLLUP입니다. 기본 ROLLUP이 지원하지 않는 복잡한 집계(멀티 컬럼 GROUP BY, 사용자 정의 계산 등)를 사전 처리할 때 사용합니다.

## 생성 구문

```sql
CREATE ROLLUP rollup_name
  INTO (dest_table_name)
  AS (select_stmt)
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)];
```

- `INTO`: 집계 결과를 저장할 TAG 테이블 (미리 생성되어 있어야 함)
- `AS`: 실행할 SELECT 쿼리 (INSERT ... SELECT 형태로 실행됨)
- WHERE 조건은 SELECT 내부에서만 사용합니다. 외부 WHERE는 지원하지 않습니다.

## 예시: 주식 틱 데이터 1분 집계

```sql
-- 1. 원본 테이블 (주식 틱)
CREATE TAG TABLE stock_tick (
    code  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    price DOUBLE SUMMARIZED
);

-- 2. 집계 결과 저장 테이블
CREATE TAG TABLE stock_rollup_1m (
    code      VARCHAR(20) PRIMARY KEY,
    time      DATETIME BASETIME,
    sum_price DOUBLE SUMMARIZED,
    cnt       DOUBLE SUMMARIZED
);

-- 3. Custom Rollup 생성 (1분마다 실행)
CREATE ROLLUP rollup_stock_1m
  INTO (stock_rollup_1m)
  AS (
    SELECT code,
           DATE_TRUNC('minute', time) AS time,
           SUM(price)                 AS sum_price,
           COUNT(*)                   AS cnt
      FROM stock_tick
     GROUP BY code, time
  )
  INTERVAL 1 MIN;
```

## 예시: 다중 센서 비율 집계

```sql
CREATE ROLLUP rollup_efficiency_1h
  INTO (efficiency_rollup)
  AS (
    SELECT name,
           DATE_TRUNC('hour', time) AS time,
           SUM(CASE WHEN value > 0 THEN 1.0 ELSE 0.0 END) / COUNT(*) AS uptime_ratio
      FROM sensor_data
     WHERE sensor_type = 'MOTOR'
     GROUP BY name, time
  )
  INTERVAL 1 HOUR;
```

## 제약사항

- `INTO` 대상 테이블은 TAG 테이블이어야 합니다.
- AS 절의 SELECT는 대상 테이블 컬럼 수와 타입이 일치해야 합니다.
- `INTERVAL ... WHERE ...` 형태(외부 WHERE)는 지원하지 않습니다. WHERE는 AS 내부에만 작성합니다.
- Rebuild(부분 재구성)는 Custom Rollup에 적용할 수 없습니다. 수동으로 대상 테이블을 관리해야 합니다.

## 시작·중지

Custom Rollup도 `ALTER ROLLUP`으로 제어합니다.

```sql
ALTER ROLLUP rollup_stock_1m STOP;
ALTER ROLLUP rollup_stock_1m START;
ALTER ROLLUP rollup_stock_1m FORCE;  -- 즉시 실행
```
