---
type: docs
title: 'PARTITION BY / ORDER BY'
weight: 30
---

`OVER` 절의 `PARTITION BY`와 `ORDER BY`는 윈도우 함수가 연산을 수행할 범위와 순서를 정의합니다. 두 절의 조합에 따라 윈도우 함수의 동작이 달라지므로 각각의 역할을 정확히 이해하는 것이 중요합니다.

## PARTITION BY

`PARTITION BY`는 결과 집합을 논리적 그룹(파티션)으로 분할합니다. 윈도우 함수는 각 파티션 내에서 독립적으로 계산됩니다.

- `GROUP BY`와 유사하지만, **행을 축소하지 않고 모든 행을 유지**한 채로 그룹별 계산을 수행합니다.
- 여러 컬럼을 지정하면 해당 컬럼 조합으로 파티션이 나뉩니다.

```sql
-- sensor_id별로 파티션을 나누어 각 센서 내에서 순번 부여
SELECT
    sensor_id,
    time,
    value,
    ROW_NUMBER() OVER (PARTITION BY sensor_id ORDER BY time) AS rn
FROM sensor_data;
```

### PARTITION BY 생략

`PARTITION BY`를 생략하면 전체 결과 집합이 하나의 윈도우가 됩니다.

```sql
-- 전체 결과를 하나의 파티션으로 처리
SELECT
    time,
    value,
    RANK() OVER (ORDER BY value DESC) AS overall_rank
FROM sensor_data;
```

## ORDER BY (OVER 절 내)

`OVER` 절 내의 `ORDER BY`는 윈도우 내에서 행의 처리 순서를 결정합니다. 일반 쿼리의 `ORDER BY`와는 별개이며, 최종 출력 순서에는 영향을 주지 않습니다.

- `LAG`, `LEAD`, `RANK`, `ROW_NUMBER` 등 순서에 의존하는 함수에서는 필수입니다.
- `NTILE`도 버킷 할당 순서를 결정하기 위해 `ORDER BY`가 필요합니다.

```sql
-- OVER 내 ORDER BY: 윈도우 내 순서 결정
-- 쿼리 끝의 ORDER BY: 최종 출력 순서 결정
SELECT
    sensor_id,
    time,
    value,
    ROW_NUMBER() OVER (PARTITION BY sensor_id ORDER BY time ASC) AS rn  -- 윈도우 내 순서
FROM sensor_data
ORDER BY sensor_id, time;  -- 출력 순서
```

### ORDER BY 생략

순서가 필요 없는 함수(예: `SUM`, `AVG` 등 집계 윈도우 함수)에서는 `ORDER BY`를 생략할 수 있습니다.

```sql
-- 각 sensor_id 파티션의 평균을 모든 행에 함께 표시
SELECT
    sensor_id,
    time,
    value,
    AVG(value) OVER (PARTITION BY sensor_id) AS partition_avg
FROM sensor_data;
```

> `LAG`, `LEAD`, `RANK`, `ROW_NUMBER`, `NTILE` 함수에서 `ORDER BY`를 생략하면 오류가 발생하거나 결과가 불확정적일 수 있습니다.

## PARTITION BY와 ORDER BY의 조합

### 둘 다 사용 (가장 일반적)

파티션별로 나누어 정렬된 순서로 계산합니다.

```sql
SELECT
    tag_name,
    time,
    value,
    LAG(value, 1, NULL) OVER (
        PARTITION BY tag_name   -- 태그별로 독립 계산
        ORDER BY time ASC       -- 시간 오름차순으로 이전 값 참조
    ) AS prev_value,
    ROW_NUMBER() OVER (
        PARTITION BY tag_name
        ORDER BY time ASC
    ) AS seq_in_tag
FROM tag_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

### PARTITION BY만 사용

전체 집계를 파티션별로 계산할 때 사용합니다.

```sql
-- 각 행에 해당 sensor_id의 전체 평균을 나란히 표시
SELECT
    sensor_id,
    time,
    value,
    AVG(value)   OVER (PARTITION BY sensor_id) AS sensor_avg,
    MAX(value)   OVER (PARTITION BY sensor_id) AS sensor_max,
    MIN(value)   OVER (PARTITION BY sensor_id) AS sensor_min
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01');
```

### ORDER BY만 사용

전체 결과 집합에서 순서 기반 계산을 수행합니다.

```sql
-- 전체 데이터에서 시간 순서로 누적 순번 부여
SELECT
    time,
    sensor_id,
    value,
    ROW_NUMBER() OVER (ORDER BY time ASC) AS global_seq
FROM sensor_data;
```

## 실전 예시: 복합 파티션

여러 컬럼의 조합으로 파티션을 구성하는 예시입니다.

```sql
-- 공장(plant_id)과 장비(device_id) 조합별로 측정 순번 및 이전 값 계산
SELECT
    plant_id,
    device_id,
    time,
    value,
    ROW_NUMBER() OVER (
        PARTITION BY plant_id, device_id
        ORDER BY time
    ) AS seq,
    LAG(value, 1, NULL) OVER (
        PARTITION BY plant_id, device_id
        ORDER BY time
    ) AS prev_value
FROM equipment_sensor
WHERE time BETWEEN TO_DATE('2024-06-01') AND TO_DATE('2024-07-01');
```

> **팁**: 하나의 `SELECT` 문에서 `OVER` 절이 동일한 윈도우 함수를 여러 번 사용할 경우, 동일한 `OVER` 정의를 반복해서 작성해야 합니다. 쿼리가 복잡해지면 서브쿼리나 CTE(Common Table Expression)로 분리하면 가독성이 높아집니다.
