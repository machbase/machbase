---
title: 롤업
type: docs
weight: 11
---

## 소개

대규모 시계열 데이터에서 통계 값을 조회하면 범위가 넓어질수록 계산 비용이 급격히 증가합니다. Machbase는 TAG 테이블에 저장된 데이터를 미리 시간 구간별로 집계하여 빠르게 조회할 수 있는 **Rollup** 기능을 제공합니다. 사전에 정의한 주기(downsample)에 따라 데이터를 자동으로 집계해 두기 때문에, 자주 사용하는 통계 값을 즉시 조회할 수 있습니다.

## 핵심 개념

**Rollup 테이블**은 원본 TAG 테이블(또는 다른 Rollup 테이블)을 기반으로 Machbase가 내부적으로 미리 계산해 둔 집계 결과를 저장합니다. 이를 통해 쿼리 시점에 비용이 큰 집계 연산을 반복하지 않아도 됩니다.

### 기본 제공 집계 함수

- `MIN()` : 구간 내 최소값
- `MAX()` : 구간 내 최대값
- `SUM()` : 구간 내 합계
- `COUNT()` : 구간 내 데이터 건수
- `AVG()` : 구간 내 평균값
- `SUMSQ()` : 값의 제곱 합

### 확장 집계 함수(선택)

Rollup 생성 시 `EXTENSION` 옵션을 지정하면 다음 함수도 사용할 수 있습니다.

- `FIRST()` : 구간 내 첫 번째 값
- `LAST()` : 구간 내 마지막 값

### 시간 단위

Rollup은 고정된 시간 간격으로 동작하며 기본 단위는 초(SEC), 분(MIN), 시(HOUR)입니다. 일·주·월·연 같은 더 큰 단위 역시 내부적으로 적절한 기본 단위(HOUR 등)에 매핑되어 처리됩니다.

## Rollup 테이블 종류

### 기본 Rollup(Default Rollup)

- TAG 테이블 생성 시 `WITH ROLLUP` 절로 자동 생성됩니다.
- 가장 작은 단위를 기준으로 초/분/시 테이블이 함께 생성됩니다. 예) `WITH ROLLUP (MIN)`이면 분·시 Rollup이 생성됩니다.
- 테이블 이름은 자동으로 `_<원본명>_ROLLUP_SEC` 형태로 만들어집니다.
- 하나의 TAG 테이블에는 하나의 기본 Rollup 세트만 존재할 수 있습니다.

### 사용자 정의 Rollup(Custom Rollup)

- `CREATE ROLLUP` 문으로 직접 생성합니다.
- 10초, 5분처럼 원하는 간격으로 설정할 수 있습니다.
- 원본으로 TAG 테이블뿐 아니라 다른 Rollup 테이블을 지정할 수 있어 다단계 집계 구조를 만들 수 있습니다.

## Rollup 테이블 생성

### 기본 Rollup 생성

```sql
CREATE TAG TABLE table_name (
    name_column datatype PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column numeric_datatype [SUMMARIZED],
    ...
)
WITH ROLLUP [ ( SEC | MIN | HOUR ) ] [ EXTENSION ];
```

- 괄호 안에 가장 세밀한 단위를 지정합니다. 생략하면 초(SEC)가 기본값입니다.
- `EXTENSION`을 붙이면 `FIRST()`, `LAST()` 함수 사용이 가능합니다.

예시:

```sql
-- 초/분/시 Rollup 생성
CREATE TAG TABLE sensor_data (...) WITH ROLLUP;

-- 분/시 Rollup 생성
CREATE TAG TABLE hourly_stats (...) WITH ROLLUP (MIN);

-- 시 Rollup만 생성
CREATE TAG TABLE daily_summary (...) WITH ROLLUP (HOUR);

-- 확장 함수 지원 포함
CREATE TAG TABLE detailed_sensor_data (...) WITH ROLLUP EXTENSION;
```

### 사용자 정의 Rollup 생성

```sql
CREATE ROLLUP rollup_name
ON source_table_or_rollup ( value_column )
INTERVAL interval_value ( SEC | MIN | HOUR )
[ EXTENSION ];
```

- `source_table_or_rollup`: 원본 TAG 테이블 또는 기존 Rollup 테이블
- `value_column`: 원본이 TAG 테이블일 경우 집계할 컬럼을 지정합니다. 원본이 Rollup이면 생략합니다.
- `interval_value`: 집계 간격 숫자
- `EXTENSION`: 확장 함수(FIRST/LAST) 사용 여부

**주의 사항**

- 원본이 Rollup 테이블일 때는 새 간격이 원본 간격의 배수이면서 더 큰 단위여야 합니다.

예시:

```sql
-- 30초 간격 Rollup 생성
CREATE ROLLUP _tag_data_rollup_30sec ON tag_data(value) INTERVAL 30 SEC;

-- 상위 Rollup (10분)
CREATE ROLLUP _tag_data_rollup_10min ON _tag_data_rollup_30sec INTERVAL 10 MIN;

-- 15분 간격 + 확장
CREATE ROLLUP _tag_data_rollup_15min_ext ON tag_data(value) INTERVAL 15 MIN EXTENSION;
```

## Rollup 데이터 조회

Rollup 테이블을 활용하려면 `ROLLUP()` 함수를 사용합니다. Machbase가 적절한 Rollup 테이블을 자동으로 선택합니다.

```sql
SELECT
    ROLLUP('hour', 1, time) AS rollup_time,
    MIN(value),
    MAX(value)
FROM tag_table
WHERE ...
GROUP BY rollup_time
ORDER BY rollup_time;
```

- 첫 번째 인자: 단위(예: 'sec', 'min', 'hour', 'day', 'week', 'month', 'year' 등)
- 두 번째 인자: 단위의 배수
- 세 번째 인자: `BASETIME` 컬럼
- 네 번째 인자: (선택) 시작 기준 시각(origin)

`ROLLUP()` 함수가 포함된 컬럼은 `GROUP BY`에 반드시 명시되어야 하며, `MIN`, `MAX`, `AVG`, `SUM`, `COUNT`, `SUMSQ`, `FIRST`, `LAST` 등의 집계 함수와 함께 사용합니다.

## Rollup 관리

### 실행 제어

```sql
EXEC ROLLUP_START('rollup_name');
EXEC ROLLUP_STOP('rollup_name');
EXEC ROLLUP_FORCE('rollup_name');
```

- `ROLLUP_FORCE`는 대기 시간을 무시하고 즉시 집계를 수행합니다.

### Rollup 데이터 삭제

```sql
DELETE FROM table_name ROLLUP; -- 전체 삭제
DELETE FROM table_name ROLLUP BEFORE TO_DATE('YYYY-MM-DD HH24:MI:SS');
DELETE FROM table_name ROLLUP WHERE name = 'TAG01';
DELETE FROM table_name ROLLUP WHERE name = 'TAG01' AND time <= TO_DATE(...);
```

원본 TAG 테이블에서 데이터를 삭제해도 Rollup 데이터는 자동으로 삭제되지 않으므로 별도로 정리해야 합니다.

### Rollup 테이블 삭제

```sql
DROP ROLLUP rollup_name;          -- 사용자 정의 Rollup 삭제
DROP TABLE tag_table CASCADE;     -- TAG 테이블과 관련 Rollup 일괄 삭제
```

다른 Rollup이 의존하는 Rollup은 먼저 하위 Rollup을 삭제해야 합니다.

## Rollup Gap

Rollup Gap은 TAG 테이블에 최신 데이터가 들어온 시점과 Rollup 테이블에 반영된 시점의 차이를 의미합니다. 간격이 크면 성능 병목이 발생하고 있음을 의미합니다.

```sql
SHOW ROLLUPGAP;
```

- `GAP` 값이 0이면 최신 상태입니다.
- 간격이 지속적으로 증가하면 아래 조치를 고려합니다.
  1. `EXEC ROLLUP_FORCE`로 즉시 집계
  2. `TAG_PARTITION_COUNT` 증가 (메모리 사용량 증가에 주의)
  3. CPU·디스크 I/O 증설
  4. 입력 속도 조절 또는 하드웨어 확장

## 제약 사항

- 지원 집계 함수는 고정되어 있으며 사용자 정의 집계는 제공하지 않습니다.
- Rollup은 원본 데이터에 의존하므로 이상값 제거 등 품질 관리는 적재 전에 수행해야 합니다.
- 고속 적재 환경에서는 CPU, I/O 사용량이 증가하며, 자원이 부족하면 Rollup Gap이 커질 수 있습니다.
- 실시간성이 매우 높은 경우에는 원본 TAG 데이터를 직접 조회하는 것이 더 적합할 수 있습니다.

## 예제

### 예제 1: 기본 Rollup 생성 및 조회

```sql
CREATE TAG TABLE iot_sensors (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
)
WITH ROLLUP;  -- 초/분/시 Rollup 자동 생성

INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:05:15', 20.1);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:15:30', 20.5);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:55:00', 21.0);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 11:05:00', 21.5);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 11:35:45', 21.8);

SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    AVG(temperature) AS avg_temp
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
  AND event_time BETWEEN TO_DATE('2024-03-10 10:00:00') AND TO_DATE('2024-03-10 12:00:00')
GROUP BY hour_interval
ORDER BY hour_interval;
```

### 예제 2: 사용자 정의 Rollup

```sql
CREATE ROLLUP _iot_sensors_rollup_15min
ON iot_sensors (temperature)
INTERVAL 15 MIN;

SELECT
    ROLLUP('min', 15, event_time) AS interval_15min,
    MIN(temperature),
    MAX(temperature)
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
GROUP BY interval_15min
ORDER BY interval_15min;
```

### 예제 3: 확장 함수(FIRST/LAST) 사용

```sql
CREATE TAG TABLE iot_sensors_ext (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    pressure DOUBLE SUMMARIZED
)
WITH ROLLUP EXTENSION;

INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:05:00', 1000.5);
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:55:00', 1001.0);
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:02:00', 1001.2);
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:40:00', 1001.8);

SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    FIRST(event_time, pressure) AS first_pressure,
    LAST(event_time, pressure) AS last_pressure
FROM iot_sensors_ext
WHERE sensor_id = 'PRES_1'
GROUP BY hour_interval
ORDER BY hour_interval;
```

### 예제 4: 일·주·월 집계

```sql
-- 일간 평균
SELECT
    ROLLUP('day', 1, event_time) AS day_interval,
    AVG(temperature) AS avg_daily_temp
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
  AND event_time BETWEEN TO_DATE('2024-03-01') AND TO_DATE('2024-03-16')
GROUP BY day_interval
ORDER BY day_interval;

-- 주간 평균(주 시작을 월요일로 정렬)
SELECT
    ROLLUP('week', 1, event_time, '2024-03-04') AS week_start,
    AVG(temperature) AS avg_weekly_temp
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
  AND event_time BETWEEN TO_DATE('2024-03-01') AND TO_DATE('2024-03-16')
GROUP BY week_start
ORDER BY week_start;

-- 월간 집계
SELECT
    ROLLUP('month', 1, event_time) AS month_interval,
    AVG(temperature) AS avg_monthly_temp,
    COUNT(*) AS count_per_month
FROM iot_sensors
WHERE sensor_id = 'TEMP_A'
  AND event_time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-04-01')
GROUP BY month_interval
ORDER BY month_interval;
```

### 예제 5: Rollup 관리 명령

```sql
SHOW ROLLUPGAP;
EXEC ROLLUP_FORCE('_iot_sensors_rollup_15min');
DELETE FROM iot_sensors ROLLUP BEFORE TO_DATE('2024-03-01 00:00:00');
DROP TABLE iot_sensors_ext CASCADE;
```

위 예제와 같이 Rollup 기능을 활용하면 방대한 시계열 데이터를 다양한 분석 단위로 빠르게 조회할 수 있습니다. 업무 요구에 맞춰 기본 Rollup과 사용자 정의 Rollup을 적절히 조합하여 사용하십시오.
