---
title: '6.10 FIRST / LAST 함수'
weight: 90
toc: true
---
FIRST / LAST 함수에 해당하는 세부 문서를 모았습니다.


<a id="first-last-rollup"></a>

## FIRST / LAST 함수

`FIRST()`와 `LAST()` 함수는 시간 구간 내 첫 번째 값과 마지막 값을 반환합니다. 확장 ROLLUP(EXTENSION)이 있을 때만 사용할 수 있습니다.

### 구문

```sql
FIRST(basetime_column, value_column)
LAST(basetime_column, value_column)
```

### 사용 예시

```sql
-- 1분 단위 FIRST/LAST (확장 ROLLUP 필요)
SELECT rollup('min', 1, time) AS rt,
       FIRST(time, value) AS first_val,
       LAST(time, value)  AS last_val,
       MIN(value), MAX(value), AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 06:00:00'
GROUP BY rt
ORDER BY rt;
```

### OHLC (캔들스틱) 패턴

금융 데이터나 시계열 분석에서 자주 사용하는 OHLC(시가/고가/저가/종가) 조회:

```sql
SELECT rollup('min', 5, time) AS rt,
       FIRST(time, price) AS open,    -- 시가
       MAX(price)         AS high,    -- 고가
       MIN(price)         AS low,     -- 저가
       LAST(time, price)  AS close    -- 종가
FROM   stock_tick
WHERE  code = 'AAPL'
  AND  time BETWEEN '2024-01-15 09:00:00' AND '2024-01-15 18:00:00'
GROUP BY rt
ORDER BY rt;
```

### 확장 ROLLUP 힌트 지정

같은 주기에 일반 ROLLUP과 확장 ROLLUP이 함께 있으면 힌트로 확장 ROLLUP을 명시해야 합니다.

```sql
SELECT /*+ ROLLUP_TABLE(_tag_ru_1m_ext) */
       rollup('min', 1, time) AS rt,
       FIRST(time, value), LAST(time, value)
FROM   tag
WHERE  name = 'SENSOR-01'
GROUP BY rt
ORDER BY rt;
```

> 일반 ROLLUP에 힌트를 지정한 상태에서 FIRST/LAST를 호출하면 오류가 발생합니다.

### 활용 사례

| 분야 | FIRST | LAST |
|------|-------|------|
| 금융 | 시가(Open) | 종가(Close) |
| 제조 | 교대 시작 값 | 교대 종료 값 |
| 에너지 | 시간 시작 계량값 | 시간 종료 계량값 (차이 = 소비량) |
| IoT | 연결 시 첫 수신값 | 연결 종료 전 마지막 수신값 |
