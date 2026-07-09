---
type: docs
title: 'ROLLUP 활용 사례'
weight: 160
---

## 사례 1: IoT 센서 실시간 대시보드

수천 개 센서의 1분 평균을 대시보드에 표시하는 상황입니다.

```sql
-- 설계: 1초 → 1분 → 1시간 계층
CREATE ROLLUP _iot_ru_1s ON iot_sensor(value) INTERVAL 1 SEC;
CREATE ROLLUP _iot_ru_1m FROM _iot_ru_1s INTERVAL 1 MIN;
CREATE ROLLUP _iot_ru_1h FROM _iot_ru_1m INTERVAL 1 HOUR;

-- 대시보드 쿼리 (최근 1시간 1분 단위)
SELECT rollup('min', 1, time) AS rt,
       AVG(value) AS avg_val,
       MAX(value) AS max_val
FROM   iot_sensor
WHERE  name = 'PUMP-01'
  AND  time BETWEEN NOW - INTERVAL '1' HOUR AND NOW
GROUP BY rt
ORDER BY rt;
```

## 사례 2: 품질 정상 데이터만 집계

품질 플래그(quality=1)인 데이터만 집계해 오류 데이터 영향을 차단합니다.

```sql
CREATE ROLLUP _iot_ok_1m ON iot_sensor(value) INTERVAL 1 MIN
  WHERE quality = 1;

-- 조건 ROLLUP 명시 조회
SELECT /*+ ROLLUP_TABLE(_iot_ok_1m) */
       rollup('min', 5, time) AS rt, AVG(value)
FROM   iot_sensor
WHERE  name = 'PUMP-01'
  AND  time BETWEEN '2024-01-01' AND '2024-01-07'
GROUP BY rt
ORDER BY rt;
```

## 사례 3: OHLC 캔들스틱 차트 (확장 ROLLUP)

주식·에너지 거래 데이터의 OHLC 집계입니다.

```sql
CREATE ROLLUP _tick_ru_5m_ext ON tick_data(price) INTERVAL 5 SEC EXTENSION;

-- 5초 단위 OHLC
SELECT /*+ ROLLUP_TABLE(_tick_ru_5m_ext) */
       rollup('sec', 5, time) AS rt,
       FIRST(time, price) AS open,
       MAX(price)         AS high,
       MIN(price)         AS low,
       LAST(time, price)  AS close,
       SUM(volume)        AS volume
FROM   tick_data
WHERE  symbol = 'KRW-BTC'
  AND  time BETWEEN '2024-01-15 09:00:00' AND '2024-01-15 18:00:00'
GROUP BY rt
ORDER BY rt;
```

## 사례 4: 멀티 센서 비교 (PIVOT + ROLLUP)

여러 센서의 시간 단위 평균을 열로 나란히 표시합니다.

```sql
SELECT * FROM (
    SELECT rollup('hour', 1, time) AS rt, name, AVG(value) AS avg_val
    FROM   iot_sensor
    WHERE  name IN ('PUMP-01', 'PUMP-02', 'PUMP-03')
      AND  time BETWEEN '2024-01-01' AND '2024-01-07'
    GROUP BY rt, name
) PIVOT (
    AVG(avg_val) FOR name IN (
        'PUMP-01' AS pump01,
        'PUMP-02' AS pump02,
        'PUMP-03' AS pump03
    )
)
ORDER BY rt;
```

## 사례 5: 일별 에너지 소비량 계산 (FIRST/LAST)

전력량계의 누적값에서 일별 소비량을 계산합니다.

```sql
CREATE ROLLUP _meter_ru_1h_ext ON energy_meter(kwh_total) INTERVAL 1 HOUR EXTENSION;

-- 일별 소비량 = 일 종료 값 - 일 시작 값
SELECT rt,
       LAST(time, kwh_total) - FIRST(time, kwh_total) AS daily_kwh
FROM (
    SELECT /*+ ROLLUP_TABLE(_meter_ru_1h_ext) */
           rollup('day', 1, time) AS rt,
           FIRST(time, kwh_total), LAST(time, kwh_total)
    FROM   energy_meter
    WHERE  name = 'METER-01'
      AND  time BETWEEN '2024-01-01' AND '2024-01-31'
    GROUP BY rt
) ORDER BY rt;
```
