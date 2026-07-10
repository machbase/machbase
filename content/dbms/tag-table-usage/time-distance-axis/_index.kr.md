---
title: '5.11 시간축과 거리축 TAG'
weight: 110
toc: true
---


<a id="time-axis-design-tag"></a>

## 시간축 TAG 테이블 설계

시간축 TAG 테이블은 `BASETIME` 키워드를 사용하여 시간을 기준 축으로 삼는 시계열 테이블입니다.

### 최소 구성

TAG 테이블은 다음 세 가지 컬럼이 필수입니다.

| 컬럼 역할 | 타입 | 키워드 | 설명 |
|---------|------|--------|------|
| 태그 식별자 | `VARCHAR(n)` | `PRIMARY KEY` | 센서 이름 등 |
| 시간 | `DATETIME` | `BASETIME` | 시간축, 나노초 정밀도 |
| 값 | 숫자형 등 | — | 계측값 |

```sql
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);
```

### 다중 값 컬럼

하나의 TAG 테이블에 여러 계측값을 함께 저장할 수 있습니다.

```sql
CREATE TAG TABLE env_sensor (
    name        VARCHAR(64) PRIMARY KEY,
    time        DATETIME    BASETIME,
    temperature DOUBLE,
    humidity    DOUBLE,
    pressure    DOUBLE
);
```

### 데이터 삽입

```sql
-- 단건 INSERT
INSERT INTO sensor_data VALUES ('sensor-01', '2024-01-01 00:00:00', 23.5);

-- APPEND API (고속 대량 입력)
-- SDK에서 Append() 함수 사용
```

### 조회

```sql
-- 최근 1시간 데이터 조회
SELECT name, time, value
FROM sensor_data
WHERE name = 'sensor-01'
  AND time >= NOW - 3600000000000
ORDER BY time DESC;

-- 여러 태그 조회
SELECT name, time, value
FROM sensor_data
WHERE name IN ('sensor-01', 'sensor-02')
  AND time BETWEEN '2024-01-01' AND '2024-01-02';
```

### 시간 단위

`DATETIME` 컬럼에 나노초 정밀도로 값을 저장합니다. NOW 함수는 현재 시각을 나노초로 반환합니다.

| 단위 | 나노초 값 |
|------|---------|
| 1초 | 1,000,000,000 |
| 1분 | 60,000,000,000 |
| 1시간 | 3,600,000,000,000 |
| 1일 | 86,400,000,000,000 |

<a id="distance-axis-design-tag"></a>

## 거리축 TAG 테이블 설계

거리축 TAG 테이블은 시간 대신 거리(위치)를 기준 축으로 사용합니다. 파이프라인 검사, 도로 센서, 레이더 등 위치 기반 데이터에 적합합니다.

### 구성

`BASETIME` 대신 `BASEDISTANCE` 키워드를 사용합니다.

```sql
CREATE TAG TABLE pipeline_inspection (
    name      VARCHAR(64) PRIMARY KEY,
    distance  DOUBLE      BASEDISTANCE,
    thickness DOUBLE,
    defect    SHORT
);
```

| 컬럼 역할 | 타입 | 키워드 |
|---------|------|--------|
| 태그 식별자 | `VARCHAR(n)` | `PRIMARY KEY` |
| 거리 | `DOUBLE` | `BASEDISTANCE` |
| 값 | 숫자형 등 | — |

### 사용 예시

```sql
-- 0~100m 구간 데이터 조회
SELECT name, distance, thickness
FROM pipeline_inspection
WHERE name = 'pipe-01'
  AND distance BETWEEN 0.0 AND 100.0
ORDER BY distance;

-- 특정 지점 근방 데이터
SELECT name, distance, defect
FROM pipeline_inspection
WHERE name = 'pipe-01'
  AND distance >= 50.0 AND distance <= 50.5;
```

### 시간축과의 차이

| 항목 | 시간축 (`BASETIME`) | 거리축 (`BASEDISTANCE`) |
|------|---------------------|------------------------|
| 축 타입 | `DATETIME` | `DOUBLE` |
| 단위 | 나노초 시각 | 미터, 킬로미터 등 임의 단위 |
| 정렬 | 시간 순서 | 거리 순서 |
| 주요 쿼리 | 시간 범위 | 거리 범위 |

### 주의사항

- `BASEDISTANCE` 컬럼은 `DOUBLE` 타입만 사용 가능합니다.
- 하나의 TAG 테이블에 `BASETIME`과 `BASEDISTANCE`를 동시에 지정할 수 없습니다.

<a id="distance-axis-query-range"></a>

## 거리축 범위 조회

거리축(BASE DISTANCE) TAG 테이블은 시간이 아닌 거리(위치) 기준으로 데이터를 조회합니다.

### 거리축 TAG 테이블

거리축 TAG 테이블은 `BASE DISTANCE` 컬럼을 사용하여 위치 기반 데이터를 저장합니다.

```sql
CREATE TAG TABLE position_sensor (
    name     VARCHAR(20) PRIMARY KEY,
    distance DOUBLE BASE DISTANCE,
    value    DOUBLE,
    quality  INT
);
```

### 거리 범위 조회

거리축 테이블은 시간 조건 대신 거리 조건으로 범위를 지정합니다.

```sql
-- 거리 0 ~ 100 범위의 데이터
SELECT name, distance, value
FROM position_sensor
WHERE distance BETWEEN 0 AND 100;

-- 특정 태그의 거리 범위
SELECT name, distance, value
FROM position_sensor
WHERE name = 'SENSOR-A'
  AND distance >= 50 AND distance <= 200;

-- 특정 거리 이후 데이터
SELECT name, distance, value
FROM position_sensor
WHERE distance > 500
ORDER BY name, distance;
```

### 거리별 집계

```sql
-- 100m 구간별 평균
SELECT name,
       FLOOR(distance / 100) * 100 AS seg_start,
       AVG(value) AS avg_val
FROM position_sensor
GROUP BY name, seg_start
ORDER BY name, seg_start;
```

### 거리축과 시간축 비교

| 항목 | 시간축 (BASETIME) | 거리축 (BASEDISTANCE) |
|------|----------------|-------------------|
| 기준 컬럼 타입 | DATETIME | DOUBLE, LONG, ULONG |
| DURATION 키워드 | O | X |
| 범위 조회 | WHERE time BETWEEN ... | WHERE distance BETWEEN ... |
| 대표 사용처 | 시계열 센서 데이터 | 위치·거리 기반 측정 데이터 |
| ROLLUP 지원 | O (WITH ROLLUP) | X |

> 거리축 테이블에는 `WITH ROLLUP`을 사용할 수 없습니다. ROLLUP은 시간축 TAG 테이블 전용입니다.
