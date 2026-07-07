---
type: docs
title: 'LAG / LEAD'
weight: 10
---

`LAG`와 `LEAD`는 현재 행을 기준으로 이전 또는 이후 행의 값을 참조하는 윈도우 함수입니다. 시계열 데이터에서 변화량(delta)을 계산하거나, 이전 측정값과 현재 측정값을 비교하는 데 유용합니다.

## 문법

```sql
LAG(컬럼, 오프셋) OVER (
    [PARTITION BY 파티션_컬럼]
    ORDER BY 정렬_컬럼
)

LEAD(컬럼, 오프셋) OVER (
    [PARTITION BY 파티션_컬럼]
    ORDER BY 정렬_컬럼
)
```

| 인자 | 설명 |
|------|------|
| `컬럼` | 참조할 컬럼 이름 |
| `오프셋` | 현재 행으로부터 몇 행 앞/뒤를 참조할지 지정 (기본값: 1) |

- **LAG**: 현재 행 기준 `오프셋`만큼 **이전** 행의 값을 반환합니다.
- **LEAD**: 현재 행 기준 `오프셋`만큼 **이후** 행의 값을 반환합니다.

> **ORDER BY는 필수입니다.** `LAG`/`LEAD`는 행의 순서에 의존하므로 `OVER` 절에 반드시 `ORDER BY`를 명시해야 합니다.

## 예시

### 이전 측정값과의 차이(변화량) 계산

센서 데이터에서 각 측정값이 직전 측정값과 얼마나 차이나는지 계산합니다.

```sql
SELECT
    time,
    sensor_id,
    value,
    LAG(value, 1) OVER (
        PARTITION BY sensor_id
        ORDER BY time
    ) AS prev_value,
    value - LAG(value, 1) OVER (
        PARTITION BY sensor_id
        ORDER BY time
    ) AS delta
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

### 1분 전 값과 현재 값 비교

```sql
SELECT
    time,
    tag_name,
    value AS current_value,
    LAG(value, 1) OVER (
        PARTITION BY tag_name
        ORDER BY time
    ) AS prev_1min_value
FROM tag_data
WHERE time BETWEEN TO_DATE('2024-06-01 00:00:00') AND TO_DATE('2024-06-01 01:00:00');
```

### 다음 행 값 참조 (LEAD)

```sql
SELECT
    time,
    sensor_id,
    value,
    LEAD(value, 1) OVER (
        PARTITION BY sensor_id
        ORDER BY time
    ) AS next_value
FROM sensor_data;
```

### 이상 감지: 이전 값 대비 급격한 변화 탐지

서브쿼리를 활용하여 직전 값 대비 일정 비율 이상 변화한 행만 필터링합니다.

```sql
SELECT *
FROM (
    SELECT
        time,
        sensor_id,
        value,
        LAG(value, 1) OVER (
            PARTITION BY sensor_id
            ORDER BY time
        ) AS prev_value
    FROM sensor_data
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
)
WHERE prev_value IS NOT NULL
  AND ABS(value - prev_value) / prev_value > 0.2;  -- 20% 이상 변화
```

## NULL 처리

오프셋이 범위를 벗어나는 경우(예: 첫 번째 행에서 LAG를 사용할 때) `NULL`이 반환됩니다.

```text
-- 첫 번째 행의 prev_value는 NULL로 반환됨
LAG(value, 1) OVER (ORDER BY time)
```

> **성능 고려사항**: `LAG`/`LEAD`는 내부적으로 데이터를 정렬한 후 처리합니다. 대용량 테이블에서는 쿼리 시간 범위를 제한하거나 `PARTITION BY` 조건을 적절히 지정하여 처리 대상 데이터를 줄이는 것을 권장합니다.
