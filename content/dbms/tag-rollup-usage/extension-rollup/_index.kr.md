---
title: '6.7 확장 ROLLUP과 FIRST/LAST'
weight: 70
toc: true
aliases:
  - /dbms/tag-rollup-usage/first-last-rollup/
---

<a id="rollup-extension"></a>

## 확장 ROLLUP (EXTENSION)

`EXTENSION` 키워드를 붙여 생성하면 기본 통계(MIN/MAX/SUM/COUNT) 외에 구간의 첫 번째 값(FIRST)과 마지막 값(LAST)도 저장합니다.

### 생성

```sql
-- 수동 생성
CREATE ROLLUP _tag_rollup_1s_ext ON tag(value) INTERVAL 1 SEC EXTENSION;

-- WITH ROLLUP 자동 생성
CREATE TAG TABLE tag (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP EXTENSION;
```

### FIRST / LAST 조회

확장 ROLLUP이 있어야 `FIRST()`, `LAST()` 집계 함수를 사용할 수 있습니다.

```sql
SELECT rollup('min', 1, time) AS rt,
       FIRST(time, value) AS first_val,
       LAST(time, value)  AS last_val,
       MIN(value), MAX(value)
FROM   tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 01:00:00'
GROUP BY rt
ORDER BY rt;
```

> 확장 ROLLUP이 아닌 일반 ROLLUP에 `ROLLUP_TABLE` 힌트를 지정한 상태에서 FIRST/LAST를 호출하면 오류가 발생합니다.

### 힌트로 특정 ROLLUP 지정

같은 주기·컬럼에 일반 롤업과 확장 롤업이 함께 있으면, 엔진은 일반 롤업을 기본으로 선택합니다. FIRST/LAST가 필요할 때는 힌트로 확장 롤업을 명시합니다.

```sql
SELECT /*+ ROLLUP_TABLE(_tag_rollup_1s_ext) */
       rollup('sec', 10, time) AS rt,
       FIRST(time, value), LAST(time, value)
FROM   tag
WHERE  name = 'SENSOR-01'
GROUP BY rt
ORDER BY rt;
```

### 선택 기준

| 요구사항 | 사용할 ROLLUP |
|----------|--------------|
| MIN/MAX/AVG/SUM/COUNT | 일반 ROLLUP |
| 구간 첫 값·마지막 값 필요 | 확장 ROLLUP (EXTENSION) |
| 캔들스틱(OHLC) 차트 | 확장 ROLLUP (FIRST=Open, LAST=Close) |

### OHLC 예제

```sql
SELECT rollup('min', 5, time) AS rt,
       FIRST(time, price) AS open,
       MAX(price)         AS high,
       MIN(price)         AS low,
       LAST(time, price)  AS close
  FROM stock_tick
 WHERE code = 'AAPL'
   AND time >= TO_DATE('2026-01-15 09:00:00')
   AND time <  TO_DATE('2026-01-15 18:00:00')
 GROUP BY rt
 ORDER BY rt;
```

`FIRST(basetime_column, value_column)`과 `LAST(basetime_column, value_column)`의 시간 컬럼은
대상 TAG 테이블의 BASETIME 컬럼을 사용합니다.
