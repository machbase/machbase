---
type: docs
title: 'STREAM 활용 예시'
weight: 60
---

## 예시 1: 센서 알람 감지

임계값을 초과하는 센서 값을 알람 테이블에 자동으로 기록합니다.

```sql
-- 알람 대상 테이블
CREATE TABLE alarm_log (
    time     DATETIME,
    sensor   VARCHAR(40),
    value    DOUBLE,
    severity VARCHAR(10)
);

-- STREAM 등록: 90 초과 시 CRITICAL, 80 초과 시 WARNING
EXEC STREAM_CREATE('stream_alarm',
  'INSERT INTO alarm_log
   SELECT time, device_id, value,
          CASE WHEN value > 90 THEN ''CRITICAL'' ELSE ''WARNING'' END
   FROM   sensor_log
   WHERE  value > 80');

EXEC STREAM_START('stream_alarm');
```

## 예시 2: 1분 단위 이동 집계

매 60초마다 소스 테이블의 신규 데이터를 집계합니다.

```sql
CREATE TABLE sensor_1min (
    time      DATETIME,
    sensor_id VARCHAR(40),
    avg_val   DOUBLE,
    max_val   DOUBLE,
    row_cnt   INTEGER
);

EXEC STREAM_CREATE('stream_1min',
  'INSERT INTO sensor_1min
   SELECT DATE_TRUNC(''minute'', time), device_id,
          AVG(value), MAX(value), COUNT(*)
   FROM   sensor_log
   GROUP BY 1, device_id
   BY 60 SECOND');

EXEC STREAM_START('stream_1min');
```

## 예시 3: 데이터 정규화 및 라우팅

원본 데이터를 단위 변환해 다른 테이블로 라우팅합니다.

```sql
-- 온도 원본 (°F) → 변환 대상 (°C)
EXEC STREAM_CREATE('stream_unit_convert',
  'INSERT INTO temp_celsius
   SELECT time, sensor_id, (value - 32.0) * 5.0 / 9.0 AS temp_c
   FROM   temp_fahrenheit');

EXEC STREAM_START('stream_unit_convert');
```

## 예시 4: 멀티 스트림으로 단계 처리

```sql
-- 1단계: 유효 데이터만 필터
EXEC STREAM_CREATE('stream_step1',
  'INSERT INTO valid_log
   SELECT * FROM raw_log WHERE value BETWEEN 0 AND 1000');

-- 2단계: 유효 데이터를 1분 집계
EXEC STREAM_CREATE('stream_step2',
  'INSERT INTO valid_summary
   SELECT DATE_TRUNC(''minute'', time), sensor_id, AVG(value)
   FROM   valid_log
   GROUP BY 1, sensor_id
   BY 60 SECOND');

EXEC STREAM_START('stream_step1');
EXEC STREAM_START('stream_step2');
```

## 운영 체크

```sql
-- 모든 STREAM 상태 점검
SELECT NAME, STATE, LAST_EX_TIME,
       CASE WHEN ERROR_MSG IS NOT NULL THEN '오류: ' || ERROR_MSG ELSE '정상' END AS status
FROM   V$STREAMS
ORDER BY NAME;
```
