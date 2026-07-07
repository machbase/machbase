---
type: docs
title: '윈도우 함수 (OVER)'
weight: 50
---

윈도우 함수(Window Function)는 현재 행과 관련된 행 집합(윈도우)에 대해 계산을 수행하는 함수입니다. `GROUP BY`와 달리 결과 행을 그룹으로 축소하지 않고 모든 행을 유지한 채로 집계 또는 순위 연산을 수행할 수 있습니다.

## 지원 함수

현재 빌드에서 SQL `OVER` 절과 함께 사용할 수 있는 함수는 다음과 같습니다.

| 함수 | 설명 |
|------|------|
| `LAG(col, n)` | 현재 행 기준 n행 이전의 값을 반환 |
| `LEAD(col, n)` | 현재 행 기준 n행 이후의 값을 반환 |
| `NTILE(n)` | 결과 집합을 n개의 동등한 버킷으로 나누고 버킷 번호를 반환 |

## 기본 문법

```sql
함수() OVER (
    [PARTITION BY 파티션_컬럼, ...]
    [ORDER BY 정렬_컬럼 [ASC | DESC]]
)
```

- **PARTITION BY**: 윈도우 계산을 수행할 데이터 그룹을 정의합니다. 생략하면 전체 결과 집합이 하나의 윈도우가 됩니다.
- **ORDER BY**: 윈도우 내에서 행의 순서를 결정합니다. `LAG`, `LEAD`, `NTILE`처럼 순서가 중요한 함수에서 사용합니다.

## 사용 예시

### 이전 행과의 비교 (LAG)

```sql
SELECT
    time,
    value,
    LAG(value, 1) OVER (PARTITION BY sensor_id ORDER BY time) AS prev_value,
    value - LAG(value, 1) OVER (PARTITION BY sensor_id ORDER BY time) AS delta
FROM sensor_data;
```

### 버킷 번호 부여 (NTILE)

```sql
SELECT
    NTILE(4) OVER (PARTITION BY tag_name ORDER BY value) AS bucket_no,
    tag_name,
    time,
    value
FROM tag_data
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

### 다음 행 참조 (LEAD)

```sql
SELECT
    sensor_id,
    time,
    value,
    LEAD(value, 1) OVER (PARTITION BY sensor_id ORDER BY time) AS next_value
FROM sensor_data;
```

## 지원 테이블 유형

윈도우 함수는 Machbase의 주요 테이블 유형 모두에서 사용할 수 있습니다.

| 테이블 유형 | 지원 여부 |
|------------|----------|
| LOG 테이블 | 지원 |
| RDB 테이블 | 지원 |
| VOLATILE 테이블 | 지원 |
| TAG 테이블 | 지원 (시간 범위 조건과 함께 사용 권장) |

## 주의사항

> **윈도우 함수는 WHERE 절에서 직접 사용할 수 없습니다.**
> 윈도우 함수의 결과를 필터링하려면 서브쿼리를 사용해야 합니다.

```sql
-- 잘못된 예시 (오류 발생)
SELECT * FROM sensor_data
WHERE LAG(value, 1) OVER (ORDER BY time) IS NOT NULL;

-- 올바른 예시 (서브쿼리 사용)
SELECT * FROM (
    SELECT
        time, value,
        LAG(value, 1) OVER (ORDER BY time) AS prev_value
    FROM sensor_data
)
WHERE prev_value IS NOT NULL;
```

> **성능 고려사항**: 윈도우 함수는 내부적으로 정렬을 수행하므로 대용량 데이터에서는 적절한 시간 범위 조건을 함께 사용하는 것을 권장합니다.

## 하위 문서

- [LAG / LEAD](./lag-lead/): 이전/다음 행 값 참조
- [NTILE](./ntile/): 결과를 n개 버킷으로 분할
- [PARTITION BY / ORDER BY](./partition-order/): 윈도우 정의 방법
