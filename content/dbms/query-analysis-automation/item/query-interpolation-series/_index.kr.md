---
type: docs
title: 'SERIES BY와 보간'
weight: 60
---

Machbase Neo는 시계열 데이터 분석에 특화된 두 가지 기능을 제공합니다. `SERIES BY`는 특정 조건을 만족하는 연속적인 행의 시퀀스를 식별하고, `INTERPOLATION` 힌트는 시간 간격 사이의 빠진 데이터를 채워 연속적인 시계열을 구성합니다.

## SERIES BY

### 개요

`SERIES BY`는 지정한 조건을 **연속적으로** 만족하는 행들의 묶음(시리즈)을 추출합니다. 조건이 중단되면 시리즈가 끊기고, 이후 다시 조건이 만족되면 새로운 시리즈가 시작됩니다.

### 문법

```sql
SELECT [SERIESNUM(),] 컬럼, ...
FROM 테이블
WHERE 조건
SERIES BY 시리즈_조건;
```

- `SERIESNUM()`: 현재 행이 속한 시리즈 번호를 반환하는 함수입니다 (1부터 시작).
- `시리즈_조건`: 시리즈를 구성하는 컬럼 또는 표현식을 지정합니다.

### 예시: 연속 고온 이벤트 탐지

온도가 80도 이상인 측정값이 **연속으로** 이어지는 구간을 시리즈로 식별합니다.

```sql
SELECT
    SERIESNUM() AS series_num,
    time,
    sensor_id,
    temperature
FROM temperature_log
WHERE temperature >= 80
SERIES BY sensor_id;
```

이 쿼리는 `sensor_id`가 동일하고 `temperature >= 80` 조건을 연속으로 만족하는 행들을 하나의 시리즈로 묶어 반환합니다.

### 예시: 연속 알람 상태 구간 찾기

```sql
SELECT
    SERIESNUM() AS series_no,
    MIN(time)   AS series_start,
    MAX(time)   AS series_end,
    COUNT(*)    AS event_count
FROM (
    SELECT
        SERIESNUM() AS sn,
        time,
        alarm_flag
    FROM equipment_log
    WHERE alarm_flag = 1
    SERIES BY equipment_id
)
GROUP BY sn
ORDER BY series_no;
```

> **활용 팁**: `SERIES BY`는 알람 발생 구간, 특정 임계값 초과 구간, 장비 가동 상태 등 연속성이 중요한 분석에 적합합니다.

---

## INTERPOLATION (보간)

### 개요

실제 측정 데이터에는 네트워크 장애, 센서 오류 등으로 인해 특정 시간대의 데이터가 누락될 수 있습니다. `INTERPOLATION` 쿼리 힌트는 지정한 시간 간격 내에 데이터가 없는 구간을 수학적 방법으로 채워 연속적인 시계열 데이터를 반환합니다.

### 힌트 문법

```sql
SELECT /*+ INTERPOLATION(컬럼 보간방법 간격) */
    time, 컬럼, ...
FROM 테이블
WHERE time BETWEEN 시작시간 AND 종료시간;
```

### 보간 방법

| 방법 | 설명 |
|------|------|
| `LINEAR` | 앞뒤 값을 이용한 선형 보간. 값이 균일하게 변화한다고 가정할 때 사용 |
| `PREV` | 이전 유효 값으로 채움(전방 채움, Forward Fill). 상태값이나 마지막 측정값을 유지할 때 사용 |
| `NULL` | 누락된 구간을 `NULL`로 채움 |

### 예시: 1분 간격 선형 보간

센서 데이터에서 1분(60,000,000,000 나노초) 간격으로 빠진 값을 선형 보간으로 채웁니다.

```sql
SELECT /*+ INTERPOLATION(value LINEAR 60000000000) */
    time,
    sensor_id,
    value
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01 00:00:00') AND TO_DATE('2024-01-01 01:00:00')
  AND sensor_id = 'TEMP_001';
```

> **시간 단위**: Machbase의 시간 간격은 나노초(ns) 단위입니다. 자주 사용하는 단위 변환은 다음을 참고하세요.
> - 1초 = 1,000,000,000 ns
> - 1분 = 60,000,000,000 ns
> - 1시간 = 3,600,000,000,000 ns

### 예시: 이전 값으로 채우기 (PREV)

상태 코드처럼 마지막 상태를 유지해야 하는 경우에 사용합니다.

```sql
SELECT /*+ INTERPOLATION(status_code PREV 60000000000) */
    time,
    device_id,
    status_code
FROM device_status
WHERE time BETWEEN TO_DATE('2024-06-01 00:00:00') AND TO_DATE('2024-06-01 06:00:00')
  AND device_id = 'DEVICE_A';
```

### 예시: TAG 테이블에서 보간

TAG 테이블과 함께 `INTERPOLATION`을 사용할 때는 시간 범위 조건(`BETWEEN`)과 태그 이름 조건을 함께 지정합니다.

```sql
SELECT /*+ INTERPOLATION(value LINEAR 300000000000) */
    time,
    name,
    value
FROM tag
WHERE name = 'plant1.sensor.temp'
  AND time BETWEEN TO_DATE('2024-01-01 00:00:00') AND TO_DATE('2024-01-02 00:00:00');
```

> **주의**: `INTERPOLATION` 힌트는 시간 범위 조건이 명시된 쿼리에서 동작합니다. 시간 범위 없이 사용하면 전체 데이터를 대상으로 하여 성능에 영향을 줄 수 있습니다.

---

## SERIES BY와 INTERPOLATION 비교

| 구분 | SERIES BY | INTERPOLATION |
|------|-----------|---------------|
| 목적 | 연속 조건을 만족하는 행 그룹 식별 | 누락된 시간대 데이터 채우기 |
| 동작 방식 | 조건 불만족 시 시리즈 분리 | 지정 간격마다 가상의 행 생성 |
| 출력 행 수 | 원본 행 수와 동일 또는 이하 | 원본보다 많을 수 있음 (보간 행 추가) |
| 주요 용도 | 이벤트 구간 분석, 연속 상태 감지 | 시계열 시각화, 균일 간격 데이터 필요 시 |
