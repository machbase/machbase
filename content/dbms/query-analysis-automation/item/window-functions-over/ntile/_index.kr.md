---
type: docs
title: 'NTILE'
weight: 20
---

`NTILE(n)`은 결과 집합을 `n`개의 동등한 크기의 버킷으로 나누고, 각 행에 해당 버킷 번호를 부여하는 윈도우 함수입니다. 백분위수 계산, 사분위수 분석, 데이터 구간 분류 등에 활용합니다.

## 문법

```sql
NTILE(버킷_수) OVER (
    [PARTITION BY 파티션_컬럼]
    ORDER BY 정렬_컬럼
)
```

| 인자 | 설명 |
|------|------|
| `버킷_수` | 결과를 나눌 버킷의 수 (양의 정수) |

- 행 수가 `버킷_수`로 나누어 떨어지지 않으면, 앞쪽 버킷이 한 행씩 더 가집니다.
- 버킷 번호는 1부터 시작합니다.

> **ORDER BY는 필수입니다.** 버킷 할당은 지정된 순서에 따라 이루어지므로 반드시 `ORDER BY`를 명시해야 합니다.

## 예시

### 사분위수(Quartile) 분류

센서 측정값을 4개 구간으로 나누어 각 행에 사분위수 번호를 부여합니다.

```sql
SELECT
    time,
    sensor_id,
    value,
    NTILE(4) OVER (
        PARTITION BY sensor_id
        ORDER BY value
    ) AS quartile
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01');
```

결과에서 `quartile = 1`은 하위 25%, `quartile = 4`는 상위 25%에 해당하는 행입니다.

### 백분위수 버킷 할당

100개의 버킷으로 나누어 백분위수를 근사 계산합니다.

```sql
SELECT
    sensor_id,
    value,
    NTILE(100) OVER (
        PARTITION BY sensor_id
        ORDER BY value
    ) AS percentile_bucket
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01');
```

### 버킷별 통계 계산

외부 쿼리와 결합하여 각 사분위수 버킷의 평균과 최대/최소값을 구합니다.

```sql
SELECT
    sensor_id,
    quartile,
    COUNT(*)    AS row_count,
    MIN(value)  AS min_value,
    MAX(value)  AS max_value,
    AVG(value)  AS avg_value
FROM (
    SELECT
        sensor_id,
        value,
        NTILE(4) OVER (
            PARTITION BY sensor_id
            ORDER BY value
        ) AS quartile
    FROM sensor_data
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-02-01')
)
GROUP BY sensor_id, quartile
ORDER BY sensor_id, quartile;
```

## NTILE vs RANK 비교

`NTILE`과 `RANK` 계열 함수는 모두 순위와 관련이 있지만 목적이 다릅니다.

| 구분 | NTILE | RANK / DENSE_RANK |
|------|-------|-------------------|
| 목적 | 전체를 n개 버킷으로 균등 분할 | 개별 행의 상대적 순위 부여 |
| 동일 값 처리 | 동일 값이라도 다른 버킷에 배치될 수 있음 | 동일 값은 반드시 같은 순위 |
| 반환값 범위 | 1 ~ n (버킷 번호) | 1 ~ 전체 행 수 |
| 주요 용도 | 백분위수, 구간 분류 | 정확한 순위 계산 |

```sql
-- NTILE: 4개 버킷으로 균등 분할
NTILE(4) OVER (ORDER BY value)

-- RANK: 값 기준 순위 (동일 값 동일 순위, 다음 순위 건너뜀)
RANK() OVER (ORDER BY value)

-- DENSE_RANK: 값 기준 순위 (동일 값 동일 순위, 연속 순위)
DENSE_RANK() OVER (ORDER BY value)
```

> **주의**: 버킷 내에서 동일한 값을 가진 행들이 서로 다른 버킷에 나뉘어 배치될 수 있습니다. 정확히 동일 값을 같은 그룹으로 묶어야 할 경우에는 `RANK` 또는 `DENSE_RANK`를 사용하세요.
