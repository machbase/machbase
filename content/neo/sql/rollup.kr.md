---
title: 롤업
type: docs
weight: 11
---

## 소개

대규모 시계열 데이터에서 통계 값을 조회하면 범위가 넓어질수록 계산 비용이 급격히 증가합니다. 긴 시간 범위나 전체 데이터를 대상으로 집계하면 계산량이 많고 시간도 오래 걸립니다. Machbase는 TAG 테이블에 저장된 데이터를 미리 시간 구간별로 집계하여 빠르게 조회할 수 있는 **Rollup** 기능을 제공합니다. 사전에 정의한 주기(downsample)에 따라 데이터를 자동으로 집계해 두기 때문에, 자주 사용하는 통계 값을 즉시 조회할 수 있습니다.

## 핵심 개념

**Rollup 테이블**은 원본 TAG 테이블(또는 다른 Rollup 테이블)을 기반으로 Machbase가 내부적으로 미리 계산해 둔 집계 결과를 저장합니다. 이를 통해 쿼리 시점에 비용이 큰 집계 연산을 반복하지 않아도 됩니다.

### 기본 제공 집계 함수

Rollup 테이블은 다음 표준 집계 함수를 기본으로 지원합니다.

- `MIN()` : 구간 내 최소값
- `MAX()` : 구간 내 최대값
- `SUM()` : 구간 내 합계
- `COUNT()` : 구간 내 데이터 건수
- `AVG()` : 구간 내 평균값
- `SUMSQ()` : 구간 내 값의 제곱 합

### 확장 집계 함수(선택)

Rollup 생성 시 `EXTENSION` 옵션을 지정하면 다음 함수도 사용할 수 있습니다.

- `FIRST()` : 구간 내 첫 번째 값
- `LAST()` : 구간 내 마지막 값

### 시간 단위

Rollup은 다음과 같은 고정된 시간 간격을 기준으로 집계합니다.

- 초(`SEC`)
- 분(`MIN`)
- 시(`HOUR`)

Rollup을 사용하는 쿼리는 이 기본 단위나 그 배수로 집계를 요청할 수 있습니다. 일·주·월·연 같은 더 큰 단위도 내부적으로 적절한 기본 Rollup 테이블에 매핑되어 처리되며, 1일 이상의 간격에는 보통 HOUR 기반 Rollup 테이블이 사용됩니다.

## Rollup 테이블 종류

Machbase는 Rollup 테이블을 생성하고 관리하는 방식으로 다음 두 가지를 제공합니다.

### 기본 Rollup(Default Rollup)

- TAG 테이블 생성 시 `WITH ROLLUP` 절로 자동 생성됩니다.
- 지정한 가장 작은 단위를 기준으로 초/분/시 Rollup 테이블이 함께 생성됩니다. 예) `WITH ROLLUP (MIN)`이면 분·시 Rollup이 생성되고, `WITH ROLLUP` 또는 `WITH ROLLUP (SEC)`이면 초·분·시 Rollup이 생성됩니다.
- 테이블 이름은 원본 TAG 테이블 이름을 바탕으로 `_<원본명>_ROLLUP_SEC` 형태로 자동으로 만들어집니다(예: `_mytag_ROLLUP_SEC`).
- 하나의 TAG 테이블에는 하나의 기본 Rollup 세트만 존재할 수 있습니다.

### 사용자 정의 Rollup(Custom Rollup)

- `CREATE ROLLUP` 문으로 직접 생성합니다.
- 10초, 5분처럼 원하는 간격으로 설정할 수 있습니다.
- 원본으로 TAG 테이블뿐 아니라 다른 Rollup 테이블을 지정할 수 있어 다단계 집계 구조를 만들 수 있습니다.
- 기본 Rollup이 제공하는 단위 외에도 필요한 집계 간격을 유연하게 정의할 수 있습니다.

## Rollup 테이블 생성

### 기본 Rollup 생성

기본 Rollup 테이블은 TAG 테이블을 정의할 때 함께 생성됩니다.

**문법:**

```sql
CREATE TAG TABLE table_name (
    name_column datatype PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column numeric_datatype [SUMMARIZED]
    [, additional_columns...]
)
WITH ROLLUP [ ( SEC | MIN | HOUR ) ] [ EXTENSION ];
```

- `SEC | MIN | HOUR`: 가장 세밀한 단위를 지정합니다. 생략하면 초(`SEC`)가 기본값입니다. 지정한 단위보다 큰 단위의 Rollup도 자동으로 포함됩니다(예: `MIN`을 지정하면 `HOUR`도 포함).
- `EXTENSION`: 선택 키워드이며, 지정하면 `FIRST()`, `LAST()` 함수를 사용할 수 있습니다.

**예시:**

```sql
-- Create SEC, MIN, HOUR Rollups
CREATE TAG TABLE sensor_data (...) WITH ROLLUP;

-- Create MIN, HOUR Rollups
CREATE TAG TABLE hourly_stats (...) WITH ROLLUP (MIN);

-- Create HOUR Rollup only
CREATE TAG TABLE daily_summary (...) WITH ROLLUP (HOUR);

-- Create SEC, MIN, HOUR Rollups with FIRST/LAST support
CREATE TAG TABLE detailed_sensor_data (...) WITH ROLLUP EXTENSION;
```

### 사용자 정의 Rollup 생성

사용자 정의 Rollup 테이블은 전용 DDL 문으로 직접 생성합니다.

**문법:**

```sql
CREATE ROLLUP rollup_name
ON source_table_or_rollup_name ( source_value_column )
INTERVAL interval_value ( SEC | MIN | HOUR )
[ EXTENSION ];
```

- `rollup_name`: 새로 만들 Rollup 테이블의 이름
- `source_table_or_rollup_name`: 원본 TAG 테이블 또는 기존 Rollup 테이블의 이름
- `source_value_column`: 원본 테이블에서 집계할 숫자형 컬럼. 원본이 Rollup 테이블이면 생략합니다.
- `interval_value`: 집계 간격 숫자(예: 10, 30)
- `SEC | MIN | HOUR`: 집계 간격의 시간 단위
- `EXTENSION`: 선택 키워드이며, 지정하면 `FIRST()`, `LAST()` 함수를 사용할 수 있습니다.

**주의 사항:**

- 원본은 TAG 테이블 또는 다른 Rollup 테이블이어야 합니다.
- 원본이 Rollup 테이블일 때는 새 `INTERVAL`이 원본 Rollup 간격의 배수이면서 더 큰 단위여야 합니다.

**예시:**

```sql
-- Create a 30-second Rollup based on the 'tag_data' table's 'value' column
CREATE ROLLUP _tag_data_rollup_30sec ON tag_data(value) INTERVAL 30 SEC;

-- Create a 10-minute Rollup based on the previously created 30-second Rollup
CREATE ROLLUP _tag_data_rollup_10min ON _tag_data_rollup_30sec INTERVAL 10 MIN;

-- Create a 15-minute Rollup with FIRST/LAST support
CREATE ROLLUP _tag_data_rollup_15min_ext ON tag_data(value) INTERVAL 15 MIN EXTENSION;
```

## Rollup 데이터 조회

사전 집계된 데이터로 성능 이점을 얻으려면 쿼리에서 `ROLLUP()` 함수를 사용해야 합니다(더 이상 권장하지 않는 `ROLLUP` 키워드 문법도 있습니다). Machbase는 요청한 간격과 단위에 맞는 Rollup 테이블을 자동으로 선택합니다.

**문법(권장):**

```sql
SELECT
    ROLLUP( time_unit, period, basetime_column [, origin ] ) AS rollup_time,
    AGGREGATE_FUNCTION( value_column ) AS aggregate_result
    [, other_aggregates... ]
FROM
    source_tag_table
WHERE
    [ time_range_predicate ]
    [ AND name_predicate ]
    [ AND other_predicates... ]
GROUP BY
    rollup_time -- Or GROUP BY ROLLUP(...) expression directly
ORDER BY
    rollup_time;
```

시간 단위로 `MIN`, `MAX`를 조회하는 예시는 다음과 같습니다.

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

- `time_unit`(첫 번째 인자): 집계 간격의 단위('sec', 'min', 'hour', 'day', 'week', 'month', 'year' 등)
- `period`(두 번째 인자): `time_unit` 기준 집계 간격의 배수. 사용하는 Rollup 테이블 간격의 유효한 배수여야 합니다.
- `basetime_column`(세 번째 인자): TAG 테이블에서 `BASETIME` 속성을 지정한 DATETIME 컬럼
- `origin`(네 번째 인자, 선택): 시간 구간의 시작 기준 시각을 지정하는 DATETIME 리터럴. 기본값은 `1970-01-01 00:00:00`이며, 주·월·연 단위 구간을 맞출 때 중요합니다.
- `AGGREGATE_FUNCTION`: 지원 집계 함수 중 하나(`MIN`, `MAX`, `AVG`, `SUM`, `COUNT`, `SUMSQ`, `EXTENSION`을 지정한 경우 `FIRST`/`LAST`)

**주의 사항:**

- `ROLLUP()` 함수가 포함된 표현식(또는 그 별칭)을 `GROUP BY`에 반드시 명시해야 합니다.
- `ROLLUP()`을 사용할 때 값 컬럼에는 위의 지원 집계 함수만 적용할 수 있습니다.

**조회 예시:**

```sql
-- Hourly MIN and MAX values for TAG_00001 within a specific month
SELECT
    ROLLUP('hour', 1, time) as mtime,
    MIN(value),
    MAX(value)
FROM TAG
WHERE name = 'TAG_00001'
  AND time BETWEEN TO_DATE('2023-01-01 00:00:00') AND TO_DATE('2023-01-31 23:59:59')
GROUP BY mtime
ORDER BY mtime;

-- 15-minute average values, assuming a MIN or SEC level Rollup exists
SELECT
    ROLLUP('min', 15, time) AS rollup_interval,
    AVG(value)
FROM TAG
WHERE name = 'SENSOR_A'
GROUP BY rollup_interval
ORDER BY rollup_interval;

-- Daily FIRST and LAST values using Extension Rollup, aligning bins to Jan 1st, 2024
SELECT
    ROLLUP('day', 1, time, '2024-01-01') as day_interval,
    FIRST(time, value),
    LAST(time, value)
FROM TAG_WITH_EXTENSION
WHERE name = 'SENSOR_B'
GROUP BY day_interval
ORDER BY day_interval;

-- Weekly average, aligned to Mondays (assuming '2024-01-01' was a Monday)
SELECT
    ROLLUP('week', 1, time, '2024-01-01') AS week_start,
    AVG(value)
FROM TAG
WHERE name = 'SENSOR_C'
GROUP BY week_start
ORDER BY week_start;
```

## Rollup 관리

### 실행 제어

Rollup 스레드가 수행하는 집계 작업은 수동으로 제어할 수 있습니다.

**명령:**

```sql
-- Start the aggregation thread for a specific Rollup
EXEC ROLLUP_START('rollup_name');

-- Stop the aggregation thread for a specific Rollup
EXEC ROLLUP_STOP('rollup_name');

-- Force immediate aggregation processing for a specific Rollup, bypassing the normal interval wait time
EXEC ROLLUP_FORCE('rollup_name');
```

- `ROLLUP_FORCE`는 대기 시간을 무시하고 즉시 집계를 수행합니다.

**예시:**

```sql
EXEC ROLLUP_START('_tag_data_rollup_30sec');
EXEC ROLLUP_STOP('_tag_data_rollup_10min');
EXEC ROLLUP_FORCE('_tag_rollup_hour'); -- Process pending data for the hourly rollup now
```

### Rollup 데이터 삭제

원본 TAG 테이블에서 데이터를 삭제해도 Rollup 테이블의 집계 데이터는 자동으로 삭제되지 **않습니다**. Rollup 데이터는 별도로 삭제해야 합니다.

**문법:**

```sql
-- Delete all Rollup data for the specified table
DELETE FROM table_name ROLLUP;

-- Delete Rollup data before a specific timestamp for the specified table
DELETE FROM table_name ROLLUP BEFORE TO_DATE('YYYY-MM-DD HH24:MI:SS');

-- Delete all Rollup data for a specific tag within the table
DELETE FROM table_name ROLLUP WHERE name = 'specific_tag_id';

-- Delete Rollup data for a specific tag before a specific timestamp
DELETE FROM table_name ROLLUP WHERE name = 'specific_tag_id' AND time <= TO_DATE('YYYY-MM-DD HH24:MI:SS');
```

**예시:**

```sql
-- Remove all Rollup data associated with the 'TAG' table older than Jan 15, 2024
DELETE FROM TAG ROLLUP BEFORE TO_DATE('2024-01-15 00:00:00');

-- Remove all Rollup data for 'TAG01' from the 'TAG' table
DELETE FROM TAG ROLLUP WHERE name = 'TAG01';
```

### Rollup 테이블 삭제

사용자 정의 Rollup 테이블은 개별적으로 삭제할 수 있습니다. 기본 Rollup 테이블은 보통 원본 TAG 테이블을 삭제할 때 함께 삭제됩니다.

**문법:**

```sql
-- Drop a specific Custom Rollup table
DROP ROLLUP rollup_name;

-- Drop a TAG table and all its dependent Rollup tables (Default and Custom)
DROP TABLE tag_table_name CASCADE;
```

**주의 사항:** 다른 Rollup이 의존하는 Rollup 테이블은 삭제할 수 없습니다. 의존하는 하위 Rollup을 먼저(생성의 역순으로) 삭제해야 합니다.

**예시:**

```sql
-- Assuming _rollup_min depends on _rollup_sec
DROP ROLLUP _rollup_min;
DROP ROLLUP _rollup_sec;

-- Drop the 'sensor_data' TAG table and all associated Rollups
DROP TABLE sensor_data CASCADE;
```

## Rollup Gap

**Rollup Gap**은 TAG 테이블에 최신 데이터가 들어온 시점과 Rollup 테이블에 반영된 시점의 차이를 의미합니다. 주기적으로 집계하므로 작은 차이는 생길 수밖에 없지만, 차이가 크거나 계속 커진다면 성능 병목이 발생하고 있을 수 있습니다.

### Rollup Gap 확인

현재 Rollup 처리 상태와 Gap 발생 여부를 확인할 수 있습니다.

**명령:**

```sql
SHOW ROLLUPGAP;
```

이 명령은 동작 중인 각 Rollup의 정보와 Gap에 해당하는 처리 대기 데이터 건수를 보여 줍니다. `GAP` 값이 0이면 최신 상태입니다.

### Rollup Gap 해소

Gap이 크게 벌어지면 다음 조치를 고려합니다.

1. **즉시 집계:** `EXEC ROLLUP_FORCE('rollup_name');`으로 특정 Rollup의 대기 데이터를 즉시 집계합니다.
2. **병렬 처리 확대:** 원본 TAG 테이블의 `TAG_PARTITION_COUNT` 속성을 늘립니다. 더 많은 Rollup 스레드가 병렬로 동작할 수 있지만 메모리 사용량이 증가하므로 주의해야 합니다.
3. **하드웨어 자원:** CPU 속도와 코어 수, 디스크 I/O 성능을 높입니다.
4. **입력 속도 관리:** 데이터 입력 속도가 계속 시스템의 처리 용량을 넘는다면 입력 속도를 조절하거나 하드웨어를 더 확장합니다.

Gap이 계속 해소되지 않는다면 데이터 적재와 Rollup 집계를 함께 처리하기에 시스템 자원이 부족한 경우가 많습니다.

## 제약 사항

Rollup 기능은 강력하지만 다음과 같은 제약이 있습니다.

- **고정된 집계 함수:** 지원 집계 함수(`MIN`, `MAX`, `AVG`, `SUM`, `COUNT`, `SUMSQ`, 선택적으로 `FIRST`/`LAST`)는 고정되어 있으며 사용자 정의 집계는 제공하지 않습니다. 별도의 집계 로직이 필요하면 다른 방법을 사용해야 합니다.
- **원본 데이터 품질:** Rollup은 원본 데이터에 의존하므로 원본 TAG 테이블에 들어간 잘못된 값이나 이상값도 집계 결과에 그대로 반영됩니다. 이상값 제거 등 품질 관리는 적재 전이나 적재 중에 수행해야 합니다.
- **자원 사용:** Rollup 처리는 원본을 읽고 Rollup 테이블에 쓰는 과정에서 CPU와 I/O를 사용합니다. 고속 적재 환경에서는 자원 경합이 생길 수 있으며, 자원이 부족하면 Rollup Gap이 커질 수 있습니다.
- **지연:** TAG 테이블에 데이터가 들어온 뒤 Rollup 테이블에 반영되기까지 집계 간격과 처리 시간만큼의 지연(Rollup Gap)이 있습니다. 실시간성이 매우 중요하거나 집계 값에 마이크로초 단위의 정밀도가 필요하다면 원본 TAG 데이터를 직접 조회하는 것이 더 적합할 수 있습니다.

## 예제

Rollup 테이블의 생성, 관리, 조회 방법을 실제 예제로 살펴봅니다.

### 예제 1: 기본 Rollup 생성 및 조회

기본 Rollup 테이블(SEC, MIN, HOUR)을 사용하는 TAG 테이블을 만들고 시간 단위 집계 값을 조회합니다.

```sql
-- 1. Create a TAG table with default Rollups enabled
CREATE TAG TABLE iot_sensors (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED -- SUMMARIZED required for Rollup on this column
)
WITH ROLLUP; -- Creates _iot_sensors_ROLLUP_SEC, _iot_sensors_ROLLUP_MIN, _iot_sensors_ROLLUP_HOUR

-- 2. Insert some sample data
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:05:15', 20.1);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:15:30', 20.5);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 10:55:00', 21.0);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 11:05:00', 21.5);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-10 11:35:45', 21.8);
INSERT INTO iot_sensors VALUES ('TEMP_B', '2024-03-10 10:10:00', 15.0);
INSERT INTO iot_sensors VALUES ('TEMP_B', '2024-03-10 11:10:00', 16.0);

-- Wait briefly for Rollup process or force it (optional)
-- EXEC ROLLUP_FORCE('_iot_sensors_ROLLUP_SEC');
-- EXEC ROLLUP_FORCE('_iot_sensors_ROLLUP_MIN');
-- EXEC ROLLUP_FORCE('_iot_sensors_ROLLUP_HOUR');

-- 3. Query the average hourly temperature for sensor TEMP_A
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    AVG(temperature) AS avg_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time BETWEEN TO_DATE('2024-03-10 10:00:00') AND TO_DATE('2024-03-10 12:00:00')
GROUP BY
    hour_interval
ORDER BY
    hour_interval;

/* Expected Approximate Output:
hour_interval                   avg_temp
---------------------------------------------------------------
2024-03-10 10:00:00 000:000:000 20.533...  -- Avg of 20.1, 20.5, 21.0
2024-03-10 11:00:00 000:000:000 21.65      -- Avg of 21.5, 21.8
*/
```

### 예제 2: 사용자 정의 Rollup 생성 및 조회

15분마다 데이터를 집계하는 사용자 정의 Rollup 테이블을 만듭니다.

```sql
-- Prerequisite: Assume iot_sensors table exists from Example 1

-- 1. Create a custom 15-minute Rollup table based on the 'temperature' column
CREATE ROLLUP _iot_sensors_rollup_15min
ON iot_sensors (temperature)
INTERVAL 15 MIN;

-- Wait or force Rollup processing (optional)
-- EXEC ROLLUP_FORCE('_iot_sensors_rollup_15min');

-- 2. Query MIN and MAX temperature aggregated over 15-minute intervals for TEMP_A
SELECT
    ROLLUP('min', 15, event_time) AS interval_15min,
    MIN(temperature) AS min_temp,
    MAX(temperature) AS max_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time BETWEEN TO_DATE('2024-03-10 10:00:00') AND TO_DATE('2024-03-10 12:00:00')
GROUP BY
    interval_15min
ORDER BY
    interval_15min;

/* Expected Approximate Output:
interval_15min                  min_temp    max_temp
---------------------------------------------------------------
2024-03-10 10:00:00 000:000:000 20.1        20.1        -- 10:00 to 10:14:59
2024-03-10 10:15:00 000:000:000 20.5        20.5        -- 10:15 to 10:29:59
2024-03-10 10:45:00 000:000:000 21.0        21.0        -- 10:45 to 10:59:59 (data at 10:55)
2024-03-10 11:00:00 000:000:000 21.5        21.5        -- 11:00 to 11:14:59
2024-03-10 11:30:00 000:000:000 21.8        21.8        -- 11:30 to 11:44:59
*/
```

### 예제 3: 확장 Rollup 조회(FIRST/LAST)

확장 Rollup을 사용해 구간 내 첫 번째 값과 마지막 값을 조회합니다.

```sql
-- 1. Create a TAG table with default Rollups and EXTENSION
DROP TABLE IF EXISTS iot_sensors_ext CASCADE; -- Clean up if exists
CREATE TAG TABLE iot_sensors_ext (
    sensor_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    pressure DOUBLE SUMMARIZED
)
WITH ROLLUP EXTENSION; -- Enable FIRST() and LAST()

-- 2. Insert sample data
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:01:00', 1000.1);
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:05:00', 1000.5); -- In 09:00 interval (the first value is 1000.1 at 09:01)
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 09:55:00', 1001.0); -- Last in 09:00 interval
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:02:00', 1001.2); -- First in 10:00 interval
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:08:00', 1001.5);
INSERT INTO iot_sensors_ext VALUES ('PRES_1', '2024-03-10 10:40:00', 1001.8); -- Last in 10:00 interval

-- Wait or force Rollup processing (optional)
-- EXEC ROLLUP_FORCE('_iot_sensors_ext_ROLLUP_SEC'); ... etc.

-- 3. Query the first and last pressure readings per hour for PRES_1
SELECT
    ROLLUP('hour', 1, event_time) AS hour_interval,
    FIRST(event_time, pressure) AS first_pressure,
    LAST(event_time, pressure) AS last_pressure
FROM
    iot_sensors_ext
WHERE
    sensor_id = 'PRES_1'
GROUP BY
    hour_interval
ORDER BY
    hour_interval;

/* Expected Approximate Output:
hour_interval                   first_pressure last_pressure
----------------------------------------------------------------------
2024-03-10 09:00:00 000:000:000 1000.1         1001.0
2024-03-10 10:00:00 000:000:000 1001.2         1001.8
*/
```

### 예제 4: 일·주 단위 조회

`iot_sensors` 테이블에 여러 날·여러 주에 걸친 데이터가 있다고 가정하고 일간 평균과 주간 평균을 조회합니다.

```sql
-- Assume 'iot_sensors' table has data for TEMP_A from 2024-03-01 to 2024-03-15

-- 1. Query Daily Average Temperature for TEMP_A
SELECT
    ROLLUP('day', 1, event_time) AS day_interval,
    AVG(temperature) AS avg_daily_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-01') AND event_time < TO_DATE('2024-03-16')
GROUP BY
    day_interval
ORDER BY
    day_interval;

-- 2. Query Weekly Average Temperature for TEMP_A, aligning weeks starting on Monday ('2024-03-04')
SELECT
    ROLLUP('week', 1, event_time, '2024-03-04') AS week_start_monday, -- Specify origin for week alignment
    AVG(temperature) AS avg_weekly_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-03-01') AND event_time < TO_DATE('2024-03-16')
GROUP BY
    week_start_monday
ORDER BY
    week_start_monday;
```

### 예제 5: 월 단위 Rollup 조회

Rollup 기능으로 데이터를 월 단위로 집계합니다. 월 단위 집계는 보통 HOUR 단위 Rollup 테이블을 사용해 효율적으로 계산합니다.

```sql
-- Assume the 'iot_sensors' table (from Example 1) has data spanning several months,
-- for example, from January 2024 to April 2024 for sensor 'TEMP_A'.
-- Ensure data exists for multiple months to see aggregation.
-- Example Data (add more if needed):
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-01-15 12:00:00', 18.0);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-01-25 14:00:00', 18.5);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-02-10 08:00:00', 19.0);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-02-20 09:00:00', 19.2);
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-05 10:00:00', 19.5); -- Use data from previous examples too
INSERT INTO iot_sensors VALUES ('TEMP_A', '2024-03-20 11:00:00', 20.0);

-- 1. Query the Average Monthly Temperature for TEMP_A
-- The origin defaults to '1970-01-01', which works for standard calendar months.
SELECT
    ROLLUP('month', 1, event_time) AS month_interval, -- Aggregate data for each calendar month
    AVG(temperature) AS avg_monthly_temp,
    COUNT(temperature) AS data_points_per_month
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    month_interval
ORDER BY
    month_interval;

/* Expected Approximate Output (values depend heavily on exact data):
month_interval                  avg_monthly_temp data_points_per_month
--------------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 18.25            2
2024-02-01 00:00:00 000:000:000 19.1             2
2024-03-01 00:00:00 000:000:000 20.628571...     7 -- (Including data from Example 1)
*/

-- 2. Query Quarterly (3-Month) SUM and COUNT for TEMP_A
-- Using period=3 with 'month' unit
SELECT
    ROLLUP('month', 3, event_time) AS quarter_interval, -- Aggregate data over 3-month periods
    SUM(temperature) AS sum_quarterly_temp,
    COUNT(temperature) AS data_points_per_quarter
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    quarter_interval
ORDER BY
    quarter_interval;

/* Expected Approximate Output:
quarter_interval                sum_quarterly_temp data_points_per_quarter
----------------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 219.1              11 -- Sum/Count for Jan, Feb, Mar combined
*/

-- 3. Explicitly setting Origin (Optional, useful if non-standard month alignment needed)
-- Note: If setting origin for 'month', it MUST be the first day of some month.
SELECT
    ROLLUP('month', 1, event_time, '2024-01-01') AS month_interval, -- Origin explicitly set
    MIN(temperature) AS min_monthly_temp,
    MAX(temperature) AS max_monthly_temp
FROM
    iot_sensors
WHERE
    sensor_id = 'TEMP_A'
    AND event_time >= TO_DATE('2024-01-01') AND event_time < TO_DATE('2024-04-01')
GROUP BY
    month_interval
ORDER BY
    month_interval;

/* Expected Approximate Output:
month_interval                  min_monthly_temp max_monthly_temp
--------------------------------------------------------------------
2024-01-01 00:00:00 000:000:000 18.0             18.5
2024-02-01 00:00:00 000:000:000 19.0             19.2
2024-03-01 00:00:00 000:000:000 19.5             21.8 -- (Including data from Example 1)
*/
```

### 예제 6: Rollup 관리 명령

Rollup 상태 확인, 즉시 집계, 오래된 Rollup 데이터 삭제, Rollup이 있는 테이블 삭제 방법을 보여 줍니다.

```sql
-- 1. Check the current Rollup gap status for all Rollups
SHOW ROLLUPGAP;

-- 2. Force immediate processing for a specific custom Rollup
-- EXEC ROLLUP_FORCE('_iot_sensors_rollup_15min');

-- 3. Delete Rollup data older than March 1st, 2024 from the iot_sensors table's Rollups
DELETE FROM iot_sensors ROLLUP BEFORE TO_DATE('2024-03-01 00:00:00');

-- 4. Drop the iot_sensors_ext table and all its associated Rollup tables
DROP TABLE iot_sensors_ext CASCADE;
```

위 예제와 같이 Rollup 기능을 활용하면 방대한 시계열 데이터를 다양한 분석 단위로 빠르게 조회할 수 있습니다. 업무 요구에 맞춰 기본 Rollup과 사용자 정의 Rollup을 적절히 조합하여 사용하십시오.
