---
title: 'Custom Rollup: 사용자 정의 집계'
type: docs
weight: 62
---

## 개요

Custom Rollup은 사용자가 작성한 `SELECT` 집계식을 주기적으로 실행하여, 지정한 대상 TAG 테이블에 결과를 누적 저장하는 기능입니다.

다중 컬럼 집계, 조건 기반 집계, 그리고 단계형(계층형) 집계 구성에 적합합니다.

## 기존 Rollup과 차이

| 구분 | 기존 Rollup | Custom Rollup |
|---|---|---|
| 생성 문법 | `CREATE ROLLUP ... ON table(column)` | `CREATE ROLLUP ... INTO (...) AS (SELECT ...)` |
| 집계 정의 | 엔진 고정 집계 | 사용자 정의 `SELECT` |
| 저장 대상 | 내부 Rollup 테이블 | 사용자가 미리 생성한 TAG 테이블 |
| WHERE 위치 | `INTERVAL ... WHERE ...` (외부 WHERE) | `SELECT` 내부 `WHERE` |
| 조회 방식 | `rollup()` 힌트 기반 | 결과 테이블 직접 조회 + 재집계 |
| 메타 구분 | `v$rollup.ext_type = 0/1` | `v$rollup.ext_type = 2` |

## 동작 모델과 재집계

Custom Rollup은 주기마다 증분 구간을 읽어 `INSERT INTO <dest> SELECT ...` 형태로 결과를 저장합니다.

같은 시간 버킷에 부분 집계 row가 여러 개 누적될 수 있으므로, 최종 조회 시에는 버킷 기준으로 반드시 재집계해야 합니다.

```sql
SELECT code,
       time,
       SUM(sum_price) / SUM(cnt) AS avg_price
  FROM stock_rollup_1m
 GROUP BY code, time
 ORDER BY time;
```

## 문법

### Custom Rollup 생성

```sql
CREATE ROLLUP <rollup_name>
INTO (<dest_tag_table>)
AS (
  SELECT ...
  FROM <source_tag_table>
  [WHERE ...]
  GROUP BY ...
)
INTERVAL <n> (SEC | MIN | HOUR)
[WAKEUP INTERVAL <m> (SEC | MIN | HOUR)];
```

### 제어 명령

```sql
ALTER ROLLUP <rollup_name> START;
ALTER ROLLUP <rollup_name> STOP;
ALTER ROLLUP <rollup_name> FORCE;
DROP ROLLUP <rollup_name>;
```

참고: 생성 직후 Rollup 스레드는 자동 시작됩니다. 즉시 `START`를 다시 호출하면 오류가 발생할 수 있습니다.

## 생성 조건 및 제약

### 소스/대상 테이블

- 소스는 TAG 테이블 1개만 허용됩니다.
- 대상은 사전에 생성된 TAG 테이블이어야 합니다.
- Rollup이 존재하는 동안 대상 테이블 `DROP`은 차단됩니다.

### SELECT 제약

- `AS (...)` 내부는 유효한 `SELECT`여야 합니다.
- `FROM`은 정확히 1개 테이블만 허용됩니다.
- `JOIN`, `FROM` 서브쿼리, `ON/USING`은 허용되지 않습니다.
- SELECT 텍스트 길이 제한이 있습니다(내부 제한 1024 기준).
- 결과 컬럼 개수/타입은 대상 테이블과 호환되어야 합니다.

### WHERE 제약

- `SELECT` 내부 `WHERE`는 사용 가능합니다.
- 소스의 BASETIME 컬럼을 `WHERE`에서 직접 참조하면 생성이 거부됩니다.
- `INTERVAL ... WHERE ...` 형태의 외부 `WHERE`는 Custom 문법에서 허용되지 않습니다.

### 간격 제약

- `INTERVAL`은 양수여야 합니다.
- `WAKEUP INTERVAL` 생략 시 `INTERVAL`과 동일 값이 사용됩니다.
- `WAKEUP INTERVAL <= INTERVAL` 이어야 하며, `INTERVAL`의 약수여야 합니다.

### DATE_BIN 사용 시 주의

`DATE_BIN`의 origin은 유효한 DATETIME 범위 값이어야 합니다. 경계값 사용 시 환경/타임존 조건에 따라 오류가 발생할 수 있으므로 충분히 여유 있는 origin을 권장합니다.

## 기본 예제

### 1) 소스/대상 테이블

```sql
CREATE TAG TABLE stock_tick (
  code      VARCHAR(20) PRIMARY KEY,
  time      DATETIME BASETIME,
  price     DOUBLE,
  volume    DOUBLE,
  bid_price DOUBLE,
  ask_price DOUBLE
);

CREATE TAG TABLE stock_rollup_1m (
  code       VARCHAR(20) PRIMARY KEY,
  time       DATETIME BASETIME,
  sum_price  DOUBLE,
  sum_volume DOUBLE,
  sum_bid    DOUBLE,
  sum_ask    DOUBLE,
  cnt        INTEGER
);
```

### 2) Custom Rollup 생성

```sql
CREATE ROLLUP rollup_stock_1m
INTO (stock_rollup_1m)
AS (
  SELECT code,
         DATE_TRUNC('minute', time) AS time,
         SUM(price)                 AS sum_price,
         SUM(volume)                AS sum_volume,
         SUM(bid_price)             AS sum_bid,
         SUM(ask_price)             AS sum_ask,
         COUNT(*)                   AS cnt
    FROM stock_tick
   GROUP BY code, time
)
INTERVAL 1 MIN;
```

### 3) 조회 시 재집계

```sql
SELECT code,
       time,
       SUM(sum_price)  / SUM(cnt) AS avg_price,
       SUM(sum_volume)            AS total_volume,
       SUM(sum_bid)    / SUM(cnt) AS avg_bid,
       SUM(sum_ask)    / SUM(cnt) AS avg_ask
  FROM stock_rollup_1m
 GROUP BY code, time
 ORDER BY time;
```

## OHLCV 패턴 (FIRST/LAST)

`FIRST/LAST`를 사용하는 경우 재집계 정확도를 위해 보조 시간 컬럼(`firsttime`, `lasttime`)을 함께 저장하는 것을 권장합니다.

```sql
SELECT code,
       time,
       FIRST(firsttime, open) AS open,
       MAX(high)              AS high,
       MIN(low)               AS low,
       LAST(lasttime, close)  AS close,
       SUM(volume)            AS volume,
       SUM(cnt)               AS cnt
  FROM stock_candle_1m
 GROUP BY code, time
 ORDER BY code, time;
```

## 계층형 구성 예시 (1분 -> 10분)

Custom Rollup 결과 테이블도 TAG 테이블이므로 다음 단계 Rollup의 소스로 사용할 수 있습니다.

```sql
CREATE ROLLUP rollup_stock_candle_10m
INTO (stock_candle_10m)
AS (
  SELECT code,
         DATE_BIN('min', 10, time, TO_DATE('2000-01-01 00:00:00')) AS time,
         MIN(firsttime)         AS firsttime,
         MAX(lasttime)          AS lasttime,
         FIRST(firsttime, open) AS open,
         MAX(high)              AS high,
         MIN(low)               AS low,
         LAST(lasttime, close)  AS close,
         SUM(volume)            AS volume,
         SUM(cnt)               AS cnt
    FROM stock_candle_1m
   GROUP BY code, time
)
INTERVAL 10 MIN;
```

## 메타 확인

```sql
SELECT rollup_table,
       source_table,
       ext_type,
       enabled,
       frequency,
       wakeup_interval,
       predicate
  FROM v$rollup
 WHERE rollup_table = 'ROLLUP_STOCK_1M';
```

- `ext_type = 2`: Custom Rollup
- `predicate`: Custom `SELECT` 본문

## 운영 주의사항

- Rollup이 존재하면 대상 테이블 `DROP`은 거부됩니다.
- 권장 삭제 순서:

```sql
ALTER ROLLUP <name> STOP;
DROP ROLLUP <name>;
DROP TABLE <dest_table>;
DROP TABLE <source_table>;
```

- 소스 TAG 테이블을 `CASCADE`로 삭제하면 종속 Rollup이 함께 정리됩니다.
- Custom Rollup 대상 테이블은 자동 삭제되지 않으므로 필요 시 별도로 삭제해야 합니다.

## 운영 권장사항

- 결과 조회 SQL은 재집계 쿼리로 표준화하는 것이 안전합니다.
- FIRST/LAST 계열은 `firsttime`, `lasttime` 보조 컬럼을 유지하는 것이 좋습니다.
- 대상 스키마 변경이 필요하면 Rollup 중지/삭제 후 재생성 절차를 사용하십시오.
- 운영 배치에서는 `WAKEUP INTERVAL`을 명시해 지연과 부하를 조정하십시오.
