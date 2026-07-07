---
type: docs
title: '윈도우 함수와 PIVOT 성능 고려사항'
weight: 30
---

윈도우 함수와 PIVOT은 강력한 분석 도구이지만, 처리 방식에 따라 메모리와 응답 시간에 큰 영향을 줄 수 있습니다. 이 페이지에서는 대용량 데이터 환경에서 이 두 기능을 안전하게 사용하는 방법을 설명합니다.

## 윈도우 함수 성능 고려사항

### 전체 결과셋 메모리 적재

윈도우 함수(`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `SUM OVER` 등)는 결과셋 전체를 메모리에 적재한 뒤 처리합니다. 수백만 건의 원시 데이터에 직접 적용하면 메모리 부족이나 응답 지연이 발생할 수 있습니다.

```sql
-- 주의: 수백만 건에 직접 윈도우 함수 적용 → 메모리 부담
SELECT name, time, value,
       LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS prev_value
FROM   sensor_tag
WHERE  time BETWEEN '2025-01-01' AND '2025-06-30';  -- 6개월 전체 데이터
```

`MAX_QPX_MEM` 프로퍼티(기본값 0 = 무제한)로 단일 쿼리의 메모리 상한을 설정해 시스템 전체 영향을 제한할 수 있습니다.

```
# machbase.conf
MAX_QPX_MEM = 2147483648   # 2 GB
```

### 서브쿼리로 결과셋을 줄인 후 윈도우 함수 적용

윈도우 함수를 적용하기 전에 서브쿼리에서 집계 또는 범위 제한을 수행해 처리 대상 행 수를 줄입니다.

```sql
-- 권장: 서브쿼리에서 1시간 단위로 집계 후 윈도우 함수 적용
SELECT name, bucket,
       avg_val,
       LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS prev_avg,
       avg_val - LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS delta
FROM (
    -- 서브쿼리에서 대용량 → 소용량으로 집계
    SELECT name,
           rollup('hour', 1, time) AS bucket,
           AVG(value)              AS avg_val
    FROM   sensor_tag
    WHERE  time BETWEEN '2025-01-01' AND '2025-06-30'
    GROUP BY name, bucket
) t
ORDER BY name, bucket;
```

서브쿼리에서 수백만 건을 수천 건으로 줄인 뒤 윈도우 함수를 적용하면 메모리 사용량과 응답 시간이 크게 감소합니다.

### PARTITION BY 컬럼과 인덱스

PARTITION BY 컬럼에 인덱스가 있으면 데이터를 그룹별로 순차 처리해 GROUP BY와 유사한 최적화가 적용될 수 있습니다. 윈도우 함수를 자주 사용하는 컬럼(태그 이름, 센서 ID 등)에 인덱스를 생성하는 것을 고려하세요.

```sql
-- TAG 테이블: name 컬럼은 메모리 인덱스로 관리되어 PARTITION BY 효율적
SELECT name, time, value,
       ROW_NUMBER() OVER (PARTITION BY name ORDER BY time) AS rn
FROM   sensor_tag
WHERE  name IN ('TEMP-01', 'TEMP-02')
  AND  time BETWEEN '2025-06-01' AND '2025-06-02';
```

## PIVOT 성능 고려사항

### IN 목록 값 수와 컬럼 수

PIVOT의 IN 목록에 포함된 값 수만큼 결과 컬럼이 생성됩니다. 값 수가 많을수록 와이드 테이블이 되어 메모리 사용량과 처리 시간이 증가합니다.

```sql
-- 주의: IN 목록이 길면 결과 컬럼 수가 많아져 성능 저하
SELECT *
FROM (
    SELECT bucket, name, avg_val FROM agg_result
)
PIVOT (
    AVG(avg_val)
    FOR name IN (
        'SENSOR-001', 'SENSOR-002', 'SENSOR-003', ..., 'SENSOR-200'  -- 200개 컬럼
    )
);
```

**권장 사항:**
- IN 목록은 실제로 필요한 태그/값으로만 제한합니다. 불필요한 항목은 제거합니다.
- 태그 수가 수십 개를 초과하는 경우 PIVOT 대신 애플리케이션에서 행렬 변환을 수행하는 것을 검토합니다.

### 서브쿼리로 집계 후 PIVOT 적용

원시 데이터에 직접 PIVOT을 적용하면 내부에서 GROUP BY를 수행하므로 비용이 큽니다. 먼저 집계 서브쿼리를 수행하고 PIVOT을 적용하면 처리 대상 행 수가 줄어 성능이 향상됩니다.

```sql
-- 권장: 서브쿼리에서 집계 후 PIVOT
SELECT *
FROM (
    SELECT rollup('hour', 1, time) AS bucket,
           name,
           AVG(value)              AS avg_val
    FROM   sensor_tag
    WHERE  name IN ('TEMP-01', 'TEMP-02', 'PRESS-01')
      AND  time BETWEEN '2025-06-01' AND '2025-06-02'
    GROUP BY bucket, name
) t
PIVOT (
    AVG(avg_val)
    FOR name IN ('TEMP-01', 'TEMP-02', 'PRESS-01')
)
ORDER BY bucket;
```

ROLLUP 결과를 서브쿼리로 사용하면 원시 데이터 스캔 없이 집계된 값에만 PIVOT이 적용됩니다.

### PIVOT과 ROLLUP 조합

ROLLUP으로 사전 집계된 데이터를 PIVOT 입력으로 사용하면 최대 성능을 얻을 수 있습니다.

```sql
-- ROLLUP 집계 결과를 직접 PIVOT 입력으로 사용
SELECT *
FROM (
    SELECT rollup('min', 5, time) AS bucket,
           name,
           AVG(value)             AS avg_val
    FROM   sensor_tag
    WHERE  name IN ('TEMP-01', 'TEMP-02')
      AND  time BETWEEN '2025-06-01 00:00:00' AND '2025-06-01 06:00:00'
    GROUP BY bucket, name
) t
PIVOT (
    AVG(avg_val)
    FOR name IN ('TEMP-01', 'TEMP-02')
)
ORDER BY bucket;
```

## 요약: 패턴별 권장 접근법

| 상황 | 권장 접근법 |
|------|-------------|
| 수백만 건에 윈도우 함수 적용 | 서브쿼리에서 집계 후 윈도우 함수 적용 |
| PIVOT IN 목록이 수십 개 초과 | 필요한 항목만 선택, 또는 애플리케이션에서 처리 |
| 윈도우 함수 + 대용량 기간 | ROLLUP 집계 후 윈도우 함수 적용 |
| 메모리 부족 오류 | `MAX_QPX_MEM` 설정 검토, 기간 범위 축소 |
