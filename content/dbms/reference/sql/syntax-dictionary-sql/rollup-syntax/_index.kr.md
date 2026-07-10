---
type: docs
title: '17.1.1.16 ROLLUP syntax'
weight: 160
toc: true
---

ROLLUP은 TAG 테이블의 시계열 데이터를 지정한 시간 단위로 자동 집계하는 기능입니다. 백그라운드 스레드가 주기적으로 집계를 수행하며, 결과는 내부 ROLLUP 테이블에 저장됩니다.

## ROLLUP 생성

```sql
CREATE ROLLUP [IF NOT EXISTS] rollup_name
    ON table_name [(column_name | column_name -> 'json_path')]
    INTERVAL number { SEC | MIN | HOUR }
    [WAKEUP INTERVAL number { SEC | MIN | HOUR }]
    [EXTENSION extension_name]
    [WHERE predicate]

CREATE ROLLUP [IF NOT EXISTS] rollup_name
    FROM source_rollup_table
    INTERVAL number { SEC | MIN | HOUR }
    [WAKEUP INTERVAL number { SEC | MIN | HOUR }]
    [EXTENSION extension_name]
    [WHERE predicate]
```

```sql
-- 1초 단위 ROLLUP 생성
CREATE ROLLUP _rollup_tag_value_sec ON tag (value) INTERVAL 1 SEC;

-- 1분 단위 ROLLUP 생성
CREATE ROLLUP _rollup_tag_value_min ON tag (value) INTERVAL 1 MIN;

-- 1시간 단위 ROLLUP 생성
CREATE ROLLUP _rollup_tag_value_hour ON tag (value) INTERVAL 1 HOUR;
```

### 지원 시간 단위

| 단위 | 설명 |
|------|------|
| `SEC` | 초 단위 집계 |
| `MIN` | 분 단위 집계 |
| `HOUR` | 시간 단위 집계 |

> `DAY` 단위는 직접 지원하지 않습니다. 하루 단위 집계는 HOUR ROLLUP을 기반으로 쿼리 단계에서 집계하거나 STREAM을 활용합니다.

### 조건부 ROLLUP

특정 조건을 만족하는 데이터만 집계하는 조건부 ROLLUP을 생성할 수 있습니다.

```sql
CREATE ROLLUP rollup_name
    ON table_name (column_name)
    INTERVAL number { SEC | MIN | HOUR }
    WHERE predicate
```

```sql
-- value2 = 0 인 데이터만 1분 단위로 집계
CREATE ROLLUP _rollup_tag_value_min_ok
    ON tag (value)
    INTERVAL 1 MIN
    WHERE value2 = 0;
```

### 사용자 정의 ROLLUP (Custom Rollup)

임의 SELECT 결과를 대상 TAG 테이블에 저장하는 사용자 정의 ROLLUP입니다.

```sql
CREATE ROLLUP rollup_name
    INTO (dest_table_name)
    AS (select_stmt)
    INTERVAL number { SEC | MIN | HOUR }
    [WAKEUP INTERVAL number { SEC | MIN | HOUR }]
```

```sql
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

### JSON 컬럼 ROLLUP

JSON 컬럼의 특정 멤버를 ROLLUP 대상 값으로 사용할 수 있습니다.

```sql
CREATE ROLLUP tag_json_metric_ru ON tag_json (value->'$.metric') INTERVAL 1 SEC;
```

## ROLLUP 삭제

```sql
DROP ROLLUP rollup_name
```

```sql
DROP ROLLUP _rollup_tag_value_sec;
```

## ROLLUP 제어

```sql
-- 롤업 스레드 시작 / 중지
ALTER ROLLUP rollup_name START;
ALTER ROLLUP rollup_name STOP;

-- 즉시 깨우기 (비동기)
ALTER ROLLUP rollup_name WAKEUP;

-- 즉시 집계 실행 후 완료 대기 (동기)
ALTER ROLLUP rollup_name FORCE;

-- wakeup 주기 변경
ALTER ROLLUP rollup_name SET WAKEUP INTERVAL number { SEC | MIN | HOUR };
```

## ROLLUP 조회

### 자동 선택

ROLLUP이 생성된 TAG 테이블에서 GROUP BY와 집계 함수를 사용하면 옵티마이저가 자동으로 ROLLUP 테이블을 선택합니다.

```sql
SELECT name, DATE_TRUNC('minute', time) AS t,
       AVG(value), MIN(value), MAX(value)
  FROM tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS')
 GROUP BY name, t
 ORDER BY t;
```

### rollup() 함수

TAG 테이블 조회에서 `rollup()` 함수를 사용해 집계 시간 단위를 명시할 수 있습니다.

```sql
SELECT name, rollup('min', 5, time) AS t, AVG(value), COUNT(value)
  FROM tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS')
 GROUP BY name, t
 ORDER BY t;
```

### ROLLUP 힌트로 특정 테이블 강제 선택

```sql
SELECT /*+ ROLLUP_TABLE(rollup_table_name) */
       name, rollup('sec', 30, time) AS rt, AVG(value), COUNT(value)
  FROM tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 00:10:00'
 GROUP BY rt
 ORDER BY rt;
```

## ROLLUP 집계 함수

| 함수 | 설명 |
|------|------|
| `AVG(col)` | 구간 평균 |
| `MIN(col)` | 구간 최솟값 |
| `MAX(col)` | 구간 최댓값 |
| `SUM(col)` | 구간 합계 |
| `COUNT(col)` | 구간 건수 |
| `FIRST(col)` | 구간 첫 번째 값 |
| `LAST(col)` | 구간 마지막 값 |

> `FIRST()` / `LAST()` 를 사용하려면 `EXTENSION` 타입 ROLLUP이 존재해야 하며, `/*+ ROLLUP_TABLE(...) */` 힌트로 해당 테이블을 명시해야 합니다.

## 관련 문서

- [ROLLUP_REBUILD syntax](../rollup-rebuild-syntax/) — 집계 재계산
- [ROLLUP 운영 가이드](/dbms/tag-rollup-usage/) — 상태 확인 및 운영 패턴
