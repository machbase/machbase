---
type: docs
title: 'EXPLAIN으로 실행 계획 확인'
weight: 90
---

`EXPLAIN`은 SELECT 쿼리의 실행 계획을 출력합니다. 데이터를 실제로 조회하지 않고 옵티마이저가 선택한 스캔 방식·인덱스 사용 여부를 확인할 수 있습니다.

## 구문

```sql
EXPLAIN SELECT ...;
```

## 예시

```sql
-- 인덱스 사용 확인
EXPLAIN SELECT sensor_id, value
FROM sensor_log
WHERE sensor_id = 'TEMP-01';
```

```
PLAN
-----------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:2, index id:4)
   [KEY RANGE]
    * sensor_id = 'TEMP-01'
```

```sql
-- 병렬 처리 힌트 적용 확인
EXPLAIN SELECT /*+ PARALLEL(sensor_log, 8) */ sensor_id, AVG(value)
FROM sensor_log
GROUP BY sensor_id;
```

```
PLAN
-----------------------------------------------------------
 PROJECT
  GROUP AGGREGATE
   PARALLEL INDEX SCAN
    *BITMAP RANGE (table id:3, column id:2, index id:4)
```

## 실행 계획 항목 설명

| 항목 | 설명 |
|------|------|
| `FULL SCAN` | 인덱스 없이 전체 테이블 스캔 |
| `INDEX SCAN` | 인덱스를 사용한 범위 스캔 |
| `PARALLEL INDEX SCAN` | 병렬 인덱스 스캔 |
| `BITMAP RANGE` | BITMAP 인덱스 범위 스캔 |
| `KEY RANGE` | 실제 적용된 인덱스 조건 |
| `FILTER` | 인덱스 적용 후 추가 필터 조건 |
| `GROUP AGGREGATE` | GROUP BY 집계 처리 |
| `PROJECT` | SELECT 대상 목록 처리 |

## 활용 팁

- `FULL SCAN`이 나타나면 WHERE 조건에 인덱스가 없는 것입니다. 인덱스를 추가하거나 힌트로 스캔 방향을 조정하세요.
- `DURATION`을 사용하면 `_ARRIVAL_TIME` 기준 파티션 가지치기가 적용되어 스캔 범위가 줄어듭니다.
- 대용량 테이블에서 느린 쿼리는 `EXPLAIN` 결과를 먼저 확인하세요.
