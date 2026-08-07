---
type: docs
title: '18.1.1.8 window function / OVER'
weight: 80
toc: true
---

윈도우 함수(Window Function)는 결과 행을 그룹으로 축소하지 않고 각 행에 대해 집계 또는 순위 계산을 수행하는 함수입니다. `OVER()` 절을 사용해 계산 범위(윈도우)를 정의합니다.

## 문법

```sql
window_function([arg]) OVER (
    [PARTITION BY col1, col2, ...]
    [ORDER BY col [ASC | DESC]]
    [{ ROWS | RANGE } BETWEEN frame_start AND frame_end]
)
```

| 절 | 설명 |
|----|------|
| `PARTITION BY` | 윈도우를 분할할 컬럼 지정. 생략하면 전체 결과가 하나의 윈도우 |
| `ORDER BY` | 윈도우 내 행 정렬 순서 |
| `ROWS BETWEEN` | 행 기준 프레임 범위 지정 |
| `RANGE BETWEEN` | 값 기준 프레임 범위 지정 |

프레임 경계 표현:

| 표현 | 설명 |
|------|------|
| `UNBOUNDED PRECEDING` | 파티션 시작 |
| `n PRECEDING` | 현재 행에서 n행 이전 |
| `CURRENT ROW` | 현재 행 |
| `n FOLLOWING` | 현재 행에서 n행 이후 |
| `UNBOUNDED FOLLOWING` | 파티션 끝 |

## 지원 윈도우 함수

### 순위 함수

| 함수 | 설명 |
|------|------|
| `ROW_NUMBER()` | 각 파티션 내 행 번호 (1부터, 동일 값도 고유) |
| `RANK()` | 순위 (동일 값은 같은 순위, 다음 순위는 건너뜀) |
| `DENSE_RANK()` | 순위 (동일 값은 같은 순위, 다음 순위는 연속) |

### 이동 참조 함수

| 함수 | 설명 |
|------|------|
| `LAG(col, n)` | 현재 행에서 n행 이전 값 |
| `LEAD(col, n)` | 현재 행에서 n행 이후 값 |
| `FIRST_VALUE(col)` | 윈도우 프레임의 첫 번째 값 |
| `LAST_VALUE(col)` | 윈도우 프레임의 마지막 값 |

### 집계 윈도우 함수

| 함수 | 설명 |
|------|------|
| `SUM(col) OVER (...)` | 누적 합계 또는 이동 합계 |
| `AVG(col) OVER (...)` | 이동 평균 |
| `COUNT(*) OVER (...)` | 누적 건수 |
| `MIN(col) OVER (...)` | 이동 최솟값 |
| `MAX(col) OVER (...)` | 이동 최댓값 |

## 예시

### 순위 함수

```sql
-- TAG별 최근 값 순위
SELECT name, time, value,
       ROW_NUMBER() OVER (PARTITION BY name ORDER BY time DESC) AS rn
  FROM sensor_tag
 WHERE time >= TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- 최신 값 1건씩 추출
SELECT * FROM (
    SELECT name, time, value,
           ROW_NUMBER() OVER (PARTITION BY name ORDER BY time DESC) AS rn
      FROM sensor_tag
     WHERE time >= TO_DATE('2024-01-01', 'YYYY-MM-DD')
) WHERE rn = 1;
```

### LAG / LEAD: 이전/이후 값 비교

```sql
-- 직전 값과의 차이 계산
SELECT name, time, value,
       LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS prev_value,
       value - LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS delta
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2024-01-01', 'YYYY-MM-DD');
```

### 이동 평균

```sql
-- 3행 이동 평균
SELECT name, time, value,
       AVG(value) OVER (
           PARTITION BY name
           ORDER BY time
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS moving_avg_3
  FROM sensor_tag
 WHERE name = 'TEMP-01';
```

### 누적 합계

```sql
-- 파티션 전체 누적 합계
SELECT name, time, value,
       SUM(value) OVER (PARTITION BY name ORDER BY time
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_sum
  FROM sensor_tag
 WHERE name = 'TEMP-01';
```

## 성능 주의사항

윈도우 함수는 결과셋 전체를 메모리에 적재한 뒤 처리합니다. 대용량 데이터에 직접 적용하면 메모리 부족이나 응답 지연이 발생할 수 있습니다.

- 먼저 서브쿼리에서 시간 범위와 태그 이름으로 대상 행을 줄이십시오.
- 또는 ROLLUP이나 일반 GROUP BY 집계 후 윈도우 함수를 적용하십시오.

```sql
-- 권장: 집계 후 윈도우 함수 적용
SELECT name, bucket, avg_val,
       LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS prev_avg
  FROM (
      SELECT name,
             rollup('hour', 1, time) AS bucket,
             AVG(value)              AS avg_val
        FROM sensor_tag
       WHERE time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
                      AND TO_DATE('2024-07-01', 'YYYY-MM-DD')
       GROUP BY name, bucket
  ) t
 ORDER BY name, bucket;
```

## 관련 문서

- [PIVOT syntax](../pivot-syntax/) — 행을 열로 변환
- [SERIES BY syntax](../series-syntax/) — 연속 구간 추출
