---
type: docs
title: 'PIVOT'
weight: 40
---

PIVOT은 행(row) 방향의 데이터를 열(column) 방향으로 변환하는 연산입니다. 여러 센서의 측정값을 시간대별로 나란히 비교하거나, 코드 값을 컬럼 헤더로 표현할 때 활용합니다.

## 기본 문법

```sql
SELECT *
FROM (서브쿼리)
PIVOT (
    집계함수(값_컬럼)
    FOR 피벗_컬럼 IN ('값1' "alias1", '값2' "alias2", ...)
);
```

- **서브쿼리**: PIVOT 대상이 될 원본 데이터를 반환합니다. 일반적으로 피벗 기준 컬럼, 피벗 대상 컬럼, 값 컬럼을 포함합니다.
- **집계함수**: `AVG`, `SUM`, `MIN`, `MAX`, `COUNT` 등을 사용합니다.
- **FOR 피벗_컬럼 IN (...)**: 행 값을 열 이름으로 변환할 컬럼과 대상 값 목록을 지정합니다.

> **주의**: PIVOT의 열 목록(`IN` 절)은 쿼리 실행 시점에 정적으로 지정해야 합니다. 동적으로 열을 생성하는 기능은 지원되지 않으며, 열 이름은 미리 알고 있어야 합니다.

## 센서별 평균값 비교 예시

여러 센서의 평균값을 한 행으로 나란히 조회합니다.

```sql
-- 원본 데이터: (time, name, value) 형태의 TAG 테이블
SELECT *
FROM (
    SELECT
        DATE_TRUNC('hour', time) AS hour,
        name,
        value
    FROM tag
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
      AND name IN ('temp_01', 'temp_02', 'pressure_01')
)
PIVOT (
    AVG(value)
    FOR name IN (
        'temp_01'     "temp_01",
        'temp_02'     "temp_02",
        'pressure_01' "pressure_01"
    )
)
ORDER BY hour;
```

결과 예시:

| hour | temp_01 | temp_02 | pressure_01 |
|------|-----------|-----------|-----------|
| 2024-01-01 00:00 | 22.5 | 23.1 | 101.3 |
| 2024-01-01 01:00 | 22.8 | 23.4 | 101.5 |
| 2024-01-01 02:00 | 21.9 | 22.7 | 100.8 |

## 최대·최솟값 PIVOT

집계 함수를 바꾸면 동일한 구조로 최대·최솟값 비교도 가능합니다.

```sql
SELECT *
FROM (
    SELECT name, value
    FROM tag
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01')
      AND name IN ('sensor_A', 'sensor_B', 'sensor_C', 'sensor_D', 'sensor_E')
)
PIVOT (
    MAX(value)
    FOR name IN (
        'sensor_A' "A_MAX",
        'sensor_B' "B_MAX",
        'sensor_C' "C_MAX",
        'sensor_D' "D_MAX",
        'sensor_E' "E_MAX"
    )
);
```

## 상태 코드를 열로 변환하는 예시

숫자나 코드 값을 열로 펼쳐 각 상태별 발생 횟수를 비교할 수 있습니다.

```sql
SELECT *
FROM (
    SELECT factory, status_code
    FROM event_log
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01')
)
PIVOT (
    COUNT(*)
    FOR status_code IN (
        '0' "NORMAL",
        '1' "WARNING",
        '2' "ERROR",
        '3' "CRITICAL"
    )
)
ORDER BY factory;
```

## ROLLUP 결과를 PIVOT으로 변환

ROLLUP으로 시간 집계한 결과를 PIVOT으로 열 변환하면 시간대별 센서 비교 대시보드 데이터를 얻을 수 있습니다.

```sql
SELECT *
FROM (
    SELECT
        DATE_TRUNC('hour', time) AS hour,
        name,
        AVG(value) AS avg_val
    FROM tag
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
      AND name IN ('inlet_temp', 'outlet_temp', 'flow_rate')
    GROUP BY hour, name
)
PIVOT (
    AVG(avg_val)
    FOR name IN (
        'inlet_temp'  "inlet_temp",
        'outlet_temp' "outlet_temp",
        'flow_rate'   "flow_rate"
    )
)
ORDER BY hour;
```

## 활용 시 고려사항

| 항목 | 내용 |
|------|------|
| 열 목록 | 쿼리 작성 시 고정된 값 목록만 지원 |
| 집계 함수 | AVG, SUM, MIN, MAX, COUNT 사용 가능 |
| 결과 테이블 | 피벗 기준 컬럼 1개 + 지정한 값 수만큼의 열로 구성 |
| NULL 처리 | 해당 시간대에 데이터가 없으면 NULL로 채워짐 |

## 관련 항목

- [ROLLUP](../rollup/): 시간 축 기반 자동 집계
- [JOIN](../join/): 메타데이터와 결합하여 풍부한 컬럼 구성
- [집계 함수와 GROUP BY](../aggregation-group/): PIVOT 내부에 사용하는 집계 함수
